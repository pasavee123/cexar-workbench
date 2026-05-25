#!/usr/bin/env bash
set -euo pipefail

mkdir -p /workspace \
         /workspace/.cache/huggingface \
         /workspace/.cache/huggingface/transformers \
         /workspace/.cache/torch

mkdir -p /root/.ssh
chmod 700 /root/.ssh

if [ -n "${PUBLIC_KEY:-}" ]; then
  echo "${PUBLIC_KEY}" >> /root/.ssh/authorized_keys
  chmod 600 /root/.ssh/authorized_keys
fi

ssh-keygen -A
service ssh start

echo "CeXaR interactive A40 environment is ready."
echo "No experiment is auto-started by this container."

sleep infinity
