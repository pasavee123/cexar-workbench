# commands.ps1

Test-Path -LiteralPath 'D:\Dataset_Chexpert'
Get-ChildItem -LiteralPath 'D:\Dataset_Chexpert' -Force | Select-Object Name,Mode,Length
Get-Content -LiteralPath 'D:\Dataset_Chexpert\archive\valid.csv' -TotalCount 5
Get-Content -LiteralPath 'D:\Dataset_Chexpert\archive\train.csv' -TotalCount 3
Get-ChildItem -Path 'D:\Dataset_Chexpert\archive\valid' -Recurse -File -ErrorAction SilentlyContinue | Select-Object -First 20 FullName,Length,Extension
New-Item -ItemType Directory -Force -Path 'experiments\EXP-0011-chexpert-xrv-real-inference','experiments\EXP-0011-chexpert-xrv-real-inference\artifacts','experiments\EXP-0011-chexpert-xrv-real-inference\artifacts\test_images','experiments\EXP-0011-chexpert-xrv-real-inference\configs' | Select-Object FullName
$rows = Import-Csv -LiteralPath 'D:\Dataset_Chexpert\archive\valid.csv' | Where-Object { $_.'Frontal/Lateral' -eq 'Frontal' } | Select-Object -First 5
$rows | Select-Object Path,Sex,Age,'Frontal/Lateral','AP/PA','No Finding','Cardiomegaly','Edema','Pneumonia','Atelectasis','Pleural Effusion' | Export-Csv -NoTypeInformation -Path 'experiments\EXP-0011-chexpert-xrv-real-inference\artifacts\sample_labels.csv'
.\.venvs\cexar-baseline\Scripts\python.exe experiments\EXP-0011-chexpert-xrv-real-inference\artifacts\run_xrv_real_inference.py
