#!/bin/bash
# View recent logs
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
tail -50 "$SCRIPT_DIR/trades.log" 2>/dev/null || echo "No logs yet"
