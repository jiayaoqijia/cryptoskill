#!/usr/bin/env python3
"""
LLM Cost Optimizer — Offline Token Estimator, API Pricing & Subscription Break-Even CLI

Zero-dependency Python 3.8+ standard-library CLI modeled on the TokenCost Zero
pricing and prompt-caching engine. Runs 100% locally with zero network calls or
telemetry.

Subcommands:
  estimate       Ranked per-session & monthly cost across flagship and open models
                 plus $20 flat-rate subscription break-even analysis.
  audit-prompt   Estimate tokens of a local prompt/codebase file, detect token
                 bloat, and calculate exact prompt-caching & trimming savings.
  compare-plans  Pay-as-you-go API vs flat-rate subscription break-even calculator
                 (ChatGPT Plus / Claude Pro / Cursor Pro / Claude Max / ChatGPT Pro).
  list-models    Display built-in 2026 reference API pricing rates.
"""

import argparse
import collections
import json
import math
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

DEFAULT_MODELS = [
    {
        "id": "gemini-2.5-flash-lite",
        "name": "Gemini 2.5 Flash-Lite",
        "provider": "Google",
        "tier": "economy",
        "context_window": 1000000,
        "input_per_1m": 0.10,
        "cached_input_per_1m": 0.025,
        "output_per_1m": 0.40,
    },
    {
        "id": "gpt-4o-mini",
        "name": "GPT-4o-mini",
        "provider": "OpenAI",
        "tier": "economy",
        "context_window": 128000,
        "input_per_1m": 0.15,
        "cached_input_per_1m": 0.075,
        "output_per_1m": 0.60,
    },
    {
        "id": "deepseek-v3",
        "name": "DeepSeek-V3.2 (Chat)",
        "provider": "DeepSeek",
        "tier": "open-weight",
        "context_window": 128000,
        "input_per_1m": 0.27,
        "cached_input_per_1m": 0.07,
        "output_per_1m": 1.10,
    },
    {
        "id": "gemini-2.5-flash",
        "name": "Gemini 2.5 Flash",
        "provider": "Google",
        "tier": "balanced",
        "context_window": 1000000,
        "input_per_1m": 0.30,
        "cached_input_per_1m": 0.075,
        "output_per_1m": 2.50,
    },
    {
        "id": "qwen-plus",
        "name": "Qwen-Plus / Max",
        "provider": "Alibaba",
        "tier": "open-weight",
        "context_window": 128000,
        "input_per_1m": 0.40,
        "cached_input_per_1m": 0.10,
        "output_per_1m": 1.20,
    },
    {
        "id": "deepseek-r1",
        "name": "DeepSeek-R1 (Reasoner)",
        "provider": "DeepSeek",
        "tier": "reasoning",
        "context_window": 128000,
        "input_per_1m": 0.55,
        "cached_input_per_1m": 0.14,
        "output_per_1m": 2.19,
    },
    {
        "id": "claude-3.5-haiku",
        "name": "Claude 3.5 Haiku",
        "provider": "Anthropic",
        "tier": "fast",
        "context_window": 200000,
        "input_per_1m": 0.80,
        "cached_input_per_1m": 0.08,
        "output_per_1m": 4.00,
    },
    {
        "id": "gemini-2.5-pro",
        "name": "Gemini 2.5 Pro",
        "provider": "Google",
        "tier": "flagship",
        "context_window": 1000000,
        "input_per_1m": 1.25,
        "cached_input_per_1m": 0.3125,
        "output_per_1m": 10.00,
    },
    {
        "id": "gpt-5",
        "name": "GPT-5 Standard",
        "provider": "OpenAI",
        "tier": "flagship",
        "context_window": 400000,
        "input_per_1m": 1.25,
        "cached_input_per_1m": 0.125,
        "output_per_1m": 10.00,
    },
    {
        "id": "gpt-4.1",
        "name": "GPT-4.1",
        "provider": "OpenAI",
        "tier": "flagship",
        "context_window": 1000000,
        "input_per_1m": 2.00,
        "cached_input_per_1m": 0.50,
        "output_per_1m": 8.00,
    },
    {
        "id": "o3",
        "name": "OpenAI o3",
        "provider": "OpenAI",
        "tier": "reasoning",
        "context_window": 200000,
        "input_per_1m": 2.00,
        "cached_input_per_1m": 0.50,
        "output_per_1m": 8.00,
    },
    {
        "id": "gpt-4o",
        "name": "GPT-4o",
        "provider": "OpenAI",
        "tier": "flagship",
        "context_window": 128000,
        "input_per_1m": 2.50,
        "cached_input_per_1m": 1.25,
        "output_per_1m": 10.00,
    },
    {
        "id": "claude-sonnet-4",
        "name": "Claude Sonnet 4",
        "provider": "Anthropic",
        "tier": "flagship",
        "context_window": 200000,
        "input_per_1m": 3.00,
        "cached_input_per_1m": 0.30,
        "output_per_1m": 15.00,
    },
    {
        "id": "claude-opus-4",
        "name": "Claude Opus 4",
        "provider": "Anthropic",
        "tier": "frontier",
        "context_window": 200000,
        "input_per_1m": 15.00,
        "cached_input_per_1m": 1.50,
        "output_per_1m": 75.00,
    },
]

