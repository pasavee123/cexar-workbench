# EXPERIMENT_LOG.md

## Session

Date: 2026-05-23 local environment date.

Outcome: FAILED during Phase 0 environment setup.

## Command Log

### 1. Read next-run prompt

- Working directory: `D:\cexar-workbench`
- Command: `Get-Content -LiteralPath 'experiments/EXP-0009-env-isolation-plan/NEXT_REAL_RUN_PROMPT.md'`
- Exit code: 0
- Summary: Read the EXP-0010 instructions, including mandatory readings, strict constraints, and stop conditions.
- Output files changed: None.

### 2. List existing experiments

- Working directory: `D:\cexar-workbench`
- Command: `Get-ChildItem -LiteralPath 'experiments'`
- Exit code: 0
- Summary: Confirmed EXP-0010 did not already exist; EXP-0001 through EXP-0009 were present.
- Output files changed: None.

### 3. Check git status

- Working directory: `D:\cexar-workbench`
- Command: `git status --short`
- Exit code: 1
- Summary: Failed with `fatal: not a git repository (or any of the parent directories): .git`.
- Output files changed: None.

### 4. Read runner protocol

- Working directory: `D:\cexar-workbench`
- Command: `Get-Content -LiteralPath 'standards/runner_protocol.md'`
- Exit code: 0
- Summary: Read runner role, allowed and forbidden actions, logging requirements, and stop conditions.
- Output files changed: None.

### 5. Read experiment protocol

- Working directory: `D:\cexar-workbench`
- Command: `Get-Content -LiteralPath 'standards/experiment_protocol.md'`
- Exit code: 0
- Summary: Read experiment boundaries, required files, success criteria, and failure criteria.
- Output files changed: None.

### 6. Read medical claims policy

- Working directory: `D:\cexar-workbench`
- Command: `Get-Content -LiteralPath 'standards/medical_claims_policy.md'`
- Exit code: 0
- Summary: Read allowed wording, forbidden claims, and required limitations.
- Output files changed: None.

### 7. Read integration gate

- Working directory: `D:\cexar-workbench`
- Command: `Get-Content -LiteralPath 'standards/integration_gate.md'`
- Exit code: 0
- Summary: Read integration prerequisites and medical AI checks.
- Output files changed: None.

### 8. Read environment plan

- Working directory: `D:\cexar-workbench`
- Command: `Get-Content -LiteralPath 'experiments/EXP-0009-env-isolation-plan/ENV_PLAN.md'`
- Exit code: 0
- Summary: Read baseline environment plan and known global environment risks. The rollback section conflicts with the EXP-0010 prompt and user instruction, so no rollback was performed.
- Output files changed: None.

### 9. Read baseline requirements

- Working directory: `D:\cexar-workbench`
- Command: `Get-Content -LiteralPath 'experiments/EXP-0009-env-isolation-plan/REQUIREMENTS_BASELINE_XRV.txt'`
- Exit code: 0
- Summary: Read pinned baseline package requirements.
- Output files changed: None.

### 10. Read global environment risk report

- Working directory: `D:\cexar-workbench`
- Command: `Get-Content -LiteralPath 'experiments/EXP-0009-env-isolation-plan/GLOBAL_ENV_RISK.md'`
- Exit code: 0
- Summary: Read documented global Python contamination risk. No global rollback or repair commands were run.
- Output files changed: None.

### 11. Read EXP-0002 result

- Working directory: `D:\cexar-workbench`
- Command: `Get-Content -LiteralPath 'experiments/EXP-0002-torchxrayvision-inspect/RESULT.md'`
- Exit code: 0
- Summary: Read prior XRV smoke-test result and preprocessing notes.
- Output files changed: None.

### 12. Read EXP-0002 experiment log

- Working directory: `D:\cexar-workbench`
- Command: `Get-Content -LiteralPath 'experiments/EXP-0002-torchxrayvision-inspect/EXPERIMENT_LOG.md'`
- Exit code: 0
- Summary: Read prior XRV install/load/forward-pass log, including Windows UTF-8 workaround.
- Output files changed: None.

### 13. Create EXP-0010 directories

- Working directory: `D:\cexar-workbench`
- Command: `New-Item -ItemType Directory -Force -Path 'experiments\EXP-0010-torchxrayvision-real-inference','experiments\EXP-0010-torchxrayvision-real-inference\artifacts','experiments\EXP-0010-torchxrayvision-real-inference\configs' | Select-Object FullName`
- Exit code: 0
- Summary: Created experiment root, `artifacts/`, and `configs/`.
- Output files changed: `experiments/EXP-0010-torchxrayvision-real-inference/`, `artifacts/`, `configs/`.

### 14. Attempt venv creation

- Working directory: `D:\cexar-workbench`
- Command: `python -m venv .venvs\cexar-baseline`
- Exit code: 1
- Summary: Failed because `python` is not recognized as a command in this PowerShell environment.
- Output files changed: None.

