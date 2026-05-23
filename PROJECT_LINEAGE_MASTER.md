# PROJECT_LINEAGE_MASTER.md — CeXaR Experiment Timeline Dashboard

> Central registry of all controlled experiments (EXP-0001 through EXP-0011).
> Last reconstructed: 2026-05-23

---

## Experiment Status Overview

| # | EXP ID | Name | Date | Verdict | Terminal Execution? | EXPERIMENT_LOG | commands.ps1 |
|---|--------|------|------|---------|---------------------|----------------|--------------|
| 1 | EXP-0001 | Workflow Smoke Test | (pre-run) | Scaffolding | No — N/A (System Scaffolding State) | ✅ Present | ✅ Present |
| 2 | EXP-0002 | TorchXRayVision Inspect | 2026-05-22 | **PASS** | Yes — 5 pip/python commands | ✅ Present | ✅ Present |
| 3 | EXP-0003 | RAD-DINO Inspect | 2026-05-22 | PASS (weights timeout) | Yes — 5 pip/python commands | ✅ Present | ✅ Present |
| 4 | EXP-0004 | BiomedCLIP & CheXzero Inspect | 2026-05-22 | **PASS** | Yes — 7 commands | ✅ Present | ✅ Present |
| 5 | EXP-0005 | XAI Trust Stack Inspect | 2026-05-22 | **PASS** | Yes — 7 commands | ✅ Present | ✅ Present |
| 6 | EXP-0006 | MONAI Hydra Engineering Smoke | 2026-05-22 | PASS (CRITICAL side-effect) | Yes — 3 commands | ✅ Present | ✅ Backfilled |
| 7 | EXP-0007 | Broad Candidate Triage | 2026-05-22 | **PASS** | No — document analysis only | ✅ Present | ✅ Backfilled |
| 8 | EXP-0008 | Flash Run Review | 2026-05-22 | Review complete | No — N/A (Review Phase) | ✅ Backfilled | N/A |
| 9 | EXP-0009 | Environment Isolation Plan | 2026-05-22 | plan-complete | No — N/A (Planning Phase) | ✅ Backfilled | N/A |
| 10 | EXP-0010 | TorchXRayVision Real Inference | 2026-05-23 | **PARTIAL PASS** | Yes — 35 commands (incl. resume/admin) | ✅ Present | ✅ Present |
| 11 | EXP-0011 | CheXpert XRV Real Inference | 2026-05-23 | **PASS** | Yes — 9 commands | ✅ Present | ✅ Present |

---

## Detailed Timeline

### Phase 1: Scaffolding & Initial Smoke Tests (2026-05-22 early)

#### 1. EXP-0001 — Workflow Smoke Test
- **Timestamp:** Pre-run (initial workspace setup)
- **Nature:** N/A — System Scaffolding State
- **What happened:** Created directory templates, defined the required file structure (README, TEST_PLAN, RUNNER_INSTRUCTIONS, commands.ps1, EXPERIMENT_LOG, etc.) that all subsequent experiments would follow. No terminal commands were executed.
- **Outcome:** Established workflow conventions. Hypothesis validated later by Flash agent's successful adherence to the protocol.

#### 2. EXP-0002 — TorchXRayVision Inspect
- **Timestamp:** 2026-05-22 20:28–20:30
- **Scripts executed:**
  1. `pip install torchxrayvision` → XRV v1.4.0 installed
  2. `python -c "import torchxrayvision as xrv; print('XRV version:', xrv.__version__)"` → 1.4.0 confirmed
  3. `python -c "...xrv.models.get_model('densenet121-res224-all')"` → **FAIL** (Windows cp874 UnicodeEncodeError, corrupted weights)
  4. `PYTHONIOENCODING=utf-8 python -c "..."` → retry → **PASS** (DenseNet121 loaded, 18 pathologies)
  5. Synthetic tensor `[1,1,224,224]` forward pass → output `[1,18]`, 6.97M params
  6. Model config inspection → normalization `[-1024,1024]` HU, 224×224 input
- **Verdict:** `integration-candidate` for baseline/data benchmark layer
- **Key risk:** Normalization mismatch (HU vs ImageNet) is #1 risk when switching models

