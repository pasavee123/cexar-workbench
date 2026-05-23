# EXPERIMENT_LOG.md

## Session

Date: 2026-05-23.

## Command Log

### 1. Verify dataset path

- Command: `Test-Path -LiteralPath 'D:\Dataset_Chexpert'`
- Exit code: 0
- Summary: Dataset path exists.

### 2. Inspect dataset root

- Command: `Get-ChildItem -LiteralPath 'D:\Dataset_Chexpert' -Force`
- Exit code: 0
- Summary: Found `archive/`.

### 3. Inspect CSV headers and validation images

- Commands:
  - `Get-Content -LiteralPath 'D:\Dataset_Chexpert\archive\valid.csv' -TotalCount 5`
  - `Get-ChildItem -Path 'D:\Dataset_Chexpert\archive\valid' -Recurse -File`
- Exit code: 0
- Summary: Confirmed CheXpert-style labels and JPG validation images.

### 4. Create experiment folders

- Command: `New-Item -ItemType Directory -Force -Path ...`
- Exit code: 0
- Summary: Created experiment, artifacts, test image, and config folders.

### 5. Copy 5 frontal validation images

- Command: PowerShell `Import-Csv`, `Where-Object Frontal`, and `Copy-Item`.
- Exit code: 0
- Summary: Copied 5 frontal validation images into `artifacts/test_images/` and wrote sample label/manifest CSV files.

### 6. Create inference script and docs

- Command: Codex file patch.
- Exit code: 0
- Summary: Created real-image inference script and experiment documentation.

### 7. Run real CheXpert sample inference

- Command: `.\.venvs\cexar-baseline\Scripts\python.exe experiments\EXP-0011-chexpert-xrv-real-inference\artifacts\run_xrv_real_inference.py`
- Exit code: 0
- Summary: Wrote `artifacts/xrv_real_inference_results.json` for 5 images and 18 XRV pathologies.

### 8. Correct label mapping bug

- Command: Codex file patch.
- Exit code: 0
- Summary: Fixed `run_xrv_real_inference.py` so copied images map to `sample_labels.csv` by sample order. The previous filename-based mapping was unsafe because CheXpert images from different patient folders share names such as `view1_frontal.jpg`.

### 9. Rerun real CheXpert sample inference after mapping fix

- Command: `.\.venvs\cexar-baseline\Scripts\python.exe experiments\EXP-0011-chexpert-xrv-real-inference\artifacts\run_xrv_real_inference.py`
- Exit code: 0
- Summary: Regenerated `artifacts/xrv_real_inference_results.json`. Confirmed 5 images processed and 18 pathologies listed.

## Final Status

PASS AS REAL-IMAGE SMOKE TEST.

This run proves the baseline XRV environment can process real CheXpert JPG images. It does not measure clinical performance.
