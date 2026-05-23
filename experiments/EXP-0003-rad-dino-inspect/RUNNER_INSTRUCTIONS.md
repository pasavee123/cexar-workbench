# EXP-0003 RUNNER_INSTRUCTIONS

1. Install huggingface_hub and transformers if not present
2. Inspect RAD-DINO model card manually (HF URL)
3. Load model using `transformers.AutoModel.from_pretrained("microsoft/rad-dino")`
4. Create a synthetic tensor (shape [1, 3, 518, 518]) and run forward pass
5. Record embedding shape and model config
6. Log all results to EXPERIMENT_LOG.md
7. Write RESULT.md with verdict
8. If blocked, write FAILURE_REPORT.md

## Safety
- Do NOT download large datasets
- Do NOT modify production code
- Stop if weights exceed 2GB or require gated approval