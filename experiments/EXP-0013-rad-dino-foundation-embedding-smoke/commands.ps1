# EXP-0013 command ledger
#
# Not run yet. The runner must append exact commands here before executing them.
# --- Phase 0: Safety & Setup ---
# CMD-001: Create artifacts directory
mkdir "D:\cexar-workbench\experiments\EXP-0013-rad-dino-foundation-embedding-smoke\artifacts"

# CMD-002: Check Python availability on PATH
where python

# CMD-003: Check Python launcher
py --list

# CMD-004: Check Python launcher paths
py -0p

# CMD-005: Check Python version
py -3.10 -c "import sys; print(sys.version)"

# CMD-006: Create .venvs\cexar-foundation
py -3.10 -m venv .venvs\cexar-foundation

# CMD-007: Verify venv exists and check python inside it
.venvs\cexar-foundation\Scripts\python.exe -c "import sys; print(sys.executable); print(sys.version)"

# CMD-008: Upgrade pip inside venv
.venvs\cexar-foundation\Scripts\python.exe -m pip install --upgrade pip

# CMD-009: Install RAD-DINO requirements inside venv
.venvs\cexar-foundation\Scripts\python.exe -m pip install -r "experiments\EXP-0013-rad-dino-foundation-embedding-smoke\configs\REQUIREMENTS_RAD_DINO.txt"

# CMD-010: pip freeze for artifact record
.venvs\cexar-foundation\Scripts\python.exe -m pip freeze > "experiments\EXP-0013-rad-dino-foundation-embedding-smoke\artifacts\pip_freeze_cexar_foundation.txt"

# CMD-011: Check HF cache for microsoft/rad-dino (via script)
.venvs\cexar-foundation\Scripts\python.exe "experiments\EXP-0013-rad-dino-foundation-embedding-smoke\_check_cache.py"

# CMD-012: Download microsoft/rad-dino weights (human approved)
.venvs\cexar-foundation\Scripts\python.exe -c "from huggingface_hub import snapshot_download; snapshot_download('microsoft/rad-dino')"

# CMD-013: Verify 100 image paths from sample manifest
.venvs\cexar-foundation\Scripts\python.exe "experiments\EXP-0013-rad-dino-foundation-embedding-smoke\_verify_images.py"

# CMD-014: Run RAD-DINO embedding smoke test
.venvs\cexar-foundation\Scripts\python.exe "experiments\EXP-0013-rad-dino-foundation-embedding-smoke\artifacts\run_rad_dino_embedding_smoke.py"

# CMD-015: Copy output files to correct experiment artifacts directory
Copy-Item -Path "D:\cexar-workbench\artifacts\EXP-0013-rad-dino-foundation-embedding-smoke\artifacts\rad_dino_embedding_summary.json" -Destination "D:\cexar-workbench\experiments\EXP-0013-rad-dino-foundation-embedding-smoke\artifacts\rad_dino_embedding_summary.json"
Copy-Item -Path "D:\cexar-workbench\artifacts\EXP-0013-rad-dino-foundation-embedding-smoke\artifacts\rad_dino_embeddings.npz" -Destination "D:\cexar-workbench\experiments\EXP-0013-rad-dino-foundation-embedding-smoke\artifacts\rad_dino_embeddings.npz"
Remove-Item -Path "D:\cexar-workbench\artifacts\EXP-0013-rad-dino-foundation-embedding-smoke" -Recurse -Force

