# RUNNER_INSTRUCTIONS.md

## Retrospective Instruction

Do not rerun this experiment as originally executed.

The original run used global Python and caused an uncontrolled PyTorch upgrade. Any future MONAI/Hydra validation must be a new experiment in an isolated environment.

## Future Runner Rules

- Create a new experiment folder.
- Use a dedicated venv.
- Register every command in `commands.ps1` before execution.
- Write `EXPERIMENT_LOG.md` throughout the run.
- Write `FAILURE_REPORT.md` immediately if dependency resolution attempts a global install or upgrade.

## Audit Note

Audit Pass 2, 2026-05-23: This file was created after the original experiment to prevent repetition of the unsafe execution pattern.
