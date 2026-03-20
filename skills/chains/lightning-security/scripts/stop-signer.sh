#!/usr/bin/env bash
# Stop the remote signer — delegates to Docker by default.
#
# Usage:
#   stop-signer.sh                          # Docker stop (auto-detect)
#   stop-signer.sh --clean                  # Docker stop + remove volumes
#   stop-signer.sh --native                 # Stop native signer process
#   stop-signer.sh --native --force         # SIGTERM native process
#   stop-signer.sh --container litd-signer  # Explicit container
#   stop-signer.sh --rpcserver remote:10012 --tlscertpath ~/tls.cert --macaroonpath ~/admin.macaroon

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NATIVE=false

# Check for --native flag before parsing other args.
PASS_ARGS=()
for arg in "$@"; do
    if [ "$arg" = "--native" ]; then
        NATIVE=true
    else
        PASS_ARGS+=("$arg")
    fi
done

# If not native mode, delegate to docker-stop.sh.
if [ "$NATIVE" = false ]; then
    # Check if we have a --container arg or docker-specific flags.
    HAS_CONTAINER_ARG=false
    HAS_RPCSERVER=false
    for arg in "${PASS_ARGS[@]}"; do
        if [ "$arg" = "--container" ]; then
            HAS_CONTAINER_ARG=true
        fi
        if [ "$arg" = "--rpcserver" ]; then
            HAS_RPCSERVER=true
        fi
    done

    # If --rpcserver is specified, fall through to native stop logic (remote
    # mode needs lncli).
    if [ "$HAS_RPCSERVER" = true ]; then
        NATIVE=true
    elif [ "$HAS_CONTAINER_ARG" = true ]; then
        # Explicit container — use native stop logic (handles docker exec).
        NATIVE=true
    elif command -v docker &>/dev/null; then
        if docker ps --format '{{.Names}}' 2>/dev/null | grep -qx 'litd-signer'; then
            exec "$SCRIPT_DIR/docker-stop.sh" "${PASS_ARGS[@]}"
        fi
        # No signer container found, fall through to native.
        NATIVE=true
    else
        NATIVE=true
    fi
fi

# --- Native / container-specific stop logic ---

LND_SIGNER_DIR="${LND_SIGNER_DIR:-}"
NETWORK="${NETWORK:-testnet}"
RPC_PORT=10012
FORCE=false
CONTAINER=""
RPCSERVER=""
TLSCERTPATH=""
MACAROONPATH=""

# Parse arguments.
set -- "${PASS_ARGS[@]}"
while [[ $# -gt 0 ]]; do
    case $1 in
        --force)
            FORCE=true
            shift
            ;;
        --network)
            NETWORK="$2"
            shift 2
            ;;
        --rpc-port)
            RPC_PORT="$2"
            shift 2
            ;;
        --container)
            CONTAINER="$2"
            shift 2
            ;;
        --rpcserver)
            RPCSERVER="$2"
            shift 2
            ;;
        --tlscertpath)
            TLSCERTPATH="$2"
            shift 2
            ;;
        --macaroonpath)
            MACAROONPATH="$2"
            shift 2
            ;;
        --clean|-v)
            # Docker-specific flags; delegate to docker-stop.sh.
            exec "$SCRIPT_DIR/docker-stop.sh" "${PASS_ARGS[@]}"
            ;;
        -h|--help)
            echo "Usage: stop-signer.sh [options]"
            echo ""
            echo "Stop the remote signer."
            echo ""
            echo "Docker options (default):"
            echo "  --clean, -v            Remove volumes (clean state)"
            echo ""
            echo "Native options (--native):"
            echo "  --native               Stop native signer process"
            echo "  --force                Send SIGTERM immediately"
            echo "  --container NAME       Stop signer in a specific container"
            echo "  --rpcserver HOST:PORT  Connect to a remote signer node"
            echo "  --tlscertpath PATH     TLS certificate for remote connection"
            echo "  --macaroonpath PATH    Macaroon for remote authentication"
            echo "  --rpc-port PORT        Signer RPC port (default: 10012)"
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            exit 1
            ;;
    esac