SUBSCRIPTION_PLANS = [
    {
        "id": "chatgpt-plus",
        "name": "ChatGPT Plus",
        "monthly_usd": 20.0,
        "primary_api_model": "gpt-5",
        "secondary_api_model": "gpt-4o",
        "notes": "General flagship chat, web research, vision, and moderate Codex usage",
    },
    {
        "id": "claude-pro",
        "name": "Claude Pro",
        "monthly_usd": 20.0,
        "primary_api_model": "claude-sonnet-4",
        "secondary_api_model": "claude-3.5-haiku",
        "notes": "Long-context reasoning, prose editing, and moderate Claude Code sessions",
    },
    {
        "id": "cursor-pro",
        "name": "Cursor Pro",
        "monthly_usd": 20.0,
        "primary_api_model": "claude-sonnet-4",
        "secondary_api_model": "gpt-5",
        "notes": "IDE-native multi-file editing, tab completions, and agentic codebase loops",
    },
    {
        "id": "claude-max-100",
        "name": "Claude Max (5x)",
        "monthly_usd": 100.0,
        "primary_api_model": "claude-sonnet-4",
        "secondary_api_model": "claude-opus-4",
        "notes": "High-volume Claude Code & multi-agent terminal workflows",
    },
    {
        "id": "chatgpt-pro",
        "name": "ChatGPT Pro",
        "monthly_usd": 200.0,
        "primary_api_model": "o3",
        "secondary_api_model": "gpt-5",
        "notes": "Heavy reasoning, deep research, and high-throughput Codex CLI engineering",
    },
]

CJK_RE = re.compile(r"[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]")
WORD_RE = re.compile(r"[A-Za-z0-9_]+")
CODE_SYMBOL_RE = re.compile(r"[{}[\]():;,\"'<>/\\=+\-*&|^%!~]")


def normalize_rate(val: float, name: str = "rate") -> float:
    """
    Accept either a decimal ratio [0.0, 1.0] or a percentage (1.0, 100.0].
    Normalizes cleanly to a float in [0.0, 1.0].
    """
    if val < 0:
        raise ValueError(f"{name} must be >= 0 (got {val})")
    if val > 100.0:
        raise ValueError(f"{name} must be <= 1.0 (or <= 100 as percent; got {val})")
    if val > 1.0:
        return val / 100.0
    return float(val)


def load_models(pricing_file: str = None):
    """Return built-in 2026 model catalog optionally merged with custom JSON overrides."""
    models = [dict(m) for m in DEFAULT_MODELS]
    if not pricing_file:
        return models
    with open(pricing_file, "r", encoding="utf-8") as fh:
        custom = json.load(fh)
    if not isinstance(custom, list):
        raise ValueError("pricing-file must contain a JSON array of model objects")
    by_id = {m["id"]: m for m in models}
    for entry in custom:
        mid = str(entry.get("id") or "").strip()
        if not mid:
            raise ValueError("Each custom pricing entry must have a non-empty 'id'")
        if mid in by_id:
            by_id[mid].update(entry)
        else:
            for req_field in ("name", "provider", "input_per_1m", "cached_input_per_1m", "output_per_1m"):
                if req_field not in entry:
                    raise ValueError(f"Custom model {mid!r} missing required field {req_field!r}")
            new_entry = {
                "tier": "custom",
                "context_window": 128000,
                **entry,
            }
            models.append(new_entry)
            by_id[mid] = new_entry
    return models


def find_model(models: list, model_id: str) -> dict:
    key = model_id.strip().lower()
    for m in models:
        if m["id"].lower() == key or m["name"].lower() == key:
            return m
    valid = ", ".join(m["id"] for m in models)
    raise ValueError(f"Unknown model {model_id!r}. Available IDs: {valid}")


def calc_turn_cost_usd(model: dict, avg_input_tokens: float, avg_output_tokens: float, cache_hit_rate: float):
    """Compute exact per-turn cost (cached & uncached) and effective blended input rate."""
    eff_in_per_1m = (
        model["input_per_1m"] * (1.0 - cache_hit_rate)
        + model["cached_input_per_1m"] * cache_hit_rate
    )
    input_cost = (avg_input_tokens / 1_000_000.0) * eff_in_per_1m
    uncached_input_cost = (avg_input_tokens / 1_000_000.0) * model["input_per_1m"]
    output_cost = (avg_output_tokens / 1_000_000.0) * model["output_per_1m"]
    return {
        "effective_input_per_1m": round(eff_in_per_1m, 4),
        "per_turn_usd": input_cost + output_cost,
        "uncached_per_turn_usd": uncached_input_cost + output_cost,
        "input_cost_per_turn_usd": input_cost,
        "output_cost_per_turn_usd": output_cost,
    }


