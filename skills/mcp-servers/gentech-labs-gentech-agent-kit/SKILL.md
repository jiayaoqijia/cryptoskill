---
name: gentech-agent-kit
description: "Full GenTech stack — payments, DeFi, self-evolution, MCP server"
version: 0.4.0
author: GenTech Labs
tags: [mcp, payments, defi, self-evolution, hermes, x402, q402]
dependencies: [hermes-v0.19+]
---

# GenTech Agent Kit

Full-stack agent infrastructure: payment rails (x402 + Q402), DeFi intelligence, self-evolution harness, and MCP server.

## Included Skills
- **x402-payments** — Solana micropayment gateway
- **robinhood-chain** — Robinhood Chain (USDG, stocks)
- **output-enforcer** — Structured output with circuit breaker
- **wakeup-protocol** — Session wakeup + env loading
- **context-cycle-proactive** — Save → route → load → resume at 80-90% context; keeps every agent synced to the second brain (tiered by model window)
- **safe-update-restart** — Safe update/restart for a production VPS: backup → controlled window → restart → verify every service & endpoint after

## a2a — Agent-to-Agent Communication

The full A2A lifecycle module: **discover → talk → self-audit**.

- `a2a/discovery/` — ERC-8004 registry monitor. Alerts on new x402/named/Base agents. Top-10 lead generator.
- `a2a/workspace/` — Buzz bridge. Self-host the relay, seed a Hermes profile as a native Buzz agent (Nostr, signed events, agents as team members).
- `a2a/self-audit/` — Self-Evolution Harness. Four cron roles (Evolution, Critic, Verifier, Gardener) that audit the agent's own execution record. Includes constitution.
- `a2a/identity/` — ERC-8004 on-chain registration across 7+ chains.

See `a2a/README.md` for the loop and quick start.

## Self-Evolution
Four cron jobs (Evolution, Critic, Verifier, Gardener) make the agent measurably better over time. Witness log auto-fed from context-weight nightly.

## Requires
- Hermes v0.19.0+
- CMC_API_KEY

## Payment Rails
- x402 Solana micropayments (Pay wallet: pX1FTLyXAskfD4y8pRwx7Go58GpM9t2PtGZGj6Lq2hR)
- Q402 gasless stablecoin (USDC/USDT on 12 chains, BNB trial)
