# EXP-0016: CheXpert Scale-Up Readiness

## Purpose

This experiment checks whether CeXaR is ready to scale from the 100-image smoke-test sample to a larger CheXpert subset for RAD-DINO downstream training.

This is a dataset readiness and planning experiment. It is not model training and not clinical performance evaluation.

## Dataset

Expected local dataset root:

```text
D:\Dataset_Chexpert
```

The runner must inspect the dataset structure safely and report what CSV files, image paths, labels, and patient identifiers are available.

## Scope

The runner may:

- Inspect dataset files under `D:\Dataset_Chexpert`.
- Create candidate manifests inside this experiment folder.
- Check image path existence for selected samples.
- Compute label distribution.
- Test patient-level split feasibility.
- Estimate runtime/storage for future RAD-DINO embedding generation.

The runner must not:

- Modify the dataset.
- Copy images into the repository.
- Run RAD-DINO inference.
- Train any model.
- Fine-tune RAD-DINO.
- Modify production code.
- Make clinical claims.

## Expected Outcome

EXP-0016 should answer whether EXP-0017 can safely begin true downstream linear-probe training, and what sample size/labels/split policy should be used first.

