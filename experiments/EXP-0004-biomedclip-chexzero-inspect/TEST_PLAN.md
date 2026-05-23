# EXP-0004 TEST_PLAN

## Pass/Fail Criteria

### Pass
1. BiomedCLIP model card/config is inspectable
2. CheXzero repo inspection reveals preprocessing/label scheme
3. At least one candidate can describe its expected output format
4. License terms documented for both

### Fail
1. Both checkpoints are inaccessible
2. Prompt/evaluation assumptions are too unclear
3. Both require large downloads without approval

## Test Cases

### TC-1: BiomedCLIP Model Card
- Fetch HF model config
- Record architecture, input size, embedding dim, license

### TC-2: BiomedCLIP open_clip Smoke Test
- Install open_clip if not present
- Try loading model via open_clip.create_model_and_transforms
- If weights are small, run synthetic tensor forward pass

### TC-3: CheXzero Repo Inspection
- Inspect GitHub repo for README, requirements, eval.py
- Record expected input, preprocessing, label format
- Identify whether zero-shot can run without dataset

### TC-4: Comparison
- Compare prompt format, output type, maintenance signal
- Recommend benchmark usage