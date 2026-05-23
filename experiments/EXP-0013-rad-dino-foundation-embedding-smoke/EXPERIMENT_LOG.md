# EXPERIMENT_LOG.md

## Status

COMPLETE — PASS

## CMD-001 — Create artifacts directory
- **Timestamp**: 2026-05-23T20:54:00+07:00
- **Working directory**: D:\cexar-workbench
- **Command**: `mkdir "D:\cexar-workbench\experiments\EXP-0013-rad-dino-foundation-embedding-smoke\artifacts"`
- **Exit code**: 0
- **Summary**: Created artifacts/ directory successfully.
- **Files changed**: `experiments/EXP-0013-rad-dino-foundation-embedding-smoke/artifacts/` (new directory)

## CMD-002 — Check Python availability
- **Timestamp**: 2026-05-23T20:54:30+07:00
- **Working directory**: D:\cexar-workbench
- **Command**: `where python`
- **Exit code**: 0 (but no output)
- **Summary**: `python` not found on PATH.
- **Files changed**: None

## CMD-003 — List Python via launcher
- **Timestamp**: 2026-05-23T20:55:00+07:00
- **Working directory**: D:\cexar-workbench
- **Command**: `py --list`
- **Exit code**: 0
- **Summary**: Found `-3.10-64 *` via `C:\WINDOWS\py.exe` launcher.
- **Files changed**: None

## CMD-004 — Check Python launcher paths
- **Timestamp**: 2026-05-23T20:55:10+07:00
- **Working directory**: D:\cexar-workbench
- **Command**: `py -0p`
- **Exit code**: 0
- **Summary**: Python 3.10-64 at `C:\Users\pasav\AppData\Local\Programs\Python\Python310\python.exe`
- **Files changed**: None

## CMD-005 — Check Python version
- **Timestamp**: 2026-05-23T20:55:30+07:00
- **Working directory**: D:\cexar-workbench
- **Command**: `py -3.10 -c "import sys; print(sys.version)"`
- **Exit code**: 0
- **Summary**: Python 3.10.2
- **Files changed**: None

## CMD-006 — Create .venvs\cexar-foundation
- **Timestamp**: 2026-05-23T20:55:40+07:00
- **Working directory**: D:\cexar-workbench
- **Command**: `py -3.10 -m venv .venvs\cexar-foundation`
- **Exit code**: 0
- **Summary**: Created `.venvs\cexar-foundation`.
- **Files changed**: `.venvs\cexar-foundation/` (new)

## CMD-007 — Verify venv Python
- **Timestamp**: 2026-05-23T20:56:00+07:00
- **Working directory**: D:\cexar-workbench
- **Command**: `.venvs\cexar-foundation\Scripts\python.exe -c "import sys; print(sys.executable); print(sys.version)"`
- **Exit code**: 0
- **Summary**: Confirmed venv Python 3.10.2.
- **Files changed**: None

## CMD-008 — Upgrade pip inside venv
- **Timestamp**: 2026-05-23T20:56:10+07:00
- **Working directory**: D:\cexar-workbench
- **Command**: `.venvs\cexar-foundation\Scripts\python.exe -m pip install --upgrade pip`
- **Exit code**: 0
- **Summary**: pip 21.2.4 → 26.1.1
- **Files changed**: venv packages

## CMD-009 — Install RAD-DINO requirements
- **Timestamp**: 2026-05-23T20:56:20+07:00
- **Working directory**: D:\cexar-workbench
- **Command**: `.venvs\cexar-foundation\Scripts\python.exe -m pip install -r "experiments\EXP-0013-rad-dino-foundation-embedding-smoke\configs\REQUIREMENTS_RAD_DINO.txt"`
- **Exit code**: 0
- **Summary**: Installed torch 2.5.1, torchvision 0.20.1, transformers 4.45.2, huggingface_hub 0.36.2, numpy 1.26.4, Pillow 12.2.0, psutil 7.2.2, etc.
- **Files changed**: venv packages

## CMD-010 — pip freeze artifact
- **Timestamp**: 2026-05-23T20:57:30+07:00
- **Working directory**: D:\cexar-workbench
- **Command**: `.venvs\cexar-foundation\Scripts\python.exe -m pip freeze > "experiments\EXP-0013-rad-dino-foundation-embedding-smoke\artifacts\pip_freeze_cexar_foundation.txt"`
- **Exit code**: 0
- **Summary**: Wrote pip freeze to artifacts.
- **Files changed**: `artifacts/pip_freeze_cexar_foundation.txt`

