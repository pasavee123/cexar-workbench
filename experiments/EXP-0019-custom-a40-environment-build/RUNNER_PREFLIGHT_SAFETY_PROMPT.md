# RUNNER_PREFLIGHT_SAFETY_PROMPT.md

You are the runner for CeXaR EXP-0019-custom-a40-environment-build.

Before doing anything, read:
- `standards/runner_protocol.md`
- `standards/experiment_protocol.md`
- `standards/medical_claims_policy.md`
- `standards/integration_gate.md`
- `experiments/EXP-0018-cloud-readiness-package/RESULT.md`
- `experiments/EXP-0018-cloud-readiness-package/cloud_provisioning_config.yaml`
- `experiments/EXP-0019-custom-a40-environment-build/README.md`
- `experiments/EXP-0019-custom-a40-environment-build/TEST_PLAN.md`
- `experiments/EXP-0019-custom-a40-environment-build/RUNNER_INSTRUCTIONS.md`
- `experiments/EXP-0019-custom-a40-environment-build/environment_contract.yaml`

Critical rules:
- Register every terminal command in `commands.ps1` before execution.
- Log every command result in `EXPERIMENT_LOG.md`.
- Do not run hidden cleanup, copy, move, delete, or registry commands.
- Do not touch global/system Python.
- Do not write secrets, SSH keys, PATs, hostnames, or private IPs into repo files.
- Do not change CUDA/Python/PyTorch/GPU targets.
- Do not run RAD-DINO inference, dataset upload, model training, metrics, or production integration.

Your task is to validate or build the custom interactive RunPod A40 image package only.

If the environment cannot build Docker images or lacks required permissions, stop cleanly and write `FAILURE_REPORT.md`.

