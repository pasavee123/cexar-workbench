# README.md — EXP-0012B

## Hypothesis

The two weaknesses found in EXP-0012 (silent failure when 0 images succeed, and non-representative "first 100 sorted by Path" sampling) can be fixed by adding a non-zero-exit guard and deterministic random sampling, without changing the XRV baseline pipeline.

## Setup

- Model: TorchXRayVision `densenet121-res224-all` (v1.4.0)
- Data: 100 frontal validation images from `D:\Dataset_Chexpert\archive\valid.csv`
- Environment: `.venvs\cexar-baseline`
- Sample: Deterministic random sample of 100 frontal images with seed 42

## Fixes Applied (vs EXP-0012)

1. **Silent failure guard**: Script exits non-zero (code 1) if `num_images_succeeded == 0`. A run with zero successful inferences must never be reported as success.

2. **Deterministic random sampling**: Replaced "first 100 sorted by Path" with `random.Random(42).sample(frontal_rows, 100)`. This provides a reproducible but non-sorted sample that better represents the validation distribution.

3. **Stratified sampling NOT implemented**: Multi-label stratification across 11 mapped CheXpert labels requires iterative stratification algorithms (e.g., scikit-multilearn) which are not available in the venv. Deterministic random sampling with a fixed seed is used instead — it is simple, reliable, and reproducible.

## Label Crosswalk

Same 11-mapping crosswalk as EXP-0012. See `artifacts/label_crosswalk.md`.

## Metric Sanity Check

AUROC computed for mapped labels where both positive and negative examples exist, using the same local AUROC implementation (no sklearn).

## Status

To be determined after run.

## Medical Limitations

These metrics are pipeline sanity checks only. They use a small deterministic sample (N=100) and do not represent clinical validation. No clinical claims are made.

## Artifacts

- `artifacts/label_crosswalk.md` — Full label crosswalk
- `artifacts/xrv_chexpert_outputs.csv` — Raw XRV outputs for 100 images × 18 pathologies
- `artifacts/metric_sanity.json` — Per-label AUROC summary
- `artifacts/sample_manifest.csv` — Exact selected sample with mapped labels
- `artifacts/run_xrv_chexpert_metrics_fixed.py` — Modified experiment script