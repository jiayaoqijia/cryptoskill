#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VERSION_FILE="$ROOT_DIR/VERSION"
README_FILE="$ROOT_DIR/README.md"
SKILL_FILE="$ROOT_DIR/SKILL.md"

usage() {
  cat <<'EOF'
Usage:
  scripts/release.sh <version> [changelog]

Environment:
  CLAWHUB_SLUG   Default: kraken-skill
  CLAWHUB_NAME   Default: Kraken Skill

Behavior:
  - validates semver
  - updates VERSION
  - prints the clawhub publish command
  - prints a suggested git tag command
EOF
}

[ "$#" -ge 1 ] || {
  usage >&2
  exit 1
}

VERSION="$1"
CHANGELOG="${2:-}"
CLAWHUB_SLUG="${CLAWHUB_SLUG:-kraken-skill}"
CLAWHUB_NAME="${CLAWHUB_NAME:-Kraken Skill}"

case "$VERSION" in
  [0-9]*.[0-9]*.[0-9]*)
    ;;
  *)
    echo "invalid semver: $VERSION" >&2
    exit 1
    ;;
esac

printf '%s\n' "$VERSION" >"$VERSION_FILE"

if [ -n "$CHANGELOG" ]; then
  echo "release notes: $CHANGELOG"
fi

echo "version updated in $VERSION_FILE"
echo
echo "publish:"
printf 'clawhub publish %q --slug %q --name %q --version %q --tags latest' "$ROOT_DIR" "$CLAWHUB_SLUG" "$CLAWHUB_NAME" "$VERSION"
if [ -n "$CHANGELOG" ]; then
  printf ' --changelog %q' "$CHANGELOG"
fi
printf '\n'
echo
echo "suggested git tag:"
printf 'git tag -a v%s -m %q\n' "$VERSION" "release v$VERSION"