def estimate_workload(
    daily_turns: float,
    avg_input_tokens: int,
    avg_output_tokens: int,
    cache_hit_rate: float,
    turns_per_session: int = 10,
    days: int = 30,
    model_filter: str = "",
    pricing_file: str = None,
):
    """Estimate ranked per-session, daily, and monthly spend across models plus $20 plan break-even."""
    if daily_turns <= 0:
        raise ValueError("daily-turns must be > 0")
    if avg_input_tokens < 0 or avg_output_tokens < 0:
        raise ValueError("Token counts must be >= 0")
    if turns_per_session <= 0 or days <= 0:
        raise ValueError("turns-per-session and days must be > 0")

    hit_rate = normalize_rate(cache_hit_rate, "cache-hit-rate")
    all_models = load_models(pricing_file)
    models = list(all_models)

    if model_filter.strip():
        wanted = {x.strip().lower() for x in model_filter.split(",") if x.strip()}
        models = [
            m
            for m in models
            if m["id"].lower() in wanted or m["provider"].lower() in wanted or m["tier"].lower() in wanted
        ]
        if not models:
            raise ValueError(f"No models matched filter {model_filter!r}")

    monthly_turns = daily_turns * days
    ranked = []
    for m in models:
        tc = calc_turn_cost_usd(m, avg_input_tokens, avg_output_tokens, hit_rate)
        per_turn = tc["per_turn_usd"]
        per_session = per_turn * turns_per_session
        daily_usd = per_turn * daily_turns
        monthly_usd = per_turn * monthly_turns
        uncached_monthly = tc["uncached_per_turn_usd"] * monthly_turns
        cache_savings = max(0.0, uncached_monthly - monthly_usd)
        breakeven_daily_at_20 = round(20.0 / (per_turn * days), 2) if per_turn > 0 else None
        delta_vs_20 = round(monthly_usd - 20.0, 2)
        if abs(delta_vs_20) < 0.01:
            verdict_20 = "BREAK_EVEN"
        elif monthly_usd < 20.0:
            verdict_20 = "API_CHEAPER"
        else:
            verdict_20 = "SUBSCRIPTION_CHEAPER"

        ranked.append({
            "id": m["id"],
            "name": m["name"],
            "provider": m["provider"],
            "tier": m["tier"],
            "input_per_1m": m["input_per_1m"],
            "cached_input_per_1m": m["cached_input_per_1m"],
            "effective_input_per_1m": tc["effective_input_per_1m"],
            "output_per_1m": m["output_per_1m"],
            "per_turn_usd": round(per_turn, 6),
            "per_session_usd": round(per_session, 4),
            "daily_usd": round(daily_usd, 4),
            "monthly_usd": round(monthly_usd, 2),
            "uncached_monthly_usd": round(uncached_monthly, 2),
            "cache_savings_monthly_usd": round(cache_savings, 2),
            "breakeven_daily_turns_vs_20_plan": breakeven_daily_at_20,
            "delta_vs_20_plan_usd": delta_vs_20,
            "vs_20_plan_verdict": verdict_20,
        })

    ranked.sort(key=lambda r: (r["monthly_usd"], r["per_turn_usd"]))

    by_id = {m["id"]: m for m in all_models}
    core_20_plans = []
    for plan in SUBSCRIPTION_PLANS:
        if plan["monthly_usd"] != 20.0:
            continue
        pm = by_id[plan["primary_api_model"]]
        tc = calc_turn_cost_usd(pm, avg_input_tokens, avg_output_tokens, hit_rate)
        api_monthly = tc["per_turn_usd"] * monthly_turns
        be_daily = round(plan["monthly_usd"] / (tc["per_turn_usd"] * days), 2) if tc["per_turn_usd"] > 0 else None
        diff = round(api_monthly - plan["monthly_usd"], 2)
        core_20_plans.append({
            "plan_id": plan["id"],
            "plan_name": plan["name"],
            "plan_monthly_usd": plan["monthly_usd"],
            "benchmark_model_id": pm["id"],
            "benchmark_model_name": pm["name"],
            "equivalent_api_monthly_usd": round(api_monthly, 2),
            "breakeven_daily_turns": be_daily,
            "monthly_savings_with_subscription_usd": diff,
            "recommendation": (
                "SUBSCRIPTION_CHEAPER"
                if diff > 0.01
                else ("API_CHEAPER" if diff < -0.01 else "BREAK_EVEN")
            ),
        })

    return {
        "workload": {
            "daily_turns": daily_turns,
            "turns_per_session": turns_per_session,
            "days": days,
            "monthly_turns": round(monthly_turns, 2),
            "avg_input_tokens": avg_input_tokens,
            "avg_output_tokens": avg_output_tokens,
            "cache_hit_rate": round(hit_rate, 4),
            "cache_hit_pct": round(hit_rate * 100.0, 2),
        },
        "cheapest_model": ranked[0]["id"],
        "models": ranked,
        "subscription_breakeven_20_usd": core_20_plans,
    }


