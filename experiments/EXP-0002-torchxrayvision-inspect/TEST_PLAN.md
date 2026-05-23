# EXP-0002 TEST_PLAN

## Pass/Fail Criteria

### Pass
1. Package installs without error
2. Model loads from pretrained weights successfully
3. Synthetic tensor forward pass produces valid output logits
4. Label order can be documented
5. Preprocessing normalization range ([-1024, 1024]) is confirmed

### Fail
1. Dependency install conflicts twice
2. Requires large dataset downloads for basic smoke test
3. Label mapping or preprocessing cannot be identified
4. Model forward pass on synthetic tensor fails

## Test Cases

### TC-1: Package Installation
- Install torchxrayvision via pip
- Log any dependency conflicts

### TC-2: Model Loading
- Load DenseNet121 (all pretrained) from xrv.models
- Log model architecture and parameter count

### TC-3: Synthetic Tensor Forward Pass
- Create random synthetic tensor of shape (1, 1, 224, 224)
- Run model inference
- Verify output shape matches expected number of classes

### TC-4: Label Order Audit
- Inspect model output label order
- Compare against CeXaR manifest expected labels

### TC-5: Preprocessing Analysis
- Confirm normalization range
- Confirm expected input size