# EXPERIMENT_LOG.md

## EXP-0018 Cloud Readiness Package - Execution Log

### 2026-05-24T22:58 - Phase 0: Safety Preflight

All required documents read:
- `experiments/RUNNER_PREFLIGHT_SAFETY_PROMPT.md`
- `standards/runner_protocol.md`
- `standards/experiment_protocol.md`
- `standards/medical_claims_policy.md`
- `standards/integration_gate.md`
- `experiments/EXP-0018-cloud-readiness-package/README.md`
- `experiments/EXP-0018-cloud-readiness-package/TEST_PLAN.md`
- `experiments/EXP-0018-cloud-readiness-package/RUNNER_INSTRUCTIONS.md`

GPU target confirmed: **NVIDIA A40** (fixed by human, no alternative selected).

### 2026-05-24T22:58 - Phase 0: Command Ledger Initialization

- Verified `commands.ps1` exists (empty scaffold, now populated with CMD-001 through CMD-004).
- Verified `EXPERIMENT_LOG.md` exists (scaffold, now populated).

### 2026-05-24T22:58 - Phase 0: Prior Artifact Verification [CMD-001]

- `CMD-001`: Test-Path for all four required prior artifacts.
- **Result: EXIT CODE 0** - All four paths returned True.
  - `candidate_manifest_1k.csv`: EXISTS
  - `linear_probe_metrics.json`: EXISTS
  - `rad_dino_embedding_summary_1k.json`: EXISTS
  - `corrected_split_report.json`: EXISTS

### 2026-05-24T22:58 - Phase 2: CSV Manifest Validation [CMD-002]

- `CMD-002`: Attempted Python CSV row count. **Result: EXIT CODE 1** - Python not found in PATH.
- Fallback: Read tool confirmed 1001 lines = 1 header + 1000 data rows.
- All 17 required columns from `manifest_integrity_audit.json` confirmed present in CSV header.
- Expected row count (1000) matches actual data rows (1000).

### 2026-05-24T22:58 - Phase 1: Cloud Provisioning Config

- Reviewed `cloud_provisioning_config.yaml`.
- GPU target: NVIDIA A40 (fixed, not modified).
- Runner decisions applied:
  - Python version: 3.10
  - CUDA version: 12.1 (compatible with A40 Ampere SM 8.6)
  - PyTorch version: 2.3.1 with cu121 build
  - Disk: 200 GB min, 500 GB recommended SSD
  - RAM: 32 GB min, 64 GB recommended
  - HF cache: /workspace/.cache/huggingface
  - Artifact root: /workspace/cexar-workbench/experiments/EXP-0019-cloud-smoke-run/artifacts
  - Cloud smoke sample size: 100 images (defined in EXP0019_READINESS.json)

### 2026-05-24T22:58 - Phase 2: Manifest Integrity Audit

- Reviewed `manifest_integrity_audit.json`.
- Contract encodes: expected_row_count=1000, 17 required_columns, 11 label_columns, patient-level integrity, U-zeros uncertain policy, metric masking rules.
- Prior artifacts `corrected_split_report.json` and `linear_probe_metrics.json` confirm the audit contract is consistent with EXP-0017 results.

### 2026-05-24T22:58 - Phase 3: Regularized Probe Config

- Reviewed `configs/regularized_probe_config.yaml`: logistic regression, L2 penalty, 7 C values, lbfgs solver, AUROC/AUPRC metrics, mask_invalid_splits=true.
- Reviewed `configs/seed_plan.yaml`: 10 seeds, patient-level split, per-seed + mean/std reporting.
- Reviewed `configs/artifact_paths.yaml`: local and cloud paths defined, output artifact names specified.

### 2026-05-24T22:58 - Phase 4: Code Skeletons

- All 6 Python skeletons present under `src/`:
  - `run_regularized_probe.py`: raises SystemExit (scaffold only).
  - `split_strategies.py`: two function stubs with NotImplementedError.
  - `embedding_io.py`: two function stubs with NotImplementedError.
  - `metrics.py`: metric stub + `should_mask_metric` helper function (functional).
  - `manifest_audit.py`: function stub with NotImplementedError.
  - `cloud_runtime_check.py`: function stub with NotImplementedError.
- No training logic, no imports that would trigger model loading.

### 2026-05-24T22:58 - Phase 5: SSH Script Templates

- All 3 shell templates present under `scripts/`:
  - `ssh_cloud_smoke_template.sh`: Placeholder REMOTE_HOST and REMOTE_USER. No real hostnames.
  - `setup_cloud_env.sh`: Environment check template. No credentials.
  - `collect_artifacts.sh`: Artifact collection template. No private paths.
- No credentials, private IPs, tokens, or secrets in any template.

### 2026-05-24T22:58 - Phase 6: Cost/Runtime Estimates and Readiness

- Reviewed `cloud_cost_runtime_estimate.json`: Basis from EXP-0017 CPU runtime (1161.52s for 1000 images). A40 estimates marked "TBD by EXP-0019 smoke run".
- Reviewed `EXP0019_READINESS.json`: Status READY_WITH_HUMAN_CLOUD_SELECTION. Blockers list is empty. Required preconditions documented.

### 2026-05-24T22:58 - Security Scan [CMD-003]

- `CMD-003`: Select-String secrets pattern scan across all package files.
- **Result: EXIT CODE 0** - No actual secrets/credentials detected.
- Four matches are policy statements or template comments (not credentials).

### 2026-05-24T22:58 - Final Documentation

- `FAILURE_REPORT.md`: No blocking failures recorded; INCIDENT-001 documents the Python PATH fallback.
- `RESULT.md`: Updated with PASS status.
- `DIFF_SUMMARY.md`: Updated with all file inventory.
- `REVIEW.md`: Created with Codex review checklist.
- `commands.ps1`: Updated with all four registered commands (CMD-001 through CMD-004).

### 2026-05-24T22:58 - Experiment Complete

- No cloud instance was started.
- No SSH commands were executed.
- No credentials or secrets were committed.
- No dataset upload occurred.
- No RAD-DINO inference or model training was run.
- No clinical claims were made.
- GPU target remains fixed to NVIDIA A40.
