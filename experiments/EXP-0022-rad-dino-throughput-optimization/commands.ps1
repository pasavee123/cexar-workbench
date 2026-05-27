# commands.ps1

# Runner command ledger for EXP-0022.
# Every terminal command must be appended here before execution.
# Record exact command text, purpose, expected output, and result.

# =============================================================================
# IMPLEMENTATION PHASE (local, before cloud deployment)
# =============================================================================

# CMD-001: Create benchmark script
# Purpose: Implement the main DataLoader throughput benchmark runner
# Working directory: D:\cexar-workbench
# Exact command: Wrote file via editor at experiments/EXP-0022-rad-dino-throughput-optimization/scripts/benchmark_rad_dino_dataloader.py
# Destructive: No
# Result: File created (264 lines)

# CMD-002: Create orchestrator script
# Purpose: Implement the experiment orchestrator shell script
# Working directory: D:\cexar-workbench
# Exact command: Wrote file via editor at experiments/EXP-0022-rad-dino-throughput-optimization/scripts/run_exp0022_benchmark.sh
# Destructive: No
# Result: File created (128 lines)

# CMD-003: Create review packet generator
# Purpose: Implement the review packet tarball generator
# Working directory: D:\cexar-workbench
# Exact command: Wrote file via editor at experiments/EXP-0022-rad-dino-throughput-optimization/scripts/generate_review_packet.py
# Destructive: No
# Result: File created (254 lines)

# =============================================================================
# CLOUD EXECUTION PHASE (to be run on the Pod)
# =============================================================================

# CMD-004: Run full EXP-0022 benchmark
# Purpose: Orchestrate runtime verification, benchmark, and review packet generation
# Working directory: /root/cexar-workbench
# Exact command:
#   bash experiments/EXP-0022-rad-dino-throughput-optimization/scripts/run_exp0022_benchmark.sh
# Destructive: No (writes artifacts under /workspace/exp_artifacts/EXP-0022/)
# Result: PENDING - not yet executed

# CMD-005: Benchmark runner (invoked by CMD-004)
# Purpose: Run batched DataLoader benchmark across batch_size x num_workers grid
# Working directory: /root/cexar-workbench
# Exact command:
#   /opt/venv/bin/python experiments/EXP-0022-rad-dino-throughput-optimization/scripts/benchmark_rad_dino_dataloader.py \
#       --manifest /workspace/exp_artifacts/EXP-0021/runs/full_10k/manifests/candidate_manifest_10k.csv \
#       --results-dir /workspace/exp_artifacts/EXP-0022/benchmark_runs \
#       --sample-size 2000 \
#       --seed 20260527 \
#       --device cuda \
#       --batch-sizes 1 8 16 32 64 \
#       --num-workers 0 2 4 8
# Destructive: No
# Result: PENDING - not yet executed

# CMD-006: Generate review packet (invoked by CMD-004)
# Purpose: Package lightweight benchmark evidence into tarball
# Working directory: /root/cexar-workbench
# Exact command:
#   /opt/venv/bin/python experiments/EXP-0022-rad-dino-throughput-optimization/scripts/generate_review_packet.py \
#       --results-dir /workspace/exp_artifacts/EXP-0022/benchmark_runs \
#       --packet-dir /workspace/exp_artifacts/EXP-0022/review_packet
# Destructive: No
# Result: PENDING - not yet executed

# CMD-007: Verify output directories exist on cloud Pod
# Purpose: Environment check before benchmark execution
# Working directory: /root/cexar-workbench
# Exact command:
#   test -d /workspace/chexpert_dataset_raw && echo "OK" || echo "MISSING"
#   test -f /workspace/exp_artifacts/EXP-0021/runs/full_10k/manifests/candidate_manifest_10k.csv && echo "OK" || echo "MISSING"
#   nvidia-smi --query-gpu=name --format=csv,noheader | head -1
#   /opt/venv/bin/python -c "import torch; print(torch.__version__)"
# Destructive: No
# Result: PENDING - not yet executed
