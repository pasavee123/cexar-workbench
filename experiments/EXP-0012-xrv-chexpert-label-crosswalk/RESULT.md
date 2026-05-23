# RESULT.md — EXP-0012

## Status

PASS AS METRIC SANITY CHECK.

## Evidence

- **Sample**: 100 frontal validation images from `D:\Dataset_Chexpert\archive\valid.csv` (deterministic, first 100 sorted by Path)
- **Model**: TorchXRayVision `densenet121-res224-all` v1.4.0
- **Images processed**: 100/100 successfully
- **XRV pathologies**: 18 per image
- **Mapped labels**: 11 of 18 XRV pathologies cross-walked to CheXpert columns
- **AUROC computed**: 9 of 11 mapped labels (2 excluded: Lung Lesion and Fracture had only one class in sample)

### AUROC Values (pipeline sanity only)

| Pathology | AUROC |
|-----------|-------|
| Atelectasis | 0.851 |
| Consolidation | 0.922 |
| Pneumothorax | 0.599 |
| Edema | 0.862 |
| Effusion → Pleural Effusion | 0.849 |
| Pneumonia | 0.784 |
| Cardiomegaly | 0.836 |
| Lung Opacity | 0.874 |
| Enlarged Cardiomediastinum | 0.820 |

## Label Crosswalk

11 mappings confirmed. 7 XRV pathologies unmappable to CheXpert columns (Infiltration, Emphysema, Fibrosis, Pleural_Thickening, Nodule, Mass, Hernia). 3 CheXpert columns unmapped to XRV (No Finding, Pleural Other, Support Devices). See `artifacts/label_crosswalk.md`.

## Technical Notes

- AUROC computed with local implementation (sklearn not available in venv; no packages installed)
- Labels use 0.0/1.0 binary format
- Path resolution: CSV paths include `CheXpert-v1.0-small/` prefix; stripped to resolve against `D:\Dataset_Chexpert\archive`

## Clinical Limitation

This is a pipeline sanity check on a small deterministic sample (N=100). AUROC values are not clinical performance metrics. They only verify that the XRV model outputs carry detectable signal above random for mapped labels in this particular data slice. No diagnostic claims are made.