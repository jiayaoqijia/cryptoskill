---
name: katbot-trading
version: 0.5.0
description: Live crypto trading on Hyperliquid via Katbot.ai. Signal-triggered research → recommendation → execution workflow with Market Intelligence, research, and configurable signal monitoring.
# Note: Homepage URL removed to avoid GitHub API rate limit errors during publish
metadata:
  {
    "openclaw":
      {
        "emoji": "📈",
        "requires": { "bins": ["python3", "openclaw"], "env": ["KATBOT_HL_AGENT_PRIVATE_KEY"] },
        "primaryEnv": "KATBOT_HL_AGENT_PRIVATE_KEY",
        "install": "pip install -r requirements.txt"
      }
  }
---

# Katbot Trading Skill

This skill teaches the agent how to use the Katbot.ai API to manage a Hyperliquid trading portfolio through a signal-driven research pipeline.

## Portfolio Types

| Type | Description |
|------|-------------|
| `HL_PAPER` | Paper trading on Hyperliquid (no real funds). Formerly called `PAPER`. |
| `HYPERLIQUID` | Live trading on Hyperliquid (agent key required, builder fee must be approved). |

## Workflow

```
Setup → Configure Signal Triggers → Signal fires → Market Intel enrichment
     → Research → (user confirms apply?) → Recommendation → (user confirms) → Execution → Monitor
```

## Capabilities

1. **Signal Triggers**: Configurable 10-minute-cadence monitor over Katbot Market Intelligence. Fires on clear Momentum, Volume-Breakout, Whale-Activity, or Trending signals and auto-starts the research→recommendation workflow.
2. **Market Intelligence**: Read trending tokens, sentiment, whale flow/activity, and composite token intelligence from `/market-intelligence/*`. Used by the signal trigger and as enrichment context for recommendations.
3. **Research**: Run Katbot AI research tasks (momentum, volume, whale activity, etc.) and reuse non-expired results to seed recommendations.
4. **Recommendations**: Get AI-powered trade setups (Entry, TP, SL, Leverage). **Requires a primary agent assigned to the portfolio.**
5. **Execution**: Execute and close trades on Hyperliquid with user confirmation.
6. **Portfolio Tracking**: Monitor open positions, uPnL, balances, timeseries, and chain info.
7. **Agent Management**: Create, configure, and assign AI agents to portfolios.
8. **Conversation History**: View and clear agent conversation history per portfolio.
9. **Subscription & Plans**: Check feature usage limits and available plans.

## Tools

**All tool scripts live exclusively in `{baseDir}/tools/`** — this is the single canonical location. There are no copies elsewhere in the project. Always reference tools via `{baseDir}/tools/<script>` and set `PYTHONPATH={baseDir}/tools` so inter-tool imports resolve correctly.

Dependencies are listed in `{baseDir}/requirements.txt`.

- `ensure_env.sh`: **Run before any tool.** Checks if dependencies are installed for the current skill version and re-installs if needed. Safe to call every time — it exits immediately if already up to date.
- `katbot_onboard.py`: **First-time setup wizard.** Authenticates via SIWE using your Wallet Key, creates/selects a portfolio, and saves credentials locally to the secure identity directory.
- `katbot_trigger_setup.py`: **Signal trigger configuration wizard.** Run after onboarding to configure which market-intelligence signal types (Momentum, Volume Breakout, Whale Activity, Trending) should fire the research→recommendation workflow. Can be re-run anytime to reconfigure.
- `katbot_signal_trigger.py`: **10-minute cadence tick runner.** Evaluates configured signals and fires alerts + workflow when a signal is clear. Run via cron or openclaw schedule.
- `katbot_client.py`: Core API client. Handles authentication, portfolio management, research, market intelligence, recommendations, and trade execution. Also usable as a CLI script.
- `katbot_workflow.py`: Signal-driven research → recommendation workflow. Accepts signal context and orchestrates market-intel enrichment, research run/reuse, and recommendation request.

> **Note for contributors**: The `scripts/` directory contains only publish tooling (`publish.sh`, `publish.py`, etc.). Do NOT add copies of tool scripts there — all trading logic lives solely in `{baseDir}/tools/`.

## Signal Triggers

Signal triggers replace manual market analysis. They run on a 10-minute cadence and evaluate four signal types using Katbot Market Intelligence data.

