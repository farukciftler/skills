# Feature Engineering

Where competitions are won. Work in hypothesis-driven batches, validate on frozen folds, and record every result.

---

## 1. The catalogue

### Numeric transforms
- Ratios and differences between related columns (`amount / balance`, `price - median_price`) — trees cannot construct ratios themselves, so this is real added information.
- Log / sqrt / Box-Cox for skew (helps linear and NN, rarely trees).
- Binning + interaction of bins (discretization can expose non-monotonic effects).
- Rank / quantile transforms (`rankgauss`) — very effective for NN inputs.
- Row-wise statistics across a group of related columns: mean, std, min, max, count of zeros, count of NaNs, argmax.
- Rounding/precision features: number of decimal places, whether a value is a round number (surprisingly predictive on financial and human-entered data).

### Categorical
- Frequency/count encoding (leak-free, cheap, strong).
- Out-of-fold target encoding with smoothing (see `tabular-modeling.md`).
- Category combinations: concatenate pairs/triples of categoricals into a new categorical, then frequency- or target-encode it. This is the "feature engineering at scale" pattern used by grandmasters — generate all pairs programmatically and let CV select.
- Rare-level collapsing: map levels with count < k to `"__rare__"`.
- Per-category statistics of a numeric column (see aggregations).

### Aggregations (the highest-value family for entity-level data)
For each group key (customer, session, product, day) and each numeric column:
`mean, std, min, max, median, sum, count, nunique, last, first, range (max-min), skew`
Then the **relative** features that actually carry the signal:
- `value - group_mean`, `value / group_mean`, `(value - group_mean) / group_std` (z-score within group)
- rank of the row within its group
- deviation from the group's previous value

Multi-level: aggregate by customer, by customer×month, by product category — then combine.

### Temporal
- Calendar parts: year, month, day, dayofweek, hour, minute, week-of-year, is_weekend, is_month_start/end, is_holiday.
- **Cyclical encoding**: `sin(2π·hour/24)`, `cos(2π·hour/24)` — for NNs and linear models; trees don't need it.
- Deltas: time since previous event, time until next event, time since first/last event for this entity.
- Lags and leads (respecting the prediction horizon!), rolling mean/std/min/max over multiple windows (3, 7, 28, 90), expanding statistics, exponentially weighted means.
- Trend features: slope of the last k points, ratio of recent window mean to long window mean.
- **Discipline**: every temporal feature must be computable with information available strictly before the prediction time. Verify by recomputing a feature for a row using only its past.

### Text
- Classic and still strong: TF-IDF (word 1-2 grams + char 3-5 grams) → SVD (100-300 comps) → GBDT.
- Cheap statistics: length, word count, unique word ratio, punctuation/uppercase/digit counts, average word length, stopword ratio.
- Embeddings: sentence-transformers (`all-MiniLM-L6-v2`, `bge-small`) run fine on MPS and give strong dense features; reduce with SVD/UMAP before feeding a GBDT.
- Fine-tuned transformer OOF predictions as a *feature* for the GBDT is the standard strong hybrid.

### Interaction and target-derived
- Explicit pairwise arithmetic on the top-k important numeric features (`a*b`, `a/b`, `a-b`). Generate systematically, filter by CV.
- OOF predictions from a different model family as a feature (this is stacking; keep it leak-free).
- Nearest-neighbour features: distance to the k nearest training points, mean target of the k nearest neighbours (computed out-of-fold) — strong when local structure matters.
- Cluster features: KMeans cluster id + distance to each centroid (fit inside the fold).

### Domain and external
- Read the discussion forum: domain features shared publicly are worth more than any tuning.
- External data (if rules allow): weather, holidays, macro indicators, geocoding. Verify alignment and licence; declare it as required by the rules.

---

## 2. Generating features at scale

The winning pattern is *generate broadly, select by validation*:

```python
# all pairwise categorical combinations
new_cols = {}
for i, c1 in enumerate(CATS[:-1]):
    for c2 in CATS[i + 1:]:
        combo = df[c1].astype(str) + "_" + df[c2].astype(str)
        new_cols[f"{c1}__{c2}_freq"] = combo.map(combo.value_counts())
df = pd.concat([df, pd.DataFrame(new_cols, index=df.index)], axis=1)
```

Notes for 16 GB:
- Build new columns in a dict and `pd.concat` **once** — repeated `df[col] = ...` fragments memory and is slow.
- Prefer **Polars** for group-by heavy aggregation pipelines: it is multi-threaded, lazily optimized, and often 5-10× less memory than pandas. Convert to pandas only at the model boundary (`df.to_pandas()`), or feed LightGBM directly from numpy.
- Downcast: `float64 → float32`, `int64 → int32/16/8` (see `scripts/mem_utils.py`). Halves memory with no accuracy cost for GBDTs.
- Cache each feature batch to parquet so a kernel restart is cheap.

---

## 3. Feature selection that doesn't lie

Order of preference:
1. **Null importance / target permutation** — train with a shuffled target N times; keep features whose real importance exceeds e.g. the 95th percentile of the null distribution. Robust, catches noise features that gain-importance loves.
2. **Forward/greedy selection on CV** — expensive but honest; feasible here with LightGBM on subsampled data. This is what level-2 stacking models use.
3. **Permutation importance on validation** — decent, but correlated features share credit and both look useless.
4. **Recursive feature elimination** — slow, and drops correlated groups arbitrarily.
5. **Correlation pruning** — drop one of any pair with |ρ| > 0.99; safe and cheap as a first pass.

Avoid: selecting by importance computed on the whole dataset, then reporting the improved CV. That is selection leakage and it inflates CV by a lot.

**Practical note**: GBDTs tolerate many irrelevant features surprisingly well. Aggressive selection often costs more than it gains — the main reasons to select are speed, memory, and reducing drift-prone features flagged by adversarial validation.

---

## 4. Drift-aware feature engineering

Cross-check every new feature batch against adversarial validation. A feature with high CV gain *and* high adversarial importance is a trap: it fits train-specific structure that won't exist in test. Prefer the version of the feature that is stationary (e.g. use "days since the entity's first event" instead of an absolute timestamp; use a within-group rank instead of a raw counter).

---

## 5. Knowing when to stop

Stop feature engineering when:
- three consecutive hypothesis batches produce no gain beyond fold-std, **and**
- feature-importance mass is concentrated in features you already understand, **and**
- ensembling experiments start producing bigger gains than feature experiments.

Then move to ensembling, and revisit FE only if a new insight arrives from the forum or from error analysis.

---

## 6. Error analysis drives the next batch

Don't guess the next feature — look at the residuals:
- Sort OOF errors descending; inspect the worst 200 rows. What do they share?
- Compare the metric across slices (category levels, time periods, group sizes). A bad slice suggests a missing feature for that regime.
- Plot residual vs each important feature — structure in the residual is an un-modelled interaction, i.e. a feature waiting to be built.
- For classification, look at confidently-wrong predictions specifically; they usually reveal either label noise or a missing signal.
