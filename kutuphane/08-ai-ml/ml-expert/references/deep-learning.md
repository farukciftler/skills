# Deep Learning on M2 Pro (and knowing when not to)

For images, text, audio, and structured-sequence problems. Everything here assumes 16 GB unified memory shared with the OS.

---

## 1. Decide first: local or cloud?

| Signal | Verdict |
|---|---|
| Model ≤ ~100M params, batch fits comfortably, epoch < ~20 min | Train locally on MPS/MLX |
| Fine-tuning a small encoder (DeBERTa-small/base, MiniLM, ModernBERT) on ≤50k short samples | Local, overnight |
| LoRA on a ≤3-8B LLM, 4-bit | Local with MLX (`mlx-lm lora`) |
| Full fine-tune of 7B+, large ViT/Swin at high resolution, diffusion training, multi-GPU | Cloud / Kaggle Notebooks |
| Submission must run in a Kaggle GPU notebook | Develop against that environment |
| Dataset > ~50 GB of images | Cloud (also an I/O problem, not just compute) |

Local is still valuable for these tasks even when training goes to the cloud: dataset construction, augmentation design, label auditing, inference/embedding extraction, and error analysis.

---

## 2. A training loop that behaves on MPS

```python
import os, torch, numpy as np, random
os.environ.setdefault("PYTORCH_ENABLE_MPS_FALLBACK", "1")

def seed_all(s=42):
    random.seed(s); np.random.seed(s); torch.manual_seed(s)
    if torch.backends.mps.is_available(): torch.mps.manual_seed(s)

device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
model = model.to(device)

loader = DataLoader(
    ds, batch_size=32, shuffle=True,
    num_workers=4,               # 2-4 on macOS; more costs memory via spawn
    persistent_workers=True,
    pin_memory=False,            # meaningless with unified memory
    drop_last=True,
)

opt = torch.optim.AdamW(model.parameters(), lr=3e-4, weight_decay=0.01)
sched = torch.optim.lr_scheduler.OneCycleLR(opt, max_lr=3e-4, total_steps=steps)

for epoch in range(epochs):
    model.train()
    for x, y in loader:
        x = x.to(device, non_blocking=True).float()   # never float64 on MPS
        y = y.to(device)
        opt.zero_grad(set_to_none=True)
        loss = criterion(model(x), y)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step(); sched.step()

    # checkpoint EVERY epoch — a laptop run can be interrupted
    torch.save({"epoch": epoch, "model": model.state_dict(),
                "opt": opt.state_dict(), "sched": sched.state_dict()},
               f"ckpt_ep{epoch}.pt")
    torch.mps.empty_cache()
```

Essentials:
- **Resumable by design.** Save optimizer and scheduler state, not just weights.
- **`float32` everywhere at the boundary.** numpy defaults to float64 and MPS does not support it.
- **Gradient accumulation** instead of a big batch when memory is tight: `loss = loss / accum_steps`, step every `accum_steps` batches. Effective batch 128 with physical batch 16 costs nothing but time.
- **Gradient checkpointing** (`model.gradient_checkpointing_enable()` in HF) trades ~30% speed for large activation savings — often the difference between fitting and OOM.
- **Mixed precision**: `torch.autocast(device_type="mps", dtype=torch.float16)` works but gains are modest and inconsistent (no tensor cores). Measure; if it doesn't help, drop it — fp16 also risks NaNs.

---

## 3. Debugging MPS-specific problems

| Symptom | Cause / fix |
|---|---|
| `MPS backend out of memory` at low apparent usage | Watermark cap — set `PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0` (or ~0.9), reduce batch, `empty_cache()` between phases |
| `Cannot convert a MPS Tensor to float64` | A numpy float64 slipped in — `.astype(np.float32)` / `.float()` |
| `NotImplementedError: aten::… for MPS` | `PYTORCH_ENABLE_MPS_FALLBACK=1`, or replace the op; check whether it's in the hot path |
| Loss is NaN on MPS but fine on CPU | fp16 overflow, or a genuine MPS kernel bug. Test the same seed on CPU; if CPU is fine, upgrade PyTorch and avoid in-place ops on non-contiguous tensors (`.contiguous()` before in-place) |
| Training much slower than expected | An op is silently falling back to CPU every step; profile with `torch.profiler` or bisect by moving submodules to CPU |
| Memory grows every epoch | Accumulating tensors that still hold graph refs — use `.detach().cpu()` when logging, `loss.item()` not `loss` |
| Results differ run-to-run despite seeds | Expected on MPS; report multi-seed means |

