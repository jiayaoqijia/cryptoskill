---
name: gate-exchange-trading-copilot
version: "2026.3.14-3"
updated: "2026-03-14"
description: 'End-to-end cryptocurrency trading copilot for Gate Exchange. Use this skill whenever the user wants one skill to complete market judgment, risk control, and execution for a cryptocurrency trade on Gate Exchange. Trigger phrases include "analyze before placing an order", "analyze before buying", "check risk before trading", or any request involving cryptocurrency trade judgment, order drafting, spot or futures execution, or post-trade management on Gate Exchange.'
---

# Gate Exchange Trading Copilot

This is an **L2 composite skill** for users who want a single skill to complete the full trading loop:

`judge the opportunity -> control risk -> produce order draft -> explicit confirmation -> execute -> verify/manage`

It is neither a pure research skill nor a pure execution skill. Its purpose is to provide a complete trading workflow inside one skill.

## General Rules

Read and follow the shared runtime rules before proceeding:
→ `../exchange-runtime-rules.md`

Before calling any named MCP tool, verify that the concrete tool name exists in the current runtime tool list. If a helper tool is absent, disclose the mismatch, use only the nearest valid fallback combination, and do not overclaim unavailable coverage such as rankings, macro breadth, or automated fund-flow tracing.

Also validate that the returned payload is rich enough for the intended analytical claim. If a tool returns sparse metadata, empty structures, or requires missing disambiguation inputs, treat it as supporting context only rather than primary evidence.

For portability across Gate MCP runtimes, treat the documented surfaces as the baseline:

- `info_*` -> Gate Info MCP
- `news_feed_*` -> Gate News MCP
- read-only `cex_spot_*` / `cex_fx_*` market-data calls -> Gate public market MCP or a local combined Gate MCP runtime
- private order / account / position `cex_*` calls -> authenticated Gate Exchange MCP or a local authenticated Gate MCP runtime

Do not make `news_events_*` a required dependency in scenario design, because it is not part of the documented baseline news surface.

---

Read `references/scenarios.md` for:

- representative user scenarios
- representative prompt examples
- expected tool-routing patterns

## Positioning

- For users who want to trade without switching across multiple skills
- Self-contained: can be installed alone and still understand both analysis and execution mapping
- Supports **spot trading** and **USDT perpetual futures**
- Supports post-trade **amend / cancel / close / verification**

## Suitable Scenarios

### Suitable

- The user already has a target asset and wants analysis before trading
  - `Check whether BTC is worth buying now, then give me a spot order draft`
  - `I want to long ETH, but check momentum, liquidation, and liquidity first`
- The user is triggered by news, abnormal moves, or new listings and wants to trade after analysis
  - `ETH just dumped. Explain why and tell me whether it is worth buying`
  - `This newly listed coin looks interesting. Check the risk before giving me a starter trade plan`
- The user already placed an order or opened a position and now wants management
  - `Raise my unfilled buy order by 1%`
  - `Close half of my BTC position`

### Not Suitable

- Pure market research with no trading goal
- Options, Alpha trading, on-chain swap, DeFi execution, copy trading, wealth products
- Fully automatic trading, skipping confirmation, bypassing compliance or risk controls

## Capability Boundary

### This skill can do

1. Recognize whether the user wants:
   - pre-trade judgment
   - judgment plus execution
   - order / position management
2. Dynamically combine analysis modules around one trade target:
   - market/news context
   - single-coin analysis
   - technical analysis
   - liquidity/slippage/liquidation/order-book analysis
   - token or contract risk check
3. Produce a **Trading Brief**
4. Produce an **Order Draft** when risk is acceptable
5. Execute after explicit confirmation:
   - spot buy/sell, conditional limit logic, amend/cancel/verification
   - USDT perpetual open/close/reverse/amend/cancel
6. Continue after execution:
   - fill verification
   - position verification
   - order / position management

### This skill cannot do

1. Decide and trade automatically on behalf of the user
2. Place orders without explicit confirmation
3. Bypass compliance, risk, minimum order, or contract safety constraints
4. Promise profit or present analysis as certainty
5. Pretend to support unsupported products

## Operating Principles

### Principle 1: Work around the trading goal

This skill is built for trading closure, not broad research.

- If the user only asks `How is the market?`
  - a lightweight market scan is fine
  - do not proactively move into order execution
- If the user says `How is the market today? Give me one trade idea`
  - a lightweight scan is allowed
  - but the workflow must narrow down to **one asset + one market (spot or futures)** before entering execution

### Principle 2: Judge first, execute second

Unless the user only wants pure order/position management, default to one round of pre-trade judgment before producing an order draft.

