# commands.ps1

# Runner command ledger for EXP-0021.
# Every terminal command must be appended here before execution.
# Record exact command text, purpose, expected output, and result.

# ---- Phase A: Script Authoring (no terminal commands executed on RunPod) ----
# Date: 2026-05-27 09:20 UTC
# Three scripts authored per TEST_PLAN.md Phase A:
#   - scripts/build_manifest_10k.py
#   - scripts/run_rad_dino_embedding_10k.py
#   - scripts/run_exp0021_10k.sh
# No Runtime Terminal commands were executed during Phase A (script authoring on Windows workspace).
# The commands below were originally proposed for Phase C/D execution on RunPod.

# ---- Phase C dry-run commands ----
# CMD-001: Dry-run 5 images
# Purpose: Verify full pipeline on 5 images
# Working directory: /root/cexar-workbench
# Command: bash experiments/EXP-0021-rad-dino-10k-cloud-embedding-run/scripts/run_exp0021_10k.sh --limit 5 --dry-run-label dryrun5
# Destructive: No
# Result observed from artifacts/dryrun5/exp0021_summary.json: exit code not directly observed by Codex; generated summary reports 5 attempted, 5 succeeded, 0 failed, embedding_dim 768.

# CMD-002: Dry-run 100 images
# Purpose: Verify full pipeline on 100 images
# Working directory: /root/cexar-workbench
# Command: bash experiments/EXP-0021-rad-dino-10k-cloud-embedding-run/scripts/run_exp0021_10k.sh --limit 100 --dry-run-label dryrun100
# Destructive: No
# Result observed from artifacts/dryrun100/exp0021_summary.json: exit code not directly observed by Codex; generated summary reports 100 attempted, 100 succeeded, 0 failed, embedding_dim 768.

# ---- Phase D full run command ----
# CMD-003: Full 10k run
# Purpose: Run 10,000-image RAD-DINO embedding extraction
# Working directory: /root/cexar-workbench
# Command: bash experiments/EXP-0021-rad-dino-10k-cloud-embedding-run/scripts/run_exp0021_10k.sh --limit 10000
# Destructive: No
# Result observed from artifacts/full_10k/exp0021_summary.json and /workspace/exp_artifacts/EXP-0021/runs/full_10k/summaries/exp0021_summary.json: exit code not directly observed by Codex; generated summary reports 10000 attempted, 10000 succeeded, 0 failed, embedding_dim 768, 10 shards.

# ---- Codex 2026-05-27 verification commands ----
# CMD-004: Full-run summary inspection
# Purpose: Inspect generated full-run summary JSON.
# Working directory: /root/cexar-workbench
# Command: python3 -m json.tool /workspace/exp_artifacts/EXP-0021/runs/full_10k/summaries/exp0021_summary.json
# Destructive: No
# Result: exit code 0; summary reported 10000 attempted, 10000 succeeded, 0 failed, embedding_dim 768, 10 shards.

# CMD-005: Full-run checkpoint inspection
# Purpose: Inspect generated full-run checkpoint JSON.
# Working directory: /root/cexar-workbench
# Command: python3 -c "import json; p='/workspace/exp_artifacts/EXP-0021/runs/full_10k/checkpoints/progress.json'; d=json.load(open(p)); xs=d['completed_indices']; print({'success_count': d.get('success_count'), 'next_shard_id': d.get('next_shard_id'), 'completed_len': len(xs), 'first': xs[:3], 'last': xs[-3:]})"
# Destructive: No
# Result: exit code 0; success_count 10000, next_shard_id 10, completed_len 10000, first [0, 1, 2], last [9997, 9998, 9999].

# CMD-006: Full-run shard inventory
# Purpose: Confirm external .npz shard files are present outside git.
# Working directory: /root/cexar-workbench
# Command: ls -lh /workspace/exp_artifacts/EXP-0021/runs/full_10k/embeddings
# Destructive: No
# Result: exit code 0; ten .npz shard files observed, shard_0000.npz through shard_0009.npz.

# CMD-007: Full-run shard shape inspection
# Purpose: Verify .npz shard embedding row counts and embedding dimension without computing clinical metrics.
# Working directory: /root/cexar-workbench
# Command: /opt/venv/bin/python -c "import numpy as np, glob, os; files=sorted(glob.glob('/workspace/exp_artifacts/EXP-0021/runs/full_10k/embeddings/*.npz')); print('files', len(files)); total=0; bad=[]; key_shapes=[]; \nfor f in files:\n data=np.load(f, allow_pickle=False); emb=data['embeddings']; total+=emb.shape[0]; key_shapes.append((os.path.basename(f), list(data.files), emb.shape));\n if emb.ndim!=2 or emb.shape[1]!=768: bad.append((os.path.basename(f), emb.shape));\nprint('total_embeddings', total); print('bad_shapes', bad); print('first', key_shapes[0]); print('last', key_shapes[-1])"
# Destructive: No
# Result: exit code 0; files 10, total_embeddings 10000, bad_shapes [], first shard shape (1000, 768), last shard shape (1000, 768).

# CMD-008: Summary copy comparison
# Purpose: Confirm git lightweight full-run summary matches external full-run summary.
# Working directory: /root/cexar-workbench
# Command: cmp -s /workspace/exp_artifacts/EXP-0021/runs/full_10k/summaries/exp0021_summary.json experiments/EXP-0021-rad-dino-10k-cloud-embedding-run/artifacts/full_10k/exp0021_summary.json; echo $?
# Destructive: No
# Result: exit code 0; printed 0, indicating byte-identical files.

# CMD-009: Manifest row count check
# Purpose: Confirm generated full-run manifest line count.
# Working directory: /root/cexar-workbench
# Command: wc -l /workspace/exp_artifacts/EXP-0021/runs/full_10k/manifests/candidate_manifest_10k.csv experiments/EXP-0021-rad-dino-10k-cloud-embedding-run/artifacts/full_10k/manifest_head_20.csv
# Destructive: No
# Result: exit code 0; external manifest had 10001 lines including header; lightweight manifest head had 20 lines.
