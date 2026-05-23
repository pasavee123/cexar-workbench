# EXPERIMENT_LOG.md — EXP-0012B

## Session

Date: 2026-05-23.

## Command Log

### 1. Create experiment folders

- Timestamp: 2026-05-23T20:29
- Working directory: `D:\cexar-workbench`
- Command: `New-Item -ItemType Directory -Force -Path 'experiments\EXP-0012B-xrv-stratified-metric-fix\artifacts','experiments\EXP-0012B-xrv-stratified-metric-fix\configs'`
- Exit code: 0
- Summary: Created experiment, artifacts, and configs directories.

### 2. Verify venv Python exists

- Timestamp: 2026-05-23T20:29
- Working directory: `D:\cexar-workbench`
- Command: `Test-Path -LiteralPath '.venvs\cexar-baseline\Scripts\python.exe'`
- Exit code: 0
- Summary: True — venv Python is available.

### 3. Verify CheXpert dataset exists

- Timestamp: 2026-05-23T20:29
- Working directory: `D:\cexar-workbench`
- Command: `Test-Path -LiteralPath 'D:\Dataset_Chexpert\archive\valid.csv'`
- Exit code: 0
- Summary: True — dataset is available.

### 4. Check sklearn availability in venv

- Timestamp: 2026-05-23T20:30
- Working directory: `D:\cexar-workbench`
- Command: `.\.venvs\cexar-baseline\Scripts\python.exe -c "import sklearn; print(sklearn.__version__)"`
- Exit code: 1
- Summary: ModuleNotFoundError — sklearn not installed. Local AUROC implementation used.

### 5. Run EXP-0012B metrics script (SUCCESS)

- Timestamp: 2026-05-23T20:31
- Working directory: `D:\cexar-workbench`
- Command: `.\.venvs\cexar-baseline\Scripts\python.exe experiments\EXP-0012B-xrv-stratified-metric-fix\artifacts\run_xrv_chexpert_metrics_fixed.py`
- Exit code: 0
- Summary: 100/100 images processed. Output: 18 pathologies per image. Silent failure guard not triggered (num_images_succeeded=100 > 0).
- Files created/changed: `artifacts/label_crosswalk.md`, `artifacts/xrv_chexpert_outputs.csv`, `artifacts/metric_sanity.json`, `artifacts/sample_manifest.csv`.

### 6. Verify CSV row counts

- Timestamp: 2026-05-23T20:32
- Working directory: `D:\cexar-workbench`
- Command: `$lines = (Get-Content ...)` x 2
- Exit code: 0
- Summary: xrv_chexpert_outputs.csv = 101 lines (1 header + 100 data), sample_manifest.csv = 101 lines (1 header + 100 data).

## Metrics Summary

| Label | N | AUROC | Status |
|-------|---|-------|--------|
| Atelectasis | 100 | 0.822 | computed |
| Consolidation | 100 | 0.874 | computed |
| Pneumothorax | 100 | 0.286 | computed |
| Edema | 100 | 0.810 | computed |
| Effusion (→Pleural Effusion) | 100 | 0.855 | computed |
| Pneumonia | 100 | 0.825 | computed |
| Cardiomegaly | 100 | 0.782 | computed |
| Lung Lesion | 100 | — | only one class present |
| Fracture | 100 | — | only one class present |
| Lung Opacity | 100 | 0.875 | computed |
| Enlarged Cardiomediastinum | 100 | 0.773 | computed |

## Comparison With EXP-0012

| Pathology | EXP-0012 (first-100) | EXP-0012B (random seed 42) | Delta |
|-----------|---------------------|---------------------------|-------|
| Atelectasis | 0.851 | 0.822 | -0.029 |
| Consolidation | 0.922 | 0.874 | -0.048 |
| Pneumothorax | 0.599 | 0.286 | -0.313 |
| Edema | 0.862 | 0.810 | -0.052 |
| Effusion | 0.849 | 0.855 | +0.006 |
| Pneumonia | 0.784 | 0.825 | +0.041 |
| Cardiomegaly | 0.836 | 0.782 | -0.054 |
| Lung Opacity | 0.874 | 0.875 | +0.001 |
| Enlarged Cardiomediastinum | 0.820 | 0.773 | -0.047 |

Notable: Pneumothorax AUROC dropped from 0.599 to 0.286 — the small sample size and random selection cause high variance for low-prevalence labels. This confirms that the "first 100 sorted by Path" sample in EXP-0012 was not representative.

## Final Status

PASS AS DETERMINISTIC RANDOM SAMPLING SANITY CHECK.