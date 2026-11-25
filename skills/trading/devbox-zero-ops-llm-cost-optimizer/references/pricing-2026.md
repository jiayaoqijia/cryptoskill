# 2026 Reference LLM API Pricing & Cost-Modeling Methodology

This reference documents the built-in 2026 reference API rates, prompt-caching math, bilingual token heuristics, and subscription break-even formulas used by `scripts/llm_cost.py`.

## 1. Reference Model Rate Card (USD per 1M Tokens)

Rates reflect standard published tier pricing (editable at runtime via `--pricing-file <custom.json>`):

| Model ID | Model Name | Provider | Tier | Context | Input / 1M | Cached Input / 1M | Cache Discount | Output / 1M |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| `gemini-2.5-flash-lite` | Gemini 2.5 Flash-Lite | Google | economy | 1,000,000 | $0.10 | $0.025 | 75% | $0.40 |
| `gpt-4o-mini` | GPT-4o-mini | OpenAI | economy | 128,000 | $0.15 | $0.075 | 50% | $0.60 |
| `deepseek-v3` | DeepSeek-V3.2 (Chat) | DeepSeek | open-weight | 128,000 | $0.27 | $0.070 | 74% | $1.10 |
| `gemini-2.5-flash` | Gemini 2.5 Flash | Google | balanced | 1,000,000 | $0.30 | $0.075 | 75% | $2.50 |
| `qwen-plus` | Qwen-Plus / Max | Alibaba | open-weight | 128,000 | $0.40 | $0.100 | 75% | $1.20 |
| `deepseek-r1` | DeepSeek-R1 (Reasoner) | DeepSeek | reasoning | 128,000 | $0.55 | $0.140 | 75% | $2.19 |
| `claude-3.5-haiku` | Claude 3.5 Haiku | Anthropic | fast | 200,000 | $0.80 | $0.080 | 90% | $4.00 |
| `gemini-2.5-pro` | Gemini 2.5 Pro (`<= 200k`) | Google | flagship | 1,000,000 | $1.25 | $0.3125 | 75% | $10.00 |
| `gpt-5` | GPT-5 Standard | OpenAI | flagship | 400,000 | $1.25 | $0.125 | 90% | $10.00 |
| `gpt-4.1` | GPT-4.1 | OpenAI | flagship | 1,000,000 | $2.00 | $0.500 | 75% | $8.00 |
| `o3` | OpenAI o3 | OpenAI | reasoning | 200,000 | $2.00 | $0.500 | 75% | $8.00 |
| `gpt-4o` | GPT-4o | OpenAI | flagship | 128,000 | $2.50 | $1.250 | 50% | $10.00 |
| `claude-sonnet-4` | Claude Sonnet 4 | Anthropic | flagship | 200,000 | $3.00 | $0.300 | 90% | $15.00 |
| `claude-opus-4` | Claude Opus 4 | Anthropic | frontier | 200,000 | $15.00 | $1.500 | 90% | $75.00 |

### Provider-Specific Caching Nuances

- **Anthropic (`claude-*`):** Steady-state cache reads cost `0.10x` base input (90% discount), while initial 5-minute TTL cache writes incur a `1.25x` write fee (amortized rapidly across `>= 2` hits within the TTL window).
- **OpenAI (`gpt-5`, `gpt-4.1`, `o3`, `gpt-4o`):** Prefix caching is automatic for prompts `>= 1,024` tokens with zero write surcharge; discounts range from 50% (`gpt-4o`) to 75% (`gpt-4.1`/`o3`) to 90% (`gpt-5`).
- **Google (`gemini-2.5-*`):** Supports both implicit and explicit context caching (~75% discount). Prompts exceeding `200k` input tokens on Gemini 2.5 Pro enter the long-context pricing tier (verify custom tiers via `--pricing-file`).
- **DeepSeek (`deepseek-v3`, `deepseek-r1`):** Automatic KV prefix caching cuts cache-hit input rates by ~74–75%.

## 2. Exact Blended Cost & Break-Even Formulas

Let $I$ be `avg_input_tokens`, $O$ be `avg_output_tokens`, $h \in [0, 1]$ be `cache_hit_rate`, $T_d$ be `daily_turns`, $D$ be billing `days` (default `30`), and $S$ be `turns_per_session` (default `10`).

```text
effective_input_per_1m = input_per_1m * (1 - h) + cached_input_per_1m * h
per_turn_usd           = (I / 1,000,000) * effective_input_per_1m + (O / 1,000,000) * output_per_1m
per_session_usd        = per_turn_usd * S
daily_usd              = per_turn_usd * T_d
monthly_usd            = per_turn_usd * T_d * D
```

### Flat-Rate Subscription Break-Even

For a flat-rate subscription priced at $P_{\text{plan}}$ USD/month (for example `$20`, `$100`, or `$200`):

```text
breakeven_monthly_turns = ceil(P_plan / per_turn_usd)
breakeven_daily_turns   = P_plan / (per_turn_usd * D)
monthly_delta_usd       = monthly_usd - P_plan
```

- When `monthly_usd > P_plan`, flat-rate subscriptions (such as **ChatGPT Plus $20**, **Claude Pro $20**, or **Cursor Pro $20**) beat pay-as-you-go flagship API spend on cost, subject to provider rolling usage caps.
- When `monthly_usd < P_plan`, pay-as-you-go API avoids paying for unused subscription capacity.
- For high-volume agent pipelines, **hybrid model routing** (for instance routing 80% of deterministic/extraction turns to `deepseek-v3` or `gemini-2.5-flash` and reserving `claude-sonnet-4` or `gpt-5` for the hardest 20% of reasoning turns) frequently outperforms both pure flagship APIs and single subscriptions.

## 3. Offline Bilingual Token Estimation

`estimate_text_tokens(text)` runs without downloading tokenizer vocabularies or calling external APIs:

```text
cjk_chars       = count of Unicode CJK Unified Ideographs / Kana / Hangul
non_cjk_chars   = total_chars - cjk_chars
symbol_ratio    = code_json_punctuation_chars / max(1, non_cjk_chars)
chars_per_token = 3.25 if symbol_ratio >= 0.14 else 3.8
est_tokens      = ceil(cjk_chars * 1.45 + non_cjk_chars / chars_per_token)
```

Typical accuracy is within `~5–10%` of BPE tokenizers (`o200k_base` / `cl100k_base`) on mixed English, CJK, Markdown, JSON, and source code—sufficient for budgeting, prompt bloat detection, and model-routing trade-offs.

## 4. Custom Pricing Override Schema (`--pricing-file`)

Pass a JSON array to override built-in rates or append private/enterprise models:

```json
[
  {
    "id": "gpt-5",
    "input_per_1m": 1.00,
    "cached_input_per_1m": 0.10,
    "output_per_1m": 8.00
  },
  {
    "id": "internal-vllm-70b",
    "name": "Self-Hosted Llama 70B",
    "provider": "Internal",
    "tier": "self-hosted",
    "context_window": 131072,
    "input_per_1m": 0.18,
    "cached_input_per_1m": 0.05,
    "output_per_1m": 0.45
  }
]
```
