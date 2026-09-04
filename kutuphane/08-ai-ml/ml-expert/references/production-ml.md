# Production / Non-Competition ML

Competitions hand you a clean target, a fixed dataset, and a metric. Real projects hand you none of those, and that is where most projects fail — not in modeling.

---

## 1. Problem framing (do not skip)

Answer in writing before touching data:

1. **What decision does this model change?** If no decision changes, there is no project. "Understand our customers better" is not a decision.
2. **What is the prediction target, exactly?** Definition, unit, time horizon, and the moment of prediction.
3. **What is available at prediction time?** Draw the timeline: event → features observable → prediction → label observable. Anything to the right of the prediction point is leakage.
4. **What is the baseline being replaced?** A rule, a human, an old model, or nothing. The bar is that baseline's performance, not 0.
5. **What error is more expensive, FP or FN?** This sets the metric and the threshold, and it is a business answer, not a modeling one.
6. **What accuracy is enough to be useful?** If nobody can say, run a cost/benefit calculation: value per correct decision × volume vs cost per error.
7. **Constraints**: latency, throughput, interpretability/regulatory requirements, retraining cadence, privacy/PII rules.

Deliverable: a one-page project brief. It prevents the most expensive failure mode, which is building the wrong thing accurately.

---

## 2. Data work

- **Data contract**: for each source — owner, refresh cadence, schema, expected nulls, known quirks. Schema drift breaks more production models than concept drift.
- **Label quality audit**: manually inspect 100 labels. Label noise sets the ceiling on achievable performance, and delayed/partial labels invalidate naive validation.
- **Point-in-time correctness**: features must be reconstructed as they were at prediction time, not as they are now. Snapshot tables or an as-of join; a feature store solves this if the org has one.
- **Train/serve consistency**: the same transformation code must run in both paths. The classic production bug is training on a pandas pipeline and serving with a hand-rewritten one.
- **Sample size reality check**: <1k labeled rows → use a simple model, expect wide error bars, and prioritize collecting more data over tuning.

---

## 3. Delivery order

1. **Rules baseline** shipped end-to-end (data → prediction → the consuming system), even if crude.
2. **Simple model** (logistic regression / small GBDT) in the same pipeline.
3. Only then improve the model.

Getting the pipeline to production early surfaces the integration problems (latency, schema, permissions, monitoring) while there is still time to fix them. A notebook with 0.95 AUC that never ships is worth zero.

---

## 4. Evaluation that survives contact with reality

- **Backtest across multiple periods**, and report the worst period, not just the mean.
- **Slice metrics**: by segment, region, customer tier, rare class. Aggregate gains that hide a degraded key slice are not acceptable.
- **Business metric simulation**: translate the model score into the decision (threshold, ranking, budget allocation) and compute the business outcome — expected revenue, cost saved, alerts generated per day. Precision at the *operating volume* matters far more than AUC.
- **Alert-budget framing** for imbalanced problems: "at 100 investigations/day, we catch X% of fraud" is the number people can act on.
- **Fairness/impact check** where decisions affect people: metric parity across relevant groups, and documented rationale for the operating point.
- **A/B test or shadow deployment** before full rollout. Offline gains routinely fail to reproduce online — because of feedback loops, drift, or an implementation gap.

---

## 5. Monitoring after deployment

Log, from day one: input feature distributions, prediction distribution, latency, error rates, and (when they arrive) labels.

Watch for:
- **Data drift** — input distribution shifts. Detect with PSI/KS per feature, or run an adversarial classifier between training data and last week's traffic (same technique as competition adversarial validation).
- **Concept drift** — the relationship between features and target changes. Only visible once labels arrive; track rolling metric.
- **Prediction drift** — score distribution shifts even when inputs look stable; often the first sign of an upstream schema change.
- **Feedback loops** — the model's own decisions alter the future data (blocked transactions never produce labels). Reserve a small random control group so unbiased labels keep flowing.
- **Silent failures**: a feature pipeline returning nulls that get imputed to a plausible value. Alert on null rates and on out-of-range values, not just on the metric.

Define the **retraining trigger** in advance: scheduled cadence, or a metric/drift threshold. Automate the retrain-validate-deploy path, with a rollback.

---

## 6. Reproducibility and artifacts

- Version: code (git), data (hash/snapshot id or DVC), model (registry), and environment (lockfile).
- Track experiments with MLflow or Weights & Biases; even a CSV beats memory. Log params, metrics, artifacts, and the git SHA.
- **Model card** per deployed model: purpose, training data window, features, metrics overall and per slice, known limitations, owner, retraining policy, rollback procedure.
- Serialize with the training library's own format (`booster.save_model`, `torch.save`, ONNX for cross-runtime). Avoid raw pickle across library versions.

---

## 7. Serving notes

- **Batch scoring** covers most business use cases and is far simpler than a real-time service. Choose it unless latency genuinely requires otherwise.
- **Real-time**: FastAPI + the model in-process; cache features; measure p99, not the mean; keep a fallback (last known score, or the rules baseline) for when the model or feature store is unavailable.
- **Latency levers** for GBDTs: fewer trees, `max_bin` reduction, ONNX/Treelite compilation. For NNs: quantization, distillation, batching.
- **Idempotence and audit**: store the inputs and the score for every prediction. When someone disputes a decision six months later, this is what you need.

---

## 8. Common production failure modes

| Failure | Prevention |
|---|---|
| Train/serve skew | Shared transformation code; a test asserting identical outputs on the same input |
| Leakage from post-outcome features | Timeline diagram; point-in-time joins; review every feature's availability |
| Model trained on a period that no longer represents reality | Rolling retrains; drift monitoring |
| Optimizing a proxy metric that diverges from the goal | Pre-register the offline→online metric mapping |
| No owner after launch | Named owner + runbook in the model card |
| Threshold set once and never revisited | Recalibrate the operating point on each retrain |
| Great AUC, useless ranking at the top | Evaluate precision@k at the real operating volume |

---

## 9. What transfers from Kaggle — and what doesn't

**Transfers well**: validation discipline, leakage instincts, feature engineering craft, error analysis, ensembling for a genuine accuracy need, fast iteration habits.

**Does not transfer**: 15-model stacks for a 0.001 gain (maintenance cost is real), squeezing the metric while ignoring latency and interpretability, assuming the target definition is given, and assuming the data distribution is static.

The production instinct is the inverse of the competition instinct: **prefer the simplest model that clears the bar**, and spend the saved effort on data quality, monitoring, and the decision layer.
