# DIFF_SUMMARY.md — EXP-0012B

## Files Created

All files in `experiments/EXP-0012B-xrv-stratified-metric-fix/` are new:

```
experiments/EXP-0012B-xrv-stratified-metric-fix/
├── README.md
├── TEST_PLAN.md
├── RUNNER_INSTRUCTIONS.md
├── EXPERIMENT_LOG.md
├── RESULT.md
├── FAILURE_REPORT.md
├── DIFF_SUMMARY.md
├── REVIEW_NOTES_FOR_CODEX.md
├── commands.ps1
├── configs/
└── artifacts/
    ├── label_crosswalk.md
    ├── xrv_chexpert_outputs.csv
    ├── metric_sanity.json
    ├── sample_manifest.csv
    └── run_xrv_chexpert_metrics_fixed.py
```

## Files Modified

None. No production code, manifests, standards, or repo_hunt files were modified.

## Source: EXP-0012

The experiment script `run_xrv_chexpert_metrics_fixed.py` is derived from `EXP-0012/artifacts/run_xrv_chexpert_metrics.py` with two changes:

1. **Silent failure guard** (lines near inference completion): Added check for `num_images_succeeded == 0` that exits with code 1.
2. **Deterministic random sampling** (lines in `load_labels()`): Replaced `frontal.sort(key=lambda r: r["Path"])` / `frontal[:SAMPLE_SIZE]` with `random.Random(42).sample(frontal, min(SAMPLE_SIZE, len(frontal)))`.

## Production Impact

None. This experiment is fully isolated in `experiments/EXP-0012B-xrv-stratified-metric-fix/`.