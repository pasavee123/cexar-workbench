# EXP-0014 command ledger
# All commands registered and executed.
# Run completed: 2026-05-24T02:20 UTC+7

# A0: Verify required artifacts exist (inspection only)
# EXECUTED: Test-Path on all 5 artifact paths
# Result: All present

# A1: Check Python in .venvs
# EXECUTED: Get-ChildItem .venvs; & .venvs\cexar-foundation\Scripts\python.exe --version
# Result: Python 3.10.2

# A2: Verify numpy in cexar-foundation venv
# EXECUTED: & .venvs\cexar-foundation\Scripts\python.exe -c "import numpy; print('numpy', numpy.__version__)"
# Result: numpy 1.26.4

# A3–A6: Probe artifact structures (read-only)
# EXECUTED: Multiple -c incantations reading CSV headers, JSON keys, NPZ shapes
# Result: All structures confirmed

# B1: Create artifacts/ directory
# EXECUTED: mkdir artifacts
# Destructive: no
# Source: none
# Destination: experiments/EXP-0014-multimodel-contract-comparison/artifacts/

# B3: Probe npz indices array
# EXECUTED: & .venvs\cexar-foundation\Scripts\python.exe -c "..."
# Result: indices = [0..99], sequential

# B4: Write run_contract_comparison.py
# EXECUTED: Write tool (no terminal command)
# Created: artifacts/run_contract_comparison.py

# B5 Attempt 1: Execute run_contract_comparison.py
# EXECUTED: & "D:\cexar-workbench\.venvs\cexar-foundation\Scripts\python.exe" artifacts\run_contract_comparison.py
# Exit code: 1 — f-string backslash error
# Fixed: replaced f'\"{l}\"' with pre-computed strings

# B5 Attempt 2: Execute run_contract_comparison.py
# EXECUTED: & "D:\cexar-workbench\.venvs\cexar-foundation\Scripts\python.exe" artifacts\run_contract_comparison.py
# Exit code: 1 — BASE path too short (artifacts dir not found)
# Fixed: added third os.path.dirname to BASE computation

# B5 Attempt 3: Execute run_contract_comparison.py
# EXECUTED: & "D:\cexar-workbench\.venvs\cexar-foundation\Scripts\python.exe" artifacts\run_contract_comparison.py
# Working directory: experiments\EXP-0014-multimodel-contract-comparison
# Exit code: 0
# Outputs:
#   - artifacts/sample_alignment_report.json
#   - artifacts/model_output_contract_comparison.json
#   - artifacts/cexar_adapter_contract_draft.md

# B7: Create configs/ directory
# EXECUTED: mkdir configs
# Destructive: no
# Source: none
# Destination: experiments/EXP-0014-multimodel-contract-comparison/configs/
# Purpose: Required directory per TEST_PLAN; no config files needed for read-only comparison