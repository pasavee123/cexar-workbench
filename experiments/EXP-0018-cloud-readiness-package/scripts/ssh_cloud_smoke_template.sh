#!/usr/bin/env bash
set -euo pipefail

# Template only. Do not commit hostnames, SSH keys, tokens, or secrets.
# Replace placeholders outside the repository or through a secure secret manager.

REMOTE_HOST="<A40_CLOUD_HOST>"
REMOTE_USER="<REMOTE_USER>"
REMOTE_PROJECT_ROOT="/workspace/cexar-workbench"

echo "Template only. Review before use."
echo "ssh ${REMOTE_USER}@${REMOTE_HOST}"
echo "cd ${REMOTE_PROJECT_ROOT}"
echo "bash experiments/EXP-0019-cloud-smoke-run/scripts/setup_cloud_env.sh"

