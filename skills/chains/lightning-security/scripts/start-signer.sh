#!/usr/bin/env bash
# Start the remote signer lnd node — delegates to Docker by default.
#
# Usage:
#   start-signer.sh                          # Docker (default)
#   start-signer.sh --network mainnet        # Mainnet
#   start-signer.sh --native                 # Native lnd signer
#   start-signer.sh --native --foreground    # Native, foreground

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

# If not native mode, delegate to docker-start.sh.
if [ "$NATIVE" = false ]; then
    if command -v docker &>/dev/null; then
        exec "$SCRIPT_DIR/docker-start.sh" "${PASS_ARGS[@]}"
    else
        echo "Docker not available. Falling back to native mode." >&2
        echo "Install Docker or use --native explicitly." >&2
        echo ""
        NATIVE=true
    fi
fi

# --- Native mode: original signer startup logic ---

LNGET_SIGNER_DIR="${LNGET_SIGNER_DIR:-$HOME/.lnget/signer}"
LND_SIGNER_DIR="${LND_SIGNER_DIR:-$HOME/.lnd-signer}"
NETWORK="testnet"
FOREGROUND=false
EXTRA_ARGS=""
RPC_PORT=10012
CONF_FILE="$LNGET_SIGNER_DIR/signer-lnd.conf"

# Parse arguments.
set -- "${PASS_ARGS[@]}"
while [[ $# -gt 0 ]]; do
    case $1 in
        --network)
            NETWORK="$2"
            shift 2
            ;;
        --lnddir)
            LND_SIGNER_DIR="$2"
            shift 2
            ;;
        --foreground)
            FOREGROUND=true
            shift
            ;;
        --rpc-port)
            RPC_PORT="$2"
            shift 2
            ;;
        --extra-args)
            EXTRA_ARGS="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: start-signer.sh [options]"
            echo ""
            echo "Start the remote signer lnd node."
            echo ""
            echo "Docker options (default):"
            echo "  --network NET     Override network (testnet, mainnet, signet)"
            echo "  --foreground      Run in foreground (show logs)"
            echo ""
            echo "Native options (--native):"
            echo "  --native             Run lnd as a local process"
            echo "  --lnddir DIR         Signer lnd data directory (default: ~/.lnd-signer)"
            echo "  --rpc-port PORT      Signer RPC port (default: 10012)"
            echo "  --extra-args ARGS    Additional lnd arguments"
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            exit 1
            ;;
    esac
done

# Verify lnd is installed.
if ! command -v lnd &>/dev/null; then
    echo "Error: lnd not found. Run install.sh first." >&2
    exit 1
fi

# Check if signer is already running by checking the RPC port.
if curl -sk "https://localhost:$RPC_PORT/v1/state" &>/dev/null 2>&1; then
    echo "Signer lnd is already running on port $RPC_PORT."
    echo "Use stop-signer.sh to stop it first."
    exit 1
fi

# Verify config exists.
if [ ! -f "$CONF_FILE" ]; then
    echo "Error: Signer config not found at $CONF_FILE" >&2
    echo "Run setup-signer.sh --native first." >&2
    exit 1
fi

echo "=== Starting Signer LND ==="
echo "Network:  $NETWORK"
echo "Data dir: $LND_SIGNER_DIR"
echo "Config:   $CONF_FILE"
echo "RPC port: $RPC_PORT"
echo ""

LOG_FILE="$LNGET_SIGNER_DIR/signer-lnd.log"

if [ "$FOREGROUND" = true ]; then
    exec lnd \
        --lnddir="$LND_SIGNER_DIR" \
        --configfile="$CONF_FILE" \
        $EXTRA_ARGS
else
    nohup lnd \
        --lnddir="$LND_SIGNER_DIR" \
        --configfile="$CONF_FILE" \
        $EXTRA_ARGS \
        > "$LOG_FILE" 2>&1 &
    SIGNER_PID=$!
    echo "Signer lnd started in background (PID: $SIGNER_PID)"
    echo "Log file: $LOG_FILE"
    echo ""

    # Wait briefly and verify it's running.
    sleep 2
    if kill -0 "$SIGNER_PID" 2>/dev/null; then
        echo "Signer lnd is running."
    else
        echo "Error: signer lnd exited immediately. Check $LOG_FILE" >&2
        tail -20 "$LOG_FILE" 2>/dev/null
        exit 1
    fi

    echo ""
    echo "The signer is ready to accept connections from watch-only nodes."
    echo "Watch-only nodes connect to this machine on port $RPC_PORT."
fi
