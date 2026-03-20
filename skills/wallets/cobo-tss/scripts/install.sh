#!/usr/bin/env bash
set -euo pipefail

# Cobo TSS Node installer
# Downloads and extracts the binary from the public GitHub release
#
# Usage: install.sh [--version VERSION] [--dir DIR]

VERSION=""
DIR="$HOME/.cobo-tss-node"
REPO="CoboTest/cobo-tss-node-release"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --version) VERSION="$2"; shift 2 ;;
    --dir)     DIR="$2"; shift 2 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

# Detect OS and arch
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m)
case "$ARCH" in
  x86_64)  ARCH="amd64" ;;
  aarch64|arm64) ARCH="arm64" ;;
  *) echo "Unsupported arch: $ARCH"; exit 1 ;;
esac

echo "📦 OS: $OS, Arch: $ARCH"

# Resolve version
if [[ -z "$VERSION" ]]; then
  echo "🔍 Finding latest release..."
  VERSION=$(curl -fsSL "https://api.github.com/repos/$REPO/releases/latest" | python3 -c "import json,sys;print(json.load(sys.stdin)['tag_name'])")
fi
echo "📌 Version: $VERSION"

# Download
ASSET_NAME="cobo-tss-node-${VERSION}-${OS}-${ARCH}.tar.gz"
DOWNLOAD_URL="https://github.com/$REPO/releases/download/$VERSION/$ASSET_NAME"
TMPDIR=$(mktemp -d)
trap "rm -rf $TMPDIR" EXIT

echo "⬇️  Downloading $ASSET_NAME..."
curl -fsSL "$DOWNLOAD_URL" -o "$TMPDIR/$ASSET_NAME"

# Extract
echo "📂 Extracting..."
tar xzf "$TMPDIR/$ASSET_NAME" -C "$TMPDIR"

# Find binary
EXTRACTED_DIR="$TMPDIR/cobo-tss-node-${VERSION}-${OS}-${ARCH}"
BINARY="$EXTRACTED_DIR/cobo-tss-node"
[[ ! -f "$BINARY" ]] && BINARY=$(find "$TMPDIR" -name "cobo-tss-node" -type f | head -1)
[[ ! -f "$BINARY" ]] && echo "❌ Binary not found in archive" && exit 1

# Install
mkdir -p "$DIR"/{configs,db,logs,recovery}
cp "$BINARY" "$DIR/cobo-tss-node"
chmod 755 "$DIR/cobo-tss-node"

# Copy config template if not exists
TEMPLATE=$(find "$TMPDIR" -name "*.yaml.template" | head -1)
if [[ -n "$TEMPLATE" && ! -f "$DIR/configs/cobo-tss-node-config.yaml" ]]; then
  cp "$TEMPLATE" "$DIR/configs/cobo-tss-node-config.yaml.template"
  cp "$TEMPLATE" "$DIR/configs/cobo-tss-node-config.yaml"
  echo "📄 Config template installed"
fi

echo ""
echo "✅ Installed cobo-tss-node $VERSION to $DIR"
echo ""
echo "Next steps:"
echo "  1. ./scripts/setup-keyfile.sh --dir $DIR"
echo "  2. ./scripts/init-node.sh --dir $DIR"