done

# Apply default lnddir if not set.
if [ -z "$LND_SIGNER_DIR" ]; then
    if [ -n "$CONTAINER" ]; then
        LND_SIGNER_DIR="/root/.lnd"
    else
        LND_SIGNER_DIR="$HOME/.lnd-signer"
    fi
fi

if [ -n "$CONTAINER" ]; then
    # Docker container mode.
    if ! docker ps --format '{{.Names}}' | grep -qx "$CONTAINER"; then
        echo "Container '$CONTAINER' is not running."
        exit 0
    fi

    echo "Stopping signer lnd in container '$CONTAINER'..."

    if [ "$FORCE" = true ]; then
        docker stop "$CONTAINER"
        echo "Container stopped."
    else
        if docker exec "$CONTAINER" lncli --rpcserver="localhost:$RPC_PORT" \
            --lnddir="$LND_SIGNER_DIR" \
            --network="$NETWORK" \
            stop 2>/dev/null; then
            echo "Graceful shutdown initiated."
        else
            echo "lncli stop failed, stopping container..."
            docker stop "$CONTAINER"
            echo "Container stopped."
        fi
    fi
    exit 0
fi

# Build connection flags for lncli.
CONN_FLAGS=(--network="$NETWORK" --lnddir="$LND_SIGNER_DIR")
if [ -n "$RPCSERVER" ]; then
    CONN_FLAGS+=("--rpcserver=$RPCSERVER")
else
    CONN_FLAGS+=("--rpcserver=localhost:$RPC_PORT")
fi
if [ -n "$TLSCERTPATH" ]; then
    CONN_FLAGS+=("--tlscertpath=$TLSCERTPATH")
fi
if [ -n "$MACAROONPATH" ]; then
    CONN_FLAGS+=("--macaroonpath=$MACAROONPATH")
fi

# Remote mode — stop via lncli only (no PID or port access).
if [ -n "$RPCSERVER" ]; then
    echo "Stopping remote signer at $RPCSERVER..."
    if lncli "${CONN_FLAGS[@]}" stop; then
        echo "Graceful shutdown initiated."
    else
        echo "Error: lncli stop failed for remote signer." >&2
        exit 1
    fi
    exit 0
fi

# Local mode — check if signer is running by probing the RPC port.
if ! curl -sk "https://localhost:$RPC_PORT/v1/state" &>/dev/null 2>&1; then
    echo "Signer lnd is not running (port $RPC_PORT not responding)."
    exit 0
fi

echo "Stopping signer lnd..."

if [ "$FORCE" = true ]; then
    # Find the process listening on the signer RPC port and kill it.
    SIGNER_PID=$(lsof -ti ":$RPC_PORT" 2>/dev/null | head -1 || true)
    if [ -n "$SIGNER_PID" ]; then
        kill "$SIGNER_PID"
        echo "Sent SIGTERM to PID $SIGNER_PID."
    else
        echo "Warning: Could not find process on port $RPC_PORT." >&2
        exit 1
    fi
else
    # Try graceful shutdown via lncli.
    if lncli "${CONN_FLAGS[@]}" stop 2>/dev/null; then
        echo "Graceful shutdown initiated."
    else
        echo "lncli stop failed, finding process on port $RPC_PORT..."
        SIGNER_PID=$(lsof -ti ":$RPC_PORT" 2>/dev/null | head -1 || true)
        if [ -n "$SIGNER_PID" ]; then
            kill "$SIGNER_PID"
            echo "Sent SIGTERM to PID $SIGNER_PID."
        else
            echo "Warning: Could not find process to stop." >&2
            exit 1
        fi
    fi
fi

# Wait for process to exit.
echo "Waiting for signer lnd to exit..."
for i in {1..15}; do
    if ! curl -sk "https://localhost:$RPC_PORT/v1/state" &>/dev/null 2>&1; then
        echo "Signer lnd stopped."
        exit 0
    fi
    sleep 1
done

echo "Warning: signer lnd did not exit within 15 seconds." >&2
echo "Use --force or manually kill the process." >&2
exit 1
