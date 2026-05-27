#!/usr/bin/env bash
set -euo pipefail

# EXP-0022 RAD-DINO Throughput Optimization Benchmark Runner.
#
# Orchestrates runtime checks and the DataLoader benchmark, then packages
# results into a review packet tarball.
#
# Usage:
#   bash experiments/EXP-0022-rad-dino-throughput-optimization/scripts/run_exp0022_benchmark.sh

REPO_ROOT="/root/cexar-workbench"
PYTHON="/opt/venv/bin/python"
EXP_DIR="${REPO_ROOT}/experiments/EXP-0022-rad-dino-throughput-optimization"
SCRIPT_DIR="${EXP_DIR}/scripts"
CONFIG_DIR="${EXP_DIR}/configs"
ARTIFACT_ROOT="/workspace/exp_artifacts/EXP-0022"
REVIEW_PACKET_DIR="${ARTIFACT_ROOT}/review_packet"
BENCHMARK_RUNS_DIR="${ARTIFACT_ROOT}/benchmark_runs"
DATASET_ROOT="/workspace/chexpert_dataset_raw"
EXP0021_MANIFEST="/workspace/exp_artifacts/EXP-0021/runs/full_10k/manifests/candidate_manifest_10k.csv"
REQUIRED_GPU_SUBSTR="RTX 6000 Ada"

echo "=== EXP-0022 RAD-DINO Throughput Optimization Benchmark ==="
echo "Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)"

# ---- Phase 1: Runtime Verification ----
echo ""
echo "=== Phase 1: Runtime Verification ==="

echo "  Hostname: $(hostname)"
echo "  pwd: $(pwd)"
echo "  REPO_ROOT: ${REPO_ROOT}"

if [ ! -d "${REPO_ROOT}" ]; then
    echo "FATAL: Repo root not found: ${REPO_ROOT}"
    exit 1
fi

if [ ! -d "/workspace" ]; then
    echo "FATAL: /workspace not mounted"
    exit 1
fi
echo "  /workspace disk: $(df -h /workspace | tail -1 | awk '{print $4 " available"}')"

if ! command -v nvidia-smi &> /dev/null; then
    echo "FATAL: nvidia-smi not found"
    exit 1
fi

GPU_NAME="$(nvidia-smi --query-gpu=name --format=csv,noheader | head -1)"
echo "  GPU: ${GPU_NAME}"

if ! echo "${GPU_NAME}" | grep -qi "${REQUIRED_GPU_SUBSTR}"; then
    echo "FATAL: Required GPU containing '${REQUIRED_GPU_SUBSTR}' not detected. Found: ${GPU_NAME}"
    exit 1
fi

if ! ${PYTHON} -c "import torch; assert torch.cuda.is_available(), 'CUDA not available'"; then
    echo "FATAL: CUDA not available via ${PYTHON}"
    exit 1
fi

echo "  Python: ${PYTHON}"
echo "  Python version: $(${PYTHON} --version 2>&1)"
echo "  torch version: $(${PYTHON} -c 'import torch; print(torch.__version__)' 2>&1)"
echo "  torch cuda: $(${PYTHON} -c 'import torch; print(torch.version.cuda)' 2>&1)"

if [ ! -d "${DATASET_ROOT}" ]; then
    echo "FATAL: Dataset root not found: ${DATASET_ROOT}"
    exit 1
fi
echo "  Dataset root present: ${DATASET_ROOT}"

if [ ! -f "${EXP0021_MANIFEST}" ]; then
    echo "FATAL: EXP-0021 manifest not found: ${EXP0021_MANIFEST}"
    exit 1
fi
echo "  EXP-0021 manifest present: ${EXP0021_MANIFEST}"

echo "  Runtime verification PASSED."

# ---- Phase 2: Create Output Directories ----
echo ""
echo "=== Phase 2: Create Output Directories ==="

mkdir -p "${BENCHMARK_RUNS_DIR}"
mkdir -p "${REVIEW_PACKET_DIR}"
echo "  Created: ${BENCHMARK_RUNS_DIR}"
echo "  Created: ${REVIEW_PACKET_DIR}"

# ---- Phase 3: Run Benchmark ----
echo ""
echo "=== Phase 3: DataLoader Throughput Benchmark ==="

BENCHMARK_CMD="${PYTHON} ${SCRIPT_DIR}/benchmark_rad_dino_dataloader.py \
    --manifest ${EXP0021_MANIFEST} \
    --results-dir ${BENCHMARK_RUNS_DIR} \
    --sample-size 2000 \
    --seed 20260527 \
    --device cuda \
    --batch-sizes 1 8 16 32 64 \
    --num-workers 0 2 4 8"

echo "  Command: ${BENCHMARK_CMD}"
${PYTHON} "${SCRIPT_DIR}/benchmark_rad_dino_dataloader.py" \
    --manifest "${EXP0021_MANIFEST}" \
    --results-dir "${BENCHMARK_RUNS_DIR}" \
    --sample-size 2000 \
    --seed 20260527 \
    --device cuda \
    --batch-sizes 1 8 16 32 64 \
    --num-workers 0 2 4 8

echo "  Benchmark PASSED."

# ---- Phase 4: Generate Review Packet ----
echo ""
echo "=== Phase 4: Generate Review Packet ==="

PACKET_CMD="${PYTHON} ${SCRIPT_DIR}/generate_review_packet.py \
    --results-dir ${BENCHMARK_RUNS_DIR} \
    --packet-dir ${REVIEW_PACKET_DIR}"

echo "  Command: ${PACKET_CMD}"
${PYTHON} "${SCRIPT_DIR}/generate_review_packet.py" \
    --results-dir "${BENCHMARK_RUNS_DIR}" \
    --packet-dir "${REVIEW_PACKET_DIR}"

PACKET_FILE="${REVIEW_PACKET_DIR}/exp0022_review_packet.tar.gz"
if [ -f "${PACKET_FILE}" ]; then
    echo "  Review packet created: ${PACKET_FILE}"
    PACKET_SIZE="$(du -h "${PACKET_FILE}" | cut -f1)"
    echo "  Packet size: ${PACKET_SIZE}"
else
    echo "  WARNING: Review packet not found at ${PACKET_FILE}"
fi

# ---- Done ----
echo ""
echo "=== EXP-0022 Complete ==="
echo "Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "Review packet: ${PACKET_FILE}"
