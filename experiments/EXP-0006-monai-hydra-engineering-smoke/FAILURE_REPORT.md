# FAILURE_REPORT.md

## Status

RETROSPECTIVE FAILURE: uncontrolled global environment mutation.

## Failure Summary

The original EXP-0006 run installed MONAI/Hydra into the global Python environment. During dependency resolution, PyTorch was upgraded from `2.0.1` to `2.12.0`.

This is a failure of experiment isolation, not proof that MONAI or Hydra are unsuitable.

## Impact

- Prior runtime assumptions for EXP-0002 through EXP-0005 were invalidated.
- The result cannot be treated as integration-ready.
- MONAI/Hydra must be rerun in a dedicated isolated environment.

## Files Touched

No production code changes were documented. Environment packages were changed globally during the original run.

## Required Follow-Up

Create a new isolated MONAI/Hydra experiment using a dedicated venv and pinned requirements.

## Audit Note

Audit Pass 2, 2026-05-23: This failure report was created retroactively from existing logs and Codex review findings.