def estimate_text_tokens(text: str) -> dict:
    """
    Bilingual EN/CJK/code token estimator modeled on TokenCost Zero.

    - CJK characters: ~1.45 tokens per character
    - Dense code/JSON punctuation: accounted for so minified payloads aren't undercounted
    - ASCII/Latin prose: ~3.8 characters per token
    """
    if not text:
        return {
            "estimated_tokens": 0,
            "chars": 0,
            "lines": 0,
            "words_and_cjk": 0,
            "cjk_chars": 0,
            "cjk_ratio": 0.0,
            "symbol_ratio": 0.0,
        }
    chars = len(text)
    lines = text.count("\n") + 1
    cjk_chars = len(CJK_RE.findall(text))
    non_cjk = chars - cjk_chars
    words = len(WORD_RE.findall(text)) + cjk_chars
    symbols = len(CODE_SYMBOL_RE.findall(text))
    symbol_ratio = symbols / max(1, non_cjk)
    chars_per_token = 3.25 if symbol_ratio >= 0.14 else 3.8
    est_tokens = int(math.ceil(cjk_chars * 1.45 + non_cjk / chars_per_token))
    return {
        "estimated_tokens": est_tokens,
        "chars": chars,
        "lines": lines,
        "words_and_cjk": words,
        "cjk_chars": cjk_chars,
        "cjk_ratio": round(cjk_chars / max(1, chars), 4),
        "symbol_ratio": round(symbol_ratio, 4),
    }


