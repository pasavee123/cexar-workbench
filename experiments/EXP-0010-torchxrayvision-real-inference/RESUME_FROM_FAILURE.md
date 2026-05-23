# Resume From Failure: EXP-0010

## Status

The first EXP-0010 run stopped correctly because `python` was not available on PATH.

A host Python executable was later identified:

```text
C:\Users\pasav\AppData\Local\Programs\Python\Python310\python.exe
```

However, a subsequent runner session reported that this host path is still not recognized inside
the current execution environment. This suggests the runner is isolated from the host filesystem.

## Resume Instruction

Continue EXP-0010 from Phase 0 only as an environment audit. Do not keep retrying the host Python
path if it is not visible.

Try the host path once only if needed:

```powershell
& "C:\Users\pasav\AppData\Local\Programs\Python\Python310\python.exe" -m venv .venvs\cexar-baseline
```

Then activate:

```powershell
.\.venvs\cexar-baseline\Scripts\Activate.ps1
```

Then verify:

```powershell
python -c "import sys; assert '.venvs' in sys.prefix, 'NOT IN VENV - ABORT'; print(sys.prefix)"
```

## Constraints

- Do not modify global Python.
- Do not rely on host paths if the runner cannot see them.
- Do not rollback anything.
- Do not use `--force-reinstall`.
- After activation, use the venv's `python` and `pip` only.
- Continue following `experiments/EXP-0009-env-isolation-plan/NEXT_REAL_RUN_PROMPT.md`.

## If Host Python Is Not Visible

Run a read-only internal runtime audit:

```powershell
Get-Command python -ErrorAction SilentlyContinue
Get-Command py -ErrorAction SilentlyContinue
Get-Command python3 -ErrorAction SilentlyContinue
where.exe python
where.exe py
where.exe python3
```

If no usable internal Python runtime is found, stop and update `FAILURE_REPORT.md` with:

```text
HARD_BLOCKED due to Environment Isolation
```

Recommend that the user rerun EXP-0010 from a non-isolated terminal or a host-authenticated
terminal where Python is visible.
