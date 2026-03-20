#!/usr/bin/env bash
# Start the remote signer container.
#
# Usage:
#   docker-start.sh                          # Default (testnet, background)
#   docker-start.sh --network mainnet        # Mainnet (real coins)
#   docker-start.sh --regtest                # Regtest with bitcoind backend
#   docker-start.sh --foreground             # Run in foreground (show logs)
#   docker-start.sh --build                  # Rebuild before starting
#   docker-start.sh --docker-network NAME    # Join an existing Docker network

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_DIR="$SCRIPT_DIR/../templates"
VERSIONS_FILE="$SCRIPT_DIR/../../../versions.env"
LIB_DIR="$SCRIPT_DIR/../../lib"

DETACH=true
BUILD=false
CUSTOM_NETWORK=""
DOCKER_NETWORK=""

# Source pinned versions so compose files pick them up as env vars.
if [ -f "$VERSIONS_FILE" ]; then
    source "$VERSIONS_FILE"
    export LND_VERSION LND_IMAGE
fi

# Source config generation functions.
source "$LIB_DIR/config-gen.sh"

# Parse arguments.
while [[ $# -gt 0 ]]; do
    case $1 in
        --network)
            CUSTOM_NETWORK="$2"
            shift 2
            ;;
        --regtest)
            CUSTOM_NETWORK="regtest"
            shift
            ;;
        --docker-network)
            DOCKER_NETWORK="$2"
            shift 2
            ;;
        --build)
            BUILD=true
            shift
            ;;
        --foreground|-f)
            DETACH=false
            shift
            ;;
        -h|--help)
            echo "Usage: docker-start.sh [options]"
            echo ""
            echo "Start the remote signer container."
            echo ""
            echo "Options:"
            echo "  --network NET         Override network (testnet, mainnet, signet, regtest)"
            echo "  --regtest             Shorthand for --network regtest"
            echo "  --docker-network NET  Join an existing Docker network (e.g., regtest bitcoind)"
            echo "  --build               Rebuild images before starting"
            echo "  --foreground, -f      Run in foreground (show logs)"
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            exit 1
            ;;
    esac
done

# Override network if specified on command line.
if [ -n "$CUSTOM_NETWORK" ]; then
    NETWORK="$CUSTOM_NETWORK"
fi

EFFECTIVE_NETWORK="${NETWORK:-testnet}"

# --- Generate runtime config from template ---

LNGET_LND_DIR="${LNGET_LND_DIR:-$HOME/.lnget/lnd}"
mkdir -p "$LNGET_LND_DIR"

generate_lnd_config \
    "$TEMPLATE_DIR/signer-lnd.conf.template" \
    "$LNGET_LND_DIR/signer-lnd.conf" \
    "$EFFECTIVE_NETWORK" \
    "${LND_DEBUG:-info}" \
    ""

export SIGNER_CONF_PATH="$LNGET_LND_DIR/signer-lnd.conf"

# --- Start container ---

cd "$TEMPLATE_DIR"

echo "=== Starting signer container ==="
echo "  Config:   $SIGNER_CONF_PATH"
echo "  Network:  $EFFECTIVE_NETWORK"
echo "  Image:    ${LND_IMAGE:-lightninglabs/lnd}:${LND_VERSION:-v0.20.0-beta}"
echo ""

# Build the docker-compose command.
CMD="docker compose -f docker-compose-signer.yml"

if [ "$BUILD" = true ]; then
    CMD="$CMD up --build"
else
    CMD="$CMD up"
fi

if [ "$DETACH" = true ]; then
    CMD="$CMD -d"
fi

echo "Running: $CMD"
eval "$CMD"

# When running on regtest, connect the signer to the regtest Docker network
# so it can reach bitcoind.
if [ "$EFFECTIVE_NETWORK" = "regtest" ] && [ "$DETACH" = true ]; then
    REGTEST_NETWORK="${DOCKER_NETWORK:-$(docker network ls --filter name=regtest --format '{{.Name}}' | head -1)}"
    if [ -n "$REGTEST_NETWORK" ]; then
        echo "Connecting signer to regtest network: $REGTEST_NETWORK"
        docker network connect "$REGTEST_NETWORK" litd-signer 2>/dev/null || true
    else
        echo "Warning: No regtest Docker network found." >&2
        echo "Start regtest bitcoind first, or use --docker-network to specify." >&2
    fi
fi

if [ "$DETACH" = true ]; then
    echo ""
    echo "Signer started in background."
    echo ""
    echo "Check logs:"
    echo "  docker logs -f litd-signer"
    echo ""
    echo "Next: set up the signer wallet (if first run):"
    echo "  skills/lightning-security-module/scripts/setup-signer.sh --container litd-signer"
fi
