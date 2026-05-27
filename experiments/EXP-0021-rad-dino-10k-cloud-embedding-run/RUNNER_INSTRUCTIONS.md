# RUNNER_INSTRUCTIONS.md

## Mission

Prepare and run EXP-0021 as a 10,000-image RAD-DINO embedding extraction on RunPod RTX 6000 Ada.

## Role Split

DeepSeek is allowed to author experiment-local scripts, but it is not allowed to make architectural decisions beyond this plan.

Codex must review the scripts before the real 10k run.

## Hard Rules

- Read `standards/runner_protocol.md` before any work.
- Register every terminal command in `commands.ps1` before execution.
- Record exact command text, not summaries.
- Use `/root/cexar-workbench` as the repo checkout path.
- Use `/workspace` only for datasets, model caches, and large artifacts.
- Use `/opt/venv` Python only.
- Do not modify global/system Python.
- Do not install packages unless explicitly approved by the human.
- Do not train models.
- Do not compute AUROC/AUPRC or clinical metrics.
- Do not make clinical claims.
- Do not modify production code.
- Do not push to `main`.
- Do not write secrets, hostnames, private IPs, SSH keys, API keys, or PATs into repo files.

## Attempt Budget

- Script authoring/debug attempts: 4
- dry-run 5 attempts: 3
- dry-run 100 attempts: 2
- full 10k run attempts: 1 initial run plus 1 resume attempt

If the budget is exceeded, stop and write `FAILURE_REPORT.md`.

## Required Review Gate

After writing or changing scripts, stop and request Codex review before running the full 10k job.

The runner may run static checks and small dry-runs only before Codex approval.

## Required Output

Write or update:

- `RESULT.md`
- `EXPERIMENT_LOG.md`
- `FAILURE_REPORT.md`
- `DIFF_SUMMARY.md`
- `REVIEW_NOTES_FOR_CODEX.md`
- `artifacts/exp0021_summary.json`

Do not commit large `.npz` embedding shards to git.

## Review Branch

Publish results only to:

```text
exp/0021-rad-dino-10k-result
```

If the branch already exists, create:

```text
exp/0021-rad-dino-10k-result-YYYYMMDD-HHMM
```