def audit_prompt_file(
    file_path: str,
    daily_turns: float = 100,
    avg_output_tokens: int = 800,
    cache_hit_rate: float = 0.70,
    trim_pct: float = 0.25,
    model_id: str = "claude-sonnet-4",
    days: int = 30,
    pricing_file: str = None,
):
    """Inspect a local prompt or codebase file, flag token bloat, and quantify caching/trimming savings."""
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    if daily_turns <= 0 or days <= 0:
        raise ValueError("daily-turns and days must be > 0")
    if avg_output_tokens < 0:
        raise ValueError("avg-output-tokens must be >= 0")

    hit_rate = normalize_rate(cache_hit_rate, "cache-hit-rate")
    trim_ratio = normalize_rate(trim_pct, "trim-pct")
    if trim_ratio >= 1.0:
        raise ValueError("trim-pct must be < 1.0 (100%)")

    with open(file_path, "r", encoding="utf-8", errors="replace") as fh:
        content = fh.read()

    stats = estimate_text_tokens(content)
    raw_lines = content.splitlines()
    total_lines = len(raw_lines)
    blank_lines = sum(1 for ln in raw_lines if not ln.strip())
    blank_ratio = blank_lines / max(1, total_lines)

    # Trailing whitespace & multi-blank runs
    excess_ws_chars = sum(len(ln) - len(ln.rstrip()) for ln in raw_lines)
    multi_space_chars = sum(len(m.group(0)) - 1 for m in re.finditer(r" {4,}", content))
    ws_overhead_ratio = (excess_ws_chars + multi_space_chars) / max(1, len(content))

    # Duplicate non-trivial lines (>= 20 chars)
    norm_lines = [re.sub(r"\s+", " ", ln.strip()) for ln in raw_lines if len(ln.strip()) >= 20]
    counts = collections.Counter(norm_lines)
    dup_occurrences = sum(c - 1 for c in counts.values() if c >= 2)
    top_dups = [{"line": k[:100], "count": c} for k, c in counts.most_common(5) if c >= 2]
    dup_ratio = dup_occurrences / max(1, len(norm_lines))

    # Pretty-printed JSON / verbose fenced code blocks
    fenced_blocks = len(re.findall(r"^```", content, re.M)) // 2
    stripped = content.strip()
    is_pretty_json = False
    json_minify_saved_tokens = 0
    if (stripped.startswith("{") and stripped.endswith("}")) or (
        stripped.startswith("[") and stripped.endswith("]")
    ):
        try:
            parsed = json.loads(stripped)
            minified = json.dumps(parsed, ensure_ascii=False, separators=(",", ":"))
            if len(minified) < len(content) * 0.90:
                is_pretty_json = True
                json_minify_saved_tokens = max(
                    0,
                    stats["estimated_tokens"] - estimate_text_tokens(minified)["estimated_tokens"],
                )
        except Exception:
            pass

    flags = []
    tok = stats["estimated_tokens"]
    if tok >= 16000:
        flags.append({
            "code": "VERY_LARGE_CONTEXT",
            "severity": "high",
            "detail": (
                f"Estimated {tok:,} input tokens per call. In multi-turn agent loops, "
                "re-sending >16k tokens per turn causes rapid bill escalation; split into "
                "cached static prefix + retrieved slices."
            ),
        })
    elif tok >= 4000:
        flags.append({
            "code": "LARGE_STATIC_PROMPT",
            "severity": "medium",
            "detail": (
                f"Estimated {tok:,} input tokens exceeds typical cache minimum thresholds "
                "(1,024–2,048 tokens). Enable prefix prompt caching to cut input rates by 50–90%."
            ),
        })

    if blank_ratio > 0.18 or ws_overhead_ratio > 0.12:
        flags.append({
            "code": "EXCESSIVE_WHITESPACE",
            "severity": "medium",
            "detail": (
                f"Blank-line ratio is {blank_ratio * 100:.1f}% and indentation/trailing "
                f"whitespace overhead is {ws_overhead_ratio * 100:.1f}%. Compact formatting "
                "can trim tokens without losing semantic content."
            ),
        })

    if dup_occurrences >= 3 or dup_ratio > 0.10:
        flags.append({
            "code": "DUPLICATE_LINES",
            "severity": "medium",
            "detail": (
                f"Detected {dup_occurrences} repeated non-trivial lines ({dup_ratio * 100:.1f}% "
                "of long lines). Deduplicate repeated rules, examples, or schema fields."
            ),
        })

    if is_pretty_json:
        flags.append({
            "code": "UNMINIFIED_JSON",
            "severity": "medium",
            "detail": (
                f"Pretty-printed JSON detected; minifying saves ~{json_minify_saved_tokens:,} "
                "tokens per request with zero data loss."
            ),
        })

    if fenced_blocks >= 6:
        flags.append({
            "code": "HEAVY_EXAMPLE_BLOCKS",
            "severity": "low",
            "detail": (
                f"Contains {fenced_blocks} fenced code/example blocks. Keep only 1–2 canonical "
                "few-shot examples inline and move extended references to external docs."
            ),
        })

    if stats["cjk_ratio"] >= 0.30:
        flags.append({
            "code": "HIGH_CJK_DENSITY",
            "severity": "low",
            "detail": (
                f"CJK characters make up {stats['cjk_ratio'] * 100:.1f}% of the file "
                "(~1.45 tokens/char). Use concise English/ASCII keys for structured schemas."
            ),
        })

    if not flags:
        flags.append({
            "code": "LEAN_PROMPT",
            "severity": "info",
            "detail": "No obvious structural token bloat detected; prompt size and formatting look compact.",
        })

    models = load_models(pricing_file)
    target_model = find_model(models, model_id)
    monthly_turns = daily_turns * days
    trimmed_tokens = int(round(tok * (1.0 - trim_ratio)))

    def scenario_block(m: dict):
        base = calc_turn_cost_usd(m, tok, avg_output_tokens, 0.0)["per_turn_usd"] * monthly_turns
        cached = calc_turn_cost_usd(m, tok, avg_output_tokens, hit_rate)["per_turn_usd"] * monthly_turns
        trimmed = calc_turn_cost_usd(m, trimmed_tokens, avg_output_tokens, 0.0)["per_turn_usd"] * monthly_turns
        combined = calc_turn_cost_usd(m, trimmed_tokens, avg_output_tokens, hit_rate)["per_turn_usd"] * monthly_turns
        return {
            "model_id": m["id"],
            "model_name": m["name"],
            "baseline_monthly_usd": round(base, 2),
            "with_caching_monthly_usd": round(cached, 2),
            "caching_savings_monthly_usd": round(base - cached, 2),
            "with_trimming_monthly_usd": round(trimmed, 2),
            "trimming_savings_monthly_usd": round(base - trimmed, 2),
            "combined_monthly_usd": round(combined, 2),
            "combined_savings_monthly_usd": round(base - combined, 2),
            "combined_savings_annual_usd": round((base - combined) * 12.0, 2),
            "combined_reduction_pct": round(((base - combined) / base) * 100.0, 2) if base > 0 else 0.0,
        }

    benchmark_ids = [target_model["id"]]
    for alt in ("gpt-5", "claude-sonnet-4", "gemini-2.5-pro", "deepseek-v3"):
        if alt not in benchmark_ids and any(m["id"] == alt for m in models):
            benchmark_ids.append(alt)

    comparisons = [scenario_block(find_model(models, mid)) for mid in benchmark_ids]

    return {
        "file": os.path.basename(file_path),
        "bytes": os.path.getsize(file_path),
        "token_stats": stats,
        "structure": {
            "blank_lines": blank_lines,
            "blank_ratio": round(blank_ratio, 4),
            "whitespace_overhead_ratio": round(ws_overhead_ratio, 4),
            "duplicate_long_lines": dup_occurrences,
            "fenced_code_blocks": fenced_blocks,
            "is_pretty_json": is_pretty_json,
            "json_minify_saved_tokens": json_minify_saved_tokens,
            "top_repeated_lines": top_dups,
        },
        "bloat_flags": flags,
        "assumptions": {
            "daily_turns": daily_turns,
            "days": days,
            "monthly_turns": round(monthly_turns, 2),
            "avg_output_tokens": avg_output_tokens,
            "target_cache_hit_rate": round(hit_rate, 4),
            "target_trim_pct": round(trim_ratio, 4),
            "trimmed_input_tokens": trimmed_tokens,
        },
        "target_model_savings": comparisons[0],
        "model_benchmarks": comparisons,
    }


