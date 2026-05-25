# EXPERIMENT_LOG.md

## 2026-05-25 20:00 UTC+7 - Session Start

Runner session started. All required standards and EXP-0018 result files read.

---

## Phase 0: Safety and Ledger

### CMD-001 - docker --version
- **Timestamp:** 2026-05-25 20:00 UTC+7
- **Exit code:** 0
- **Summary:** Docker version 28.3.3, build 980b856. Docker is installed and available.

### CMD-002 - docker buildx version
- **Timestamp:** 2026-05-25 20:00 UTC+7
- **Exit code:** 1 (unknown command)
- **Summary:** `docker buildx` is not available as a separate subcommand. On Docker 28.x, buildx is the default builder. `docker build --platform` is the supported path.

### CMD-003 - docker build --help | Select-String platform
- **Timestamp:** 2026-05-25 20:00 UTC+7
- **Exit code:** 0
- **Summary:** `--platform` flag is supported on `docker build` directly. Confirmed.

### CMD-004 - docker info | Select-String OS/Architecture/Server
- **Timestamp:** 2026-05-25 20:00 UTC+7
- **Exit code:** 0
- **Summary:** Non-conclusive Docker server check. A Server-related line was reported, but CMD-006 later proved the Docker Desktop Linux Engine was unreachable.

### CMD-005 - git rev-parse HEAD
- **Timestamp:** 2026-05-25 20:00 UTC+7
- **Exit code:** 0
- **Summary:** Current commit SHA: `c1faf5818f3e3d280340c4f8b465a095826c0a45`

### Phase 0 Decision
Docker CLI is available. Docker daemon availability still requires build confirmation. `docker build --platform linux/amd64` will be used. Proceeding to Phase 1.

---

## Phase 1: Static Contract Review

### Verification Results

| Item | Requirement | Actual | Status |
|------|-------------|--------|--------|
| GPU target | NVIDIA A40 (fixed) | `environment_contract.yaml:9`: A40, `runner_may_change_gpu: false` | PASS |
| Base image | nvidia/cuda:12.1.1-cudnn8-devel-ubuntu22.04 | `docker/Dockerfile:1` | PASS |
| Python version | 3.10 | `docker/Dockerfile:15` - apt `python3` (Ubuntu 22.04 = Python 3.10) | PASS |
| Python venv | /opt/venv | `docker/Dockerfile:19` | PASS |
| PyTorch version | 2.3.1+cu121 | `docker/Dockerfile:25`: `torch==2.3.1` from cu121 index | PASS |
| torchvision version | 0.18.1+cu121 | `docker/Dockerfile:26`: `torchvision==0.18.1` from cu121 index | PASS |
| PyTorch index URL | https://download.pytorch.org/whl/cu121 | `docker/Dockerfile:24` | PASS |
| Workspace path | /workspace | `docker/Dockerfile:37`: `WORKDIR /workspace` | PASS |
| HF cache | /workspace/.cache/huggingface | `docker/Dockerfile:5`: `HF_HOME` env var + `docker/Dockerfile:31`: mkdir | PASS |
| Torch cache | /workspace/.cache/torch | `docker/Dockerfile:7`: `TORCH_HOME` env var + `docker/Dockerfile:31`: mkdir | PASS |
| SSH setup | Required | `docker/start.sh:12-18`: SSH key from PUBLIC_KEY env, sshd start | PASS |
| Auto-run experiments | Must NOT auto-run | `docker/start.sh:21`: "No experiment is auto-started" | PASS |
| Exposed ports | 22/tcp | `docker/Dockerfile:39`: `EXPOSE 22` | PASS |
| Keepalive | sleep infinity | `docker/start.sh:23` | PASS |
| requirements.lock.txt | Match EXP-0018 required packages | All 9 required packages present (+ safetensors, huggingface-hub extras) | PASS |

### Phase 1 Decision
Static contract review PASSES. All version pins, paths, and runtime behavior match `environment_contract.yaml` and EXP-0018 cloud provisioning config. No target changes needed. Proceeding to Phase 2.

---

## Phase 2: Docker Build Check

### CMD-006 - docker build (ATTEMPT 1/3)
- **Timestamp:** 2026-05-25 20:00 UTC+7
- **Command:** `docker build --platform linux/amd64 -f experiments/EXP-0019-custom-a40-environment-build/docker/Dockerfile -t ghcr.io/pasavee123/cexar-a40:cuda121-torch231-c1faf58 experiments/EXP-0019-custom-a40-environment-build`
- **Exit code:** 1
- **Error:** `Head "http://%2F%2F.%2Fpipe%2FdockerDesktopLinuxEngine/_ping": open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified.`
- **Summary:** Docker daemon is not reachable. The Docker Desktop Linux Engine pipe does not exist.

### CMD-007 - Docker Desktop process check
- **Timestamp:** 2026-05-25 20:00 UTC+7
- **Exit code:** 0 (no process found)
- **Summary:** Docker Desktop process is not running on the Windows host.

