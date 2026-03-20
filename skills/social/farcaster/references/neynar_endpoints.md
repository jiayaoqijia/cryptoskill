# Neynar v2 API — Endpoint Reference

Base URL: `https://api.neynar.com/v2/farcaster`

All requests require header: `x-api-key: <NEYNAR_API_KEY>`

## Casts

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/cast` | Post a new cast |
| DELETE | `/cast` | Delete a cast |
| GET | `/cast?identifier=HASH&type=hash` | Lookup cast by hash |
| GET | `/cast?identifier=URL&type=url` | Lookup cast by Warpcast URL |
| GET | `/cast/conversation?identifier=HASH&type=hash` | Get thread/replies |
| GET | `/cast/search?q=QUERY` | Search casts |

### POST /cast — Body
```json
{
  "signer_uuid": "required",
  "text": "max 320 chars",
  "embeds": [{"url": "..."}, {"cast_id": {"hash": "0x...", "fid": 123}}],
  "channel_id": "optional",
  "parent": "hash or parent_url (for replies)",
  "idem": "optional idempotency key",
  "parent_author_fid": "optional, int"
}
```

### DELETE /cast — Body
```json
{
  "signer_uuid": "required",
  "target_hash": "0x..."
}
```

## Feeds

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/feed/user/casts?fid=FID&limit=N` | User's casts |
| GET | `/feed?feed_type=following&fid=FID&limit=N` | Following feed |
| GET | `/feed/channels?channel_ids=ID&limit=N` | Channel feed |
| GET | `/feed/trending?limit=N` | Trending casts |

Pagination: all feed endpoints return `next.cursor` for pagination via `&cursor=TOKEN`.

## Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/user/by_username?username=NAME` | Lookup by username |
| GET | `/user/bulk?fids=1,2,3` | Bulk lookup by FIDs |
| GET | `/user/bulk-by-address?addresses=0x...` | Lookup by ETH address |
| GET | `/user/search?q=NAME&limit=N` | Search users |

## Reactions

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/reaction` | Add like or recast |
| DELETE | `/reaction` | Remove like or recast |

### Body
```json
{
  "signer_uuid": "required",
  "reaction_type": "like" | "recast",
  "target": "0x... (cast hash)"
}
```

## Channels

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/channel?id=ID` | Channel details |
| GET | `/channel/search?q=KEYWORD` | Search channels |
| GET | `/channel/trending?time_window=7d` | Trending channels |
| GET | `/channel/list?limit=N` | List all channels |

## Follows

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/user/follow` | Follow a user |
| DELETE | `/user/follow` | Unfollow a user |

### Body
```json
{
  "signer_uuid": "required",
  "target_fids": [123, 456]
}
```

## Rate Limits

- Free tier: 300 requests/minute
- Paid tiers scale higher
- Rate-limited responses return HTTP 429

## Common Response Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad request (invalid params) |
| 401 | Invalid API key |
| 403 | Signer not approved / wrong API key |
| 404 | Resource not found |
| 429 | Rate limited |
| 500 | Neynar server error |
