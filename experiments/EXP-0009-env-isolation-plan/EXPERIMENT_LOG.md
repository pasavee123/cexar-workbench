# EXPERIMENT_LOG.md — EXP-0009 Environment Isolation Plan

## Session 1 — Environment Isolation Planning

### Overview

EXP-0009 is a **planning and documentation phase** — no terminal commands were executed. This experiment addressed the critical blocker identified in EXP-0008: the lack of virtual environment boundaries that allowed EXP-0006 to globally upgrade PyTorch from 2.0.1 to 2.12.0, contaminating all prior experiments.

## Command Log

| Timestamp | Working Directory | Command | Exit Code | Summary |
| --- | --- | --- | --- | --- |
| N/A | N/A | N/A | N/A | N/A - Review and Planning Phase Only (No terminal execution performed) |

## Activities Performed (Non-Execution)

### [2026-05-22] Activity 1: Analyze global environment contamination
- **Method:** Document analysis of EXP-0008 ENVIRONMENT_SIDE_EFFECTS.md and GLOBAL_ENV_RISK.md
- **Result:** Documented PyTorch 2.0.1→2.12.0 contamination, timm 0.4.12→1.0.27 cascade, 12+ global package installs

### [2026-05-22] Activity 2: Design 4-venv isolation architecture
- **Method:** Requirements analysis per dependency profile
- **Result:** Designed `cexar-baseline` (PyTorch 2.0.1, XRV), `cexar-foundation` (PyTorch >=2.4.1, RAD-DINO/BiomedCLIP), `cexar-xai` (PyTorch 2.0.1, grad-cam/Captum/Quantus), `cexar-training` (PyTorch >=2.4.1, MONAI/Hydra/Lightning)

### [2026-05-22] Activity 3: Pin exact package versions per environment
- **Method:** Cross-reference experiment logs and dependency compatibility
- **Result:** Produced REQUIREMENTS_BASELINE_XRV.txt, REQUIREMENTS_FOUNDATION.txt, REQUIREMENTS_XAI.txt, REQUIREMENTS_TRAINING_FUTURE.txt

### [2026-05-22] Activity 4: Write EXP-0010 runner prompt
- **Method:** Compose NEXT_REAL_RUN_PROMPT.md with strict constraints
- **Result:** TorchXRayVision designated as first real-data inference target; venv creation and pip install instructions specified

### [2026-05-22] Activity 5: Write deliverables
- **Output files:** README.md, RESULT.md, DIFF_SUMMARY.md, ENV_PLAN.md, GLOBAL_ENV_RISK.md, NEXT_REAL_RUN_PROMPT.md, REQUIREMENTS_BASELINE_XRV.txt, REQUIREMENTS_FOUNDATION.txt, REQUIREMENTS_XAI.txt, REQUIREMENTS_TRAINING_FUTURE.txt

## Observations

- This experiment produced no terminal output, no model artifacts, and no package changes.
- The global environment remained contaminated with PyTorch 2.12.0 as of the original planning run. Later policy changed: do not roll back global Python from a runner session; use isolated venvs instead.
- No venvs were created — actual creation is the next runner's responsibility per the plan.
- The key design decision: TorchXRayVision is the safest first real-data inference candidate because it works on PyTorch 2.0.1 and has the narrowest dependency surface.

> ⚠️ **Audit Note (2026-05-23):** This document was retroactively generated/updated during the repository stress-test to reconstruct the historical timeline based on verified experiment artifacts and execution traces.
