# DIFF_SUMMARY.md

## Experiment: EXP-0015 — RAD-DINO Linear Probe Smoke Test

### Files Created

| File | Purpose |
|------|---------|
| `artifacts/run_rad_dino_linear_probe_smoke.py` | Complete smoke test script covering all phases |
| `artifacts/input_validation_report.json` | Phase 1 artifact — input file existence, shape, and alignment checks |
| `artifacts/label_feasibility_report.json` | Phase 2 artifact — per-label class balance and usability assessment |
| `artifacts/split_manifest.csv` | Phase 3 artifact — deterministic patient-level train/eval split |
| `artifacts/probe_smoke_metrics.json` | Phase 4 artifact — LogisticRegression AUROC per label |
| `EXPERIMENT_LOG.md` | Updated with full chronological run log |
| `RESULT.md` | Created — PASS AS LINEAR PROBE SMOKE TEST |
| `DIFF_SUMMARY.md` | This file |
| `FAILURE_REPORT.md` | Updated — no failures |
| `REVIEW_NOTES_FOR_CODEX.md` | Created — review notes for Codex reviewer |

### Files Modified

| File | Change |
|------|--------|
| `commands.ps1` | Updated with CMD-001 through CMD-005 (5 commands total) |

### Files Read (Read-Only)

| File | Experiment | Read-only access |
|------|-----------|-----------------|
| `sample_manifest.csv` | EXP-0012B | Validated row count and label data |
| `rad_dino_embeddings.npz` | EXP-0013 | Validated shape [100, 768] |
| `rad_dino_embedding_summary.json` | EXP-0013 | Validated 100/100 succeeded |
| `model_output_contract_comparison.json` | EXP-0014 | Read for contract context |
| `cexar_adapter_contract_draft.md` | EXP-0014 | Read for contract context |

### Environment Changes

| Change | Location |
|--------|----------|
| Installed scikit-learn==1.4.2 | .venvs/cexar-foundation (human approved) |
| Installed scipy==1.15.3 (dependency) | .venvs/cexar-foundation |
| Installed joblib==1.5.3 (dependency) | .venvs/cexar-foundation |
| Installed threadpoolctl==3.6.0 (dependency) | .venvs/cexar-foundation |

### No Changes To

- Production code
- EXP-0012B, EXP-0013, or EXP-0014 artifacts
- Standards or manifests
- Global/system Python installation
- System PATH, registry, or environment variables
- Any files outside the experiment folder (except the approved venv package install)

### Wrong-Path Artifact (Not Cleaned)

During the first failed script execution, `input_validation_report.json` was written to a nested wrong path:

```
experiments/EXP-0015-.../experiments/EXP-0015-.../artifacts/input_validation_report.json
```

This file has NOT been deleted per runner protocol. Human approval required for cleanup.

### Compliance Backfill Note

During Codex review, a command ledger gap was found.

`EXPERIMENT_LOG.md` reported two failed script attempts before the successful run:

1. Attempt 1 failed because a relative venv path was not found from the experiment directory.
2. Attempt 2 failed because the script used incorrect BASE path resolution.

These failed attempts were not recorded as separate exact commands in `commands.ps1` at execution time. Because the exact terminal text cannot be verified from the current artifacts, the backfilled entries in `commands.ps1` are explicitly marked as `UNKNOWN - NOT RECORDED AT EXECUTION TIME`.

This is a compliance limitation, not a model-result failure. The final successful run remains traceable through CMD-004 and the generated artifacts.

### Nested Wrong-Path Artifacts

Two wrong-path artifact locations were found during Codex review:

1. `D:\cexar-workbench\experiments\experiments\EXP-0015-rad-dino-linear-probe-smoke-test\artifacts\input_validation_report.json`
2. `D:\cexar-workbench\experiments\EXP-0015-rad-dino-linear-probe-smoke-test\experiments\EXP-0015-rad-dino-linear-probe-smoke-test\artifacts\input_validation_report.json`

These files appear to be leftover `input_validation_report.json` outputs from failed BASE path resolution attempts.

Cleanup status:

- Not deleted.
- Not moved.
- Preserved as evidence.
- Human approval is required before any cleanup command is run.

The correct artifact is:

`D:\cexar-workbench\experiments\EXP-0015-rad-dino-linear-probe-smoke-test\artifacts\input_validation_report.json`