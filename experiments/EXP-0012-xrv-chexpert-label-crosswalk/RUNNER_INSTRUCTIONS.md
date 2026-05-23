# RUNNER_INSTRUCTIONS.md — EXP-0012

Use `.venvs\cexar-baseline` from EXP-0010.

Run:

```powershell
.\.venvs\cexar-baseline\Scripts\python.exe experiments\EXP-0012-xrv-chexpert-label-crosswalk\artifacts\run_xrv_chexpert_metrics.py
```

Do not modify `D:\Dataset_Chexpert`.

Do not install sklearn or any other packages globally. The script uses a local AUROC implementation.

Do not train, download datasets, or make clinical claims.