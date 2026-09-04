# Storage, Databases & Analytics on AWS vs Azure vs GCP — Expert Reference

**Verified as of: 2026-08-28.** Prices are list, on-demand, USD, for **us-east-1 (AWS) / East US (Azure) / us-central1 (GCP)** unless noted. Anything not re-checked against a primary source this month is marked "~approx, verify". Main sources: aws.amazon.com pricing pages (S3, EBS, EFS/FSx, Aurora/RDS, DynamoDB, ElastiCache, Redshift, Kinesis/Firehose/MSK, AWS Backup), azure.microsoft.com pricing (Blob, Managed Disks, Files/NetApp Files, Azure SQL, Cosmos DB, Managed Redis, Fabric, Event Hubs, Backup), cloud.google.com pricing (GCS, Hyperdisk/PD, Filestore/NetApp Volumes, Cloud SQL/AlloyDB/Spanner, Firestore/Bigtable, Memorystore, BigQuery, Pub/Sub, Backup and DR), plus AWS What's New / Azure Updates / GCP release notes for 2024–2026 launches (S3 Express price cut Apr 2025, DynamoDB cut Nov 2024, Aurora DSQL GA May 2025, Azure Managed Redis GA May 2025, Firestore-MongoDB GA Aug 2025, GCS Rapid Storage 2025–26, Redshift Serverless 4-RPU minimum May 2026).

---

## 1. Object Storage: S3 vs Azure Blob vs GCS

### Tier mapping and per-GB pricing (LRS / regional, first-tier rates)

| Intent | AWS S3 | $/GB-mo | Azure Blob (LRS) | $/GB-mo | GCS (regional) | $/GB-mo |
|---|---|---|---|---|---|---|
| Hot | Standard | $0.023 (→$0.022 >50TB, $0.021 >500TB) | Hot | $0.018 (tiered down ~$0.0166) | Standard | $0.020 |
| Hot, low-latency | **S3 Express One Zone** | $0.11 | Premium block blob | ~$0.15 (~approx, verify) | **Rapid Bucket (zonal)** | per-GB-**hour**, zone-priced (~approx, verify) |
| Warm / IA | Standard-IA | $0.0125 | Cool | $0.010 | Nearline | $0.010 |
| Warm, 1 zone | One Zone-IA | $0.010 | (no direct equiv; ZRS is a redundancy option, not a discount tier) | — | (none) | — |
| Cold, ms access | Glacier Instant Retrieval | $0.004 | Cold | $0.0045 | Coldline | $0.004 |
| Cold, async | Glacier Flexible Retrieval | $0.0036 | Archive (rehydrate) | $0.00099 | Archive (ms access!) | $0.0012 |
| Deep archive | Glacier Deep Archive | $0.00099 | Archive | $0.00099 | Archive | $0.0012 |
| Auto-tiering | Intelligent-Tiering ($0.0025/1k obj monitoring, no retrieval fees) | — | Lifecycle + last-access-time tiering (no managed equivalent of INT) | — | Autoclass ($0.0025/1k obj/mo, retrieval fees waived) | — |

Key structural differences:
- **Azure Archive and GCS Archive/Coldline are online-ish**: GCS Archive/Coldline serve reads in **milliseconds** (same API, just retrieval fees); Azure Archive requires **rehydration (up to 15h standard, ~1h high-priority)**; S3 Glacier Flexible/Deep require restore jobs (expedited 1–5 min / standard 3–5h / bulk 5–12h; Deep: 12h standard, 48h bulk). Glacier **Instant** Retrieval is S3's ms-latency archive answer.
- **Minimum storage durations**: S3 — IA/One-Zone 30d, Glacier IR + Flexible 90d, Deep Archive 180d. Azure — Cool 30d, Cold 90d, Archive 180d. GCS — Standard 0, Nearline 30d, Coldline 90d, Archive **365d**. Early deletion bills the remainder.
- **Minimum billable object size**: S3 IA classes 128KB; Azure Cool/Cold/Archive 128KiB; GCS has none (advantage for small objects in cold tiers).
- **Retrieval fees ($/GB)**: S3 Standard-IA $0.01, Glacier IR $0.03, Flexible: standard $0.01 / bulk free / expedited $0.03; Deep: $0.02 standard / $0.0025 bulk. Azure: Cool $0.01, Cold $0.03, Archive $0.022 (+high-priority premium) (~approx, verify). GCS: Nearline $0.01, Coldline $0.02, Archive $0.05.
- **Requests** (per 1k): S3 Standard PUT $0.005 / GET $0.0004; IA $0.01/$0.001; Glacier IR $0.02/$0.01 (~approx, verify). Azure Hot write ~$0.0055 / read ~$0.00044 per 1k; archive read ops are expensive (rehydration billed per op). GCS Class A (writes/lists) $0.005/1k Standard, $0.01 Nearline/Coldline, $0.05 Archive; Class B (reads) $0.0004/1k Standard.
- **Lifecycle**: all three support age/prefix/tag(S3)/last-access(Azure, GCS Autoclass) transitions and expiry; S3 lifecycle transition requests are billed per 1k objects (Glacier transitions $0.03–0.05/1k, ~approx, verify) — a classic bill-shock item when transitioning millions of small objects.

