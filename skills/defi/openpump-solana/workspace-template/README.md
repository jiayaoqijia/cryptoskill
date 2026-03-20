# OpenPump Trading Agent -- OpenClaw Workspace Template

An autonomous Solana memecoin trading agent powered by OpenPump's MCP server and OpenClaw. This workspace template turns OpenClaw into a disciplined, risk-managed trading agent that monitors positions, executes stop-losses and take-profits, and reports portfolio status on a 30-minute heartbeat cycle.

## What This Agent Does

- Buys and sells pump.fun memecoin tokens via the OpenPump MCP server
- Monitors open positions every 30 minutes (heartbeat cycle)
- Executes mechanical stop-losses (-50%) and take-profits (+200%)
- Applies trailing stops on winning positions
- Exits stale positions after 4 hours of minimal movement
- Pauses trading after 3 consecutive losses (circuit breaker)
- Reports portfolio summaries and alerts after every heartbeat

## What This Agent Does NOT Do

- Create new tokens (tools are available but not part of the trading strategy)
- Use multi-wallet bundle operations (single-wallet trading only)
- Transfer SOL externally without explicit user instruction
- Override risk parameters without explicit user instruction
- Trade when the circuit breaker is active

## Quick Start

### 1. Prerequisites

- [OpenClaw](https://github.com/openclaw/openclaw) installed and configured
- Node.js 18+ (for the MCP server process)
- An OpenPump account with an API key

### 2. Get Your OpenPump API Key

1. Sign up at [openpump.io](https://openpump.io)
2. Go to **Dashboard > API Keys**
3. Create a new key (starts with `op_sk_live_`)

### 3. Set Up the Workspace

Copy this template directory into your OpenClaw workspace:

```bash
# Option A: Copy the template into a new workspace
cp -r /path/to/workspace-template ~/my-trading-agent
cd ~/my-trading-agent

# Option B: If you already have an OpenClaw workspace, copy the files into it
cp SOUL.md TOOLS.md SKILLS.md HEARTBEAT.md openclaw.json /path/to/your/workspace/
```

### 4. Configure the API Key

Set the environment variable:

```bash
export OPENPUMP_API_KEY="op_sk_live_YOUR_KEY_HERE"
```

Or add it to your `~/.openclaw/.env` file for persistence:

```bash
echo 'OPENPUMP_API_KEY=op_sk_live_YOUR_KEY_HERE' >> ~/.openclaw/.env
```

### 5. Fund Your Trading Wallet

The agent needs SOL to trade. After starting OpenClaw, the agent will:

1. Check for existing wallets via `list-wallets`
2. If no wallet exists, create one via `create-wallet`
3. Display the deposit address via `get-wallet-deposit-address`

Send SOL to the displayed address from Phantom, Solflare, or any Solana wallet.

**Recommended starting balance:** 5-10 SOL (the agent will never risk more than 3 SOL in open positions at once).

### 6. Start OpenClaw

```bash
cd ~/my-trading-agent
openclaw
```

The agent will announce itself, scan portfolio state, and begin the heartbeat monitoring cycle.

## Risk Parameters

These are configured in `SOUL.md` and enforced by the agent on every trade:

| Parameter | Default | Description |
|-----------|---------|-------------|
| Max per position | 0.5 SOL | Maximum SOL allocated to any single token buy |
| Max total exposure | 3.0 SOL | Maximum SOL across all open token positions combined |
| Min SOL reserve | 0.5 SOL | Always kept for gas fees and emergency exits |
| Max open positions | 5 | Prevents overextension |
| Stop-loss | -50% | Sell entire position when value drops 50% from entry |
| Take-profit | +200% | Sell entire position when value triples from entry |
| Trailing stop | -30% from peak | Activates when position has been up >100% |
| Time decay | 4 hours | Exit if position hasn't moved >+20% within 4 hours |
| Circuit breaker | 3 consecutive losses | Pause new buys for 1 hour |
| Session loss limit | 2.0 SOL | Stop all trading for the session |
| Daily loss limit | 3.0 SOL | Stop all trading until next UTC day |

### Customizing Risk Parameters

Edit the **Risk Parameters** section in `SOUL.md` to adjust limits. For example, to trade more conservatively:

```
Max per position:    0.2 SOL  (was 0.5)
Max total exposure:  1.0 SOL  (was 3.0)
Stop-loss:          -30%      (was -50%)
Take-profit:       +100%      (was +200%)
```

Or to trade more aggressively:

```
Max per position:    1.0 SOL  (was 0.5)
Max total exposure:  5.0 SOL  (was 3.0)
Max open positions:  10       (was 5)
```

## File Structure

```
workspace-template/
  SOUL.md           -- Agent personality, core behaviors, risk parameters
  TOOLS.md          -- Complete tool reference (57 tools, all parameters)
  SKILLS.md         -- ClawHub skill references (openpump-solana-mcp)
  HEARTBEAT.md      -- 30-minute autonomous check cycle procedure
  openclaw.json     -- MCP server configuration
  README.md         -- This file
```

## How It Works

### Startup

When OpenClaw starts, it:
1. Reads `SOUL.md` to understand its identity and behavior rules
2. Reads `TOOLS.md` to understand available MCP tools
3. Connects to the OpenPump MCP server via the config in `openclaw.json`
4. Calls `list-wallets`, `get-aggregate-balance`, and `get-token-holdings` to scan portfolio state
5. Reports its startup summary and begins the heartbeat cycle

### Heartbeat Cycle (Every 30 Minutes)

The agent follows the procedure in `HEARTBEAT.md`:
1. Checks all open positions
2. Evaluates exit conditions (stop-loss, take-profit, trailing stop, time decay, risk deterioration)
3. Scans for new opportunities (if configured and circuit breaker is inactive)
4. Compiles and logs a portfolio summary
5. Reports any alerts

### User Interaction

Between heartbeats, you can give the agent direct instructions:
- "Buy 0.3 SOL of [mint address]"
- "Sell all my holdings of [mint]"
- "Check the risk metrics for [mint]"
- "What's my current portfolio?"
- "Increase max position size to 1 SOL"
- "Pause trading"

The agent will follow the safety checklist from `SOUL.md` for any buy instruction, even if given directly.

## Connecting via HTTP (Alternative)

If you prefer a remote MCP connection instead of a local stdio process, update `openclaw.json`:

```json
{
  "mcpServers": {
    "openpump": {
      "url": "https://mcp.openpump.io/mcp",
      "headers": {
        "Authorization": "Bearer ${OPENPUMP_API_KEY}"
      }
    }
  }
}
```

This connects to the hosted OpenPump MCP server without running a local Node.js process.

## Troubleshooting

### "OPENPUMP_API_KEY not set"

Set the environment variable before starting OpenClaw:
```bash
export OPENPUMP_API_KEY="op_sk_live_YOUR_KEY_HERE"
```

### "WALLET_NOT_FOUND" errors

The agent needs at least one wallet. It will create one automatically on first run. If errors persist, run `list-wallets` to check the current state.

### "INSUFFICIENT_BALANCE" on trades

The trading wallet needs SOL. Use `get-wallet-deposit-address` to get the deposit address and send SOL from an external wallet.

### Tool calls timing out

The OpenPump MCP server connects to Solana RPC nodes. During high congestion, requests may be slow. The agent will retry once with a higher priority level before logging and moving on.

### Circuit breaker activated

The agent will log "Circuit breaker activated" and pause new buys. Existing positions are still monitored (stop-losses still fire). The cooldown lasts 1 hour (2 heartbeat cycles).

## Disclaimer

This agent trades real SOL on the Solana blockchain. Memecoin trading is extremely risky. You can lose your entire investment. The agent's risk parameters reduce but do not eliminate the possibility of loss. Never trade with funds you cannot afford to lose. Not available to US persons. Use at own risk.

## Links

- [OpenPump](https://openpump.io) -- Platform and API key management
- [OpenPump Docs](https://docs.openpump.io) -- API documentation
- [@openpump/mcp](https://www.npmjs.com/package/@openpump/mcp) -- npm package
- [OpenClaw](https://github.com/openclaw/openclaw) -- Agent framework
