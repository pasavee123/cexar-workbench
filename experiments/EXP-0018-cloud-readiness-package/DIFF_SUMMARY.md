# DIFF_SUMMARY.md

## Files Modified During EXP-0018

| File | Action | Phase |
|------|--------|-------|
| `commands.ps1` | Populated with CMD-001 through CMD-004 | Phase 0 |
| `cloud_provisioning_config.yaml` | Added explicit CUDA 12.1 and PyTorch 2.3.1 (cu121) version selections | Phase 1 |
| `EXPERIMENT_LOG.md` | Populated with full chronological execution log | All phases |
| `RESULT.md` | Updated with PASS status and criteria evaluation | Final |
| `FAILURE_REPORT.md` | Updated with INCIDENT-001 (Python PATH) | Final |
| `DIFF_SUMMARY.md` | Updated with this file inventory | Final |

## Files Created During EXP-0018

| File | Purpose |
|------|---------|
| `REVIEW.md` | Codex review checklist (required by experiment_protocol.md) |

## Files Verified But Not Modified

| File | Phase |
|------|-------|
| `README.md` | Pre-existing, unchanged |
| `TEST_PLAN.md` | Pre-existing, unchanged |
| `RUNNER_INSTRUCTIONS.md` | Pre-existing, unchanged |
| `RUNNER_PREFLIGHT_SAFETY_PROMPT.md` | Pre-existing, unchanged |
| `REVIEW_NOTES_FOR_CODEX.md` | Pre-existing, unchanged |
| `manifest_integrity_audit.json` | Phase 2 (validated against CSV) |
| `EXP0019_READINESS.json` | Phase 6 (reviewed) |
| `cloud_cost_runtime_estimate.json` | Phase 6 (reviewed) |
| `configs/regularized_probe_config.yaml` | Phase 3 (reviewed) |
| `configs/seed_plan.yaml` | Phase 3 (reviewed) |
| `configs/artifact_paths.yaml` | Phase 3 (reviewed) |
| `src/run_regularized_probe.py` | Phase 4 (reviewed) |
| `src/split_strategies.py` | Phase 4 (reviewed) |
| `src/embedding_io.py` | Phase 4 (reviewed) |
| `src/metrics.py` | Phase 4 (reviewed) |
| `src/manifest_audit.py` | Phase 4 (reviewed) |
| `src/cloud_runtime_check.py` | Phase 4 (reviewed) |
| `scripts/ssh_cloud_smoke_template.sh` | Phase 5 (reviewed, no credentials) |
| `scripts/setup_cloud_env.sh` | Phase 5 (reviewed, no credentials) |
| `scripts/collect_artifacts.sh` | Phase 5 (reviewed, no credentials) |

## Scope Boundary

- No cloud instance was started.
- No SSH commands were executed.
- No credentials or secrets were committed.
- No dataset upload occurred.
- No RAD-DINO inference or model training occurred.
- No production code was modified.
- GPU target remains fixed to NVIDIA A40.