### 2024–2026 additions
- **S3 Express One Zone** (directory buckets, single-AZ, single-digit-ms, session auth): after the **April 2025 cut** — storage $0.16→**$0.11/GB-mo** (−31%), PUT −55% (~$0.00113/1k), GET −85% (~$0.00003/1k), per-GB bandwidth charges −60% and now applied to all bytes (upload ~$0.0032/GB, retrieval ~$0.0006/GB, ~approx, verify). Use for ML training, low-latency analytics shuffle, high-TPS small objects.
- **S3 Tables** (re:Invent 2024, GA 2025): first-party **Apache Iceberg** table buckets — built-in compaction, snapshot management, Iceberg REST catalog, SageMaker Lakehouse/Glue/Athena/EMR integration. Storage ~$0.0265/GB-mo (≈15% premium over Standard) + request pricing + compaction ($/GB processed + per-object; ~approx, verify).
- **S3 Metadata** (re:Invent 2024, expanded 2025): auto-maintained Iceberg tables — a **journal table** (change log, ~$0.30/M updates, ~approx, verify) and **live inventory table** (free <1B objects; $0.10/M objects/mo above). Queryable via Athena/any Iceberg engine.
- **Azure**: Cold tier (GA 2023) filled the Cool↔Archive gap; **ADLS Gen2 = hierarchical namespace (HNS) flag on Blob** — real directories, POSIX ACLs, atomic renames; required for serious Spark/Hadoop workloads and OneLake interop. Premium block blob = SSD-backed, no retrieval fees, cheap transactions — for high-TPS small-object workloads.
- **GCS**: **hierarchical namespace buckets** (GA 2024 — atomic folder renames, higher initial QPS, needed for AI/analytics); **Anywhere Cache** — SSD read cache co-located with compute zone (now folded into "**Cloud Storage Rapid**" branding: **Rapid Bucket** = zonal HNS bucket, sub-ms latency, up to 20M QPS / 15 TB/s, per-GB-hour pricing; **Rapid Cache** ≈ renamed Anywhere Cache, ~2.5 TB/s read bursts). This is GCP's answer to S3 Express One Zone.
- **Consistency**: all three now offer **strong read-after-write consistency including list operations** (S3 since Dec 2020; GCS and Azure long-standing). Caveat: Azure RA-GRS/RA-GZRS secondary endpoint is **eventually consistent**; GCS multi-region/dual-region default replication is async (RPO minutes; **turbo replication** on dual-region gives 15-min RPO SLA at ~$0.04/GB, ~approx, verify).
- **Redundancy model difference (interview classic)**: S3 Standard is always ≥3-AZ (One Zone classes excepted). Azure makes redundancy an explicit knob — LRS / ZRS / GRS / GZRS / RA-* — GRS ≈ 2× LRS price. GCS makes location the knob — regional / dual-region / multi-region (multi-region Standard $0.026/GB).

---

## 2. Block Storage: EBS vs Managed Disks vs Hyperdisk/PD

All three converged on the **gp3 model**: pay for capacity + independently provisioned IOPS + throughput.

| | AWS gp3 | AWS io2 Block Express | Azure Premium SSD v2 | Azure Ultra Disk | GCP Hyperdisk Balanced | GCP Hyperdisk Extreme |
|---|---|---|---|---|---|---|
| $/GB-mo | $0.08 | $0.125 | ~$0.081–0.095 (billed hourly/GiB) (~approx, verify) | ~$0.12 (~approx, verify) | ~$0.084–0.096 (~approx, verify) | ~$0.125 (~approx, verify) |
| Free baseline | 3,000 IOPS + 125 MB/s | none | 3,000 IOPS + 125 MB/s | none | 3,000 IOPS + 140 MB/s (~approx) | none |
| Extra IOPS | $0.005/IOPS-mo | $0.065 first 32k, $0.046 to 64k, $0.032 above (tiered) | ~$0.005–0.006/IOPS-mo | per-IOPS rate | ~$0.005/IOPS-mo | ~$0.032/IOPS-mo |
| Extra throughput | $0.04/MBps-mo | included | ~$0.041–0.048/MBps-mo | per-MBps rate | ~$0.041/MBps-mo | included |
| Max per volume | 16k IOPS / 1,000 MB/s | 256k IOPS / 4,000 MB/s | 80k IOPS / 1,200 MB/s | 160k+ IOPS (400k on select VM/NVMe combos, ~approx, verify) | ~160k IOPS | 350k IOPS |
| Durability | 99.8–99.9% | **99.999%** | n/a (SLA via VM) | n/a | built on Colossus | — |

