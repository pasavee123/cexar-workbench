# DIFF_SUMMARY.md

## Files Created

None. No new files were created during this run.

## Files Modified

| File | Type of Change | Summary |
|------|---------------|---------|
| `commands.ps1` | Content added | 8 commands registered (CMD-001 through CMD-008) covering Phase 0 environment checks and Phase 2 build attempt. |
| `EXPERIMENT_LOG.md` | Content added | Phase 0 and Phase 1 results logged. Phase 2 blocker documented with CMD-006/007/008 results. |
| `RESULT.md` | Content added | Final status set to BLOCKED. Pass/fail criteria table populated with 7 PASS, 4 NOT EXECUTED. |
| `FAILURE_REPORT.md` | Content added | Detailed blocker description, root cause (stopped Docker daemon), and 3 recommended next actions. |
| `REVIEW_NOTES_FOR_CODEX.md` | Content added | Summary for Codex review with pass/fail breakdown. |
| `DIFF_SUMMARY.md` | Content added | This file. |

## Codex Post-Review Files Created

| File | Type of Change | Summary |
|------|---------------|---------|
| `.github/workflows/build-cexar-a40-image.yml` | Created | Manual GitHub Actions workflow for canonical linux/amd64 image build and GHCR push. |

## Codex Post-Review Files Modified

| File | Type of Change | Summary |
|------|---------------|---------|
| `BUILD_AND_PUSH_NOTES.md` | Updated | Marked GitHub Actions as the selected canonical build path. |
| `RESULT.md` | Updated | Required follow-up now points to the installed manual workflow. |
| `REVIEW_NOTES_FOR_CODEX.md` | Updated | Notes now state the workflow is installed and ready for manual trigger. |
| `EXPERIMENT_LOG.md` | Updated | Added Codex post-review update note. |
| `commands.ps1` | Corrected | Clarified CMD-004 was non-conclusive after CMD-006 proved daemon unreachable. |
| `FAILURE_REPORT.md` | Corrected | Replaced non-ASCII dash rendering with plain ASCII text. |

## Codex Post-Review Workflow Fix

| File | Type of Change | Summary |
|------|---------------|---------|
| `.github/workflows/build-cexar-a40-image.yml` | Updated | Added disk cleanup before CUDA image build, plain BuildKit logs, and disabled provenance output. |
| `BUILD_AND_PUSH_NOTES.md` | Updated | Documented disk cleanup rationale for large CUDA/PyTorch build. |
| `EXPERIMENT_LOG.md` | Updated | Recorded first GitHub Actions build failure and workflow-level mitigation. |

## Codex No-Space Build Mitigation

| File | Type of Change | Summary |
|------|---------------|---------|
| `.github/workflows/build-cexar-a40-image.yml` | Updated | Expanded disk cleanup to remove swap, hosted tool cache, Android, .NET, GHC, Boost, ghcup, and apt lists before build. |
| `docker/Dockerfile` | Updated | Added pip no-cache environment settings and cleanup of temporary/cache directories after install layers. |
| `BUILD_AND_PUSH_NOTES.md` | Updated | Documented the no-space mitigation. |
| `EXPERIMENT_LOG.md` | Updated | Recorded the `Errno 28` failure and mitigation. |

## Codex Docker Root Relocation Mitigation

| File | Type of Change | Summary |
|------|---------------|---------|
| `.github/workflows/build-cexar-a40-image.yml` | Updated | Moved Docker data root to `/mnt/docker` before the build to avoid root filesystem exhaustion. |
| `BUILD_AND_PUSH_NOTES.md` | Updated | Documented `/mnt/docker` rationale. |
| `EXPERIMENT_LOG.md` | Updated | Recorded second no-space failure and Docker root relocation mitigation. |

## Codex WarpBuild Runner Selection Update

| File | Type of Change | Summary |
|------|---------------|---------|
| `.github/workflows/build-cexar-a40-image.yml` | Updated | Added manual `runner_label` input and changed `runs-on` to use the selected runner label. |
| `BUILD_AND_PUSH_NOTES.md` | Updated | Documented WarpBuild Runner ID usage and disk requirement rationale. |
| `EXPERIMENT_LOG.md` | Updated | Recorded WarpBuild path selection without changing the environment contract. |

## Codex WarpBuild Default Runner Update

| File | Type of Change | Summary |
|------|---------------|---------|
| `.github/workflows/build-cexar-a40-image.yml` | Updated | Default `runner_label` set to `warp-ubuntu-latest-x86-64-16x`. |
| `BUILD_AND_PUSH_NOTES.md` | Updated | Documented selected WarpBuild default runner. |
| `EXPERIMENT_LOG.md` | Updated | Recorded default runner change from `ubuntu-latest` to WarpBuild. |

## Files NOT Modified

| File | Reason |
|------|--------|
| `docker/Dockerfile` | Static review confirmed no changes needed |
| `docker/start.sh` | Static review confirmed no changes needed |
| `src/verify_environment.py` | Static review confirmed no changes needed |
| `requirements.lock.txt` | Static review confirmed no changes needed |
| `environment_contract.yaml` | Runner must not modify contracts |
| `BUILD_AND_PUSH_NOTES.md` | Reference only |
| `RUNPOD_TEMPLATE_NOTES.md` | Reference only |
| `RUNNER_PREFLIGHT_SAFETY_PROMPT.md` | Reference only |
| All `standards/` files | Runner must not modify standards |
| All EXP-0018 files | Runner must not modify other experiments |
| Production code | Not in scope |
