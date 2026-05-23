# EXP-0014 Multi-Model Contract Comparison

## Purpose

Compare the output contracts of the XRV DenseNet121 baseline and RAD-DINO foundation embedding pipeline on the same EXP-0012B sample.

## Scope

This is a contract comparison and adapter-design experiment.

Allowed:

- Read existing EXP-0012B and EXP-0013 artifacts.
- Verify sample alignment.
- Compare output schema, shape, label/embedding semantics, and downstream requirements.
- Draft a CeXaR model adapter contract.

Forbidden:

- No new model inference unless artifact corruption blocks the comparison.
- No training.
- No RAD-DINO classification.
- No AUROC or new metric calculation.
- No threshold tuning.
- No production integration.
- No global Python or venv modification.

## Inputs

XRV artifacts:

```text
experiments/EXP-0012B-xrv-stratified-metric-fix/artifacts/sample_manifest.csv
experiments/EXP-0012B-xrv-stratified-metric-fix/artifacts/xrv_chexpert_outputs.csv
experiments/EXP-0012B-xrv-stratified-metric-fix/artifacts/metric_sanity.json
```

RAD-DINO artifacts:

```text
experiments/EXP-0013-rad-dino-foundation-embedding-smoke/artifacts/rad_dino_embedding_summary.json
experiments/EXP-0013-rad-dino-foundation-embedding-smoke/artifacts/rad_dino_embeddings.npz
```

## Expected Verdict

PASS AS MULTI-MODEL CONTRACT COMPARISON.

This experiment cannot establish clinical performance.
