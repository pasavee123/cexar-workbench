# EXPERIMENT_LOG.md

## Status

COMPLETE — All phases passed. 8 of 11 labels completed smoke probe with trainable pipeline.

## Run Log

### 2026-05-24T12:44:12+07:00 — Phase 0: Safety and Preflight

- All required protocol documents read.
- `.venvs/cexar-foundation` present.
- numpy 1.26.4 available; scikit-learn missing.
- Human approved installation of scikit-learn==1.4.2.

### 2026-05-24T12:44:12+07:00 — CMD-001: Install scikit-learn

- Working directory: D:\cexar-workbench
- Command: `.\\.venvs\\cexar-foundation\\Scripts\\python.exe -m pip install scikit-learn==1.4.2`
- Exit code: 0
- Summary: Installed scikit-learn-1.4.2, scipy-1.15.3, joblib-1.5.3, threadpoolctl-3.6.0
- Files changed: .venvs/cexar-foundation/Lib/site-packages/ (new packages installed)

### 2026-05-24T12:44:12+07:00 — CMD-002: Verify scikit-learn

- Working directory: D:\cexar-workbench
- Command: `.\\.venvs\\cexar-foundation\\Scripts\\python.exe -c "import sklearn; print(sklearn.__version__)"`
- Exit code: 0
- Summary: scikit-learn version 1.4.2 confirmed.
- Files changed: None

### 2026-05-24T12:44:12+07:00 — CMD-003: Create smoke test script

- Working directory: D:\cexar-workbench\experiments\EXP-0015-rad-dino-linear-probe-smoke-test
- Action: Wrote `artifacts/run_rad_dino_linear_probe_smoke.py`
- Summary: Python script covering all 4 phases: input validation, label feasibility, split, probe training.
- Files created: artifacts/run_rad_dino_linear_probe_smoke.py

### 2026-05-24T12:44:12+07:00 — CMD-004: Execute smoke test script

- Working directory: D:\cexar-workbench\experiments\EXP-0015-rad-dino-linear-probe-smoke-test
- Command: `D:\cexar-workbench\.venvs\cexar-foundation\Scripts\python.exe artifacts\run_rad_dino_linear_probe_smoke.py`
- Exit code: 0
- Attempt 1 failed: relative venv path not found from experiment directory
- Attempt 2 failed: BASE path resolution error (3 dirnames instead of 4)
- Attempt 3 succeeded

### Phase 1: Input Validation (CMD-004 output)

- sample_manifest.csv: 100 rows, indices 0-99 sequential — PASSED
- rad_dino_embedding_summary.json: 100 attempted, 100 succeeded — PASSED
- rad_dino_embeddings.npz: shape (100, 768), indices align 0-99 — PASSED
- Output: artifacts/input_validation_report.json (status: passed)

### Phase 2: Label Feasibility (CMD-004 output)

- 11 CheXpert labels examined from sample_manifest.csv
- 9 usable (both positive and negative present): Atelectasis (34+/66-), Consolidation (14+/86-), Pneumothorax (2+/98-), Edema (18+/82-), Pleural Effusion (35+/65-), Pneumonia (3+/97-), Cardiomegaly (31+/69-), Lung Opacity (59+/41-), Enlarged Cardiomediastinum (51+/49-)
- 2 skipped: Lung Lesion (0 positive, 100 negative), Fracture (0 positive, 100 negative)
- No missing/uncertain label values found — all values are 0.0 or 1.0
- Output: artifacts/label_feasibility_report.json

### Phase 3: Deterministic Split (CMD-004 output)

- Seed: 42, train fraction: 0.8
- Patient-level split: True (extracted from Path column in manifest)
- 99 unique patients identified
- Train: 79 samples, Eval: 21 samples
- Output: artifacts/split_manifest.csv (sample_index, split, patient_id columns)

### Phase 4: Linear Probe Smoke Test (CMD-004 output)

- Classifier: sklearn.linear_model.LogisticRegression (seed=42, max_iter=1000, solver=lbfgs, class_weight=balanced)
- Device: CPU
- Train embeddings: [79, 768], Eval embeddings: [21, 768]

Per-label results (PIPELINE SANITY ONLY — NOT CLINICAL PERFORMANCE):