### Setup

```bash
# Run once after onboarding (or any time to reconfigure)
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_trigger_setup.py
```

The wizard will:
1. Confirm portfolio and primary agent.
2. Ask which signal types to enable (Momentum, Volume Breakout, Whale Activity, Trending).
3. Set thresholds for each enabled signal.
4. Ask for alert channel/target.
5. Write `~/.openclaw/workspace/katbot_signal_trigger.json` (mode 600).
6. Print a ready-to-paste cron line.

### Signal Types

| Signal | Source | Fires when |
|--------|--------|-----------|
| **Momentum** | `/market-intelligence/sentiment` | Sentiment delta for ≥ N tokens crosses threshold |
| **Volume Breakout** | `/market-intelligence/trending` | Article-volume Z-score ≥ threshold |
| **Whale Activity** | `/market-intelligence/whale-flow` | Whale net-flow magnitude ≥ threshold USD |
| **Trending** | `/market-intelligence/trending` | New token with article volume ≥ threshold not in portfolio |

### Trigger Config Schema

`~/.openclaw/workspace/katbot_signal_trigger.json`:

```json
{
  "version": 1,
  "portfolio_id": 123,
  "agent_id": 45,
  "notify": { "channel": "telegram", "target": "..." },
  "signals": {
    "momentum":        { "enabled": true,  "threshold_abs": 0.6, "min_tokens": 2 },
    "volume_breakout": { "enabled": true,  "z_score_threshold": 2.0 },
    "whale_activity":  { "enabled": true,  "min_net_flow_usd": 500000 },
    "trending":        { "enabled": true,  "min_article_volume": 10 }
  },
  "auto_start_workflow": true,
  "auto_execute_trade":  false
}
```

### Running the Trigger

```bash
# Dry run — prints what would fire, no alerts or workflow
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_signal_trigger.py --dry-run

# Force fire (bypasses dedup — for testing)
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_signal_trigger.py --force

# Normal run
bash {baseDir}/tools/ensure_env.sh {baseDir}
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_signal_trigger.py
```

### Suggested Cron Line (10-minute cadence)

```
*/10 * * * * bash {baseDir}/tools/ensure_env.sh {baseDir} && PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_signal_trigger.py >> /tmp/katbot_trigger.log 2>&1
```

Replace `{baseDir}` with the absolute path to the skill directory.

## Market Intelligence `[local only]`

Read-only signal feeds from Katbot. Synchronous GETs — no ticket/polling required. These calls degrade gracefully: a failure must never block the trading pipeline.

```python
# Trending tokens by article volume
trending = get_trending_tokens(token)
trending = get_trending_tokens(token, limit=20)

# LLM-enriched news with sentiment
articles = get_intelligence_articles(token, limit=10)

# Aggregated sentiment across tokens
sentiment_list = get_aggregated_sentiment(token)

# Detailed sentiment for one token
btc_sentiment = get_token_sentiment(token, "BTC")

# Whale position flow per token
whale_flow = get_whale_flow(token)
whale_flow = get_whale_flow(token, symbol="ETH")

# Individual whale activity events
whale_events = get_whale_activity(token)

# Composite intelligence (news + whale)
intelligence = get_token_intelligence(token)
intelligence = get_token_intelligence(token, symbol="SOL")
```

### Market Intelligence CLI

```bash
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_client.py trending [--limit N]
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_client.py articles [--limit N]
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_client.py sentiment [--symbol BTC]
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_client.py whale-flow [--symbol ETH]
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_client.py whale-activity [--symbol SOL]
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_client.py token-intelligence [--symbol BTC]
```

## Research `[local only except run_research]`

Research tasks are agent-driven analyses. Results expire — always prefer reusing a non-expired result over running a new one unnecessarily.

> `apply_research_result` mutates `portfolio.tokens_selected`. **Always ask the user before calling it.**

