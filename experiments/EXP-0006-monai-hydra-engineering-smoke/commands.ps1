# EXP-0006 MONAI Hydra Engineering Smoke - Command Ledger
# Reconstructed from EXPERIMENT_LOG.md execution traces.

# Step 1: Install MONAI and Hydra
pip install monai hydra-core

# Step 2: MONAI deterministic transform test
python -c "
from monai.utils import set_determinism
from monai.transforms import Compose, ScaleIntensity, RandRotate
import torch

set_determinism(seed=42)
transforms = Compose([ScaleIntensity(), RandRotate(range_x=0.1, prob=1.0)])
img = torch.rand(1, 64, 64)
out1 = transforms(img)
out2 = transforms(img)
print('Determinism test - outputs identical:', torch.equal(out1, out2))
print('MONAI version:', __import__('monai').__version__)
"

# Step 3: Hydra config composition test
python -c "
from hydra import compose, initialize_config_dir
import os

config_dir = os.path.abspath('experiments/EXP-0006-monai-hydra-engineering-smoke/configs')
with initialize_config_dir(config_dir=config_dir, version_base=None):
    cfg = compose(config_name='config')
    print('Config loaded:', cfg)
    print('Seed:', cfg.seed)
    print('Dataset:', cfg.dataset)
    print('Model:', cfg.model)
"

# Audit Note (2026-05-23): This document was retroactively generated/updated during
# the repository stress-test to reconstruct the historical timeline based on verified
# experiment artifacts and execution traces.
