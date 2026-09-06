# AIBTC Bitcoin Wallet Skill

An [Agent Skills](https://agentskills.io) compatible skill that teaches any LLM how to use Bitcoin L1 wallet operations with optional Pillar smart wallet and Stacks L2 DeFi capabilities.

## Installation

### With MCP Server (Recommended)

Install the MCP server which includes this skill:

```bash
npx @aibtc/mcp-server@latest --install
```

The skill is available at `node_modules/@aibtc/mcp-server/skill/`.

### From ClawHub

Browse and install from ClawHub registry:

```bash
npx clawhub install aibtc-bitcoin-wallet
```

Or view at [clawhub.ai/skills](https://www.clawhub.ai/skills) and search for `aibtc-bitcoin-wallet`.

### Standalone (Local)

Clone and reference directly:

```bash
git clone https://github.com/aibtcdev/aibtc-mcp-server.git
# Reference skill/ directory in your agent configuration
```

## Usage with Any LLM Agent

Point your agent to the skill file:

```
skill/SKILL.md
```

The skill follows the Agent Skills open specification and works with:
- Claude Code
- Cursor
- Codex
- Gemini CLI
- 20+ other compatible tools

## Skill Structure

```
skill/
├── SKILL.md                    # Main skill - Bitcoin L1 core workflows
├── README.md                   # This file
└── references/
    ├── pillar-wallet.md        # Pillar smart wallet (passkey auth, DeFi)
    ├── stacks-defi.md          # Stacks L2 (ALEX DEX, Zest, x402)
    └── troubleshooting.md      # Common issues and solutions
```

### Content Hierarchy

1. **SKILL.md** - Bitcoin L1 essentials: balance, fees, send BTC, wallet management
2. **pillar-wallet.md** - sBTC smart wallet with passkey auth and Zest yield
3. **stacks-defi.md** - STX transfers, DEX swaps, lending, paid APIs
4. **troubleshooting.md** - Error resolution guide

## Local Testing

To verify the skill loads correctly:

1. Install the MCP server locally:
   ```bash
   cd aibtc-mcp-server
   npm install && npm run build
   ```

2. Configure Claude Code to use local version:
   ```json
   {
     "mcpServers": {
       "aibtc": {
         "command": "node",
         "args": ["/path/to/aibtc-mcp-server/dist/index.js"]
       }
     }
   }
   ```

3. Start a new Claude Code session and ask:
   ```
   "What Bitcoin wallet tools are available?"
   ```

4. Claude should reference the skill workflows from SKILL.md.

## Links

- [Main Repository](https://github.com/aibtcdev/aibtc-mcp-server)
- [npm Package](https://www.npmjs.com/package/@aibtc/mcp-server)
- [ClawHub Registry](https://www.clawhub.ai/skills)
- [Agent Skills Specification](https://agentskills.io)

## License

MIT
