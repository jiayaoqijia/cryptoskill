#!/usr/bin/env bash
# Add the MCP LNC server to Claude Code's MCP configuration.
#
# Usage:
#   setup-claude-config.sh                  # Project-level config (.mcp.json)
#   setup-claude-config.sh --scope global   # Global config (~/.claude.json)
#   setup-claude-config.sh --scope project  # Project config (.mcp.json)
#   setup-claude-config.sh --docker         # Use Docker instead of local binary
#
# Requires: jq

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MCP_SERVER_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)/lightning-mcp-server"

SCOPE="project"
USE_DOCKER=false

# Parse arguments.
while [[ $# -gt 0 ]]; do
    case $1 in
        --scope)
            SCOPE="$2"
            shift 2
            ;;
        --docker)
            USE_DOCKER=true
            shift
            ;;
        -h|--help)
            echo "Usage: setup-claude-config.sh [options]"
            echo ""
            echo "Add the MCP LNC server to Claude Code's MCP configuration."
            echo ""
            echo "Options:"
            echo "  --scope project    Add to .mcp.json in repo root (default)"
            echo "  --scope global     Add to ~/.claude.json (all projects)"
            echo "  --docker           Use Docker to run the server"
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            exit 1
            ;;
    esac
done

# Verify jq is available.
if ! command -v jq &>/dev/null; then
    echo "Error: jq is required. Install with: brew install jq" >&2
    exit 1
fi

# Determine config file path.
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
case $SCOPE in
    project)
        CONFIG_FILE="$REPO_ROOT/.mcp.json"
        ;;
    global)
        CONFIG_FILE="$HOME/.claude.json"
        ;;
    *)
        echo "Error: --scope must be 'project' or 'global'" >&2
        exit 1
        ;;
esac

echo "=== Setting Up Claude Code MCP Config ==="
echo ""
echo "Scope:  $SCOPE"
echo "Config: $CONFIG_FILE"
echo ""

# Load .env to read mailbox config.
ENV_FILE="$MCP_SERVER_DIR/.env"
LNC_MAILBOX_SERVER="mailbox.terminal.lightning.today:443"
LNC_DEV_MODE="false"
LNC_INSECURE="false"

if [ -f "$ENV_FILE" ]; then
    # Source only known variables.
    while IFS='=' read -r key value; do
        # Skip comments and empty lines.
        [[ "$key" =~ ^#.*$ ]] && continue
        [[ -z "$key" ]] && continue
        # Trim whitespace.
        key=$(echo "$key" | xargs)
        value=$(echo "$value" | xargs)
        case "$key" in
            LNC_MAILBOX_SERVER) LNC_MAILBOX_SERVER="$value" ;;
            LNC_DEV_MODE) LNC_DEV_MODE="$value" ;;
            LNC_INSECURE) LNC_INSECURE="$value" ;;
        esac
    done < "$ENV_FILE"
fi

# Build the MCP server config JSON.
if [ "$USE_DOCKER" = true ]; then
    MCP_ENTRY=$(jq -n \
        --arg mailbox "$LNC_MAILBOX_SERVER" \
        --arg devmode "$LNC_DEV_MODE" \
        --arg insecure "$LNC_INSECURE" \
        '{
            command: "docker",
            args: ["run", "--rm", "-i", "--network", "host",
                   "--env", "LNC_MAILBOX_SERVER",
                   "--env", "LNC_DEV_MODE",
                   "--env", "LNC_INSECURE",
                   "lightning-mcp-server"],
            env: {
                LNC_MAILBOX_SERVER: $mailbox,
                LNC_DEV_MODE: $devmode,
                LNC_INSECURE: $insecure
            }
        }')
else
    # Check that binary exists.
    BINARY_PATH=$(command -v lightning-mcp-server 2>/dev/null || echo "")
    if [ -z "$BINARY_PATH" ]; then
        echo "Warning: lightning-mcp-server not found on PATH." >&2
        echo "Run install.sh first, or use --docker." >&2
        echo ""
        BINARY_PATH="lightning-mcp-server"
    fi

    MCP_ENTRY=$(jq -n \
        --arg cmd "$BINARY_PATH" \
        --arg mailbox "$LNC_MAILBOX_SERVER" \
        --arg devmode "$LNC_DEV_MODE" \
        --arg insecure "$LNC_INSECURE" \
        '{
            command: $cmd,
            env: {
                LNC_MAILBOX_SERVER: $mailbox,
                LNC_DEV_MODE: $devmode,
                LNC_INSECURE: $insecure
            }
        }')
fi

# Read or create config file.
if [ -f "$CONFIG_FILE" ]; then
    CONFIG=$(cat "$CONFIG_FILE")
else
    CONFIG='{}'
fi

# Add or update the lnc server entry.
UPDATED=$(echo "$CONFIG" | jq --argjson entry "$MCP_ENTRY" '.mcpServers.lnc = $entry')

echo "$UPDATED" | jq . > "$CONFIG_FILE"

echo "MCP server config written to $CONFIG_FILE"
echo ""
echo "Entry added:"
echo "$MCP_ENTRY" | jq .
echo ""
echo "Next steps:"
echo "  1. Restart Claude Code to pick up the new MCP server"
echo "  2. Use lnc_connect with a pairing phrase to connect to your node"
