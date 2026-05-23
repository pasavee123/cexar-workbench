# TEST_PLAN.md

## Original Test Intent

1. Install MONAI and Hydra.
2. Run a MONAI deterministic transform smoke test.
3. Run a Hydra config composition smoke test.

## Retrospective Assessment

The tests showed MONAI and Hydra could execute, but the environment was not isolated. The package install upgraded global PyTorch and contaminated the shared environment.

## Required Rerun Plan

Future validation must:

- Use a dedicated venv such as `.venvs\cexar-training`.
- Avoid global Python.
- Pin PyTorch and MONAI/Hydra versions.
- Record `pip freeze`.
- Stop if dependency resolution attempts to mutate another environment.

## Audit Note

Audit Pass 2, 2026-05-23: This file was created after the original experiment to document the intended and corrected test plan.
