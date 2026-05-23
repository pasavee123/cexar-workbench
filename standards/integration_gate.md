# CeXaR Integration Gate

This gate must pass before any experiment result can be integrated into production code.

## Required Approvals

- Experiment completed in `experiments/`
- Codex review completed
- Human approval recorded
- Integration scope identified
- Rollback plan written

## Medical AI Checks

- Patient-level split verified when datasets are used
- No train/validation/test patient overlap
- Label order documented
- Preprocessing documented and matched to model assumptions
- Thresholds frozen from validation data only
- Per-label metrics reported
- Calibration or uncertainty limitations documented
- External validation risk documented
- No unsupported clinical claims

## External Repository Checks

- License checked
- Maintenance status checked
- Dependencies reviewed
- Python/PyTorch/CUDA compatibility reviewed
- Input/output shape documented
- Checkpoint format documented
- Tests or demos inspected
- Security and privacy risks documented

## Integration Decision

Allowed outcomes:

- Reject
- Retry in experiment
- Keep as research reference only
- Prepare integration patch for human review
- Integrate after human approval

