# TEST_PLAN.md

## Plan

1. Inspect `D:\Dataset_Chexpert` read-only.
2. Copy 5 frontal validation JPG images into `artifacts/test_images/`.
3. Copy a small matching label subset into `artifacts/sample_labels.csv`.
4. Run TorchXRayVision DenseNet121 from `.venvs\cexar-baseline`.
5. Save output JSON to `artifacts/xrv_real_inference_results.json`.

## Success Criteria

- Five real JPG files are copied into the experiment folder.
- XRV loads with `torchxrayvision==1.4.0`.
- Every image produces 18 outputs.
- No medical claim is made from the outputs.

## Failure Criteria

- Dataset path is unavailable.
- Venv cannot run.
- XRV model load fails.
- Any image cannot be preprocessed.
- Output count differs from 18.
