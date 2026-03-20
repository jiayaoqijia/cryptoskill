# Coinpilot Hyperliquid Copy Trade Skill

Use this skill to access and control Coinpilot, allowing you to discover, investigate, and copy-trade top on-chain traders on Hyperliquid in real time with low execution latency.

It supports non-custodial wallet infrastructure, near-instant execution, and real-time position management with advanced trading controls.

Runtime use requires a local credentials JSON containing a Coinpilot API key, a
Privy user ID, one primary wallet private key, and 9 follower wallet private
keys. The API key and private keys are high-sensitivity secrets; the `userId` is
a required identifier. The install/runtime metadata points to the local file
path; the secrets themselves remain inside that local file. The CLI reads a
fixed user-home config path.

## What this skill does

Connect your agent to Coinpilot to mirror top-performing Hyperliquid traders through a discovery and execution engine.

- **Elite Trader Discovery**: Access Coinpilot's proprietary curation using multi-factor analysis.
- **Wallet Management and Tracking**: Track and monitor specific wallet addresses directly, including wallets not currently on the leaderboard.
- **Sub-Second Mirroring**: Real-time trade detection with next-block execution through the Coinpilot engine.
- **Parallel Copying**: Manage up to 9 independent sub-portfolios simultaneously to prevent position offsetting.
- **Advanced Risk Management**: Set automated take profit (TP) and stop loss (SL) at both subscription and position levels.
- **Self-Custodial Execution**: Powered by Privy. Your keys, your crypto.

Full platform functions are documented at <https://docs.coinpilot.com/>.

## Setup Instructions

### 1) Prepare your Coinpilot account

1. Download Coinpilot on [App Store or Google Play](https://refer.coinpilot.com/7ef646).
2. Create an account and fund your trading account.
3. Obtain your Coinpilot **API Key** and **Privy User ID** by opening a ticket in the [Coinpilot Discord](https://discord.com/invite/UTfdDcMTHH).

### 2) Install the skill

You can install this skill using either method below.

#### Option A: ClawHub

```bash
npx clawhub install coinpilot-hyperliquid-copy-trade
```

#### Option B: Skills CLI (`skills.sh`)

```bash
# Install the Skills CLI (https://skills.sh/)
npm install -g skills

# Add Coinpilot skill to your instance
npx skills add https://github.com/coinpilot-labs/skills -g -y --skill coinpilot-hyperliquid-copy-trade
```

### 3) Create your local credentials file

Create a local credentials file (for example `coinpilot.json`) with your
credentials and wallet metadata:

```json
{
  "apiBaseUrl": "https://api.coinpilot.bot",
  "apiKey": "your-experimental-api-key",
  "userId": "did:privy:your-user-id",
  "wallets": [
    {
      "index": 0,
      "address": "0x-primary",
      "privateKey": "0x-key-0",
      "isPrimary": true
    },
    {
      "index": 1,
      "address": "0x-sub-1",
      "privateKey": "0x-key-1",
      "isPrimary": false
    },
   ...
    {
      "index": 9,
      "address": "0x-sub-9",
      "privateKey": "0x-key-9",
      "isPrimary": false
    }
  ]
}
```

Use the template in `assets/coinpilot.template.json` and keep this file private.
Provide exactly 9 subwallets (10 total wallets including the primary).

Credentials path on all supported platforms:

- `~/.coinpilot/coinpilot.json`

This file contains high-sensitivity secrets (API key and private keys):

- Never commit it to Git or share it publicly.
- Keep it on your own machine and let only a trusted local agent runtime read it by path.
- Do not paste the populated file or any private keys into chat, tickets, or shared docs.
- Do not pass private keys as CLI flags. Use wallet selectors such as
  `--follower-index`, `--follower-wallet`, or `--use-prepare-wallet` so the
  helper loads keys from the local credentials file in memory.
- Do not use repo-local or relative-path credential files. Keep `coinpilot.json`
  at the fixed user-home config path only.
- The only supported API base URL source is `coinpilot.json.apiBaseUrl`, and it
  must match the script allowlist.

Runtime trading actions require the secrets stored inside that local credentials file.

Coinpilot API calls from this skill require `x-api-key`, `x-wallet-private-key`,
and `x-user-id`, which are sourced from this credentials file.

### 4) Connect and verify

1. Configure your local agent runtime (OpenClaw or equivalent) to use the fixed user-home config path.
2. Do not paste the credentials JSON into chat; keep it as a local file reference only.
3. Verify integration with a balance query, for example:
   - "What is my current balance on Coinpilot?"

## Use Cases and Example Prompts

Use natural language to automate and optimize your strategy:

- **Discover and Recommend**: "Find traders in Coinpilot metrics with Sharpe ratio > 2.0 and drawdown < 15% over 30D, rank them by Sharpe and consistency, and recommend the top 3 to copy."
- **Start with Guardrails**: "Start copying wallet 0x123... with 500 USDC on sub-wallet 1, set a 10% stop loss and 30% take profit, and alert me when the subscription is live."
- **Auto-Adjust Risk Settings**: "Monitor this subscription and tighten stop loss to 5% if volatility increases, then update max leverage limits."
- **Scheduled Status**: "Send me a portfolio health update every hour with active subscriptions, PnL, risk alerts, and current Coinpilot balance."
- **Proactive Portfolio Management**: "Monitor my portfolio every hour, rebalance by stopping weaker subscriptions and starting stronger replacements, and execute the required config or position actions based on my rules."
- **Subscription Health Audit**: "Audit all active subscriptions and flag any with weak performance, high drawdown, or stale activity."
- **Position-Level Risk Intervention**: "If any single position exceeds my loss threshold, close that position only and keep the subscription active."
- **One-Click De-Risking**: "Close all positions for subscription X now, but keep the subscription configuration ready to restart later."
- **History and Attribution Review**: "Give me a weekly performance review by subscription with realized PnL, win/loss behavior, and key activity events."
- **Emergency Protection**: "If market volatility spikes across the market, close all open positions and stop all active subscriptions across all portfolios."

## Security and Transparency

- **Self-Custodial**: Privy-secured infrastructure ensures only you can control your funds.
- **On-Chain Verification**: Every trade can be verified on Hyperliquid Explorer.
- **0.05% Flat Fee**: Transparent platform fee per trade charged by Coinpilot.

For more details and full capabilities, visit the [Coinpilot documentation](https://docs.coinpilot.com/).

> Disclaimer: Trading perpetuals involves significant risk. This skill is an automation tool and does not constitute financial advice.
