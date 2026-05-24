# EXP-0016 command ledger
# Runner must append every exact terminal command before execution.
# Do not summarize multiple commands.

# CMD-001: List dataset root structure
# Purpose: Inventory D:\Dataset_Chexpert
# Working directory: D:\cexar-workbench
# Destructive: No
# Exit code: 0
# Summary: Dataset contains archive/ with train/, valid/, train.csv, valid.csv
Get-ChildItem -Recurse -Depth 2 D:\Dataset_Chexpert | Select-Object FullName, Length, Mode

# CMD-002: Check venv Python and installed packages
# Purpose: Verify .venvs/cexar-foundation is usable
# Working directory: D:\cexar-workbench
# Destructive: No
# Exit code: 0
# Summary: Python 3.10.2, numpy 1.26.4, sklearn 1.4.2, pandas NOT INSTALLED
.venvs\cexar-foundation\Scripts\python.exe -c "import pandas; print('pandas', pandas.__version__)" ; .venvs\cexar-foundation\Scripts\python.exe -c "import numpy; print('numpy', numpy.__version__)" ; .venvs\cexar-foundation\Scripts\python.exe -c "import sklearn; print('sklearn', sklearn.__version__)" ; .venvs\cexar-foundation\Scripts\python.exe --version

# CMD-003: Install pandas into existing venv
# Purpose: Required for CSV analysis, manifest creation, label distribution
# Working directory: D:\cexar-workbench
# Destructive: No (adds package to venv only)
# Exit code: 0
# Summary: pandas==2.2.2 installed with python-dateutil, pytz, tzdata, six
.venvs\cexar-foundation\Scripts\python.exe -m pip install pandas==2.2.2

# CMD-004: Verify pandas installation
# Purpose: Confirm pandas installed correctly
# Working directory: D:\cexar-workbench
# Destructive: No
# Exit code: 0
# Summary: pandas 2.2.2 confirmed
.venvs\cexar-foundation\Scripts\python.exe -c "import pandas as pd; print(pd.__version__)"

# CMD-005: Inspect train.csv - row count, columns, first 5 rows
# Purpose: Identify CSV structure for CheXpert train set
# Working directory: D:\cexar-workbench
# Destructive: No (read-only)
# Exit code: 0
# Summary: 223,414 rows, 19 columns including Path and all 11 CheXpert labels
.venvs\cexar-foundation\Scripts\python.exe -c "import pandas as pd; df = pd.read_csv(r'D:\Dataset_Chexpert\archive\train.csv'); print('ROWS:', len(df)); print('COLUMNS:', list(df.columns)); print(df.head(3).to_string())"

# CMD-006: Inspect valid.csv - row count, columns, first 5 rows
# Purpose: Identify CSV structure for CheXpert valid set
# Working directory: D:\cexar-workbench
# Destructive: No (read-only)
# Exit code: 0
# Summary: 234 rows, same 19 columns as train.csv
.venvs\cexar-foundation\Scripts\python.exe -c "import pandas as pd; df = pd.read_csv(r'D:\Dataset_Chexpert\archive\valid.csv'); print('ROWS:', len(df)); print('COLUMNS:', list(df.columns)); print(df.head(3).to_string())"

# CMD-007: Verify path mapping (NOTE: Superseded by CMD-008; inline command had syntax issues on Windows)
# Result: Superseded by full analysis script CMD-008

# AUDIT-BACKFILL-001: Superseded failed inline path-mapping command
# Purpose: Retroactively document CMD-007 issue reported as "inline command had syntax issues on Windows"
# Backfill reason: commands.ps1 did not record the exact failed inline command text at execution time.
# Destructive: No
# Working directory: D:\cexar-workbench
# Exact command: UNKNOWN - NOT RECORDED AT EXECUTION TIME
# Observed result: Inline command had syntax issues on Windows and was superseded by CMD-008 full analysis script.
# Compliance note: This entry is an audit backfill. It must not be treated as an exact command record.

# CMD-008: Run full scale-up readiness analysis script
# Purpose: Execute all 6 phases (inventory, manifest, labels, split, estimate, readiness)
# Working directory: D:\cexar-workbench
# Destructive: No (writes artifacts only)
# Exit code: 0
# Summary: All 6 phases completed. Result: PASS AS SCALE-UP READINESS CHECK
.venvs\cexar-foundation\Scripts\python.exe experiments\EXP-0016-chexpert-scale-up-readiness\artifacts\run_chexpert_scale_up_readiness.py

# CMD-009: Correction pass - re-run analysis script with fixed split feasibility logic
# Purpose: Codex review found split_feasibility logic only checked positive counts,
#          missing zero-negative and low-count-negative thresholds. Also update
#          phase6 result to PARTIAL PASS and add blocker text.
# Working directory: D:\cexar-workbench
# Destructive: No (overwrites artifacts with corrected versions)
# Exit code: 0
# Summary: 5 labels flagged as needing stratified sampling: Atelectasis, Pneumonia,
#          Lung Lesion, Fracture, Lung Opacity. Result: PARTIAL PASS AS SCALE-UP READINESS CHECK.
.venvs\cexar-foundation\Scripts\python.exe experiments\EXP-0016-chexpert-scale-up-readiness\artifacts\run_chexpert_scale_up_readiness.py

