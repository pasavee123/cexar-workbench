# Label Crosswalk: TorchXRayVision DenseNet121 ↔ CheXpert Validation Labels

XRV pathology count: 18
CheXpert validation pathology columns: 14

## Mapped Labels

| XRV Index | XRV Pathology | CheXpert Column |
|-----------|---------------|-----------------|
| 0 | Atelectasis | Atelectasis |
| 1 | Consolidation | Consolidation |
| 3 | Pneumothorax | Pneumothorax |
| 4 | Edema | Edema |
| 7 | Effusion | Pleural Effusion |
| 8 | Pneumonia | Pneumonia |
| 10 | Cardiomegaly | Cardiomegaly |
| 14 | Lung Lesion | Lung Lesion |
| 15 | Fracture | Fracture |
| 16 | Lung Opacity | Lung Opacity |
| 17 | Enlarged Cardiomediastinum | Enlarged Cardiomediastinum |

## Unmapped XRV Pathologies (no matching CheXpert column)

| XRV Index | XRV Pathology | Reason |
|-----------|---------------|--------|
| 2 | Infiltration | No corresponding column in CheXpert valid.csv |
| 5 | Emphysema | No corresponding column in CheXpert valid.csv |
| 6 | Fibrosis | No corresponding column in CheXpert valid.csv |
| 9 | Pleural_Thickening | No corresponding column in CheXpert valid.csv |
| 11 | Nodule | No corresponding column in CheXpert valid.csv |
| 12 | Mass | No corresponding column in CheXpert valid.csv |
| 13 | Hernia | No corresponding column in CheXpert valid.csv |

## Unmapped CheXpert Columns (no matching XRV pathology)

| CheXpert Column |
|----------------|
| No Finding |
| Pleural Other |
| Support Devices |
