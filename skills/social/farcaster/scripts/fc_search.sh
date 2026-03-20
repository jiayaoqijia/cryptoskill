#!/usr/bin/env bash
set -euo pipefail

# fc_search.sh — Search Farcaster casts via Neynar v2 API

NEYNAR_BASE="https://api.neynar.com/v2/farcaster"
API_KEY="${NEYNAR_API_KEY:-}"
QUERY=""
AUTHOR_FID=""
CHANNEL=""
LIMIT=10
CURSOR=""

usage() {
  cat <<'EOF'
Usage: fc_search.sh --query "keyword" [options]

Options:
  --query TEXT           Search query (required)
  --author-fid FID       Filter by author FID
  --channel ID           Filter by channel
  --limit N              Number of results (default 10, max 100)
  --cursor TOKEN         Pagination cursor
  --api-key KEY          Neynar API key (or set NEYNAR_API_KEY)
  -h, --help             Show this help

Examples:
  fc_search.sh --query "base chain"
  fc_search.sh --query "ethereum" --author-fid 3 --limit 5
  fc_search.sh --query "gm" --channel "base"
EOF
  exit 0
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --query) QUERY="$2"; shift 2 ;;
    --author-fid) AUTHOR_FID="$2"; shift 2 ;;
    --channel) CHANNEL="$2"; shift 2 ;;
    --limit) LIMIT="$2"; shift 2 ;;
    --cursor) CURSOR="$2"; shift 2 ;;
    --api-key) API_KEY="$2"; shift 2 ;;
    -h|--help) usage ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

if [[ -z "$API_KEY" ]]; then
  echo '{"error":"NEYNAR_API_KEY not set. Use --api-key or export NEYNAR_API_KEY."}' >&2
  exit 1
fi
if [[ -z "$QUERY" ]]; then
  echo '{"error":"--query is required"}' >&2
  exit 1
fi

HEADERS=(-H "x-api-key: $API_KEY")

# URL-encode query
ENCODED_QUERY=$(python3 -c 'import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))' "$QUERY" 2>/dev/null || echo "$QUERY")

URL="$NEYNAR_BASE/cast/search?q=$ENCODED_QUERY&limit=$LIMIT"
[[ -n "$AUTHOR_FID" ]] && URL="$URL&author_fid=$AUTHOR_FID"
[[ -n "$CHANNEL" ]] && URL="$URL&channel_id=$CHANNEL"
[[ -n "$CURSOR" ]] && URL="$URL&cursor=$CURSOR"

RESP=$(curl -sS --connect-timeout 10 --max-time 30 -w "\n%{http_code}" "$URL" "${HEADERS[@]}")
HTTP_CODE=$(echo "$RESP" | tail -1)
RESP_BODY=$(echo "$RESP" | sed '$d')

if [[ "$HTTP_CODE" -ge 200 && "$HTTP_CODE" -lt 300 ]]; then
  echo "$RESP_BODY" | jq '{
    casts: [.result.casts[] | {
      hash, text, timestamp,
      author: {fid: .author.fid, username: .author.username, display_name: .author.display_name},
      embeds: [.embeds[]? | .url // .cast.hash],
      reactions: {likes: .reactions.likes_count, recasts: .reactions.recasts_count},
      replies: .replies.count
    }],
    next_cursor: .next.cursor
  }'
else
  echo "$RESP_BODY" | jq --argjson s "$HTTP_CODE" '. + {status: $s}' >&2
  exit 1
fi
