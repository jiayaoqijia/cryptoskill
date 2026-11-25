---
name: llm-cost-optimizer
description: >-
  Offline zero-dependency Python CLI for estimating exact per-session and
  monthly LLM API spend across flagship and open models (OpenAI GPT-5/4.1/4o/o3,
  Claude Sonnet/Opus/Haiku, Gemini 2.5 Pro/Flash, DeepSeek V3/R1, Qwen) with
  prompt-cache hit rates, auditing local prompt/codebase files for token bloat
  and caching/trimming savings, and calculating pay-as-you-go API vs flat-rate
  subscription break-even (ChatGPT Plus $20, Claude Pro $20, Cursor Pro $20,
  Claude Max $100, ChatGPT Pro $200).
---

# llm-cost-optimizer

Estimate multi-model LLM API costs, audit local prompts/files for token bloat, and run pay-as-you-go vs. flat-rate subscription break-even analysis from a single standard-library Python script (`scripts/llm_cost.py`).

- **Runtime:** Python 3.8+ standard library only (`argparse`, `json`, `math`, `re`, `collections`). Zero third-party installs (`tiktoken` not required).
- **Privacy & Auth:** 100% offline local execution—zero API keys, zero network requests, zero telemetry. Prompts and source files never leave the local machine.
- **Customizable rates:** Built-in 2026 reference pricing for 14 flagship/open models, overridable anytime via `--pricing-file <custom.json>`.

## When to Use

- **Budgeting agent & app workloads (`estimate`):** Rank exact per-turn, per-session, daily, and 30-day monthly spend across **OpenAI (GPT-5, GPT-4.1, GPT-4o, GPT-4o-mini, o3)**, **Anthropic (Claude Opus 4, Sonnet 4, 3.5 Haiku)**, **Google (Gemini 2.5 Pro, Flash, Flash-Lite)**, **DeepSeek (V3.2, R1)**, and **Qwen**, with realistic prompt-caching hit rates and instant `$20` plan break-even flags.
- **Auditing local prompts & codebase context (`audit-prompt`):** Estimate EN/CJK/code token counts on any local file (`SKILL.md`, system prompt, JSON schema, or source file), surface concrete bloat flags (`VERY_LARGE_CONTEXT`, `LARGE_STATIC_PROMPT`, `EXCESSIVE_WHITESPACE`, `DUPLICATE_LINES`, `UNMINIFIED_JSON`, `HEAVY_EXAMPLE_BLOCKS`), and calculate exact monthly & annual dollar savings from prefix caching and context trimming.
- **Choosing API vs. flat-rate plans (`compare-plans`):** Calculate exact daily and monthly break-even turn thresholds comparing pay-as-you-go API spend against **ChatGPT Plus ($20)**, **Claude Pro ($20)**, **Cursor Pro ($20)**, **Claude Max ($100)**, **ChatGPT Pro ($200)**, or any custom seat price (`--custom-plan-usd`), plus an 80/20 hybrid model-routing benchmark.

## CLI Usage Examples

Run `scripts/llm_cost.py` from the skill directory:

```bash
# 1. Estimate monthly & per-session cost across all 14 models (Markdown table)
python scripts/llm_cost.py estimate \
  --daily-turns 60 \
  --avg-input-tokens 8000 \
  --avg-output-tokens 1200 \
  --cache-hit-rate 0.65 \
  --turns-per-session 12 \
  --format markdown

# 2. Estimate for specific models in machine-readable JSON
python scripts/llm_cost.py estimate \
  --daily-turns 120 \
  --avg-input-tokens 25000 \
  --avg-output-tokens 2000 \
  --cache-hit-rate 0.70 \
  --models gpt-5,o3,claude-sonnet-4,gemini-2.5-pro,deepseek-v3

# 3. Audit a local system prompt, JSON schema, or source file for token bloat & savings
python scripts/llm_cost.py audit-prompt \
  --file ./system_prompt.md \
  --daily-turns 150 \
  --avg-output-tokens 1000 \
  --cache-hit-rate 0.75 \
  --trim-pct 0.30 \
  --model claude-sonnet-4 \
  --format markdown

# 4. Compare pay-as-you-go API vs flat-rate subscriptions (+ custom $40 seat)
python scripts/llm_cost.py compare-plans \
  --daily-turns 45 \
  --avg-input-tokens 6000 \
  --avg-output-tokens 1200 \
  --cache-hit-rate 0.50 \
  --custom-plan-usd 40 \
  --format markdown

# 5. List built-in 2026 reference pricing IDs and rates
python scripts/llm_cost.py list-models --format markdown
```

### Subcommand Reference

| Subcommand | Key Flags & Defaults | Purpose |
| --- | --- | --- |
| `estimate` | `--daily-turns 50`, `--avg-input-tokens 4000`, `--avg-output-tokens 800`, `--cache-hit-rate 0.5`, `--turns-per-session 10`, `--days 30`, `--models ""`, `--format json\|markdown`, `--pricing-file` | Ranked per-session & monthly cost across 14 models + `$20` plan break-even |
| `audit-prompt` | `--file` (req), `--daily-turns 100`, `--avg-output-tokens 800`, `--cache-hit-rate 0.7`, `--trim-pct 0.25`, `--model claude-sonnet-4`, `--days 30`, `--format json\|markdown`, `--pricing-file` | Estimate file tokens, flag bloat patterns, and compute caching/trimming savings |
| `compare-plans` | `--daily-turns 40`, `--avg-input-tokens 6000`, `--avg-output-tokens 1200`, `--cache-hit-rate 0.5`, `--days 30`, `--model ""`, `--custom-plan-usd`, `--format json\|markdown`, `--pricing-file` | Break-even turn calculator comparing API vs. ChatGPT Plus/Pro, Claude Pro/Max, Cursor Pro |
| `list-models` | `--format json\|markdown`, `--pricing-file` | Print built-in model IDs, context windows, and USD / 1M token rates |

