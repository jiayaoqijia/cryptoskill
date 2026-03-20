#!/usr/bin/env bash
set -euo pipefail

# fc_user.sh — Look up Farcaster users via Neynar v2 API
# Supports: by username, by FID, by ETH address, bulk by FIDs.

NEYNAR_BASE="https://api.neynar.com/v2/farcaster"
API_KEY="${NEYNAR_API_KEY:-}"
USERNAME=""
FID=""
ADDRESS=""
FIDS=""

usage() {
  cat <<'EOF'
Usage: fc_user.sh [options]

Lookup methods (pick one):
  --username NAME        Look up by Farcaster username
  --fid FID              Look up by FID
  --address ADDR         Look up by verified ETH address
  --fids "1,2,3"         Bulk lookup by comma-separated FIDs (max 100)

Options:
  --api-key KEY          Neynar API key (or set NEYNAR_API_KEY)
  -h, --help             Show this help

Examples:
  fc_user.sh --username "dwr"
  fc_user.sh --fid 3
  fc_user.sh --address "0x1234..."
  fc_user.sh --fids "3,194,6131"
EOF
  exit 0
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --username) USERNAME="$2"; shift 2 ;;
    --fid) FID="$2"; shift 2 ;;
    --address) ADDRESS="$2"; shift 2 ;;
    --fids) FIDS="$2"; shift 2 ;;
    --api-key) API_KEY="$2"; shift 2 ;;
    -h|--help) usage ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

if [[ -z "$API_KEY" ]]; then
  echo '{"error":"NEYNAR_API_KEY not set. Use --api-key or export NEYNAR_API_KEY."}' >&2
  exit 1
fi

HEADERS=(-H "x-api-key: $API_KEY")

format_user() {
  jq '{
    fid, username, display_name,
    bio: .profile.bio.text,
    pfp_url,
    follower_count, following_count,
    verified_eth: [.verified_addresses.eth_addresses[]?],
    verified_sol: [.verified_addresses.sol_addresses[]?],
    score,
    registered_at
  }'
}

if [[ -n "$USERNAME" ]]; then
  URL="$NEYNAR_BASE/user/by_username?username=$USERNAME"
  RESP=$(curl -sS --connect-timeout 10 --max-time 30 -w "\n%{http_code}" "$URL" "${HEADERS[@]}")
  HTTP_CODE=$(echo "$RESP" | tail -1)
  RESP_BODY=$(echo "$RESP" | sed '$d')

  if [[ "$HTTP_CODE" -ge 200 && "$HTTP_CODE" -lt 300 ]]; then
    echo "$RESP_BODY" | jq '.user' | format_user
  else
    echo "$RESP_BODY" | jq --argjson s "$HTTP_CODE" '. + {status: $s}' >&2; exit 1
  fi

elif [[ -n "$FIDS" ]]; then
  URL="$NEYNAR_BASE/user/bulk?fids=$FIDS"
  RESP=$(curl -sS --connect-timeout 10 --max-time 30 -w "\n%{http_code}" "$URL" "${HEADERS[@]}")
  HTTP_CODE=$(echo "$RESP" | tail -1)
  RESP_BODY=$(echo "$RESP" | sed '$d')

  if [[ "$HTTP_CODE" -ge 200 && "$HTTP_CODE" -lt 300 ]]; then
    echo "$RESP_BODY" | jq '[.users[] | {
      fid, username, display_name,
      bio: .profile.bio.text,
      pfp_url,
      follower_count, following_count,
      verified_eth: [.verified_addresses.eth_addresses[]?],
      score
    }]'
  else
    echo "$RESP_BODY" | jq --argjson s "$HTTP_CODE" '. + {status: $s}' >&2; exit 1
  fi

elif [[ -n "$FID" ]]; then
  URL="$NEYNAR_BASE/user/bulk?fids=$FID"
  RESP=$(curl -sS --connect-timeout 10 --max-time 30 -w "\n%{http_code}" "$URL" "${HEADERS[@]}")
  HTTP_CODE=$(echo "$RESP" | tail -1)
  RESP_BODY=$(echo "$RESP" | sed '$d')

  if [[ "$HTTP_CODE" -ge 200 && "$HTTP_CODE" -lt 300 ]]; then
    echo "$RESP_BODY" | jq '.users[0]' | format_user
  else
    echo "$RESP_BODY" | jq --argjson s "$HTTP_CODE" '. + {status: $s}' >&2; exit 1
  fi

elif [[ -n "$ADDRESS" ]]; then
  URL="$NEYNAR_BASE/user/bulk-by-address?addresses=$ADDRESS"
  RESP=$(curl -sS --connect-timeout 10 --max-time 30 -w "\n%{http_code}" "$URL" "${HEADERS[@]}")
  HTTP_CODE=$(echo "$RESP" | tail -1)
  RESP_BODY=$(echo "$RESP" | sed '$d')

  if [[ "$HTTP_CODE" -ge 200 && "$HTTP_CODE" -lt 300 ]]; then
    # Response keyed by address
    echo "$RESP_BODY" | jq --arg a "$ADDRESS" '
      (.[$a] // [(.[] | .[])]) | .[0] // empty |
      {
        fid, username, display_name,
        bio: .profile.bio.text,
        pfp_url,
        follower_count, following_count,
        verified_eth: [.verified_addresses.eth_addresses[]?],
        score
      }
    '
  else
    echo "$RESP_BODY" | jq --argjson s "$HTTP_CODE" '. + {status: $s}' >&2; exit 1
  fi

else
  echo '{"error":"Specify one of: --username, --fid, --fids, --address"}' >&2
  exit 1
fi