Notes that matter:
- **gp3 vs gp2**: gp3 is ~20% cheaper and decouples IOPS from size (gp2 = 3 IOPS/GB coupling). No reason to run gp2 in 2026.
- **Azure Premium SSD (v1)** still exists with **fixed-size tiers** (P10/P20/P30… bundled IOPS) — the legacy coupled model; **Premium SSD v2** is the gp3 analog but historically had restrictions (no OS disk, limited region/zone coverage, no classic VM-image support — re-verify current limits). **Ultra Disk** = io2 analog, sub-ms, per-IOPS/MBps billed hourly.
- **GCP Hyperdisk** (Balanced / Extreme / Throughput / Balanced HA / ML) has replaced Persistent Disk for current-gen machine families (C3/C4/N4…): decoupled provisioning, **Hyperdisk Storage Pools** (thin-provisioned capacity/IOPS pooling — unique among the three), Hyperdisk ML (read-only multi-attach at very high throughput for model weights). Legacy **PD**: pd-standard $0.04, pd-balanced $0.10, pd-ssd $0.17/GB-mo (bundled perf scaling with size).
- Anchor comparison, 1 TB @ 20k IOPS: io2 BX ≈ $1,400/mo; Ultra ≈ $1,200/mo; Hyperdisk Extreme ≈ $770/mo (~approx, verify) — GCP is aggressive at high IOPS; AWS gp3 wins the commodity mid-range ($80 + 17k×$0.005 = ~$165).
- All three bill **provisioned, not used**, capacity. Snapshots: EBS $0.05/GB-mo (archive tier $0.0125), Azure snapshot ~$0.05/GB, GCP standard snapshot $0.05/GB-mo with cheaper **archive snapshots** and instant snapshots (~approx, verify).

---

## 3. File Storage

| Need | AWS | Azure | GCP |
|---|---|---|---|
| General NFS | **EFS** — elastic, serverless, NFSv4; Standard $0.30/GB-mo, IA $0.016, **Archive $0.008**; One Zone ~half; Elastic throughput billed per GB transferred (~$0.03/GB read, $0.06/GB write, ~approx, verify) | **Azure Files** (NFS on premium only) | **Filestore** Basic HDD ~$0.16 / Basic SSD ~$0.30 / Zonal / Enterprise (regional) ~$0.60/GiB-mo (~approx, verify) |
| General SMB | FSx for Windows File Server (SSD ~$0.13/GB + throughput ~$2.20/MBps-mo, ~approx, verify) — AD-integrated, DFS | **Azure Files SMB** — HDD pay-as-you-go (Hot ~$0.024/GB used) or **Provisioned v2** (GA Nov 2024: provision GiB+IOPS+throughput separately, HDD and SSD); Premium SSD ~$0.16/GiB provisioned; **Azure File Sync** for hybrid | Filestore (SMB not native — use NetApp Volumes) |
| HPC / scratch | **FSx for Lustre** — persistent SSD $0.145–0.60/GB-mo by throughput tier (125–1000 MB/s per TiB); scratch cheaper; S3-linked (lazy hydration); **Intelligent-Tiering option (2024)** brings $/GB down ~10x for cold data (~approx, verify) | Azure Managed Lustre | Parallelstore (DAOS-based) + Hyperdisk ML |
| NetApp ONTAP (multiprotocol, SnapMirror, FlexClone, cross-cloud DR) | **FSx for NetApp ONTAP** — SSD $0.125/GB-mo + provisioned SSD IOPS + throughput capacity + capacity-pool tier $0.025/GB-mo; 2nd-gen file systems scale to multi-GB/s | **Azure NetApp Files** — Standard ~$0.147 / Premium ~$0.294 / Ultra ~$0.39/GiB-mo, 4TiB minimum capacity pool (1TiB with Flexible ~$0.11/GiB + separate throughput) (~approx, verify) | **Google Cloud NetApp Volumes** — Flex/Standard/Premium/Extreme service levels, ~$0.20–0.40/GiB-mo provisioned (~approx, verify) |
| ZFS semantics | FSx for OpenZFS (~$0.09/GB SSD + throughput, snapshots/clones, ~approx, verify) | — | — |

Structural notes: EFS is the only truly **elastic** (pay-for-use) file system of the majors; Azure Files Provisioned v2 and Filestore/ANF are provisioned models. ANF requires capacity-pool minimums (cost floor ~$600+/mo) but delivers the best latency profile on Azure; it's the default for SAP on Azure. FSx ONTAP is the de facto answer for VMware/enterprise NAS migrations on AWS.

---

## 4. Relational Databases

### Service mapping

