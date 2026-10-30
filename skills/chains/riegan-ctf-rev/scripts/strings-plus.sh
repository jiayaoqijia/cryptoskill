#!/usr/bin/env bash
# strings-plus.sh — one-shot triage bundle for a binary.
# Prints: file type, entropy per section (stdlib python3 estimate), strings
# highlights, ldd, filtered readelf header/dynamic/symbols, objdump sections.
#
# Usage: strings-plus.sh <binary> [--help]
set -euo pipefail

usage() {
    sed -n '2,6p' "$0" | sed 's/^# \{0,1\}//'
}

if [[ $# -lt 1 || "$1" == "--help" || "$1" == "-h" ]]; then
    usage
    exit 0
fi

BIN=$1
[[ -f "$BIN" ]] || { echo "no such file: $BIN" >&2; exit 1; }

hr() { printf '\n===== %s =====\n' "$1"; }

hr "file"
file "$BIN"

hr "entropy per section (0-8; >7.0 suggests packed/encrypted)"
python3 - "$BIN" <<'EOF'
import math, sys, re

def entropy(b):
    if not b:
        return 0.0
    freq = [0]*256
    for x in b:
        freq[x] += 1
    n = len(b)
    e = 0.0
    for c in freq:
        if c:
            p = c/n
            e -= p*math.log2(p)
    return e

data = open(sys.argv[1], 'rb').read()
print("whole file: %.2f" % entropy(data))
# crude section split via readelf-independent scan: report entropy in 4KB
# windows too, so packed regions stand out without parsing ELF headers
W = 4096
hi = []
for i in range(0, len(data), W):
    e = entropy(data[i:i+W])
    if e > 7.0:
        hi.append((i, e))
if hi:
    print("high-entropy windows (>7.0): %d of %d" % (len(hi), (len(data)+W-1)//W))
    for off, e in hi[:10]:
        print("  offset 0x%x: %.2f" % (off, e))
else:
    print("no windows above 7.0")
EOF

hr "strings of interest"
strings -n 6 "$BIN" | grep -aiE 'flag|ctf\{|key|passw|secret|token|correct|wrong|win|denied|license|serial|http|upx|\.dll|\.so' | sort -u | head -60 || true

hr "top strings sample"
strings -n 6 "$BIN" | head -40 || true

hr "hex around any flag-like token (first 3 matches)"
python3 - "$BIN" <<'EOF'
import sys
data = open(sys.argv[1], 'rb').read()
for pat in (b'flag', b'FLAG', b'key', b'passw'):
    i = data.find(pat)
    if i >= 0:
        print("0x%08x: %s" % (i, data[max(0,i-8):i+72].hex()))
EOF

hr "ldd (runs the loader — skip for untrusted binaries)"
ldd "$BIN" 2>/dev/null || echo "(ldd n/a or not ELF)"

hr "readelf -h (header)"
readelf -h "$BIN" 2>/dev/null || echo "(readelf n/a)"

hr "readelf -d (dynamic)"
readelf -d "$BIN" 2>/dev/null | grep -aE 'NEEDED|INTERP|RPATH|RUNPATH|FLAGS|RELRO' || echo "(static or not ELF)"

hr "readelf -s symbol counts + interesting symbols"
readelf -sW "$BIN" 2>/dev/null | awk 'NR>3 {c[$7]++} END {for (k in c) print c[k], k}' | sort -rn || true
readelf -sW "$BIN" 2>/dev/null | grep -aiE 'main|check|valid|license|flag|key|ptrace|(glbl|jni)' | head -30 || true

hr "sections (objdump -h)"
objdump -h "$BIN" 2>/dev/null || echo "(objdump n/a)"
