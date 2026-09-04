# RAG, Agents & Context Engineering (verified July 2026)

Contents: 1. Context engineering · 2. RAG pipeline design · 3. RAG variants ·
4. Long context vs RAG · 5. Agent design · 6. MCP & tool design · 7. Memory ·
8. Reliability patterns

---

## 1. Context engineering (the frame that replaced "prompt engineering")

The unit of design is the whole context window, not the prompt string:
system instructions + tool definitions + retrieved knowledge + memory +
conversation/trajectory history. Principles:

- Context is a budget. Every token competes; irrelevant context actively
  degrades output ("context rot" — quality decays as windows fill with
  stale tool logs). Curate, don't dump.
- Static-first ordering (system prompt, tools, few-shots before variable
  content) to maximize prefix-cache hits — a cost lever, not just hygiene.
- **Compaction**: summarize/prune old trajectory turns past a threshold;
  keep decisions and open state, drop raw tool dumps.
- **Sub-agents as context isolation**: spawn a worker with a clean, scoped
  context for a subtask; return only the distilled result to the parent.
  This — not anthropomorphic "teams" — is the real reason multi-agent
  patterns work.
- Few-shot examples remain the highest-leverage instruction tool; 2–5
  curated, diverse examples of the *exact* output you want.

## 2. RAG pipeline design (default recipe)

Ingest: parse → chunk (start ~400–800 tokens, respect structural boundaries —
headings, functions; add doc-level metadata) → embed → index.

Retrieve: **hybrid** = BM25/keyword + dense vector, fused (RRF), then a
**reranker** (cross-encoder) over top-50 → top-5–10. Hybrid+rerank over pure
vector search is the single biggest quality jump in most RAG systems; exact
IDs/codes/names are where pure dense retrieval fails.

Generate: cited answers ("answer only from context; cite chunk IDs; say
'not found' when absent") — citations enable eval and trust.

Query side: rewrite conversational queries into standalone search queries;
decompose multi-part questions; HyDE (embed a hypothetical answer) when
queries and docs differ in register.

Embeddings: pick by MTEB-class retrieval scores *on your language(s)* —
multilingual quality varies wildly (matters for Turkish); dimension/cost
trade-off; keep the embedding model versioned — changing it means reindexing.
Vector store: pgvector for existing-Postgres shops; Qdrant/Milvus/Weaviate
purpose-built; FAISS for embedded/local.

## 3. RAG variants (when the default recipe fails)

- **Agentic RAG** — retrieval as a tool in a loop: model searches, reads,
  refines query, searches again. Beats single-shot retrieval for multi-hop
  questions; costs latency. The default for agent products now.
- **GraphRAG** — extract entities/relations into a graph; retrieve
  subgraphs/community summaries. Justified when questions are relational
  ("who connects A to B", org-wide rollups); expensive to build/maintain —
  don't lead with it.
- **Contextual chunk augmentation** — prepend an LLM-written doc-context
  line to each chunk before embedding; cheap, meaningfully lifts retrieval.
- Parent-child retrieval (embed small chunks, feed larger parents to the
  model), late-interaction/ColBERT-style for high-recall needs.

## 4. Long context vs RAG

1M-token usable contexts (DeepSeek V4-class, Gemini) shrink but don't kill
RAG: (a) corpora exceed any window; (b) cost — reprocessing megatokens per
query vs retrieving 5k; (c) attention quality still degrades with distance
even in models tuned against it. Practical split: session-scale material
(a repo, a case file, a long doc set) → stuff into context and rely on
prefix caching; org-scale corpora, freshness, permissions → RAG. Hybrid:
retrieve generously (50–100 chunks), let the model filter.

## 5. Agent design

An agent = model + tools + loop (act → observe → act) toward a goal.
Design order:

1. **Don't build an agent if a workflow works.** Fixed pipelines (prompt
   chains, routers) are cheaper, faster, debuggable. Agents earn their cost
   only on open-ended tasks where the path is unknowable upfront.
2. Single agent + good tools first; multi-agent only for context isolation
   (§1) or parallelizable subtasks.
3. The loop: plan lightly, act, verify. Verification (run the tests, check
   the diff, re-read the output) is what separates working agents from
   demos.
4. Budget/guardrails: max steps, max cost, timeouts, allow-listed tools,
   human confirmation on irreversible actions (send/delete/pay).
5. Trajectory logging from day one — you cannot improve what you can't
   replay (see evaluation.md).

## 6. MCP & tool design

**MCP (Model Context Protocol)** is the de-facto standard for exposing
tools/data to models — adopted across major vendors and clients; design
integrations as MCP servers to be client-agnostic.

Tool design rules (bigger quality lever than model choice in agent systems):
few, well-named tools > many overlapping ones; descriptions written like docs
for a junior engineer (when to use, when NOT to, edge cases); return
*distilled* results, not raw dumps (a 50k-token JSON blob poisons the
context); make errors instructive strings the model can act on; idempotent
where possible; structured outputs via schema/constrained decoding rather
than free-text parsing.

## 7. Memory

Layers, cheapest first: (1) conversation window; (2) session compaction
summaries; (3) persistent store — files/notes or a vector/graph store the
model reads and writes via tools. Write policy matters more than storage
tech: store stable facts, decisions, preferences; skip transient state;
namespace per user/project; let the model retrieve at need instead of
injecting everything (context budget, §1).

## 8. Reliability patterns

- Structured output everywhere at boundaries (JSON schema / grammar-
  constrained decoding).
- Retries with modified context (append the error, not just resend).
- Fallback chains across models/providers via gateway.
- Prompt-injection posture: treat all retrieved/tool content as untrusted
  data, never as instructions; sandbox tool side effects; confirm
  destructive actions with the human.
- Cache aggressively (prefix cache + response cache for idempotent asks).
- Version prompts/tools/indexes like code; every change through the eval
  harness (evaluation.md).
