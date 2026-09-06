#!/usr/bin/env python3
"""
katbot_signal_trigger.py — 10-minute cadence signal monitor.

Evaluates four Katbot Market-Intelligence signal types and, when at least
one is clear, sends an openclaw alert and optionally starts the
research → recommendation workflow.

Run with ensure_env.sh before each invocation:
  bash {baseDir}/tools/ensure_env.sh {baseDir}
  PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_signal_trigger.py

Flags:
  --dry-run   Print what would fire; no alerts or workflow starts.
  --force     Bypass dedup (useful for testing).
"""
import argparse
import json
import os
import subprocess
import sys
import time
import pathlib

_TOOLS_DIR = str(pathlib.Path(__file__).parent.resolve())

TRIGGER_CONFIG_PATH = os.path.expanduser(
    "~/.openclaw/workspace/katbot_signal_trigger.json"
)
STATE_PATH = os.path.expanduser(
    "~/.openclaw/workspace/memory/katbot_signal_state.json"
)

# Suppress a signal that fired for the same token+direction within this window
DEDUP_SECONDS = 600  # 10 minutes


# ---------------------------------------------------------------------------
# State helpers
# ---------------------------------------------------------------------------

def _load_state() -> dict:
    try:
        with open(STATE_PATH) as f:
            return json.load(f)
    except Exception:
        return {}


def _save_state(state: dict):
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    with open(STATE_PATH, "w") as f:
        json.dump(state, f, indent=2)


def _dedup_key(signal_name: str, token: str, direction: str) -> str:
    return f"{signal_name}:{token}:{direction}"


def _is_suppressed(state: dict, key: str, force: bool) -> bool:
    if force:
        return False
    entry = state.get(key)
    if not entry:
        return False
    last_fire = entry.get("last_fire", 0)
    return (time.time() - last_fire) < DEDUP_SECONDS


def _record_fire(state: dict, key: str):
    state[key] = {"last_fire": time.time()}


# ---------------------------------------------------------------------------
# Alert
# ---------------------------------------------------------------------------

def _send_alert(config: dict, message: str, dry_run: bool):
    notify = config.get("notify", {})
    channel = notify.get("channel", "")
    target = notify.get("target", "")

    if dry_run:
        print(f"[DRY-RUN] Would send alert:\n{message}")
        return

    if channel and target:
        subprocess.run(
            ["openclaw", "message", "send",
             "--channel", channel,
             "--target", target,
             "--message", message],
            capture_output=True, text=True,
        )
    print(message)


# ---------------------------------------------------------------------------
# Signal evaluation
# ---------------------------------------------------------------------------

def _eval_momentum(config: dict, token_obj, state: dict, force: bool,
                   sentiment_data: list) -> list:
    """Returns list of (key, token, direction, rationale) tuples that fired."""
    cfg = config["signals"].get("momentum", {})
    threshold = cfg.get("threshold_abs", 0.6)
    min_tokens = cfg.get("min_tokens", 2)

    fired = []
    for item in sentiment_data:
        sym = item.get("symbol") or item.get("token", "")
        score = float(item.get("score") or item.get("sentiment_score") or 0)
        direction = "BULLISH" if score > 0 else "BEARISH"

        prev_score_key = f"momentum_prev:{sym}"
        prev_entry = state.get(prev_score_key, {})
        prev_score = float(prev_entry.get("score", 0))
        delta = abs(score - prev_score)

        # Update stored score regardless of fire
        state[prev_score_key] = {"score": score}

        if delta >= threshold:
            key = _dedup_key("momentum", sym, direction)
            if not _is_suppressed(state, key, force):
                fired.append((key, sym, direction,
                               f"Sentiment delta {delta:.2f} (now {score:.2f}) >= {threshold}"))

    return fired if len(fired) >= min_tokens else []


