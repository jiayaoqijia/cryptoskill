#!/usr/bin/env bash
# recon.sh - phased nmap wrapper for boot2root boxes.
# Usage: recon.sh <target> [ports]     (comma-separated port list skips phase 1)
#        recon.sh --help
# Phases: 1) full TCP port sweep (-p- --min-rate 2000)
#         2) -sV -sC service/script scan on found ports
#         (3) UDP top-50 is printed as a hint, not run: needs root and time)
# Output: nmap/allports.{nmap,gnmap,xml} and nmap/enumerate.* in cwd.
# Authorized targets only (see ctf router remote gate).
set -euo pipefail

usage() {
    sed -n '2,8p' "$0"; exit 0
}
case "${1:-}" in --help|-h) usage ;; esac
[ $# -ge 1 ] && [ $# -le 2 ] || { echo "usage: recon.sh <target> [ports]" >&2; exit 2; }

target=$1
outdir=nmap
mkdir -p "$outdir"

# nmap -sS needs root; use it when passwordless sudo works, else -sT.
scan_tcp_flag="-sT"
SUDO=
if [ "$(id -u)" -eq 0 ]; then
    scan_tcp_flag="-sS"
elif sudo -n true 2>/dev/null; then
    scan_tcp_flag="-sS"   # phases below then run under sudo
    SUDO=sudo
else
    echo "note: no root and no passwordless sudo -> using -sT connect scan (noisier, no SYN stealth)" >&2
    SUDO=
fi

ports=${2:-}
if [ -z "$ports" ]; then
    $SUDO nmap $scan_tcp_flag -p- --min-rate 2000 -oA "$outdir/allports" "$target"
    ports=$(grep -oE '[0-9]+/open/' "$outdir/allports.gnmap" | cut -d/ -f1 | paste -sd, -)
    [ -n "$ports" ] || { echo "no open TCP ports found" >&2; exit 1; }
else
    echo "[*] skipping phase 1 (ports given)"
fi
echo "[*] open TCP ports: $ports"

echo "[*] phase 2: service/version + default scripts on $ports"
$SUDO nmap $scan_tcp_flag -sV -sC -p "$ports" -oA "$outdir/enumerate" "$target"

echo "[*] summary"
awk '/^[0-9]+\/tcp/ {print}' "$outdir/enumerate.nmap" || true
echo "[hint] UDP pass (root, slow): nmap -sU --top-ports 50 -oA $outdir/udp $target"
