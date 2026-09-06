# Robinhood Agent Skill

A ready-to-use skill for [Hermes Agent](https://github.com/NousResearch/hermes-agent), [OpenClaw](https://github.com/open-claw/open-claw), [Claude Code](https://docs.anthropic.com/en/docs/claude-code), [Codex CLI](https://github.com/openai/codex), and other MCP-compatible AI agents that provides read-only access to your Robinhood portfolio.

Gives your agent instant access to positions, quotes, fundamentals, news, earnings, analyst ratings, dividends, options — plus a cache-first strategy, research workflows, and optional Obsidian vault integration.

## Quick Start

### Hermes Agent

```bash
# Install the skill
hermes skills install uzairansaruzi/robinhood-agent-skill/robinhood

# Or use the tap system
hermes skills tap add uzairansaruzi/robinhood-agent-skill
hermes skills search robinhood
hermes skills install robinhood
```

### Claude Code / OpenClaw

```bash
# Clone into your project's .claude/skills directory
mkdir -p .claude/skills
git clone https://github.com/uzairansaruzi/robinhood-agent-skill.git .claude/skills/robinhood
```

### Any Agent (Manual)

Download the `SKILL.md` file and place it in your agent's skills directory. Then configure the MCP server (see below).

## MCP Server Setup

This skill requires the [robinhood-mcp](https://github.com/verygoodplugins/robinhood-mcp) server. Configuration templates for popular agents are in the `templates/` directory.

### Environment Variables

Set these before starting your agent:

```bash
export ROBINHOOD_USERNAME="your_email@example.com"
export ROBINHOOD_PASSWORD="your_password"
# Only needed if using an authenticator app (not SMS):
export ROBINHOOD_TOTP_SECRET="your_totp_secret"
```

### Hermes Agent

Add to `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  robinhood:
    command: uvx
    args:
      - robinhood-mcp
    env:
      ROBINHOOD_USERNAME: "${ROBINHOOD_USERNAME}"
      ROBINHOOD_PASSWORD: "${ROBINHOOD_PASSWORD}"
      # ROBINHOOD_TOTP_SECRET: "${ROBINHOOD_TOTP_SECRET}"
    timeout: 60
    connect_timeout: 30
```

### Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "robinhood": {
      "command": "uvx",
      "args": ["robinhood-mcp"],
      "env": {
        "ROBINHOOD_USERNAME": "your_email",
        "ROBINHOOD_PASSWORD": "your_password"
      }
    }
  }
}
```

### Other Agents

See `templates/` for configuration snippets for:
- **Claude Code** (`.mcp.json`)
- **Codex CLI** (`codex.json`)
- **OpenCode** (`opencode.json`)
- **Cline** (`.cline/mcp.json`)
- **Windsurf** (`.codeium/windsurf/mcp.json`)

## What You Get

### 13 MCP Tools

| Tool | What it does |
|------|-------------|
| `robinhood_get_portfolio` | Total equity, buying power, day change |
| `robinhood_get_positions` | All holdings with cost basis, P&L |
| `robinhood_get_position` | Single ticker lookup |
| `robinhood_get_watchlist` | Your watchlists |
| `robinhood_get_quote` | Real-time price, bid/ask, volume |
| `robinhood_get_fundamentals` | P/E, market cap, dividend yield, 52-week range |
| `robinhood_get_historicals` | OHLCV price history (5min to weekly) |
| `robinhood_get_news` | Recent news for a symbol |
| `robinhood_get_earnings` | Earnings dates, EPS estimates/actuals |
| `robinhood_get_ratings` | Analyst buy/hold/sell ratings |
| `robinhood_get_dividends` | Dividend payment history |
| `robinhood_get_options_positions` | Current options positions |
| `robinhood_search_symbols` | Search stocks by name or ticker |

### Smart Caching

- Portfolio data cached locally at `~/.hermes/data/robinhood/portfolio_cache.json`
- Cache-first strategy — avoids unnecessary API calls
- 15-minute staleness threshold
- Manual refresh via `python3 scripts/refresh_cache.py`

### Research Workflows

- **Entity pages** — persistent per-ticker research with position history
- **Research queue** — track tickers you're evaluating but haven't bought
- **Delta computation** — automatic change detection between snapshots

### Optional: Obsidian Integration

- Immutable dated snapshots in `_ephemeral/portfolio/snapshots/`
- Overwritable `latest.md` with computed deltas
- Dataview-compatible frontmatter
- See SKILL.md for full details

## One-Click Setup

```bash
# Interactive setup (recommended)
bash scripts/install.sh