### Phase 2: Foundation Model Inspection (2026-05-22 mid-session)

#### 3. EXP-0003 — RAD-DINO Inspect
- **Timestamp:** 2026-05-22 20:34–20:40
- **Scripts executed:**
  1. `pip install transformers huggingface_hub` → transformers 5.9.0 (needs PyTorch >=2.4)
  2. `pip install "transformers>=4.30.0,<4.41.0"` → downgrade to 4.40.2 (PyTorch 2.0.1 compatible)
  3. `AutoModel.from_pretrained('microsoft/rad-dino')` → **TIMEOUT** (~1GB weights, 300s limit)
  4. `model_info('microsoft/rad-dino')` → MIT, ViT-B/14, 768-dim
  5. `list_repo_files` + `hf_hub_download` → config.json, preprocessor_config.json documented
- **Verdict:** `benchmark-candidate` for frozen backbone evaluation
- **Key risk:** Requires PyTorch >=2.4 and ~1GB weight download

#### 4. EXP-0004 — BiomedCLIP & CheXzero Inspect
- **Timestamp:** 2026-05-22 20:53–20:56
- **Scripts executed:**
  1. `model_info('microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224')` → MIT, ~954K downloads
  2. `hf_hub_download` → open_clip_config.json → embed_dim=512, ViT-B/16@224
  3. `open_clip.create_model_and_transforms('hf-hub:microsoft/BiomedCLIP-...')` → loaded (output_dim attr failed)
  4. `model.encode_image(torch.randn(1,3,224,224))` → output `[1,512]`, ~196M params
  5. GitHub API `rajpurkarlab/CheXzero` → MIT, 225 stars
  6. CheXzero requirements.txt → torch==1.10.2 (conflicts with current env)
  7. CheXzero zero_shot.py → CLIP ViT-B/32, HDF5 data format
- **Verdict:** BiomedCLIP `integration-candidate`; CheXzero `benchmark-candidate` only
- **CRITICAL side-effect:** timm upgraded 0.4.12 → 1.0.27 (may break segmentation-models-pytorch)

### Phase 3: XAI Stack & Engineering Layer (2026-05-22 late)

#### 5. EXP-0005 — XAI Trust Stack Inspect
- **Timestamp:** 2026-05-22 21:09–21:12
- **Scripts executed:**
  1. `pip install captum grad-cam --no-deps` → installed without PyTorch upgrade
  2. `pip install ttach --no-deps` → grad-cam dependency
  3. grad-cam smoke test (synthetic CNN) → output `(1,64,64)`, values `[0,1]` → **PASS**
  4. Captum IG smoke test (synthetic CNN) → attribution `(1,3,64,64)`, delta ~1e-5 → **PASS**
  5. `pip install quantus --no-deps` → Quantus 0.6.0 (no smoke test run)
  6. GitHub API `rajpurkarlab/cheXlocalize` → MIT, 40 stars
- **Verdict:** grad-cam `integration-candidate`; Captum `integration-candidate`; Quantus `integration-candidate` (downgraded by EXP-0008 — no smoke test); CheXlocalize `benchmark-candidate`

#### 6. EXP-0006 — MONAI Hydra Engineering Smoke
- **Timestamp:** 2026-05-22 21:19–21:20
- **Scripts executed:**
  1. `pip install monai hydra-core` → MONAI 1.5.2, Hydra 1.3.2
  2. `set_determinism(seed=42)` + `Compose(ScaleIntensity, RandRotate)` → **PASS**
  3. Hydra `initialize_config_dir` + `compose` → config loaded → **PASS**
- **Verdict:** Both `integration-candidate` (downgraded by EXP-0008 due to side-effects)
- **CRITICAL side-effect:** PyTorch upgraded globally from **2.0.1 → 2.12.0** — violates no-side-effects rule, invalidates runtime assumptions of EXP-0002 through EXP-0005
- **Missing files at run time:** README, TEST_PLAN, RUNNER_INSTRUCTIONS, FAILURE_REPORT, commands.ps1 (backfilled 2026-05-23)

