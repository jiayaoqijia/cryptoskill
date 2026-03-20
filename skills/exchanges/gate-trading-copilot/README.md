# Gate Exchange Trading Copilot

## Overview

An AI Agent skill that orchestrates cryptocurrency trade judgment, risk control, and execution on Gate Exchange.

It combines analysis and execution into one closed loop:

`judge -> risk control -> order draft -> explicit confirmation -> execution -> post-trade management`

This skill is for users who want one skill to handle the full trading workflow instead of switching among separate market, news, risk, spot, and futures skills.

### Core Capabilities

| Capability | Description | Example |
|------------|-------------|---------|
| **Trade-decision orchestration** | Narrow a vague cryptocurrency trading request into one asset, one market, and one direction on Gate Exchange | `Can I buy BTC now?` |
| **Risk-aware Trading Brief** | Combine coin analysis, technicals, event explanation, microstructure, and token risk into one pre-trade brief | `ETH dumped. Analyze it first before I buy` |
| **Spot execution loop** | Draft -> confirm -> place -> verify -> manage a spot order on Gate Exchange | `If it looks fine, give me a spot buy draft` |
| **Futures execution loop** | Draft -> confirm -> open/close/reverse -> verify -> manage a USDT perpetual trade | `Check momentum and liquidation, then help me long ETH` |
| **Post-trade management** | Amend, cancel, verify fills, verify positions, partially close, or fully close | `Raise my unfilled buy order by 1%` |
| **Risk gating** | Convert pre-trade findings into `GO / CAUTION / BLOCK` before any order draft is created | `Check this newly listed token before I trade it` |

## Supported Scope

### Supported

- Spot buy / sell / market / limit / amend / cancel / fill verification
- USDT perpetual open / close / reverse / amend / cancel
- Market overview before a trade
- Single-coin analysis before a trade
- Technical analysis before a trade
- Event explanation before a trade
- Risk check for new coins / contract addresses
- Liquidity / slippage / momentum / liquidation / basis / funding checks

### Not Supported

- Options
- Alpha trading
- On-chain swap / bridge / DeFi execution
- Fully automatic trading without confirmation
- Bypassing compliance or risk controls
- Pretending to support TP/SL daemon-style auto triggering

## What Makes It Self-Contained

This skill is designed to work even when installed alone:

- It does not assume separate research or execution skills are installed
- It includes **analysis-side MCP mapping**
- It includes **execution-side MCP mapping**
- It defines a consistent intermediate artifact: **Trading Brief**
- It defines a consistent execution gate: **Order Draft + explicit confirmation**

## General Runtime Rules

This skill follows the shared exchange runtime rules:

- `../exchange-runtime-rules.md`

At the skill level, the key expectation is simple:

- analysis-side runtime must expose the referenced `info_*` and `news_*` tools
- execution-side runtime must expose the referenced `cex_spot_*` and `cex_fx_*` tools
- if those shared runtime gates are not satisfied, the skill must not overclaim analysis completeness or execution success
- if a named helper tool is absent in the current runtime, the skill must disclose the gap, use only the nearest valid fallback tools, and avoid overclaiming rankings, macro breadth, or automated fund-flow tracing
- if a tool returns sparse or low-signal payloads in the current runtime, the skill must downgrade it to supporting context instead of using it as the main analytical basis

Portable baseline mapping:

- `info_*` tools should map to Gate Info MCP
- `news_feed_*` tools should map to Gate News MCP
- read-only `cex_spot_*` / `cex_fx_*` market-data tools may come from Gate public market MCP or a local combined Gate MCP runtime
- private trading and account `cex_*` tools should map to authenticated Gate Exchange MCP or a local authenticated Gate MCP runtime

The skill should not require `news_events_*` to be present, because those tools are not part of the documented baseline news surface.

## Guardrail (Mandatory)

Before any real trade placement:

1. Produce a **Trading Brief**
2. Produce an **Order Draft**
3. Wait for explicit user confirmation in the immediately previous turn
4. Execute only after confirmation

If confirmation is missing, stale, ambiguous, or the parameters changed:

- do not execute
- stay in analysis / draft / query mode only

## Architecture

```text
gate-exchange-trading-copilot/
├── SKILL.md
├── README.md
├── CHANGELOG.md
└── references/
    ├── scenarios.md
    ├── routing-and-analysis.md
    └── execution-and-guardrails.md
```

This package references the shared runtime rules from `../exchange-runtime-rules.md`; that shared file is intentionally not duplicated inside this skill folder.

See `references/scenarios.md` for packaged scenario cases and representative prompt examples.

## Internal Composition

### Analysis Side

- market overview
- news briefing
- event explanation
- single-coin analysis
- trend analysis
- token risk check
- address tracing (when needed)
- microstructure analysis (liquidity / slippage / liquidation / funding / basis)

### Execution Side

- spot execution flow
- futures execution flow
- order / position management flow

## Typical Usage Examples

```text
"Check whether BTC is worth buying now. If yes, give me a spot order draft."
"ETH suddenly dumped. Explain why, check liquidity, and tell me whether I should buy the dip."
"I want to long ETH. Check momentum, liquidation, and funding first."
"This newly listed coin looks interesting. Check contract risk and tradability before giving me a small starter trade plan."
"Amend the buy order you helped me place earlier."
"Close half of my BTC perpetual position."
```

## Trigger Profile

Use this skill when the user wants **one skill** to complete:

- judgment
- risk control
- trade preparation
- trade execution
- post-trade follow-up

Typical trigger phrases:

- `analyze before buying`
- `check risk before trading`
- `help me decide whether to use spot or futures`
- `give me an order draft`
- `analyze then place order`
- `check risk then trade`
- `manage the order or position you just helped place`

## Safety Summary

- Never auto-trade without explicit confirmation
- Never bypass compliance, risk, or minimum order constraints
- Never present analysis as certainty
- Never produce an order draft after a `BLOCK` result
- For multi-leg trading, require draft + confirmation per leg
