# EXP-0017: RAD-DINO True Linear Probe Training v1

## Purpose

This is the first controlled downstream training experiment for RAD-DINO in CeXaR.

The experiment trains lightweight classification heads on frozen RAD-DINO embeddings from a 1,000-image CheXpert manifest. This is still a research pipeline experiment, not clinical validation and not production integration.

## Clean Start Note

EXP-0017 was reset before execution because an earlier runner session stopped mid-run due to token exhaustion. No prior EXP-0017 outputs were committed. This folder is a clean specification for a fresh run.

## Required Precondition

EXP-0016 found that the default random patient-level split is structurally valid but not metric-ready for every label. EXP-0017 must create or validate a corrected patient-level split before training.

Labels requiring split correction or metric masking:

- Atelectasis
- Pneumonia
- Lung Lesion
- Fracture
- Lung Opacity

## Scope

The runner may:

- Read EXP-0016 manifest artifacts.
- Create a corrected patient-level split artifact inside this experiment.
- Generate RAD-DINO embeddings for the selected 1,000-image manifest if no matching embeddings already exist.
- Train lightweight downstream probes on frozen embeddings only.
- Compute research pipeline metrics only for labels with valid class representation.

The runner must not:

- Fine-tune RAD-DINO.
- Modify production code.
- Modify CheXpert dataset files.
- Copy images into the repository.
- Make clinical claims.
- Treat this as production readiness.

