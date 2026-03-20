---
name: xmtp-agents
description: >
  Building and extending XMTP agents with the Agent SDK.
  Use when: (1) creating or configuring an XMTP agent, (2) implementing agent features (commands, attachments, reactions, groups, transactions, inline actions, or domain resolution).
license: MIT
metadata:
  author: xmtp
  version: "1.0.0"
---

# XMTP agents

Build event-driven messaging agents on the XMTP network. This skill is the entry point; use the sub-skills below for specific features.

## When to apply

- Starting or configuring a new XMTP agent
- Adding behavior: commands, attachments, reactions, groups, payments, inline actions, or address/domain resolution

## Sub-skills

| Sub-skill | Use when |
|-----------|----------|
| **building-agents** | Setup, env vars, text/lifecycle events, middleware |
| **handling-commands** | Slash commands, validators, message filters, type guards |
| **handling-attachments** | Send/receive files, remote attachments, upload storage |
| **sending-reactions** | Send or receive reactions, thinking/reply patterns |
| **managing-groups** | Create groups, add members, roles, welcome-on-install |
| **handling-transactions** | USDC transfers, balance checks, transaction references |
| **creating-inline-actions** | Inline actions, confirmation/selection helpers, config menus |
| **resolving-domains** | Resolve addresses, Farcaster profiles, extract mentions |

## How to use

1. Pick the sub-skill that matches the task (e.g. slash commands → `handling-commands`).
2. Read that sub-skill’s `SKILL.md` and its `rules/` for step-by-step guidance.
3. For SDK or API details, use the xmtp-docs skill (index + specific page fetch).

## Quick start

Install the Agent SDK, create an agent from env, handle text, then start:

```bash
npm install @xmtp/agent-sdk
```

Create the agent and handle messages using patterns from **building-agents** (setup, events, middleware). For commands, attachments, reactions, groups, transactions, inline actions, or resolution, use the corresponding sub-skill above.
