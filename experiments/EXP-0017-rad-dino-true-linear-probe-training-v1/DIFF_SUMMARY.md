# DIFF_SUMMARY.md

## Files Modified

| File | Action | Description |
|------|--------|-------------|
| commands.ps1 | Modified | Added CMD-001 through CMD-006 with exact commands and results |
| EXPERIMENT_LOG.md | Modified | Full chronological log of all phases |
| RESULT.md | Modified | Final experiment result: PASS AS TRUE LINEAR PROBE TRAINING V1 |
| FAILURE_REPORT.md | Modified | No failure recorded |
| DIFF_SUMMARY.md | Modified | This file |

## Files Created

| File | Phase | Description |
|------|-------|-------------|
| artifacts/run_exp0017_true_linear_probe.py | Pre | Main experiment script (562 lines, all 5 phases) |
| artifacts/input_environment_validation.json | 1 | Environment validation results |
| artifacts/corrected_split_manifest_1k.csv | 2 | Corrected 1k manifest with split assignment |
| artifacts/corrected_split_report.json | 2 | Split feasibility report |
| artifacts/rad_dino_embeddings_1k.npz | 3 | Frozen RAD-DINO embeddings [1000, 768] |
| artifacts/rad_dino_embedding_summary_1k.json | 3 | Embedding generation summary |
| artifacts/linear_probe_metrics.json | 4 | Per-label training metrics |
| artifacts/linear_probe_model_inventory.json | 4 | Probe model inventory |
| artifacts/baseline_context_comparison.md | 5 | Baseline context comparison report |

## Files Read Only (Not Modified)

| File | Purpose |
|------|---------|
| experiments/RUNNER_PREFLIGHT_SAFETY_PROMPT.md | Safety rules |
| standards/runner_protocol.md | Runner protocol |
| standards/experiment_protocol.md | Experiment protocol |
| standards/medical_claims_policy.md | Medical claims policy |
| standards/integration_gate.md | Integration gate |
| experiments/EXP-0016-chexpert-scale-up-readiness/artifacts/candidate_manifest_1k.csv | Input manifest |
| experiments/EXP-0016-chexpert-scale-up-readiness/artifacts/patient_split_feasibility_report.json | Split feasibility reference |
| experiments/EXP-0016-chexpert-scale-up-readiness/artifacts/EXP0017_READINESS.md | Readiness assessment |
| experiments/EXP-0013-rad-dino-foundation-embedding-smoke/artifacts/run_rad_dino_embedding_smoke.py | Embedding pipeline reference |
| D:\Dataset_Chexpert | Dataset images (read-only) |
| ~/.cache/huggingface/hub/models--microsoft--rad-dino | RAD-DINO weights (read-only) |

## No Files Deleted, Moved, or Renamed

## External Directories Accessed (Read Only)

- D:\Dataset_Chexpert (CheXpert dataset images)
- ~/.cache/huggingface/hub/ (HuggingFace model cache)
- .venvs/cexar-foundation/ (Python virtual environment)