### Principle 3: Use the minimum necessary analysis

Do not run every module every time. Only call the modules needed for the current decision.

Read `references/routing-and-analysis.md` for:

- intent routing
- analysis module selection by scenario
- risk gating
- module-to-MCP mapping and call patterns

### Principle 4: Strong confirmation at execution layer

Any real trading action must follow this order:

1. Produce a `Trading Brief`
2. Produce an `Order Draft`
3. Wait for explicit confirmation in the immediately previous user turn
4. Execute only after confirmation

Read `references/execution-and-guardrails.md` for:

- spot and futures execution rules
- execution MCP mapping
- draft requirements
- confirmation rules
- hard and soft blocks

## Overall Workflow

### Step 0: Apply the shared runtime rules first

Before analysis or execution:

- read and follow `../exchange-runtime-rules.md`
- resolve any required runtime, update, or authorization gate before continuing
- verify that the named tools you plan to call exist in the current runtime before relying on them

### Step 1: Identify task mode

Classify the user request into one of these modes:

1. **Trade Decision**
   - analyze first, then decide whether to trade
2. **Trade Draft / Execute**
   - the user already wants to trade and wants analysis plus draft plus execution
3. **Order / Position Management**
   - the user wants to manage an existing order or position

### Step 2: Narrow down to one trade target

Before entering execution, try to make these explicit:

- asset: BTC / ETH / SOL / a new coin / a futures contract
- market: spot or USDT perpetual
- direction: buy / sell / long / short / close

If information is still incomplete:

- a lightweight market scan is allowed
- but before producing an order draft, the workflow must narrow down to one asset and one market

### Step 3: Build the pre-trade analysis package

Call only the modules needed for this request:

- market overview / news briefing
- listing / exchange announcement context
- single-coin analysis
- technical analysis
- event explanation
- risk check
- address tracing (only when the user really provides an address and wants tracing)
- liquidity / slippage / momentum / liquidation / basis / order-book analysis

### Step 4: Produce a Trading Brief

`Trading Brief` is the mandatory intermediate artifact before execution. It must include:

1. what the user wants to do
2. current market/asset judgment
3. key risks
4. whether the skill should continue to order drafting

Only three result states are allowed:

- `GO` = safe enough to continue to order drafting
- `CAUTION` = meaningful risk exists, but drafting may continue after warning
- `BLOCK` = do not continue into order drafting

### Step 5: Produce an Order Draft

Only produce an order draft when all of the following are true:

- the user has real trading intent
- the trade target is sufficiently clear
- no hard block is triggered

### Step 6: Wait for explicit confirmation

If the user does not provide a clear, immediate confirmation:

- do not execute
- remain in analysis / draft / query mode only

### Step 7: Execute and verify

After execution, always return:

- whether execution succeeded
- core fill/order/position results
- reasonable next actions, such as verify fill, amend, cancel, or close

## Market Identification Rules

### Default behavior

- If the request clearly contains `long / short / leverage / contract / perp / futures / open / close`
  - route to **USDT perpetual futures**
- If the request clearly contains `buy coin / sell coin / spot / buy BTC / sell ETH`
  - route to **spot**
- If the user says `buy BTC` without specifying market
  - default to **spot**
- If the user says `trade this move`
  - ask whether they want spot or USDT perpetual futures

## Recommended Output Rhythm

### Before execution

1. `Trading Brief`
2. if allowed: `Order Draft`
3. wait for confirmation

### After execution

1. `Execution Result`
2. if needed: `Next Actions`

## Special Rule for Order / Position Management

If the user asks for:

- amend order
- cancel order
- verify fill
- close half
- close all
- reverse

then the skill does not need to rerun the full research chain, but it still must:

- locate the correct target order or position
- apply the corresponding execution rules
- require strong confirmation for high-risk actions

## Risk Policy

### Hard blocks

Must stop immediately if:

- the user asks to skip confirmation
- the user asks to bypass compliance or risk controls
- the product is unsupported
- the asset is not tradable
- token security check shows a critical malicious risk

### Soft blocks

Warn but allow continuation if:

- liquidity is poor
- slippage is high
- funding is extreme
- crowding/liquidation risk is elevated
- a major event just hit and direction is unstable
- the coin is newly listed or still in price discovery

For soft blocks:

- surface the warning clearly in `Trading Brief`
- if the user still wants to continue, drafting is allowed
- confirmation is still mandatory

## Reading Order

1. Read `references/routing-and-analysis.md`
2. Read `references/execution-and-guardrails.md`
3. Execute only the modules needed for the current task; do not run the full stack by default
