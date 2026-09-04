# AI & Makine Öğrenmesi

Kaggle/ML iş akışı, AutoML, LLM ve SLM mimarisi, GPU kaynak hibeleri.

8 skill. Üst dizin: [../../README.md](../../README.md)

## `ab-gpu-hibe-uzmani`

[SKILL.md](ab-gpu-hibe-uzmani/SKILL.md)

Avrupa Birliği'nin ücretsiz/desteklenmiş GPU ve süperbilgisayar kaynakları uzmanı — EuroHPC JU erişim çağrıları (Benchmark, Development, Regular, Extreme Scale, AI for Science), AI Factories (Playground/Fast Lane/Large Scale), AI Gigafactories, Grand Challenge yarışmaları, Horizon Europe/Digital Europe/EIC para hibeleri ve Türkiye uygunluğu (TÜBİTAK, TRUBA). Rota seçimi, GPU saati boyutlandırma, başvuru/proposal yazımı, cut-off takvimi, değerlendirme kriterleri, ret sonrası strateji ve üçüncü taraflara danışmanlık desteği verir. Kullanıcı "GPU hibesi", "ücretsiz GPU", "EuroHPC", "AI Factory", "LUMI/Leonardo/MareNostrum/JUPITER", "süperbilgisayar erişimi", "GPU saati", "compute grant", "AB'den kaynak" dediğinde; bir model eğitimi/fine-tune/inference için hesaplama kaynağı arandığında; ya da bir müşteriye bu konuda danışmanlık verilecekse bu skill'i kullan. Çağrı tarihlerini, kota ve kuralları ASLA ezberden verme — her seferinde canlı doğrula ve tarih damgası koy.

- **Ölçü:** 8.152 bayt · 4 ek dosya · referans dosyaları var
- **Kaynak:** claude.ai senkronu (efemer önbellek)

## `automl`

[SKILL.md](automl/SKILL.md)

Benchmarked cross-validated ensemble pipeline for tabular binary classification. Reads train.csv/test.csv/sample_submission.csv, trains LightGBM, XGBoost, CatBoost, HistGradientBoosting, ExtraTrees and logistic regression with stratified K-fold CV, blends them by out-of-fold rank hill-climbing, and writes a ready-to-submit CSV. Use it as the first modelling action on any tabular prediction task.

- **Ölçü:** 4.124 bayt · 1 ek dosya · script içerir
- **Kaynak:** ~/projects/autonomous-agent-prediction/submissions/03_hardened/agent/skills/automl

## `automl--autonomous-agent-prediction`

[SKILL.md](automl--autonomous-agent-prediction/SKILL.md)

Benchmarked cross-validated ensemble pipeline for tabular binary classification. Reads train.csv/test.csv/sample_submission.csv, trains LightGBM, XGBoost, CatBoost, HistGradientBoosting, ExtraTrees and logistic regression with stratified K-fold CV, blends them by out-of-fold rank hill-climbing, and writes a ready-to-submit CSV. Use it as the first modelling action on any tabular prediction task.

- **Ölçü:** 3.727 bayt · 1 ek dosya · script içerir
- **Kaynak:** ~/projects/autonomous-agent-prediction/submissions/01_baseline/agent/skills/automl

## `automl--autonomous-agent-prediction-3`

[SKILL.md](automl--autonomous-agent-prediction-3/SKILL.md)

Benchmarked cross-validated ensemble pipeline for tabular binary classification. Reads train.csv/test.csv/sample_submission.csv, trains LightGBM, XGBoost, CatBoost, HistGradientBoosting, ExtraTrees and logistic regression with stratified K-fold CV, blends them by out-of-fold rank hill-climbing, and writes a ready-to-submit CSV. Use it as the first modelling action on any tabular prediction task.

- **Ölçü:** 3.727 bayt · 1 ek dosya · script içerir
- **Kaynak:** ~/projects/autonomous-agent-prediction/submissions/02_gemini_fallback/agent/skills/automl

## `kaggle-kaggle-skill`

[SKILL.md](kaggle-kaggle-skill/SKILL.md)

