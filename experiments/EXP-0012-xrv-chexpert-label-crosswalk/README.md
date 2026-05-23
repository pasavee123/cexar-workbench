# EXP-0012: XRV CheXpert Label Crosswalk

## Hypothesis

TorchXRayVision DenseNet121 pathology outputs can be mapped to CheXpert validation labels, and a pipeline-level sanity check using AUROC can verify that the inferred scores carry signal above random for mapped label pairs.

## Setup

- Model: TorchXRayVision `densenet121-res224-all` (v1.4.0)
- Data: 100 frontal validation images from `D:\Dataset_Chexpert\archive\valid.csv`
- Environment: `.venvs\cexar-baseline`
- Sample: First 100 frontal images, sorted by Path (deterministic)

## Label Crosswalk

11 of 18 XRV pathologies have a direct mapping to a CheXpert validation column. 7 XRV pathologies (Infiltration, Emphysema, Fibrosis, Pleural_Thickening, Nodule, Mass, Hernia) have no matching CheXpert column. 3 CheXpert columns (No Finding, Pleural Other, Support Devices) lack a matching XRV pathology.

Full crosswalk: `artifacts/label_crosswalk.md`

## Metric Sanity Check

AUROC computed for 9/11 mapped labels using a local implementation (sklearn not needed). 2 labels (Lung Lesion, Fracture) had only one class in the sample — AUROC could not be computed.

Full metrics: `artifacts/metric_sanity.json`

## Status

PASS AS METRIC SANITY CHECK.

## Medical Limitations

These metrics are pipeline sanity checks only. They use a small deterministic sample (N=100) and do not represent clinical validation. No clinical claims are made.

## Artifacts

- `artifacts/label_crosswalk.md` — Full label crosswalk
- `artifacts/xrv_chexpert_outputs.csv` — Raw XRV outputs for 100 images × 18 pathologies
- `artifacts/metric_sanity.json` — Per-label AUROC summary
- `artifacts/run_xrv_chexpert_metrics.py` — Experiment script