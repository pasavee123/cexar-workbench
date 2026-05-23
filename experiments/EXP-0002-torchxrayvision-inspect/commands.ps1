# Install
pip install torchxrayvision

# Verify import
python -c "import torchxrayvision as xrv; print('XRV version:', xrv.__version__)"

# Load model smoke test
python -c "
import torchxrayvision as xrv
model = xrv.models.get_model('densenet121-res224-all')
print('Model loaded:', type(model).__name__)
print('Pathologies:', model.pathologies)
print('Number of classes:', len(model.pathologies))
"

# Synthetic tensor forward pass
python -c "
import torch
import torchxrayvision as xrv
model = xrv.models.get_model('densenet121-res224-all')
model.eval()
x = torch.randn(1, 1, 224, 224)
with torch.no_grad():
    out = model(x)
print('Output shape:', out.shape)
print('Output sample:', out[0, :5])
"

# Inspect preprocessing requirements
python -c "
import torchxrayvision as xrv
model = xrv.models.get_model('densenet121-res224-all')
print('Model config:', model.cfg if hasattr(model, 'cfg') else 'N/A')
print('Expected input size: 224x224')
print('Normalization: [-1024, 1024] (HU units)')
"