#!/usr/bin/env bash
# Bootstrap universal-account-example in the current workspace.
# Usage:
#   ./bootstrap-example.sh [target-dir]

set -euo pipefail

REPO_URL="${UNIVERSAL_ACCOUNT_EXAMPLE_REPO:-https://github.com/Particle-Network/universal-account-example.git}"
TARBALL_URL="${UNIVERSAL_ACCOUNT_EXAMPLE_TARBALL:-https://github.com/Particle-Network/universal-account-example/archive/refs/heads/main.tar.gz}"
FETCH_MODE="${UNIVERSAL_ACCOUNT_EXAMPLE_FETCH:-auto}" # auto | git | tarball
TARGET_DIR="${1:-universal-account-example}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

require_command() {
    if ! command -v "$1" >/dev/null 2>&1; then
        echo "Missing required command: $1"
        exit 1
    fi
}

require_command node
require_command npm

clone_with_fallback() {
    if [ "$FETCH_MODE" = "git" ]; then
        require_command git
        echo "Cloning $REPO_URL into $TARGET_DIR (git forced)"
        git clone "$REPO_URL" "$TARGET_DIR"
        return
    fi

    if [ "$FETCH_MODE" = "auto" ] && command -v git >/dev/null 2>&1; then
        echo "Cloning $REPO_URL into $TARGET_DIR (git)"
        git clone "$REPO_URL" "$TARGET_DIR"
        return
    fi

    if [ "$FETCH_MODE" != "auto" ] && [ "$FETCH_MODE" != "tarball" ]; then
        echo "Invalid UNIVERSAL_ACCOUNT_EXAMPLE_FETCH: $FETCH_MODE"
        echo "Use one of: auto, git, tarball"
        exit 1
    fi

    require_command curl
    require_command tar

    echo "Downloading source archive (fetch mode: $FETCH_MODE)."
    echo "Downloading $TARBALL_URL"

    tmp_dir="$(mktemp -d)"
    archive_path="$tmp_dir/universal-account-example.tar.gz"
    extract_dir="$tmp_dir/extract"

    curl -fsSL "$TARBALL_URL" -o "$archive_path"
    mkdir -p "$extract_dir"
    tar -xzf "$archive_path" -C "$extract_dir"

    source_dir="$(find "$extract_dir" -mindepth 1 -maxdepth 1 -type d | head -n 1)"
    if [ -z "${source_dir:-}" ] || [ ! -d "$source_dir" ]; then
        echo "Failed to locate extracted source directory."
        exit 1
    fi

    mv "$source_dir" "$TARGET_DIR"
    rm -rf "$tmp_dir"
}

if [ -d "$TARGET_DIR/.git" ]; then
    echo "Repository already exists: $TARGET_DIR"
elif [ -d "$TARGET_DIR" ]; then
    if [ -f "$TARGET_DIR/package.json" ]; then
        echo "Directory exists and has package.json: $TARGET_DIR"
    else
        echo "Target directory exists but is not a git repo: $TARGET_DIR"
        echo "Choose another path or remove the directory first."
        exit 1
    fi
else
    clone_with_fallback
fi

if [ ! -f "$TARGET_DIR/package.json" ]; then
    echo "package.json not found in $TARGET_DIR"
    exit 1
fi

echo "Installing npm dependencies in $TARGET_DIR"
(
    cd "$TARGET_DIR"
    npm install
)

echo ""
echo "Bootstrap complete."
echo "Next commands:"
echo "  cd $TARGET_DIR"
echo "  bash $SCRIPT_DIR/setup-wizard.sh new"
echo "  npx tsx examples/get-primary-asset.ts"
