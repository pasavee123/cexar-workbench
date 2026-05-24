# RESULT.md — EXP-0014

## Status

PASS AS MULTI-MODEL CONTRACT COMPARISON.

## Summary

EXP-0014 compared the output contracts of XRV DenseNet121 (supervised classifier) and RAD-DINO (foundation image encoder) using the same 100-image CheXpert validation sample from EXP-0012B. The contract comparison correctly distinguishes classifier outputs from embedding outputs and provides a draft adapter contract for CeXaR.

## Evidence

### Artifact Availability

All 5 required input artifacts from EXP-0012B and EXP-0013 were present and readable at run time:

| Artifact | Source | Exists |
|----------|--------|--------|
| sample_manifest.csv | EXP-0012B | Yes |
| xrv_chexpert_outputs.csv | EXP-0012B | Yes |
| metric_sanity.json | EXP-0012B | Yes |
| rad_dino_embedding_summary.json | EXP-0013 | Yes |
| rad_dino_embeddings.npz | EXP-0013 | Yes |

### Sample Alignment

- sample_manifest.csv: 100 rows (indices 0–99)
- xrv_chexpert_outputs.csv: 100 rows (indices 0–99)
- rad_dino_embedding_summary.json: 100 attempted, 100 succeeded
- rad_dino_embeddings.npz: shape [100, 768], indices 0–99
- **Alignment status: matched** — all artifacts refer to the same 100-image sample with consistent indices.

### XRV Output Contract

- **Model family**: supervised chest X-ray classifier (TorchXRayVision densenet121-res224-all v1.4.0)
- **Output type**: per-class pathology logit scores
- **Output shape**: [100, 18]
- **Label space**: 18 explicit XRV pathologies, 11 mapped to CheXpert
- **Direct metrics**: Yes — 9 of 11 AUROC values computable (2 excluded due to single-class sample)
- **Requires downstream head**: No

### RAD-DINO Output Contract

- **Model family**: foundation image encoder (microsoft/rad-dino)
- **Output type**: image embeddings (frozen backbone)
- **Output shape**: [100, 768]
- **Embedding dimension**: 768
- **Label space**: None
- **Direct metrics**: No — requires a downstream classification head
- **Requires downstream head**: Yes

### Adapter Contract Draft

Generated `artifacts/cexar_adapter_contract_draft.md` with:
- Generic contract schema (6 sections: identity, input, output, metrics, safety, artifacts)
- Concrete XRV instance (from EXP-0012B)
- Concrete RAD-DINO instance (from EXP-0013)
- Contract enforcement rules (6 rules)
- Multi-model comparison summary table

## Scope Compliance

| Constraint | Complied |
|------------|----------|
| Read-only comparison | Yes |
| No packages installed | Yes |
| No global Python modified | Yes |
| No .venvs modified | Yes |
| No EXP-0012B artifacts modified | Yes |
| No EXP-0013 artifacts modified | Yes |
| No new model inference | Yes |
| No training | Yes |
| No RAD-DINO classification | Yes |
| No AUROC computed | Yes |
| No threshold tuning | Yes |
| No production integration | Yes |
| All commands in commands.ps1 | Yes |
| All commands logged in EXPERIMENT_LOG.md | Yes |

## Output Artifacts

- `artifacts/sample_alignment_report.json` — alignment verified, 100 images, indices matched
- `artifacts/model_output_contract_comparison.json` — XRV vs RAD-DINO contracts with key differences
- `artifacts/cexar_adapter_contract_draft.md` — generic adapter schema + 2 concrete instances
- `artifacts/run_contract_comparison.py` — comparison script (source)

## Known Limitations

- N=100 sample (deterministic random, seed=42). High variance.
- No RAD-DINO downstream classification was performed; adapter contract assumes a downstream head.
- CPU-only inference for both prior experiments.
- Public RAD-DINO checkpoint may not match paper setup (EXP-0003 finding).
- Adapter contract is a draft; has not been validated with additional model families.
- Spurious empty directory `artifacts/artifacts/` exists from a one-time path resolution fix during script development. Not cleaned per cleanup protocol.

No clinical claims are made. This is a structural contract comparison only.