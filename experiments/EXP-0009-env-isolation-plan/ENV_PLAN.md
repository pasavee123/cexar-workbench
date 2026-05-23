# CeXaR Environment Isolation Plan

## 1. The Problem: Flash's Global PyTorch Upgrade

EXP-0006's `pip install monai` triggered a global PyTorch upgrade from 2.0.1 to 2.12.0 (an 11-minor-version leap) because MONAI >=1.5.x requires PyTorch >=2.4.1. This retroactively invalidated the runtime assumptions of every prior experiment (EXP-0002 through EXP-0005). The environment was not restored.

### 1.1 Root Cause

No virtual environment was used. All experiments shared the same global Python site-packages. Any `pip install` that pulled a transitive dependency upgrade silently changed behavior for every other package.

### 1.2 Principle

**Every install-heavy experiment must run in its own isolated environment. No `pip install` in the global Python ever again.**

---

## 2. Four Isolated Environments

| Environment | Purpose | PyTorch | Key Packages | Risk Level |
|---|---|---|---|---|
| `cexar-baseline` | TorchXRayVision inference, DenseNet121 outputs, label contract verification, real CXR data pipeline | **2.0.1** (pinned) | torchxrayvision==1.4.0, torchvision==0.15.2 | LOW — known good, smoke-tested on 2.0.1 |
| `cexar-foundation` | RAD-DINO, BiomedCLIP, open_clip, zero-shot classification, embedding extraction | **2.4.1+** (>=2.4.1) | transformers==4.40.2, open_clip_torch==3.3.0, timm==0.4.12, huggingface_hub | MEDIUM — torch/timm version conflict with baseline |
| `cexar-xai` | pytorch-grad-cam, Captum, Quantus, heatmap generation, faithfulness metrics | **2.0.1** (pinned) | grad-cam==1.5.5, captum==0.9.0, quantus==0.6.0, scikit-image, opencv-python | MEDIUM — Quantus full deps untested |
| `cexar-training` | MONAI, Hydra, PyTorch Lightning, MLflow, W&B, future fine-tuning and config management | **2.12.0** (>=2.4.1) | monai==1.5.2, hydra-core==1.3.2, pytorch-lightning, mlflow | HIGH — newest PyTorch, slowest to stabilize |

---

## 3. Which Environment Should Be Used First

### `cexar-baseline` (TorchXRayVision)

**This is the first and only environment for the next real run.**

Reasons:

1. **It is the best-tested environment.** EXP-0002 confirmed torchxrayvision 1.4.0 installs, loads DenseNet121, and runs forward passes on PyTorch 2.0.1 without any dependency cascade.
2. **It has zero temporary regressions.** Unlike `cexar-foundation` (timm 0.4.12 was already broken globally by EXP-0004) and `cexar-training` (PyTorch was globally upgraded), the baseline stack requires no rollback gymnastics — just create a clean venv with the pinned requirements.
3. **It uses the lowest-risk dependency set.** TorchXRayVision's only hard dependencies are torch and torchvision. No transformers, no open_clip, no timm, no MONAI. The surface area for environment contamination is minimal.
4. **It produces a real deliverable.** A pretrained DenseNet121 forward pass on a real CXR image subset yields 18 pathology logits — a concrete, reviewable artifact. The zero-shot radiology reports from RAD-DINO/BiomedCLIP are downstream of having a working inference pipeline.
5. **It matches the original PyTorch 2.0.1 production baseline.** If CeXaR ever had a production assumption, it was torch==2.0.1. XRV is the safest path to confirm that baseline still holds.

---

## 4. Why TorchXRayVision Should Be the First Real-Data Inference Run

### 4.1 Technical Readiness (from EXP-0002)

| Capability | Status |
|---|---|
| Package installs without dependency conflicts | Confirmed on torch 2.0.1 |
| Pretrained DenseNet121 loads | Confirmed (447 MB weights cached) |
| Forward pass produces [B, 18] logits | Confirmed |
| 18 pathology labels documented | Confirmed |
| Preprocessing: [-1024, 1024] HU, 224x224 | Confirmed |
| License | Apache 2.0 (repo inspected, needs documentation in RESULT.md) |

### 4.2 Strategic Reasons

1. **Minimal moving parts.** XRV is a single package wrapping a single model (DenseNet121). No HF hub auth, no clip tokenizer, no multi-GPU config. Fewer failure modes = faster to a real result.
2. **Real-data CXR inference is CeXaR's core value proposition.** Encoding a chest X-ray into 18 pathology probabilities is the first concrete capability CeXaR can demonstrate end-to-end. RAD-DINO embeddings and BiomedCLIP zero-shot classification are valuable but come second.
3. **Label contract validation is a pre-requisite for everything downstream.** If XRV's 18-label order does not match CeXaR manifest expectations, every other model's outputs must be cross-walked differently. Fix the label contract first.
4. **Preprocessing validation on real data.** The [-1024, 1024] HU normalization was only tested on synthetic random tensors. Real DICOM PNGs may have different HU ranges, padding, or bit depths. Catching preprocessing failures early prevents subtle bugs later.

