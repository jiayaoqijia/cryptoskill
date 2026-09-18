#!/usr/bin/env bash
#
# Two-arm type proof: does a hand-written type agree with the authoritative one?
#
#   substitution-ab.sh <repo-path> <probe-dir> [probe-dest]
#
#   <repo-path>   repo checked out at the PR head, deps installed
#   <probe-dir>   directory of probe-*.ts files (see skill.md Step 3)
#   [probe-dest]  where to stage them, relative to <repo-path>; must sit inside
#                 the tsconfig `include` paths. Default: src/__type-probe__
#
# Arm A must be silent. If it is not, stop — nothing in Arm B is attributable.
set -uo pipefail

REPO=${1:?usage: substitution-ab.sh <repo-path> <probe-dir> [probe-dest]}
PROBES=${2:?usage: substitution-ab.sh <repo-path> <probe-dir> [probe-dest]}
DEST=${3:-src/__type-probe__}

: "${NODE_OPTIONS:=--max-old-space-size=9216}"
export NODE_OPTIONS

cd "$REPO" || exit 1
[ -d "$PROBES" ] || { echo "no such probe dir: $PROBES" >&2; exit 1; }

cleanup() { rm -rf "$REPO/$DEST"; }
trap cleanup EXIT INT TERM

echo "=== Arm A — PR head as written (must be silent) ==="
A=$(npx tsc -p tsconfig.json --noEmit 2>&1)
A_STATUS=$?
if [ -n "$A" ]; then
  echo "$A"
  echo
  echo "!! Arm A is NOT silent (exit $A_STATUS). The comparison is INCONCLUSIVE:"
  echo "!! Arm B's diagnostics cannot be attributed to the substitution."
  echo "!! Fix the baseline (toolchain, lockfile, heap, project scope) before reading Arm B."
  exit 2
fi
echo "0 diagnostics — baseline clean, Arm B is attributable."
echo

echo "=== Arm B — same commit, derived types substituted ==="
mkdir -p "$DEST"
cp "$PROBES"/probe-*.ts "$DEST"/ 2>/dev/null || {
  echo "no probe-*.ts found in $PROBES" >&2; exit 1; }

npx tsc -p tsconfig.json --noEmit 2>&1
echo
echo "=== Each diagnostic above is a disagreement the hand-written type concealed. ==="
echo "=== Before believing any of them: confirm the diagnostic is the one the    ==="
echo "=== claim needs, not an earlier cause short-circuiting it (skill.md Step 5).==="
