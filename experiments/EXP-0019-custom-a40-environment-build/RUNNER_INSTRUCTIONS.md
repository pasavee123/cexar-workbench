# RUNNER_INSTRUCTIONS.md

## Mission

Create and verify the CeXaR custom A40 environment package. This is an environment-build experiment, not a model experiment.

## Hard Constraints

- Read `standards/runner_protocol.md` before doing any work.
- Register every terminal command in `commands.ps1` before execution.
- Log every command result in `EXPERIMENT_LOG.md`.
- Do not run hidden cleanup commands.
- Do not modify production code.
- Do not modify global/system Python.
- Do not commit secrets, SSH keys, PATs, hostnames, or private IPs.
- Do not run RAD-DINO inference, dataset upload, training, or clinical evaluation.
- Do not change GPU target from NVIDIA A40.
- Do not change pinned CUDA/Python/PyTorch versions without human approval.

## Required Work

1. Read all required standards and EXP-0018 result files.
2. Review `environment_contract.yaml`.
3. Inspect `docker/Dockerfile` and `docker/start.sh`.
4. Inspect `requirements.lock.txt`.
5. Decide whether this session can build Docker images.
6. If build is available, build the image with `linux/amd64`.
7. If build is not available, stop after static validation and write a clear blocker.
8. If a container can be run, execute `verify_environment.py` inside it.
9. If on RunPod A40, verify `nvidia-smi` and torch GPU visibility.
10. Write final result documents.

## Attempt Budget

- Docker build attempts: maximum 3.
- Dependency/version fix attempts: maximum 2, only if the target contract is unchanged.
- Registry/GHCR attempts: maximum 2, only with human-approved credentials.

After the attempt budget is exceeded, stop and write `FAILURE_REPORT.md`.

## Output Rules

`RESULT.md` must include:
- final status
- image tag tested
- exact versions verified
- whether GPU verification happened
- whether `/workspace` persistence was verified
- whether GHCR push/pull was verified
- limitations

`FAILURE_REPORT.md` must include any non-blocking incidents, not only fatal failures.

