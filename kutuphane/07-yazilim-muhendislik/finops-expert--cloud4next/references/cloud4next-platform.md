# Cloud4Next FinOps Intelligence — data model & where each answer lives

**Code-verified as of: 2026-09-07**, against `release/int` (core, fe, collector, orchestration)
and `develop` (ai, feeder). This file is the one place in this skill whose facts came from
reading the repository rather than from general knowledge. Code moves — re-check a table or
endpoint name before building on it.

## Pipeline

```
Cloud APIs ─▶ unified-collector (Go, single binary)
                 └─▶ Kafka  topic: finops.<provider>.raw
                        └─▶ ClickHouse  kafka_*_raw ─▶ typed per-provider tables ─▶ all_* unified
K8s cluster ─▶ feeder/oc-agent (Prometheus + OpenCost, outbound only) ─▶ ingest (Bearer JWT) ─▶ Kafka
ClickHouse ─▶ core (.NET 9 REST API) ─▶ fe (Vue 3)
ClickHouse ─▶ ai (Python/Prefect: anomaly, RCA, forecast) ─▶ Postgres ─▶ core
```

ClickHouse database: `finops_intelligence`. Schema lives in
`finops-intelligence-collector/setup/clickhouse/` — 145 numbered `.sql` migrations, applied in
filename order. The collector README's architecture section is **stale** (it describes a retired
OpenSearch/Data Prepper pipeline) and says so at the top; trust the SQL, not that README.

## Unified inventory: the `all_*` tables

The hard part of multi-cloud FinOps — one row shape across three providers — is done here.
Each `all_<entity>` table is fed by per-provider materialized views named
`mv_all_<entity>_<provider>`, plus an `all_<entity>_snapshot` variant.

| Table | AWS | GCP | Azure |
|---|:--:|:--:|:--:|
| `all_instances` · `all_disks` · `all_buckets` | ✔ | ✔ | ✔ |
| `all_managed_dbs` · `all_unmanaged_dbs` · `all_clusters` | ✔ | ✔ | ✔ |
| `all_functions` · `all_load_balancers` · `all_vpcs` | ✔ | ✔ | ✔ |
| `all_ips` · `all_firewalls` · `all_network_interfaces` | ✔ | ✔ | ✔ |
| `all_recommendations` | ✔ | ✔ | ✔ |
| `all_iam_principals` / `_policies` / `_bindings` / `_group_memberships` | ✘ | ✔ | ✘ |

**IAM is the only gap** — GCP-only (`103-gcp-iam-inventory-mv.sql`). Any governance answer that
spans identity is effectively single-cloud today; say so rather than implying parity.

Canonical shape (`all_instances`, `077-all-instances.sql`):

```
organization_id String · cloud_provider LowCardinality(String) · provider_id Nullable(String)
instance_id String · instance_name · region · zone · instance_type · state
vcpu_count Nullable(UInt16) · memory_capacity_gb Nullable(Float64)
timestamp DateTime · created_at DateTime · raw_data String · document_id String

ENGINE = ReplacingMergeTree(timestamp)
PARTITION BY (organization_id, toYYYYMM(timestamp))
ORDER BY (organization_id, cloud_provider, instance_id, timestamp)
```

Two consequences you must respect when querying:

- **ReplacingMergeTree deduplicates lazily.** Without `FINAL` (or an explicit
  `argMax`/`LIMIT 1 BY` pattern) you can read several versions of the same resource. Every
  "how many instances do we have" query needs a de-duplication strategy, not a bare `COUNT(*)`.
- **`organization_id` leads every ORDER BY and PARTITION.** Queries that omit it scan
  everything. It is also the tenant boundary — never write a cross-org query without an explicit
  reason, and note that the AI service has a `scope_gate` for exactly this.

`raw_data` keeps the untouched provider payload on every row, so a field that was never mapped
into a typed column is still recoverable without re-collecting.

## Billing and cost

- **AWS:** CUR-derived. `131-01-aws-billing-dedup-table.sql` (dedup), `110-03-aws-invoices-mv.sql`,
  `105-aws-billing-usd-cost.sql`, `142-02-aws-invoice-winner-views.sql`. Billing upload path also
  exists in core (`BillingUploadsController` + `BillingUploadService`/`Storage`/`ConflictService`/
  `CapacityGate`).
- **GCP:** BigQuery billing export. Requires **both** `billing_dataset_id` and `billing_table_id`
  in the provider config. ⚠ If `billing_table_id` is empty the collector still builds the query
  and BigQuery returns `Invalid empty identifier` (HTTP 400) hourly, writing zero rows — and the
  error appears **only in the collector log**, never in the UI. A tenant showing $0 with healthy
  inventory is this bug until proven otherwise.
- **Azure:** cost export; currency/FX handled separately (`139-01/02/03-azure-currency-fx-*`).
  The Azure plugin explicitly anticipates **FOCUS-shaped exports** and warns that column names
  differ there (`x_`-prefixed Azure-specific fields) — see `plugins/azure/billing_export_currency.go`.
- **Kubernetes:** `090-k8s-opencost-from-raw.sql` turns OpenCost allocation into cost rows.

## Pricing — asymmetric, and this shapes what you can answer

