#!/usr/bin/env bash
set -euo pipefail

# fc_cast.sh — Post a cast to Farcaster via Neynar v2 API
# Supports text, embeds (URL or cast), channel, and reply-to.

NEYNAR_BASE="https://api.neynar.com/v2/farcaster"
API_KEY="${NEYNAR_API_KEY:-}"
SIGNER="${NEYNAR_SIGNER_UUID:-}"
TEXT=""
EMBEDS=()
EMBED_CASTS=()
CHANNEL=""
PARENT=""
IDEM=""

usage() {
  cat <<'EOF'
Usage: fc_cast.sh --text "message" [options]

Options:
  --text TEXT            Cast text (required, max 320 chars)
  --embed URL            Embed a URL (image, video, link). Can use twice (max 2).
  --embed-cast HASH      Embed another cast by hash (+ --embed-cast-fid FID)
  --embed-cast-fid FID   FID of the embedded cast's author
  --channel ID           Post to a channel (e.g. "base", "farcaster")
  --parent HASH          Reply to a cast (parent hash or URL)
  --idem KEY             Idempotency key (prevents duplicate posts)
  --api-key KEY          Neynar API key (or set NEYNAR_API_KEY)
  --signer UUID          Signer UUID (or set NEYNAR_SIGNER_UUID)
  -h, --help             Show this help

Examples:
  fc_cast.sh --text "Hello Farcaster!"
  fc_cast.sh --text "Look at this" --embed "https://img.com/pic.png" --channel "base"
  fc_cast.sh --text "Great thread!" --parent "0xabc123..."
EOF
  exit 0
}

EMBED_CAST_FID=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --text) TEXT="$2"; shift 2 ;;
    --embed) EMBEDS+=("$2"); shift 2 ;;
    --embed-cast) EMBED_CASTS+=("$2"); shift 2 ;;
    --embed-cast-fid) EMBED_CAST_FID="$2"; shift 2 ;;
    --channel) CHANNEL="$2"; shift 2 ;;
    --parent) PARENT="$2"; shift 2 ;;
    --idem) IDEM="$2"; shift 2 ;;
    --api-key) API_KEY="$2"; shift 2 ;;
    --signer) SIGNER="$2"; shift 2 ;;
    -h|--help) usage ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

if [[ -z "$API_KEY" ]]; then
  echo '{"error":"NEYNAR_API_KEY not set. Use --api-key or export NEYNAR_API_KEY."}' >&2
  exit 1
fi
if [[ -z "$SIGNER" ]]; then
  echo '{"error":"NEYNAR_SIGNER_UUID not set. Use --signer or export NEYNAR_SIGNER_UUID."}' >&2
  exit 1
fi
if [[ -z "$TEXT" ]]; then
  echo '{"error":"--text is required"}' >&2
  exit 1
fi

# Build JSON body
BODY=$(jq -n --arg signer "$SIGNER" --arg text "$TEXT" '{signer_uuid: $signer, text: $text}')

# Add embeds (URL embeds)
if [[ ${#EMBEDS[@]} -gt 0 ]]; then
  EMBED_JSON="[]"
  for url in "${EMBEDS[@]}"; do
    EMBED_JSON=$(echo "$EMBED_JSON" | jq --arg u "$url" '. + [{"url": $u}]')
  done
  BODY=$(echo "$BODY" | jq --argjson e "$EMBED_JSON" '. + {embeds: $e}')
fi

# Add cast embeds
if [[ ${#EMBED_CASTS[@]} -gt 0 ]]; then
  EXISTING=$(echo "$BODY" | jq '.embeds // []')
  for hash in "${EMBED_CASTS[@]}"; do
    if [[ -n "$EMBED_CAST_FID" ]]; then
      EXISTING=$(echo "$EXISTING" | jq --arg h "$hash" --argjson f "$EMBED_CAST_FID" '. + [{"cast_id": {"hash": $h, "fid": $f}}]')
    else
      echo '{"error":"--embed-cast-fid is required when using --embed-cast"}' >&2
      exit 1
    fi
  done
  BODY=$(echo "$BODY" | jq --argjson e "$EXISTING" '. + {embeds: $e}')
fi

# Add optional fields
if [[ -n "$CHANNEL" ]]; then
  BODY=$(echo "$BODY" | jq --arg c "$CHANNEL" '. + {channel_id: $c}')
fi
if [[ -n "$PARENT" ]]; then
  BODY=$(echo "$BODY" | jq --arg p "$PARENT" '. + {parent: $p}')
fi
if [[ -n "$IDEM" ]]; then
  BODY=$(echo "$BODY" | jq --arg i "$IDEM" '. + {idem: $i}')
fi

# Make the request
RESP=$(curl -sS --connect-timeout 10 --max-time 30 -w "\n%{http_code}" -X POST "$NEYNAR_BASE/cast" \
  -H "x-api-key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d "$BODY")

HTTP_CODE=$(echo "$RESP" | tail -1)
RESP_BODY=$(echo "$RESP" | sed '$d')

if [[ "$HTTP_CODE" -ge 200 && "$HTTP_CODE" -lt 300 ]]; then
  echo "$RESP_BODY" | jq '{success: .success, hash: .cast.hash, author_fid: .cast.author.fid, text: .cast.text}'
else
  echo "$RESP_BODY" | jq --argjson s "$HTTP_CODE" '. + {status: $s}' >&2
  exit 1
fi
