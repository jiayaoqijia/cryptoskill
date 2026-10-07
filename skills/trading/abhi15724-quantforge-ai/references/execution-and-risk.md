# Execution, Risk Limits, Low-Latency

## Modes (never switch silently)
RESEARCH, PAPER, SIMULATION, LIVE. State the active mode in every execution-related answer. Moving to LIVE requires the user's explicit instruction in the current conversation.

## Hard risk limits (user supplies values; never invent them)
Max daily loss, max strategy loss, max portfolio drawdown, max leverage, max position size, max order size/value, max correlated exposure, max open orders, kill switch. If missing, ask, or use clearly labelled conservative placeholders. On breach: **stop or reduce, never increase risk to recover.**

## Pre-trade checklist (all must pass)
Instrument valid and tradable, quantity within lot/limit, direction, price sane vs market (fat-finger band), order type, capital and margin available, position limit, max loss if stopped, session open, liquidity adequate, duplicate-order prevention (idempotency key), rate-limit headroom, risk limits not breached, kill switch armed. Missing information means ask, never invent.

## Safety mechanisms for execution code
Circuit breaker on repeated rejects/errors, stale-data guard, heartbeat/disconnect handling, position reconciliation with the broker, emergency flatten, full audit log, dry-run flag default ON.

## Latency tiers (always label which applies)
| Tier | Typical reality | Honest claim |
|---|---|---|
| Research | Offline, batch | No latency constraint |
| Paper | Simulated fills | Fill model must include spread/impact |
| Retail live | Broker REST/WebSocket, tens to hundreds of ms or more, rate-limited | Minutes-to-days horizons |
| Institutional low-latency | Co-location, kernel bypass, FPGA/C++/Rust, us-ns tick-to-trade | Needs exchange connectivity and hardware; never promise otherwise |

A Python app on cloud or retail infrastructure is not HFT. Never promise nanosecond execution. Treat HFT components (market-data handlers, order-book reconstruction, lock-free queues, CPU pinning, FIX/native gateways, latency/jitter measurement) as architecture knowledge, and require measured benchmarks before any claim.

## Repo layout
market_data/ research/ strategies/ backtesting/ risk/ portfolio/ execution/ monitoring/ config/ tests/
