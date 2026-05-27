# RUNNER_PREFLIGHT_SAFETY_PROMPT.md

You are the runner for CeXaR EXP-0021-rad-dino-10k-cloud-embedding-run.

Before doing anything, read:

- `standards/runner_protocol.md`
- `standards/experiment_protocol.md`
- `standards/medical_claims_policy.md`
- `standards/integration_gate.md`
- `experiments/EXP-0020-runpod-a40-runtime-rad-dino-smoke/RESULT.md`
- `experiments/EXP-0021-rad-dino-10k-cloud-embedding-run/README.md`
- `experiments/EXP-0021-rad-dino-10k-cloud-embedding-run/TEST_PLAN.md`
- `experiments/EXP-0021-rad-dino-10k-cloud-embedding-run/RUNNER_INSTRUCTIONS.md`
- `experiments/EXP-0021-rad-dino-10k-cloud-embedding-run/CODEX_REVIEW_PLAN.md`
- `experiments/EXP-0021-rad-dino-10k-cloud-embedding-run/configs/exp0021_config.yaml`

Critical runtime facts:

- Repository checkout path: `/root/cexar-workbench`
- Persistent network volume: `/workspace`
- Required GPU: NVIDIA RTX 6000 Ada Generation
- Required Python: `/opt/venv`
- Required image: `ghcr.io/pasavee123/cexar-a40:cuda121-torch231-03b1e789264b581b1166f7fd0c8416d717116858`
- Large artifact root: `/workspace/exp_artifacts/EXP-0021`
- Path mapping: `D:\Dataset_Chexpert\archive -> /workspace/chexpert_dataset_raw`

Critical process rules:

- Do not run any terminal command before registering the exact command in `commands.ps1`.
- Use exact command text, not shortened summaries.
- Do not delete, move, or clean dataset/cache/repo files.
- Do not install packages outside `/opt/venv`.
- Do not modify production code.
- Do not train, classify, compute AUROC/AUPRC, or make clinical claims.
- Do not push to `main`.
- Do not write secrets or connection details to repo files.

Your first task is Phase A script authoring and small dry-run readiness only. Stop for Codex review before any 10,000-image run.

