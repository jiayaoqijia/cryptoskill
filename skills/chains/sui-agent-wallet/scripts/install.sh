#!/bin/bash
# Sui Agent Wallet - Installation Script

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

echo "🔧 Installing Sui Agent Wallet..."

# Install server dependencies
echo "📦 Installing server dependencies..."
cd "$SKILL_DIR/server"
bun install

# Generate icons from SVG
echo "🎨 Generating icons..."
ICONS_DIR="$SKILL_DIR/extension/icons"

# Create simple PNG icons using ImageMagick or just use placeholder
if command -v convert &> /dev/null; then
  # Create SVG first
  cat > /tmp/sui-agent-wallet.svg << 'EOF'
<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" viewBox="0 0 128 128">
  <rect width="128" height="128" rx="16" fill="#4da2ff"/>
  <path d="M32 48 L64 32 L96 48 L96 80 L64 96 L32 80 Z" fill="white" opacity="0.9"/>
  <circle cx="64" cy="64" r="16" fill="#4da2ff"/>
</svg>
EOF
  
  convert /tmp/sui-agent-wallet.svg -resize 16x16 "$ICONS_DIR/icon16.png"
  convert /tmp/sui-agent-wallet.svg -resize 48x48 "$ICONS_DIR/icon48.png"
  convert /tmp/sui-agent-wallet.svg -resize 128x128 "$ICONS_DIR/icon128.png"
  echo "   ✓ Icons generated"
else
  echo "   ⚠️  ImageMagick not found, using placeholder icons"
  # Create minimal 1x1 PNG as placeholder (base64 decoded)
  echo -n "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==" | base64 -d > "$ICONS_DIR/icon16.png"
  cp "$ICONS_DIR/icon16.png" "$ICONS_DIR/icon48.png"
  cp "$ICONS_DIR/icon16.png" "$ICONS_DIR/icon128.png"
fi

echo ""
echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo "1. Start the server:"
echo "   cd $SKILL_DIR/server && bun run index.ts"
echo ""
echo "2. Load the Chrome extension:"
echo "   - Open chrome://extensions/"
echo "   - Enable 'Developer mode'"
echo "   - Click 'Load unpacked'"
echo "   - Select: $SKILL_DIR/extension"
echo ""
echo "3. The wallet will auto-generate a new address on first start."
echo "   Check server logs for the address."
