#!/usr/bin/env bash
# checker-wrap.sh — run an organizer checker/bot against a service and emit
# one SLA verdict line. Two uses:
#   * pre-deploy gate: patched service must be OK locally before shipping
#   * per-tick monitoring: verdicts.log feeds the alert-on-2-fails check
#
# Usage: checker-wrap.sh [-t SECONDS] [-n NAME] [-o OUTDIR] [--] <checker cmd...>
#   -t SECONDS  hard timeout for the checker run (default 30)
#   -n NAME     service name in the verdict line (default: derived from the
#               command — set it explicitly for curl-style checks)
#   -o OUTDIR   dir for verdicts.log + failures/ (default: ./monitor)
#
# Verdict line (append-only, OUTDIR/verdicts.log):
#   <ISO8601> <NAME> <OK|FAIL|INFRA> rc=<n> t=<sec.ms>s <first line of output>
# Exit codes: 0 = OK    (SLA holds)
#             1 = FAIL  (checker says the service is broken — or too slow)
#             2 = INFRA (the checker command could not be executed at all —
#                 fix the wrapper call; do NOT count as an SLA failure)
# Note: an interpreter that starts but dies on its own bad path (e.g.
# `python3 missing.py`) exits non-zero and reports FAIL — check failures/
# before paging anyone.

set -u

T=30
NAME=""
OUT="monitor"

usage() {
    cat <<'EOF'
checker-wrap.sh — run a checker against a service, emit an SLA verdict line.

Usage: checker-wrap.sh [-t SECONDS] [-n NAME] [-o OUTDIR] [--] <checker cmd...>
  -t SECONDS  hard timeout for the checker run (default 30)
  -n NAME     service name in the verdict line (default: derived; set it
              explicitly for curl-style checks)
  -o OUTDIR   dir for verdicts.log + failures/ (default: ./monitor)

Verdict line: <ISO8601> <NAME> <OK|FAIL|INFRA> rc=<n> t=<sec.ms>s <summary>
Exit codes: 0 OK (SLA holds) | 1 FAIL (service broken/slow) | 2 INFRA
            (checker command itself could not run)
EOF
}

case "${1-}" in
    -h|--help) usage; exit 0 ;;
esac

while getopts ":t:n:o:h" opt; do
    case "$opt" in
        t) T=$OPTARG ;;
        n) NAME=$OPTARG ;;
        o) OUT=$OPTARG ;;
        h) usage; exit 0 ;;
        :) echo "checker-wrap.sh: -$OPTARG needs a value" >&2; usage >&2; exit 2 ;;
        \?) echo "checker-wrap.sh: unknown option -$OPTARG" >&2; usage >&2; exit 2 ;;
    esac
done
shift $((OPTIND - 1))
if [ "$1" = "--" ]; then
    shift
fi
if [ $# -lt 1 ]; then
    echo "checker-wrap.sh: no checker command given" >&2
    usage >&2
    exit 2
fi
case "$T" in (*[!0-9]*|'') echo "checker-wrap.sh: -t must be a number" >&2; exit 2 ;; esac

# Default name: first *.py/*.sh/*.pl argument looks like the checker script;
# otherwise the basename of the command word.
if [ -z "$NAME" ]; then
    NAME=$(basename -- "$1")
    for a in "$@"; do
        case "$a" in
            *.py|*.sh|*.pl) NAME=$(basename -- "$a"); break ;;
        esac
    done
fi

mkdir -p "$OUT/failures"
OUTFILE=$(mktemp)
trap 'rm -f "$OUTFILE"' EXIT

START=$(date +%s%3N)
timeout "$T" "$@" >"$OUTFILE" 2>&1
RC=$?
MS=$(( $(date +%s%3N) - START ))
DUR="$((MS / 1000)).$(printf '%03d' $((MS % 1000)))"
STAMP=$(date -Is)
SUMMARY=$(tr -d '\n' <"$OUTFILE" | cut -c1-100)
[ -n "$SUMMARY" ] || SUMMARY="-"

case "$RC" in
    0)   VERDICT=OK ;;
    124) VERDICT=FAIL; SUMMARY="checker timeout after ${T}s" ;;
    125|126|127)
         VERDICT=INFRA; SUMMARY="checker did not run (rc=$RC): $SUMMARY" ;;
    *)   VERDICT=FAIL ;;
esac

echo "$STAMP $NAME $VERDICT rc=$RC t=${DUR}s $SUMMARY" | tee -a "$OUT/verdicts.log"
if [ "$VERDICT" != "OK" ]; then
    cp "$OUTFILE" "$OUT/failures/${NAME}-$(date +%s%3N).log"
fi

case "$VERDICT" in
    OK) exit 0 ;;
    FAIL) exit 1 ;;
    *) exit 2 ;;
esac
