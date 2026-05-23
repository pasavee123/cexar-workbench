# TEST_PLAN.md — EXP-0012

## Plan

1. Inspect CheXpert validation labels from `D:\Dataset_Chexpert\archive\valid.csv`.
2. Select a deterministic sample of 100 frontal validation images (first 100 sorted by Path).
3. Create label crosswalk between XRV pathologies and CheXpert columns.
4. Run TorchXRayVision DenseNet121 inference on the sample.
5. Save raw outputs to `artifacts/xrv_chexpert_outputs.csv`.
6. Compute AUROC for each mapped label where both positive and negative examples exist.
7. Save metric summary to `artifacts/metric_sanity.json`.

## Success Criteria

- 100 frontal validation images processed successfully
- Output count is exactly 18 per image
- Label crosswalk documents all 11 mapped and 7 unmapped XRV pathologies
- AUROC computed for all mapped labels with both class values present
- No clinical claims made

## Failure Criteria

- Venv Python cannot run
- TorchXRayVision import fails
- Dataset path unavailable
- Output shape is not 18
- Any command requires modifying global Python
- Repeated failure occurs twice