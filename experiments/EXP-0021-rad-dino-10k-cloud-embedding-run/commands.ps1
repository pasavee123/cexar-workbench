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
# The commands below are PROPOSED for Phase B/C execution on RunPod - they have NOT been run yet.

# ---- PROPOSED Phase C dry-run commands (NOT YET EXECUTED) ----
# CMD-001: Dry-run 5 images
# Purpose: Verify full pipeline on 5 images
# Working directory: /root/cexar-workbench
# Command: bash experiments/EXP-0021-rad-dino-10k-cloud-embedding-run/scripts/run_exp0021_10k.sh --limit 5 --dry-run-label dryrun5
# Destructive: No

# CMD-002: Dry-run 100 images
# Purpose: Verify full pipeline on 100 images
# Working directory: /root/cexar-workbench
# Command: bash experiments/EXP-0021-rad-dino-10k-cloud-embedding-run/scripts/run_exp0021_10k.sh --limit 100 --dry-run-label dryrun100
# Destructive: No

# ---- PROPOSED Phase D full run command (NOT YET EXECUTED) ----
# CMD-003: Full 10k run
# Purpose: Run 10,000-image RAD-DINO embedding extraction
# Working directory: /root/cexar-workbench
# Command: bash experiments/EXP-0021-rad-dino-10k-cloud-embedding-run/scripts/run_exp0021_10k.sh --limit 10000
# Destructive: No
