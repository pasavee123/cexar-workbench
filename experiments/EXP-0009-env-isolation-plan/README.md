# EXP-0009: Environment Isolation Plan

## Hypothesis

CeXaR can achieve reproducible, version-pinned environments that isolate PyTorch 2.0.1 (production baseline) from PyTorch 2.4+ (foundation models and training infrastructure) via separate venvs, preventing the global PyTorch upgrade contamination observed in EXP-0006.

## Why This Matters

EXP-0006's `pip install monai` triggered an uncontrolled global PyTorch upgrade from 2.0.1 to 2.12.0 — an 11-minor-version leap that retroactively invalidated the runtime assumptions of every prior experiment (EXP-0002 through EXP-0005). No further install-heavy experiment is safe until the environment is compartmentalized. This is the highest-priority blocker before any real-data inference run.

## Scope

- Inspect the damage from Flash's global PyTorch upgrade (documented in GLOBAL_ENV_RISK.md)
- Design four isolated venvs for the four distinct dependency profiles in CeXaR
- Pin exact package versions per environment
- Document which packages must never coexist in the same venv
- Write the exact prompt for the next AI agent to run TorchXRayVision on real CXR data
- Do NOT create venvs — only write the plan (actual venv creation is the next runner's job)
- Do NOT run model experiments
- Do NOT install or upgrade any packages

## Dependencies

- Python 3.10+
- venv (stdlib, no separate install needed)

## References

- EXP-0002: TorchXRayVision smoke test (confirmed working on PyTorch 2.0.1)
- EXP-0006: MONAI smoke test (source of global PyTorch upgrade contamination)
- EXP-0008: Pro review of Flash's run (identified environment isolation as #1 blocker)
- ENVIRONMENT_SIDE_EFFECTS.md: Full audit of package changes outside experiments/
- CLAIMS_AUDIT.md: Verdict downgrades and rerun requirements
- GLOBAL_ENV_RISK.md: Current state of the contaminated global environment