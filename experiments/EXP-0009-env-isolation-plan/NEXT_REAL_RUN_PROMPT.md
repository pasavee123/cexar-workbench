# Next Real Run Prompt

## Target Agent

This prompt is written for the strongest available AI agent. The agent must follow `runner_protocol.md` and `experiment_protocol.md`.

## Prompt

```text
You are executing a CeXaR runner session. Your job is to perform the FIRST real-data TorchXRayVision pretrained inference run.

## Mandatory Reading

Read these files first, in this order:

1. standards/runner_protocol.md
2. standards/experiment_protocol.md
3. standards/medical_claims_policy.md
4. standards/integration_gate.md
5. experiments/EXP-0009-env-isolation-plan/ENV_PLAN.md
6. experiments/EXP-0009-env-isolation-plan/REQUIREMENTS_BASELINE_XRV.txt
7. experiments/EXP-0009-env-isolation-plan/GLOBAL_ENV_RISK.md
8. experiments/EXP-0002-torchxrayvision-inspect/RESULT.md
9. experiments/EXP-0002-torchxrayvision-inspect/EXPERIMENT_LOG.md

## Task

Create a new experiment folder:

experiments/EXP-0010-torchxrayvision-real-inference/

Run TorchXRayVision DenseNet121 pretrained inference on a SMALL real CXR subset if real CXR images already exist in the project. If no real CXR images exist, run a synthetic HU-range fallback and clearly label it as synthetic.

Do not train. Do not integrate. Do not make medical claims.

## Phase 0: Environment Setup

1. Read GLOBAL_ENV_RISK.md. Understand that the global Python environment may be contaminated by previous package installs and PyTorch upgrades.

2. Do NOT roll back, repair, uninstall from, or force-reinstall into the global Python environment.

   The global environment must be avoided by this experiment. If any step requires changing global Python, stop and write FAILURE_REPORT.md.

3. Create and activate the baseline venv using an available Python interpreter inside the
   current runner environment.

   Preferred command when the host Python path is visible:

   ```powershell
   & "C:\Users\pasav\AppData\Local\Programs\Python\Python310\python.exe" -m venv .venvs\cexar-baseline
   .\.venvs\cexar-baseline\Scripts\Activate.ps1
   ```

   If that full host path is not recognized, do not keep retrying it. The runner may be inside
   an isolated sandbox or container that cannot see the host filesystem.

   In that case, run a read-only internal runtime audit:

   ```powershell
   Get-Command python -ErrorAction SilentlyContinue
   Get-Command py -ErrorAction SilentlyContinue
   Get-Command python3 -ErrorAction SilentlyContinue
   where.exe python
   where.exe py
   where.exe python3
   ```

   If no usable internal Python interpreter exists, stop and write `FAILURE_REPORT.md` with:

   ```text
   HARD_BLOCKED due to Environment Isolation
   ```

   Recommend that the user open a non-isolated terminal or a new terminal session bound to the
   host machine where Python is accessible, then rerun this experiment.

4. Verify you are inside the venv before any pip or python work:

   ```powershell
   python -c "import sys; assert '.venvs' in sys.prefix, 'NOT IN VENV - ABORT'; print(sys.prefix)"
   ```

   If venv creation or activation fails, stop and write FAILURE_REPORT.md.

5. Install only the pinned baseline requirements inside the active venv:

   ```powershell
   pip install -r experiments\EXP-0009-env-isolation-plan\REQUIREMENTS_BASELINE_XRV.txt
   ```

6. Verify PyTorch inside the venv:

   ```powershell
   python -c "import torch; assert torch.__version__.startswith('2.0.1'), f'WRONG VENV TORCH VERSION: {torch.__version__}'; print(torch.__version__)"
   ```

   If the PyTorch version is not 2.0.1 inside the venv, stop and write FAILURE_REPORT.md.

7. Freeze and save the venv state:

   ```powershell
   pip freeze > experiments\EXP-0010-torchxrayvision-real-inference\artifacts\frozen_pip.txt
   ```

## Phase 1: TorchXRayVision Smoke Test

Reproduce the EXP-0002 smoke test inside the new venv:

```powershell
$env:PYTHONIOENCODING='utf-8'
python -c "import torch, torchxrayvision as xrv; model = xrv.models.DenseNet(weights='densenet121-res224-all'); out = model(torch.rand(1,1,224,224)); print('Output shape:', tuple(out.shape)); print('Pathologies:', model.pathologies)"
```

Expected:

- Output shape is `(1, 18)`
- 18 pathology labels are printed

Log the full command, exit code, and output in EXPERIMENT_LOG.md. If it fails, stop and write FAILURE_REPORT.md.

## Phase 2: Locate Real CXR Data

Search the project for real CXR image files:

```powershell
Get-ChildItem -Recurse -Include *.png,*.jpg,*.jpeg,*.dcm,*.dicom -ErrorAction SilentlyContinue | Select-Object -First 20 FullName
```

If no real CXR images exist in the project:

- Document this in EXPERIMENT_LOG.md.
- Proceed with synthetic HU-range tensors.
- Do not download datasets.

If real CXR images are found:

- Pick up to 5 images as the test subset.
- Copy them to `artifacts/test_images/`.
- Do not modify originals.
- Log source paths and filenames.

## Phase 3: Inference Script

Write `artifacts/run_xrv_inference.py`.

The script must:

- Load TorchXRayVision DenseNet121 once at startup.
- For each input image:
  - Load image using PIL or scikit-image.
  - Convert RGB to grayscale if needed.
  - Resize to 224x224.
  - Convert to tensor shape `[1, 1, 224, 224]`.
  - Normalize/scale into the input range expected by XRV.
  - Run model forward pass.
  - Record 18 logits.
- If no real images exist, generate 5 synthetic tensors in `[-1024, 1024]`, shape `[1, 1, 224, 224]`.
- Save `artifacts/xrv_inference_results.json`.

The JSON must include:

```json
{
  "model": "densenet121-res224-all",
  "torchxrayvision_version": "1.4.0",
  "data_mode": "real_or_synthetic",
  "num_images": 0,
  "pathologies": [],
  "results": []
}
```

Do not present synthetic outputs as medical results.

## Phase 4: Required Documentation

Write all required files inside:

experiments/EXP-0010-torchxrayvision-real-inference/

Required files:

- README.md
- TEST_PLAN.md
- RUNNER_INSTRUCTIONS.md
- EXPERIMENT_LOG.md
- RESULT.md
- FAILURE_REPORT.md
- DIFF_SUMMARY.md
- REVIEW_NOTES_FOR_CODEX.md
- commands.ps1
- artifacts/frozen_pip.txt
- artifacts/run_xrv_inference.py
- artifacts/xrv_inference_results.json

`configs/` may be empty, but explain why in RESULT.md.

## Strict Constraints

- Activate `.venvs\cexar-baseline\Scripts\Activate.ps1` before every pip or python command.
- Never run pip install unless venv activation has been verified.
- Do not modify global Python.
- Do not run rollback commands.
- Do not use `--force-reinstall`.
- Do not install packages outside `REQUIREMENTS_BASELINE_XRV.txt`.
- Do not upgrade torch, torchvision, timm, or numpy.
- Do not download datasets.
- Do not modify files outside `experiments/EXP-0010-torchxrayvision-real-inference/`, except creating/using `.venvs\cexar-baseline`.
- Do not modify production code, manifests, standards, or repo_hunt.
- Do not make clinical claims.
- If the TorchXRayVision model weight download fails, retry once. If it fails again, stop and write FAILURE_REPORT.md.
- Log every command.

## Stop Conditions

Stop and write FAILURE_REPORT.md if:

- Any step requires modifying global Python.
- The full host Python path is not visible and no internal Python runtime exists.
- Venv creation fails.
- Venv activation fails.
- PyTorch inside `.venvs\cexar-baseline` is not 2.0.1.
- TorchXRayVision import fails.
- DenseNet121 weight download fails twice.
- Inference output shape is not `[1, 18]`.
- Any command requires dataset download or private credentials.
```

## Rationale

This prompt intentionally avoids global environment rollback. The next real run should prove that CeXaR can run inside a clean, isolated baseline environment without repairing or mutating the contaminated global Python state.
