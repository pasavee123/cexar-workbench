# EXP-0018 command ledger
# Runner must append every exact terminal command before execution.
# Do not summarize multiple commands.

# CMD-001: Preflight check - verify all required prior experiment artifacts exist
# Purpose: Confirm EXP-0016 and EXP-0017 outputs are available before proceeding
# Working directory: D:\cexar-workbench
# Destructive: false
Test-Path "D:\cexar-workbench\experiments\EXP-0016-chexpert-scale-up-readiness\artifacts\candidate_manifest_1k.csv" ; Test-Path "D:\cexar-workbench\experiments\EXP-0017-rad-dino-true-linear-probe-training-v1\artifacts\linear_probe_metrics.json" ; Test-Path "D:\cexar-workbench\experiments\EXP-0017-rad-dino-true-linear-probe-training-v1\artifacts\rad_dino_embedding_summary_1k.json" ; Test-Path "D:\cexar-workbench\experiments\EXP-0017-rad-dino-true-linear-probe-training-v1\artifacts\corrected_split_report.json"
# Result: EXIT CODE 0 - All four paths returned True

# CMD-002: Validate CSV manifest row count and columns
# Purpose: Confirm candidate_manifest_1k.csv has 1000 data rows and required columns
# Working directory: D:\cexar-workbench
# Destructive: false
python -c "import csv; f=open('experiments/EXP-0016-chexpert-scale-up-readiness/artifacts/candidate_manifest_1k.csv','r'); r=csv.reader(f); h=next(r); rows=sum(1 for _ in r); f.close(); print(f'HEADER: {h}'); print(f'ROWS: {rows}')"
# Result: EXIT CODE 1 - Python not found in PATH. Runner cannot modify system PATH.
# Fallback: CSV validated via Read tool - 1001 lines (1 header + 1000 data), all required columns confirmed present.

# CMD-003: Check for secrets/credentials in EXP-0018 package files
# Purpose: Verify no credentials, tokens, private IPs, or SSH keys in any package file
# Working directory: D:\cexar-workbench\experiments\EXP-0018-cloud-readiness-package
# Destructive: false
Select-String -Path "cloud_provisioning_config.yaml","manifest_integrity_audit.json","EXP0019_READINESS.json","cloud_cost_runtime_estimate.json","configs/regularized_probe_config.yaml","configs/seed_plan.yaml","configs/artifact_paths.yaml","src/run_regularized_probe.py","src/split_strategies.py","src/embedding_io.py","src/metrics.py","src/manifest_audit.py","src/cloud_runtime_check.py","scripts/ssh_cloud_smoke_template.sh","scripts/setup_cloud_env.sh","scripts/collect_artifacts.sh" -Pattern "(api_key|token|secret|password|BEGIN RSA|BEGIN OPENSSH|AKIA[0-9A-Z]{16}|ghp_[0-9a-zA-Z]{36}|sk-[0-9a-zA-Z]{32,})" -CaseSensitive:$false 2>&1
# Result: EXIT CODE 0 - No secrets detected. Four matches are policy statements/instructions, not actual credentials.
#   - cloud_provisioning_config.yaml:61 "api_tokens_allowed_in_repo: false" (policy)
#   - EXP0019_READINESS.json:11 "without committing secrets" (instruction)
#   - ssh_cloud_smoke_template.sh:4-5 (template comments about secrets)

# CMD-004: Full file inventory verification
# Purpose: Confirm all required files are present per experiment_protocol.md
# Working directory: D:\cexar-workbench
# Destructive: false
Get-ChildItem -Path "experiments\EXP-0018-cloud-readiness-package" -Recurse | Select-Object FullName -ExpandProperty FullName
# Result: EXIT CODE 0 - 31 files confirmed (11 required protocol files + configs/src/scripts/artifacts + extra files)


