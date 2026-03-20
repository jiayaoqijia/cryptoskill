#!/bin/bash
# Start the whale copier in background
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
screen -dmS whale-copier python3 "$SCRIPT_DIR/copy_trader.py" "$@"
echo "🐋 Whale Copier started in background"
echo "   View logs: screen -r whale-copier"
echo "   Or: tail -f $SCRIPT_DIR/trades.log"