# Non-interactive (for CI/automation)
ROBINHOOD_USERNAME="you@email.com" \
ROBINHOOD_PASSWORD="your_password" \
bash scripts/install.sh --non-interactive
```

The install script:
1. Checks prerequisites (Python 3, uvx/pip, Node.js/npx)
2. Installs robinhood-mcp and dependencies
3. Prompts for Robinhood credentials (or reads from env)
4. Configures MCP for your agent
5. Creates skill directories for all supported agents
6. Tests the MCP connection
7. Prints next steps

## Cache Refresh Script

```bash
# Default — refresh cache, skip Obsidian
python3 scripts/refresh_cache.py

# With Obsidian vault integration
python3 scripts/refresh_cache.py --vault-path ~/my-obsidian-vault

# Custom cache directory
python3 scripts/refresh_cache.py --cache-dir ~/my-data

# Force refresh even if cache is fresh
python3 scripts/refresh_cache.py --force

# JSON output only (no Obsidian, no markdown)
python3 scripts/refresh_cache.py --json-only
```

## Security

- ✅ **Read-only** — no trade execution, no account modifications
- ✅ **Local processing** — credentials used locally, data never leaves your machine
- ✅ **No credentials in this repo** — all auth via environment variables
- ✅ **Session tokens cached locally** — `~/.tokens/robinhood.pickle`
- ⚠️ **Unofficial API** — uses `robin_stocks` which may break if Robinhood changes their API

## Example Prompts

Once set up, ask your agent:

- "What's my portfolio worth right now?"
- "Give me a health check on my portfolio — concentration, gains, losses"
- "How's my NVDA position doing? Should I add to it?"
- "Show me analyst ratings for AAPL"
- "What earnings are coming up this week for my holdings?"
- "Compare the fundamentals of my top 3 holdings"
- "Any news on TSLA?"
- "Refresh my portfolio data"

## Project Structure

```
robinhood-agent-skill/
├── SKILL.md                    # Agent-readable skill document
├── README.md                   # This file
├── LICENSE                     # MIT
├── scripts/
│   ├── refresh_cache.py        # Portfolio cache refresh + Obsidian snapshots
│   └── install.sh              # One-click setup script
├── templates/
│   ├── config-snippet.yaml     # Hermes Agent MCP config
│   ├── claude-desktop.json     # Claude Desktop config
│   ├── claude-code-mcp.json    # Claude Code / OpenClaw config
│   ├── codex.json              # Codex CLI config
│   ├── opencode.json           # OpenCode config
│   ├── cline-mcp.json          # Cline config
│   └── windsurf-mcp.json       # Windsurf config
└── index.json                  # skills.sh registry metadata
```

## Requirements

- Python 3.9+
- [uv](https://docs.astral.sh/uv/) (for `uvx`) or `pip`
- A Robinhood account
- An MCP-compatible AI agent (Hermes, Claude Code, Codex, OpenCode, etc.)

## License

MIT License — see [LICENSE](LICENSE).

## Related

- [robinhood-mcp](https://github.com/verygoodplugins/robinhood-mcp) — The underlying MCP server by Jack Arturo
- [robin_stocks](https://github.com/robinhood-unofficial/robin_stocks) — Unofficial Robinhood API wrapper
- [Hermes Agent](https://github.com/NousResearch/hermes-agent) — The agent framework this skill was built for
