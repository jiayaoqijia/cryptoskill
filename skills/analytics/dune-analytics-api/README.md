# Dune Analytics API Skill

📊 An [Agent Skill](https://github.com/agentskills/agentskills) for querying and analyzing blockchain data via the [Dune Analytics](https://dune.com) API.

## What's Included

- **API Usage** — Execute queries, manage SQL, track credits, handle parameters
- **40+ Common Tables** — Raw, decoded, curated (DEX/NFT/tokens/prices/labels) across EVM & Solana
- **SQL Optimization** — CTE patterns, JOIN strategies, array operations, partition pruning
- **Wallet Analysis** — Cross-chain wallet tracking, fee analysis, multi-chain aggregation

## Installation

### Claude Code / Codex / Gemini CLI / Cursor
```bash
# Copy to your agent's skills directory
cp -r dune-analytics-api ~/.claude/skills/
# or
cp -r dune-analytics-api ~/.codex/skills/
```

### OpenClaw
```bash
# Via ClawHub
clawhub install dune-analytics-api

# Or copy to workspace
cp -r dune-analytics-api /path/to/workspace/skills/
```

## Requirements

- Python 3.x
- `pip install dune-client`
- `DUNE_API_KEY` environment variable ([get one here](https://dune.com/settings/api))

## Structure

```
dune-analytics-api/
├── SKILL.md                      # Core skill instructions
├── README.md                     # This file
└── references/
    ├── index.md                  # Reference directory
    ├── query-execution.md        # API patterns & code examples
    ├── common-tables.md          # Dune table reference
    ├── sql-optimization.md       # SQL optimization techniques
    └── wallet-analysis.md        # Wallet tracking queries
```

## License

MIT