def _eval_volume_breakout(config: dict, state: dict, force: bool,
                          trending_data: list) -> list:
    cfg = config["signals"].get("volume_breakout", {})
    z_thresh = cfg.get("z_score_threshold", 2.0)

    # Compute a simple Z-score from the article volumes in this response
    volumes = []
    for item in trending_data:
        v = item.get("article_volume") or item.get("volume") or 0
        try:
            volumes.append(float(v))
        except (TypeError, ValueError):
            pass

    if len(volumes) < 3:
        return []

    mean = sum(volumes) / len(volumes)
    variance = sum((x - mean) ** 2 for x in volumes) / len(volumes)
    std = variance ** 0.5 if variance > 0 else 1.0

    fired = []
    for item, vol in zip(trending_data, volumes):
        sym = item.get("symbol") or item.get("token", "")
        z = (vol - mean) / std
        if z >= z_thresh:
            direction = "TRENDING"
            key = _dedup_key("volume_breakout", sym, direction)
            if not _is_suppressed(state, key, force):
                fired.append((key, sym, direction,
                               f"Article volume Z-score {z:.2f} >= {z_thresh}"))
    return fired


def _eval_whale_activity(config: dict, state: dict, force: bool,
                          whale_data: list) -> list:
    cfg = config["signals"].get("whale_activity", {})
    min_flow = cfg.get("min_net_flow_usd", 500000)

    fired = []
    for item in whale_data:
        sym = item.get("symbol") or item.get("token", "")
        net = abs(float(item.get("net_flow_usd") or item.get("net_flow") or 0))
        direction = item.get("direction", "LONG" if net >= 0 else "SHORT")
        if net >= min_flow:
            key = _dedup_key("whale_activity", sym, direction)
            if not _is_suppressed(state, key, force):
                fired.append((key, sym, direction,
                               f"Whale net-flow ${net:,.0f} >= ${min_flow:,.0f}"))
    return fired


