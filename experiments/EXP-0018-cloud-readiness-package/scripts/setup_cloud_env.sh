#!/usr/bin/env bash
set -euo pipefail

# Template only. Intended for EXP-0019 after cloud host approval.

python --version
nvidia-smi

# TODO: create venv/conda env
# TODO: install approved requirements
# TODO: verify torch CUDA build
# TODO: verify HuggingFace cache path

