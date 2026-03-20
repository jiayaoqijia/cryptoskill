#!/usr/bin/env bash
# Set up a remote signer: create wallet, export credentials bundle.
#
# Container mode (default — auto-detects litd-signer container):
#   setup-signer.sh                              # Auto-detect container
#   setup-signer.sh --container litd-signer      # Explicit container
#
# Native mode:
#   setup-signer.sh --native                     # Local lnd signer
#   setup-signer.sh --native --network mainnet   # Mainnet
#   setup-signer.sh --native --password "mypass" # Custom passphrase
#
# Stores credentials at:
#   ~/.lnget/signer/wallet-password.txt           (mode 0600)
#   ~/.lnget/signer/seed.txt                      (mode 0600)
#   ~/.lnget/signer/credentials-bundle/           (exported credentials)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LNGET_SIGNER_DIR="${LNGET_SIGNER_DIR:-$HOME/.lnget/signer}"
LND_SIGNER_DIR="${LND_SIGNER_DIR:-$HOME/.lnd-signer}"
NETWORK="testnet"
PASSWORD=""
RPC_PORT=10012
REST_PORT=10013
CONTAINER=""
NATIVE=false

# Parse arguments.
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
        --password)
            PASSWORD="$2"
            shift 2
            ;;
        --rpc-port)
            RPC_PORT="$2"
            shift 2
            ;;
        --rest-port)
            REST_PORT="$2"
            shift 2
            ;;
        --container)
            CONTAINER="$2"
            shift 2
            ;;
        --native)
            NATIVE=true
            shift
            ;;
        -h|--help)
            echo "Usage: setup-signer.sh [options]"
            echo ""
            echo "Set up an lnd remote signer node."
            echo ""
            echo "Connection options:"
            echo "  --container NAME    Set up signer in a Docker container"
            echo "  --native            Set up signer on local lnd process"
            echo ""
            echo "Options:"
            echo "  --network NETWORK   Bitcoin network (default: testnet)"
            echo "  --lnddir DIR        Signer lnd data directory (default: ~/.lnd-signer)"
            echo "  --password PASS     Wallet passphrase (auto-generated if omitted)"
            echo "  --rpc-port PORT     Signer RPC port (default: 10012)"
            echo "  --rest-port PORT    Signer REST port (default: 10013)"
            echo ""
            echo "Container auto-detection: looks for litd-signer container."
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            exit 1
            ;;
    esac
done

# Auto-detect container if not native and no container specified.
if [ "$NATIVE" = false ] && [ -z "$CONTAINER" ]; then
    if command -v docker &>/dev/null; then
        if docker ps --format '{{.Names}}' 2>/dev/null | grep -qx 'litd-signer'; then
            CONTAINER="litd-signer"
        fi
    fi

    # If no container found, fall back to native.
    if [ -z "$CONTAINER" ]; then
        NATIVE=true
    fi
fi

# Container mode: verify container is running.
if [ -n "$CONTAINER" ]; then
    if ! docker ps --format '{{.Names}}' 2>/dev/null | grep -qx "$CONTAINER"; then
        echo "Error: Container '$CONTAINER' is not running." >&2
        echo "Start it with: skills/lightning-security-module/scripts/docker-start.sh" >&2
        exit 1
    fi
fi

echo "=== Remote Signer Setup ==="
echo ""
if [ -n "$CONTAINER" ]; then
    echo "Container:   $CONTAINER"
else
    echo "Mode:        native"
    echo "Signer dir:  $LND_SIGNER_DIR"
fi
echo "Network:     $NETWORK"
echo "Creds dir:   $LNGET_SIGNER_DIR"
echo "RPC port:    $RPC_PORT"
echo "REST port:   $REST_PORT"
echo ""

# Native mode: verify lnd is installed.
if [ "$NATIVE" = true ]; then
    if ! command -v lnd &>/dev/null; then
        echo "Error: lnd not found. Run install.sh first." >&2
        exit 1
    fi
fi

# Create directories with restricted permissions.
mkdir -p "$LNGET_SIGNER_DIR"
chmod 700 "$LNGET_SIGNER_DIR"

if [ "$NATIVE" = true ]; then
    mkdir -p "$LND_SIGNER_DIR"
fi

PASSWORD_FILE="$LNGET_SIGNER_DIR/wallet-password.txt"
SEED_OUTPUT="$LNGET_SIGNER_DIR/seed.txt"
CONF_FILE="$LNGET_SIGNER_DIR/signer-lnd.conf"

# Generate or use provided passphrase.
if [ -n "$PASSWORD" ]; then
    echo "Using provided passphrase."
else
    echo "Generating secure passphrase..."
    PASSWORD=$(openssl rand -base64 32 | tr -d '/+=' | head -c 32)
fi

# Store passphrase with restricted permissions on the host.
echo -n "$PASSWORD" > "$PASSWORD_FILE"
chmod 600 "$PASSWORD_FILE"
echo "Passphrase saved to $PASSWORD_FILE (mode 0600)"
echo ""

# Copy password file into container if applicable.
if [ -n "$CONTAINER" ]; then
    docker cp "$PASSWORD_FILE" "$CONTAINER:/root/.lnd/wallet-password.txt"
    echo "Password file copied into container."
fi

# Source shared REST helpers. REST_HOST defaults to localhost for
# the signer; CONTAINER_PORT defaults to REST_PORT.
REST_HOST="localhost"
source "$SCRIPT_DIR/../../lib/rest.sh"

