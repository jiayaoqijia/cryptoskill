---
name: celo-official-agent-skills
description: "Agent Skills for building on Celo and EVM chains. Compatible with [Claude Code](https://claude.ai/code), [Cursor](https://cursor.com), [Windsurf](https://codeium.com/windsurf), [OpenAI Codex](https://openai.com/codex), and other [Agent Skills](https://agentskills.io) compatible tools."
---

# celo-official-agent-skills

_Source: [github.com/celo-org/agent-skills](https://github.com/celo-org/agent-skills). The body below is the upstream README.md captured at the time of registration._

---

# Celo Agent Skills

Agent Skills for building on Celo and EVM chains. Compatible with [Claude Code](https://claude.ai/code), [Cursor](https://cursor.com), [Windsurf](https://codeium.com/windsurf), [OpenAI Codex](https://openai.com/codex), and other [Agent Skills](https://agentskills.io) compatible tools.

## Installation

```bash
# Install all skills
npx openskills install celo-org/agent-skills -g

# Install a specific skill
npx openskills install celo-org/agent-skills --skill evm-hardhat -g
```

### Package managers

```bash
# pnpm
pnpm dlx openskills install celo-org/agent-skills -g

# yarn
yarn dlx openskills install celo-org/agent-skills -g

# bun
bunx openskills install celo-org/agent-skills -g
```

## Skills

### Development Tools

| Skill | Description |
|-------|-------------|
| [evm-hardhat](skills/evm-hardhat) | Hardhat development for EVM chains including Celo. Covers project setup, compilation, testing, deployment, and verification. |
| [evm-foundry](skills/evm-foundry) | Foundry development for EVM chains including Celo. Covers forge, cast, anvil, testing, deployment, and verification. |
| [celo-composer](skills/celo-composer) | Scaffold Celo dApps with templates. Supports React, Next.js, and various wallet providers. |
| [contract-verification](skills/contract-verification) | Verify smart contracts on Celo. Covers Celoscan, Blockscout, Sourcify, and Remix verification methods. |

### Blockchain Interaction

| Skill | Description |
|-------|-------------|
| [celo-rpc](skills/celo-rpc) | Interact with Celo blockchain via RPC. Covers reading balances, transactions, blocks, and Celo-specific methods. |
| [viem](skills/viem) | TypeScript library for Celo with first-class support for fee currencies and CIP-64 transactions. |
| [wagmi](skills/wagmi) | React hooks for Celo dApps. Covers wallet connection, contract interaction, and transaction handling. |
| [fee-abstraction](skills/fee-abstraction) | Pay gas fees with ERC-20 tokens on Celo. Covers supported tokens (USDC, USDT, cUSD), wallet compatibility, and implementation. |

### Wallet Integration

| Skill | Description |
|-------|-------------|
| [evm-wallet-integration](skills/evm-wallet-integration) | Integrate wallets into Celo dApps. Covers Reown AppKit, Dynamic, and custom wagmi implementations. |
| [minipay-integration](skills/minipay-integration) | Build Mini Apps for MiniPay. Covers wallet detection, stablecoin payments, and fee currency support. |
| [thirdweb](skills/thirdweb) | Full-stack Web3 development with thirdweb SDK. Covers contract deployment, wallet connection, and pre-built components. |

### AI Agent Infrastructure

| Skill | Description |
|-------|-------------|
| [8004](skills/8004) | ERC-8004 Agent Trust Protocol for AI agent identity, reputation, and validation on Celo. |
| [x402](skills/x402) | x402 HTTP-native payment protocol for AI agents. Covers pay-per-use APIs and micropayments with stablecoins. |

### DeFi & Assets

| Skill | Description |
|-------|-------------|
| [celo-stablecoins](skills/celo-stablecoins) | Work with Mento stablecoins (cUSD, cEUR, cREAL) and bridged stables (USDC, USDT) on Celo. |
| [celo-defi](skills/celo-defi) | DeFi protocol integration on Celo. Covers Uniswap, Aave, and Ubeswap. |
| [bridging](skills/bridging) | Bridge assets to and from Celo. Covers native bridge, Wormhole, LayerZero, and other bridges. |

## Skill Structure

Each skill follows the [Agent Skills](https://agentskills.io) specification:

```
skill-name/
├── SKILL.md           # Main instructions (required)
├── references/        # Detailed documentation
├── rules/             # Best practices and standards
└── scripts/           # Executable scripts
```

Skills activate automatically when relevant tasks are detected.

## Celo Network Information

| Network | Chain ID | RPC Endpoint | Explorer |
|---------|----------|--------------|----------|
| Celo Mainnet | 42220 | https://forno.celo.org | https://celoscan.io |
| Celo Sepolia | 11142220 | https://forno.celo-sepolia.celo-testnet.org | https://sepolia.celoscan.io |

### Block Explorers

- **Celoscan**: https://celoscan.io (Etherscan-style)
- **Blockscout**: https://celo.blockscout.com (open-source)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

Apache-2.0
