# REVIEW_NOTES_FOR_CODEX.md

## Phase A Result

DeepSeek authored the EXP-0021 scripts. Codex reviewed and applied pre-run fixes.

## Scripts Authored

| File | Purpose |
|------|---------|
| `scripts/build_manifest_10k.py` | Deterministic 10k manifest builder |
| `scripts/run_rad_dino_embedding_10k.py` | Resumable RAD-DINO embedding extraction |
| `scripts/run_exp0021_10k.sh` | One-shot orchestrator with environment checks |

## Codex Review Checklist

- [x] Scripts are confined to experiment folder
- [x] Large artifacts write only to `/workspace/exp_artifacts/EXP-0021`
- [x] Dry-run and full-run artifacts are isolated by run label
- [x] Dataset roots are read-only from the script perspective
- [x] No script deletes, moves, or overwrites dataset/cache/repo roots
- [x] No script installs packages or modifies `/opt/venv`
- [x] Runtime check requires NVIDIA RTX 6000 Ada Generation
- [x] Python invocation uses `/opt/venv/bin/python`
- [x] CheXpert CSV paths are resolved against `/workspace/chexpert_dataset_raw`
- [x] Dry-run modes implemented
- [x] Resume/checkpoint behavior implemented
- [x] Summary JSON includes image counts, runtime, GPU, cache location, shard list, and failures
- [x] No training, classifier fitting, AUROC/AUPRC, or clinical claims

## Codex Fixes Applied

- Changed embedding extraction to match EXP-0020: `outputs.last_hidden_state[:, 0, :]`.
- Added run-label artifact isolation to prevent dry-run checkpoint pollution.
- Added strict non-zero exit for partial/incomplete runs unless `--allow-partial` is explicitly passed.
- Added failure JSONL logging for image-level exceptions.
- Changed checkpoint semantics so only successful image indices are marked complete. Failed images remain retryable on resume.

## Pre-Run Verdict

`APPROVE_DRY_RUN_ONLY`

The next step is to run:

```bash
bash experiments/EXP-0021-rad-dino-10k-cloud-embedding-run/scripts/run_exp0021_10k.sh --limit 5 --dry-run-label dryrun5
bash experiments/EXP-0021-rad-dino-10k-cloud-embedding-run/scripts/run_exp0021_10k.sh --limit 100 --dry-run-label dryrun100
```

Do not run the full 10k command until Codex reviews the dry-run outputs and upgrades the verdict to `APPROVE_FULL_10K_RUN`.

## Post-Run Codex Verification

Codex inspected the dry-run and full-run lightweight summaries plus the external full-run checkpoint and shard inventory on 2026-05-27.

Observed dry-run summaries:

- `dryrun5`: 5 attempted, 5 succeeded, 0 failed, embedding dimension 768.
- `dryrun100`: 100 attempted, 100 succeeded, 0 failed, embedding dimension 768.

Observed full-run summary:

- 10,000 images attempted.
- 10,000 images succeeded.
- 0 images failed.
- 10 shard files listed.
- Embedding dimension reported as 768.
- GPU reported as `NVIDIA RTX 6000 Ada Generation`.
- `allow_partial` reported as false.

Observed checkpoint:

- `success_count`: 10000.
- `completed_indices` length: 10000.
- First indices: `[0, 1, 2]`.
- Last indices: `[9997, 9998, 9999]`.
- `next_shard_id`: 10.

Codex also inspected the `.npz` shard internals with `/opt/venv/bin/python`; ten shard files were present, total embedding rows were 10000, and no shard had a non-`[N, 768]` embedding shape.

Final Codex verdict: `PASS_AS_EMBEDDING_REHEARSAL`.

This verdict is limited to artifact production and documentation review. It is not a clinical evaluation, does not include AUROC/AUPRC, and does not approve production integration.
