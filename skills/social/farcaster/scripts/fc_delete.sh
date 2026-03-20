#!/usr/bin/env bash
set -euo pipefail

# fc_delete.sh — Delete a Farcaster cast via Neynar v2 API

NEYNAR_BASE="https://api.neynar.com/v2/farcaster"
API_KEY="${NEYNAR_API_KEY:-}"
SIGNER="${NEYNAR_SIGNER_UUID:-}"
HASH=""

usage() {
  cat <<'EOF'
Usage: fc_delete.sh --hash "0xabcdef..."

Options:
  --hash HASH            Cast hash to delete (required)
  --api-key KEY          Neynar API key (or set NEYNAR_API_KEY)
  --signer UUID          Signer UUID (or set NEYNAR_SIGNER_UUID)
  -h, --help             Show this help

Example:
  fc_delete.sh --hash "0x71d5225f77e0164388b1d4c120825f3a2c1f131c"
EOF
  exit 0
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --hash) HASH="$2"; shift 2 ;;
    --api-key) API_KEY="$2"; shift 2 ;;
    --signer) SIGNER="$2"; shift 2 ;;
    -h|--help) usage ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

if [[ -z "$API_KEY" ]]; then
  echo '{"error":"NEYNAR_API_KEY not set."}' >&2; exit 1
fi
if [[ -z "$SIGNER" ]]; then
  echo '{"error":"NEYNAR_SIGNER_UUID not set."}' >&2; exit 1
fi
if [[ -z "$HASH" ]]; then
  echo '{"error":"--hash is required"}' >&2; exit 1
fi

BODY=$(jq -n --arg s "$SIGNER" --arg h "$HASH" '{signer_uuid: $s, target_hash: $h}')

RESP=$(curl -sS --connect-timeout 10 --max-time 30 -w "\n%{http_code}" -X DELETE "$NEYNAR_BASE/cast" \
  -H "x-api-key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d "$BODY")

HTTP_CODE=$(echo "$RESP" | tail -1)
RESP_BODY=$(echo "$RESP" | sed '$d')

if [[ "$HTTP_CODE" -ge 200 && "$HTTP_CODE" -lt 300 ]]; then
  echo '{"success":true,"deleted":"'"$HASH"'"}'
else
  echo "$RESP_BODY" | jq --argjson s "$HTTP_CODE" '. + {status: $s}' >&2
  exit 1
fi
