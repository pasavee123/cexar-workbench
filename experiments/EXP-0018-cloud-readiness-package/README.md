# EXP-0018: Cloud Readiness Package

## Purpose

Prepare CeXaR for controlled cloud execution after EXP-0017 proved the RAD-DINO frozen-embedding linear-probe path on 1,000 CheXpert images.

This experiment prepares configs, audit contracts, code skeletons, and SSH templates for EXP-0019 cloud smoke execution. It does not run cloud training.

## Fixed Human Decision

The target GPU is fixed by the human:

```text
NVIDIA A40
```

The runner must not choose a different GPU. If A40 is unavailable, the runner must stop and report the blocker instead of selecting an alternative.

## Non-Goals

- Do not start a cloud instance.
- Do not run SSH commands.
- Do not upload credentials.
- Do not upload dataset images.
- Do not run RAD-DINO inference.
- Do not train a model.
- Do not make clinical claims.

