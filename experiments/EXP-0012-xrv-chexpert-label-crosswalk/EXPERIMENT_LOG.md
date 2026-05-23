# EXPERIMENT_LOG.md — EXP-0012

## Session

Date: 2026-05-23.

## Command Log

### 1. Create experiment folders

- Timestamp: 2026-05-23T20:12
- Working directory: `D:\cexar-workbench`
- Command: `New-Item -ItemType Directory -Force -Path 'experiments\EXP-0012-xrv-chexpert-label-crosswalk\artifacts','experiments\EXP-0012-xrv-chexpert-label-crosswalk\configs'`
- Exit code: 0
- Summary: Created experiment, artifacts, and configs directories.

### 2. Inspect valid.csv headers

- Timestamp: 2026-05-23T20:13
- Working directory: `D:\cexar-workbench`
- Command: `Get-Content -LiteralPath 'D:\Dataset_Chexpert\archive\valid.csv' -TotalCount 1`
- Exit code: 0
- Summary: CheXpert columns: Path, Sex, Age, Frontal/Lateral, AP/PA, No Finding, Enlarged Cardiomediastinum, Cardiomegaly, Lung Opacity, Lung Lesion, Edema, Consolidation, Pneumonia, Atelectasis, Pneumothorax, Pleural Effusion, Pleural Other, Fracture, Support Devices.

### 3. Count frontal validation images

- Timestamp: 2026-05-23T20:13
- Working directory: `D:\cexar-workbench`
- Command: `$csv = Import-Csv ...`
- Exit code: 0
- Summary: Total rows=234, Frontal rows=202. 100-sample target is viable.

### 4. Verify venv Python exists

- Timestamp: 2026-05-23T20:14
- Working directory: `D:\cexar-workbench`
- Command: `Test-Path -LiteralPath '.venvs\cexar-baseline\Scripts\python.exe'`
- Exit code: 0
- Summary: True — venv Python is available.

### 5. Check sklearn availability

- Timestamp: 2026-05-23T20:14
- Working directory: `D:\cexar-workbench`
- Command: `.\.venvs\cexar-baseline\Scripts\python.exe -c "import sklearn; print(sklearn.__version__)"`
- Exit code: 1
- Summary: ModuleNotFoundError — sklearn not installed. Will use local AUROC implementation.

### 6. Check CheXpert label value format

- Timestamp: 2026-05-23T20:15
- Working directory: `D:\cexar-workbench`
- Command: `Get-Content -LiteralPath 'D:\Dataset_Chexpert\archive\valid.csv' -TotalCount 3`
- Exit code: 0
- Summary: Labels use 0.0/1.0 format. No -1.0 uncertainty values observed.

### 7. Check archive directory structure

- Timestamp: 2026-05-23T20:16
- Working directory: `D:\cexar-workbench`
- Command: `Get-ChildItem -LiteralPath 'D:\Dataset_Chexpert\archive' -Directory | Select-Object -ExpandProperty Name`
- Exit code: 0
- Summary: Directories: train, valid.

### 8. Run EXP-0012 metrics script (attempt 1 — FAILED)

- Timestamp: 2026-05-23T20:17
- Working directory: `D:\cexar-workbench`
- Command: `.\.venvs\cexar-baseline\Scripts\python.exe experiments\EXP-0012-xrv-chexpert-label-crosswalk\artifacts\run_xrv_chexpert_metrics.py`
- Exit code: 0 (script exited 0 but with warnings)
- Summary: 0/100 images succeeded. Path resolution bug: `VALID_DIR` was set to `D:\Dataset_Chexpert\archive\valid`, producing double `valid\valid` paths. Fixed `VALID_DIR` to `D:\Dataset_Chexpert\archive`.

### 9. Run EXP-0012 metrics script (attempt 2 — SUCCESS)

- Timestamp: 2026-05-23T20:18
- Working directory: `D:\cexar-workbench`
- Command: `.\.venvs\cexar-baseline\Scripts\python.exe experiments\EXP-0012-xrv-chexpert-label-crosswalk\artifacts\run_xrv_chexpert_metrics.py`
- Exit code: 0
- Summary: 100/100 images processed. Output: 18 pathologies per image.
- Files created/changed: `artifacts/label_crosswalk.md`, `artifacts/xrv_chexpert_outputs.csv`, `artifacts/metric_sanity.json`.

## Metrics Summary

| Label | N | AUROC | Status |
|-------|---|-------|--------|
| Atelectasis | 100 | 0.851 | computed |
| Consolidation | 100 | 0.922 | computed |
| Pneumothorax | 100 | 0.599 | computed |
| Edema | 100 | 0.862 | computed |
| Effusion (→Pleural Effusion) | 100 | 0.849 | computed |
| Pneumonia | 100 | 0.784 | computed |
| Cardiomegaly | 100 | 0.836 | computed |
| Lung Lesion | 100 | — | only one class present |
| Fracture | 100 | — | only one class present |
| Lung Opacity | 100 | 0.874 | computed |
| Enlarged Cardiomediastinum | 100 | 0.820 | computed |

## Final Status

PASS AS METRIC SANITY CHECK.