| | AWS | Azure | GCP |
|---|---|---|---|
| Vanilla managed engines | **RDS**: MySQL, PostgreSQL, MariaDB, SQL Server, Oracle, **Db2** | Azure SQL Database / SQL MI; **Azure Database for PostgreSQL / MySQL Flexible Server** (Single Server retired Mar 2025) | **Cloud SQL**: MySQL, PostgreSQL, SQL Server |
| Cloud-native premium engine | **Aurora** (MySQL/PG) | **Azure SQL Hyperscale**; (**Azure HorizonDB** — scale-out Postgres announced at Ignite Nov 2025, preview — verify GA status) | **AlloyDB** (PG) |
| Serverless relational | Aurora Serverless v2 | Azure SQL serverless (GP + Hyperscale) | (Cloud SQL has no serverless; AlloyDB has none — closest is autoscaled read pools) |
| Distributed SQL | **Aurora DSQL** (GA May 2025) | Cosmos DB for PostgreSQL (Citus) — check status; HorizonDB | **Spanner** |
| Managed sharding | **Aurora Limitless** (PG; GA Oct 2024, still maintained through PG 16.x updates in 2025) | Hyperscale named replicas / elastic pools (not sharding); Citus | Spanner (native), AlloyDB (no) |

### Architectural differences (the consulting answer)
- **Aurora**: compute-storage separation; storage is a purpose-built distributed log — **6 copies across 3 AZs**, quorum 4/6 writes, only redo log shipped to storage (no full-page writes), up to 15 low-lag read replicas sharing the same storage volume, ~128–256 TiB max. Two billing modes: **Standard** (compute + $0.10/GB-mo storage + $0.20/M I/Os) vs **I/O-Optimized** (no I/O charges, ~+30% compute, $0.225/GB-mo storage) — I/O-Optimized wins when I/O >~25% of the bill. **Serverless v2**: 0.5-ACU granularity, ~$0.12/ACU-hr (Standard), **scales to zero** with auto-pause (Nov 2024), ~15s resume. **Global Database**: <1s cross-region replication, managed failover/switchover.
- **Aurora DSQL**: PostgreSQL-compatible **serverless distributed SQL**, active-active **multi-region strong consistency**, optimistic concurrency (OCC — no locks; retry on conflict), disaggregated architecture (compute/journal/storage), scales to zero. Pricing: **$8/M DPUs** + $0.33/GB-mo; free tier 100k DPU + 1GB/mo. GA **May 2025**. Trade-offs: no FKs at launch, transaction size/duration limits, subset of PG features — verify current feature list.
- **Azure SQL Database**: **DTU** model (legacy blended units — Basic/S/P tiers; avoid for new builds) vs **vCore** (General Purpose / Business Critical / **Hyperscale**). **Hyperscale**: Aurora-style decoupled architecture — page servers + log service, up to 128 TB, fast scale-out via named replicas, snapshot-based near-instant backups/restores; Dec 2023 compute price cut made it ~$0.10/vCore-hr class (~approx, verify). **Serverless**: per-second vCore billing (~$0.000145/vCore-sec ≈ $0.52/vCore-hr, ~approx, verify) with auto-pause (GP). **Azure Hybrid Benefit** (BYO SQL licenses) is the big TCO lever nobody on AWS/GCP can match for SQL Server.
- **AlloyDB**: PG-compatible; disaggregated storage with a log-processing service; **in-memory columnar engine** auto-populated from row store (HTAP: 100x analytic claims); ML-driven adaptive autovacuum/memory; **AlloyDB Omni** runs the engine anywhere (on-prem/laptop/other clouds). ~2× Cloud SQL per-vCPU price, aimed at Oracle/enterprise-PG migrations.
- **Spanner**: globally distributed, synchronously replicated (Paxos), **external consistency (strictest: linearizable + serializable) via TrueTime** atomic-clock/GPS timestamps; horizontal scale-out with automatic splits; 99.999% multi-region SLA; relational + interleaved tables; PostgreSQL-dialect interface; also serves Cassandra- and (2025) MongoDB-compatible interfaces (~verify). Granular provisioning from **100 processing units (1/10 node)**; editions (Standard/Enterprise/Enterprise Plus, 2024) gate features like dual-region configs and advanced tiered storage.

### Small-production pricing anchors (2 vCPU class, single instance + HA where noted; ~approx, verify all)
- RDS PostgreSQL db.m7g.large single-AZ: ~$0.17/hr ≈ $125/mo + storage (gp3 $0.115/GB-mo); Multi-AZ ×2. Multi-AZ **DB cluster** (2 readable standbys) is a different, pricier product.
- Aurora PG db.r6g.large: ~$0.26/hr ≈ $190/mo per instance (add a reader for HA → ~$380) + storage/IO. Serverless v2 at steady 2 ACU ≈ $175/mo.
- Azure SQL GP 2-vCore provisioned: ~$370/mo license-included (much less with AHB); Hyperscale 2 vCore ≈ $150–190/mo + $0.10/GB storage (~approx, verify).
- Azure PG Flexible Server D2ds_v5: ~$130/mo + storage; zone-redundant HA ×2.
- Cloud SQL Enterprise PG 2 vCPU/8GB: ~$100–140/mo zonal; regional HA ×2; **Enterprise Plus** edition (+~30%) adds data cache, 99.99% SLA with near-zero-downtime maintenance.
- AlloyDB 2 vCPU/16GB: ~$350–400/mo regional (storage billed separately, pay-per-use).
- Spanner: 100 PU ≈ $0.09/hr ≈ $65/mo + $0.30/GB-mo — cheapest "real Spanner" footprint; a full node $0.90/hr ≈ $657/mo regional.

