---
name: gate-info-coinanalysis-info-news-runtime-rules
version: "2026.4.6-1"
updated: "2026-04-06"
description: "Packaged info/news common runtime rules for gate-info-coinanalysis."
---

# Info & News Common Runtime Rules

> Packaged common rules for `gate-info-*` and `gate-news-*` review.

## 1. MCP Availability

- Before using MCP-dependent capabilities, confirm the required Gate Info or Gate News tools are available.
- If a required tool is missing, explain the limitation and degrade gracefully instead of fabricating data.

## 2. Tool Degradation

- A single MCP tool failure must not block the entire skill.
- Skip the unavailable dimension, label it clearly in the report, and continue with the remaining data.
- If all required tools fail, return a concise failure summary and suggest checking MCP availability.

## 3. Output Standards

- Use markdown output.
- Match the user's language.
- Use a neutral, data-driven tone and avoid explicit buy/sell advice.

## 4. Security and Privacy

- Do not expose credentials or secrets in chat.
- Use only publicly available on-chain, market, and news data returned by the documented MCP tools.
