# commands.ps1
#
# Command ledger for EXP-0010. Commands after the stop condition were not run.

Get-Content -LiteralPath 'experiments/EXP-0009-env-isolation-plan/NEXT_REAL_RUN_PROMPT.md'
Get-ChildItem -LiteralPath 'experiments'
git status --short
Get-Content -LiteralPath 'standards/runner_protocol.md'
Get-Content -LiteralPath 'standards/experiment_protocol.md'
Get-Content -LiteralPath 'standards/medical_claims_policy.md'
Get-Content -LiteralPath 'standards/integration_gate.md'
Get-Content -LiteralPath 'experiments/EXP-0009-env-isolation-plan/ENV_PLAN.md'
Get-Content -LiteralPath 'experiments/EXP-0009-env-isolation-plan/REQUIREMENTS_BASELINE_XRV.txt'
Get-Content -LiteralPath 'experiments/EXP-0009-env-isolation-plan/GLOBAL_ENV_RISK.md'
Get-Content -LiteralPath 'experiments/EXP-0002-torchxrayvision-inspect/RESULT.md'
Get-Content -LiteralPath 'experiments/EXP-0002-torchxrayvision-inspect/EXPERIMENT_LOG.md'
New-Item -ItemType Directory -Force -Path 'experiments\EXP-0010-torchxrayvision-real-inference','experiments\EXP-0010-torchxrayvision-real-inference\artifacts','experiments\EXP-0010-torchxrayvision-real-inference\configs' | Select-Object FullName
python -m venv .venvs\cexar-baseline
python --version
py -0p
Get-Content -LiteralPath 'experiments/EXP-0010-torchxrayvision-real-inference/RESUME_FROM_FAILURE.md'
Get-Content -LiteralPath 'experiments/EXP-0010-torchxrayvision-real-inference/EXPERIMENT_LOG.md'
Get-Content -LiteralPath 'experiments/EXP-0010-torchxrayvision-real-inference/commands.ps1'
& "C:\Users\pasav\AppData\Local\Programs\Python\Python310\python.exe" -m venv .venvs\cexar-baseline
Get-Content -LiteralPath 'experiments/EXP-0010-torchxrayvision-real-inference/FAILURE_REPORT.md'
Get-Content -LiteralPath 'experiments/EXP-0010-torchxrayvision-real-inference/EXPERIMENT_LOG.md' | Select-Object -Last 80
Get-Content -LiteralPath 'experiments/EXP-0010-torchxrayvision-real-inference/commands.ps1' | Select-Object -Last 20
& "C:\Users\pasav\AppData\Local\Programs\Python\Python310\python.exe" --version
Test-Path -LiteralPath 'C:\Users\pasav\AppData\Local\Programs\Python\Python310\python.exe'
Get-Command python -ErrorAction SilentlyContinue
Get-Command py -ErrorAction SilentlyContinue
where.exe python
where.exe py
& "C:\Users\pasav\AppData\Local\Programs\Python\Python310\python.exe" -m venv .venvs\cexar-baseline
.\.venvs\cexar-baseline\Scripts\python.exe -c "import sys; print(sys.executable); print(sys.prefix); assert '.venvs' in sys.prefix"
.\.venvs\cexar-baseline\Scripts\python.exe -m pip install -r experiments\EXP-0009-env-isolation-plan\REQUIREMENTS_BASELINE_XRV.txt
.\.venvs\cexar-baseline\Scripts\python.exe -c "import torch, torchvision, torchxrayvision as xrv; print('torch', torch.__version__); print('torchvision', torchvision.__version__); print('xrv', xrv.__version__); assert torch.__version__.startswith('2.0.1')"
.\.venvs\cexar-baseline\Scripts\python.exe -m pip freeze | Out-File -FilePath 'experiments\EXP-0010-torchxrayvision-real-inference\artifacts\frozen_pip.txt' -Encoding utf8
$env:PYTHONIOENCODING='utf-8'; .\.venvs\cexar-baseline\Scripts\python.exe -c "import torch, torchxrayvision as xrv; model = xrv.models.DenseNet(weights='densenet121-res224-all'); out = model(torch.rand(1,1,224,224)); print('Output shape:', tuple(out.shape)); print('Pathologies:', model.pathologies)"
Get-ChildItem -Path . -Recurse -Include *.png,*.jpg,*.jpeg,*.dcm,*.dicom -ErrorAction SilentlyContinue | Where-Object { $_.FullName -notlike '*\.venvs\*' } | Select-Object -First 20 FullName
.\.venvs\cexar-baseline\Scripts\python.exe experiments\EXP-0010-torchxrayvision-real-inference\artifacts\run_xrv_inference.py
