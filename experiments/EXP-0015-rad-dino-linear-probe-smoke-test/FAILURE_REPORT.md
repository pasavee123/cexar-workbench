# FAILURE_REPORT.md

## Experiment: EXP-0015 — RAD-DINO Linear Probe Smoke Test

### Status: No Failures

The experiment completed successfully. All phases passed:

- Phase 1 (Input Validation): PASSED — 8 of 8 checks passed
- Phase 2 (Label Feasibility): PASSED — 9 of 11 labels usable, 2 skipped with reasons
- Phase 3 (Deterministic Split): PASSED — patient-level split created (seed=42, 79/21)
- Phase 4 (Linear Probe): PASSED — 8 labels completed with AUROC, 3 skipped with reasons

### Minor Issues Encountered

1. **scikit-learn missing from venv**: Required package `scikit-learn` was not present in `.venvs/cexar-foundation`. Human approved installation of scikit-learn==1.4.2. Resolved.

2. **Script BASE path resolution** (internal, corrected in same session): Initial script used 2 `dirname` calls to find workspace root from `artifacts/run_rad_dino_linear_probe_smoke.py`. Required 4 `dirname` calls. Fixed in scripts with no data loss.

3. **Venv relative path** (internal, corrected in same session): Relative path `.venvs/cexar-foundation/Scripts/python.exe` failed from experiment directory. Switched to absolute path. No data loss.

### No Follow-Up Required for Failure Resolution

All issues were resolved within the same session. No blocking conditions remain.