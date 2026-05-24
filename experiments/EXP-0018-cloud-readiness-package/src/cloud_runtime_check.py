"""Cloud runtime check skeleton.

No credentials or provider-specific startup logic belongs in this file.
"""

from __future__ import annotations


def collect_runtime_info() -> dict:
    """TODO: Collect GPU, CUDA, torch, disk, RAM, and HF cache info on cloud."""
    raise NotImplementedError("Implemented during EXP-0019 cloud smoke run.")

