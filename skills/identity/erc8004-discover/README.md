# ERC-8004 Agent Discovery Tool

Search and discover AI agents registered via ERC-8004 across multiple chains.

## Overview

This tool queries the [Agentscan API](https://agentscan.info) to help you find registered AI agents. Whether you're looking for a security auditor, a trading bot, or just exploring the ecosystem, this tool makes discovery easy.

## Installation

No dependencies required - uses Python standard library only.

```bash
# Make executable (optional)
chmod +x scripts/discover.py
```

## Quick Start

```bash
# Search for agents
python scripts/discover.py search "security"

# Find top-rated agents
python scripts/discover.py top --limit 10

# Get details on a specific agent
python scripts/discover.py info 0x1234...

# View ecosystem stats
python scripts/discover.py stats

# List all skills/capabilities
python scripts/discover.py skills
```

## Commands

### `search <query>`

Search for agents by name, description, or skills.

```bash
# Basic search
python scripts/discover.py search "auditor"

# Filter by chain
python scripts/discover.py search "trading" --chain base

# Filter by minimum reputation
python scripts/discover.py search "defi" --min-rep 50

# Combine filters
python scripts/discover.py search "oracle" --chain ethereum --min-rep 75 --limit 5
```

**Options:**
- `--chain`, `-c`: Filter by blockchain (base, ethereum, polygon, monad, bnb)
- `--min-rep`, `-r`: Minimum reputation score (0-100)
- `--has-services`, `-s`: Only show agents with defined skills
- `--limit`, `-l`: Maximum results (default: 20)

### `top`

Show top agents by reputation score.

```bash
# Top 20 overall
python scripts/discover.py top

# Top 10 on Base
python scripts/discover.py top --chain base --limit 10
```

**Options:**
- `--chain`, `-c`: Filter by blockchain
- `--limit`, `-l`: Number of results (default: 20)

### `info <agent_id>`

Get detailed information about a specific agent.

```bash
# By address
python scripts/discover.py info 0x1234567890abcdef...

# By name (partial match)
python scripts/discover.py info "MyAgent"

# By token ID
python scripts/discover.py info 42
```

**Output includes:**
- Address and network
- Owner address
- Reputation score
- Skills and domains
- Decoded metadata (from base64 data URIs)

### `stats`

View ecosystem-wide statistics.

```bash
python scripts/discover.py stats
```

**Shows:**
- Total registered agents
- Agents per chain (with visual bar chart)
- Percentage with metadata, reputation, skills
- Average reputation score

### `skills`

List all unique skills and domains across registered agents.

```bash
python scripts/discover.py skills
```

**Shows:**
- All unique skills with agent counts
- All unique domains with agent counts

## Example Output

```
$ python scripts/discover.py search "security"

Searching for agents matching 'security'...

Found 5 matching agent(s):

Name                      Chain           Rep        Skills               Description
----------------------------------------------------------------------------------------------------
SecurityBot               base            85.0 ★★★   audit, security      Automated security auditing...
AuditHelper               ethereum        72.0 ★★    security, review     Smart contract review...
```

## Supported Chains

- Base (base, base-mainnet, base-sepolia)
- Ethereum (ethereum, eth, mainnet)
- Polygon (polygon, matic)
- Monad (monad, monad-testnet)
- BNB Chain (bnb, bsc, binance)

## API Details

This tool uses the Agentscan public API:
- Agents: `https://agentscan.info/api/agents`
- Networks: `https://agentscan.info/api/networks`

No authentication required. Read-only access.

## Error Handling

- Network errors display helpful messages
- Missing metadata is gracefully handled
- Agents without reputation show "-" instead of 0
- Base64 data URIs are automatically decoded

## License

MIT
