# RESULT.md

## Status

PASS AS REAL-IMAGE SMOKE TEST.

The CheXpert dataset path was found, 5 frontal validation images were copied into the experiment folder, and TorchXRayVision DenseNet121 inference ran successfully in `.venvs\cexar-baseline`.

## Evidence

- Source dataset: `D:\Dataset_Chexpert\archive`
- Copied images: `artifacts/test_images/`
- Sample labels: `artifacts/sample_labels.csv`
- Output artifact: `artifacts/xrv_real_inference_results.json`
- Model: `densenet121-res224-all`
- TorchXRayVision: `1.4.0`
- Images processed: 5
- XRV outputs per image: 18

## Notes

The run verifies preprocessing and model execution on real JPG chest X-ray files. It does not evaluate clinical accuracy yet because EXP-0011 does not include thresholding, uncertainty handling, label crosswalk validation, or metrics.

## Clinical Limitation

Any outputs from this experiment are technical model outputs only. They are not diagnoses and must not be used for clinical decision-making.