#### 7. EXP-0007 — Broad Candidate Triage
- **Timestamp:** 2026-05-22 21:26
- **Scripts executed:** None — document analysis of `deep-research-report.md` only
- **Result:** Triage table with 15 candidates across 4 buckets; timm and open_clip identified as strongest integration candidates
- **Missing files at run time:** TEST_PLAN, RUNNER_INSTRUCTIONS, FAILURE_REPORT, commands.ps1 (backfilled 2026-05-23)

### Phase 4: Audit & Remediation (2026-05-22 post-session)

#### 8. EXP-0008 — Flash Run Review (Pro Review)
- **Timestamp:** 2026-05-22 (after EXP-0007)
- **Nature:** N/A — Review and Planning Phase Only (No terminal execution performed)
- **Activities:**
  - Cross-referenced all EXPERIMENT_LOG files (EXP-0002–0007)
  - Audited required file completeness → identified EXP-0006 and EXP-0007 as incomplete
  - Audited environment side effects → identified PyTorch 2.0.1→2.12.0 global upgrade as CRITICAL
  - Assessed verdict reliability → downgraded Quantus, MONAI, Hydra, BiomedCLIP
  - Produced: PRO_REVIEW_RESULT.md, CLAIMS_AUDIT.md, ENVIRONMENT_SIDE_EFFECTS.md, NEXT_EXPERIMENTS.md
- **Key recommendation:** Environment isolation is the #1 blocker before any further install-heavy experiment

