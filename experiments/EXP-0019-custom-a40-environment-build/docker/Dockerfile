FROM nvidia/cuda:12.1.1-cudnn8-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    HF_HOME=/workspace/.cache/huggingface \
    TRANSFORMERS_CACHE=/workspace/.cache/huggingface/transformers \
    TORCH_HOME=/workspace/.cache/torch

RUN apt-get update -y && apt-get install -y --no-install-recommends \
      ca-certificates \
      curl \
      git \
      openssh-server \
      python3 \
      python3-pip \
      python3-venv \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /opt/venv
ENV PATH=/opt/venv/bin:$PATH

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /root/.cache/pip

RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && rm -rf /tmp/* /var/tmp/* /root/.cache/pip

RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cu121 \
      torch==2.3.1 \
      torchvision==0.18.1 \
    && rm -rf /tmp/* /var/tmp/* /root/.cache/pip

COPY requirements.lock.txt /tmp/requirements.lock.txt
RUN pip install --no-cache-dir -r /tmp/requirements.lock.txt \
    && rm -rf /tmp/* /var/tmp/* /root/.cache/pip

RUN mkdir -p /var/run/sshd /workspace /workspace/.cache/huggingface /workspace/.cache/torch

COPY docker/start.sh /start.sh
COPY src/verify_environment.py /opt/cexar/verify_environment.py
RUN chmod +x /start.sh

WORKDIR /workspace

EXPOSE 22

CMD ["/start.sh"]
