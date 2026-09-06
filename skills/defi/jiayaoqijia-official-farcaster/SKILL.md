---
name: farcaster
description: >
  Post, read, search, and engage on Farcaster via the Neynar API. Use when an agent needs to
  post casts, read feeds, search casts, look up users, like/recast, or interact with channels.
  Activate for any Farcaster social media interaction or Web3 social protocol query.
---

# Farcaster

Interact with Farcaster — the decentralized social protocol — via the Neynar v2 REST API.

## Setup

```bash
export NEYNAR_API_KEY="your-api-key"        # required for all ops
export NEYNAR_SIGNER_UUID="your-signer-uuid"  # required for write ops
```

Get API key at https://neynar.com

## API

Base: `https://api.neynar.com/v2/farcaster`

### Read Operations (Free tier)

**User's casts by FID**:
```
web_fetch url="https://api.neynar.com/v2/farcaster/feed/user/3?limit=10" headers="api_key: NEYNAR_API_KEY"
```

**User lookup by username**:
```
web_fetch url="https://api.neynar.com/v2/farcaster/user/by_username?username=vitalik" headers="api_key: NEYNAR_API_KEY"
```

**User lookup by FID**:
```
web_fetch url="https://api.neynar.com/v2/farcaster/user/bulk?fids=3" headers="api_key: NEYNAR_API_KEY"
```

**Cast thread/replies**:
```
web_fetch url="https://api.neynar.com/v2/farcaster/cast/conversation?identifier=0xHASH&type=hash" headers="api_key: NEYNAR_API_KEY"
```

### Write Operations (Require signer)

**Post a cast**:
```
exec command="curl -s -X POST 'https://api.neynar.com/v2/farcaster/cast' -H 'api_key: NEYNAR_API_KEY' -H 'Content-Type: application/json' -d '{\"signer_uuid\":\"SIGNER_UUID\",\"text\":\"Hello Farcaster!\"}'"
```

**Post to a channel**:
```
exec command="curl -s -X POST 'https://api.neynar.com/v2/farcaster/cast' -H 'api_key: NEYNAR_API_KEY' -H 'Content-Type: application/json' -d '{\"signer_uuid\":\"SIGNER_UUID\",\"text\":\"gm\",\"channel_id\":\"base\"}'"
```

**Reply to a cast**:
```
exec command="curl -s -X POST 'https://api.neynar.com/v2/farcaster/cast' -H 'api_key: NEYNAR_API_KEY' -H 'Content-Type: application/json' -d '{\"signer_uuid\":\"SIGNER_UUID\",\"text\":\"Great point!\",\"parent\":\"0xHASH\"}'"
```

**Like a cast**:
```
exec command="curl -s -X POST 'https://api.neynar.com/v2/farcaster/reaction' -H 'api_key: NEYNAR_API_KEY' -H 'Content-Type: application/json' -d '{\"signer_uuid\":\"SIGNER_UUID\",\"reaction_type\":\"like\",\"target\":\"0xHASH\"}'"
```

### Search (Paid tier)

**Search casts by keyword**:
```
web_fetch url="https://api.neynar.com/v2/farcaster/cast/search?q=ethereum&limit=10" headers="api_key: NEYNAR_API_KEY"
```

**Search channels**:
```
web_fetch url="https://api.neynar.com/v2/farcaster/channel/search?q=defi" headers="api_key: NEYNAR_API_KEY"
```

## Free vs Paid

| Feature | Free |
|---------|------|
| Post cast | Yes |
| User lookup | Yes |
| User feed | Yes |
| Like/recast | Yes |
| Following feed | Yes |
| Cast search | Paid |
| Channel feed | Paid |
| Channel search | Paid |

Rate limit: 300 req/min (free tier)

## Use Cases

- **Agent social presence**: post updates, market alerts, DeFi insights to Farcaster
- **Community monitoring**: track mentions, replies, and channel activity
- **Social signals**: correlate social engagement with token performance
- **Agent-to-agent**: coordinate with other agents via Farcaster channels
