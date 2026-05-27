# RUNNER_INSTRUCTIONS.md

## Mission

DeepSeek should write a strong EXP-0022 throughput benchmark system for RAD-DINO, then run it on the cloud Pod without requiring AI-assisted documentation on the Pod.

## Hard Rules

- Read `standards/runner_protocol.md` before any work.
- Register every terminal command in `commands.ps1` before execution.
- Use exact command text.
- Use `/root/cexar-workbench` as repo path.
- Use `/workspace` for persistent datasets, caches, and artifacts.
- Use `/opt/venv/bin/python` only.
- Do not modify global/system Python.
- Do not install packages unless explicitly approved by the human.
- Do not train models.
- Do not compute AUROC/AUPRC or clinical metrics.
- Do not make clinical claims.
- Do not push from the Pod unless explicitly asked.
- Do not write secrets or connection details to repo files.

## Implementation Tasks

Implement experiment-local scripts:

- `scripts/run_exp0022_benchmark.sh`
- `scripts/benchmark_rad_dino_dataloader.py`
- `scripts/generate_review_packet.py`

The system must:

- use batched inference
- use a PyTorch Dataset/DataLoader
- benchmark batch size and worker grids
- write machine-readable results
- recommend the best config
- create a small review packet tarball
- keep large artifacts out of git

## Execution Policy

The default run should be:

```bash
bash experiments/EXP-0022-rad-dino-throughput-optimization/scripts/run_exp0022_benchmark.sh
```

The script should create:

```text
/workspace/exp_artifacts/EXP-0022/review_packet/exp0022_review_packet.tar.gz
```

After that, the human downloads the packet with `scp`, shuts down the Pod, and Codex local finalizes docs/pushes.