---

## 5. NoSQL Key-Value / Document

### DynamoDB vs Cosmos DB vs Firestore/Bigtable

**Pricing units (the core interview distinction):**
- **DynamoDB**: RCU/WCU (provisioned) or RRU/WRU (on-demand). 1 RCU = 1 strongly-consistent 4KB read/s (eventual = ½ price); 1 WCU = 1×1KB write/s. **Nov 2024: on-demand cut 50%, global tables up to 67%** → on-demand now **$0.625/M WRU and $0.125/M RRU** (~verify — post-cut list); provisioned $0.00065/WCU-hr, $0.00013/RCU-hr; storage $0.25/GB-mo (first 25GB free). On-demand is now the recommended default; provisioned+reserved only for very flat workloads.
- **Cosmos DB**: everything is **RU/s** (1 RU ≈ 1KB point read; writes ~5+ RU). Provisioned: ~$0.008/hr per 100 RU/s (≈$5.84/mo per 100 RU/s); **autoscale** = 1.5× rate but scales 10%–100% of max; **serverless** $0.25/M RU; storage $0.25/GB-mo. Throughput is provisioned per container or shared per database; free tier 1000 RU/s + 25GB.
- **Firestore**: per-operation — regional us-central1 roughly $0.033–0.06 per 100k reads, $0.18/100k writes (nam5 multi-region: $0.06/$0.18/$0.02 deletes), storage $0.18/GB-mo; real-time listeners and offline sync built in. **Firestore Enterprise edition (GA Aug 2025)** adds **MongoDB compatibility**, billed in tranche-based read/write units ($0.05/M 4KiB-read units, $0.26/M 1KiB-write units, ~approx, verify).
- **Bigtable**: node-based — **$0.65/node-hr** (+SSD $0.17/GB-mo, HDD ~$0.026); autoscaling; CUDs −20/−40%. Wide-column, single-digit-ms, linear scale; now with GoogleSQL support, and distributed counters (2024–25).

**Consistency & partitioning:**
- DynamoDB: partition-key hashing, adaptive capacity; strong consistency only within a region (option per-read); **Global Tables** historically last-writer-wins eventual — **multi-region strong consistency (MRSC) GA June 2025** for Global Tables (2-region+witness topology). 400KB item limit. DAX for microsecond caching. Streams/CDC, TTL, transactions (2× cost).
- Cosmos DB: logical partitions (20GB limit per logical partition — the classic gotcha), physical partitions of 10k RU/s; **five consistency levels** (strong, bounded staleness, session [default], consistent prefix, eventual); multi-region writes (LWW/custom conflict resolution); 99.999% read/write SLA multi-master; per-partition RU throughput can throttle hot partitions (429s) even when aggregate RU/s looks fine.
- Firestore: document/collection model, automatic scaling with **strong consistency** and real ACID transactions; historically 1 write/sec/document soft guidance and 10k writes/s/database limits lifted (now effectively no hard write ceiling — verify workload class).
- Bigtable: eventual consistency across replicated clusters (single-cluster routing for strong), single-row atomicity only.

**API surface:** Cosmos DB is multi-API (NoSQL/core, MongoDB RU + **MongoDB vCore**, Cassandra, Gremlin, Table, PostgreSQL/Citus — verify Gremlin/Cassandra roadmap status, Microsoft has been steering to NoSQL+vCore). DynamoDB is single-API (plus Keyspaces for Cassandra, Neptune for graph as separate services). GCP splits by workload: Firestore (docs/mobile), Bigtable (wide-column/throughput), Memorystore, Spanner.

**MongoDB options ranked:** (1) **MongoDB Atlas** — real MongoDB, runs on all three clouds, best compatibility, marketplace-billable; (2) **Cosmos DB for MongoDB vCore** — familiar $/vCore pricing, native Azure integration, decent 6.0/7.0 compat; (3) **Amazon DocumentDB** — Aurora-style storage, MongoDB **5.0 API-emulation** (compatibility gaps persist), instance-based ~$0.28/hr r6g.large + $0.10/GB-mo + I/O, **DocumentDB Serverless (GA Jan 2025, DCU-based, ~approx, verify)**, global clusters; (4) **Firestore w/ MongoDB compatibility** (GA Aug 2025) — serverless, strongly consistent, but an emulation layer too. Wildcard: Microsoft open-sourced **DocumentDB** (Postgres extension powering vCore Mongo) and moved it to the Linux Foundation (2025) — emerging open standard angle.