| Label | Train Pos/Neg | Eval Pos/Neg | AUROC | Status |
|-------|---------------|--------------|-------|--------|
| Atelectasis | 30/49 | 4/17 | 0.7206 | completed |
| Consolidation | 12/67 | 2/19 | 0.8421 | completed |
| Pneumothorax | 0/79 | 2/19 | N/A | skipped (no positive in train after patient-level split) |
| Edema | 15/64 | 3/18 | 0.3519 | completed |
| Pleural Effusion | 30/49 | 5/16 | 0.7000 | completed |
| Pneumonia | 2/77 | 1/20 | 1.0000 | completed |
| Cardiomegaly | 28/51 | 3/18 | 0.5000 | completed |
| Lung Lesion | 0/79 | 0/21 | N/A | skipped (no positive anywhere) |
| Fracture | 0/79 | 0/21 | N/A | skipped (no positive anywhere) |
| Lung Opacity | 46/33 | 13/8 | 0.7019 | completed |
| Enlarged Cardiomediastinum | 41/38 | 10/11 | 0.6818 | completed |

- 8 labels completed, 3 labels skipped
- Output: artifacts/probe_smoke_metrics.json

### 2026-05-24T12:44:12+07:00 — CMD-005: List generated artifacts

- Working directory: D:\cexar-workbench\experiments\EXP-0015-rad-dino-linear-probe-smoke-test
- Command: `Get-ChildItem -Path "artifacts" | Select-Object Name`
- Exit code: 0
- Files confirmed: input_validation_report.json, label_feasibility_report.json, probe_smoke_metrics.json, run_rad_dino_linear_probe_smoke.py, split_manifest.csv, .gitkeep

## Compliance Notes

- No production code modified.
- No prior experiment artifacts modified (EXP-0012B, EXP-0013, EXP-0014 read-only access).
- No RAD-DINO inference run.
- No RAD-DINO fine-tuning.
- No threshold tuning or hyperparameter search.
- No file cleanup, deletion, or relocation.
- All commands recorded in commands.ps1.
- All results traceable to CMD-004 output.

### Wrong-Path Incident

During the first failed script execution (BASE = `experiments/` instead of workspace root), `input_validation_report.json` was written to the wrong path:

```
experiments/EXP-0015-rad-dino-linear-probe-smoke-test/experiments/EXP-0015-rad-dino-linear-probe-smoke-test/artifacts/input_validation_report.json
```

This file is a leftover from the failed run. The correct artifact is at `artifacts/input_validation_report.json`. The wrong-path file has NOT been deleted. Human approval is required before any cleanup.

### Compliance Backfill Note

During Codex review, a command ledger gap was found.

`EXPERIMENT_LOG.md` reported two failed script attempts before the successful run:

1. Attempt 1 failed because a relative venv path was not found from the experiment directory.
2. Attempt 2 failed because the script used incorrect BASE path resolution.

These failed attempts were not recorded as separate exact commands in `commands.ps1` at execution time. Because the exact terminal text cannot be verified from the current artifacts, the backfilled entries in `commands.ps1` are explicitly marked as `UNKNOWN - NOT RECORDED AT EXECUTION TIME`.

This is a compliance limitation, not a model-result failure. The final successful run remains traceable through CMD-004 and the generated artifacts.

### Nested Wrong-Path Artifacts

Two wrong-path artifact locations were found during Codex review:

1. `D:\cexar-workbench\experiments\experiments\EXP-0015-rad-dino-linear-probe-smoke-test\artifacts\input_validation_report.json`
2. `D:\cexar-workbench\experiments\EXP-0015-rad-dino-linear-probe-smoke-test\experiments\EXP-0015-rad-dino-linear-probe-smoke-test\artifacts\input_validation_report.json`

These files appear to be leftover `input_validation_report.json` outputs from failed BASE path resolution attempts.

Cleanup status:

- Not deleted.
- Not moved.
- Preserved as evidence.
- Human approval is required before any cleanup command is run.

The correct artifact is:

`D:\cexar-workbench\experiments\EXP-0015-rad-dino-linear-probe-smoke-test\artifacts\input_validation_report.json`