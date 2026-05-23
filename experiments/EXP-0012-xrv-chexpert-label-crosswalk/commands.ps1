# EXP-0012 commands.ps1
# Generated: 2026-05-23T20:12:00+07:00

# 1. Create experiment folders
New-Item -ItemType Directory -Force -Path 'experiments\EXP-0012-xrv-chexpert-label-crosswalk\artifacts','experiments\EXP-0012-xrv-chexpert-label-crosswalk\configs'

# 2. Inspect valid.csv headers
Get-Content -LiteralPath 'D:\Dataset_Chexpert\archive\valid.csv' -TotalCount 1

# 3. Count frontal validation images
$csv = Import-Csv -LiteralPath 'D:\Dataset_Chexpert\archive\valid.csv'; $frontal = $csv | Where-Object { $_.'Frontal/Lateral' -eq 'Frontal' }; Write-Host "Total rows: $($csv.Count)"; Write-Host "Frontal rows: $($frontal.Count)"

# 4. Verify venv Python exists
Test-Path -LiteralPath '.venvs\cexar-baseline\Scripts\python.exe'

# 5. Check sklearn availability in venv
.\.venvs\cexar-baseline\Scripts\python.exe -c "import sklearn; print(sklearn.__version__)"

# 6. Check CheXpert label value format
Get-Content -LiteralPath 'D:\Dataset_Chexpert\archive\valid.csv' -TotalCount 3

# 7. Check archive directory structure
Get-ChildItem -LiteralPath 'D:\Dataset_Chexpert\archive' -Directory | Select-Object -ExpandProperty Name

# 8. Run EXP-0012 metrics script (attempt 1 - failed: path resolution bug)
.\.venvs\cexar-baseline\Scripts\python.exe experiments\EXP-0012-xrv-chexpert-label-crosswalk\artifacts\run_xrv_chexpert_metrics.py

# 9. Run EXP-0012 metrics script (attempt 2 - fixed VALID_DIR path)
.\.venvs\cexar-baseline\Scripts\python.exe experiments\EXP-0012-xrv-chexpert-label-crosswalk\artifacts\run_xrv_chexpert_metrics.py

# 10. Verify CSV row count (101 = 1 header + 100 data)
$lines = (Get-Content -LiteralPath 'experiments\EXP-0012-xrv-chexpert-label-crosswalk\artifacts\xrv_chexpert_outputs.csv' | Measure-Object -Line).Lines; Write-Host "CSV lines: $lines (expected 101: 1 header + 100 data rows)"