def compare_subscription_plans(
    daily_turns: float,
    avg_input_tokens: int,
    avg_output_tokens: int,
    cache_hit_rate: float = 0.5,
    days: int = 30,
    model_id: str = "",
    custom_plan_usd: float = None,
    pricing_file: str = None,
):
    """Compare pay-as-you-go API spend vs flat-rate subscriptions and compute exact break-even points."""
    if daily_turns <= 0 or days <= 0:
        raise ValueError("daily-turns and days must be > 0")
    if avg_input_tokens < 0 or avg_output_tokens < 0:
        raise ValueError("Token counts must be >= 0")

    hit_rate = normalize_rate(cache_hit_rate, "cache-hit-rate")
    models = load_models(pricing_file)
    override_model = find_model(models, model_id) if model_id.strip() else None
    monthly_turns = daily_turns * days

    plans_to_eval = list(SUBSCRIPTION_PLANS)
    if custom_plan_usd is not None:
        if custom_plan_usd <= 0:
            raise ValueError("custom-plan-usd must be > 0")
        plans_to_eval.append({
            "id": "custom-plan",
            "name": f"Custom Subscription (${custom_plan_usd:.2f}/mo)",
            "monthly_usd": float(custom_plan_usd),
            "primary_api_model": override_model["id"] if override_model else "claude-sonnet-4",
            "secondary_api_model": "gpt-5",
            "notes": "User-supplied flat-rate seat price",
        })

    rows = []
    for plan in plans_to_eval:
        m = override_model if override_model else find_model(models, plan["primary_api_model"])
        tc = calc_turn_cost_usd(m, avg_input_tokens, avg_output_tokens, hit_rate)
        per_turn = tc["per_turn_usd"]
        api_monthly = per_turn * monthly_turns
        be_monthly_turns = int(math.ceil(plan["monthly_usd"] / per_turn)) if per_turn > 0 else None
        be_daily_turns = round(plan["monthly_usd"] / (per_turn * days), 2) if per_turn > 0 else None
        delta = round(api_monthly - plan["monthly_usd"], 2)
        if delta > 0.01:
            winner = "SUBSCRIPTION"
        elif delta < -0.01:
            winner = "PAY_AS_YOU_GO_API"
        else:
            winner = "BREAK_EVEN"
        rows.append({
            "plan_id": plan["id"],
            "plan_name": plan["name"],
            "plan_monthly_usd": plan["monthly_usd"],
            "matched_api_model_id": m["id"],
            "matched_api_model_name": m["name"],
            "api_per_turn_usd": round(per_turn, 6),
            "api_monthly_usd": round(api_monthly, 2),
            "monthly_savings_vs_api_usd": delta,
            "breakeven_daily_turns": be_daily_turns,
            "breakeven_monthly_turns": be_monthly_turns,
            "cheaper_option": winner,
            "notes": plan["notes"],
        })

    # Compute hybrid-routing reference (80% economy/open-weight + 20% flagship)
    econ_model = find_model(models, "deepseek-v3")
    flag_model = override_model if override_model else find_model(models, "claude-sonnet-4")
    econ_turn = calc_turn_cost_usd(econ_model, avg_input_tokens, avg_output_tokens, hit_rate)["per_turn_usd"]
    flag_turn = calc_turn_cost_usd(flag_model, avg_input_tokens, avg_output_tokens, hit_rate)["per_turn_usd"]
    hybrid_monthly = (0.80 * econ_turn + 0.20 * flag_turn) * monthly_turns

    return {
        "workload": {
            "daily_turns": daily_turns,
            "days": days,
            "monthly_turns": round(monthly_turns, 2),
            "avg_input_tokens": avg_input_tokens,
            "avg_output_tokens": avg_output_tokens,
            "cache_hit_rate": round(hit_rate, 4),
            "cache_hit_pct": round(hit_rate * 100.0, 2),
        },
        "plan_comparisons": rows,
        "hybrid_routing_reference": {
            "split": f"80% {econ_model['id']} + 20% {flag_model['id']}",
            "estimated_monthly_usd": round(hybrid_monthly, 2),
        },
    }


