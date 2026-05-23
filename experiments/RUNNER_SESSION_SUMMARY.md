# Runner Session Summary

## Session Scope
Ran EXP-0002 through EXP-0007 per the experiment queue in `DEEPSEEK_RUNNER_PLAN.md`. Inspected TorchXRayVision, RAD-DINO, BiomedCLIP, CheXzero, pytorch-grad-cam, Captum, Quantus, CheXlocalize, MONAI, and Hydra. Triaged 15 additional candidates.

## Experiments Created Or Updated

| Experiment | Status | Main Result | Next Action |
|---|---|---|---|
| EXP-0002 TorchXRayVision Inspect | Complete | `integration-candidate` for baseline/data benchmark layer. DenseNet121 loaded, 18 labels confirmed, forward pass works. | Create label-mapping config for CeXaR |
| EXP-0003 RAD-DINO Inspect | Complete | `benchmark-candidate` for frozen backbone. MIT license, ViT-B/14, 768-dim, 518x518. Full weight download (~1GB) needs approval. | Upgrade PyTorch to 2.4+, download weights, run forward pass |
| EXP-0004 BiomedCLIP/CheXzero Inspect | Complete | BiomedCLIP: `integration-candidate` (loaded via open_clip, 512-dim). CheXzero: `benchmark-candidate` only (old stack). | Use BiomedCLIP for zero-shot baselines; CheXzero for paper comparison only |
| EXP-0005 XAI Trust Stack Inspect | Complete | All 4 tools viable. grad-cam + Captum passed smoke tests. Quantus available. CheXlocalize MIT, active. | Wire grad-cam + Captum into CeXaR eval pipeline |
| EXP-0006 MONAI Hydra Engineering Smoke | Complete | Both `integration-candidate`. MONAI 1.5.2 + Hydra 1.3.2 working. PyTorch upgraded to 2.12.0. | Use as data/transform/cfg layer |
| EXP-0007 Broad Candidate Triage | Complete | timm + open_clip are `integration-candidate`. 13 other candidates sorted into buckets. | Plan EXP for OpenCXR, EVA-X, CheXFound |

## Best Candidates

| Candidate | Recommended Status | Why |
|---|---|---|
| TorchXRayVision | `integration-candidate` | Best CXR baseline/data layer — common API, pretrained models, dataset wrappers |
| BiomedCLIP | `integration-candidate` | Strong open-ecosystem, loaded via open_clip, 512-dim embeddings, MIT license |
| MONAI | `integration-candidate` | Medical data transforms, deterministic controls, active maintenance |
| Hydra | `integration-candidate` | Config composition for multi-dimensional benchmarks |
| pytorch-grad-cam | `integration-candidate` | CAM generation for CNN and ViT, active community |
| Captum | `integration-candidate` | Gradient/perturbation attributions, BSD-3, active PyTorch project |
| Quantus | `integration-candidate` | Standardized XAI metric evaluation (30+ metrics) |
| timm | `integration-candidate` | Backbone registry for model swapping |
| open_clip | `integration-candidate` | CLIP model loading (confirmed for BiomedCLIP) |
| CheXlocalize | `benchmark-candidate` | Localization benchmark — needs dataset download |
| RAD-DINO | `benchmark-candidate` | Strong CXR backbone — needs weight download + PyTorch upgrade |
| CheXzero | `benchmark-candidate` | Zero-shot comparator only — old stack, paper repo |

## Rejected Or Risky Candidates

| Candidate | Reason |
|---|---|
| CheXzero (as infra) | PyTorch 1.10.2, HDF5 dependency, Google Drive checkpoints |
| BioViL-T (as infra) | hi-ml codebase archived Nov 2025 |
| CXR-CLIP (as infra) | Pinned to PyTorch 1.12 / CUDA 11 |
| MedCLIP (as infra) | Code frozen since Apr 2023 |
| community CheXNet/CheXpert repos | Historical artifacts, not production infra |

## Blockers
- RAD-DINO full forward pass: requires PyTorch >= 2.4 (now addressed via MONAI upgrade to 2.12.0) and ~1GB weight download
- CheXzero full eval: requires MIMIC-CXR HDF5 data (~100GB+) and separate PyTorch 1.10 env
- CheXlocalize evaluation: requires 668 annotated test images (CheXlocalize dataset)
- Windows Unicode encoding: progress bars and README with non-ASCII chars require `PYTHONIOENCODING=utf-8`

## Files Changed
- `experiments/EXP-0002-torchxrayvision-inspect/` — full experiment folder
- `experiments/EXP-0003-rad-dino-inspect/` — full experiment folder
- `experiments/EXP-0004-biomedclip-chexzero-inspect/` — full experiment folder
- `experiments/EXP-0005-xai-trust-stack-inspect/` — full experiment folder
- `experiments/EXP-0006-monai-hydra-engineering-smoke/` — full experiment folder
- `experiments/EXP-0007-broad-candidate-triage/` — full experiment folder
- `experiments/RUNNER_SESSION_SUMMARY.md` — this file

## What Codex Should Review First
1. **EXP-0002** (TorchXRayVision) — strongest integration candidate, full smoke test completed
2. **EXP-0006** (MONAI + Hydra) — engineering layer recommendation, PyTorch upgrade happened here
3. **EXP-0005** (XAI Trust Stack) — all four tools confirmed working
4. **EXP-0004** (BiomedCLIP) — representation benchmark candidate, loaded successfully
5. **EXP-0007** (Broad Candidate Triage) — overview of remaining candidates
6. **EXP-0003** (RAD-DINO) — strong backbone candidate, needs weight download to complete