```python
# Run a new research task (async)
ticket = run_research(token, portfolio_id,
    symbol="BTC",           # Optional: focus on a specific token
    time_horizon="medium",  # Optional: "short", "medium", "long"
    risk_profile="medium"   # Optional: "low", "medium", "high"
)
# ticket = {"ticket_id": "...", "status": "PENDING"}

# Poll for completion (up to 120s)
result = poll_research(token, portfolio_id, ticket["ticket_id"], max_wait=120)
# result = {"ticket_id": "...", "status": "COMPLETED"|"FAILED", "done": True, "result": {...}}

# List non-expired results
results = list_research_results(token, portfolio_id)

# Get one result
result = get_research_result(token, portfolio_id, result_id)

# Delete a result
result = delete_research_result(token, portfolio_id, result_id)

# Apply token selection to portfolio — REQUIRES EXPLICIT USER CONFIRMATION
result = apply_research_result(token, portfolio_id, result_id)
# Returns: {"success": True, "tokens_selected": [...], ...}

# Research configuration (per-agent)
configs = list_research_configs(token, agent_id)
config  = get_research_config(token, agent_id, config_id)
config  = create_research_config(token, agent_id, payload)
config  = update_research_config(token, agent_id, config_id, payload)
result  = delete_research_config(token, agent_id, config_id)
```

### Research CLI

```bash
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_client.py run-research [--symbol BTC] [--time-horizon short|medium|long] [--risk-profile low|medium|high]
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_client.py poll-research <ticket_id>
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_client.py list-research-results
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_client.py get-research-result <result_id>
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_client.py delete-research-result <result_id>
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_client.py apply-research-result <result_id>
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_client.py list-research-configs <agent_id>
```

## Workflow Tool Usage

The workflow runs the full pipeline from a signal context:

```bash
# Manual run (no signal trigger)
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_workflow.py \
  --signal-type manual \
  --tokens BTC,ETH \
  --rationale "Manual analysis run"

# With risk and horizon settings
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_workflow.py \
  --signal-type whale_activity \
  --tokens SOL \
  --risk-profile medium \
  --time-horizon short

# Skip enrichment (faster, less context)
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_workflow.py \
  --signal-type manual --no-enrich

# Always run fresh research (ignore existing results)
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_workflow.py \
  --signal-type manual --no-reuse-research
```

## Environment Variables

**Normal operation requires only `KATBOT_HL_AGENT_PRIVATE_KEY`.** The skill reads this from `katbot_secrets.json` automatically after onboarding, so it does not need to be set in the environment at all during day-to-day use.

`WALLET_PRIVATE_KEY` is **not** a runtime requirement. It is an emergency fallback used only when both the access token and refresh token have expired and the session must be fully re-established. It must never be pre-set in the environment — supply it interactively only when onboarding or re-onboarding explicitly requires it.

| Variable | When needed | Description |
|----------|-------------|-------------|
| `KATBOT_HL_AGENT_PRIVATE_KEY` | First run only (if not yet onboarded) | Agent private key for Hyperliquid trade execution. Onboarding saves it to `katbot_secrets.json` (mode 600). After that the skill loads it from the secrets file automatically — **no env var needed for daily operation.** |
| `WALLET_PRIVATE_KEY` | Emergency re-auth only | MetaMask wallet key. Used only for SIWE login when session tokens are fully expired. **Never pre-set this in the environment. Never export to a shell profile. Provide interactively only when re-onboarding is required.** |
| `KATBOT_BASE_URL` | Optional override | API base URL. Default: `https://api.katbot.ai` |
| `KATBOT_IDENTITY_DIR` | Optional override | Path to identity files directory. Default: `~/.openclaw/workspace/katbot-identity` |
| `CHAIN_ID` | Optional override | EVM chain ID. Default: `42161` (Arbitrum) |
| `OPENCLAW_NOTIFY_CHANNEL` | Required for alerting | The openclaw channel name for signal trigger alerts (e.g. `telegram`, `slack`, `discord`). If unset, alerts print to stdout. The trigger wizard stores this in `katbot_signal_trigger.json` so cron invocations don't need it in the shell. |
| `OPENCLAW_NOTIFY_TARGET` | Required for alerting | The target ID within the channel (e.g. a chat ID or user handle). Must be set together with `OPENCLAW_NOTIFY_CHANNEL`. Stored in trigger config. |

### `.env` File Loader — CLI/Development Use Only

`katbot_client.py` contains a `.env` file loader for CLI use outside OpenClaw (`tubman-bobtail-py` mode). At import time it searches these paths for a `katbot_client.env` file:

1. `{projectRoot}/env/local/katbot_client.env`
2. `{baseDir}/../env/local/katbot_client.env`
3. `{baseDir}/tools/katbot_client.env`

