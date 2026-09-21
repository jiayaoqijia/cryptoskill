#!/usr/bin/env bash
# Fast secret-pattern scan. Prints file:line:match, sorted, deduped.
# Usage: scan.sh [project_root]   (default: .)
set -uo pipefail

ROOT="${1:-.}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PATTERNS_FILE="$SCRIPT_DIR/../references/patterns.txt"

EXCLUDES=(
  --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=vendor
  --exclude-dir=dist --exclude-dir=build --exclude-dir=target
  --exclude-dir=.venv --exclude-dir=venv --exclude-dir=__pycache__
  --exclude-dir=coverage --exclude-dir=.next --exclude-dir=.terraform
  --exclude=*.min.js --exclude=*.map
)

if [ ! -f "$PATTERNS_FILE" ]; then
  echo "error: patterns file missing: $PATTERNS_FILE" >&2
  exit 1
fi

while IFS= read -r pat; do
  [ -z "$pat" ] && continue
  case "$pat" in \#*) continue ;; esac
  grep -rInE --binary-files=without-match "$pat" "$ROOT" "${EXCLUDES[@]}" 2>/dev/null
done < "$PATTERNS_FILE" | sort -u

exit 0
