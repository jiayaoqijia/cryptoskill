#!/bin/bash

# Package Gate MCP Skill for distribution
# Creates both .skill file and release archives

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_NAME="gate-mcp"
VERSION="${1:-1.0.0}"

echo "📦 Packaging Gate MCP Skill v$VERSION"
echo ""

cd "$SCRIPT_DIR/.."

# Create temp directory
mkdir -p dist
cd dist

# Copy files
cp -r ../scripts .
cp ../SKILL.md .
cp ../README.md .
cp ../LICENSE . 2>/dev/null || true

# Create .skill file (zip with .skill extension)
zip -r "${PROJECT_NAME}-${VERSION}.skill" scripts/ SKILL.md README.md LICENSE

echo "✓ Created: dist/${PROJECT_NAME}-${VERSION}.skill"

# Also create tar.gz for GitHub releases
tar -czf "${PROJECT_NAME}-${VERSION}.tar.gz" scripts/ SKILL.md README.md LICENSE

echo "✓ Created: dist/${PROJECT_NAME}-${VERSION}.tar.gz"

cd ..

echo ""
echo "🎉 Packaging complete!"
echo ""
echo "Files in dist/:"
ls -lh dist/
echo ""
