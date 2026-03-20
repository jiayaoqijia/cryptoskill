---
name: ERC-8004 Reputation
description: On-chain reputation for AI agents. Give feedback, check scores, view leaderboards, and build trust via the ERC-8004 Reputation Registry. Supports Base, Ethereum, Polygon, Monad, BNB.
---

# ERC-8004 Reputation Skill

Interact with the ERC-8004 Reputation Registry — the decentralized reputation layer for AI agents.

## Use This When...

- "Check an agent's reputation"
- "Rate this agent"
- "Give feedback to agent X"
- "What's my agent's reputation?"
- "Who gave feedback to my agent?"
- "Show me the reputation leaderboard"
- "Top agents by reputation"
- "Revoke my feedback"

## Commands

### lookup
Look up an agent's reputation summary.

```bash
python scripts/reputation.py lookup <agentId> [--chain CHAIN]
```

Shows: reviewer count, feedback count, summary value, individual feedback.

### give
Give feedback to an agent.

```bash
python scripts/reputation.py give <agentId> <value> [--decimals N] [--tag1 TAG] [--tag2 TAG] [--chain CHAIN]
```

**Examples:**
```bash
# Simple score (0-100)
python scripts/reputation.py give 16700 85 --tag1 reliable

# Percentage with decimals (99.77%)
python scripts/reputation.py give 16700 9977 --decimals 2 --tag1 uptime
```

### my-rep
Check your agent's reputation across all chains.

```bash
python scripts/reputation.py my-rep <agentId> [--chains base,ethereum,polygon]
```

### clients
List all addresses that gave feedback.

```bash
python scripts/reputation.py clients <agentId> [--chain CHAIN]
```

### feedback
Read a specific feedback entry.

```bash
python scripts/reputation.py feedback <agentId> <clientAddress> <feedbackIndex> [--chain CHAIN]
```

### revoke
Revoke feedback you previously gave.

```bash
python scripts/reputation.py revoke <agentId> <feedbackIndex> [--chain CHAIN]
```

### leaderboard
Show top agents by reputation score.

```bash
python scripts/reputation.py leaderboard [--chain CHAIN] [--limit 20]
```

Fetches from Agentscan API and displays top agents with scores and star ratings.

## Cross-Skill Workflows

### Post-Registration Reputation Building
```bash
# 1. Register your agent (from erc8004-register skill)
python scripts/register.py register --name "MyBot" --description "..."

# 2. Validate the registration
python scripts/register.py validate 42

# 3. Check initial reputation (should be empty)
python scripts/reputation.py lookup 42

# 4. After interacting with clients, check reputation growth
python scripts/reputation.py my-rep 42
```

### Before Interacting with an Agent
```bash
# 1. Find the agent (from erc8004-discover skill)
python scripts/discover.py search "oracle"

# 2. Get detailed info
python scripts/discover.py info 0x1234...

# 3. Check their reputation
python scripts/reputation.py lookup 42 --chain base

# 4. If satisfied, interact and then give feedback
python scripts/reputation.py give 42 85 --tag1 reliable --tag2 accurate
```

### Reputation Monitoring
```bash
# Check your reputation regularly
python scripts/reputation.py my-rep 42

# See who's giving feedback
python scripts/reputation.py clients 42 --chain base

# Read specific feedback
python scripts/reputation.py feedback 42 0xABC... 1 --chain base
```

## Heartbeat Integration

Monitor reputation changes in automated pipelines:

```bash
# Cron: check reputation daily
0 9 * * * python scripts/reputation.py my-rep 42 >> /var/log/rep-monitor.log 2>&1

# In a monitoring script:
#!/bin/bash
# Get current feedback count
count=$(python scripts/reputation.py lookup 42 2>&1 | grep "Feedback count:" | awk '{print $3}')
last_count=$(cat /tmp/rep-count-42.txt 2>/dev/null || echo 0)
if [ "$count" != "$last_count" ]; then
    echo "New feedback received! Count: $count" | notify-send
    echo "$count" > /tmp/rep-count-42.txt
fi
```

## Configuration

### Wallet (required for write operations)

```bash
export ERC8004_MNEMONIC="your twelve word mnemonic phrase here"
# OR
export ERC8004_PRIVATE_KEY="0xabc123..."
```

Read operations (lookup, my-rep, clients, feedback, leaderboard) don't need a wallet.

### Supported Chains

| Chain    | ID   | Default | Gas Cost |
|----------|------|---------|----------|
| Base     | 8453 | Yes     | ~$0.001  |
| Ethereum | 1    |         | ~$1-10   |
| Polygon  | 137  |         | ~$0.01   |
| Monad    | 143  |         | ~$0.001  |
| BNB      | 56   |         | ~$0.05   |

Base is recommended — cheapest gas by far.

## Contract Addresses

Same on all chains:
- **Identity Registry**: `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432`
- **Reputation Registry**: `0x8004BAa17C55a88189AE136b182e5fdA19dE9b63`

## Dependencies

```bash
pip install web3 eth-account
```

## Related Skills

- **erc8004-register**: Register and manage agents on-chain
- **erc8004-discover**: Find and monitor agents
