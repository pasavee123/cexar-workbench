# TEST_PLAN.md

## Checks

1. Create `.venvs\cexar-baseline` with Python 3.10.
2. Install only `REQUIREMENTS_BASELINE_XRV.txt`.
3. Verify `torch==2.0.1` inside the venv.
4. Load `torchxrayvision` DenseNet121 pretrained weights.
5. Confirm smoke-test output shape is `(1, 18)`.
6. Search for local real CXR files.
7. If no real CXR files exist, run synthetic fallback and save JSON output.

## Success Criteria

- Venv exists and uses `.venvs\cexar-baseline`.
- Baseline package versions match the plan.
- XRV model produces 18 outputs.
- Results are saved to `artifacts/xrv_inference_results.json`.
- Synthetic outputs are clearly labeled as non-medical.

## Failure Criteria

- Any global Python mutation is required.
- Venv cannot run.
- Torch version is not 2.0.1.
- XRV import/model load fails.
- Output shape is not `(1, 18)`.
