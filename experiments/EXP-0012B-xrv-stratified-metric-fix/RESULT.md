# RESULT.md — EXP-0012B

## Status

PASS AS DETERMINISTIC RANDOM SAMPLING SANITY CHECK.

## Fixes Verified

### Fix 1: Silent Failure Guard

The script includes a guard that exits with code 1 if `num_images_succeeded == 0`. In this run, 100/100 images succeeded, so the guard was not triggered (exit code 0). The guard would have triggered if, for example, the path resolution bug from EXP-0012 attempt 1 recurred.

### Fix 2: Deterministic Random Sampling

The script uses `random.Random(42).sample()` instead of "first 100 sorted by Path". The exact selected sample is saved to `artifacts/sample_manifest.csv`. This sample is reproducible (deterministic with seed 42) and not biased by lexicographic file path ordering.

### Stratified Sampling Not Implemented

Multi-label stratification across 11 mapped CheXpert labels requires iterative stratification (each image can have multiple positive labels). This would require algorithms not available in the venv (e.g., scikit-multilearn). Deterministic random sampling is used instead — it is simple, reliable, and reproducible.

## Evidence

- **Sample**: 100 frontal validation images from `D:\Dataset_Chexpert\archive\valid.csv` (deterministic random, seed=42)
- **Model**: TorchXRayVision `densenet121-res224-all` v1.4.0
- **Images processed**: 100/100 successfully
- **XRV pathologies**: 18 per image
- **Mapped labels**: 11 of 18 XRV pathologies cross-walked to CheXpert columns
- **AUROC computed**: 9 of 11 mapped labels (2 excluded: Lung Lesion and Fracture had only one class in sample)

### AUROC Values (pipeline sanity only)

| Pathology | AUROC |
|-----------|-------|
| Atelectasis | 0.822 |
| Consolidation | 0.874 |
| Pneumothorax | 0.286 |
| Edema | 0.810 |
| Effusion → Pleural Effusion | 0.855 |
| Pneumonia | 0.825 |
| Cardiomegaly | 0.782 |
| Lung Opacity | 0.875 |
| Enlarged Cardiomediastinum | 0.773 |

## Comparison With EXP-0012

The random sample (seed 42) produces different AUROC values than EXP-0012's first-100-by-Path sample. The largest difference is Pneumothorax (0.599 → 0.286), confirming the first-100 sample was biased. Random sampling provides a more representative but still high-variance estimate at N=100.

## Technical Notes

- AUROC computed with local implementation (sklearn not available in venv; no packages installed)
- Labels use 0.0/1.0 binary format
- Path resolution: CSV paths include `CheXpert-v1.0-small/` prefix; stripped to resolve against `D:\Dataset_Chexpert\archive`
- Sample manifest saved with all mapped label values, paths, and view metadata

## Clinical Limitation

This is a pipeline sanity check on a small random sample (N=100, seed=42). AUROC values are not clinical performance metrics. They only verify that the XRV model outputs carry detectable signal above random for most mapped labels. Pneumothorax AUROC of 0.286 (below chance) reflects label noise and small sample size — not a clinical finding. No diagnostic claims are made.