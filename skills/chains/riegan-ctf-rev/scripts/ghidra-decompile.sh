#!/usr/bin/env bash
# ghidra-decompile.sh — headless Ghidra decompile-to-C dump of a binary.
#
# Usage:
#   ghidra-decompile.sh <binary> [-o out.c]
#   ghidra-decompile.sh --help
#
# Requires: Ghidra installed (sudo pacman -S ghidra) and GHIDRA_INSTALL_DIR
# set (on this host typically /usr/share/ghidra — verify with
# `pacman -Ql ghidra | grep analyzeHeadless`). Ghidra >=10 runs the postScript
# under Jython; 11.x also supports PyGhidra — ghidra_dump.py is compatible
# with both.
set -euo pipefail

usage() {
    sed -n '2,11p' "$0" | sed 's/^# \{0,1\}//'
}

if [[ $# -lt 1 || "$1" == "--help" || "$1" == "-h" ]]; then
    usage
    exit 0
fi

BIN=$1
shift || true
OUT=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        -o) OUT=$2; shift 2 ;;
        *)   echo "unknown arg: $1" >&2; usage; exit 2 ;;
    esac
done

if [[ ! -f "$BIN" ]]; then
    echo "no such file: $BIN" >&2
    exit 1
fi

if [[ -z "${GHIDRA_INSTALL_DIR:-}" ]]; then
    for cand in /usr/share/ghidra /opt/ghidra; do
        [[ -x "$cand/support/analyzeHeadless" ]] && export GHIDRA_INSTALL_DIR=$cand
    done
    if [[ -z "${GHIDRA_INSTALL_DIR:-}" ]]; then
        echo "GHIDRA_INSTALL_DIR not set and no Ghidra under /usr/share/ghidra or /opt/ghidra." >&2
        echo "Install: sudo pacman -S ghidra ; export GHIDRA_INSTALL_DIR=/usr/share/ghidra" >&2
        exit 1
    fi
fi

HEADLESS="$GHIDRA_INSTALL_DIR/support/analyzeHeadless"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJ_DIR=$(mktemp -d -t ghidra-proj-XXXXXX)
PROJ_NAME=ctfdump
trap 'rm -rf "$PROJ_DIR"' EXIT

# Analyze, run dump script, delete project. Script writes to $OUT if given,
# else prints decompiled C on stdout (redirect to capture).
if [[ -n "$OUT" ]]; then
    "$HEADLESS" "$PROJ_DIR" "$PROJ_NAME" \
        -import "$BIN" \
        -scriptPath "$SCRIPT_DIR" \
        -postScript ghidra_dump.py "$OUT" \
        -deleteProject >/dev/null
    echo "decompiled C written to $OUT" >&2
else
    "$HEADLESS" "$PROJ_DIR" "$PROJ_NAME" \
        -import "$BIN" \
        -scriptPath "$SCRIPT_DIR" \
        -postScript ghidra_dump.py \
        -deleteProject
fi