## Stop

The run stopped immediately after command 14 because venv creation failure is a stop condition in the EXP-0010 prompt.

## Follow-up Command Log

### 15. Verify `python` availability

- Working directory: `D:\cexar-workbench`
- Command: `python --version`
- Exit code: 1
- Summary: Failed because `python` is not recognized as a command in this PowerShell environment.
- Output files changed: None.

### 16. Check Windows Python launcher paths

- Working directory: `D:\cexar-workbench`
- Command: `py -0p`
- Exit code: 0
- Summary: The launcher ran but reported `No Installed Pythons Found!`; no full Python executable path was available.
- Output files changed: None.

## Follow-up Stop

The run remains stopped because neither `python --version` nor `py -0p` provided a usable Python executable for creating `.venvs/cexar-baseline`.

## Resume From Failure Command Log

### 17. Read resume instructions

- Working directory: `D:\cexar-workbench`
- Command: `Get-Content -LiteralPath 'experiments/EXP-0010-torchxrayvision-real-inference/RESUME_FROM_FAILURE.md'`
- Exit code: 0
- Summary: Read the instruction to resume Phase 0 using the exact full Python path `C:\Users\pasav\AppData\Local\Programs\Python\Python310\python.exe`, without using `py` or relying on `python` from PATH before venv activation.
- Output files changed: None.

### 18. Read current experiment log

- Working directory: `D:\cexar-workbench`
- Command: `Get-Content -LiteralPath 'experiments/EXP-0010-torchxrayvision-real-inference/EXPERIMENT_LOG.md'`
- Exit code: 0
- Summary: Reviewed prior logged stop state before continuing.
- Output files changed: None.

### 19. Read current command ledger

- Working directory: `D:\cexar-workbench`
- Command: `Get-Content -LiteralPath 'experiments/EXP-0010-torchxrayvision-real-inference/commands.ps1'`
- Exit code: 0
- Summary: Reviewed prior command ledger before continuing.
- Output files changed: None.

### 20. Attempt venv creation with exact provided path

- Working directory: `D:\cexar-workbench`
- Command: `& "C:\Users\pasav\AppData\Local\Programs\Python\Python310\python.exe" -m venv .venvs\cexar-baseline`
- Exit code: 1
- Summary: Failed because the provided executable path was not recognized as a command, script file, or operable program in this environment.
- Output files changed: None.

### 21. Read failure report for update context

- Working directory: `D:\cexar-workbench`
- Command: `Get-Content -LiteralPath 'experiments/EXP-0010-torchxrayvision-real-inference/FAILURE_REPORT.md'`
- Exit code: 0
- Summary: Read current failure report before appending the resume-attempt failure.
- Output files changed: None.

### 22. Read log tail for update context

- Working directory: `D:\cexar-workbench`
- Command: `Get-Content -LiteralPath 'experiments/EXP-0010-torchxrayvision-real-inference/EXPERIMENT_LOG.md' | Select-Object -Last 80`
- Exit code: 0
- Summary: Read the log tail to place the resume command entries correctly.
- Output files changed: None.

### 23. Read command ledger tail for update context

- Working directory: `D:\cexar-workbench`
- Command: `Get-Content -LiteralPath 'experiments/EXP-0010-torchxrayvision-real-inference/commands.ps1' | Select-Object -Last 20`
- Exit code: 0
- Summary: Read the command ledger tail to append new commands.
- Output files changed: None.

## Resume Stop

The run stopped again at Phase 0 because venv creation did not succeed. No `py` command, PATH-based `python` command, pip command, install, rollback, or global Python modification was attempted.

## Admin Rerun Command Log

### 24. Verify host Python path from default sandbox

- Working directory: `D:\cexar-workbench`
- Command: `& "C:\Users\pasav\AppData\Local\Programs\Python\Python310\python.exe" --version`
- Exit code: 1
- Summary: The default agent shell still could not recognize the host Python executable.
- Output files changed: None.

### 25. Check host Python path visibility

- Working directory: `D:\cexar-workbench`
- Command: `Test-Path -LiteralPath 'C:\Users\pasav\AppData\Local\Programs\Python\Python310\python.exe'`
- Exit code: 1
- Summary: Returned `Access is denied`, confirming the default agent shell still had a sandbox boundary around the host path.
- Output files changed: None.

### 26. Create baseline venv from host Python with elevated execution

- Working directory: `D:\cexar-workbench`
- Command: `& "C:\Users\pasav\AppData\Local\Programs\Python\Python310\python.exe" -m venv .venvs\cexar-baseline`
- Exit code: 0
- Summary: Created `.venvs\cexar-baseline` successfully using the host Python 3.10 executable through an elevated/outside-sandbox execution path.
- Output files changed: `.venvs\cexar-baseline/`.