| Provider | What exists | What it is |
|---|---|---|
| GCP | `gcp_sku_events`, `compute_pricing_noregions` (019), Cloud SQL pricing (034), billing machine specs (073) | A real **SKU catalog** — list prices per region/machine family, including for resources you do not run |
| AWS | `aws_cur_unit_prices` (062/063) — `cpu_unit_cost_per_vcpu_hour`, `ram_unit_cost_per_gb_hour`, `pv_unit_cost_per_gb_hour`, `network_unit_cost_per_gb`; MV `REFRESH EVERY 15 MINUTE` | **Observed effective unit prices derived from your own CUR**, per org/account/period. Not a catalog |
| Azure | nothing but FX | No price catalog at all |

**The rule this implies:** you can price what a tenant already runs; you cannot price what they
do not. Any "what would this cost on X" question is unanswerable for Azure, and for AWS only in
the four unit dimensions above. Say this instead of producing a number that looks authoritative.

Instance specs (`002-instance-type-specs.sql`) are **hardcoded INSERT lists** of common types
for `aws_instance_type_specs` and `azure_vm_size_specs` (GCP machine types in 003). They silently
age as new families ship — treat a missing type as "unknown", never as "no vCPU".

## AI service — anomaly, RCA, forecast

Repo `finops-intelligence-ai` (Python 3.11 + Prefect 2). Reads ClickHouse, writes Postgres,
serves REST + a `/chat-blocks` natural-language assistant.

| Area | Modules | Schedule |
|---|---|---|
| Anomaly | `flows/{cost,ops,billing}_anomaly_flow.py`, `ml/{anomaly_detector,billing_anomaly}.py` (Isolation Forest) | ops 30 min · cost 1 h |
| RCA | `flows/rca_flow.py`, `ml/{rca,rca_causality,rca_events}.py` — **deterministic, no LLM** | 1 h |
| Forecast | `flows/{cost,ops,org_billing}_forecast_flow.py`, `ml/{chronos_predictor,forecaster}.py` (Chronos-2) | ops 2 h · cost 12 h · billing 4 h |
| Explainability | `flows/xai_flow.py`, `ml/xai_service.py` | |
| Assistant | `agent/{agent_intent_parser,agent_query_planner,agent_query_executor,agent_tool_engine,blocks_builder,scope_gate,org_tz}.py`, `rag/` | on demand |

`forecasts` table holds 30 d hourly + 90 d 3-hourly horizons; **no horizon beyond 90 days**.

**Org-total forecasting is a special case worth knowing.** Resource-level series exclude
unmapped, tax and support line items, which made org totals systematically low. `queries/org_billing.sql`
unions the three billing tables hourly, **gross** (credits not deducted), broken down by account
(`provider_id`), with synthetic `inventory_id = __total__:<CURRENCY>` so multiple currencies in one
account stay separate series. Azure exports daily, so its daily amount is spread evenly over 24 h
(totals tie exactly). Gated by `MetricConfig.forecast_only` — the cost anomaly flow does **not**
run this series.

⚠ The AI service is **not in the Helm chart**: deployed via its own `podman-compose.int.yaml` and
reached at a hardcoded address (`forecastApiBaseUrl` in `values-int.yaml`). When it is
unreachable, anomaly surfaces return empty rather than stale — core applies per-request timeout
caps (KPI 5 s, org-alerts 15 s, chat 300 s).

## Where a FinOps question lands in `core` (.NET 9)

`BudgetsController` (+ `.Labels`, `BudgetRecipientsController`, `BudgetPlanEstimateService`) ·
`AnomaliesController` / `AnomalyRulesController` / `AnomalyStatesController` ·
`CostAnalyticsController` · `ForecastController` · `DashboardController` ·
`CommitmentsController` · `RecommendationStatesController` (accept/dismiss workflow over
`all_recommendations`) · `InventoryAlertRulesController` · `DispatchController` (email) ·
`ExportRenderController` (queued PDF via `export_jobs`; PNG deliberately disabled) ·
`BillingUploadsController` · `AuditLogsController`.

Frontend is feature-based (`fe/src/features/`), not view-based: `costs`, `planning`
(budgets/forecast/anomaly rules), `optimization` (rightsizing, idle, commitments, kubernetes),
`governance` (tag policies, contact channels), `reporting`, `overview`, `finbot`, `ti`.

## Known gaps — do not promise these

1. **No pricing catalog for Azure**, and AWS pricing is CUR-derived only (above).
2. **No sync-health surface.** Collector failures are invisible to users; `core` has only a
   generic `HealthController`.
3. **Commitments are half-built.** CUR-based coverage works; utilization, missed-savings and
   Azure/GCP coverage need collector plugins that do not exist yet.
4. **`all_recommendations` is a passthrough** of native advisors (Compute Optimizer / GCP
   Recommender / Azure Advisor) — per-resource, single-cloud. There is no cross-cloud or
   architecture-level recommendation engine.
5. **No K8s pod rightsizing.** OpenCost data is in ClickHouse; the percentile analysis is unwritten.
6. **Module entitlements fall back to a mock fixture** in the frontend; Stripe is not configured
   (`SubscriptionController` reports `configured: false`).
