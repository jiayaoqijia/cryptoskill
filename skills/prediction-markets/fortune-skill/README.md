# QLWY Fortune Casting Skill

Agent skill for integrating with QLWY's on-chain I Ching divination (链上算卦), powered by VRF randomness and AI interpretation.

## Install

```bash
npx skills add qlwy/fortune-skill
```

## What's Included

| File | Description |
|------|-------------|
| `SKILL.md` | Machine-readable skill definition for AI agents |
| `references/QLWYFortuneCore.abi.json` | FortuneCore contract ABI (cast, mint, query) |
| `references/hexagramData.json` | All 64 I Ching hexagrams (name, lines, judgment text) |
| `examples/cast-fortune.ts` | Full flow: cast → wait VRF → query result → AI interpretation |

## Quick Start

```bash
# Cast a fortune and get AI reading
PRIVATE_KEY=0x... npx tsx examples/cast-fortune.ts "我的事业运如何？"

# Cast without interpretation (no auth needed)
PRIVATE_KEY=0x... npx tsx examples/cast-fortune.ts "财运" --no-interpret
```

## Deployed Contracts (BSC Mainnet)

| Contract | Address |
|----------|---------|
| QLWYFortuneCore | `0xcE6f2F55898050C0D1769164c4Ceb828B4fC54f8` |

## License

MIT

