# Install dependencies (if needed)
pip install transformers huggingface_hub

# Check if transformers can load rad-dino
python -c "from transformers import AutoModel; print('transformers available')"

# Load RAD-DINO model
python -c "
import torch
from transformers import AutoModel
model = AutoModel.from_pretrained('microsoft/rad-dino')
print('Model type:', type(model).__name__)
print('Config:', model.config)
print('Parameters:', sum(p.numel() for p in model.parameters()))
"

# Synthetic tensor forward pass
python -c "
import torch
from transformers import AutoModel
model = AutoModel.from_pretrained('microsoft/rad-dino')
model.eval()
x = torch.randn(1, 3, 518, 518)
with torch.no_grad():
    out = model(x)
print('Output shape:', out.shape)
print('Output (last):', out[0, -1, :5] if out.dim() == 3 else out[0, :5])
"