---

## 6. Caching

**Licensing backdrop (know this story):** Redis Ltd moved Redis OSS to RSALv2/SSPL (**March 2024**) → Linux Foundation **Valkey** fork (backed by AWS, Google, Oracle, Ericsson). Redis 8 later added **AGPLv3** (May 2025) — partially open again, but the clouds had already shipped Valkey. Result: AWS and GCP lead with Valkey; **Azure went the other way**, partnering with Redis Ltd to build **Azure Managed Redis** on Redis Enterprise.

- **AWS ElastiCache**: engines = Valkey, Redis OSS (7.x frozen), Memcached. **Valkey priced ~20% below Redis OSS node-based, ~33% below serverless.** Node anchor: cache.r7g.large Redis ~$0.226/hr, Valkey ~$0.18/hr (~approx, verify). **ElastiCache Serverless**: pay per GB-hr stored + per-M ECPUs; Valkey serverless minimum 100MB → **from ~$6/mo**. Database Savings Plans (Dec 2025) give up to 20–30% off. Valkey 8 engine: faster scaling, better memory efficiency.
- **Azure**: legacy **Azure Cache for Redis** (Basic/Standard/Premium on OSS 6; Enterprise tiers being retired — migration path is AMR; verify dates, Enterprise/Enterprise Flash retirement ~2027). **Azure Managed Redis (GA May 2025)**: Redis Enterprise under the hood — tiers Memory Optimized / Balanced / Compute Optimized / Flash Optimized, node-based (HA = 2 nodes), Redis 7.4+ features (JSON, search, time series), active geo-replication. Note community grumbling about 2026 price increases (~approx, verify current rate card). No serverless option.
- **GCP Memorystore**: **for Valkey** (GA 2024–25, cluster architecture, per-node billing, CUDs −20/−40%), for Redis Cluster, for Redis (standalone legacy), for Memcached. Valkey/Redis Cluster instances support zero-downtime scaling, replicas, persistence.

Rule of thumb: greenfield on AWS/GCP → Valkey (cheaper, drop-in, OSS-governed). Azure → AMR Balanced tier. If you need Redis Stack modules (search/JSON) managed on AWS/GCP, that's Redis Cloud (marketplace) or MemoryDB (AWS's durable Valkey/Redis with Multi-AZ WAL — separate service, ~2× ElastiCache price).

---

## 7. Data Warehouses / Lakehouse (the classic comparison)

### Architecture & pricing model in one table

| | Redshift | BigQuery | Synapse dedicated | Microsoft Fabric | Snowflake | Databricks |
|---|---|---|---|---|---|---|
| Model | Provisioned clusters (RA3 compute + managed storage) or Serverless (RPU) | **Fully serverless**; on-demand per-TiB scanned or capacity slots | Provisioned DWU blocks, pause/resume | **Unified capacity (CU)** — one F-SKU pool shared by ALL workloads | Virtual warehouses (T-shirt sizes) billed in credits/sec | Clusters/SQL warehouses billed in DBU + cloud VMs |
| Compute pricing | ra3.xlplus $1.086/hr, ra3.4xl $3.26/hr, ra3.16xl $13.04/hr; Serverless **$0.375/RPU-hr** (min lowered to **4 RPU May 2026** → $1.50/hr floor while active) | On-demand **$6.25/TiB scanned** (1 TiB/mo free); Editions per slot-hr: Standard $0.04 / Enterprise $0.06 / Ent Plus $0.10 (+1yr/3yr commit discounts) | ~$1.20/hr per DW100c (~approx, verify); serverless SQL $5/TB | **~$0.18/CU-hr PAYG**: F2 ≈ $263/mo, F64 ≈ $8,410/mo; ~41% off reserved; F64+ includes Power BI viewer rights | $2/$3/$4 per credit (Std/Ent/BC, AWS us-east on-demand); XS warehouse = 1 credit/hr | SQL Serverless ~$0.70/DBU; jobs/all-purpose cheaper/more (~approx, verify) |
| Storage | RMS $0.024/GB-mo (RA3/serverless) | Logical: active $0.02/GB-mo, long-term $0.01 (untouched 90d); optional **physical (compressed)** billing $0.04/$0.02 | included/attached | **OneLake $0.023/GB-mo** | ~$23/TB-mo on-demand (pass-through with compression) | your S3/ADLS/GCS (Delta) |
| Separation of storage/compute | Yes (RA3 onward) | Yes (Colossus + Dremel slots) | Partial | Yes (OneLake + capacity) | Yes | Yes |
| Scaling behavior | Concurrency scaling clusters; serverless auto-RPU; AI-driven optimization | Slots autoscale per-second (editions); on-demand ~2000-slot soft pool | Manual DWU resize | **Bursting + smoothing** (24h averaging) then **throttling/rejection** when capacity exhausted | Multi-cluster warehouses | Autoscaling clusters, serverless |

