#!/bin/bash
# Setup script for sui-move skill
# Clones official Sui and Move documentation

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REF_DIR="$SCRIPT_DIR/references"

echo "🚀 Setting up Sui Move skill references..."

mkdir -p "$REF_DIR"
cd "$REF_DIR"

# Clone Move Book
if [ ! -d "move-book" ]; then
    echo "📚 Cloning Move Book..."
    git clone --depth 1 https://github.com/MystenLabs/move-book.git
else
    echo "📚 Move Book already exists, pulling latest..."
    cd move-book && git pull && cd ..
fi

# Clone Sui docs (sparse checkout for docs only)
if [ ! -d "sui" ]; then
    echo "📖 Cloning Sui docs..."
    git clone --depth 1 --filter=blob:none --sparse https://github.com/MystenLabs/sui.git
    cd sui && git sparse-checkout set docs && cd ..
else
    echo "📖 Sui docs already exists, pulling latest..."
    cd sui && git pull && cd ..
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Reference locations:"
echo "  Move Book: $REF_DIR/move-book/book/"
echo "  Sui Docs:  $REF_DIR/sui/docs/"
echo ""
echo "Quick search:"
echo "  rg -i 'keyword' $REF_DIR/move-book/book/ --type md"
