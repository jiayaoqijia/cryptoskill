#!/bin/bash
# x402-client setup script
# Creates a lightweight Node.js project with x402 client dependencies
# and copies the x402 scripts into the install directory.
# Usage: bash setup.sh <skill-dir> [install-dir]

set -e

SKILL_DIR="${1:?Usage: bash setup.sh <skill-dir> [install-dir]}"
DIR="${2:-$HOME/.x402-client}"

if [ -d "$DIR/node_modules/@x402" ]; then
  echo "x402 client already installed at $DIR"
  # Still copy scripts in case they were updated
  cp "$SKILL_DIR/scripts/"*.mjs "$DIR/" 2>/dev/null || true
  exit 0
fi

echo "Installing x402 client to $DIR..."
mkdir -p "$DIR"
cd "$DIR"

cat > package.json << 'EOF'
{
  "name": "x402-client",
  "version": "1.0.0",
  "private": true,
  "type": "module",
  "dependencies": {
    "@x402/fetch": "^2.3",
    "@x402/evm": "^2.3",
    "viem": "^2.0"
  }
}
EOF

npm install --quiet 2>&1 | tail -3

# Copy scripts into install dir so they resolve node_modules correctly
cp "$SKILL_DIR/scripts/"*.mjs "$DIR/"

echo "x402 client installed at $DIR"
echo "Scripts available: wallet-gen.mjs, x402-fetch.mjs"
