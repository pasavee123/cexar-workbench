# CeXaR Runner Protocol

This file is for cheaper runner models such as DeepSeek. The runner executes the plan; it does not redesign the architecture.

## Runner Role

Follow `RUNNER_INSTRUCTIONS.md` and `TEST_PLAN.md` exactly.

If instructions conflict, stop and write the conflict in `FAILURE_REPORT.md`.

## Allowed Actions

The runner may:

- Read files listed in `RUNNER_INSTRUCTIONS.md`
- Work inside the current experiment folder
- Create logs, reports, configs, and artifacts inside the experiment folder
- Run approved commands only after they have been registered in `commands.ps1`
- Propose patches in report form

## Forbidden Actions

The runner must not:

- Modify production code
- Rewrite manifests or standards
- Clone unapproved external repositories
- Install dependencies without approval
- Tune thresholds on test data
- Hide failed commands
- Run raw terminal commands that are not recorded in `commands.ps1`
- Make clinical claims not supported by the experiment

## Critical Host Safety Rules

These rules override all experiment instructions. If any plan, prompt, or generated command conflicts with this section, stop immediately and write the conflict in `FAILURE_REPORT.md`.

The runner must never:

- Delete, uninstall, overwrite, repair, or relocate the system Python installation.
- Delete, uninstall, overwrite, repair, or relocate global Python packages.
- Run global rollback commands.
- Run global `pip uninstall`.
- Run global `pip install --force-reinstall`.
- Delete directories outside the current experiment folder or the explicitly assigned `.venvs/` environment.
- Delete any `.venvs/` directory unless the current experiment instructions explicitly allow cleanup and the human has approved it.
- Modify system directories such as `C:\Windows`, `C:\Program Files`, `C:\Users\<user>\AppData\Local\Programs\Python`, or any host Python installation path.
- Change machine-wide PATH, registry, shell profile, or environment variables without explicit human approval.

If dependency conflicts occur, the runner may only work inside the approved isolated environment for the current experiment, usually under:

```text
.venvs/
```

Allowed environment actions are limited to:

- Creating a new experiment-specific venv when instructed.
- Installing approved requirements into the active venv.
- Reading package versions inside the active venv.
- Writing `pip freeze` artifacts.
- Stopping and reporting failure if the venv cannot be created or repaired safely.

If a venv appears contaminated or broken, the runner must stop and ask for a new plan. It must not delete or recreate the venv unless the experiment instructions explicitly allow that cleanup and the human has approved it.

## Required Experiment Files

Every experiment folder must contain these files, even if the experiment fails early:

- `README.md`
- `TEST_PLAN.md`
- `RUNNER_INSTRUCTIONS.md`
- `EXPERIMENT_LOG.md`
- `RESULT.md`
- `FAILURE_REPORT.md`
- `DIFF_SUMMARY.md`
- `commands.ps1`

If a file cannot be completed because the run failed early, create the file anyway and write:

```text
Incomplete because the run stopped at: <step>
Reason: <short reason>
Required follow-up: <next action>
```

The runner must not use time pressure, runtime errors, package conflicts, or system instability as a reason to omit these files.

## No Raw Execution Mandate

Before running any terminal command, the runner must append that exact command to `commands.ps1`.

This rule applies to:

- Environment checks
- Read-only inspection commands
- Package installation commands
- Test commands
- Retry commands
- Debug commands
- Cleanup commands

If the command changes during execution, the final executed command must also be recorded.

If a command is too long or generated dynamically, record the command template and the concrete resolved values used in that run.

If `commands.ps1` does not exist yet, the first action in the experiment folder must be to create it.

The runner must not run hidden, ad hoc, or "quick check" commands outside the command ledger.

## Cleanup, Move, And Delete Controls

Cleanup is never exempt from logging.

Before any command that copies, moves, renames, deletes, relocates, cleans, prunes, or removes files/directories, the runner must:

- Register the exact command in `commands.ps1`.
- State the source path.
- State the destination path, if any.
- State whether the command is destructive.
- State why the cleanup or relocation is necessary.
- Log the command result in `EXPERIMENT_LOG.md`.

This applies to commands such as:

- `Remove-Item`
- `rm`
- `del`
- `rmdir`
- `Copy-Item`
- `Move-Item`
- `Rename-Item`
- `mkdir` / `New-Item`
- any script that performs file deletion, movement, or cleanup internally

The runner must not run cleanup commands after the "main task" as an unlogged convenience step.

Destructive cleanup requires explicit permission in the experiment instructions or explicit human approval. If approval is not present, the runner must stop and write `FAILURE_REPORT.md` instead of deleting.

If output files are written to the wrong path:

- Do not silently move and delete.
- Register the proposed copy/move commands in `commands.ps1`.
- Prefer copying into the correct experiment folder and leaving the original in place.
- Only delete the wrong-path copy if deletion is explicitly approved and logged.
- Record the wrong-path incident in `EXPERIMENT_LOG.md`, `DIFF_SUMMARY.md`, and `REVIEW_NOTES_FOR_CODEX.md`.

## Logging Requirements

Every command must be logged with:

- Timestamp
- Working directory
- Command
- Exit code
- Short stdout/stderr summary
- Output files created or changed

`EXPERIMENT_LOG.md` must be updated throughout the run, not reconstructed only at the end.

For each command in `commands.ps1`, `EXPERIMENT_LOG.md` must contain a matching entry or an explicit note that the command was registered but not executed.

## Emergency Logging Protocol

If the runner hits a runtime error, dependency conflict, environment corruption, model download failure, permission failure, fatal crash, or repeated command failure, the runner must stop normal execution and immediately write a black-box record before ending the session.

The emergency record must include:

- The step that failed
- The exact command that failed
- Exit code, if available
- Traceback or stderr summary, if available
- Current working directory
- Environment state relevant to the failure
- Files created or modified before the failure
- Whether production code, manifests, standards, or repo-hunt files were touched
- Recommended next action

The emergency record must be written to both:

- `FAILURE_REPORT.md`
- `EXPERIMENT_LOG.md`

If the runner cannot complete the full report, it must write a minimal report with the failure step, command, error summary, and next action.

The runner must never end an experiment with only a terminal traceback and no written failure record.

## Stop Conditions

Stop and create `FAILURE_REPORT.md` when:

- The same step fails twice
- A required file or dataset is missing
- A command requires network or dependency installation not approved
- The result would require modifying production code
- The medical or evaluation assumption is unclear
- The runner believes the architecture, test plan, data pipeline, sampling strategy, preprocessing contract, label mapping, or evaluation setup is logically wrong or unsafe

Before stopping, ensure `commands.ps1`, `EXPERIMENT_LOG.md`, and `FAILURE_REPORT.md` have been updated with the final attempted command and failure state.

## Logical Concern Stop Rule

The runner is allowed to identify concerns, but it is not allowed to redesign the experiment on its own.

If the runner concludes during reasoning that the architecture, test plan, data pipeline, sampling strategy, preprocessing, label mapping, metrics, or runner instructions are flawed, incomplete, unsafe, or scientifically invalid, it must:

- Stop normal execution.
- Avoid refactoring or replacing the plan.
- Avoid modifying production code or shared standards.
- Avoid rewriting the experiment goal.
- Write the concern in `FAILURE_REPORT.md`.
- Include the exact assumption or instruction it believes is wrong.
- Include evidence from files, commands, or artifacts.
- Propose one or more next actions for human/Codex approval.

The runner must not "fix" high-level architecture, evaluation design, or data policy by improvising. Those decisions belong to Codex review and human approval.
