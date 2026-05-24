# EXPERIMENT_LOG.md

## Run Metadata

- Experiment: EXP-0014 (multi-model contract comparison)
- Start: 2026-05-24T02:09 UTC+7
- Runner: Kilo (ark-code-latest)
- Python: .venvs\cexar-foundation\Scripts\python.exe (Python 3.10.2, numpy 1.26.4)
- Working directory: experiments\EXP-0014-multimodel-contract-comparison

## Command Log

### A0 — Artifact availability check (2026-05-24T02:09)
- Working directory: D:\cexar-workbench
- Command: Test-Path on all 5 required artifact paths
- Exit code: 0
- Result: All 5 artifacts present (sample_manifest.csv, xrv_chexpert_outputs.csv, metric_sanity.json, rad_dino_embedding_summary.json, rad_dino_embeddings.npz)

### A1 — Check Python in .venvs (2026-05-24T02:10)
- Working directory: D:\cexar-workbench
- Command: python --version (global) → not found; then found venv Pythons via Get-ChildItem
- Exit code: 0
- Result: Python 3.10.2 found in cexar-baseline and cexar-foundation

### A2 — Check numpy availability (2026-05-24T02:10)
- Working directory: D:\cexar-workbench
- Command: & .venvs\cexar-foundation\Scripts\python.exe -c "import numpy"
- Exit code: 0
- Result: numpy 1.26.4 available in cexar-foundation

### A3–A7 — Probe artifact structures (2026-05-24T02:11–02:12)
- Working directory: D:\cexar-workbench
- Commands: Multiple `-c` incantations to read CSV headers, JSON keys, NPZ shapes
- Exit code: 0 (all)
- Results:
  - sample_manifest.csv: 100 rows, 16 columns (indices 0–99)
  - xrv_chexpert_outputs.csv: 100 rows, 20 columns (18 XRV pathologies + image_index + PatientPath)
  - metric_sanity.json: 18 labels, 11 mapped to CheXpert, 9 AUROC computed
  - rad_dino_embedding_summary.json: 100/100 succeeded, shape [100, 768]
  - rad_dino_embeddings.npz: embeddings [100, 768] float32, indices 0–99

### B1 — Create artifacts/ directory (2026-05-24T02:13)
- Working directory: D:\cexar-workbench\experiments\EXP-0014-multimodel-contract-comparison
- Command: mkdir artifacts
- Exit code: 0
- Destructive: no
- Files changed: created artifacts/ directory

### B3 — Additional npz probe (2026-05-24T02:14)
- Working directory: D:\cexar-workbench
- Command: & python.exe -c "..." to read npz indices array
- Exit code: 0
- Result: indices = [0, 1, ..., 99], confirms sequential alignment with manifest

### B4 — Write run_contract_comparison.py (2026-05-24T02:15)
- Working directory: N/A (file write)
- File created: artifacts/run_contract_comparison.py (495 lines)
- No terminal command executed

### B5 — Execute run_contract_comparison.py — Attempt 1 (2026-05-24T02:16)
- Working directory: D:\cexar-workbench\experiments\EXP-0014-multimodel-contract-comparison
- Command: & .venvs\cexar-foundation\Scripts\python.exe artifacts\run_contract_comparison.py
- Exit code: 1
- Error: f-string expression part cannot include a backslash (line 362, 365)
- Fix: Replaced f-string \"{l}\" patterns with pre-computed string variables
- Files changed: run_contract_comparison.py modified

### B5 — Execute run_contract_comparison.py — Attempt 2 (2026-05-24T02:18)
- Working directory: D:\cexar-workbench\experiments\EXP-0014-multimodel-contract-comparison
- Command: & .venvs\cexar-foundation\Scripts\python.exe artifacts\run_contract_comparison.py
- Exit code: 1
- Error: Missing required artifacts — BASE path wrong (only 2 dirnames, needed 3)
- Fix: Changed BASE from os.path.dirname × 2 to os.path.dirname × 3 (script is inside artifacts/)
- Files changed: run_contract_comparison.py modified

### B5 — Execute run_contract_comparison.py — Attempt 3 (2026-05-24T02:20)
- Working directory: D:\cexar-workbench\experiments\EXP-0014-multimodel-contract-comparison
- Command: & .venvs\cexar-foundation\Scripts\python.exe artifacts\run_contract_comparison.py
- Exit code: 0
- Output: Phase 1 PASS, Phase 2 PASS, Phase 4 COMPLETE
- Files created:
  - artifacts/sample_alignment_report.json
  - artifacts/model_output_contract_comparison.json
  - artifacts/cexar_adapter_contract_draft.md

### B6 — Verify output artifacts (2026-05-24T02:21)
- Working directory: D:\cexar-workbench\experiments\EXP-0014-multimodel-contract-comparison
- Command: Get-ChildItem artifacts
- Exit code: 0
- Result: All 3 output files present + run_contract_comparison.py + spurious artifacts/artifacts/ (empty)

## Environment Notes

- Python used: D:\cexar-workbench\.venvs\cexar-foundation\Scripts\python.exe (existing venv, not modified)
- No packages were installed
- No global Python was modified
- No EXP-0012B or EXP-0013 artifacts were modified
- No new model inference was run
- No training, AUROC, or threshold tuning was performed
- No RAD-DINO classification was performed

## Artifacts Produced

1. artifacts/sample_alignment_report.json — 100-image alignment verified, indices matched, no mismatches
2. artifacts/model_output_contract_comparison.json — XRV (classifier) vs RAD-DINO (encoder) contracts
3. artifacts/cexar_adapter_contract_draft.md — Generic CeXaR adapter schema + 2 concrete instances
4. artifacts/run_contract_comparison.py — Comparison script (source)

## Known Issue

A spurious empty directory `artifacts/artifacts/` was created by an initial incorrect os.makedirs call in the first version of run_contract_comparison.py. The directory is empty and harmless. Per cleanup protocol, it was not deleted. If human approval is granted, it can be removed with `Remove-Item artifacts/artifacts`.

## Final Status

PASS — All required artifacts generated, no violations of safety constraints.

### B7 — Create configs/ directory (2026-05-24T02:23)
- Working directory: D:\cexar-workbench\experiments\EXP-0014-multimodel-contract-comparison
- Command: mkdir configs
- Exit code: 0
- Destructive: no
- Purpose: Required directory per TEST_PLAN; no config files needed for read-only comparison