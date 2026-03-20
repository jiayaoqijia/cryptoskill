# CryptoSkill

Crypto skill hub for AI agents. Browse, search, and install crypto skills at [cryptoskill.app](https://cryptoskill.app).

## Structure

- `skills/` — Curated crypto skills organized by category
  - `exchanges/` — CEX & DEX integrations (Binance, OKX, Hyperliquid, etc.)
  - `chains/` — Blockchain-specific skills (Ethereum, Solana, Bitcoin, Lightning, etc.)
  - `defi/` — DeFi protocols (Uniswap, Aave, Pump.fun, Raydium, etc.)
  - `wallets/` — Wallet integrations (MetaMask, MPC, Cobo TSS, etc.)
  - `analytics/` — Data & analytics (Dune, CoinGecko, Nansen, etc.)
  - `dev-tools/` — Developer tools (Moralis, Alchemy, Foundry, etc.)
  - `trading/` — Trading bots, signals, and strategies
  - `prediction-markets/` — Prediction markets (Polymarket)
  - `payments/` — Crypto payment protocols (x402)
  - `social/` — Decentralized social (Farcaster, Nostr, XMTP)
  - `ai-crypto/` — AI x Crypto (Bittensor, Virtuals, ElizaOS)
  - `identity/` — On-chain identity & reputation (ERC-8004)
  - `mcp-servers/` — Official MCP protocol servers (Coinbase, Alchemy, GOAT, etc.)
- `docs/` — Static website (GitHub Pages)

## Skill Format

Each skill follows the ClawHub/OpenClaw format:
- `SKILL.md` — Frontmatter (name, description, version, metadata) + documentation
- `_meta.json` — Version history and ownership
- `scripts/` — Optional executable scripts
- `references/` — Optional reference docs

## Naming Convention

- Skill directories: `kebab-case`
- Categories: lowercase singular nouns
- Skills are organized as: `skills/{category}/{skill-name}/`

## Development

- Static site in `docs/` — pure HTML/CSS/JS, no build step
- Deploy via GitHub Pages from `docs/` directory