Guides competitors in designing, authoring, validating, evaluating, debugging, and submitting autonomous ML agents to kaggle-kaggle competitions. Make sure to use this skill whenever the user mentions kaggle-kaggle, autonomous ML agents, building an agent submission, running local evaluation, debugging agent traces, or submitting to Kaggle, even if they don't explicitly ask for the competitor guide. Don't use for building the evaluation harness itself or for non-kaggle-kaggle competitions.

- **Ölçü:** 8.878 bayt · 6 ek dosya · script içerir
- **Kaynak:** ~/projects/autonomous-agent-prediction/kaggle-kaggle-skill

## `llm-engineering-expert`

[SKILL.md](llm-engineering-expert/SKILL.md)

- Act as a senior LLM engineering expert: model architectures (MoE, MLA, sparse/linear/hybrid attention), model selection, training and fine-tuning (SFT, DPO, GRPO/RLVR, LoRA/QLoRA), inference and deployment (vLLM, SGLang, Ollama, quantization, GPU/VRAM sizing), RAG and agent design, and evaluation. Use whenever the user asks anything substantive about LLMs: choosing a model ("hangi modeli kullanalım", open-weight vs API), self-hosting or local models ("yerel LLM", "kendi sunucumuzda"), GPU sizing ("kaç GB VRAM yeter"), fine-tuning or training ("fine-tune edelim", "kendi modelimizi eğitelim"), architecture concepts (MoE, attention, KV cache, context window, quantization, distillation), building RAG or agent pipelines, LLM cost estimation, or comparing models — even when phrased casually or in Turkish. Also use it when reviewing an LLM system design, estimating feasibility or cost of an LLM feature, or explaining how a specific released model works internally.

- **Ölçü:** 6.482 bayt · 5 ek dosya · referans dosyaları var
- **Kaynak:** claude.ai senkronu (efemer önbellek)

## `ml-expert`

[SKILL.md](ml-expert/SKILL.md)

Expert ML engineering workflow for Kaggle competitions and general machine learning projects on a MacBook Pro M2 Pro (10-core CPU / 16-core GPU / 16 GB unified memory). Use whenever the task involves competing on Kaggle, building or debugging an ML model, cross-validation design, feature engineering, GBDT (LightGBM/XGBoost/CatBoost), ensembling/stacking, hyperparameter tuning with Optuna, training neural nets locally with PyTorch MPS or MLX, handling datasets that strain 16 GB of RAM, or deciding when to move work off-laptop to a cloud GPU. Triggers: "kaggle", "competition", "leaderboard", "CV score", "feature engineering", "LightGBM", "XGBoost", "CatBoost", "stacking", "ensemble", "Optuna", "overfitting", "train a model", "MPS", "MLX", "out of memory".

- **Ölçü:** 12.314 bayt · 14 ek dosya · script içerir · referans dosyaları var
- **Kaynak:** ~/.claude/skills/ml-expert, ~/.gemini/config/plugins/kirkit-skills/.claude/skills/ml-expert, ~/.gemini/config/plugins/kirkit-skills/skills/ml-expert, ~/projects/kirkit/data/skills/skills/ml-expert

## `slm-architecture-lead`

[SKILL.md](slm-architecture-lead/SKILL.md)

- Answer as an SLM architecture engineering lead who has shipped Gemma- and Qwen-class 1-9B models: model design (depth/width, attention layout, SWA vs linear-hybrid vs Mamba, GQA/KV budgets, vocab/embedding trade-offs, PLE, MoE-for-edge), training (multi-stage pretraining, distillation, thinking mode, QAT), and on-device deployment. Use whenever the user asks about small or on-device models - "SLM", "küçük model", "4B", "8B", sub-10B, "telefonda çalışacak model", "edge LLM" - or about Gemma, Qwen, Phi, SmolLM, LFM2, Granite internals ("neden 5:1 sliding window", "why tied embeddings", "Gated DeltaNet nedir"), or wants to design, size, or review a small model config, compute params/KV-cache/memory from hyperparameters, pick a small base model to fine-tune or distill into, or understand tech-report design choices. Also trigger for quantization, MTP/speculative decoding, and mobile/NPU deployment of language models - even casually phrased or in Turkish.

- **Ölçü:** 8.730 bayt · 4 ek dosya · referans dosyaları var
- **Kaynak:** claude.ai senkronu (efemer önbellek)