def format_estimate_markdown(data: dict) -> str:
    w = data["workload"]
    lines = [
        f"## LLM API Cost Estimate ({w['daily_turns']} turns/day x {w['days']}d = {w['monthly_turns']} turns/mo)",
        (
            f"- Context: **{w['avg_input_tokens']:,}** input / **{w['avg_output_tokens']:,}** output tokens/turn "
            f"| Cache hit rate: **{w['cache_hit_pct']}%** | Session: **{w['turns_per_session']}** turns"
        ),
        "",
        "| Rank | Model | Provider | Eff. In / 1M | Out / 1M | Per Session | Monthly (30d) | Cache Saved | vs $20 Plan |",
        "| ---: | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for idx, r in enumerate(data["models"], 1):
        lines.append(
            f"| {idx} | {r['name']} | {r['provider']} | ${r['effective_input_per_1m']:.3f} | "
            f"${r['output_per_1m']:.2f} | ${r['per_session_usd']:.4f} | **${r['monthly_usd']:,.2f}** | "
            f"${r['cache_savings_monthly_usd']:,.2f} | {r['vs_20_plan_verdict']} ({r['breakeven_daily_turns_vs_20_plan']} t/d BE) |"
        )
    lines.extend([
        "",
        "### $20 Flat-Rate Subscription Break-Even",
        "",
        "| Plan | Monthly | Benchmark API Model | Equiv. API Monthly | Break-Even Turns/Day | Verdict |",
        "| --- | ---: | --- | ---: | ---: | --- |",
    ])
    for p in data["subscription_breakeven_20_usd"]:
        lines.append(
            f"| {p['plan_name']} | ${p['plan_monthly_usd']:.2f} | {p['benchmark_model_name']} | "
            f"${p['equivalent_api_monthly_usd']:,.2f} | {p['breakeven_daily_turns']} | {p['recommendation']} |"
        )
    return "\n".join(lines)


def format_audit_markdown(data: dict) -> str:
    ts = data["token_stats"]
    t = data["target_model_savings"]
    a = data["assumptions"]
    lines = [
        f"## Prompt Audit: `{data['file']}` ({data['bytes']:,} bytes)",
        (
            f"- Estimated tokens: **{ts['estimated_tokens']:,}** | Chars: **{ts['chars']:,}** | "
            f"Lines: **{ts['lines']:,}** | CJK ratio: **{ts['cjk_ratio'] * 100:.1f}%**"
        ),
        "",
        "### Bloat Diagnostics",
    ]
    for f in data["bloat_flags"]:
        lines.append(f"- **[{f['severity'].upper()}] `{f['code']}`**: {f['detail']}")
    lines.extend([
        "",
        (
            f"### Monthly Cost & Savings ({a['daily_turns']} turns/day, "
            f"{a['target_cache_hit_rate'] * 100:.0f}% cache hit, {a['target_trim_pct'] * 100:.0f}% trim)"
        ),
        "",
        "| Model | Baseline / mo | Caching Only | Trimming Only | Combined / mo | Monthly Saved | Annual Saved | Reduction |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ])
    for b in data["model_benchmarks"]:
        lines.append(
            f"| {b['model_name']} | ${b['baseline_monthly_usd']:,.2f} | "
            f"${b['with_caching_monthly_usd']:,.2f} | ${b['with_trimming_monthly_usd']:,.2f} | "
            f"**${b['combined_monthly_usd']:,.2f}** | ${b['combined_savings_monthly_usd']:,.2f} | "
            f"${b['combined_savings_annual_usd']:,.2f} | {b['combined_reduction_pct']:.1f}% |"
        )
    lines.append("")
    lines.append(
        f"Primary target (`{t['model_id']}`): saves **${t['combined_savings_monthly_usd']:,.2f}/mo** "
        f"(**${t['combined_savings_annual_usd']:,.2f}/yr**, -{t['combined_reduction_pct']:.1f}%)."
    )
    return "\n".join(lines)


def format_compare_markdown(data: dict) -> str:
    w = data["workload"]
    lines = [
        f"## Pay-As-You-Go API vs Flat-Rate Subscriptions ({w['daily_turns']} turns/day, {w['days']}d)",
        (
            f"- Context: **{w['avg_input_tokens']:,}** in / **{w['avg_output_tokens']:,}** out | "
            f"Cache hit: **{w['cache_hit_pct']}%**"
        ),
        "",
        "| Plan | Plan / mo | Matched API Model | API / mo | Delta (API - Plan) | Break-Even Turns/Day | Cheaper Option |",
        "| --- | ---: | --- | ---: | ---: | ---: | --- |",
    ]
    for r in data["plan_comparisons"]:
        sign = "+" if r["monthly_savings_vs_api_usd"] > 0 else ""
        lines.append(
            f"| {r['plan_name']} | ${r['plan_monthly_usd']:.2f} | {r['matched_api_model_name']} | "
            f"${r['api_monthly_usd']:,.2f} | {sign}${r['monthly_savings_vs_api_usd']:,.2f} | "
            f"{r['breakeven_daily_turns']} | **{r['cheaper_option']}** |"
        )
    h = data["hybrid_routing_reference"]
    lines.append("")
    lines.append(f"- Hybrid routing reference ({h['split']}): **${h['estimated_monthly_usd']:,.2f}/mo**")
    return "\n".join(lines)


def format_models_markdown(models: list) -> str:
    lines = [
        "## Built-In 2026 Reference API Pricing (USD / 1M Tokens)",
        "",
        "| ID | Model | Provider | Tier | Context | Input | Cached Input | Output |",
        "| --- | --- | --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for m in models:
        lines.append(
            f"| `{m['id']}` | {m['name']} | {m['provider']} | {m['tier']} | "
            f"{m['context_window']:,} | ${m['input_per_1m']:.2f} | "
            f"${m['cached_input_per_1m']:.4f} | ${m['output_per_1m']:.2f} |"
        )
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="llm_cost.py",
        description=(
            "Offline zero-dependency LLM token counter, multi-model API cost "
            "estimator, prompt bloat auditor, and subscription break-even CLI."
        ),
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    p_est = sub.add_parser("estimate", help="Rank monthly & per-session API costs across flagship & open models")
    p_est.add_argument("--daily-turns", type=float, default=50.0, help="Average turns/requests per day")
    p_est.add_argument("--avg-input-tokens", type=int, default=4000, help="Average input tokens per turn")
    p_est.add_argument("--avg-output-tokens", type=int, default=800, help="Average output tokens per turn")
    p_est.add_argument(
        "--cache-hit-rate",
        type=float,
        default=0.5,
        help="Prompt cache hit rate as 0.0-1.0 (or 0-100 percentage)",
    )
    p_est.add_argument("--turns-per-session", type=int, default=10, help="Turns per interactive session")
    p_est.add_argument("--days", type=int, default=30, help="Billing days per month")
    p_est.add_argument("--models", default="", help="Optional comma-separated model IDs, providers, or tiers")
    p_est.add_argument("--format", choices=["json", "markdown"], default="json")
    p_est.add_argument("--pricing-file", default=None, help="Optional custom JSON pricing override file")

    p_aud = sub.add_parser("audit-prompt", help="Count file tokens, detect bloat, and quantify caching/trimming savings")
    p_aud.add_argument("--file", required=True, help="Path to local prompt, markdown spec, JSON, or source file")
    p_aud.add_argument("--daily-turns", type=float, default=100.0, help="Projected daily calls using this file")
    p_aud.add_argument("--avg-output-tokens", type=int, default=800, help="Expected output tokens per call")
    p_aud.add_argument("--cache-hit-rate", type=float, default=0.70, help="Target cache hit rate (0.0-1.0 or 0-100)")
    p_aud.add_argument("--trim-pct", type=float, default=0.25, help="Projected context trimming ratio (0.0-1.0 or 0-100)")
    p_aud.add_argument("--model", default="claude-sonnet-4", help="Primary model ID for cost impact")
    p_aud.add_argument("--days", type=int, default=30)
    p_aud.add_argument("--format", choices=["json", "markdown"], default="json")
    p_aud.add_argument("--pricing-file", default=None)

    p_cmp = sub.add_parser("compare-plans", help="Break-even calculator: pay-as-you-go API vs flat-rate subscriptions")
    p_cmp.add_argument("--daily-turns", type=float, default=40.0)
    p_cmp.add_argument("--avg-input-tokens", type=int, default=6000)
    p_cmp.add_argument("--avg-output-tokens", type=int, default=1200)
    p_cmp.add_argument("--cache-hit-rate", type=float, default=0.5)
    p_cmp.add_argument("--days", type=int, default=30)
    p_cmp.add_argument("--model", default="", help="Optional single model ID to benchmark against all plans")
    p_cmp.add_argument("--custom-plan-usd", type=float, default=None, help="Optional custom monthly subscription USD")
    p_cmp.add_argument("--format", choices=["json", "markdown"], default="json")
    p_cmp.add_argument("--pricing-file", default=None)

    p_ls = sub.add_parser("list-models", help="Display built-in 2026 reference API pricing table")
    p_ls.add_argument("--format", choices=["json", "markdown"], default="json")
    p_ls.add_argument("--pricing-file", default=None)

    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.cmd == "estimate":
            res = estimate_workload(
                daily_turns=args.daily_turns,
                avg_input_tokens=args.avg_input_tokens,
                avg_output_tokens=args.avg_output_tokens,
                cache_hit_rate=args.cache_hit_rate,
                turns_per_session=args.turns_per_session,
                days=args.days,
                model_filter=args.models,
                pricing_file=args.pricing_file,
            )
            print(format_estimate_markdown(res) if args.format == "markdown" else json.dumps(res, indent=2, ensure_ascii=False))
        elif args.cmd == "audit-prompt":
            res = audit_prompt_file(
                file_path=args.file,
                daily_turns=args.daily_turns,
                avg_output_tokens=args.avg_output_tokens,
                cache_hit_rate=args.cache_hit_rate,
                trim_pct=args.trim_pct,
                model_id=args.model,
                days=args.days,
                pricing_file=args.pricing_file,
            )
            print(format_audit_markdown(res) if args.format == "markdown" else json.dumps(res, indent=2, ensure_ascii=False))
        elif args.cmd == "compare-plans":
            res = compare_subscription_plans(
                daily_turns=args.daily_turns,
                avg_input_tokens=args.avg_input_tokens,
                avg_output_tokens=args.avg_output_tokens,
                cache_hit_rate=args.cache_hit_rate,
                days=args.days,
                model_id=args.model,
                custom_plan_usd=args.custom_plan_usd,
                pricing_file=args.pricing_file,
            )
            print(format_compare_markdown(res) if args.format == "markdown" else json.dumps(res, indent=2, ensure_ascii=False))
        elif args.cmd == "list-models":
            models = load_models(args.pricing_file)
            if args.format == "markdown":
                print(format_models_markdown(models))
            else:
                print(json.dumps({"model_count": len(models), "models": models}, indent=2, ensure_ascii=False))
        else:
            parser.error(f"Unknown command: {args.cmd}")
            return 2
    except Exception as exc:
        print(json.dumps({"error": str(exc), "command": args.cmd}, indent=2, ensure_ascii=False), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
