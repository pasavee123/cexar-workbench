# Inspect BiomedCLIP model card
python -c "
from huggingface_hub import model_info
info = model_info('microsoft/BiomedCLIP-PubMedBERT_256-vit_base_patch16_224')
print('Model ID:', info.modelId)
print('License:', info.cardData.get('license', 'N/A') if info.cardData else 'N/A')
print('Tags:', info.tags)
"

# Try loading BiomedCLIP via open_clip
pip install open_clip_torch

# Inspect CheXzero repo
python -c "
import requests
r = requests.get('https://api.github.com/repos/stanfordmlgroup/CheXzero')
data = r.json()
print('Repo:', data.get('full_name'))
print('Stars:', data.get('stargazers_count'))
print('Description:', data.get('description'))
print('Updated:', data.get('updated_at'))
print('License:', data.get('license', {}).get('spdx_id') if data.get('license') else 'N/A')
"