Sanity ritual for any new architecture: run 20 steps on CPU and 20 on MPS with the same seed and compare losses. Divergence beyond noise means an MPS issue, not a modeling issue.

---

## 4. Vision

- Use `timm` backbones; start small: `convnext_tiny`, `efficientnet_b0/b3`, `resnet50`, `vit_small_patch16_224`.
- Resolution dominates cost: 224px is affordable, 384px is 3× more, 512px+ is cloud territory.
- Augmentation with `albumentations` on CPU workers; keep augmentation cheap or the 6 P-cores become the bottleneck instead of the GPU.
- Preprocess/resize the dataset once to disk (e.g. 256px JPEG/webp or a packed `.npy`) instead of decoding full-size images every epoch — usually the single biggest local speedup.
- Test-time augmentation (hflip + a couple of scales) is cheap and reliably worth +0.2-1%.
- Transformers (ViT/DINOv2/Swin) now outnumber CNNs among competition winners, but they are heavier — locally, prefer fine-tuning a pretrained DINOv2-small as a *feature extractor* (frozen) plus a light head, which is fast and surprisingly strong.

---

## 5. NLP

- **Encoders** (DeBERTa-v3-small/base, ModernBERT) still fine-tune well and are the practical local option: seq len 256, batch 8-16 with accumulation.
- **Decoders/LLMs**: use MLX for local work. `mlx_lm.lora` fine-tunes 3-8B models at 4-bit within 16 GB; `mlx_lm.generate` for inference. Qwen-family models dominated 2025 text competitions and have good MLX support.
- **Embeddings as features**: `sentence-transformers` on MPS gives strong dense features for a GBDT — often the best accuracy/effort ratio locally.
- Truncation strategy matters more than model size for long documents: head+tail truncation, or chunk-and-pool.
- For competitions: fine-tune in the cloud, export OOF predictions, and blend locally.

---

## 6. Tabular neural nets

Worth building for ensemble diversity:
- **MLP with categorical embeddings**: embedding dim ≈ `min(50, (cardinality+1)//2)`, 2-3 hidden layers, BatchNorm/LayerNorm, dropout 0.1-0.3, rankgauss-transformed numerics.
- **TabM / FT-Transformer / SAINT** style models when you want a stronger tabular NN.
- **1D-CNN over feature embeddings** is a known Kaggle trick for tabular data and adds unusual diversity.
- Train on CPU for small data (often faster than MPS due to transfer overhead) and on MPS above ~500k rows.
- Always feed rankgauss/quantile-transformed inputs; raw skewed features cripple NNs while trees don't care.

---

## 7. Time series / sequences

- GBDT on lag/rolling features is the baseline to beat, and it usually wins.
- Deep options that are feasible locally: GRU/LSTM, temporal CNN, N-BEATS/NHITS, PatchTST-small.
- Respect the horizon: features must be computable at the forecast origin; validation must be time-based (see `validation.md`).
- Statistical baselines (seasonal naive, ETS, AutoARIMA via `statsforecast`) are fast, strong, and add ensemble diversity.

---

## 8. Efficiency tricks worth knowing

- **Freeze most of the backbone**, train the head + last block: 3-5× faster, often within 1% of full fine-tuning on small datasets.
- **LoRA/PEFT** instead of full fine-tuning: a fraction of the memory, and multiple adapters can share one base model.
- **Knowledge distillation** from a cloud-trained big model into a small local model when the submission has runtime limits.
- **Snapshot ensembles / SWA**: several ensemble members from one training run.
- **Early stopping on the fold metric**, and a strict epoch cap — laptop time is the scarcest resource in the project.