If a file is found, it loads **only non-secret config** from it: `KATBOT_BASE_URL`, `KATBOT_IDENTITY_DIR`, and `CHAIN_ID`. Private keys (`WALLET_PRIVATE_KEY` and `KATBOT_HL_AGENT_PRIVATE_KEY`) are explicitly **not** read from `.env` files — they must come from the environment or the identity directory only.

**Agent rules:**
- **NEVER** create or suggest creating a `katbot_client.env` containing private keys.
- **NEVER** place `WALLET_PRIVATE_KEY` or `KATBOT_HL_AGENT_PRIVATE_KEY` in any `.env` file.
- A `katbot_client.env` is acceptable only for non-secret config (`KATBOT_BASE_URL`, `CHAIN_ID`, `KATBOT_IDENTITY_DIR`, `PORTFOLIO_ID`, `WALLET_ADDRESS`).

## Identity Files

All persistent credentials are stored in `KATBOT_IDENTITY_DIR` (default: `~/.openclaw/workspace/katbot-identity/`). This directory is **outside the project tree** deliberately — its contents are never committed to git.

| File | Mode | Contents |
|------|------|----------|
| `katbot_config.json` | 644 | `base_url`, `wallet_address`, `portfolio_id`, `portfolio_name`, `chain_id` |
| `katbot_token.json` | 600 | `access_token`, `refresh_token` |
| `katbot_secrets.json` | 600 | `agent_private_key` |

The trigger config lives outside `KATBOT_IDENTITY_DIR` by design (it holds no secrets):

| File | Mode | Contents |
|------|------|----------|
| `~/.openclaw/workspace/katbot_signal_trigger.json` | 600 | portfolio/agent IDs, notify config, signal thresholds |
| `~/.openclaw/workspace/memory/katbot_signal_state.json` | 644 | last-fire timestamps per signal+token (auto-managed by trigger) |

`katbot_client.py` reads all three identity files automatically. The agent key is loaded from `katbot_secrets.json` if `KATBOT_HL_AGENT_PRIVATE_KEY` is not set in the environment.

**Security properties of identity files:**
- `katbot_token.json` and `katbot_secrets.json` are written with mode 600 (owner read/write only).
- `WALLET_PRIVATE_KEY` (MetaMask key) is **never** written to any identity file — it is used only in-memory during onboarding and authentication.
- If `~/.openclaw/workspace/katbot-identity/` is compromised, an attacker gains the agent trading key and session tokens but **not** the MetaMask wallet key, limiting the blast radius to funds accessible via the Hyperliquid agent wallet.

## Authentication Flow

The skill manages tokens automatically via `katbot_client.get_token()`. **Never call this manually** — all API functions call it internally.

1. **Check access token**: Decode the JWT `exp` claim from `katbot_token.json`. If valid (not expiring within 60s), use it directly.
2. **Refresh if expired**: If the access token is expired, call `POST /refresh` with `{"refresh_token": "<token>"}`. The API **rotates** the refresh token on every call — both the new `access_token` and new `refresh_token` are written to `katbot_token.json` (mode 600) immediately. The old refresh token is invalid as soon as the response arrives.
3. **Re-authenticate if refresh fails**: If the refresh token is missing or the `/refresh` call fails, fall back to full SIWE re-authentication via `POST /login`. This requires `WALLET_PRIVATE_KEY`.

**Never call `/login` if `/refresh` can succeed first.**

Refresh tokens are opaque (not JWTs) and expire after **7 days of inactivity**. If the session is fully expired, re-run onboarding.

## Credential Transmission Notice

> **The agent must present this notice to the user and obtain acknowledgement before running onboarding or any trading operation for the first time.**

This skill transmits the **agent trading private key** (`KATBOT_HL_AGENT_PRIVATE_KEY`) to the remote Katbot API (`api.katbot.ai`) on certain calls. This is required for the API to sign and submit trades on-chain via Hyperliquid.

**What leaves your machine and when:**

