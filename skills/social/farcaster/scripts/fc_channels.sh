#!/usr/bin/env bash
set -euo pipefail

# fc_channels.sh — List, search, and look up Farcaster channels via Neynar v2 API

NEYNAR_BASE="https://api.neynar.com/v2/farcaster"
API_KEY="${NEYNAR_API_KEY:-}"
SEARCH=""
CHANNEL_ID=""
TRENDING=false
LIMIT=10

usage() {
  cat <<'EOF'
Usage: fc_channels.sh [options]

Actions (pick one):
  --search KEYWORD       Search channels by name/description
  --id CHANNEL_ID        Get channel details by ID (e.g. "base")
  --trending             List trending channels

Options:
  --limit N              Number of results (default 10)
  --api-key KEY          Neynar API key (or set NEYNAR_API_KEY)
  -h, --help             Show this help

Examples:
  fc_channels.sh --search "defi"
  fc_channels.sh --id "base"
  fc_channels.sh --trending --limit 20
EOF
  exit 0
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --search) SEARCH="$2"; shift 2 ;;
    --id) CHANNEL_ID="$2"; shift 2 ;;
    --trending) TRENDING=true; shift ;;
    --limit) LIMIT="$2"; shift 2 ;;
    --api-key) API_KEY="$2"; shift 2 ;;
    -h|--help) usage ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

if [[ -z "$API_KEY" ]]; then
  echo '{"error":"NEYNAR_API_KEY not set."}' >&2; exit 1
fi

HEADERS=(-H "x-api-key: $API_KEY")

if [[ -n "$CHANNEL_ID" ]]; then
  URL="$NEYNAR_BASE/channel?id=$CHANNEL_ID"
  RESP=$(curl -sS --connect-timeout 10 --max-time 30 -w "\n%{http_code}" "$URL" "${HEADERS[@]}")
  HTTP_CODE=$(echo "$RESP" | tail -1)
  RESP_BODY=$(echo "$RESP" | sed '$d')

  if [[ "$HTTP_CODE" -ge 200 && "$HTTP_CODE" -lt 300 ]]; then
    echo "$RESP_BODY" | jq '.channel | {
      id, name, description,
      image_url,
      follower_count,
      created_at,
      lead: .lead.username,
      url
    }'
  else
    echo "$RESP_BODY" | jq --argjson s "$HTTP_CODE" '. + {status: $s}' >&2; exit 1
  fi

elif [[ -n "$SEARCH" ]]; then
  ENCODED=$(python3 -c 'import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))' "$SEARCH" 2>/dev/null || echo "$SEARCH")
  URL="$NEYNAR_BASE/channel/search?q=$ENCODED&limit=$LIMIT"
  RESP=$(curl -sS --connect-timeout 10 --max-time 30 -w "\n%{http_code}" "$URL" "${HEADERS[@]}")
  HTTP_CODE=$(echo "$RESP" | tail -1)
  RESP_BODY=$(echo "$RESP" | sed '$d')

  if [[ "$HTTP_CODE" -ge 200 && "$HTTP_CODE" -lt 300 ]]; then
    echo "$RESP_BODY" | jq '[.channels[] | {
      id, name, description: .description[0:100],
      follower_count, image_url
    }]'
  else
    echo "$RESP_BODY" | jq --argjson s "$HTTP_CODE" '. + {status: $s}' >&2; exit 1
  fi

elif [[ "$TRENDING" == "true" ]]; then
  URL="$NEYNAR_BASE/channel/trending?time_window=7d&limit=$LIMIT"
  RESP=$(curl -sS --connect-timeout 10 --max-time 30 -w "\n%{http_code}" "$URL" "${HEADERS[@]}")
  HTTP_CODE=$(echo "$RESP" | tail -1)
  RESP_BODY=$(echo "$RESP" | sed '$d')

  if [[ "$HTTP_CODE" -ge 200 && "$HTTP_CODE" -lt 300 ]]; then
    echo "$RESP_BODY" | jq '[.channels[] | {
      id: .channel.id, name: .channel.name,
      description: .channel.description[0:100],
      follower_count: .channel.follower_count
    }]'
  else
    echo "$RESP_BODY" | jq --argjson s "$HTTP_CODE" '. + {status: $s}' >&2; exit 1
  fi

else
  echo '{"error":"Specify one of: --search, --id, --trending"}' >&2
  exit 1
fi
