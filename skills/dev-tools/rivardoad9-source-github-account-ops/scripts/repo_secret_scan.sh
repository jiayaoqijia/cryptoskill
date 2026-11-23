#!/usr/bin/env bash
# Two-layer repo leak scan: gitleaks (full history, all branches) + custom patterns.
# Usage: repo_secret_scan.sh <repo-dir> [<repo-dir> ...]
# Prints MASKED hits only — never full secret values. Exit 0 even when hits exist;
# read the report and classify each hit by hand.
set -u
GITLEAKS=${GITLEAKS:-$HOME/.local/bin/gitleaks}
PAT='([0-9]{8,10}:[A-Za-z0-9_-]{35})|([0-9a-f]{64})|([1-9A-HJ-NP-Za-km-z]{87,88})|(BEGIN [A-Z ]*PRIVATE KEY)|(secretKey|private_key|PRIVATE_KEY|api_key|API_KEY)[^A-Za-z0-9]{0,4}["'"'"'][A-Za-z0-9+/=_-]{25,}|(\+62[0-9]{8,13})'
mask() { sed -E 's/[0-9a-f]{64}/[HEX64]/g; s/[0-9]{8,10}:[A-Za-z0-9_-]{35}/[TG-TOKEN]/g; s/[1-9A-HJ-NP-Za-km-z]{87,88}/[BASE58]/g; s/[A-Za-z0-9+/=_-]{25,}/[VALUE-REDACTED]/g; s/\+62[0-9]{8,13}/[PHONE-62]/g'; }

# gitleaks: install once from the release asset if missing
if [ ! -x "$GITLEAKS" ]; then
  echo "gitleaks missing. Install with:"
  echo "  URL=\$(gh api repos/gitleaks/gitleaks/releases/latest -q '.assets[]|select(.name|test(\"linux_x64.tar.gz\$\"))|.browser_download_url')"
  echo "  curl -sL \"\$URL\" -o /tmp/gl.tgz && tar xzf /tmp/gl.tgz -C /tmp gitleaks && install -m755 /tmp/gitleaks ~/.local/bin/gitleaks"
fi

for r in "$@"; do
  [ -d "$r/.git" ] || { echo "skip (bukan repo git): $r"; continue; }
  echo "════ $(basename "$r") ════"
  echo "author/identity: $(git -C "$r" log --all --format='%an <%ae>' 2>/dev/null | sort -u | tr '\n' ',')"
  if [ -x "$GITLEAKS" ]; then
    ( cd "$r" && "$GITLEAKS" detect --source . --no-banner --redact --log-opts="--all" \
        -f json -r /tmp/gl_scan_"$(basename "$r")".json >/dev/null 2>&1 )
    python3 - "$r" <<'PY'
import json, sys, os
p = "/tmp/gl_scan_%s.json" % os.path.basename(sys.argv[1])
try:
    d = json.load(open(p))
except Exception:
    print("  gitleaks: n/a"); raise SystemExit
print("  gitleaks findings:", len(d))
for f in d[:10]:
    print("   -", f.get("RuleID"), "|", f.get("File"), "line", f.get("StartLine"),
          "| commit", (f.get("Commit") or "")[:8], "| match:", (f.get("Match") or "")[:40].replace("\n", " "))
PY
  fi
  # custom patterns: working tree then history (scoped to THIS repo dir only)
  ( cd "$r"
    echo "  working tree hits:"
    grep -rInE "$PAT" . --exclude-dir=.git --exclude-dir=node_modules 2>/dev/null | head -8 | mask | cut -c1-150
    echo "  history hits:"
    for c in $(git rev-list --all 2>/dev/null | head -500); do
      git grep -InE "$PAT" "$c" -- . 2>/dev/null | head -3
    done | head -8 | mask | cut -c1-150
    echo "  .env / db / keypair ever tracked:"
    git rev-list --all --objects 2>/dev/null | awk '{print $2}' | grep -Ei '^\.env|\.env\.|\.(db|sqlite3?)$|keypair|id\.json|\.pem$' | sort -u | head -8
    echo "  sensitive files in working tree:"
    find . -path ./.git -prune -o -type f \( -iname '.env*' -o -iname '*secret*' -o -iname '*.pem' -o -iname '*credential*' \) -print 2>/dev/null | head -8
  )
done
echo "=== DONE — classify every hit by hand before publishing ==="
echo "benign: .env.example placeholders, 44-char base58 Solana mint in tests,"
echo "        87-88 char base58 (tx sigs), 43-char program IDs, tx hashes in logs"