#### 9. EXP-0009 — Environment Isolation Plan
- **Timestamp:** 2026-05-22 (after EXP-0008)
- **Nature:** N/A — Review and Planning Phase Only (No terminal execution performed)
- **Activities:**
  - Analyzed global environment contamination from EXP-0006
  - Designed 4-venv architecture: `cexar-baseline` (torch 2.0.1), `cexar-foundation` (torch >=2.4.1), `cexar-xai` (torch 2.0.1), `cexar-training` (torch >=2.4.1)
  - Pinned exact package versions → REQUIREMENTS_BASELINE_XRV.txt, REQUIREMENTS_FOUNDATION.txt, REQUIREMENTS_XAI.txt, REQUIREMENTS_TRAINING_FUTURE.txt
  - Wrote NEXT_REAL_RUN_PROMPT.md for EXP-0010
  - Did NOT create venvs (next runner's job)
- **Verdict:** `plan-complete`

### Phase 5: Real-Data Inference (2026-05-23)

#### 10. EXP-0010 — TorchXRayVision Real Inference
- **Timestamp:** 2026-05-23
- **Scripts executed (35 steps, including resume and admin rerun):**
  - Read all required standards and prior experiment results
  - `python -m venv .venvs\cexar-baseline` → **FAIL** (python not in PATH)
  - `py -0p` → "No Installed Pythons Found!"
  - `C:\...\python.exe -m venv .venvs\cexar-baseline` → **FAIL** (sandbox boundary)
  - Admin rerun with elevated execution → venv created → **PASS**
  - Install baseline requirements in venv → torch 2.0.1+cpu, xrv 1.4.0 verified
  - `pip freeze` → frozen_pip.txt saved
  - XRV DenseNet121 smoke test → output `(1,18)` → **PASS**
  - Search for real CXR images → **none found**
  - Created synthetic fallback `run_xrv_inference.py` → 5 synthetic inputs, 18 logits each
- **Verdict:** **PARTIAL PASS** — environment verified, but no real CXR images available in repo

#### 11. EXP-0011 — CheXpert XRV Real Inference
- **Timestamp:** 2026-05-23
- **Scripts executed:**
  1. `Test-Path 'D:\Dataset_Chexpert'` → exists
  2. `Get-ChildItem 'D:\Dataset_Chexpert'` → found `archive/`
  3. Read `valid.csv` headers + list validation images → CheXpert JPG confirmed
  4. Created experiment folders + `artifacts/test_images/`
  5. Copied 5 frontal validation images + wrote `sample_labels.csv`, `sample_manifest.csv`
  6. Created `run_xrv_real_inference.py`
  7. Ran inference → `xrv_real_inference_results.json` (5 images, 18 pathologies)
  8. Fixed label mapping bug (filename-based → sample-order, due to CheXpert naming collision)
  9. Reran inference → confirmed 5 images × 18 pathologies
- **Verdict:** **PASS** — baseline XRV environment processes real CheXpert JPG images (smoke test only, not clinical evaluation)

---

## Environment Side Effects Summary

| Side Effect | Source EXP | Severity | Status |
|---|---|---|---|
| PyTorch 2.0.1 → 2.12.0 global upgrade | EXP-0006 | **CRITICAL** | Mitigated by venv in EXP-0010 |
| timm 0.4.12 → 1.0.27 cascade upgrade | EXP-0004 | HIGH | Documented, not yet rolled back |
| torchvision upgrade (version unknown) | EXP-0006 | MEDIUM | Part of PyTorch upgrade cascade |
| 12+ packages installed globally (no venv) | EXP-0002–0006 | MEDIUM | Addressed by venv plan in EXP-0009 |
| XRV weights cached (~447 MB) | EXP-0002 | LOW | Expected side effect |
| HF cache entries | EXP-0003, EXP-0004 | LOW | Expected side effect |

---

## Candidate Verdict Matrix (Post-EXP-0008 Review)

| Candidate | Flash Verdict | Post-Review Verdict | Status |
|---|---|---|---|
| TorchXRayVision | integration-candidate | integration-candidate | **Confirmed** |
| BiomedCLIP | integration-candidate | integration-candidate (downgraded confidence) | Dependency cascade risk |
| MONAI | integration-candidate | integration-candidate (downgraded) | Needs isolated venv rerun |
| Hydra | integration-candidate | integration-candidate (downgraded) | Needs isolated venv rerun |
| pytorch-grad-cam | integration-candidate | integration-candidate | **Confirmed** |
| Captum | integration-candidate | integration-candidate | **Confirmed** |
| Quantus | integration-candidate | needs-evidence (downgraded) | No smoke test run |
| timm | integration-candidate | integration-candidate (derived evidence) | Confirmed via EXP-0004 side effect |
| open_clip | integration-candidate | integration-candidate | **Confirmed** |
| RAD-DINO | benchmark-candidate | benchmark-candidate | Needs weight download + PyTorch upgrade |
| CheXzero | benchmark-candidate | benchmark-candidate | Old stack, reference only |
| CheXlocalize | benchmark-candidate | benchmark-candidate | Needs dataset download |

---

## File Compliance Audit (Post-Backfill 2026-05-23)

| EXP | EXPERIMENT_LOG | commands.ps1 | README | RESULT | DIFF_SUMMARY | Notes |
|-----|:---:|:---:|:---:|:---:|:---:|---|
| EXP-0001 | ✅ Updated | ✅ Updated | — | ✅ (Pending) | ✅ | Status changed from "Pending" to "N/A — Scaffolding" |
| EXP-0002 | ✅ Present | ✅ Present | ✅ | ✅ | ✅ | Complete |
| EXP-0003 | ✅ Present | ✅ Present | ✅ | ✅ | ✅ | Complete |
| EXP-0004 | ✅ Present | ✅ Present | ✅ | ✅ | ✅ | Complete |
| EXP-0005 | ✅ Present | ✅ Present | ✅ | ✅ | ✅ | Complete |
| EXP-0006 | ✅ Present | ✅ **Backfilled** | ❌ Missing | ✅ | ✅ | commands.ps1 retroactively created |
| EXP-0007 | ✅ Present | ✅ **Backfilled** | ✅ | ✅ | ✅ | commands.ps1 retroactively created |
| EXP-0008 | ✅ **Backfilled** | N/A (review) | N/A | N/A | ✅ | EXPERIMENT_LOG retroactively created |
| EXP-0009 | ✅ **Backfilled** | N/A (planning) | ✅ | ✅ | ✅ | EXPERIMENT_LOG retroactively created |
| EXP-0010 | ✅ Present | ✅ Present | — | ✅ | — | Complete (35-step detailed log) |
| EXP-0011 | ✅ Present | ✅ Present | — | ✅ | — | Complete (9-step log) |

---

> ⚠️ **Audit Note (2026-05-23):** This document was retroactively generated/updated during the repository stress-test to reconstruct the historical timeline based on verified experiment artifacts and execution traces.
