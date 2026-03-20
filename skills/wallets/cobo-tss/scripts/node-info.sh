#!/usr/bin/env bash
set -euo pipefail

# Show Cobo TSS Node info
# Usage: node-info.sh [--dir DIR] [--group [GROUP_ID]]

DIR="$HOME/.cobo-tss-node"
GROUP=""
GROUP_ID=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dir)   DIR="$2"; shift 2 ;;
    --group)
      GROUP="yes"
      if [[ $# -gt 1 && ! "$2" =~ ^-- ]]; then
        GROUP_ID="$2"; shift 2
      else
        shift
      fi
      ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

BIN="$DIR/cobo-tss-node"
KEYFILE="$DIR/.password"

[[ ! -x "$BIN" ]] && echo "❌ Binary not found: $BIN" && exit 1
[[ ! -f "$KEYFILE" ]] && echo "❌ Key file not found: $KEYFILE" && exit 1

cd "$DIR"
if [[ -n "$GROUP" ]]; then
  "$BIN" info group $GROUP_ID \
    --key-file "$KEYFILE" \
    --db "db/secrets.db"
else
  "$BIN" info \
    --key-file "$KEYFILE" \
    --db "db/secrets.db"
fi
