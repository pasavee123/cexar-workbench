#!/usr/bin/env bash
set -euo pipefail

# EXP-0021 one-shot runner.
# Orchestrates runtime checks, manifest building, and RAD-DINO embedding extraction.
#
# Usage:
#   bash run_exp0021_10k.sh [--limit N] [--dry-run-label LABEL]
#
# Examples:
#   bash run_exp0021_10k.sh --limit 5 --dry-run-label dryrun5
#   bash run_exp0021_10k.sh --limit 100 --dry-run-label dryrun100
#   bash run_exp0021_10k.sh --limit 10000

REPO_ROOT="/root/cexar-workbench"
PYTHON="/opt/venv/bin/python"
SCRIPT_DIR="${REPO_ROOT}/experiments/EXP-0021-rad-dino-10k-cloud-embedding-run/scripts"
EXP_DIR="${REPO_ROOT}/experiments/EXP-0021-rad-dino-10k-cloud-embedding-run"
ARTIFACT_ROOT="/workspace/exp_artifacts/EXP-0021"
DATASET_ROOT="/workspace/chexpert_dataset_raw"
REQUIRED_GPU="NVIDIA RTX 6000 Ada Generation"

LIMIT=""
DRY_RUN_LABEL=""
RUN_LABEL="full_10k"

usage() {
    echo "Usage: $0 [--limit N] [--dry-run-label LABEL]"
    echo ""
    echo "  --limit N            Process at most N images (dry-run mode)"
    echo "  --dry-run-label LABEL  Label for dry-run output subdirectory"
    exit 1
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --limit)
            LIMIT="$2"
            shift 2
            ;;
        --dry-run-label)
            DRY_RUN_LABEL="$2"
            shift 2
            ;;
        -h|--help)
            usage
            ;;
        *)
            echo "Unknown option: $1"
            usage
            ;;
    esac
done

if [ -n "${DRY_RUN_LABEL}" ]; then
    RUN_LABEL="${DRY_RUN_LABEL}"
elif [ -n "${LIMIT}" ] && [ "${LIMIT}" != "10000" ]; then
    RUN_LABEL="limit_${LIMIT}"
fi

RUN_ARTIFACT_ROOT="${ARTIFACT_ROOT}/runs/${RUN_LABEL}"
MANIFEST_PATH="${RUN_ARTIFACT_ROOT}/manifests/candidate_manifest_10k.csv"

echo "=== EXP-0021 RAD-DINO 10k Cloud Embedding Run ==="
echo "Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)"

# ---- Phase 1: Runtime Verification ----
echo ""
echo "=== Phase 1: Runtime Verification ==="

echo "  Hostname: $(hostname)"
echo "  pwd: $(pwd)"

if ! command -v nvidia-smi &> /dev/null; then
    echo "FATAL: nvidia-smi not found"
    exit 1
fi

GPU_NAME="$(nvidia-smi --query-gpu=name --format=csv,noheader | head -1)"
echo "  GPU: ${GPU_NAME}"

if ! echo "${GPU_NAME}" | grep -qi "RTX 6000 Ada"; then
    echo "FATAL: Required GPU '${REQUIRED_GPU}' not detected. Found: ${GPU_NAME}"
    exit 1
fi

if ! ${PYTHON} -c "import torch; assert torch.cuda.is_available(), 'CUDA not available'"; then
    echo "FATAL: CUDA not available via ${PYTHON}"
    exit 1
fi

echo "  Python path: ${PYTHON}"
echo "  Python version: $(${PYTHON} --version 2>&1)"
echo "  torch version: $(${PYTHON} -c 'import torch; print(torch.__version__)' 2>&1)"
echo "  torch cuda: $(${PYTHON} -c 'import torch; print(torch.version.cuda)' 2>&1)"

if [ ! -d "${DATASET_ROOT}" ]; then
    echo "FATAL: Dataset root not found: ${DATASET_ROOT}"
    exit 1
