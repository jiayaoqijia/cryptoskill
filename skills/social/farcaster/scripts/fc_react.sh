#!/usr/bin/env bash
set -euo pipefail

# fc_react.sh — Like or recast on Farcaster via Neynar v2 API

NEYNAR_BASE="https://api.neynar.com/v2/farcaster"
API_KEY="${NEYNAR_API_KEY:-}"
SIGNER="${NEYNAR_SIGNER_UUID:-}"
LIKE_HASH=""
RECAST_HASH=""
UNDO=false

usage() {
  cat <<'EOF'
Usage: fc_react.sh [options]

Actions (pick one):
  --like HASH            Like a cast by hash
  --recast HASH          Recast a cast by hash

Modifiers:
  --undo                 Remove the like/recast instead of adding

Options:
  --api-key KEY          Neynar API key (or set NEYNAR_API_KEY)
  --signer UUID          Signer UUID (or set NEYNAR_SIGNER_UUID)
  -h, --help             Show this help

Examples:
  fc_react.sh --like "0xabcdef..."
  fc_react.sh --like "0xabcdef..." --undo
  fc_react.sh --recast "0xabcdef..."
EOF
  exit 0
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --like) LIKE_HASH="$2"; shift 2 ;;
    --recast) RECAST_HASH="$2"; shift 2 ;;
    --undo) UNDO=true; shift ;;
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

HEADERS=(-H "x-api-key: $API_KEY" -H "Content-Type: application/json")

if [[ -n "$LIKE_HASH" ]]; then
  ENDPOINT="$NEYNAR_BASE/reaction"
  BODY=$(jq -n --arg s "$SIGNER" --arg h "$LIKE_HASH" '{signer_uuid: $s, reaction_type: "like", target: $h}')

  if [[ "$UNDO" == "true" ]]; then
    METHOD="-X DELETE"
  else
    METHOD="-X POST"
  fi

elif [[ -n "$RECAST_HASH" ]]; then
  ENDPOINT="$NEYNAR_BASE/reaction"
  BODY=$(jq -n --arg s "$SIGNER" --arg h "$RECAST_HASH" '{signer_uuid: $s, reaction_type: "recast", target: $h}')

  if [[ "$UNDO" == "true" ]]; then
    METHOD="-X DELETE"
  else
    METHOD="-X POST"
  fi

else
  echo '{"error":"Specify --like or --recast with a cast hash"}' >&2
  exit 1
fi

RESP=$(curl -sS --connect-timeout 10 --max-time 30 -w "\n%{http_code}" $METHOD "$ENDPOINT" "${HEADERS[@]}" -d "$BODY")
HTTP_CODE=$(echo "$RESP" | tail -1)
RESP_BODY=$(echo "$RESP" | sed '$d')

if [[ "$HTTP_CODE" -ge 200 && "$HTTP_CODE" -lt 300 ]]; then
  ACTION="liked"
  [[ -n "$RECAST_HASH" ]] && ACTION="recasted"
  [[ "$UNDO" == "true" ]] && ACTION="un${ACTION}"
  echo "$RESP_BODY" | jq --arg a "$ACTION" '{success: .success, action: $a}'
else
  echo "$RESP_BODY" | jq --argjson s "$HTTP_CODE" '. + {status: $s}' >&2
  exit 1
fi
