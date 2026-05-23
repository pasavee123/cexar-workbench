# RUNNER_INSTRUCTIONS.md

Follow `experiments/EXP-0009-env-isolation-plan/NEXT_REAL_RUN_PROMPT.md`.

For this environment, Python and venv commands must use the elevated execution path that can access:

```text
D:\cexar-workbench\.venvs\cexar-baseline\Scripts\python.exe
```

Do not use the default sandbox shell for Python execution if it reports:

```text
No Python at 'C:\Users\pasav\AppData\Local\Programs\Python\Python310\python.exe'
```

Log every command in `EXPERIMENT_LOG.md` and `commands.ps1`.
