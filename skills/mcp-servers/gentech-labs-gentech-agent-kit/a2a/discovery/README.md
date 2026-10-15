# a2a/discovery — ERC-8004 Agent Registry Monitor

**Discover** new agents as they register on-chain, so you can reach out before
anyone else does. This is the first stage of the agent-to-agent lifecycle:
**discover → talk → self-audit**.

## What It Does

Polls the ERC-8004 agent registry (`8004scan.io/api/v1/agents`) and alerts on
registrations that matter:

| Signal | Why It Matters |
|--------|---------------|
| `x402_supported: true` | Potential payment-rail customer / integration partner |
| Real name (not `Agent #xxxxx`) | Named agent = deliberate deployment, likely maintained |
| Description present | Real intent, worth reading |
| Base chain + activity | Our primary deployment chain, cross-sell surface |

## Usage

```bash
# Initialize state (records latest agent, no alerts)
python3 discovery.py --init

# Normal run (daily cron recommended)
python3 discovery.py

# Dry run — fetch + print, no state changes
python3 discovery.py --dry-run
```

### Cron Example (daily)

```
0 1 * * *  cd /path/to/a2a/discovery && python3 discovery.py >> discovery.log 2>&1
```

## Configuration

| Env Var | Default | Purpose |
|---------|---------|---------|
| `A2A_DISCOVERY_API_URL` | `https://8004scan.io/api/v1/agents` | Registry API |
| `A2A_DISCOVERY_STATE` | `./a2a-discovery-state.json` | Watermark file (dedup) |
| `A2A_DISCOVERY_LOG` | `./a2a-discovery-log.md` | Alert log (markdown table) |

## Output

- `a2a-discovery-state.json` — dedup watermark (`last_seen_id`)
- `a2a-discovery-log.md` — append-only alert log with UTC timestamps

## Lead Triage (Built In)

Raw registry alerts are noisy (~60% duplicates like Ave.ai Trading Agent,
testnet chains, smoke-test agents). The monitor now runs `triage()` on every
batch automatically:

1. **Drops** testnet/staging chains (84532, 11155111, 1187947933, 97, 5)
2. **Drops** known spam families (Ave.ai Trading Agent duplicates)
3. **Drops** `smoke-*` and `Agent #xxxxx` entries
4. **Scores** the rest: x402 (+3), real description (+2), Base chain (+1),
   reputation score ≥ 10 (+2)
5. **Sorts** leads by score — top of the list is your best outreach target

The alert log only receives triaged leads, so the channel stays clean and the
outreach queue is ready to consume directly.

## Next Stage

See [`../workspace/README.md`](../workspace/README.md) — join the room where
agents talk (Buzz bridge).
