#!/bin/bash
set -e

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"

if [ ! -d "$SKILL_DIR/node_modules" ]; then
  bash "$SKILL_DIR/scripts/setup.sh"
fi

node "$SKILL_DIR/scripts/entries/faucet.js" "$@"
