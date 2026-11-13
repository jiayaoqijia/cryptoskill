#!/usr/bin/env bash
# Dump the live Koinju ClickHouse schema (database = api) over HTTPS.
# Read-only: DESCRIBE TABLE, SHOW CREATE TABLE, SELECT FROM system.tables.
#
# Use this to verify the bundled references (data-tables.md etc.) against
# reality, or to discover columns before writing a query. Run it whenever
# a query fails with "Unknown table" or "Unknown column".
#
# IMPORTANT: DESCRIBE returns ZERO columns for a *parameterized view* (e.g.
# api.ohlcv, which takes `candle_duration_in_minutes`). That does NOT mean the
# table is missing. For those, this script falls back to SHOW CREATE TABLE to
# surface the {param:Type} signature and prints how to query it. It never emits
# a bare empty column list under a header.
#
# Usage:
#   bash probe-schema.sh                # dump all api.* tables and columns
#   bash probe-schema.sh <table>        # dump columns for one table only

set -u

# Auto-source .koinju.env (project) then ~/.koinju.env (global) — same as helpers
# shellcheck disable=SC1091
[ -f .koinju.env ] && source .koinju.env 2>/dev/null || true
# shellcheck disable=SC1091
[ -f "$HOME/.koinju.env" ] && source "$HOME/.koinju.env" 2>/dev/null || true

for v in KOINJU_DB_HOST KOINJU_DB_USER KOINJU_DB_PASSWORD; do
    if [ -z "${!v:-}" ]; then
        echo "[probe-schema] missing $v — set in .koinju.env or ~/.koinju.env" >&2
        exit 1
    fi
done

# Normalize host (strip scheme / path / port if user pasted a full URL)
HOST="$KOINJU_DB_HOST"
HOST="${HOST#https://}"
HOST="${HOST#http://}"
HOST="${HOST%%/*}"
case "$HOST" in
    *:*[0-9]) HOST="${HOST%:*}" ;;
esac
PORT="${KOINJU_DB_PORT:-8443}"
DB="${KOINJU_DB_DATABASE:-api}"

# Base64 for HTTP basic auth (BSD and GNU compatible)
AUTH=$(printf '%s' "$KOINJU_DB_USER:$KOINJU_DB_PASSWORD" | base64 | tr -d '\n')
URL="https://$HOST:$PORT/"

run_q() {
    local sql="$1"
    curl -sS -H "Authorization: Basic $AUTH" -H "X-ClickHouse-Database: $DB" \
        --data-binary "$sql" "$URL"
}

# Print the columns of one object, handling parameterized views.
describe_one() {
    local t="$1" cols create params pname
    cols=$(run_q "DESCRIBE TABLE $DB.$t FORMAT TSV")

    if [ -n "$cols" ] && ! printf '%s' "$cols" | grep -qiE 'DB::Exception|Code: [0-9]+'; then
        printf '%s\n' "$cols" | awk -F'\t' '{printf "  %-32s %s\n", $1, $2}'
        return
    fi

    # Empty (or error) DESCRIBE → parameterized view in ClickHouse. NOT missing.
    echo "  NOTE: DESCRIBE returns no columns — this is a PARAMETERIZED VIEW, not a missing table."
    create=$(run_q "SHOW CREATE TABLE $DB.$t FORMAT TSVRaw")
    params=$(printf '%s' "$create" \
        | grep -oE '\{[[:space:]]*[A-Za-z_][A-Za-z0-9_]*[[:space:]]*:[[:space:]]*[A-Za-z0-9()]+[[:space:]]*\}' \
        | tr -d ' ' | sort -u | tr '\n' ' ')
    pname=$(printf '%s' "$create" \
        | grep -oE '\{[[:space:]]*[A-Za-z_][A-Za-z0-9_]*[[:space:]]*:' | head -1 | tr -d ' {:')
    [ -n "$params" ] && echo "  parameter(s): $params"
    if [ -n "$pname" ]; then
        echo "  query it:     SELECT * FROM $DB.$t($pname = <value>) WHERE ... LIMIT 10"
        echo "  columns via:  DESCRIBE (SELECT * FROM $DB.$t($pname = <value>) LIMIT 0)"
    fi
    echo "  full def:     SHOW CREATE TABLE $DB.$t"
}

if [ $# -ge 1 ]; then
    # One-table mode
    TBL="$1"
    echo "=== columns of $DB.$TBL ==="
    describe_one "$TBL"
    exit 0
fi

echo "=== tables in $DB ==="
TABLES=$(run_q "SELECT name FROM system.tables WHERE database = '$DB' ORDER BY name FORMAT TSV")
echo "$TABLES" | sed 's/^/  /'
echo

for t in $TABLES; do
    echo "--- $DB.$t ---"
    describe_one "$t"
    echo
done
