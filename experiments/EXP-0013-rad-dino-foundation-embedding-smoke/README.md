# EXP-0013 RAD-DINO Foundation Embedding Smoke

## Purpose

Test whether RAD-DINO can run in an isolated foundation environment and produce embeddings for the same 100 CheXpert sample images used by EXP-0012B.

## Final Status

PASS AS RAD-DINO EMBEDDING SMOKE TEST.

## Key Result

- Model: `microsoft/rad-dino`
- Images attempted: 100
- Images succeeded: 100
- Embedding shape: `[100, 768]`
- Runtime: 90.35 seconds
- Device: CPU

## Scope

This experiment was an embedding compatibility smoke test only.

No classification, AUROC, training, thresholding, production integration, or medical claims were performed.

## Audit Note

On 2026-05-24, Codex found that the experiment folder had been polluted with RAD-DINO snapshot files and some experiment documentation files were missing. This README was restored as experiment documentation. The model card content that had overwritten this README appears to belong to the downloaded RAD-DINO snapshot.
