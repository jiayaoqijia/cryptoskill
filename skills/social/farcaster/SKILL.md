---
name: farcaster-skill
description: "Post, read, search, and engage on Farcaster via the Neynar API. Use when an agent needs to: (1) post casts with text, embeds, or in channels, (2) reply to or thread casts, (3) read a user's feed or a channel feed, (4) search casts by keyword, (5) look up user profiles by username or FID, (6) like or recast, (7) delete casts, (8) list or search channels. Pure bash+curl+jq — zero npm dependencies."
---

# Farcaster Skill (Neynar v2)

All scripts use the Neynar v2 REST API. Requires `curl` and `jq`.

## Setup

Set these env vars (or pass `--api-key` / `--signer` flags):

```bash
export NEYNAR_API_KEY="your-api-key"
export NEYNAR_SIGNER_UUID="your-signer-uuid"   # required for write ops
```

Alternatively, put credentials in a JSON file and source them:
```bash
eval $(jq -r '"export NEYNAR_API_KEY=\(.apiKey)\nexport NEYNAR_SIGNER_UUID=\(.signerUuid)"' /path/to/neynar.json)
```

## Scripts

### fc_cast.sh — Post a Cast

Post text, with optional embeds, channel, or reply-to.

```bash
# Simple text cast
scripts/fc_cast.sh --text "Hello Farcaster!"

# Cast with image/video embed
scripts/fc_cast.sh --text "Check this out" --embed "https://example.com/image.png"

# Cast with two embeds (max 2)
scripts/fc_cast.sh --text "Links" --embed "https://a.com" --embed "https://b.com"

# Post to a channel
scripts/fc_cast.sh --text "gm" --channel "base"

# Reply to a cast
scripts/fc_cast.sh --text "Great point!" --parent "0xabcdef1234..."

# Quote-cast (embed another cast)
scripts/fc_cast.sh --text "This 👆" --embed-cast "0xabcdef1234..." --embed-cast-fid 12345
```

Output: JSON `{success, hash}`.

### fc_feed.sh — Read Feeds

```bash
# User's casts by FID
scripts/fc_feed.sh --fid 3 --limit 10

# User's casts by username
scripts/fc_feed.sh --username "vitalik" --limit 5

# Channel feed
scripts/fc_feed.sh --channel "base" --limit 10

# Following feed (casts from people the signer follows)
scripts/fc_feed.sh --following --fid 3 --limit 10

# Cast replies/thread
scripts/fc_feed.sh --thread "0xabcdef..."

# Pagination with cursor
scripts/fc_feed.sh --fid 3 --cursor "eyJwYWdlIjoxfQ=="
```

Output: JSON array of casts with `{hash, author, text, timestamp, embeds, reactions, replies}`.

### fc_user.sh — User Lookup

```bash
# By username
scripts/fc_user.sh --username "dwr"

# By FID
scripts/fc_user.sh --fid 3

# By Ethereum address (verified)
scripts/fc_user.sh --address "0x1234..."

# Bulk by FIDs
scripts/fc_user.sh --fids "3,194,6131"
```

Output: JSON user object(s) with `{fid, username, display_name, bio, follower_count, following_count, verified_addresses}`.

### fc_search.sh — Search Casts

```bash
# Search by keyword
scripts/fc_search.sh --query "base chain"

# Search with author filter
scripts/fc_search.sh --query "ethereum" --author-fid 3

# Search in channel
scripts/fc_search.sh --query "gm" --channel "base"

# Limit results
scripts/fc_search.sh --query "nft" --limit 5
```

Output: JSON array of matching casts.

### fc_react.sh — Like / Recast

```bash
# Like a cast
scripts/fc_react.sh --like "0xabcdef..."

# Unlike
scripts/fc_react.sh --like "0xabcdef..." --undo

# Recast
scripts/fc_react.sh --recast "0xabcdef..."

# Undo recast
scripts/fc_react.sh --recast "0xabcdef..." --undo
```

### fc_delete.sh — Delete a Cast

```bash
scripts/fc_delete.sh --hash "0xabcdef..."
```

### fc_channels.sh — List and Search Channels

```bash
# Search channels by keyword
scripts/fc_channels.sh --search "defi"

# Get channel details by ID
scripts/fc_channels.sh --id "base"

# List trending channels
scripts/fc_channels.sh --trending --limit 10
```

## Common Patterns

### Thread a multi-cast announcement

```bash
HASH1=$(scripts/fc_cast.sh --text "Thread 🧵 1/3: Big news!" --channel "base" | jq -r .hash)
HASH2=$(scripts/fc_cast.sh --text "2/3: Details here..." --parent "$HASH1" | jq -r .hash)
scripts/fc_cast.sh --text "3/3: Link below" --parent "$HASH2" --embed "https://example.com"
```

### Monitor mentions (poll loop)

```bash
while true; do
  scripts/fc_search.sh --query "@yourusername" --limit 5
  sleep 300
done
```

### Post with media (upload first, then embed)

```bash
# Upload to catbox/litterbox first
URL=$(curl -sS -F "reqtype=fileupload" -F "time=72h" \
  -F "fileToUpload=@/path/to/image.png" \
  https://litterbox.catbox.moe/resources/internals/api.php)

# Then embed the URL
scripts/fc_cast.sh --text "Check this out!" --embed "$URL"
```

## Free vs Paid Tier

Not all endpoints are available on Neynar's free plan.

| Feature | Script | Free? |
|---------|--------|-------|
| Post cast | fc_cast.sh | ✅ |
| User casts feed | fc_feed.sh --fid | ✅ |
| User lookup (username/FID/address) | fc_user.sh | ✅ |
| Like / recast | fc_react.sh | ✅ |
| Following feed | fc_feed.sh --following | ✅ |
| Channel feed | fc_feed.sh --channel | ❌ Paid |
| Cast search | fc_search.sh | ❌ Paid |
| Channel search/details/trending | fc_channels.sh | ❌ Paid |
| Delete cast | fc_delete.sh | ❌ Paid |
| Thread/conversation | fc_feed.sh --thread | ✅ |

Scripts that hit paid endpoints will exit non-zero with a clear `402 PaymentRequired` error.

## Error Handling

All scripts exit 0 on success, non-zero on failure. Errors print to stderr as JSON:
```json
{"error": "message", "status": 403}
```

Common errors:
- `401` — Invalid API key
- `402` — Feature requires paid Neynar plan
- `403` — Signer not approved or not paired with API key
- `404` — Cast/user/channel not found
- `429` — Rate limited (Neynar free tier: 300 req/min)

## API Reference

See `references/neynar_endpoints.md` for the full endpoint list and parameter docs.
