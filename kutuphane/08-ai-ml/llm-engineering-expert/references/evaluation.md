# Evaluation (verified July 2026)

Contents: 1. Public benchmark map · 2. Reading benchmarks critically ·
3. Building your own evals · 4. LLM-as-judge · 5. RAG & agent evals ·
6. In production

---

## 1. Public benchmark map (what measures what)

- Coding: **SWE-bench Verified / Pro** (real-repo issue fixing — the
  headline agentic-coding number), LiveCodeBench (contamination-resistant,
  rolling), Terminal-Bench (shell agents).
- Reasoning/knowledge: **GPQA Diamond** (graduate science), AIME (competition
  math), **HLE** (Humanity's Last Exam — frontier-hard), MMLU-Pro (older,
  near-saturated), ARC-AGI-2 (abstraction).
- Agents/tool use: tau-bench (customer-service tool loops), OSWorld /
  computer-use suites, BrowseComp (web research).
- Long context: RULER, MRCR-style multi-needle — advertised window ≠ usable
  window; check these before trusting 1M claims.
- Human preference: LMArena Elo (vibes + style bias), plus task-specific
  arenas (WebDev, coding).
- Scores move quarterly — pull current numbers via web search before quoting
  (freshness protocol in SKILL.md).

## 2. Reading benchmarks critically

Contamination (test data in training sets) inflates static benchmarks —
prefer rolling/refreshed ones (LiveBench-style, LiveCodeBench). Saturated
benchmarks (MMLU-class) no longer discriminate at the top. Elo rewards
confident, well-formatted answers, not correctness. Vendor-reported numbers
use best-case scaffolds/budgets; independent reruns land lower. "Thinking"
scores depend heavily on token budget — compare at matched budgets. A 1–2
point gap is noise; buy on your own eval, not leaderboard deltas.

## 3. Building your own evals (the actual moat)

Public benchmarks pick a model *class*; only your eval picks a model for
your product.

1. **Golden set**: 50–200 real cases from your task (include hard/adversarial
   and "should refuse / should say not-found" cases). Version it; grow it
   from production failures.
2. **Graders**, most-deterministic-first: exact/normalized match →
   programmatic checks (schema validity, tests pass, constraint holds) →
   LLM-as-judge for fuzzy quality.
3. **Run matrix**: candidate models × your golden set, matched decoding
   params, ≥3 runs when sampling (report variance, not one lucky run).
4. **Regression gate**: every prompt/model/RAG-index change runs the eval in
   CI; block on score drops. Evals-as-tests is the discipline separating
   teams that improve from teams that thrash.

## 4. LLM-as-judge (do it properly or not at all)

- Rubric-based scoring with explicit criteria and few-shot anchor examples
  beats bare 1–10 ratings.
- Pairwise comparison (A vs B) is more reliable than absolute scores;
  **swap positions** and average (position bias is real); watch for
  self-preference (judge favoring its own family) and length bias — use a
  judge from a different family than candidates when possible.
- Use a strong model as judge; spot-check judge decisions with humans
  (~5–10%) and track agreement before trusting it at scale.

## 5. RAG & agent evals

RAG — evaluate the two stages separately:

- Retrieval: recall@k / MRR against labeled query→relevant-chunk pairs
  (build ~100; it's an afternoon of labeling, saves weeks of blind tuning).
  Most RAG failures are retrieval failures — check this first.
- Generation: faithfulness (claims supported by retrieved context — judge
  with citations), answer relevance, correct "not found" behavior (measures
  hallucination pressure).

Agents — evaluate trajectories, not just final answers: task success rate,
steps/cost per success, tool-error recovery, unsafe-action rate. Replayable
logged trajectories (rag-agents.md §5) are the dataset; grade with
programmatic end-state checks (did the ticket get filed? do the tests pass?)
plus judge review of the path.

## 6. In production

Online signals: thumbs/edit-rate/acceptance, task completion, escalation
rate, latency and cost per request. Sample production traffic into the
golden set weekly. Shadow-test new models/prompts on real traffic before
cutover; canary rollouts for model swaps. Alert on drift (score drop,
cost spike, refusal spike) — model providers silently update endpoints;
pin versions where offered.