**The distinctions to articulate:**
- **BigQuery** is the only pure serverless-native: no clusters to size ever; risk is **unbounded on-demand scan costs** (mitigate: max-bytes-billed, partitioning/clustering, move hot teams to Editions slots). On-demand charges by **bytes scanned regardless of runtime**; slots charge by time regardless of bytes.
- **Redshift** kept the provisioned mental model; RA3 + managed storage decoupled it; Serverless (RPU) closes the gap but bills per-second **while queries run** with 60s minimums. Zero-ETL ingestion from Aurora/RDS/DynamoDB is its differentiator inside AWS. Spectrum queries S3 at $5/TB (bundled into serverless RPU).
- **Fabric's F-SKU capacity model is the one people get wrong**: you buy ONE capacity (F2…F2048); Power BI, Spark, Warehouse, Data Factory, Real-Time Intelligence, Copilot **all draw from the same CU pool**; usage is **smoothed over 24h** and can **burst** beyond purchased CU, but sustained overage → interactive-query throttling then rejection for the whole tenant capacity — noisy-neighbor risk across teams. Copilot/AI features require F64+ (F2+ since late 2024 for some — verify). Pay-as-you-go can pause; reservations (~−41%) cannot.
- **Synapse**: not formally retired (Microsoft says no retirement plan), but strategically frozen — Data Explorer retired Oct 2025, Synapse Link for Cosmos deprecated for new work (→ Fabric Mirroring), trusted-services network path change Aug 1 2026 breaks unmigrated workspaces, migration assistant for ADF/Synapse pipelines in preview (FabCon Mar 2026). Treat new builds on Synapse as malpractice; treat existing as migration-planning engagements.
- **Snowflake**: cross-cloud (AWS/Azure/GCP) with identical UX; per-second credit billing with 60s min; Gen2 warehouses / adaptive compute (2025) improve price-perf; strengths: zero-copy cloning, time travel, data sharing/marketplace; watch: storage is cheap, compute credits dominate.
- **Databricks**: lakehouse-first (Delta Lake; acquired Tabular/Iceberg founders in 2024 — Delta/Iceberg interop via UniForm); first-party service on Azure, marketplace on AWS/GCP; Photon engine; Unity Catalog governance; DBU + underlying VM cost = two-line-item bill.
- Open-table-format convergence: **Iceberg won neutrality** (S3 Tables, BigQuery Iceberg tables/BigLake, Snowflake Iceberg tables, Fabric OneLake shortcuts + Delta as native), Delta remains Databricks/Fabric native format.

---

## 8. Streaming & Messaging

| | AWS Kinesis Data Streams | Azure Event Hubs | GCP Pub/Sub |
|---|---|---|---|
| Model | Provisioned **shards** (1MB/s in, 2MB/s out each): $0.015/shard-hr + $0.014/M PUT-payload-units (25KB); **On-demand**: $0.04/stream-hr + $0.08/GB in + $0.04/GB out; **On-demand Advantage (Nov 2025)**: $0.032/GB in, $0.016/GB out (~approx, verify terms) | Capacity units: Basic $0.015/TU-hr; Standard $0.03/TU-hr + $0.028/M events (TU = 1MB/s in / 2MB/s out); Premium ~$1.23/PU-hr; Dedicated ~$6.85/CU-hr (~approx, verify) | Pure throughput: **$40/TiB** (each of publish, pull-delivery, push billed), first 10 GiB/mo free; no capacity to size |
| Kafka compat | MSK (separate) | **Kafka protocol endpoint built into Event Hubs** (Standard+) — huge migration lever | Managed Service for Apache Kafka (GA 2025) |
| Retention | 24h default, up to 365d (extra $/GB) | 1–7d Standard (90d Premium+) | 7d default, up to 31d; ack-based |
| Ordering | Per shard/partition key | Per partition | Per ordering key (optional) |
| Fan-out | Enhanced fan-out ($/consumer-shard-hr + $/GB); up to 50 EFO consumers (2025) | Consumer groups | Unlimited subscriptions; BigQuery/GCS subscriptions (direct sink, cheaper than Dataflow for plain loads) |

