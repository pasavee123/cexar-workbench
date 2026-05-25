# REVIEW_NOTES_FOR_CODEX.md

## Session Summary

The runner for EXP-0019 completed Phase 0 (Safety checks) and Phase 1 (Static Contract Review) successfully. All 15 static contract items passed verification against `environment_contract.yaml`, the Dockerfile, start.sh, and `requirements.lock.txt`. The experiment was blocked at Phase 2 because the Docker daemon was not running on the Windows runner host.

## What Codex Should Review

### 1. Static Contract Consistency (PASS)
All version pins and runtime behaviors are internally consistent:
- `environment_contract.yaml` -> `docker/Dockerfile` -> `docker/start.sh` -> `src/verify_environment.py` -> `requirements.lock.txt`
- No discrepancies found. The image package is correct as spec'd.

### 2. Build Blocked (NO IMAGE PRODUCED)
- The runner-reserved local build tag `ghcr.io/pasavee123/cexar-a40:cuda121-torch231-c1faf58` was not built and is superseded by the migrated organization package path.
- Canonical GHCR output now uses `ghcr.io/cexar-lab/cexar-a40`.
- The installed GitHub Actions workflow will generate new short-SHA and full-SHA tags from the commit that contains the workflow.
- The `docker build` command template is fully registered in `commands.ps1` (CMD-006).
- The GitHub Actions workflow is installed at `.github/workflows/build-cexar-a40-image.yml`.

### 3. Next Steps For Codex

- **If using local build:** Codex should wait for the human to start Docker Desktop, then re-issue the CMD-006 build command and continue through Phases 3-5.
- **If using GitHub Actions:** The workflow is installed at `.github/workflows/build-cexar-a40-image.yml`. The human should trigger it manually from the GitHub Actions tab.
- **After build succeeds:** Codex should run Phases 3-5 (container verification, GHCR readiness, A40 GPU verification) in the same experiment folder, using the existing ledger.

### 4. No Safety Violations
- No secrets, SSH keys, PATs, hostnames, or private IPs were written to any file.
- No production code, standards, or manifests were modified.
- No global Python or system configuration was changed.
- No clinical claims were made.
- No RAD-DINO inference, training, or dataset work occurred.

### 5. Required Follow-Up (from RESULT.md)
> Human starts Docker Desktop and re-runs EXP-0019 from Phase 2, OR
> Human triggers the installed GitHub Actions workflow after it has been pushed.
