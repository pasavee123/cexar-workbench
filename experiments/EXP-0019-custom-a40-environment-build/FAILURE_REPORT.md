# FAILURE_REPORT.md

## Final Status: BLOCKED - Docker Daemon Not Running

The experiment stopped at Phase 2 (Docker Build Check) because the Docker daemon is unreachable.

## Failure Details

| Field | Value |
|-------|-------|
| Failed step | Phase 2: Docker Build Check (CMD-006) |
| Failed command | `docker build --platform linux/amd64 -f experiments/EXP-0019-custom-a40-environment-build/docker/Dockerfile -t ghcr.io/pasavee123/cexar-a40:cuda121-torch231-c1faf58 experiments/EXP-0019-custom-a40-environment-build` |
| Exit code | 1 |
| Error | `Head "http://%2F%2F.%2Fpipe%2FdockerDesktopLinuxEngine/_ping": open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified.` |
| Root cause | Docker Desktop is installed (v28.3.3) but not running. WSL2 `docker-desktop` instance is `Stopped`. |
| Working directory | D:\cexar-workbench |
| Environment | Windows, Docker Desktop stopped, WSL2 stopped |

## What Was Checked

- **CMD-007:** `Get-Process "Docker Desktop"` - no process found.
- **CMD-008:** `wsl --list --verbose` - docker-desktop state is `Stopped` (version 2).

## What Passed Before The Blocker

- **Phase 0 (Safety):** All required standards and inputs read and verified.
- **Phase 1 (Static Contract Review):** All 15 contract items passed (GPU target, base image, Python/PyTorch versions, paths, SSH setup, no-auto-run policy). See `EXPERIMENT_LOG.md` for the full verification table.

## What Was NOT Executed (Blocked Work)

- Phase 2: Docker image build (daemon unavailable)
- Phase 3: Container runtime verification
- Phase 4: GHCR readiness verification
- Phase 5: A40 GPU verification (`nvidia-smi`, GPU device name)

## Files Modified During This Run

- `commands.ps1` - 8 commands registered (CMD-001 through CMD-008)
- `EXPERIMENT_LOG.md` - Phase 0 and Phase 1 logs written
- `FAILURE_REPORT.md` - This file
- `RESULT.md` - Updated with final status
- `DIFF_SUMMARY.md` - Updated
- `REVIEW_NOTES_FOR_CODEX.md` - Updated

## Production Code / Standards Touched

None. No production code, manifests, standards, or repo-hunt files were modified.

## Recommended Next Actions

1. **Human starts Docker Desktop** on the runner host (Windows), then re-run EXP-0019 from Phase 2.
2. **Alternative: Build on a separate machine** with a running Docker daemon, using the same `docker build` command registered in `commands.ps1`.
3. **Preferred follow-up: GitHub Actions** - the workflow is installed at `.github/workflows/build-cexar-a40-image.yml` and can be triggered manually from the GitHub Actions tab after this change is pushed.
4. After a successful build, continue with Phase 3 (container runtime verification) and Phase 5 (A40 GPU check if on RunPod).

## Attempt Budget Status

- Docker build attempts: 1 of 3 used. Remaining 2 attempts should not be consumed until the daemon is confirmed running.
- Dependency/version fix attempts: 0 of 2 used. Not needed; contract is clean.
- Registry/GHCR attempts: 0 of 2 used.
