# RUNNER_INSTRUCTIONS.md — EXP-0012B

Use `.venvs\cexar-baseline` from EXP-0010.

Run:

```powershell
.\.venvs\cexar-baseline\Scripts\python.exe experiments\EXP-0012B-xrv-stratified-metric-fix\artifacts\run_xrv_chexpert_metrics_fixed.py
```

Do not modify `D:\Dataset_Chexpert`.

Do not install sklearn or any other packages globally. The script uses a local AUROC implementation.

Do not train, download datasets, or make clinical claims.

## Changes From EXP-0012

1. The script uses `random.Random(42).sample()` instead of "first 100 sorted by Path".
2. The script exits non-zero (code 1) if `num_images_succeeded == 0`.
3. The script produces `sample_manifest.csv` with the exact selected sample.