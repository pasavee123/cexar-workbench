#!/usr/bin/env bash
set -euo pipefail

echo "== pwd =="
pwd

echo "== hostname =="
hostname

echo "== nvidia-smi =="
nvidia-smi

echo "== python =="
python --version

echo "== nvcc =="
nvcc --version

echo "== EXP-0019 verifier =="
python /opt/cexar/verify_environment.py

echo "== workspace disk =="
df -h /workspace

echo "== dataset mount disk =="
df -h /mnt/chexpert

