# EXP-0012B commands.ps1
# Generated: 2026-05-23T20:29:00+07:00

# 1. Create experiment folders
New-Item -ItemType Directory -Force -Path 'experiments\EXP-0012B-xrv-stratified-metric-fix\artifacts','experiments\EXP-0012B-xrv-stratified-metric-fix\configs'

# 2. Verify venv Python exists
Test-Path -LiteralPath '.venvs\cexar-baseline\Scripts\python.exe'

# 3. Verify CheXpert dataset exists
Test-Path -LiteralPath 'D:\Dataset_Chexpert\archive\valid.csv'

# 4. Check sklearn availability in venv
.\.venvs\cexar-baseline\Scripts\python.exe -c "import sklearn; print(sklearn.__version__)"

# 5. Run EXP-0012B metrics script
.\.venvs\cexar-baseline\Scripts\python.exe experiments\EXP-0012B-xrv-stratified-metric-fix\artifacts\run_xrv_chexpert_metrics_fixed.py

# 6. Verify CSV row counts
$lines = (Get-Content -LiteralPath 'experiments\EXP-0012B-xrv-stratified-metric-fix\artifacts\xrv_chexpert_outputs.csv' | Measure-Object -Line).Lines; Write-Host "xrv_chexpert_outputs.csv lines: $lines (expected 101: 1 header + 100 data rows)"
$lines = (Get-Content -LiteralPath 'experiments\EXP-0012B-xrv-stratified-metric-fix\artifacts\sample_manifest.csv' | Measure-Object -Line).Lines; Write-Host "sample_manifest.csv lines: $lines (expected 101: 1 header + 100 data rows)"