def _eval_trending(config: dict, state: dict, force: bool,
                   trending_data: list, portfolio_tokens: list) -> list:
    cfg = config["signals"].get("trending", {})
    min_vol = cfg.get("min_article_volume", 10)

    fired = []
    for item in trending_data:
        sym = item.get("symbol") or item.get("token", "")
        vol = float(item.get("article_volume") or item.get("volume") or 0)
        if vol >= min_vol and sym not in portfolio_tokens:
            key = _dedup_key("trending", sym, "NEW")
            if not _is_suppressed(state, key, force):
                fired.append((key, sym, "NEW",
                               f"Article volume {vol:.0f} >= {min_vol}, new to portfolio"))
    return fired


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Katbot signal trigger — run on a 10-min cadence."
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Print what would fire; no alerts or workflow starts.")
    parser.add_argument("--force", action="store_true",
                        help="Bypass dedup suppression (for testing).")
    args = parser.parse_args()

    # --- Load config ---
    if not os.path.exists(TRIGGER_CONFIG_PATH):
        print(
            "No trigger config found. Run the setup wizard first:\n"
            f"  PYTHONPATH={_TOOLS_DIR} python3 {_TOOLS_DIR}/katbot_trigger_setup.py"
        )
        sys.exit(0)

    with open(TRIGGER_CONFIG_PATH) as f:
        config = json.load(f)

    portfolio_id = config.get("portfolio_id")
    if not portfolio_id:
        print("ERROR: trigger config missing portfolio_id. Re-run katbot_trigger_setup.py.")
        sys.exit(1)

    signals_cfg = config.get("signals", {})

    # --- Auth ---
    try:
        from katbot_client import (
            get_token, get_portfolio,
            get_trending_tokens, get_aggregated_sentiment, get_whale_flow,
        )
        token = get_token()
    except Exception as e:
        print(f"ERROR: Auth failed: {e}", file=sys.stderr)
        sys.exit(1)

    # --- Load state ---
    state = _load_state()

    # --- Fetch market-intel data ---
    trending_data = []
    sentiment_data = []
    whale_data = []
    portfolio_tokens = []

    try:
        trending_data = get_trending_tokens(token) or []
    except Exception as e:
        print(f"[WARNING] Trending fetch failed: {e}", file=sys.stderr)

    try:
        sentiment_data = get_aggregated_sentiment(token) or []
    except Exception as e:
        print(f"[WARNING] Sentiment fetch failed: {e}", file=sys.stderr)

    try:
        whale_data = get_whale_flow(token) or []
    except Exception as e:
        print(f"[WARNING] Whale-flow fetch failed: {e}", file=sys.stderr)

    try:
        portfolio = get_portfolio(token, portfolio_id, require_agent=False)
        portfolio_tokens = portfolio.get("tokens_selected") or []
    except Exception as e:
        print(f"[WARNING] Could not fetch portfolio tokens: {e}", file=sys.stderr)

    # --- Evaluate each enabled signal ---
    all_fired = []  # list of (key, sym, direction, rationale, signal_name)

    if signals_cfg.get("momentum", {}).get("enabled"):
        fired = _eval_momentum(config, None, state, args.force, sentiment_data)
        all_fired.extend([(k, s, d, r, "momentum") for k, s, d, r in fired])

    if signals_cfg.get("volume_breakout", {}).get("enabled"):
        fired = _eval_volume_breakout(config, state, args.force, trending_data)
        all_fired.extend([(k, s, d, r, "volume_breakout") for k, s, d, r in fired])

    if signals_cfg.get("whale_activity", {}).get("enabled"):
        fired = _eval_whale_activity(config, state, args.force, whale_data)
        all_fired.extend([(k, s, d, r, "whale_activity") for k, s, d, r in fired])

    if signals_cfg.get("trending", {}).get("enabled"):
        fired = _eval_trending(config, state, args.force, trending_data, portfolio_tokens)
        all_fired.extend([(k, s, d, r, "trending") for k, s, d, r in fired])

    if not all_fired:
        if args.dry_run:
            print("[DRY-RUN] No signals fired.")
        _save_state(state)
        sys.exit(0)

    # --- Group fired signals for alert ---
    signal_summary = []
    tokens_for_workflow = []
    rationale_parts = []
    signal_types_fired = set()

    for key, sym, direction, rationale, signal_name in all_fired:
        signal_summary.append(f"  [{signal_name}] {sym} ({direction}): {rationale}")
        if sym and sym not in tokens_for_workflow:
            tokens_for_workflow.append(sym)
        rationale_parts.append(f"{signal_name}:{sym}:{rationale}")
        signal_types_fired.add(signal_name)
        if not args.dry_run and not args.force:
            _record_fire(state, key)

    alert_message = (
        f"🚨 Katbot Signal Alert\n\n"
        f"Signals fired:\n" + "\n".join(signal_summary) + "\n\n"
        f"Tokens: {', '.join(tokens_for_workflow)}\n"
        f"Run the workflow to get a recommendation:\n"
        f"  PYTHONPATH={_TOOLS_DIR} python3 {_TOOLS_DIR}/katbot_workflow.py "
        f"--signal-type {list(signal_types_fired)[0]} "
        f"--tokens {','.join(tokens_for_workflow)}"
    )

    _send_alert(config, alert_message, dry_run=args.dry_run)

    # --- Optionally start workflow ---
    if config.get("auto_start_workflow") and not args.dry_run:
        workflow_cmd = [
            sys.executable,
            os.path.join(_TOOLS_DIR, "katbot_workflow.py"),
            "--portfolio-id", str(portfolio_id),
            "--signal-type", list(signal_types_fired)[0],
            "--tokens", ",".join(tokens_for_workflow),
            "--rationale", "; ".join(rationale_parts[:3]),
        ]
        print(f"\n[Trigger] Starting workflow: {' '.join(workflow_cmd)}")
        env = {**os.environ, "PYTHONPATH": _TOOLS_DIR}
        subprocess.run(workflow_cmd, env=env)
    elif args.dry_run:
        print(
            f"[DRY-RUN] Would start workflow with tokens: {tokens_for_workflow}"
        )

    _save_state(state)
    sys.exit(0)


if __name__ == "__main__":
    main()
