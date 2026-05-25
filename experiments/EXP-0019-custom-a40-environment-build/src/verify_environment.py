import json
import os
import platform
import subprocess
import sys


def run_optional(command):
    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
        )
        return {
            "command": command,
            "returncode": completed.returncode,
            "stdout": completed.stdout.strip(),
            "stderr": completed.stderr.strip(),
        }
    except Exception as exc:
        return {"command": command, "error": repr(exc)}


def main():
    import numpy
    import pandas
    import PIL
    import psutil
    import sklearn
    import torch
    import torchvision
    import tqdm
    import transformers
    import yaml

    report = {
        "python": sys.version,
        "platform": platform.platform(),
        "env": {
            "HF_HOME": os.environ.get("HF_HOME"),
            "TRANSFORMERS_CACHE": os.environ.get("TRANSFORMERS_CACHE"),
            "TORCH_HOME": os.environ.get("TORCH_HOME"),
            "PATH": os.environ.get("PATH"),
        },
        "packages": {
            "torch": torch.__version__,
            "torch_cuda": torch.version.cuda,
            "torchvision": torchvision.__version__,
            "transformers": transformers.__version__,
            "pillow": PIL.__version__,
            "numpy": numpy.__version__,
            "pandas": pandas.__version__,
            "scikit_learn": sklearn.__version__,
            "psutil": psutil.__version__,
            "tqdm": tqdm.__version__,
            "pyyaml": yaml.__version__,
        },
        "cuda": {
            "available": torch.cuda.is_available(),
            "device_count": torch.cuda.device_count(),
            "device_name_0": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        },
        "commands": {
            "nvidia_smi": run_optional(["nvidia-smi"]),
            "nvcc_version": run_optional(["nvcc", "--version"]),
            "workspace_disk": run_optional(["df", "-h", "/workspace"]),
        },
    }

    print(json.dumps(report, indent=2, sort_keys=True))

    failures = []
    if not sys.version.startswith("3.10."):
        failures.append("Python version is not 3.10.x")
    if torch.__version__ != "2.3.1+cu121":
        failures.append(f"Unexpected torch version: {torch.__version__}")
    if torch.version.cuda != "12.1":
        failures.append(f"Unexpected torch CUDA build: {torch.version.cuda}")
    if torchvision.__version__ != "0.18.1+cu121":
        failures.append(f"Unexpected torchvision version: {torchvision.__version__}")
    if os.environ.get("HF_HOME") != "/workspace/.cache/huggingface":
        failures.append("HF_HOME is not /workspace/.cache/huggingface")
    if os.environ.get("TORCH_HOME") != "/workspace/.cache/torch":
        failures.append("TORCH_HOME is not /workspace/.cache/torch")

    if failures:
        print("ENVIRONMENT_CONTRACT_FAILURES:")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)

    print("ENVIRONMENT_CONTRACT_PASS")


if __name__ == "__main__":
    main()
