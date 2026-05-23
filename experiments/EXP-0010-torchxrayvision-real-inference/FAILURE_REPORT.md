# FAILURE_REPORT.md

## Experiment

EXP-0010-torchxrayvision-real-inference

## Status

SUPERSEDED BY ADMIN RERUN.

Previous status: HARD_BLOCKED due to Environment Isolation.

The previous hard block was valid for the default sandboxed runner shell. After the user relaunched the IDE with administrator privileges, the host Python path still remained inaccessible to the default sandbox shell, but venv creation succeeded through an elevated/outside-sandbox execution path.

## Issue Summary

EXP-0010 cannot proceed past Phase 0 in the current runner session.

The first run failed because `python` was not available on PATH. A host Python executable was then identified:

```text
C:\Users\pasav\AppData\Local\Programs\Python\Python310\python.exe
```

However, the runner session still reported that this full host path is not recognized in the current environment. This strongly suggests that the runner is operating inside an isolated sandbox/container that cannot see or execute host filesystem paths.

## Root Cause

The current runner environment does not expose a usable Python runtime to the session:

- `python` is not available on PATH.
- `py`/Windows launcher does not expose an installed Python runtime.
- The known host Python full path is not visible to the runner.

This is an environment isolation boundary, not a TorchXRayVision failure.

## Scope Compliance

- No production code modified.
- No manifests modified.
- No standards modified.
- No repo_hunt files modified.
- No global Python rollback attempted.
- No packages installed.
- No model inference run.

## Required Human Action

Rerun EXP-0010 from a non-isolated terminal or a host-authenticated terminal where Python is visible.

Before rerunning, confirm one of these works in the runner terminal:

```powershell
python --version
```

or:

```powershell
& "C:\Users\pasav\AppData\Local\Programs\Python\Python310\python.exe" --version
```

Then resume with:

```powershell
& "C:\Users\pasav\AppData\Local\Programs\Python\Python310\python.exe" -m venv .venvs\cexar-baseline
```

## Recommendation

Continue EXP-0010 only through the execution path that can access `.venvs\cexar-baseline`. The default sandbox shell should not be used for Python, pip, package installation, or inference steps if it cannot execute the venv interpreter.

## Final Note

The experiment later progressed successfully through package installation, package verification, XRV smoke test, and synthetic fallback inference. There is no active model failure in the current EXP-0010 result. The remaining limitation is the absence of real CXR image files in the repository.
