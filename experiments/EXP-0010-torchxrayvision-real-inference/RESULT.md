# RESULT.md

## Result

PARTIAL PASS.

EXP-0010 successfully created the baseline venv, installed the pinned XRV requirements, verified package versions, loaded TorchXRayVision DenseNet121 pretrained weights, and produced a smoke-test output shape of `(1, 18)`.

No real CXR images were found outside `.venvs`, so real-data inference was not performed. The experiment continued with synthetic HU-range tensors only.

## Evidence

- Venv: `.venvs\cexar-baseline`
- Torch: `2.0.1+cpu`
- TorchVision: `0.15.2+cpu`
- TorchXRayVision: `1.4.0`
- Smoke output shape: `(1, 18)`
- Result artifact: `artifacts/xrv_inference_results.json`

## Clinical Limitation

This experiment does not provide diagnostic evidence. Synthetic outputs must not be interpreted as clinical predictions.

## Configs

`configs/` is empty because this run used the fixed baseline requirement file and a small standalone script rather than a configurable training or evaluation pipeline.
