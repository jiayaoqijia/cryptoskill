#!/bin/bash
# Resolve the eth2-quickstart repo root for an installed skill.

set -Eeuo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

is_repo_root() {
    local candidate="$1"
    [[ -x "$candidate/scripts/eth2qs.sh" && -f "$candidate/exports.sh" ]]
}

print_or_fail() {
    local candidate="$1"
    if is_repo_root "$candidate"; then
        printf '%s\n' "$candidate"
        exit 0
    fi
}

if git_root="$(git rev-parse --show-toplevel 2>/dev/null)"; then
    print_or_fail "$git_root"
fi

candidate="$(realpath "$SCRIPT_DIR/../../..")"
print_or_fail "$candidate"

candidate="$PWD"
while [[ "$candidate" != "/" ]]; do
    print_or_fail "$candidate"
    candidate="$(dirname "$candidate")"
done

echo "eth2-quickstart repo root not found. Install/use this skill inside an eth2-quickstart checkout." >&2
exit 1