| Credential | Sent to | On which calls | Why |
|------------|---------|----------------|-----|
| `KATBOT_HL_AGENT_PRIVATE_KEY` | `api.katbot.ai` | `request_recommendation`, `execute_recommendation`, `close_position`, `get_portfolio_timeseries` — in the `X-Agent-Private-Key` header and/or the JSON request body | The Katbot API uses it to sign Hyperliquid on-chain transactions on your behalf |
| `access_token` / `refresh_token` | `api.katbot.ai` | All authenticated API calls — in the `Authorization: Bearer` header | Session authentication |
| `WALLET_PRIVATE_KEY` | Never sent remotely | Used only locally to sign the SIWE message during onboarding/re-auth | Signature is computed locally; only the resulting signature is sent |

**What this means:**
- The agent trading key is a high-value credential. Once transmitted, the Katbot API server has access to it for the duration of the request.
- The MetaMask wallet key (`WALLET_PRIVATE_KEY`) is **never transmitted** — it signs a message locally and the signature alone is sent.
- If you do not trust `api.katbot.ai` with your agent trading key, do not use this skill.

**Agent instruction:** Before running onboarding or any recommendation/execution call for the first time in a session, inform the user: *"This skill will send your Hyperliquid agent private key to api.katbot.ai to authorize on-chain trades. Do you want to proceed?"* Do not proceed without affirmative confirmation.

## `katbot_client.py` API Reference

All functions require a `token` argument obtained from `get_token()`.

**Key transmission legend used below:**
- `[key→remote]` — the agent private key is sent to `api.katbot.ai` in this call
- `[local only]` — no private key is transmitted; only the JWT bearer token is sent

### Authentication `[local only]`
```python
token  = get_token()    # Returns valid access token (refreshes automatically)
config = get_config()   # Returns dict from katbot_config.json
```

### Portfolio `[local only unless noted]`
```python
portfolios = list_portfolios(token)

# Create a paper portfolio (HL_PAPER) or live portfolio (HYPERLIQUID)
portfolio = create_portfolio(
    token, name,
    portfolio_type="HL_PAPER",  # "HL_PAPER" or "HYPERLIQUID" (was "PAPER")
    is_testnet=True,             # Always True for safety; set False for mainnet
    amount=10000.0,              # Initial USD balance (paper only, ignored for HYPERLIQUID)
    primary_agent_id=None,       # Optional: assign an agent immediately on creation
    arbitrum_rpc_url=None,       # Optional: custom Arbitrum RPC URL
)

portfolio = get_portfolio(token, portfolio_id, require_agent=True)
# Returns full PortfolioInfo: positions, PnL, risk metrics, active_agent, etc.
# require_agent=False for paper portfolios that don't need the agent key.

updated = update_portfolio(token, portfolio_id,
    name=None, tokens_selected=["BTC","ETH","SOL"], max_history_messages=None)

result  = delete_portfolio(token, portfolio_id)

# Portfolio metadata
tokens     = get_portfolio_tokens(token, portfolio_id)      # ["BTC","ETH","SOL",...]
chain_info = get_portfolio_chain_info(token, portfolio_id)  # {chain_id, is_testnet, network_name}

# Timeseries data [key→remote for HYPERLIQUID]
ts = get_portfolio_timeseries(
    token, portfolio_id,
    granularity="1h",   # "1m","5m","15m","1h","4h","1d","1w","1M"
    limit=100,
    window="24H"        # "24H","7D","30D"
)

# Hyperliquid-specific
result = validate_hyperliquid(token, agent_private_key=None, is_testnet=True)
result = approve_builder_fee(token, portfolio_id, action, signature, nonce)
# Note: approve_builder_fee is called after the frontend signs EIP-712; not a routine agent call.
```

### Recommendations `[key→remote]`
> The agent private key is sent in the JSON body of `request_recommendation`.
> A **primary agent must be assigned to the portfolio** before calling this — the API returns HTTP 422 otherwise.
> Confirm user consent before calling.

```python
ticket = request_recommendation(
    token, portfolio_id, message,
    agent_id=None  # Optional: select a specific agent; uses portfolio primary if None
)
# ticket = {"ticket_id": "...", "status": "PENDING"}

result = poll_recommendation(token, ticket["ticket_id"], max_wait=60)
# result = {"ticket_id": "...", "status": "COMPLETED"|"FAILED", "done": True, "response": {...}, "error": None}

recs = get_recommendations(token, portfolio_id)   # List saved recommendations
```

