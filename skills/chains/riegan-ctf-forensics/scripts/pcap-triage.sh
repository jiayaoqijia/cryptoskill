#!/usr/bin/env bash
# pcap-triage.sh — one-shot tshark triage of a pcap/pcapng capture.
#
# Usage:   pcap-triage.sh <capture.pcap>
# Output:  pcap-triage-<name>/ next to the capture:
#            capinfos.txt   capture metadata (if capinfos present)
#            phs.txt        protocol hierarchy
#            conv.txt       ip/tcp/udp conversations
#            http.txt       HTTP request summary
#            dns.txt        top DNS query names (exfil patterns)
#            streams.txt    followed TCP streams (first 50, ascii)
#            extracted/     exported http + imf objects
#            flags.txt      flag-regex hits (raw file, strings, outputs)
#          Without tshark the script degrades to strings + flag grep and
#          tells you how to install it.
# Canonical flag regex lives in the ctf router skill; the one here is the
# generic fallback.
set -euo pipefail

usage() {
    sed -n '2,17p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
    exit "${1:-0}"
}

case "${1:-}" in
    -h|--help) usage 0 ;;
esac
[ $# -eq 1 ] || usage 1
pcap=$1
[ -f "$pcap" ] || { echo "not a file: $pcap" >&2; exit 1; }
pcap=$(realpath "$pcap")
FLAG_RE='(flag|FLAG|ctf|CTF|picoCTF|HTB)\{[^}]{4,}\}'
WRAP_RE='[a-zA-Z0-9_]{2,16}\{[^}]{4,}\}'

stem=$(basename "$pcap"); stem=${stem%.*}
outdir=$(dirname "$pcap")/pcap-triage-$stem
mkdir -p "$outdir/extracted"
cd "$outdir"

echo "== pcap-triage: $pcap -> $outdir"

if ! command -v tshark >/dev/null 2>&1; then
    echo "tshark not found — install with: sudo pacman -S wireshark-cli" >&2
    echo "falling back to strings + flag grep" >&2
    { strings -n 6 "$pcap" | grep -aE "$FLAG_RE|$WRAP_RE"; } > flags.txt 2>/dev/null || true
    echo "flag candidates: $(wc -l < flags.txt) (see $outdir/flags.txt)"
    exit 0
fi

echo "-- capture info"
capinfos -u -a -e -d -c "$pcap" > capinfos.txt 2>&1 || true
cat capinfos.txt

echo "-- protocol hierarchy / conversations"
tshark -r "$pcap" -q -z io,phs > phs.txt 2>&1 || true
tshark -r "$pcap" -q -z conv,ip -z conv,tcp -z conv,udp > conv.txt 2>&1 || true
cat phs.txt conv.txt

echo "-- HTTP requests"
tshark -r "$pcap" -Y http.request -T fields \
    -e frame.number -e ip.src -e http.request.method \
    -e http.host -e http.request.uri -e http.user_agent \
    > http.txt 2>&1 || true
cat http.txt

echo "-- DNS top queries"
tshark -r "$pcap" -Y 'dns.flags.response == 0' -T fields -e dns.qry.name 2>/dev/null \
    | sort | uniq -c | sort -rn | head -30 > dns.txt || true
cat dns.txt

echo "-- exporting objects (http, imf)"
tshark -r "$pcap" --export-objects http,extracted/ >/dev/null 2>&1 || true
tshark -r "$pcap" --export-objects imf,extracted/ >/dev/null 2>&1 || true
find extracted -type f | sed 's|^|  |'

echo "-- following TCP streams"
: > streams.txt
for s in $(tshark -r "$pcap" -T fields -e tcp.stream 2>/dev/null | sort -un | head -50); do
    {
        echo "===== tcp.stream $s ====="
        tshark -r "$pcap" -q -z follow,tcp,ascii,"$s" 2>/dev/null
    } >> streams.txt
done
echo "streams dumped: $(grep -c '^===== ' streams.txt)"

echo "-- flag hunt (regex over raw capture, strings, and all outputs)"
{
    echo "# raw-file hits:"
    grep -aoE "$FLAG_RE" "$pcap" | sort -u
    echo "# strings hits:"
    strings -n 6 "$pcap" | grep -aE "$FLAG_RE|$WRAP_RE" | sort -u
    echo "# output-file hits:"
    grep -ahE "$FLAG_RE|$WRAP_RE" capinfos.txt phs.txt conv.txt http.txt dns.txt streams.txt 2>/dev/null | sort -u
} > flags.txt 2>/dev/null || true
cat flags.txt

echo "== done: $outdir (extracted/, streams.txt, flags.txt)"
