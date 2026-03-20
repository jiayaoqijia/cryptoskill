#!/bin/bash
# Nostr Skill - Silent installation (agent runs this)
set -e

SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"

# Install Node dependencies (includes cocod locally)
cd "$SKILL_DIR/scripts"
npm install --quiet 2>/dev/null

echo "OK"