### 4.3 Risk of Skipping XRV First

If a more complex model (RAD-DINO, BiomedCLIP, MONAI training) is attempted first and fails due to environment contamination, the debugging surface is huge: is it the PyTorch version, the transformers version, the timm version, the open_clip version, the dataset format, or the model weights? XRV isolates one variable at a time.

---

## 5. Package Versions — What to Pin

### 5.1 `cexar-baseline` (MUST pin exactly)

| Package | Version | Constraint | Rationale |
|---|---|---|---|
| torch | 2.0.1 | `==2.0.1` | Original production baseline; avoids XRV breakage from 2.12.x API changes |
| torchvision | 0.15.2 | `==0.15.2` | Must match torch 2.0.1 exactly (PyTorch community convention) |
| torchxrayvision | 1.4.0 | `==1.4.0` | Only version tested in EXP-0002 |
| numpy | <2.0 | `>=1.21,<2.0` | NumPy 2.x breaks torch 2.0.1 |
| Pillow | >=9.0 | `>=9.0` | Image loading for real CXR files |
| scikit-image | >=0.19 | `>=0.19` | DICOM/PNG processing for real data pipeline |

### 5.2 `cexar-foundation` (Pin within range)

| Package | Version | Constraint | Rationale |
|---|---|---|---|
| torch | >=2.4.1 | `>=2.4.1,<2.6` | RAD-DINO requires 2.4+; upper bound prevents unplanned breaking changes |
| torchvision | >=0.19 | `>=0.19,<0.22` | Matches torch >=2.4.1 |
| transformers | 4.40.2 | `==4.40.2` | Tested compatible with PyTorch 2.x in EXP-0003 |
| open_clip_torch | 3.3.0 | `==3.3.0` | Version used in EXP-0004 BiomedCLIP loading |
| timm | 0.4.12 | `==0.4.12` | Locked to avoid segmentation-models-pytorch breakage (0.2.1 requires timm==0.4.12) |
| huggingface_hub | >=0.20 | `>=0.20` | HF model card inspection, no tight upper bound |
| tokenizers | >=0.15 | `>=0.15` | CLIP tokenizer dependency |

### 5.3 `cexar-xai` (Pin exactly, MUST install full deps)

| Package | Version | Constraint | Rationale |
|---|---|---|---|
| torch | 2.0.1 | `==2.0.1` | Baseline-compatible for XRV heatmaps |
| grad-cam | 1.5.5 | `==1.5.5` | Smoke-tested on synthetic CNN in EXP-0005 |
| captum | 0.9.0 | `==0.9.0` | IG convergence tested in EXP-0005 |
| quantus | 0.6.0 | `==0.6.0` | **Untested** — must install WITH full dependencies (NOT `--no-deps`) |
| scikit-image | >=0.19 | `>=0.19` | Quantus dependency (image metrics) |
| opencv-python | >=4.5 | `>=4.5` | Quantus dependency (image processing) |
| scipy | >=1.7 | `>=1.7` | Quantus dependency |
| numpy | <2.0 | `>=1.21,<2.0` | NumPy 2.x breaks torch 2.0.1 and potentially Quantus |
| matplotlib | >=3.5 | `>=3.5` | Heatmap visualization |
| ttach | 0.0.3 | `==0.0.3` | Test-time augmentation for grad-cam |

### 5.4 `cexar-training` (Pin exactly, most volatile)

| Package | Version | Constraint | Rationale |
|---|---|---|---|
| torch | >=2.4.1 | `>=2.4.1` | Required by MONAI 1.5.2 |
| monai | 1.5.2 | `==1.5.2` | Smoke-tested in EXP-0006 (results contaminated) |
| hydra-core | 1.3.2 | `==1.3.2` | Config composition tested in EXP-0006 |
| omegaconf | >=2.2 | `>=2.2` | Hydra dependency |
| pytorch-lightning | >=2.0 | `>=2.0` | Training loop management (triaged in EXP-0007) |
| mlflow | >=2.8 | `>=2.8` | Experiment tracking (Apache 2.0) |
| wandb | >=0.16 | `>=0.16` | Optional: proprietary; gate behind team decision |

---

## 6. Packages That MUST NOT Be Mixed

