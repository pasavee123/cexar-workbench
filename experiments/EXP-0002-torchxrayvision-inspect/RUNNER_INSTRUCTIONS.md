# EXP-0002 RUNNER_INSTRUCTIONS

1. Install torchxrayvision with `pip install torchxrayvision`
2. Run `python -c "import torchxrayvision as xrv; print(xrv.__version__)"` to verify install
3. Load a pretrained DenseNet121 model with `xrv.models.get_model("densenet121-res224-all")`
4. Create a synthetic tensor (random noise, shape [1,1,224,224]) and run forward pass
5. Inspect model output labels using `model.pathologies` attribute
6. Log all results to EXPERIMENT_LOG.md
7. Write RESULT.md with verdict
8. If blocked, write FAILURE_REPORT.md

## Safety
- Do NOT download any medical datasets
- Do NOT modify production code
- Do NOT install unapproved dependencies