- **Firehose (Amazon Data Firehose)**: zero-admin delivery to S3/Redshift/OpenSearch/Snowflake/**Iceberg tables**; $0.029/GB (5KB rounding gotcha), volume tiers to $0.020.
- **Kafka managed**: **MSK provisioned** (per-broker-hr, e.g. kafka.m5.large ~$0.21/hr + EBS $0.10/GB-mo); **MSK Express brokers (Nov 2024)** — Kafka-API brokers with disaggregated, elastic storage (no EBS sizing, faster scaling/rebalancing; broker-hr + $/GB ingest ~$0.01, ~approx, verify) — AWS's answer to WarpStream-style economics; **MSK Serverless** ($0.75/cluster-hr + $0.0015/partition-hr + $0.10/GB in). **Confluent Cloud**: Basic/Standard/Enterprise (eCKU, elastic) / Dedicated (CKU) / **Freight** clusters (2024, S3-direct, high-throughput relaxed-latency, ~90% cheaper for logs/telemetry); bundles Schema Registry, ksqlDB/Flink, connectors — MSK is cheaper raw brokering, Confluent bundles the platform.
- **Pub/Sub Lite is retired (March 2026)** — do not propose it.
- Azure note: Event Hubs = ingestion/streaming; Service Bus = transactional messaging (queues/topics, sessions, DLQ); Event Grid = discrete events/CloudEvents routing (incl. MQTT). AWS analog split: Kinesis / SQS+SNS / EventBridge. GCP: Pub/Sub covers most of all three roles.

---

## 9. Backup / DR

- **AWS Backup**: policy-based, cross-service (EBS/RDS/Aurora/DynamoDB/EFS/FSx/S3/VMware/EC2). Billed per service: e.g. EFS warm $0.05/GB-mo, EFS cold $0.01, EBS snapshot $0.05, RDS snapshot $0.095, DynamoDB $0.10 + restore fees ($0.02/GB EFS warm etc.); **logically air-gapped vaults** (2024, ~$0.10/GB-mo, ~approx, verify) for ransomware isolation with cross-account restore. Cross-region copy = snapshot storage in target + inter-region transfer (~$0.02/GB between US regions).
- **Azure Backup**: **protected-instance fee + storage**. VM example: ~$10/mo per 500GB increment per VM + backup storage at LRS ~$0.0224/GB-mo, GRS ~$0.0448, ZRS between (~approx, verify); SQL/SAP HANA in VM ~$30/500GB instance fee. Vault-standard vs archive tier; soft delete, MUA, immutable vaults. Azure Site Recovery (DR orchestration) ~$25/mo per protected instance.
- **GCP Backup and DR**: backup vaults (immutable/indestructible option) — vault storage ~$0.10/GiB-mo single-region (~approx, verify) + standard snapshot pricing ($0.05/GB-mo, archive snapshots cheaper) for PD/VM snapshots.
- **Cross-region replication cost pattern (all clouds)**: destination storage + replication egress. S3 CRR: dest storage + $0.02/GB inter-region + replication PUTs (+ $0.015/GB for RTC 15-min SLA). Azure: GRS is baked into the redundancy SKU (≈2× LRS) with RPO ~15min, no separate egress line; blob object replication billed as ops + egress. GCS: dual-region/multi-region pricing includes default async replication; **turbo replication** adds ~$0.04/GB for 15-min RPO SLA. Egress remains the silent DR-test killer: full cross-region restore of 100TB ≈ $2k in transfer alone on AWS/Azure, more on GCP inter-continental.

---

## Cheat-sheet: cross-cloud equivalents

| Concept | AWS | Azure | GCP |
|---|---|---|---|
| Object | S3 | Blob (ADLS Gen2 = +HNS) | GCS |
| Low-latency object | S3 Express One Zone | Premium block blob | Rapid Bucket / Rapid (Anywhere) Cache |
| Managed Iceberg | S3 Tables | OneLake (Delta-native, Iceberg via shortcuts) | BigLake / BigQuery Iceberg tables |
| Block | EBS gp3 / io2 BX | Premium SSD v2 / Ultra | Hyperdisk Balanced / Extreme |
| NFS/SMB | EFS / FSx family | Azure Files / Azure NetApp Files | Filestore / NetApp Volumes |
| Managed RDBMS | RDS | Azure SQL DB, PG/MySQL Flexible | Cloud SQL |
| Cloud-native RDBMS | Aurora | SQL Hyperscale | AlloyDB |
| Distributed SQL | Aurora DSQL | (HorizonDB preview / Citus) | Spanner |
| KV/document NoSQL | DynamoDB | Cosmos DB | Firestore + Bigtable |
| Cache | ElastiCache (Valkey) | Azure Managed Redis | Memorystore (Valkey) |
| Warehouse | Redshift | Fabric (Synapse legacy) | BigQuery |
| Streams | Kinesis / MSK | Event Hubs | Pub/Sub / Managed Kafka |
| Backup | AWS Backup | Azure Backup | Backup and DR |

**Pricing-model one-liners worth memorizing:** S3/Blob/GCS ≈ price parity on hot storage ($0.018–0.023/GB) — differentiation is retrieval fees, min durations, and ops. Block storage: everyone copied gp3's decoupled capacity/IOPS/throughput. NoSQL units: RCU/WCU (throughput-provisioned per op size) vs RU/s (blended abstract capacity, per-partition) vs Firestore per-document ops. Warehouses: pay-per-scan (BigQuery on-demand) vs pay-per-slot-time (Editions/Redshift RPU/Snowflake credits) vs pay-per-shared-capacity (Fabric CU with smoothing/throttling). Streaming: capacity units (shards/TUs) vs pure per-GB (Pub/Sub, Kinesis on-demand).
