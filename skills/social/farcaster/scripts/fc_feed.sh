#!/usr/bin/env bash
set -euo pipefail

# fc_feed.sh — Read Farcaster feeds via Neynar v2 API
# Supports: user casts, channel feed, following feed, thread/replies.

NEYNAR_BASE="https://api.neynar.com/v2/farcaster"
API_KEY="${NEYNAR_API_KEY:-}"
FID=""
USERNAME=""
CHANNEL=""
FOLLOWING=false
THREAD=""
LIMIT=10
CURSOR=""

usage() {
  cat <<'EOF'
Usage: fc_feed.sh [options]

Feed types (pick one):
  --fid FID              User's casts by FID
  --username NAME        User's casts by username (resolves to FID)
  --channel ID           Channel feed (e.g. "base")
  --following             Following feed (requires --fid)
  --thread HASH          Thread/replies for a cast hash

Options:
  --limit N              Number of casts (default 10, max 100)
  --cursor TOKEN         Pagination cursor from previous response
  --api-key KEY          Neynar API key (or set NEYNAR_API_KEY)
  -h, --help             Show this help

Examples:
  fc_feed.sh --fid 3 --limit 5
  fc_feed.sh --username "vitalik" --limit 10
  fc_feed.sh --channel "base" --limit 20
  fc_feed.sh --thread "0xabc123..."
EOF
  exit 0
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --fid) FID="$2"; shift 2 ;;
    --username) USERNAME="$2"; shift 2 ;;
    --channel) CHANNEL="$2"; shift 2 ;;
    --following) FOLLOWING=true; shift ;;
    --thread) THREAD="$2"; shift 2 ;;
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

HEADERS=(-H "x-api-key: $API_KEY")

# Resolve username to FID if needed
if [[ -n "$USERNAME" && -z "$FID" ]]; then
  USER_RESP=$(curl -sS --connect-timeout 10 --max-time 30 "$NEYNAR_BASE/user/by_username?username=$USERNAME" "${HEADERS[@]}")
  FID=$(echo "$USER_RESP" | jq -r '.user.fid // empty')
  if [[ -z "$FID" ]]; then
    echo '{"error":"Could not resolve username to FID","username":"'"$USERNAME"'"}' >&2
    exit 1
  fi
fi

# Build URL based on feed type
if [[ -n "$THREAD" ]]; then
  URL="$NEYNAR_BASE/cast/conversation?identifier=$THREAD&type=hash&reply_depth=2&include_chronological_parent_casts=false&limit=$LIMIT"
  [[ -n "$CURSOR" ]] && URL="$URL&cursor=$CURSOR"

elif [[ -n "$CHANNEL" ]]; then
  URL="$NEYNAR_BASE/feed/channels?channel_ids=$CHANNEL&limit=$LIMIT&with_recasts=true"
  [[ -n "$CURSOR" ]] && URL="$URL&cursor=$CURSOR"

elif [[ "$FOLLOWING" == "true" ]]; then
  if [[ -z "$FID" ]]; then
    echo '{"error":"--following requires --fid"}' >&2
    exit 1
  fi
  URL="$NEYNAR_BASE/feed?feed_type=following&fid=$FID&limit=$LIMIT&with_recasts=true"
  [[ -n "$CURSOR" ]] && URL="$URL&cursor=$CURSOR"

elif [[ -n "$FID" ]]; then
  URL="$NEYNAR_BASE/feed/user/casts?fid=$FID&limit=$LIMIT&include_replies=false"
  [[ -n "$CURSOR" ]] && URL="$URL&cursor=$CURSOR"

else
  echo '{"error":"Specify one of: --fid, --username, --channel, --following, --thread"}' >&2
  exit 1
fi

RESP=$(curl -sS --connect-timeout 10 --max-time 30 -w "\n%{http_code}" "$URL" "${HEADERS[@]}")
HTTP_CODE=$(echo "$RESP" | tail -1)
RESP_BODY=$(echo "$RESP" | sed '$d')

if [[ "$HTTP_CODE" -ge 200 && "$HTTP_CODE" -lt 300 ]]; then
  # Normalize output: extract casts array + cursor
  if [[ -n "$THREAD" ]]; then
    echo "$RESP_BODY" | jq '{
      casts: [.conversation.cast] + (.conversation.cast.direct_replies // [])
        | map({
            hash, text, timestamp,
            author: {fid: .author.fid, username: .author.username, display_name: .author.display_name},
            embeds: [.embeds[]? | .url // .cast.hash],
            reactions: {likes: .reactions.likes_count, recasts: .reactions.recasts_count},
            replies: .replies.count
          })
    }'
  else
    echo "$RESP_BODY" | jq '{
      casts: [.casts[] | {
        hash, text, timestamp,
        author: {fid: .author.fid, username: .author.username, display_name: .author.display_name},
        embeds: [.embeds[]? | .url // .cast.hash],
        reactions: {likes: .reactions.likes_count, recasts: .reactions.recasts_count},
        replies: .replies.count
      }],
      next_cursor: .next.cursor
    }'
  fi
else
  echo "$RESP_BODY" | jq --argjson s "$HTTP_CODE" '. + {status: $s}' >&2
  exit 1
fi
