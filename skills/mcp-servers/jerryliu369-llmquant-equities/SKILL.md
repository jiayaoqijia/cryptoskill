<!--
  Imported from: https://github.com/LLMQuant/skills
  Source Path: skills/llmquant-equities/SKILL.md
  Curated for awesome-quant-skills
-->

---
name: llmquant-equities
description: Router skill for LLMQuant equities workflows. Use when the user needs stock analysis, equity comparison, research memos, merger-arb memos, or sell/take-profit work.
input_data_source: LLMQuant Data
category: equities
---

# LLMQuant Equities

This category routes equity research, comparison, valuation, catalyst, and sell-discipline workflows.

## Routing Rules

1. Identify ticker(s), investment horizon, benchmark, and requested deliverable.
2. Select the closest workflow below.
3. Open only the selected workflow and needed local resources.
4. Use LLMQuant Data for filings, prices, fundamentals, ownership, macro, estimates, and events.
5. Report data periods, filing dates, observation dates, stale notices, and missing future inputs.

## Workflow Index

| User intent | Workflow |
|---|---|
| Score a stock across fundamentals, valuation, technicals, sentiment, and flow. | [`workflows/five-lens-stock-analysis.md`](workflows/five-lens-stock-analysis.md) |
| Compare 2-5 stocks or ETFs side by side. | [`workflows/equity-compare.md`](workflows/equity-compare.md) |
| Build a full equity research memo. | [`workflows/equity-research-memo.md`](workflows/equity-research-memo.md) |
| Build a catalyst-bound merger-arbitrage memo. | [`workflows/merger-arb-memo.md`](workflows/merger-arb-memo.md) |
| Analyze hold versus systematic profit-taking rules. | [`workflows/take-profit-lab.md`](workflows/take-profit-lab.md) |

## LLMQuant Data Contract

Prefer LLMQuant Data when available. The workflows may need these data capabilities:
- Retrieve equity prices, returns, market cap, volume, technical indicators, and realized volatility.
- Retrieve company fundamentals, estimates, valuation multiples, peer context, and corporate events.
- Read SEC filings and specific filing sections for business, MD&A, risks, and catalysts.
- Retrieve institutional ownership, top holders, manager concentration, and 13F sponsorship context.

Fallback:
- If fundamentals, estimates, or event feeds are unavailable, name the missing input and continue only with retrieved or user-provided evidence.