| Conflict Pair | Reason | Consequence |
|---|---|---|
| **torch 2.0.1 + monai >=1.5** | MONAI 1.5+ requires torch >=2.4.1 | pip will auto-upgrade torch to 2.12.x — FLASH'S EXACT BUG |
| **timm 0.4.12 + open_clip_torch >=3.0** | open_clip 3.x pulls timm >=1.x | Breaks `segmentation-models-pytorch 0.2.1` which requires `timm==0.4.12` |
| **transformers 5.x + torch 2.0.1** | transformers 5.x drops PyTorch 2.0.x support | EXP-0003 had to downgrade from 5.9.0 to 4.40.2 |
| **numpy >=2.0 + torch 2.0.1** | NumPy 2.x breaks torch 2.0.1 ABI | Import errors, segfaults |
| **quantus + --no-deps install** | Quantus has 12+ implicit deps (scipy, skimage, opencv, etc.) | No metric can actually run (EXP-0005's gap) |

### 6.1 The Two-PyTorch Barrier

The project must live with **two PyTorch versions simultaneously**:
- PyTorch 2.0.1 for the baseline (XRV, XAI, any production inference)
- PyTorch >=2.4.1 for foundation models and future training (RAD-DINO, MONAI, Lightning)

**These must never coexist in the same venv.** A single `pip install` in the wrong environment is all it takes to break reproducibility.

---

## 7. How to Avoid Repeating Flash's Global Upgrade Problem

### 7.1 Creation Protocol

Every environment must be created with:

```powershell
# Step 1: Create venv (not conda — venv is faster and lighter for no-CUDA)
python -m venv .venvs\cexar-baseline

# Step 2: Activate — ALWAYS before any pip command
.\.venvs\cexar-baseline\Scripts\Activate.ps1

# Step 3: Verify PYTHON_PATH is inside .venvs, NOT global site-packages
python -c "import sys; print(sys.prefix)"

# Step 4: Install from pinned requirements file
pip install -r experiments\EXP-0009-env-isolation-plan\REQUIREMENTS_BASELINE_XRV.txt

# Step 5: Freeze and verify
pip freeze > experiments\EXP-0009-env-isolation-plan\artifacts\baseline_frozen_pip.txt
```

### 7.2 Activation Discipline

| Rule | Violation Prevention |
|---|---|
| **Activate venv before any pip command** | `pip` outside a venv installs to global site-packages |
| **Always check `sys.prefix` before installing** | Confirms you are in the venv, not global |
| **Never run `pip install` without `--require-virtualenv` check** | Set `PIP_REQUIRE_VIRTUALENV=true` as a global env var |
| **Use `pip install --no-deps` only when explicitly justified** | Prevents hidden transitive upgrades; document justification in log |
| **Freeze after every install session** | Creates a point-in-time lockfile for reproducibility |

### 7.3 Verification Checklist (Before Any Experiment)

- [ ] `python -c "import sys; assert '.venvs' in sys.prefix, 'NOT IN VENV'"` passes
- [ ] `pip freeze` matches the requirements file for THIS environment only
- [ ] No package from a different environment tier is present
- [ ] `torch.__version__` matches the pinned version for this tier
- [ ] `timm.__version__` is 0.4.12 (NOT 1.x)
- [ ] `numpy.__version__` is 1.x (NOT 2.x)

### 7.4 Venv Cleanup Protocol

If contamination is detected:

```powershell
# Destroy and recreate — do NOT attempt to repair in-place
# Do not run cleanup unless the human explicitly approves it.
# First verify the resolved path is inside D:\cexar-workbench\.venvs\.
# Prefer creating a new versioned venv instead of deleting evidence.
# Cleanup command intentionally omitted from runner instructions.
# No runnable cleanup commands are provided here.
# A future runner must use a fresh experiment-specific plan after human approval.
```

### 7.5 Environment Variable Safeguard

Add to shell profile or set per-session:

```powershell
$env:PIP_REQUIRE_VIRTUALENV = "true"
```

This causes `pip install` to fail with an error if not inside an active venv. Remove this safeguard only with explicit justification logged in EXPERIMENT_LOG.md.

---

## 8. Environment Directory Layout

```
.venvs/
  cexar-baseline/       # TorchXRayVision + torch 2.0.1
  cexar-foundation/     # RAD-DINO, BiomedCLIP + torch >=2.4.1
  cexar-xai/            # grad-cam, Captum, Quantus + torch 2.0.1
  cexar-training/       # MONAI, Hydra, Lightning + torch >=2.4.1
```

These venvs live at the project root and are `.gitignore`d. They are not part of any experiment subfolder.

---

## 9. Experiment-to-Environment Mapping

| Experiment | Environment | PyTorch | Rationale |
|---|---|---|---|
| EXP-0010: XRV Label Contract | `cexar-baseline` | 2.0.1 | XRV-native env, no torch upgrade needed |
| EXP-0011: Quantus Smoke Test | `cexar-xai` | 2.0.1 | Quantus + full deps; baseline-compatible |
| EXP-0012: RAD-DINO Forward Pass | `cexar-foundation` | >=2.4.1 | RAD-DINO requires >=2.4.1 |
| EXP-0013: BiomedCLIP Zero-Shot | `cexar-foundation` | >=2.4.1 | open_clip requires timm; isolated from baseline timm |
| EXP-0014: MONAI Rerun (isolated) | `cexar-training` | >=2.4.1 | MONAI 1.5.2 needs 2.4+; must NOT touch baseline |

---

## 10. First Action: Avoid Global Environment

Do not restore, roll back, uninstall from, or force-reinstall into the global Python environment from a runner session.

The selected strategy is:

- Do not trust global Python.
- Create new venvs from an approved Python executable.
- Never run experiments outside activated venvs again.
- Treat any global rollback as a separate human-approved maintenance task, not an experiment action.

Audit Pass 2, 2026-05-23: This section replaces the earlier rollback instruction. The current policy is venv-only execution for runners.
