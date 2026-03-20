#!/usr/bin/env bash
# Install lnd for the remote signer machine.
#
# Default: pulls the pre-built Docker image (fast, no Go required).
# Fallback: --source builds lnd from source (requires Go 1.21+).
#
# The signer only needs lnd (not litd) since it only performs signing
# operations via gRPC — no loop, pool, tapd, or UI needed.
#
# Usage:
#   install.sh                              # Docker pull (default)
#   install.sh --version v0.20.0-beta       # Specific version
#   install.sh --source                     # Build from source

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VERSIONS_FILE="$SCRIPT_DIR/../../../versions.env"

# Source pinned versions.
if [ -f "$VERSIONS_FILE" ]; then
    source "$VERSIONS_FILE"
fi

VERSION=""
SOURCE=false
BUILD_TAGS="signrpc walletrpc chainrpc invoicesrpc routerrpc peersrpc kvdb_sqlite neutrinorpc"

# Parse arguments.
while [[ $# -gt 0 ]]; do
    case $1 in
        --version)
            VERSION="$2"
            shift 2
            ;;
        --source)
            SOURCE=true
            shift
            ;;
        --tags)
            BUILD_TAGS="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: install.sh [options]"
            echo ""
            echo "Install lnd for the remote signer."
            echo ""
            echo "Default: pulls the pre-built Docker image."
            echo ""
            echo "Options:"
            echo "  --version VERSION  Image tag or git tag (default: from versions.env)"
            echo "  --source           Build lnd from source instead of pulling Docker image"
            echo "  --tags TAGS        Build tags for --source mode"
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            exit 1
            ;;
    esac
done

if [ "$SOURCE" = true ]; then
    # --- Source build mode: clone and build lnd from source ---
    echo "=== Installing lnd (signer) from source ==="
    echo ""

    # Verify Go is installed.
    if ! command -v go &>/dev/null; then
        echo "Error: Go is not installed." >&2
        echo "Install Go from https://go.dev/dl/" >&2
        exit 1
    fi

    GO_VERSION=$(go version | grep -oE 'go[0-9]+\.[0-9]+' | head -1)
    echo "Go version: $GO_VERSION"
    echo "Build tags: $BUILD_TAGS"
    echo ""

    # Use LND_VERSION from versions.env if no --version given.
    SOURCE_VERSION="${VERSION:-${LND_VERSION:-}}"

    # Clone lnd into a temp directory and build from source.
    TMPDIR=$(mktemp -d)
    trap "rm -rf $TMPDIR" EXIT

    echo "Cloning lnd..."
    git clone --quiet https://github.com/lightningnetwork/lnd.git "$TMPDIR/lnd"

    cd "$TMPDIR/lnd"

    # Checkout specific version if requested, otherwise use latest tag.
    if [ -n "$SOURCE_VERSION" ]; then
        echo "Checking out $SOURCE_VERSION..."
        git checkout --quiet "$SOURCE_VERSION"
    else
        LATEST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
        if [ -n "$LATEST_TAG" ]; then
            echo "Using latest tag: $LATEST_TAG"
            git checkout --quiet "$LATEST_TAG"
        else
            echo "Using HEAD (no tags found)."
        fi
    fi
    echo ""

    GOBIN=$(go env GOPATH)/bin

    # Build lnd.
    echo "Building lnd..."
    go build -tags "$BUILD_TAGS" -o "$GOBIN/lnd" ./cmd/lnd
    echo "Done."

    # Build lncli.
    echo "Building lncli..."
    go build -tags "$BUILD_TAGS" -o "$GOBIN/lncli" ./cmd/lncli
    echo "Done."
    echo ""

    # Verify installation.
    if command -v lnd &>/dev/null; then
        echo "lnd installed: $(which lnd)"
        lnd --version 2>/dev/null || true
    else
        echo "Warning: lnd not found on PATH." >&2
        echo "Ensure \$GOPATH/bin is in your PATH." >&2
        echo "  export PATH=\$PATH:\$(go env GOPATH)/bin" >&2
    fi

    if command -v lncli &>/dev/null; then
        echo "lncli installed: $(which lncli)"
    else
        echo "Warning: lncli not found on PATH." >&2
    fi

    echo ""
    echo "Source installation complete."
    echo ""
    echo "Next steps:"
    echo "  1. Set up signer: skills/lightning-security-module/scripts/setup-signer.sh"

else
    # --- Docker mode (default): pull pre-built lnd image ---
    echo "=== Installing lnd (signer) via Docker ==="
    echo ""

    # Verify Docker is available.
    if ! command -v docker &>/dev/null; then
        echo "Error: Docker is not installed." >&2
        echo "Install Docker from https://docs.docker.com/get-docker/" >&2
        echo "" >&2
        echo "Or use --source to build from source (requires Go 1.21+)." >&2
        exit 1
    fi

    IMAGE="${LND_IMAGE:-lightninglabs/lnd}"
    TAG="${VERSION:-${LND_VERSION:-v0.20.0-beta}}"

    echo "Image: $IMAGE:$TAG"
    echo ""

    # Pull the image.
    echo "Pulling image..."
    docker pull "$IMAGE:$TAG"
    echo ""

    # Verify the image works.
    echo "Verifying installation..."
    docker run --rm "$IMAGE:$TAG" lnd --version 2>/dev/null || true
    echo ""

    echo "Installation complete."
    echo ""
    echo "Next steps:"
    echo "  1. Start signer:  skills/lightning-security-module/scripts/docker-start.sh"
    echo "  2. Set up signer: skills/lightning-security-module/scripts/setup-signer.sh"
fi
