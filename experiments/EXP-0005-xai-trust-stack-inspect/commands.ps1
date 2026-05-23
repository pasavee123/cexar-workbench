# Install (no-deps to avoid PyTorch upgrade conflict)
python -m pip install grad-cam captum --no-deps

# Test grad-cam import
python -c "import pytorch_grad_cam; print('grad-cam available')"

# Test grad-cam with ResNet18
python -c "
import torch
import torchvision
from pytorch_grad_cam import GradCAM
model = torchvision.models.resnet18(weights='DEFAULT')
model.eval()
target_layer = [model.layer4[-1]]
cam = GradCAM(model=model, target_layers=target_layer)
x = torch.randn(1, 3, 224, 224)
grayscale_cam = cam(input_tensor=x, targets=None)
print('Grad-CAM output shape:', grayscale_cam.shape)
print('Grad-CAM values (min, max, mean):', grayscale_cam.min(), grayscale_cam.max(), grayscale_cam.mean())
"

# Test Captum import
python -c "
import torch
import torchvision
from captum.attr import IntegratedGradients
model = torchvision.models.resnet18(weights='DEFAULT')
model.eval()
ig = IntegratedGradients(model)
x = torch.randn(1, 3, 224, 224)
baseline = torch.zeros_like(x)
attributions, delta = ig.attribute(x, baselines=baseline, target=0, return_convergence_delta=True)
print('IG attribution shape:', attributions.shape)
print('IG convergence delta:', delta.item())
"

# Check Quantus
pip install quantus --no-deps

# CheXlocalize repo check
python -c "
import requests
r = requests.get('https://api.github.com/repos/rajpurkarlab/cheXlocalize')
data = r.json()
print('Repo:', data.get('full_name'))
print('Stars:', data.get('stargazers_count'))
print('Description:', data.get('description'))
print('License:', data.get('license', {}).get('spdx_id') if data.get('license') else 'N/A')
print('Updated:', data.get('updated_at'))
"