fi
echo "  Dataset root present: ${DATASET_ROOT}"

if [ ! -d "/workspace" ]; then
    echo "FATAL: /workspace not mounted"
    exit 1
fi
echo "  /workspace disk: $(df -h /workspace | tail -1 | awk '{print $4 " available"}')"

if [ -d "${RUN_ARTIFACT_ROOT}" ]; then
    echo "  Run artifact root present: ${RUN_ARTIFACT_ROOT}"
else
    echo "  Run artifact root will be created: ${RUN_ARTIFACT_ROOT}"
fi

echo "  Runtime verification PASSED."

# ---- Phase 2: Manifest Building ----
echo ""
echo "=== Phase 2: Manifest Building ==="

MANIFEST_LIMIT_ARG=""
if [ -n "${LIMIT}" ]; then
    MANIFEST_LIMIT_ARG="--limit ${LIMIT}"
fi

echo "  Running: ${PYTHON} ${SCRIPT_DIR}/build_manifest_10k.py --dataset-root ${DATASET_ROOT} --output-csv ${MANIFEST_PATH} --seed 20260527 ${MANIFEST_LIMIT_ARG}"
${PYTHON} "${SCRIPT_DIR}/build_manifest_10k.py" \
    --dataset-root "${DATASET_ROOT}" \
    --output-csv "${MANIFEST_PATH}" \
    --seed 20260527 \
    ${MANIFEST_LIMIT_ARG}
echo "  Manifest building PASSED."

# ---- Phase 3: RAD-DINO Embedding Extraction ----
echo ""
echo "=== Phase 3: RAD-DINO Embedding Extraction ==="

EMBED_LIMIT_ARG=""
if [ -n "${LIMIT}" ]; then
    EMBED_LIMIT_ARG="--limit ${LIMIT}"
fi

echo "  Running: ${PYTHON} ${SCRIPT_DIR}/run_rad_dino_embedding_10k.py --manifest ${MANIFEST_PATH} --output-dir ${RUN_ARTIFACT_ROOT}/embeddings --checkpoint-dir ${RUN_ARTIFACT_ROOT}/checkpoints --summary-dir ${RUN_ARTIFACT_ROOT}/summaries --device cuda --shard-size 1000 ${EMBED_LIMIT_ARG}"
${PYTHON} "${SCRIPT_DIR}/run_rad_dino_embedding_10k.py" \
    --manifest "${MANIFEST_PATH}" \
    --output-dir "${RUN_ARTIFACT_ROOT}/embeddings" \
    --checkpoint-dir "${RUN_ARTIFACT_ROOT}/checkpoints" \
    --summary-dir "${RUN_ARTIFACT_ROOT}/summaries" \
    --device cuda \
    --shard-size 1000 \
    ${EMBED_LIMIT_ARG}
echo "  Embedding extraction PASSED."

# ---- Phase 4: Copy Lightweight Summary ----
echo ""
echo "=== Phase 4: Copy Summary Artifacts ==="

SUMMARY_DST="${EXP_DIR}/artifacts/${RUN_LABEL}"
mkdir -p "${SUMMARY_DST}"

if [ -f "${RUN_ARTIFACT_ROOT}/summaries/exp0021_summary.json" ]; then
    cp "${RUN_ARTIFACT_ROOT}/summaries/exp0021_summary.json" "${SUMMARY_DST}/exp0021_summary.json"
    echo "  Copied summary to ${SUMMARY_DST}/exp0021_summary.json"
else
    echo "  WARNING: Summary not found at ${RUN_ARTIFACT_ROOT}/summaries/exp0021_summary.json"
fi

if [ -f "${MANIFEST_PATH}" ]; then
    head -20 "${MANIFEST_PATH}" > "${SUMMARY_DST}/manifest_head_20.csv"
    echo "  Copied manifest head to ${SUMMARY_DST}/manifest_head_20.csv"
fi

echo ""
echo "=== EXP-0021 Complete ==="
echo "Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
