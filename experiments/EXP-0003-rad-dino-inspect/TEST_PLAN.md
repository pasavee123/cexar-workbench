# EXP-0003 TEST_PLAN

## Pass/Fail Criteria

### Pass
1. Model card accessible and provides clear preprocessing specs
2. HuggingFace model loads via transformers API
3. Embedding shape determined (expected 768 for ViT-B/14)
4. Expected input size confirmed (518x518)
5. License terms are acceptable for research use

### Fail
1. Model weights require gated/credentialed access that fails
2. Weights too large for session (< 2GB limit)
3. Preprocessing or output shape cannot be established
4. License prohibits research use

## Test Cases

### TC-1: Model Card & License Inspection
- Fetch RAD-DINO model card from HF
- Record license, terms, preprocessing, expected input

### TC-2: Model Loading
- Install transformers + huggingface_hub if needed
- Load RAD-DINO model from HF
- Log model architecture and parameter count

### TC-3: Embedding Shape Test
- Create synthetic tensor of expected input size (518x518, 3-channel)
- Run forward pass without head
- Verify embedding dimensionality

### TC-4: Preprocessing Audit
- Compare with manifest 03 table
- Document any discrepancies