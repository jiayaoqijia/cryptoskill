#!/usr/bin/env bash
# probe_tools.sh - detect optional security scanners and print the usable ones.
# Tool bridges are OPTIONAL: skills stay fully functional with rg/grep alone.
# Usage: bash skills/security-audit/scripts/probe_tools.sh [project_root]
# Output: one "tool<TAB>how-to-run" line per available scanner (empty = none).
set -uo pipefail

ROOT="${1:-.}"

have() { command -v "$1" >/dev/null 2>&1 && echo "yes" || echo "no"; }

# tool | binary | read-only invocation (all scans are non-mutating)
check() {
  local tool="$1" bin="$2" run="$3"
  if [ "$(have "$bin")" = "yes" ]; then
    printf '%s\t%s\n' "$tool" "$run"
  fi
}

# --- secrets (full history coverage that regex-on-worktree cannot give) ---
check gitleaks    gitleaks    "gitleaks detect --source '$ROOT' --redact -v"
check trufflehog  trufflehog  "trufflehog filesystem '$ROOT' --only-verified"

# --- dataflow / AST analysis (cross-file taint that greps cannot do) ---
check semgrep     semgrep     "semgrep scan --config auto --json --quiet '$ROOT'"

# --- dependency CVEs (offline complement to skills' live OSV API call) ---
check osv-scanner osv-scanner "osv-scanner --json --lockfile"   # run per lockfile
check npm-audit   npm         "npm audit --json (in project root)"
check pip-audit   pip-audit   "pip-audit -r requirements.txt --format json"

# --- IaC ---
check checkov     checkov     "checkov -d '$ROOT' --framework kubernetes,terraform,dockerfile --quiet"
check kube-linter kube-linter "kube-linter lint '$ROOT' --format json"
check tfsec       tfsec       "tfsec '$ROOT' --format json"

exit 0