## CMD-011 — Check HF cache for microsoft/rad-dino
- **Timestamp**: 2026-05-23T20:57:40+07:00
- **Working directory**: D:\cexar-workbench
- **Command**: `.venvs\cexar-foundation\Scripts\python.exe "experiments\EXP-0013-rad-dino-foundation-embedding-smoke\_check_cache.py"`
- **Exit code**: 0
- **Summary**: RAD-DINO NOT cached locally. Triggered stop per TEST_PLAN.md Phase 2.
- **Files changed**: None

## CMD-012 — Download microsoft/rad-dino weights (human approved)
- **Timestamp**: 2026-05-23T20:58:20+07:00
- **Working directory**: D:\cexar-workbench
- **Command**: `.venvs\cexar-foundation\Scripts\python.exe -c "from huggingface_hub import snapshot_download; snapshot_download('microsoft/rad-dino')"`
- **Exit code**: 0
- **Summary**: Downloaded 16 files (~2 min). Weights cached locally.
- **Files changed**: `~/.cache/huggingface/hub/models--microsoft--rad-dino/` (new cache dir)

## CMD-013 — Verify 100 image paths
- **Timestamp**: 2026-05-23T20:59:00+07:00
- **Working directory**: D:\cexar-workbench
- **Command**: `.venvs\cexar-foundation\Scripts\python.exe "experiments\EXP-0013-rad-dino-foundation-embedding-smoke\_verify_images.py"`
- **Exit code**: 0
- **Summary**: 100/100 images found on disk, 0 missing.
- **Files changed**: None

## CMD-014 — Run RAD-DINO embedding smoke test
- **Timestamp**: 2026-05-23T21:35:00+07:00
- **Working directory**: D:\cexar-workbench
- **Command**: `.venvs\cexar-foundation\Scripts\python.exe "experiments\EXP-0013-rad-dino-foundation-embedding-smoke\artifacts\run_rad_dino_embedding_smoke.py"`
- **Exit code**: 0
- **Summary**: 100/100 images processed successfully. Embedding shape [100, 768], hidden size 768. Runtime 90.35s on CPU. CUDA not available. AMP autocast wrapped with CPU fallback support. 0 failures.
- **Files changed**: `artifacts/rad_dino_embedding_summary.json`, `artifacts/rad_dino_embeddings.npz` (initially written to wrong path, then moved)

## CMD-015 — Move output files to correct location
- **Timestamp**: 2026-05-23T21:39:00+07:00
- **Working directory**: D:\cexar-workbench
- **Command**: Copy-Item + Remove-Item to relocate artifacts from `artifacts/EXP-0013*/` to `experiments/EXP-0013*/artifacts/`
- **Exit code**: 0
- **Summary**: Moved `rad_dino_embedding_summary.json` and `rad_dino_embeddings.npz` to correct experiment artifacts directory. Removed external artifacts dir.
- **Files changed**: artifacts relocated; external `artifacts/EXP-0013*/` removed

## CMD-016 — Fix output paths in script
- **Timestamp**: 2026-05-23T21:40:00+07:00
- **Working directory**: D:\cexar-workbench
- **Command**: Edit `run_rad_dino_embedding_smoke.py` to correct OUTPUT_SUMMARY and OUTPUT_EMBEDDINGS paths.
- **Exit code**: N/A (file edit)
- **Summary**: Corrected paths from `artifacts/EXP-0013*/` to `experiments/EXP-0013*/artifacts/`.
- **Files changed**: `artifacts/run_rad_dino_embedding_smoke.py`

## CMD-017 — Clean up temp helper scripts
- **Timestamp**: 2026-05-23T21:40:30+07:00
- **Working directory**: D:\cexar-workbench
- **Command**: Remove-Item for `_check_cache.py` and `_verify_images.py`
- **Exit code**: 0
- **Summary**: Removed temporary helper scripts.
- **Files changed**: `_check_cache.py` (deleted), `_verify_images.py` (deleted)

## Safety Compliance Summary

- Global Python: NOT touched
- Global pip install/uninstall/--force-reinstall: NOT executed
- `.venvs\cexar-baseline`: NOT modified
- Existing venvs: NOT deleted or recreated
- Production code, manifests, standards, repo_hunt: NOT modified
- EXP-0012B artifacts: NOT modified
- `D:\Dataset_Chexpert`: treated as read-only (only reads)
- All commands registered in `commands.ps1` before execution
- All commands logged in EXPERIMENT_LOG.md