# For native mode, create config and start lnd temporarily if needed.
if [ "$NATIVE" = true ]; then
    # Create signer config from template.
    TEMPLATE="$SCRIPT_DIR/../templates/signer-lnd.conf.template"
    if [ -f "$TEMPLATE" ]; then
        echo "Creating signer config from template..."
        # Replace network flag — match any existing network variant.
        sed -E "s/bitcoin\.(testnet|mainnet|signet|regtest)=true/bitcoin.$NETWORK=true/g" "$TEMPLATE" > "$CONF_FILE"

        # Replace password file path.
        sed -i.bak "s|wallet-unlock-password-file=.*|wallet-unlock-password-file=$PASSWORD_FILE|g" "$CONF_FILE"

        # Replace port numbers. Native mode binds to localhost, not 0.0.0.0.
        sed -i.bak "s|rpclisten=0.0.0.0:10012|rpclisten=localhost:$RPC_PORT|g" "$CONF_FILE"
        sed -i.bak "s|restlisten=0.0.0.0:10013|restlisten=localhost:$REST_PORT|g" "$CONF_FILE"
        rm -f "$CONF_FILE.bak"
        echo "Config saved to $CONF_FILE"
    else
        echo "Error: Config template not found at $TEMPLATE" >&2
        exit 1
    fi
    echo ""

    # Start signer lnd temporarily for wallet creation if not running.
    if rest_call GET "/v1/state" &>/dev/null; then
        echo "Signer lnd is already running."
    else
        echo "Starting signer lnd temporarily for wallet creation..."
        nohup lnd \
            --lnddir="$LND_SIGNER_DIR" \
            --configfile="$CONF_FILE" \
            > "$LNGET_SIGNER_DIR/signer-setup.log" 2>&1 &
        SIGNER_PID=$!

        echo "Waiting for signer lnd to start (PID: $SIGNER_PID)..."
        for i in {1..30}; do
            if rest_call GET "/v1/state" &>/dev/null; then
                break
            fi
            if ! kill -0 "$SIGNER_PID" 2>/dev/null; then
                echo "Error: signer lnd exited. Check $LNGET_SIGNER_DIR/signer-setup.log" >&2
                exit 1
            fi
            sleep 2
            echo "  Waiting... ($i/30)"
        done
        echo ""
    fi
else
    # Container mode: wait for REST API to be available inside container.
    wait_for_rest "signer REST API"
fi

# Create wallet via REST API.
echo "=== Creating Signer Wallet ==="

# Generate seed.
echo "Generating wallet seed..."
SEED_RESPONSE=$(rest_call GET "/v1/genseed")

MNEMONIC=$(echo "$SEED_RESPONSE" | jq -r '.cipher_seed_mnemonic[]' 2>/dev/null)
if [ -z "$MNEMONIC" ] || [ "$MNEMONIC" = "null" ]; then
    echo "Error: Failed to generate seed." >&2
    echo "Response: $SEED_RESPONSE" >&2
    exit 1
fi

# Store seed with restricted permissions on host.
echo "$MNEMONIC" > "$SEED_OUTPUT"
chmod 600 "$SEED_OUTPUT"
echo "Seed mnemonic saved to $SEED_OUTPUT (mode 0600)"
echo ""

# Initialize wallet with password and seed.
SEED_JSON=$(echo "$MNEMONIC" | jq -R . | jq -s .)
PAYLOAD=$(jq -n \
    --arg pass "$(echo -n "$PASSWORD" | base64)" \
    --argjson seed "$SEED_JSON" \
    '{wallet_password: $pass, cipher_seed_mnemonic: $seed}')

RESPONSE=$(rest_call POST "/v1/initwallet" "$PAYLOAD")

ERROR=$(echo "$RESPONSE" | jq -r '.message // empty' 2>/dev/null)
if [ -n "$ERROR" ]; then
    echo "Error creating wallet: $ERROR" >&2
    exit 1
fi

echo "Signer wallet created successfully!"
echo ""

# Wait for signer to be fully ready (wallet unlocked, RPC available).
echo "Waiting for signer to be fully ready..."
for i in {1..30}; do
    STATE=$(rest_call GET "/v1/state" 2>/dev/null | jq -r '.state // empty' 2>/dev/null)
    if [ "$STATE" = "SERVER_ACTIVE" ]; then
        break
    fi
    sleep 2
    echo "  Waiting for RPC... ($i/30)"
done
echo ""

# Export credentials bundle.
echo "=== Exporting Credentials Bundle ==="
if [ -n "$CONTAINER" ]; then
    "$SCRIPT_DIR/export-credentials.sh" \
        --container "$CONTAINER" \
        --network "$NETWORK" \
        --rpc-port "$RPC_PORT"
else
    "$SCRIPT_DIR/export-credentials.sh" \
        --network "$NETWORK" \
        --lnddir "$LND_SIGNER_DIR" \
        --rpc-port "$RPC_PORT"
fi

echo ""
echo "=== Signer Setup Complete ==="
echo ""
echo "Credential locations:"
echo "  Passphrase: $PASSWORD_FILE"
echo "  Seed:       $SEED_OUTPUT"
if [ "$NATIVE" = true ]; then
    echo "  Config:     $CONF_FILE"
fi
echo ""
echo "IMPORTANT: The seed mnemonic at $SEED_OUTPUT is the master secret."
echo "Back it up securely and restrict access to this machine."
echo ""
echo "Next steps:"
echo "  1. Copy the credentials bundle to your agent machine"
echo "  2. On the agent: skills/lnd/scripts/import-credentials.sh --bundle <path>"
echo "  3. On the agent: skills/lnd/scripts/create-wallet.sh"
if [ -n "$CONTAINER" ]; then
    echo "  4. On the agent: skills/lnd/scripts/docker-start.sh --watchonly"
else
    echo "  4. On the agent: skills/lnd/scripts/start-lnd.sh --native --signer-host <this-ip>:$RPC_PORT"
fi
