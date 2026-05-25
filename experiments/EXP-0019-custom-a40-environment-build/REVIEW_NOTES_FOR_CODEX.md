# REVIEW_NOTES_FOR_CODEX.md

## Session Summary

The runner for EXP-0019 completed Phase 0 (Safety checks) and Phase 1 (Static Contract Review) successfully. All 15 static contract items passed verification against `environment_contract.yaml`, the Dockerfile, start.sh, and `requirements.lock.txt`. The original local build was blocked because the Windows Docker daemon was not running, but Codex later completed the canonical image build through GitHub Actions.

## What Codex Should Review

### 1. Static Contract Consistency (PASS)
All version pins and runtime behaviors are internally consistent:
- `environment_contract.yaml` -> `docker/Dockerfile` -> `docker/start.sh` -> `src/verify_environment.py` -> `requirements.lock.txt`
- No discrepancies found. The image package is correct as spec'd.

### 2. Build Completed (IMAGE PRODUCED)
- Build record ID: `C4HFU6`
- Duration: 7m12s
- Short SHA tag: `ghcr.io/pasavee123/cexar-a40:cuda121-torch231-03b1e78`
- Full SHA tag: `ghcr.io/pasavee123/cexar-a40:cuda121-torch231-03b1e789264b581b1166f7fd0c8416d717116858`
- The runner-reserved local build tag `ghcr.io/pasavee123/cexar-a40:cuda121-torch231-c1faf58` was not built and remains historical evidence only.
- The installed GitHub Actions workflow is `.github/workflows/build-cexar-a40-image.yml`.

### 3. Next Steps For Codex

- Prepare EXP-0020 using the full SHA image tag.
- Verify runtime behavior on RunPod A40 before RAD-DINO smoke testing.
- Confirm `/workspace`, Hugging Face cache, SSH, Python, CUDA, PyTorch, and GPU visibility.

### 4. No Safety Violations
- No secrets, SSH keys, PATs, hostnames, or private IPs were written to any file.
- No production code, standards, or manifests were modified.
- No global Python or system configuration was changed.
- No clinical claims were made.
- No RAD-DINO inference, training, or dataset work occurred.

### 5. Required Follow-Up (from RESULT.md)
> Use the full SHA image tag in EXP-0020 and validate it on RunPod A40.