#### Foreign Recommendation Response (openclaw/katpack)
```python
# Submit another agent's recommendation for analysis
ticket = submit_recommendation_response(
    token, portfolio_id,
    recommendation={
        "agent_name": "...", "symbol": "ETH", "action": "BUY",
        "confidence": 0.8, "entry_price": 3000.0,
        "take_profit_pct": 5.0, "stop_loss_pct": 2.0,
        "rationale": "...", "katbot_portfolio_id": portfolio_id
    },
    pack_goals=None,   # Optional katpack goals string
)
result = poll_recommendation_response(token, ticket["ticket_id"], max_wait=60)
```

### Trade Execution `[key→remote]`
> Always require explicit user confirmation before calling `execute_recommendation` or `close_position`.

```python
# Execute a saved recommendation [key→remote]
result = execute_recommendation(
    token, portfolio_id, rec_id,
    execute_onchain=False,      # True to submit to Hyperliquid on-chain
    user_master_address=None    # Optional: override wallet address
)

# Close an open position [key→remote]
result = close_position(
    token, portfolio_id, "ETH",
    reason="Manual close via agent",   # Optional reason string
    execute_onchain=False,
    user_master_address=None
)

# List trades and events [local only]
trades = list_trades(token, portfolio_id)
events = get_position_events(token, portfolio_id, limit=20, event_type=None)
# event_type: "TP_HIT" | "SL_HIT" | "LIQUIDATED" | "MANUAL_CLOSE"
```

### Agent Management `[local only]`
> A portfolio **must have a primary agent assigned** before `request_recommendation` will succeed.

```python
# CRUD
agents = list_agents(token)
agent  = create_agent(token, name, max_history_messages=10)
# name must be a slug: lowercase letters/numbers/hyphens; server appends a 6-char suffix
agent  = get_agent(token, agent_id)
agent  = update_agent(token, agent_id, name=None, max_history_messages=None, avatar_seed=None)
result = delete_agent(token, agent_id)   # fails if agent is primary on any portfolio

# Search (cross-user, for invite flow — min 3 chars)
results = search_agents(token, q="my-agent", portfolio_id=None)

# Portfolio assignments
assignment = get_portfolio_agent(token, portfolio_id)       # Get active primary agent
assignments = list_portfolio_agents(token, portfolio_id)    # All agents (primary + observers)
assignment = assign_agent(token, portfolio_id, agent_id, role="primary")
result     = unassign_agent(token, portfolio_id, agent_id)
```

### Agent Observer Invitations `[local only]`
```python
invite   = create_agent_invitation(token, portfolio_id, agent_id)
invites  = list_portfolio_invitations(token, portfolio_id)
pending  = list_pending_invitations(token)    # Invitations for agents you own
result   = respond_to_invitation(token, agent_id, invitation_id, action="accepted")
# action: "accepted" or "rejected"
observed = list_observer_portfolios(token)   # Portfolios you observe via accepted invite
```

### Conversation History `[local only]`
```python
history = get_conversation(token, portfolio_id)
# {"exists": True, "message_count": N, "conversation": [...], ...}

result = delete_conversation(token, portfolio_id)  # Clear history, preserve portfolio state
```

### User & Subscription `[local only]`
```python
user  = get_user(token)   # {sub, id, is_whitelisted, subscription, plan, feature_usage}
plans = get_plans()       # No auth required; list of subscription plans
```

### CLI Mode
`katbot_client.py` can be run as a standalone script (reads `PORTFOLIO_ID` from `.env` or environment):

```bash
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_client.py portfolio-state
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_client.py recommendations
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_client.py request-recommendation "Analyze and recommend"
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_client.py poll-recommendation <ticket_id>
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_client.py execute <rec_id>
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_client.py close-position ETH
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_client.py list-agents
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_client.py get-agent <agent_id>
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_client.py list-portfolio-agents
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_client.py assign-agent <agent_id> [--role primary|observer]
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_client.py conversation
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_client.py clear-conversation
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_client.py user
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_client.py plans
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_client.py tokens
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_client.py chain-info
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_client.py update-portfolio --tokens BTC,ETH,SOL [--name "New Name"]
```

## Usage Rules

