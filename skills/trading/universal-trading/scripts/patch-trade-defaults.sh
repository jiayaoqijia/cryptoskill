#!/usr/bin/env bash
# Patch upstream example defaults to avoid forcing one fee token.
# Run from universal-account-example directory.

set -euo pipefail

TARGET_DIR="${1:-.}"
BUY_EVM_FILE="$TARGET_DIR/examples/buy-evm.ts"

if [ ! -f "$BUY_EVM_FILE" ]; then
    echo "buy-evm.ts not found, skip default patch."
    exit 0
fi

if ! grep -q "usePrimaryTokens" "$BUY_EVM_FILE"; then
    echo "buy-evm.ts already has no usePrimaryTokens restriction."
    exit 0
fi

tmp_file="$(mktemp)"
awk '
    /usePrimaryTokens/ { next }
    /\/\/ can use specific token to pay/ { next }
    { print }
' "$BUY_EVM_FILE" > "$tmp_file"
mv "$tmp_file" "$BUY_EVM_FILE"

echo "Patched buy-evm.ts: removed usePrimaryTokens restriction."
