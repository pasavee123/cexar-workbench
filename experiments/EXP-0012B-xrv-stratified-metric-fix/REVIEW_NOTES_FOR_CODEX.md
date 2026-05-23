# REVIEW_NOTES_FOR_CODEX.md — EXP-0012B

## What Was Done

Ran TorchXRayVision DenseNet121 inference on a deterministic random sample (seed 42) of 100 frontal CheXpert validation images and computed label-level AUROC for 11 cross-walked pathology labels.

## Fixes Applied

### Fix 1: Silent Failure Guard

In EXP-0012, if all 100 images failed inference (path resolution bug), the script still exited with code 0 and wrote "PASS." This is unsafe — a run with zero successful inferences must never be reported as success.

Fix: After the inference loop, if `num_images_succeeded == 0`, the script writes a failure entry to `metric_sanity.json`, prints a clear error message, and exits with code 1.

### Fix 2: Deterministic Random Sampling

In EXP-0012, the sample was "first 100 frontal images sorted by Path." This produces a sample biased toward the lexicographically earliest file paths, which may not represent the validation distribution well.

Fix: Replaced with `random.Random(42).sample(frontal, 100)`. The seed 42 ensures reproducibility. The exact sample is saved to `sample_manifest.csv`.

### Why Not Stratified Sampling

Stratified sampling on multi-label CheXpert data requires iterative stratification (handling 11+ label columns simultaneously where each image can have multiple positive labels). This requires algorithms like scikit-multilearn's iterative_train_test_split, which is not available in the venv. Implementing a custom iterative stratification would be complex and error-prone. The task instructions state: "If stratified sampling becomes complex or unsafe, use deterministic random sampling and explain why." Deterministic random sampling with a fixed seed is simple, reliable, and reproducible.

## Items for Codex to Consider

- Does this sample produce comparable per-label prevalence to EXP-0012's first-100 sample?
- Should future experiments implement iterative multi-label stratified sampling as a separate fix?
- Should the silent failure guard be backported to other experiment scripts?