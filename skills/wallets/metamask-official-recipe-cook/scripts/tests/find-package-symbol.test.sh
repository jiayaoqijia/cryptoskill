#!/usr/bin/env bash
set -euo pipefail

# `! cmd` is exempt from errexit, so negative assertions go through refute.
refute() { if "$@"; then echo "unexpected match: $*" >&2; exit 1; fi; }

sandbox="$(mktemp -d)"
trap 'rm -rf "$sandbox"' EXIT
root="$sandbox/checkout"
mkdir -p "$root/node_modules/@metamask/example/dist" "$root/node_modules/example/dist"
cat > "$root/node_modules/@metamask/example/dist/types.d.mts" <<'EOF'
export interface Position { symbol: string }
EOF
cat > "$root/node_modules/example/dist/types.d.ts" <<'EOF'
export type decoy = thing0
export type exact = thing[0]
EOF

skill="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
output="$("$skill/scripts/find-package-symbol" @metamask/example Position "$root")"
grep -q 'types.d.mts:1:export interface Position' <<<"$output"

literal_output="$("$skill/scripts/find-package-symbol" example 'thing[0]' "$root")"
grep -q 'types.d.ts:2:export type exact = thing\[0\]' <<<"$literal_output"
refute grep -q 'decoy' <<<"$literal_output"

set +e
missing="$("$skill/scripts/find-package-symbol" @metamask/missing Position "$root" 2>&1)"
status=$?
set -e
test "$status" -eq 1
grep -q 'Package not installed:' <<<"$missing"

# Invalid names fail before rg can inspect any path. The traversal target exists
# and carries the requested symbol so the old behavior would expose it.
mkdir -p "$sandbox/outside-secret" "$sandbox/probe-bin"
printf '%s\n' 'export type OUTSIDE_SECRET_MARKER = string' > "$sandbox/outside-secret/leak.d.ts"
real_rg="$(command -v rg)"
cat > "$sandbox/probe-bin/rg" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
touch "${RG_PROBE:?}"
exec "${REAL_RG:?}" "$@"
SH
chmod +x "$sandbox/probe-bin/rg"

too_long="$(printf 'a%.0s' {1..215})"
invalid_packages=(
  '../../outside-secret'
  '@scope\name'
  '@scope'
  '@scope/'
  '@/name'
  '@scope/name/extra'
  'Uppercase'
  '.hidden'
  '..'
  "$too_long"
)
for invalid in "${invalid_packages[@]}"; do
  rm -f "$sandbox/rg-called"
  set +e
  invalid_output="$(PATH="$sandbox/probe-bin:$PATH" RG_PROBE="$sandbox/rg-called" REAL_RG="$real_rg" \
    "$skill/scripts/find-package-symbol" "$invalid" OUTSIDE_SECRET_MARKER "$root" 2>&1)"
  invalid_status=$?
  set -e
  test "$invalid_status" -eq 2
  grep -q '^Invalid npm package name:' <<<"$invalid_output"
  refute grep -q 'OUTSIDE_SECRET_MARKER' <<<"$invalid_output"
  test ! -e "$sandbox/rg-called"
done

rg -Fq '.agents/skills/mms-recipe-cook/scripts/find-package-symbol <package> <symbol>' "$skill/skill.md"

echo 'find-package-symbol: safe package names, literal symbols, bounded lookup passed'
