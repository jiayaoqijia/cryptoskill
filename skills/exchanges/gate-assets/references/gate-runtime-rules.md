---
name: gate-exchange-assets-runtime-rules
version: "2026.4.8-1"
updated: "2026-04-08"
description: "Packaged runtime rules for gate-exchange-assets so the published skill bundle contains every mandatory guardrail referenced by SKILL.md."
---

# Gate Exchange Assets Runtime Rules

> Packaged runtime rules for `gate-exchange-assets`.
> This file is included in the skill bundle so ClawHub reviewers can audit every mandatory runtime artifact without relying on files outside this directory.

## 1. MCP Session and Authentication

- Use the already configured Gate MCP session for the current host.
- Local Gate MCP deployments use `GATE_API_KEY` and `GATE_API_SECRET`; never ask the user to paste these secrets into chat.
- Minimal permissions for this skill are `Delivery:Read`, `Earn:Read`, `Fx:Read`, `Margin:Read`, `Options:Read`, `Spot:Read`, `Tradfi:Read`, `Unified:Read`, and `Wallet:Read`.
- If the required Gate asset tools are missing, stop and switch to setup guidance only.
- If the MCP session returns an auth or permission error, stop and guide the user to repair the configured local MCP credentials before continuing.

## 2. Tool Scope

- Use only the MCP tools documented in `SKILL.md` and `references/mcp.md`.
- Do not call undocumented Gate tools, browser flows, or unrelated system tools.
- This skill is read-only. Do not use it for transfers, order placement, or account writes.

## 3. Balance Reporting

- Report only values returned by the documented MCP tools.
- Keep TradFi or payment balances separated when `SKILL.md` requires that presentation.
- Do not fabricate valuation or account-book entries.

## 4. Failure Handling

- On missing MCP configuration, auth failure, permission failure, or unsupported account mode, stay in read-only explanation mode.
- Explain why execution is blocked and what must be fixed.

## 5. Persistence and Secrets

- This skill does not install software or modify host configuration during normal execution.
- This skill does not store, rotate, export, or paste API secrets in chat.
