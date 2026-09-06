#!/usr/bin/env bash
# Build the .skill ZIP package for Claude Desktop.
#
# Users can attach this single file to a Claude Desktop conversation
# instead of copying individual files.
#
# Usage:
#   ./skills/elfa-ai/scripts/build-skill.sh
#
# Output:
#   dist/elfa-ai.skill

set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
REPO_ROOT="$(cd "$SKILL_DIR/../.." && pwd)"
DIST_DIR="$REPO_ROOT/dist"
SKILL_NAME="elfa-ai"
OUTPUT="$DIST_DIR/${SKILL_NAME}.skill"

rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"

# Stage files under elfa-ai/ directory and zip
STAGING=$(mktemp -d)
trap 'rm -rf "$STAGING"' EXIT

mkdir -p "$STAGING/$SKILL_NAME/references" "$STAGING/$SKILL_NAME/scripts"
cp "$SKILL_DIR/SKILL.md" "$STAGING/$SKILL_NAME/"
cp "$SKILL_DIR/references/swagger.json" "$STAGING/$SKILL_NAME/references/"
cp "$SKILL_DIR/scripts/elfa_call.sh" "$STAGING/$SKILL_NAME/scripts/"

cd "$STAGING"
zip -r "$OUTPUT" "$SKILL_NAME/"

echo "Built: $OUTPUT ($(du -h "$OUTPUT" | cut -f1))"
