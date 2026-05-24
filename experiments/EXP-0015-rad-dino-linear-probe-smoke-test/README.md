# EXP-0015: RAD-DINO Linear Probe Smoke Test

## Purpose

This experiment checks whether RAD-DINO embeddings from EXP-0013 can support a minimal downstream classification-head workflow on the same 100-image CheXpert sample from EXP-0012B.

This is a smoke test only. It is not a clinical performance evaluation.

## Scope

The runner may:

- Read EXP-0012B, EXP-0013, and EXP-0014 artifacts.
- Load `rad_dino_embeddings.npz`.
- Load labels from `sample_manifest.csv`.
- Build a deterministic train/eval split.
- Train a lightweight downstream probe only if labels are valid.
- Report class balance, valid labels, skipped labels, and sanity metrics.

The runner must not:

- Run RAD-DINO inference again.
- Fine-tune RAD-DINO.
- Modify existing experiment artifacts.
- Modify production code.
- Make clinical claims.

## Expected Outcome

The output should tell Codex and the human reviewer whether the downstream probe path is technically viable, which labels can be used, and what must be fixed before larger-scale training.

