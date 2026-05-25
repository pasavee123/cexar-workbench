# commands.ps1

# Runner command ledger for EXP-0019.
# Every terminal command must be appended here before execution.
# Record exact command text, purpose, expected output, and result.

# =================================================================
# Phase 0: Safety and Ledger / Environment Checks
# =================================================================

# CMD-001 : docker --version
# Purpose: Determine if Docker is installed.
# Working directory: D:\cexar-workbench
# Destructive: No
# Result: Docker version 28.3.3, build 980b856 -- available.

# CMD-002 : docker buildx version
# Purpose: Check if buildx subcommand is available.
# Working directory: D:\cexar-workbench
# Destructive: No
# Result: "docker: unknown command: docker buildx" -- buildx is NOT a separate command on this installation
#        (Docker 28.x uses buildx as the default builder; `docker build --platform` is the supported path).

# CMD-003 : docker build --help | Select-String platform
# Purpose: Confirm --platform flag is supported on `docker build` directly.
# Working directory: D:\cexar-workbench
# Destructive: No
# Result: "--platform string  Set platform if server is multi-platform capable" -- flag supported.

# CMD-004 : docker info | Select-String OS/Architecture/Server
# Purpose: Check Docker server info for platform details.
# Working directory: D:\cexar-workbench
# Destructive: No
# Result: Non-conclusive. A Server-related line was reported, but CMD-006 later proved the Docker Desktop Linux Engine was unreachable.

# CMD-005 : git rev-parse HEAD
# Purpose: Get current git commit SHA for immutable image tag.
# Working directory: D:\cexar-workbench
# Destructive: No
# Result: c1faf5818f3e3d280340c4f8b465a095826c0a45

# =================================================================
# Phase 2: Docker Build Check
# =================================================================

# CMD-006 : docker build --platform linux/amd64 (ATTEMPT 1/3)
# Purpose: Build the custom A40 environment Docker image for linux/amd64.
# Working directory: D:\cexar-workbench
# Destructive: No (creates a Docker image, does not modify repo files)
# Image tag: ghcr.io/pasavee123/cexar-a40:cuda121-torch231-c1faf58
# Note: This runner-reserved tag is again aligned with the current canonical personal repository path.
# Result: Exit code 1. Docker daemon not running. Error: "Head http://%2F%2F.%2Fpipe%2FdockerDesktopLinuxEngine/_ping: The system cannot find the file specified."

# CMD-007 : Get-Process "Docker Desktop"
# Purpose: Check if Docker Desktop process is running on the Windows host.
# Working directory: D:\cexar-workbench
# Destructive: No
# Result: No process found. Docker Desktop is not running.

# CMD-008 : wsl --list --verbose
# Purpose: Check WSL2 VM status (Docker Desktop backend).
# Working directory: D:\cexar-workbench
# Destructive: No
# Result: docker-desktop: STATE=Stopped, VERSION=2. WSL2 backend is stopped.
#
