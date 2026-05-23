# TEST_PLAN.md — EXP-0012B

## Plan

1. Inspect CheXpert validation labels from `D:\Dataset_Chexpert\archive\valid.csv`.
2. Select a deterministic random sample of 100 frontal validation images using `random.Random(42).sample()`.
3. Save the exact selected sample to `artifacts/sample_manifest.csv` with paths, view, and mapped label values.
4. Create label crosswalk between XRV pathologies and CheXpert columns.
5. Run TorchXRayVision DenseNet121 inference on the sample.
6. **Guard**: If `num_images_succeeded == 0`, write failure to `metric_sanity.json`, print error, exit non-zero.
7. Save raw outputs to `artifacts/xrv_chexpert_outputs.csv`.
8. Compute AUROC for each mapped label where both positive and negative examples exist.
9. Save metric summary to `artifacts/metric_sanity.json`.

## Success Criteria

- 100 frontal validation images processed successfully
- Output count is exactly 18 per image
- Label crosswalk documents all 11 mapped and 7 unmapped XRV pathologies
- AUROC computed for all mapped labels with both class values present
- Script exits 0 only when `num_images_succeeded > 0`
- No clinical claims made

## Failure Criteria

- Venv Python cannot run
- TorchXRayVision import fails
- Dataset path unavailable
- Output shape is not 18
- `num_images_succeeded == 0` (guarded by non-zero exit)
- Any command requires modifying global Python
- Any command would delete/recreate .venvs
- Repeated failure occurs twice

## Changes From EXP-0012

| Aspect | EXP-0012 | EXP-0012B |
|--------|----------|-----------|
| Sampling | First 100 sorted by Path | Deterministic random, seed 42 |
| Zero-success exit | Exits 0 (silent failure) | Exits 1 with error |
| Sample manifest | Not produced | `sample_manifest.csv` produced |