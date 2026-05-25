# BUILD_AND_PUSH_NOTES.md

## Canonical Build Recommendation

Build outside RunPod for auditability:
- GitHub Actions, or
- local Docker with explicit `linux/amd64` platform.

RunPod GPU Pods should be used as runtime targets, not the canonical image builder.

## Selected Canonical Path

CeXaR now uses GitHub Actions as the preferred canonical builder for this image.

Workflow path:

```text
.github/workflows/build-cexar-a40-image.yml
```

Manual trigger:

```text
GitHub repository -> Actions -> build-cexar-a40-image -> Run workflow
```

Runner selection:

```text
runner_label = <WarpBuild Runner ID>
```

The workflow keeps `ubuntu-latest` as a fallback default, but the preferred build path is to enter the WarpBuild Runner ID provided by the WarpBuild dashboard.

Expected GHCR tags:

```text
ghcr.io/pasavee123/cexar-a40:cuda121-torch231-<short_sha>
ghcr.io/pasavee123/cexar-a40:cuda121-torch231-<full_sha>
```

Use the full SHA tag in experiment records when possible.

## Local Build Example

Register exact commands in `commands.ps1` before executing.

```bash
docker buildx build \
  --platform linux/amd64 \
  -f experiments/EXP-0019-custom-a40-environment-build/docker/Dockerfile \
  -t ghcr.io/pasavee123/cexar-a40:cuda121-torch231-<gitsha> \
  experiments/EXP-0019-custom-a40-environment-build
```

## Push Example

Only push after human approval and registry authentication.

```bash
docker push ghcr.io/pasavee123/cexar-a40:cuda121-torch231-<gitsha>
```

## GitHub Actions Workflow

The workflow has been installed at `.github/workflows/build-cexar-a40-image.yml`.

It is manual-only (`workflow_dispatch`) to prevent unplanned large image builds on every push.

The workflow frees unused GitHub-hosted runner disk space before building because CUDA devel images and PyTorch wheels are large. It also removes swap and hosted tool caches to reduce the chance of `No space left on device` during the PyTorch install layer.

The workflow also moves Docker's data root to `/mnt/docker` before the build. GitHub-hosted runners often have more usable space on `/mnt` than on the default Docker root filesystem, and CUDA devel image layers plus PyTorch wheels can exceed the default root volume.

For WarpBuild, choose a runner with enough disk for CUDA devel image layers and PyTorch CUDA wheels. The version contract remains unchanged; only the build runner changes.

If GHCR push fails, check repository Actions permissions and package permissions before changing the Dockerfile.
