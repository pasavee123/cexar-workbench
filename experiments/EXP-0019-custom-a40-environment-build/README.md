# EXP-0019 Custom A40 Environment Build

## Purpose

Build and verify a reproducible custom RunPod interactive Pod image for CeXaR before running RAD-DINO cloud workloads.

This experiment is environment-only. It must not run medical inference, model training, dataset upload, AUROC evaluation, or production integration.

## Target Contract

- GPU target: NVIDIA A40 only
- Base image: `nvidia/cuda:12.1.1-cudnn8-devel-ubuntu22.04`
- Python: 3.10 from Ubuntu 22.04 apt packages
- Python environment: `/opt/venv`
- PyTorch: `torch==2.3.1+cu121`
- torchvision: `torchvision==0.18.1+cu121`
- Workspace: `/workspace`
- Hugging Face cache: `/workspace/.cache/huggingface`
- Torch cache: `/workspace/.cache/torch`
- Run mode: interactive Pod, SSH / VS Code Remote-SSH
- Serverless: out of scope
- Jupyter: optional, not required

## Success Definition

EXP-0019 passes only if the runner creates a complete custom image package and verifies the environment contract without changing the version targets.

The expected next step is EXP-0020: RAD-DINO 100-image GPU smoke run using the verified image.

