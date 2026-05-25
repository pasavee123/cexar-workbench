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

If GHCR push fails, check repository Actions permissions and package permissions before changing the Dockerfile.
