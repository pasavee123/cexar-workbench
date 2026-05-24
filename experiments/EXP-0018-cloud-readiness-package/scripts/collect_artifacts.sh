#!/usr/bin/env bash
set -euo pipefail

# Template only. Do not embed credentials or private paths.

ARTIFACT_ROOT="/workspace/cexar-workbench/experiments/EXP-0019-cloud-smoke-run/artifacts"
echo "Collect artifacts from: ${ARTIFACT_ROOT}"
# TODO: tar or rsync approved artifacts only.

