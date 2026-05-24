# REVIEW.md

## Codex Review Checklist for EXP-0018

### GPU Target

- [x] GPU target is fixed to NVIDIA A40 (not T4, L4, A10, A100, H100, CPU-only, or any other).
- [x] The runner did not select an alternative GPU.
- [x] CUDA 12.1 and PyTorch 2.3.1+cu121 selected as compatible versions for A40 (Ampere SM 8.6).

### Security

- [x] `CMD-003` secrets scan returned 0 actual credentials.
- [x] SSH templates contain only placeholders (`<A40_CLOUD_HOST>`, `<REMOTE_USER>`).
- [x] No hostnames, private IPs, API keys, tokens, or passwords in any file.
- [x] `cloud_provisioning_config.yaml` explicitly prohibits credentials, SSH keys, and API tokens in the repo.

### File Completeness (required by experiment_protocol.md)

- [x] `README.md`
- [x] `TEST_PLAN.md`
- [x] `RUNNER_INSTRUCTIONS.md`
- [x] `EXPERIMENT_LOG.md` (populated with chronological log)
- [x] `RESULT.md` (PASS AS CLOUD READINESS PACKAGE)
- [x] `FAILURE_REPORT.md` (INCIDENT-001: Python PATH, resolved via fallback)
- [x] `DIFF_SUMMARY.md` (all file changes documented)
- [x] `REVIEW.md` (this file)
- [x] `configs/` (3 YAML configs)
- [x] `artifacts/` (.gitkeep only, no cloud artifacts)
- [x] `commands.ps1` (4 registered commands)

### Config Machine-Readability

- [x] `cloud_provisioning_config.yaml`: valid YAML with compute, software, paths, security, and runner_decision_scope sections.
- [x] `manifest_integrity_audit.json`: valid JSON with columns, label policy, patient integrity, metric masking.
- [x] `configs/regularized_probe_config.yaml`: logistic regression, L2 penalty, 7 C values.
- [x] `configs/seed_plan.yaml`: 10 explicit seeds, patient-level split policy.
- [x] `configs/artifact_paths.yaml`: local and cloud path mappings.
- [x] `cloud_cost_runtime_estimate.json`: basis from EXP-0017 CPU data, A40 estimates marked TBD.
- [x] `EXP0019_READINESS.json`: READY_WITH_HUMAN_CLOUD_SELECTION, blockers empty.

### Code Skeletons

- [x] 6 Python modules present under `src/`.
- [x] All skeletons raise `SystemExit` or `NotImplementedError` by default.
- [x] `metrics.py:should_mask_metric` is the only functional helper (no training dependency).
- [x] No model imports, no dataset loading, no GPU code.

### SSH Templates

- [x] 3 shell templates under `scripts/`.
- [x] All use placeholder values.
- [x] Template comments explicitly warn against committing secrets.
- [x] No executable cloud logic.

### Evidence Chain

- [x] All claims in `RESULT.md` trace to: `commands.ps1` entries, `EXPERIMENT_LOG.md` entries, or direct file inspection.
- [x] No fabricated metrics, timings, or environment data.

### Forbidden Actions (Verified Not Performed)

- [x] Cloud instance startup: NOT performed.
- [x] SSH execution: NOT performed.
- [x] RAD-DINO inference: NOT performed.
- [x] Model training: NOT performed.
- [x] Dataset upload: NOT performed.
- [x] Production code modification: NOT performed.
- [x] Clinical claims: NOT made.
- [x] System Python modification: NOT performed.
- [x] Global pip operations: NOT performed.

### Medical Claims Policy Compliance

- [x] All metric configs include RESEARCH PIPELINE METRIC ONLY notice.
- [x] `RESULT.md` includes limitations section.
- [x] No claim of clinical validation, diagnostic readiness, or radiologist-level performance.

### Prior Artifact Traceability

- [x] `manifest_integrity_audit.json` references `experiments/EXP-0016-chexpert-scale-up-readiness/artifacts/candidate_manifest_1k.csv`.
- [x] `cloud_cost_runtime_estimate.json` references EXP-0017 embedding summary (1161.52s).
- [x] EXP-0017 `corrected_split_report.json` and `linear_probe_metrics.json` used for audit validation.

### Remaining for Human

- [ ] Select cloud provider with NVIDIA A40 availability.
- [ ] Provision credentials outside the repository.
- [ ] Decide dataset transfer or mount strategy.
- [ ] Review and approve before EXP-0019-cloud-smoke-run.
