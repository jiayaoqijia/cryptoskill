#!/usr/bin/env bash
# new_skill.sh - scaffold a new security skill with everything CI expects.
# Usage: bash scripts/new_skill.sh <skill-name> ["One-line description"]
set -euo pipefail

NAME="${1:?usage: new_skill.sh <skill-name> [description]}"
DESC="${2:-TODO: one-line description with trigger conditions}"
[ "${#NAME}" -le 64 ] || { echo "name must be <= 64 chars" >&2; exit 1; }
[[ "$NAME" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]] || { echo "name must be lowercase-hyphens" >&2; exit 1; }

SK="skills/$NAME"
FIX="evals/fixtures/${NAME}-vuln-app"

mkdir -p "$SK/references" "$FIX"

cat > "$SK/SKILL.md" <<EOF
---
name: $NAME
description: $DESC
license: MIT
---

# ${NAME}

## Method
1. Map the surface (what to enumerate first)
2. Grep the sinks (start here; grow via evals)
\`\`\`bash
rg -n "TODO-SINK" -g '*.js' -g '*.py'
\`\`\`
3. Triage false positives (what makes a hit safe)
4. Severity defaults + fix patterns

## Reporting
Per finding: file:line, evidence excerpt, abuse story, fix. Tag with this skill's class names.
EOF

cat > "$SK/references/patterns.md" <<'PATTERNS_EOF'
# Pattern Library — NAME

| Sink | Dangerous | Safe | Notes |
|---|---|---|---|
| TODO | TODO | TODO | |
PATTERNS_EOF
sed -i "s/NAME/$NAME/g" "$SK/references/patterns.md"

cat > "$FIX/expected-findings.md" <<EOF
# ${NAME}-vuln-app — Expected findings

| # | Category | Where | Severity |
|---|---|---|---|
| 1 | TODO | app.js:1 | TODO |

## Must NOT trigger (near-misses — safe-counterpart file)

- TODO
EOF

echo "Scaffolded:"
echo "  $SK/SKILL.md              (frontmatter passes validate.py)"
echo "  $SK/references/patterns.md"
echo "  $FIX/expected-findings.md"
echo "Next: write fixture code, take Where-anchors from grep -n AFTER writing,"
echo "add selftest rules to scripts/selftest_patterns.py, run gates:"
echo "  python3 scripts/validate.py && python3 scripts/selftest_patterns.py"