- **ALWAYS** present the Credential Transmission Notice and obtain user acknowledgement before the first onboarding or trading operation in any session.
- **ALWAYS** check for a non-expired research result (or run one) before calling `request_recommendation` for a new trade idea. Include the research result summary / ID (and market-intelligence signals that triggered it) in the recommendation message.
- **ALWAYS** explicitly ask the user ("Apply this research result to your portfolio token selection?") before calling `apply_research_result`. Never auto-apply — it mutates `portfolio.tokens_selected`.
- **NEVER** execute a trade without explicit user confirmation (e.g., "Confirm execution of LONG AAVE?").
- **NEVER** log, print, or reveal any private key or token value in the chat.
- **ALWAYS** report the risk/reward ratio and leverage for any recommendation.
- **ALWAYS** let `get_token()` handle token refresh automatically — do not manually manage tokens.
- **ALWAYS** verify a primary agent is assigned to the portfolio before calling `request_recommendation`. If the API returns HTTP 422 ("No primary agent assigned"), guide the user to create an agent and call `assign_agent()` first.
- **NEVER** use the old portfolio type `"PAPER"` — it has been renamed to `"HL_PAPER"`. Always use `"HL_PAPER"` for paper trading.
- **NEVER** execute live trades on a mainnet HYPERLIQUID portfolio unless `builder_fee_approved` is `True` in the portfolio info. If it is `False`, inform the user they must complete the builder fee approval step.
- **NEVER** enable `auto_execute_trade: true` in `katbot_signal_trigger.json` without a clear, informed user choice — it causes unattended trade execution.
- **NEVER** block the trigger or workflow on a failed market-intelligence call — log a warning and proceed. Market-intel feeds enrich but do not gate the pipeline.
- **NEVER** pre-set `WALLET_PRIVATE_KEY` in the environment. It is an emergency re-auth key only. If the agent detects it already set in the environment outside of an active onboarding/re-auth session, warn the user and suggest unsetting it.
- **NEVER** create a `katbot_client.env` file containing `WALLET_PRIVATE_KEY` or `KATBOT_HL_AGENT_PRIVATE_KEY`. The `.env` loader will not inject private keys into the process, but placing them in such a file is still a bad practice that stores secrets on disk unnecessarily.
- **NEVER** suggest exporting any private key to a shell profile or persistent environment file.
- **NEVER** read, display, or summarize the contents of `katbot_token.json`, `katbot_secrets.json`, or any file in the identity directory.

## Environment Management

This skill tracks its installed dependency version using a stamp file at `{baseDir}/.installed_version`. When the skill is upgraded, the stamp version will not match the skill version, and `ensure_env.sh` will automatically re-run `pip install`.

**The agent MUST run `ensure_env.sh` before every tool invocation:**

```bash
bash {baseDir}/tools/ensure_env.sh {baseDir}
```

- If the stamp matches the current version: exits immediately (fast, no pip call).
- If the skill was upgraded or never installed: runs `pip install -r requirements.txt` and writes the new stamp.
- If `python3` is missing: prints a clear error and exits with code 1.

If a tool fails with `ImportError` or `ModuleNotFoundError`, always run `ensure_env.sh` first to sync dependencies before retrying.

## First-Time Setup (Install)

```bash
# 1. Install dependencies
bash {baseDir}/tools/ensure_env.sh {baseDir}

# 2. Run onboarding wizard (interactive)
python3 {baseDir}/tools/katbot_onboard.py

# 3. Configure signal triggers (interactive)
PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_trigger_setup.py
```

The onboarding wizard will:
1. Prompt for `WALLET_PRIVATE_KEY` (hidden input — never stored to disk).
2. Authenticate with api.katbot.ai via SIWE.
3. List existing portfolios or create a new Hyperliquid one.
4. Save `KATBOT_HL_AGENT_PRIVATE_KEY`, `katbot_config.json`, and `katbot_token.json` to `~/.openclaw/workspace/katbot-identity/`.
5. Print instructions for authorizing the agent wallet on Hyperliquid.

After onboarding, run the trigger setup wizard to configure which signal types should fire the workflow.

## Upgrade

When the skill is updated (new version published to clawhub):

```bash
# Re-run ensure_env.sh — it detects the version change and re-installs dependencies
bash {baseDir}/tools/ensure_env.sh {baseDir}
```

No re-onboarding is needed for upgrades. The identity files in `~/.openclaw/workspace/katbot-identity/` are preserved across upgrades. If a tool fails after upgrade, run `ensure_env.sh` first.
