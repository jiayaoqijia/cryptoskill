---
name: ERC-8004 Register
description: Register AI agents on-chain, update metadata, validate registrations, and auto-fix broken profiles via the ERC-8004 Identity Registry. Supports Base, Ethereum, Polygon, Monad, BNB.
---

# ERC-8004 Registration Skill

Register, update, validate, and fix agents on-chain via the ERC-8004 Identity Registry.

## Use This When...

- "Register my agent on-chain"
- "I need to create a new ERC-8004 agent"
- "Update my agent's metadata"
- "Check if my agent registration is valid"
- "Fix my agent's registration issues"
- "Show my agent's on-chain info"
- "What agents do I own?"
- "Health check my agents"

## Commands

### register
Register a new agent on-chain.

```bash
python scripts/register.py register --name "AgentName" --description "Description" [--image URL] [--chain base]
```

**Options:**
- `--name` (required): Agent name
- `--description` (required): Agent description
- `--image`: Image URL (must be https://)
- `--chain`: Blockchain (base, ethereum, polygon, monad, bnb). Default: base

### update
Update an existing agent's metadata.

```bash
python scripts/register.py update <agentId> [--name NAME] [--description DESC] [--image URL] [--add-service name=X,endpoint=Y] [--remove-service NAME] [--chain base]
```

### info
Display agent information.

```bash
python scripts/register.py info <agentId> [--chain base]
```

### validate
Check registration for common issues.

```bash
python scripts/register.py validate <agentId> [--chain base]
```

**Checks:**
- Missing `type` field
- Local-path images (/home/..., ./, file://)
- Empty name/description
- Missing registrations array
- Unreachable image URLs

### fix
Auto-fix common registration issues.

```bash
python scripts/register.py fix <agentId> [--chain base] [--dry-run]
```

**Auto-fixes:**
- Missing `type` field
- Missing `registrations` array
- Local-path images (removes them)

Use `--dry-run` to preview changes without applying.

### self-check
Check all agents owned by your wallet.

```bash
python scripts/register.py self-check
```

Queries Agentscan for your agents, validates each, and prints a health report.

## Cross-Skill Workflows

### Post-Registration Flow
```bash
# 1. Register new agent
python scripts/register.py register --name "MyBot" --description "Trading assistant"

# 2. Validate the registration
python scripts/register.py validate 42 --chain base

# 3. Check initial reputation (from erc8004-reputation skill)
python scripts/reputation.py lookup 42 --chain base

# 4. Monitor for discovery (from erc8004-discover skill)
python scripts/discover.py info 42
```

### Periodic Health Check
```bash
# Run self-check to validate all your agents
python scripts/register.py self-check

# Fix any issues found
python scripts/register.py fix 42 --chain base
```

## Heartbeat Integration

For automated monitoring, run self-check periodically:

```bash
# Cron: check health every hour
0 * * * * cd /path/to/skill && python scripts/register.py self-check >> /var/log/agent-health.log 2>&1

# Or in a script:
#!/bin/bash
python scripts/register.py self-check
if [ $? -ne 0 ]; then
    echo "Agent health check failed!" | notify-send
fi
```

## Wallet Configuration

Set one of these environment variables:

```bash
export ERC8004_MNEMONIC="your twelve word mnemonic phrase here"
# OR
export ERC8004_PRIVATE_KEY="0x..."
```

## Contract

Identity Registry: `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` (same on all chains)

## Supported Chains

| Chain    | ID   | Explorer             |
|----------|------|----------------------|
| Base     | 8453 | basescan.org         |
| Ethereum | 1    | etherscan.io         |
| Polygon  | 137  | polygonscan.com      |
| Monad    | 143  | explorer.monad.xyz   |
| BNB      | 56   | bscscan.com          |

## Dependencies

```bash
pip install web3 eth-account
```

## Related Skills

- **erc8004-discover**: Find and monitor agents
- **erc8004-reputation**: Rate agents and check trust scores