Note: `--cache-hit-rate` and `--trim-pct` accept either decimal ratios (`0.7`) or percentages (`70`).

## Output Schema

Default output (`--format json`) prints UTF-8 JSON to `stdout`. Pass `--format markdown` for formatted GitHub-flavored Markdown tables.

### `estimate`

```json
{
  "workload": {
    "daily_turns": 60.0,
    "turns_per_session": 12,
    "days": 30,
    "monthly_turns": 1800.0,
    "avg_input_tokens": 8000,
    "avg_output_tokens": 1200,
    "cache_hit_rate": 0.65,
    "cache_hit_pct": 65.0
  },
  "cheapest_model": "gemini-2.5-flash-lite",
  "models": [
    {
      "id": "gpt-5",
      "name": "GPT-5 Standard",
      "provider": "OpenAI",
      "tier": "flagship",
      "effective_input_per_1m": 0.5188,
      "output_per_1m": 10.0,
      "per_turn_usd": 0.01615,
      "per_session_usd": 0.1938,
      "daily_usd": 0.969,
      "monthly_usd": 29.07,
      "uncached_monthly_usd": 39.6,
      "cache_savings_monthly_usd": 10.53,
      "breakeven_daily_turns_vs_20_plan": 41.28,
      "delta_vs_20_plan_usd": 9.07,
      "vs_20_plan_verdict": "SUBSCRIPTION_CHEAPER"
    }
  ],
  "subscription_breakeven_20_usd": [
    {
      "plan_id": "chatgpt-plus",
      "plan_name": "ChatGPT Plus",
      "plan_monthly_usd": 20.0,
      "benchmark_model_id": "gpt-5",
      "equivalent_api_monthly_usd": 29.07,
      "breakeven_daily_turns": 41.28,
      "monthly_savings_with_subscription_usd": 9.07,
      "recommendation": "SUBSCRIPTION_CHEAPER"
    }
  ]
}
```

### `audit-prompt`

Returns `file`, `bytes`, `token_stats` (`estimated_tokens`, `chars`, `lines`, `words_and_cjk`, `cjk_chars`, `cjk_ratio`, `symbol_ratio`), `structure` (blank lines, whitespace overhead, duplicate long lines, fenced blocks, pretty-printed JSON detection), `bloat_flags[]`, `target_model_savings`, and `model_benchmarks[]` comparing baseline, caching-only, trimming-only, and combined monthly & annual savings.

### `compare-plans`

Returns `workload`, `plan_comparisons[]` (`plan_id`, `plan_name`, `plan_monthly_usd`, `matched_api_model_id`, `api_per_turn_usd`, `api_monthly_usd`, `monthly_savings_vs_api_usd`, `breakeven_daily_turns`, `breakeven_monthly_turns`, `cheaper_option`), and `hybrid_routing_reference` (`80% deepseek-v3 + 20% flagship`).

## Pricing & Methodology Reference

Read [references/pricing-2026.md](references/pricing-2026.md) for:

- Full 2026 reference rate card across 14 models and provider-specific caching semantics (Anthropic 1.25x cache write vs. OpenAI/DeepSeek automatic prefix caching)
- Exact blended input, session, and subscription break-even equations
- Offline EN/CJK/code token estimation heuristic and `--pricing-file` custom JSON schema

## Operational Caveats

- **Approximate local tokenization:** Token counts use a zero-dependency EN/CJK/code heuristic (`~5–10%` of BPE tokenizers). Always leave a 10–15% safety margin when sizing near hard context limits or strict monthly budgets.
- **Reasoning-token overhead:** Reasoning models (`o3`, `deepseek-r1`, thinking-enabled flagship models) bill internal reasoning tokens as output tokens. Increase `--avg-output-tokens` (e.g., `2,500–6,000`) when modeling deep reasoning tasks.
- **Subscription usage caps:** Flat-rate plans (ChatGPT Plus, Claude Pro, Cursor Pro) enforce rolling message/compute windows rather than unlimited API throughput; API billing remains required for unattended batch automation or custom SLAs.

## Ecosystem & Resources

- **Live Browser Calculator (Zero Tracking):** [TokenCost Zero](https://devbox-zero-ops.github.io/tokencost-zero/) — interactive local prompt token estimator, multi-model cost table, and CSV export.
- **Free Developer & Cost-Guide Hub:** [XiaheAI Hub](https://devbox-zero-ops.github.io/xiaheai-hub/) — local developer utilities plus side-by-side ChatGPT Plus / Claude Pro / Cursor Pro / Codex CLI calculators.
- **Commercial White-Label Source Kit:** [XiaheAI ZeroSuite Pro](https://devbox-zero-ops.github.io/xiaheai-hub/pro.html) — full multi-tool self-hostable source bundle for teams.
