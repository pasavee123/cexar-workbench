# FAILURE_REPORT.md

## Status

No failure. EXP-0014 completed successfully (PASS AS MULTI-MODEL CONTRACT COMPARISON).

## Transient Errors During Execution

Two script-level bugs were encountered and fixed during `run_contract_comparison.py` development:

1. **Syntax Error (Attempt 1)**: f-string backslash in Python 3.10 — `f'\"{l}\"'` is invalid. Fixed by pre-computing quoted label strings before the f-string block.

2. **Path Resolution Error (Attempt 2)**: `BASE` was computed with 2 `os.path.dirname` calls, but the script is inside `artifacts/`, so 3 `os.path.dirname` calls are needed to reach `experiments/`. Fixed by adding a third `os.path.dirname`.

Both were script authoring bugs, not environment or artifact failures. The final run (Attempt 3) completed with exit code 0 and produced all 3 required output artifacts.

## Spurious Directory

An empty `artifacts/artifacts/` directory was created during script development. This is harmless and was not cleaned per protocol. Awaiting human approval for removal.