### CMD-008 - WSL2 status check
- **Timestamp:** 2026-05-25 20:00 UTC+7
- **Exit code:** 0
- **Summary:** WSL2 `docker-desktop` instance state is `Stopped`.

### Phase 2 Decision: BLOCKED
Docker daemon is not running. Docker Desktop and its WSL2 backend are stopped. The runner cannot start system services without explicit human approval per `standards/runner_protocol.md:48`. 

Remaining build attempts: 2 of 3 budget unused, but all would fail identically with a non-running daemon. Stopping per `RUNNER_INSTRUCTIONS.md` line 7: "If build is not available, stop after static validation and write a clear blocker."

---

## Codex Post-Review Update

### 2026-05-25 UTC+7 - GitHub Actions build path selected

After reviewing the runner blocker, Codex and the human selected GitHub Actions as the preferred canonical image build path.

Changes made after runner completion:
- Added `.github/workflows/build-cexar-a40-image.yml`.
- Updated `BUILD_AND_PUSH_NOTES.md` to mark GitHub Actions as the selected canonical path.
- Updated `RESULT.md` and `REVIEW_NOTES_FOR_CODEX.md` with the manual workflow trigger path.
- Corrected minor documentation inconsistencies and non-ASCII dash/arrow rendering issues.

No Docker build, GHCR push, RAD-DINO inference, dataset upload, training, or production integration was performed by Codex during this update.

### 2026-05-25 UTC+7 - GitHub Actions build failure follow-up

The first GitHub Actions build failed during the PyTorch install layer:

```text
pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cu121 torch==2.3.1 torchvision==0.18.1
```

The official PyTorch previous-versions install command for CUDA 12.1 uses this same torch/torchvision version pair and index URL, so the version contract was not changed.

Codex updated the workflow to:
- free unused GitHub-hosted runner disk space before Docker build
- request plain BuildKit progress logs
- disable provenance output for this large image build

No Dockerfile version pins were changed.

### 2026-05-25 UTC+7 - No-space build failure mitigation

The subsequent GitHub Actions build reported:

```text
OSError: [Errno 28] No space left on device
```

This occurred during the `torch==2.3.1` and `torchvision==0.18.1` install layer. Codex applied a space mitigation without changing the CUDA/PyTorch contract:

- More aggressive GitHub runner cleanup: swapfile, hosted tool cache, Android, .NET, GHC, Boost, ghcup, apt lists.
- Dockerfile pip cleanup: `PIP_NO_CACHE_DIR=1`, `PIP_DISABLE_PIP_VERSION_CHECK=1`, and removal of `/tmp`, `/var/tmp`, and pip cache after each Python install layer.

CUDA, Python, PyTorch, torchvision, and base image targets remain unchanged.

### 2026-05-25 UTC+7 - Second no-space build failure mitigation

The next GitHub Actions attempt still reported:

```text
ERROR: Could not install packages due to an OSError: [Errno 28] No space left on device
```

The repeated failure suggests that cleanup alone is insufficient because Docker build layers are being stored on the default Docker root filesystem. Codex updated the workflow to move Docker's data root to `/mnt/docker` before the build.

This keeps the CUDA/PyTorch contract unchanged while giving BuildKit more working space for large base image layers and PyTorch wheels.

### 2026-05-25 UTC+7 - WarpBuild runner path selected

The human selected WarpBuild to avoid further GitHub-hosted runner disk limitations while preserving clean build logs.

Codex updated the workflow to accept a manual `runner_label` input:

```text
runner_label = warp-ubuntu-latest-x64-16x
```

This changes only the build runner selection. It does not change the image contract, Dockerfile base image, Python version, CUDA version, PyTorch version, or GHCR tag policy.

The workflow default was updated from `ubuntu-latest` to `warp-ubuntu-latest-x64-16x` to reduce accidental reruns on the disk-limited GitHub-hosted runner.

Codex corrected the runner tag to match WarpBuild's official naming convention: `x64`, not `x86-64`.

### 2026-05-25 UTC+7 - Repository organization migration alignment

The human confirmed the active repository for WarpBuild is:

```text
cexar-lab/cexar-workbench
```

Codex updated canonical GHCR package references from `ghcr.io/pasavee123/cexar-a40` to:

```text
ghcr.io/cexar-lab/cexar-a40
```

The old runner-reserved local build tag remains documented as historical evidence only. No image was built or pushed under that old tag.

### 2026-05-25 UTC+7 - GitHub hosted free-disk-space fallback selected

WarpBuild runner routing remained stuck at:

```text
Waiting for a runner to pick up this job...
```

The human proposed trying a GitHub-hosted runner again with the maintained `jlumbroso/free-disk-space@v1.3.1` action. Codex updated the workflow to:

- default `runner_label` back to `ubuntu-latest`
- run `jlumbroso/free-disk-space@v1.3.1` before checkout
- preserve the existing manual cleanup and `/mnt/docker` data-root relocation
- preserve non-`latest` GHCR tags and the experiment-specific Docker build context

The workflow still avoids `:latest` image tags and does not change the environment contract.
