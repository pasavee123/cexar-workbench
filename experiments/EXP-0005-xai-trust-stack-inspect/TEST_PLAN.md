# EXP-0005 TEST_PLAN

## Pass/Fail Criteria

### Pass
1. grad-cam generates heatmap from synthetic model
2. Captum generates attribution from synthetic model
3. Each tool's output shape is documented
4. License and maintenance status recorded

### Fail
1. Both grad-cam and captum fail to install/import
2. Neither can produce attribution from a synthetic model
3. Quantitative evaluation path cannot be defined

## Test Cases

### TC-1: grad-cam smoke test
- Load a pretrained ResNet18 from torchvision
- Generate Grad-CAM heatmap on synthetic image
- Record heatmap shape and values

### TC-2: Captum smoke test
- Generate Integrated Gradients on same model
- Record attribution shape and values

### TC-3: Quantus availability check
- Check if quantus can be installed without dependency conflicts
- Record what metrics are available

### TC-4: CheXlocalize availability
- Inspect repo for evaluation API
- Record required data format