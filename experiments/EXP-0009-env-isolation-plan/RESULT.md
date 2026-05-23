# RESULT.md

## Verdict

- [x] **plan-complete** — Environment isolation plan is ready for runner execution.

## Summary

This experiment produces a complete environment isolation plan for CeXaR, addressing the critical blocker identified in EXP-0008: the lack of virtual environment boundaries allowed EXP-0006 to globally upgrade PyTorch from 2.0.1 to 2.12.0, contaminating all prior experiments.

## Deliverables Produced

| File | Purpose | Status |
|---|---|---|
| ENV_PLAN.md | Detailed isolation strategy, 4-venv design, pinning rationale, anti-contamination protocol | Complete |
| REQUIREMENTS_BASELINE_XRV.txt | Pinned deps for TorchXRayVision (torch 2.0.1) | Complete |
| REQUIREMENTS_FOUNDATION.txt | Pinned deps for RAD-DINO/BiomedCLIP (torch >=2.4.1) | Complete |
| REQUIREMENTS_XAI.txt | Pinned deps for grad-cam/Captum/Quantus (torch 2.0.1) | Complete |
| REQUIREMENTS_TRAINING_FUTURE.txt | Pinned deps for MONAI/Hydra/Lightning (torch >=2.4.1) | Complete |
| GLOBAL_ENV_RISK.md | Current contamination state and mitigation checklist | Complete |
| NEXT_REAL_RUN_PROMPT.md | Exact prompt for EXP-0010 TorchXRayVision real-data inference | Complete |
| README.md | Experiment overview | Complete |
| RESULT.md | This file | Complete |
| DIFF_SUMMARY.md | File change summary | Complete |

## Key Design Decisions

1. **TorchXRayVision is designated the first real-data inference run** because:
   - It is the best-tested environment (confirmed working on PyTorch 2.0.1 in EXP-0002)
   - It has the narrowest dependency surface (torch, torchvision, torchxrayvision only)
   - It requires no PyTorch upgrade — compatible with the rollback target of 2.0.1
   - It produces a concrete, reviewable artifact (18 pathology logits)

2. **Two PyTorch versions are unavoidable.** PyTorch 2.0.1 for the baseline/XAI stack; PyTorch >=2.4.1 for foundation models and training. These must live in separate venvs with activation discipline enforced by `PIP_REQUIRE_VIRTUALENV=true`.

3. **timm 0.4.12 is the only safe version** until `segmentation-models-pytorch 0.2.1` is upgraded or removed. open_clip_torch 3.3.0 in cexar-foundation must be installed AFTER timm is locked to 0.4.12 to prevent cascade upgrade.

## Risks

- The global environment is still contaminated with PyTorch 2.12.0 as of this writing. The rollback must happen before EXP-0010 starts.
- Quantus full-deps install (REQUIREMENTS_XAI.txt) has never been tested. It may pull additional transitive dependencies that conflict with the torch 2.0.1 baseline.
- The `cexar-training` venv uses the newest PyTorch (>=2.4.1) and is the most volatile. Its future requirements may drift as MONAI, Lightning, and MLflow release new versions.

## Next Steps

1. Pass NEXT_REAL_RUN_PROMPT.md to the next strongest AI agent (Codex-level) to execute EXP-0010.
2. After EXP-0010 succeeds, proceed to EXP-0011 (Quantus smoke test in cexar-xai).
3. After XAI is validated, proceed to EXP-0012 (RAD-DINO forward pass in cexar-foundation).