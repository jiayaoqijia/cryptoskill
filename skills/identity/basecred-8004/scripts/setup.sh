#!/usr/bin/env bash
set -e

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
echo "=== ERC-8004 Skill Setup ==="
echo "Directory: $SKILL_DIR"

# Check Node.js
if ! command -v node &>/dev/null; then
  echo "❌ Node.js not found. Install Node.js >= 18."
  exit 1
fi

NODE_VER=$(node -v | sed 's/v//' | cut -d. -f1)
if [ "$NODE_VER" -lt 18 ]; then
  echo "❌ Node.js >= 18 required (found v$NODE_VER)"
  exit 1
fi
echo "✅ Node.js $(node -v)"

# Init package.json if missing
if [ ! -f "$SKILL_DIR/package.json" ]; then
  cd "$SKILL_DIR"
  npm init -y --silent 2>/dev/null
  # Set type to module for ESM
  node -e "const p=require('./package.json'); p.type='module'; require('fs').writeFileSync('package.json', JSON.stringify(p,null,2))"
  echo "✅ package.json created (ESM)"
fi

# Install agent0-sdk
cd "$SKILL_DIR"
npm install agent0-sdk@1.5.2 2>&1
echo "✅ agent0-sdk installed"

echo ""
echo "=== Setup complete ==="
echo "Set env vars: PRIVATE_KEY, RPC_URL, CHAIN_ID (optional), PINATA_JWT (optional)"
