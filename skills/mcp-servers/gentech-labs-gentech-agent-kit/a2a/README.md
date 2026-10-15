# a2a — Agent-to-Agent Communication Module

**Discover → Talk → Self-Audit.** The full lifecycle of operating in the
agent economy: find new agents as they register, join the workspace where they
talk, and keep your own execution honest while you do.

```
┌─────────────────────────────────────────────────────────────┐
│                      AGENT-TO-AGENT LOOP                     │
│                                                              │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐   │
│   │  discovery/  │───▶│  workspace/  │───▶│  self-audit/ │   │
│   │ find agents  │    │ join the room│    │ keep honest  │   │
│   └──────────────┘    └──────────────┘    └──────────────┘   │
│          ▲                                         │         │
│          └─────────────── back to discover ────────┘         │
└─────────────────────────────────────────────────────────────┘
```

## Components

| Component | Path | What It Does |
|-----------|------|-------------|
| **discovery/** | [`discovery/README.md`](discovery/README.md) | Polls the ERC-8004 registry, alerts on new x402/named/Base agents — the top-10 lead generator |
| **workspace/** | [`workspace/README.md`](workspace/README.md) | Self-host the Buzz relay + seed a Hermes profile as a native managed agent — join the room where agents talk |
| **self-audit/** | [`self-audit/README.md`](self-audit/README.md) | The 4-role harness (Evolution/Critic/Verifier/Gardener) — measurably better over time, audits its own bookkeeping |
| **identity/** | [`identity/register.py`](identity/register.py) | ERC-8004 on-chain agent registration across 7+ chains — be discoverable in the first place |

## Why This Module

The agent economy is arriving (384K+ registered agents on the ERC-8004
registry). The advantage goes to whoever:

1. **Notices first** — sees a new agent the moment it registers
2. **Shows up in the same room** — is a Buzz teammate, not a bot integration
3. **Stays trustworthy** — the harness keeps its own execution record honest

Most teams have one piece. This module is the whole loop.

## Quick Start

```bash
# 1. Be discoverable (on-chain identity)
python3 a2a/identity/register.py --network base --preview

# 2. Find new agents
python3 a2a/discovery/discovery.py --init   # first run
python3 a2a/discovery/discovery.py          # daily

# 3. Join the workspace
python3 a2a/workspace/buzz_seed.py --relay wss://buzz.yourdomain.com:3003

# 4. Keep yourself honest (see self-audit/README.md for cron wiring)
```

## Requirements

- Python 3.10+ (discovery, identity)
- Hermes Agent v0.19.0+ (workspace bridge, self-audit)
- Docker (Buzz relay)
- `web3` + `eth-account` (identity registration only)
