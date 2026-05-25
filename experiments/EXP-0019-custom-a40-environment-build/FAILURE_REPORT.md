# FAILURE_REPORT.md

## Final Status: RESOLVED INCIDENTS - Final Build Passed Via GitHub Actions

The runner session originally stopped at Phase 2 because the local Windows Docker daemon was unreachable. This blocker was resolved by using the installed GitHub Actions workflow. The final image build completed successfully.

## Resolution Evidence

| Field | Value |
|-------|-------|
| Successful build system | GitHub Actions |
| Build record ID | `C4HFU6` |
| Status | Completed |
| Duration | 7m12s |
| Short SHA tag | `ghcr.io/pasavee123/cexar-a40:cuda121-torch231-03b1e78` |
| Full SHA tag | `ghcr.io/pasavee123/cexar-a40:cuda121-torch231-03b1e789264b581b1166f7fd0c8416d717116858` |

## Original Local Failure Details

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

1. Use the full SHA image tag in EXP-0020.
2. Boot the image on RunPod A40.
3. Run runtime verification inside the container.
4. Only after runtime verification passes, proceed to RAD-DINO 100-image GPU smoke testing.

## Attempt Budget Status

- Docker build attempts: local runner attempt blocked; GitHub Actions build completed successfully.
- Dependency/version fix attempts: 0 of 2 used. Not needed; contract is clean.
- Registry/GHCR attempts: 0 of 2 used.
