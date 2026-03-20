#!/bin/bash
set -e

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"

if [ ! -d "$SKILL_DIR/node_modules" ]; then
  echo "Installing aaveclaw dependencies..."
  cd "$SKILL_DIR"
  npm install --omit=dev
  echo "Dependencies installed."
else
  echo "Dependencies already installed."
fi
