---
name: gate-news-briefing-runtime-rules
version: "2026.4.7-1"
updated: "2026-04-07"
description: "Packaged runtime rules for gate-news-briefing so every mandatory artifact referenced by SKILL.md is included in the published bundle."
---

# Gate News Briefing Runtime Rules

> Packaged runtime rules for `gate-news-briefing`.
> This file is bundled with the skill so reviewers can audit the required guardrails without depending on files outside this directory.

## 1. Intent and Scope

- Use this skill only for news and headline briefing requests.
- If the user asks for attribution, coin fundamentals, or another dedicated dimension, route to the matching skill instead of stretching this one.

## 2. Tool Scope

- Use only the MCP tools documented in `SKILL.md`.
- Do not call undocumented tools, browser flows, or unrelated system tools.

## 3. Installation and Fallback

- This skill requires the Gate News MCP server.
- If the required MCP tools are unavailable, stop and provide setup guidance or graceful partial output as documented in `SKILL.md`.

## 4. Persistence and Secrets

- This skill is read-only.
- This skill does not install software, write local files, or handle API secrets during normal execution.