### 27. Verify venv from default sandbox

- Working directory: `D:\cexar-workbench`
- Command: `.\.venvs\cexar-baseline\Scripts\python.exe -c "import sys; print(sys.executable); print(sys.prefix); assert '.venvs' in sys.prefix"`
- Exit code: 1
- Summary: The default sandbox could see the venv files but could not execute the venv Python because it resolves back to the inaccessible host base interpreter.
- Output files changed: None.

### 28. Verify venv with elevated execution

- Working directory: `D:\cexar-workbench`
- Command: `.\.venvs\cexar-baseline\Scripts\python.exe -c "import sys; print(sys.executable); print(sys.prefix); assert '.venvs' in sys.prefix"`
- Exit code: 0
- Summary: Confirmed the venv executable and prefix are both inside `D:\cexar-workbench\.venvs\cexar-baseline`.
- Output files changed: None.

### 29. Install baseline requirements inside venv

- Working directory: `D:\cexar-workbench`
- Command: `.\.venvs\cexar-baseline\Scripts\python.exe -m pip install -r experiments\EXP-0009-env-isolation-plan\REQUIREMENTS_BASELINE_XRV.txt`
- Exit code: 124 from the tool wrapper timeout, then the background install completed successfully.
- Summary: The command exceeded the 10-minute tool timeout while downloading/installing packages. A later check showed the expected baseline packages were installed in `.venvs\cexar-baseline`.
- Output files changed: `.venvs\cexar-baseline\Lib\site-packages\`.

### 30. Verify baseline package versions

- Working directory: `D:\cexar-workbench`
- Command: `.\.venvs\cexar-baseline\Scripts\python.exe -c "import torch, torchvision, torchxrayvision as xrv; print('torch', torch.__version__); print('torchvision', torchvision.__version__); print('xrv', xrv.__version__); assert torch.__version__.startswith('2.0.1')"`
- Exit code: 0
- Summary: Verified `torch 2.0.1+cpu`, `torchvision 0.15.2+cpu`, and `torchxrayvision 1.4.0`.
- Output files changed: None.

### 31. Save pip freeze

- Working directory: `D:\cexar-workbench`
- Command: `.\.venvs\cexar-baseline\Scripts\python.exe -m pip freeze | Out-File -FilePath 'experiments\EXP-0010-torchxrayvision-real-inference\artifacts\frozen_pip.txt' -Encoding utf8`
- Exit code: 0
- Summary: Saved the exact installed package list for reproducibility.
- Output files changed: `artifacts/frozen_pip.txt`.

### 32. Run XRV DenseNet121 smoke test

- Working directory: `D:\cexar-workbench`
- Command: `$env:PYTHONIOENCODING='utf-8'; .\.venvs\cexar-baseline\Scripts\python.exe -c "import torch, torchxrayvision as xrv; model = xrv.models.DenseNet(weights='densenet121-res224-all'); out = model(torch.rand(1,1,224,224)); print('Output shape:', tuple(out.shape)); print('Pathologies:', model.pathologies)"`
- Exit code: 0
- Summary: Model loaded and produced output shape `(1, 18)`. The expected XRV warning appeared because the smoke-test tensor was in `[0, 1]`, not XRV's expected `[-1024, 1024]` range.
- Output files changed: None.

### 33. Search for local real CXR files

- Working directory: `D:\cexar-workbench`
- Command: `Get-ChildItem -Path . -Recurse -Include *.png,*.jpg,*.jpeg,*.dcm,*.dicom -ErrorAction SilentlyContinue | Where-Object { $_.FullName -notlike '*\.venvs\*' } | Select-Object -First 20 FullName`
- Exit code: 0
- Summary: No real CXR image files were found outside `.venvs`.
- Output files changed: None.

### 34. Create synthetic fallback inference script

- Working directory: `D:\cexar-workbench`
- Command: file edit via Codex patch.
- Exit code: 0
- Summary: Created `artifacts/run_xrv_inference.py` to run 5 synthetic HU-range tensors through XRV and save JSON output.
- Output files changed: `artifacts/run_xrv_inference.py`.

### 35. Run synthetic fallback inference

- Working directory: `D:\cexar-workbench`
- Command: `.\.venvs\cexar-baseline\Scripts\python.exe experiments\EXP-0010-torchxrayvision-real-inference\artifacts\run_xrv_inference.py`
- Exit code: 0
- Summary: Saved `artifacts/xrv_inference_results.json` with 5 synthetic inputs and 18 pathology logits per input. These are technical smoke-test outputs only, not medical predictions.
- Output files changed: `artifacts/xrv_inference_results.json`.

## Final Status

PARTIAL PASS.

The environment, package verification, model load, smoke test, and synthetic fallback inference passed. Real CXR inference was not run because no real CXR images were found in the repository.
