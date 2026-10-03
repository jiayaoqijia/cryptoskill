---
name: gdex-livestream-discovery
description: Solana livestream-token discovery — currently-live streams, per-token live status, and big-buy alert feeds
---

# GDEX: Livestream Discovery

Surface the Solana livestream token-launch ecosystem inside an AI agent or
trading UI: tokens that are currently live-streaming, per-token live status,
and the "big buy" alert feed.

## When to Use

- Building a discovery feed for live token launches
- Showing a live indicator next to a token
- Alerting users to large incoming buys on a chain

## Prerequisites

- `@gemachdao/gdex-skill` installed
- No authentication required for these read endpoints (whitelisted)

## Backend Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| `GET`  | `/v1/currently_live` | Tokens currently live-streaming |
| `GET`  | `/v1/live_status/:address` | Per-token live status |
| `GET`  | `/v1/bigbuys/:chainId` | Big-buy alert feed for a chain |

## SDK Usage

```typescript
import { GdexSkill } from '@gemachdao/gdex-skill';

const skill = new GdexSkill();

// Currently-live launches (Solana-centric)
const live = await skill.getCurrentlyLiveTokens({ limit: 50 });

// Live status for one token
const status = await skill.getLiveStatus({ address: 'SoLanA1111...' });

// Big-buy feed (chainId 622112261 = Solana)
const bigBuys = await skill.getBigBuys({ chainId: 622112261, limit: 100 });
```

## Notes

- The livestream surface is currently Solana-only — the most common
  `chainId` for `bigbuys` is `622112261`.
- These endpoints are cached server-side and may return slightly stale data
  (typically <30s).
- The `live_status` path includes the token address inline; pass the raw
  address (no chain prefix).
