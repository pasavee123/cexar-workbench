# RESULT.md

## Final Status

PASS AS EMBEDDING REHEARSAL.

This status is limited to 10,000-image RAD-DINO embedding extraction artifact production. It is not a clinical evaluation and does not support clinical claims.

## Phase Progress

| Phase | Status |
|-------|--------|
| Phase A - Script Authoring | COMPLETE |
| Phase B - Codex Review | COMPLETE |
| Phase C - Cloud Dry Run | COMPLETE |
| Phase D - Full 10k Run | COMPLETE |

## Observed Run Results

Evidence sources:

- `/workspace/exp_artifacts/EXP-0021/runs/full_10k/summaries/exp0021_summary.json`
- `/workspace/exp_artifacts/EXP-0021/runs/full_10k/checkpoints/progress.json`
- `/workspace/exp_artifacts/EXP-0021/runs/full_10k/embeddings/`
- `artifacts/full_10k/exp0021_summary.json`
- `artifacts/full_10k/codex_verification_summary.json`

Observed values:

- `limit`: 10000
- `total_in_manifest`: 10000
- `images_attempted`: 10000
- `images_succeeded`: 10000
- `images_failed`: 0
- `embedding_dim`: 768
- `shard_size`: 1000
- `num_shards`: 10
- `runtime_seconds`: 498.3
- `device`: `cuda`
- `gpu_name`: `NVIDIA RTX 6000 Ada Generation`
- `allow_partial`: false
- `failures_log`: null

Checkpoint values:

- `success_count`: 10000
- `completed_indices` length: 10000
- first completed indices: `[0, 1, 2]`
- last completed indices: `[9997, 9998, 9999]`
- `next_shard_id`: 10

Shard verification:

- Ten `.npz` shard files were present outside git under `/workspace/exp_artifacts/EXP-0021/runs/full_10k/embeddings/`.
- The `.npz` files contained `embeddings` and `paths` arrays.
- Total embedding rows across shards: 10000.
- No shard had an embedding shape outside `[N, 768]`.

## Boundaries

No model training, classifier/probe fitting, AUROC/AUPRC calculation, clinical evaluation, production code edit, or production integration was performed or approved by this result.

Required limitations remain: dataset shift, patient leakage risk, label noise, class imbalance, calibration uncertainty, shortcut learning, missing external validation, and human-in-the-loop validation needs.
