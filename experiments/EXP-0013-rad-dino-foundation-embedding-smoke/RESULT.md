# RESULT.md

## Verdict

PASS AS RAD-DINO EMBEDDING SMOKE TEST.

## Summary

EXP-0013 demonstrated that RAD-DINO (`microsoft/rad-dino`) can run in the isolated foundation environment `.venvs\cexar-foundation` and produce image embeddings for the same 100 CheXpert images used by EXP-0012B.

## Evidence

- Model: `microsoft/rad-dino`
- Weight source: downloaded during the session after human approval, then loaded from local cache
- Images attempted: 100
- Images succeeded: 100
- Images failed: 0
- Embedding shape: `[100, 768]`
- Hidden size: 768
- Runtime: 90.35 seconds
- Effective device: CPU
- CUDA available: false
- Main summary artifact: `artifacts/rad_dino_embedding_summary.json`
- Embedding artifact: `artifacts/rad_dino_embeddings.npz`

## Scope Compliance

- No classification performed.
- No AUROC computed.
- No training performed.
- No threshold tuning performed.
- No production integration performed.
- No clinical claims made.

## Limitations

- CPU-only inference; GPU/VRAM behavior was not tested.
- This confirms embedding pipeline compatibility only.
- Embedding quality and downstream classification performance were not evaluated.
- Public RAD-DINO checkpoint may not exactly match the paper setup, per EXP-0003 findings.

## Audit Note

On 2026-05-24, this file was restored because `RESULT.md` was missing when preparing EXP-0014. The result content is reconstructed from `artifacts/rad_dino_embedding_summary.json`, `EXPERIMENT_LOG.md`, and prior Codex review.
