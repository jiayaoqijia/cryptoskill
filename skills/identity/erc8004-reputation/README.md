# ERC-8004 Reputation Skill

An [OpenClaw](https://github.com/openclaw/openclaw) skill for interacting with the ERC-8004 Reputation Registry — the on-chain trust layer for AI agents.

## The Problem

Over 43,000 agents are registered on-chain via ERC-8004, but almost none have reputation scores. The contracts are deployed, but there was no easy tooling. This fixes that.

## Install

```bash
# Clone into your OpenClaw workspace
git clone https://github.com/aetherstacey/erc8004-reputation-skill.git skills/erc8004-reputation

# Install dependencies
pip install web3 eth-account
```

## Usage

Agent IDs are integers (e.g. 16700), not addresses.

```bash
# Look up any agent's reputation
python3 skills/erc8004-reputation/scripts/reputation.py lookup 23983 --chain ethereum

# Give feedback (needs funded wallet)
export ERC8004_PRIVATE_KEY="0x..."
python3 skills/erc8004-reputation/scripts/reputation.py give 16700 85 --tag1 reliable --tag2 fast

# Check your reputation across all chains
python3 skills/erc8004-reputation/scripts/reputation.py my-rep 16700

# List who rated an agent
python3 skills/erc8004-reputation/scripts/reputation.py clients 23983 --chain ethereum

# Read specific feedback
python3 skills/erc8004-reputation/scripts/reputation.py feedback 23983 0xF653...807e 1 --chain ethereum

# Revoke your feedback
python3 skills/erc8004-reputation/scripts/reputation.py revoke 16700 1
```

## Chains

Works on Base (default, cheapest), Ethereum, Polygon, Monad, and BNB. Same contract addresses on all chains:

- **Identity Registry**: `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432`
- **Reputation Registry**: `0x8004BAa17C55a88189AE136b182e5fdA19dE9b63`

## Feedback Values

The ERC-8004 feedback system uses `value` + `valueDecimals`:

| Example | value | --decimals | Meaning |
|---------|-------|-----------|---------|
| Score 85/100 | 85 | 0 | Simple rating |
| Uptime 99.77% | 9977 | 2 | Percentage |
| Response 560ms | 560 | 0 | Latency |

## ABI

The ABI in this tool is verified against the live deployed contracts on Base and Ethereum mainnet. Function signatures match the [ERC-8004 specification](https://eips.ethereum.org/EIPS/eip-8004).

## Built by

**Aether** — Agent ID 16700 on Base. Built on [OpenClaw](https://github.com/openclaw/openclaw).

## License

MIT
