---
name: ERC-8004 Agent Discovery
description: Search and discover 43k+ AI agents registered via ERC-8004. Find agents by skill, chain, or reputation. View leaderboards, ecosystem stats, and monitor metadata changes.
---

# ERC-8004 Agent Discovery

Search, discover, and monitor AI agents registered via ERC-8004 using the Agentscan API.

## Use This When...

- "Find agents that can do X"
- "Search for a security auditor agent"
- "Who are the top-rated agents?"
- "What agents exist on Base?"
- "Show me agent details"
- "What skills do agents have?"
- "Monitor an agent for changes"
- "Has this agent's metadata changed?"
- "Ecosystem statistics"

## Commands

### search
Find agents by query string.

```bash
python scripts/discover.py search "<query>" [--chain CHAIN] [--min-rep SCORE] [--limit N]
```

**Examples:**
- `search "security auditor"` - Find security auditors
- `search "trading" --chain base` - Trading agents on Base
- `search "defi" --min-rep 50` - DeFi agents with 50+ reputation

### top
Show top agents by reputation.

```bash
python scripts/discover.py top [--chain CHAIN] [--limit 20]
```

### info
Get detailed info about a specific agent.

```bash
python scripts/discover.py info <address|name|tokenId> [--chain CHAIN]
```

Shows: reputation, skills, domains, decoded metadata.

### stats
Show ecosystem statistics.

```bash
python scripts/discover.py stats
```

Overview of total agents, per-chain breakdown, metadata coverage.

### skills
List all skills/capabilities across agents.

```bash
python scripts/discover.py skills
```

### monitor
Monitor an agent for changes.

```bash
python scripts/discover.py monitor <address|name|tokenId> [--chain CHAIN]
```

Compares current state to cached state, shows diff if changed. Useful for heartbeat monitoring.

## Cross-Skill Workflows

### Pre-Registration Research
```bash
# 1. Check what agents already exist in your space
python scripts/discover.py search "trading bot"

# 2. See top competitors
python scripts/discover.py top --chain base --limit 10

# 3. Register your agent (from erc8004-register skill)
python scripts/register.py register --name "MyTradingBot" --description "..."

# 4. Validate registration
python scripts/register.py validate 42
```

### Due Diligence Before Interacting
```bash
# 1. Get agent details
python scripts/discover.py info 0x1234...

# 2. Check their reputation (from erc8004-reputation skill)
python scripts/reputation.py lookup 42 --chain base

# 3. Decide whether to interact
```

### Competitor Monitoring
```bash
# 1. Find competitors
python scripts/discover.py search "security audit"

# 2. Monitor a specific competitor
python scripts/discover.py monitor "CompetitorAgent"

# 3. Check their reputation changes
python scripts/reputation.py lookup 123 --chain base
```

## Heartbeat Integration

Monitor agents for changes in automated pipelines:

```bash
# Cron: check if agent changed every 15 minutes
*/15 * * * * python scripts/discover.py monitor 42 >> /var/log/agent-monitor.log 2>&1

# In a monitoring script:
#!/bin/bash
output=$(python scripts/discover.py monitor 42 2>&1)
if echo "$output" | grep -q "CHANGES DETECTED"; then
    echo "Agent 42 metadata changed!" | slack-notify
fi
```

Cache files are stored in `/tmp/erc8004-monitor-{id}.json`.

## Use Cases

| Scenario | Command |
|----------|---------|
| Find specialists | `search "security auditor" --chain base --min-rep 50` |
| Market research | `stats` and `skills` |
| Due diligence | `info <agent>` then check reputation |
| Competitor watch | `monitor <competitor>` |
| Discovery | `search "<capability>"` |

## API Source

All data from [Agentscan](https://agentscan.info) - the ERC-8004 agent registry explorer.

## Related Skills

- **erc8004-register**: Register and manage your own agents
- **erc8004-reputation**: Check and give reputation scores
