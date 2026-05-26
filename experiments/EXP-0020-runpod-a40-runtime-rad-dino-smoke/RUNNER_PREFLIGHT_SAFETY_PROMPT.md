# RUNNER_PREFLIGHT_SAFETY_PROMPT.md

You are the runner for CeXaR EXP-0020-runpod-a40-runtime-rad-dino-smoke.

Before doing anything, read:
- `standards/runner_protocol.md`
- `standards/experiment_protocol.md`
- `standards/medical_claims_policy.md`
- `standards/integration_gate.md`
- `experiments/EXP-0019-custom-a40-environment-build/RESULT.md`
- `experiments/EXP-0020-runpod-a40-runtime-rad-dino-smoke/README.md`
- `experiments/EXP-0020-runpod-a40-runtime-rad-dino-smoke/TEST_PLAN.md`
- `experiments/EXP-0020-runpod-a40-runtime-rad-dino-smoke/RUNNER_INSTRUCTIONS.md`
- `experiments/EXP-0020-runpod-a40-runtime-rad-dino-smoke/runpod_runtime_contract.yaml`

Critical rules:
- Register every terminal command in `commands.ps1` before execution.
- Log every command result in `EXPERIMENT_LOG.md`.
- Use image `ghcr.io/pasavee123/cexar-a40:cuda121-torch231-03b1e789264b581b1166f7fd0c8416d717116858`.
- Stop if GPU is not NVIDIA A40.
- Stop if CUDA is not available.
- Stop if `/workspace` or `/workspace/chexpert_dataset_raw` is unavailable.
- Do not train, classify, compute AUROC/AUPRC, or make clinical claims.
- Do not modify production code.
- Do not commit secrets or host connection details.
- After completion, commit and push results only to branch `exp/0020-runpod-smoke-result`.
- Never push to `main`.
- If Git authentication is missing or asks for a token, stop and ask the human. Do not paste tokens into logged commands and do not write tokens to files.

Your task is runtime verification plus a 100-image RAD-DINO embedding smoke test only.
