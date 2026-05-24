# EXP-0015 command ledger
# Runner must append every exact terminal command before execution.
# Do not summarize multiple commands.

# CMD-001: Install scikit-learn into .venvs/cexar-foundation (human approved)
# Purpose: Required for linear probe smoke test
# Destructive: No
# Working directory: D:\cexar-workbench
.\.venvs\cexar-foundation\Scripts\python.exe -m pip install scikit-learn==1.4.2

# CMD-002: Verify scikit-learn version in venv
# Purpose: Confirm scikit-learn installed correctly
# Destructive: No
# Working directory: D:\cexar-workbench
.\.venvs\cexar-foundation\Scripts\python.exe -c "import sklearn; print(sklearn.__version__)"

# CMD-003: Create smoke test script
# Purpose: Write the complete linear probe smoke test Python script
# Destructive: No (creates new file)
# Working directory: D:\cexar-workbench\experiments\EXP-0015-rad-dino-linear-probe-smoke-test
# File created: artifacts/run_rad_dino_linear_probe_smoke.py

# AUDIT-BACKFILL-001: Failed script execution attempt 1
# Purpose: Retroactively document failed attempt reported in EXPERIMENT_LOG.md
# Backfill reason: EXPERIMENT_LOG.md reports "Attempt 1 failed: relative venv path not found from experiment directory", but the exact terminal command was not recorded in commands.ps1 at execution time.
# Destructive: No
# Working directory: D:\cexar-workbench\experiments\EXP-0015-rad-dino-linear-probe-smoke-test
# Exact command: UNKNOWN - NOT RECORDED AT EXECUTION TIME
# Observed result: Failed before successful run; relative venv path was not found from experiment directory.
# Compliance note: This entry is an audit backfill. It must not be treated as an exact command record.

# AUDIT-BACKFILL-002: Failed script execution attempt 2
# Purpose: Retroactively document failed attempt reported in EXPERIMENT_LOG.md
# Backfill reason: EXPERIMENT_LOG.md reports "Attempt 2 failed: BASE path resolution error (3 dirnames instead of 4)", but commands.ps1 did not contain a separate exact command entry for this failed attempt.
# Destructive: No
# Working directory: D:\cexar-workbench\experiments\EXP-0015-rad-dino-linear-probe-smoke-test
# Exact command: UNKNOWN - NOT RECORDED AS A SEPARATE COMMAND AT EXECUTION TIME
# Observed result: Failed after writing wrong-path input_validation_report.json due to incorrect BASE path resolution.
# Compliance note: This entry is an audit backfill. It must not be treated as an exact command record.

# CMD-004: Execute smoke test script - successful recorded run
# Purpose: Run all phases (input validation, label feasibility, split, probe training)
# Destructive: No
# Working directory: D:\cexar-workbench\experiments\EXP-0015-rad-dino-linear-probe-smoke-test
D:\cexar-workbench\.venvs\cexar-foundation\Scripts\python.exe artifacts\run_rad_dino_linear_probe_smoke.py

# CMD-005: List generated artifacts
# Purpose: Verify all output files created
# Destructive: No
# Working directory: D:\cexar-workbench\experiments\EXP-0015-rad-dino-linear-probe-smoke-test
Get-ChildItem -Path "artifacts" | Select-Object Name

