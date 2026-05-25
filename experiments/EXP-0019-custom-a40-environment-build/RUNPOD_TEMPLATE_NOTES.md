# RUNPOD_TEMPLATE_NOTES.md

## Intended Template Type

Interactive RunPod Pod, not Serverless.

## Container Image

Use the immutable GHCR image produced from this experiment.

Preferred tag form:

```text
ghcr.io/pasavee123/cexar-a40:cuda121-torch231-<gitsha>
```

Do not use `latest` as the experiment image tag.

## Template Settings

- GPU: NVIDIA A40
- Exposed port: `22/tcp`
- Volume mount path: `/workspace`
- Container disk: at least 200 GB, recommended 500 GB
- SSH over exposed TCP: enabled
- Jupyter: optional, not required
- Startup command: default image `CMD ["/start.sh"]`
- SSH key: use RunPod key injection or pass a public key via a runtime environment variable such as `PUBLIC_KEY`; never store private keys or PATs in the image or repository.

## Registry

Public GHCR image is preferred for the first RunPod pull.

If private GHCR is required:
- Registry: `ghcr.io`
- Username: GitHub username or bot user
- Password: GitHub PAT with `read:packages`
- Select this registry credential in the RunPod template.

Never write PATs or registry credentials into repository files.

## Immediate Runtime Checks

After Pod boot:

```bash
nvidia-smi
python --version
nvcc --version
python /opt/cexar/verify_environment.py
df -h /workspace
```
