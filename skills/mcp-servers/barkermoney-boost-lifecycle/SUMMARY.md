## Overview

Boost Lifecycle manages a Barker boost campaign end to end: deposit with reward attribution, expiry reminders, reward claiming, redemption, and risk monitoring. Boost rewards follow min(D, C) accounting — D is the share balance attributed through Barker's entry (deposits bound to a `campaign_id`), C is the wallet's on-chain share balance — so every deposit this skill drives is campaign-bound; deposits made without the campaign binding earn nothing. Every money-moving step goes through a campaign-bound execution intent that the user explicitly confirms and signs — Barker never broadcasts and never holds funds.

## Prerequisites

- An LLM runtime that can load Claude Code skills (OKX Wallet Agent, Claude Code, Cursor, or any MCP-compatible host).
- Network access to Barker's MCP at `mcp.barker.money` (port 443).
- An x402/wallet payment flow on the agent to settle HTTP 402 challenges.
- A user wallet that can sign the returned transactions (the skill only prepares them).

## Quick Start

1. `boost-lifecycle quickstart` — invoke the skill in your assistant to load the campaign playbook and confirm Barker's MCP at `mcp.barker.money` is reachable.
2. Try a sample query: "Help me join the current boost campaign with 500 USDC and manage it until it ends."
3. The assistant resolves the live campaign, prepares a campaign-bound deposit intent for your confirmation, then tracks the lifecycle — expiry reminders, reward claiming, redemption windows, and risk flags — surfacing each next action as it comes due.
