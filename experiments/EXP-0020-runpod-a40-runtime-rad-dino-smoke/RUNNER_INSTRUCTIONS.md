# RUNNER_INSTRUCTIONS.md

## Mission

Run EXP-0020 on a RunPod A40 pod using the EXP-0019 image and verify that RAD-DINO embedding extraction works on 100 real CheXpert images.

## Hard Rules

- Read `standards/runner_protocol.md` before any work.
- Register every terminal command in `commands.ps1` before execution.
- Log every command result in `EXPERIMENT_LOG.md`.
- Do not write secrets, tokens, hostnames, private IPs, or SSH keys into repo files.
- Do not modify production code.
- Do not modify global/system Python.
- Do not train models.
- Do not compute clinical metrics.
- Do not make clinical claims.
- Do not continue if GPU is not NVIDIA A40.
- Do not continue if CUDA is unavailable.

## Attempt Budget

- Runtime verification attempts: 2
- Dataset mount/path mapping attempts: 3
- RAD-DINO smoke attempts: 2

After the attempt budget is exceeded, stop and write `FAILURE_REPORT.md`.

## Required Output

`RESULT.md` must include:
- image tag used
- RunPod GPU model
- Python/CUDA/torch/torchvision versions
- dataset mount status
- RAD-DINO model source (`local_cache` or `downloaded`)
- images attempted/succeeded/failed
- embedding shape
- runtime seconds
- peak/observed VRAM if available
- explicit statement: no clinical claims

