#!/usr/bin/env bash
set -euo pipefail

# Start Cobo TSS Node (foreground)
# Usage: start-node.sh [--dir DIR] [--env dev|sandbox|prod]

DIR="$HOME/.cobo-tss-node"
ENV="prod"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dir) DIR="$2"; shift 2 ;;
    --env) ENV="$2"; shift 2 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

BIN="$DIR/cobo-tss-node"
KEYFILE="$DIR/.password"
CONFIG="$DIR/configs/cobo-tss-node-config.yaml"

[[ ! -x "$BIN" ]] && echo "❌ Binary not found: $BIN" && exit 1
[[ ! -f "$KEYFILE" ]] && echo "❌ Key file not found: $KEYFILE" && exit 1
[[ ! -f "$CONFIG" ]] && echo "❌ Config not found: $CONFIG" && exit 1

echo "🚀 Starting TSS Node (env: $ENV)..."
cd "$DIR"
exec "$BIN" start \
  "--${ENV}" \
  --key-file "$KEYFILE" \
  --config "$CONFIG" \
  --db "db/secrets.db"
