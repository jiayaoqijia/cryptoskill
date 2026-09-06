#!/usr/bin/env python3
"""
katbot_trigger_setup.py — Interactive wizard to configure signal triggers.

Creates or updates ~/.openclaw/workspace/katbot_signal_trigger.json, which
controls which Market-Intelligence signal types fire the research →
recommendation workflow.

Run this once after onboarding, or any time you want to reconfigure:
  PYTHONPATH={baseDir}/tools python3 {baseDir}/tools/katbot_trigger_setup.py
"""
import json
import os
import sys
import pathlib

_TOOLS_DIR = str(pathlib.Path(__file__).parent.resolve())
TRIGGER_CONFIG_PATH = os.path.expanduser(
    "~/.openclaw/workspace/katbot_signal_trigger.json"
)

DEFAULT_SIGNALS = {
    "momentum":        {"enabled": False, "threshold_abs": 0.6, "min_tokens": 2},
    "volume_breakout": {"enabled": False, "z_score_threshold": 2.0},
    "whale_activity":  {"enabled": False, "min_net_flow_usd": 500000},
    "trending":        {"enabled": False, "min_article_volume": 10},
}

SIGNAL_DESCRIPTIONS = {
    "momentum":        "Sentiment-delta momentum: fires when aggregate sentiment shifts sharply",
    "volume_breakout": "Volume breakout: fires when article-volume Z-score spikes above threshold",
    "whale_activity":  "Whale activity: fires when whale net-flow magnitude exceeds threshold",
    "trending":        "Trending: fires when a new token surges in article volume",
}

SIGNAL_THRESHOLD_PROMPTS = {
    "momentum": [
        ("threshold_abs", float,
         "Sentiment delta threshold (absolute value, 0–1, default 0.6): ", 0.6),
        ("min_tokens", int,
         "Minimum tokens crossing threshold to fire (default 2): ", 2),
    ],
    "volume_breakout": [
        ("z_score_threshold", float,
         "Volume Z-score threshold (default 2.0): ", 2.0),
    ],
    "whale_activity": [
        ("min_net_flow_usd", float,
         "Minimum whale net-flow in USD to fire (default 500000): ", 500000.0),
    ],
    "trending": [
        ("min_article_volume", int,
         "Minimum article volume to fire (default 10): ", 10),
    ],
}


def _prompt(prompt_text: str, default=None, cast=str) -> object:
    suffix = f" [{default}]" if default is not None else ""
    try:
        raw = input(f"{prompt_text}{suffix}: ").strip()
    except (EOFError, KeyboardInterrupt):
        print()
        sys.exit(0)
    if not raw and default is not None:
        return default
    try:
        return cast(raw) if raw else default
    except (ValueError, TypeError):
        print(f"  Invalid input, using default: {default}")
        return default


def _prompt_yn(prompt_text: str, default: bool = True) -> bool:
    suffix = " [Y/n]" if default else " [y/N]"
    try:
        raw = input(f"{prompt_text}{suffix}: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print()
        sys.exit(0)
    if not raw:
        return default
    return raw in ("y", "yes")


def _load_existing() -> dict | None:
    if os.path.exists(TRIGGER_CONFIG_PATH):
        try:
            with open(TRIGGER_CONFIG_PATH) as f:
                return json.load(f)
        except Exception:
            pass
    return None


def main():
    print("=" * 60)
    print("  Katbot Signal Trigger Setup Wizard")
    print("=" * 60)
    print(f"\nConfig will be written to:\n  {TRIGGER_CONFIG_PATH}\n")

    existing = _load_existing()
    if existing:
        print("Found an existing trigger config. You can update it below.")
        print("Press Enter at any prompt to keep the current value.\n")

    # --- Portfolio ID ---
    default_portfolio_id = (existing or {}).get("portfolio_id")
    if not default_portfolio_id:
        try:
            from katbot_client import get_config
            cfg = get_config()
            default_portfolio_id = cfg.get("portfolio_id")
        except Exception:
            pass

    portfolio_id = _prompt(
        "Portfolio ID", default=default_portfolio_id, cast=int
    )
    if not portfolio_id:
        print("ERROR: Portfolio ID is required. Run onboarding first.")
        sys.exit(1)

    # --- Agent ID ---
    default_agent_id = (existing or {}).get("agent_id")
    if not default_agent_id:
        try:
            from katbot_client import get_token, get_portfolio_agent
            token = get_token()
            assignment = get_portfolio_agent(token, portfolio_id)
            default_agent_id = assignment.get("agent_id")
        except Exception:
            pass

    agent_id = _prompt(
        "Primary Agent ID (leave blank to skip)", default=default_agent_id, cast=int
    )

    # --- Notify channel ---
    existing_notify = (existing or {}).get("notify", {})
    notify_channel = _prompt(
        "Alert channel (e.g. telegram, slack, discord; blank = stdout only)",
        default=existing_notify.get("channel", ""),
        cast=str,
    )
    notify_target = ""
    if notify_channel:
        notify_target = _prompt(
            "Alert target (chat ID, user handle, etc.)",
            default=existing_notify.get("target", ""),
            cast=str,
        )

    # --- Signal types ---
    print("\n--- Signal Types ---")
    print("Enable the signals you want to monitor. Each fires the research→recommendation workflow.")
    print()
    signals = {}
    existing_signals = (existing or {}).get("signals", DEFAULT_SIGNALS)

    for signal_name, description in SIGNAL_DESCRIPTIONS.items():
        current = existing_signals.get(signal_name, DEFAULT_SIGNALS[signal_name]).copy()
        currently_on = current.get("enabled", False)
        print(f"  {signal_name}: {description}")
        enable = _prompt_yn(f"  Enable '{signal_name}'?", default=currently_on)
        current["enabled"] = enable

        if enable:
            for key, cast, prompt_text, default_val in SIGNAL_THRESHOLD_PROMPTS.get(signal_name, []):
                current_val = current.get(key, default_val)
                current[key] = _prompt(f"    {prompt_text}", default=current_val, cast=cast)
        signals[signal_name] = current
        print()

    if not any(v.get("enabled") for v in signals.values()):
        print("WARNING: No signals enabled. The trigger will never fire.")
        print("         Re-run this wizard to enable signals.\n")

    # --- Workflow settings ---
    print("--- Workflow Settings ---")
    auto_start = _prompt_yn(
        "Auto-start research→recommendation workflow on signal fire?",
        default=(existing or {}).get("auto_start_workflow", True),
    )
    auto_execute = False
    if auto_start:
        auto_execute = _prompt_yn(
            "Auto-execute trades on recommendation completion? (NOT recommended)",
            default=(existing or {}).get("auto_execute_trade", False),
        )
        if auto_execute:
            print(
                "  ⚠️  WARNING: auto_execute_trade=true causes unattended trade execution.\n"
                "              Katbot skill rules strongly advise against this setting.\n"
            )

    # --- Build and write config ---
    config = {
        "version": 1,
        "portfolio_id": portfolio_id,
        "agent_id": agent_id,
        "notify": {"channel": notify_channel, "target": notify_target},
        "signals": signals,
        "auto_start_workflow": auto_start,
        "auto_execute_trade": auto_execute,
    }

    os.makedirs(os.path.dirname(TRIGGER_CONFIG_PATH), exist_ok=True)
    with open(TRIGGER_CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)
    try:
        os.chmod(TRIGGER_CONFIG_PATH, 0o600)
    except Exception:
        pass

    print(f"\n✅  Config written to: {TRIGGER_CONFIG_PATH}")
    print(json.dumps(config, indent=2))

    # --- Cron line ---
    tools_dir = _TOOLS_DIR
    base_dir = str(pathlib.Path(tools_dir).parent)
    cron_line = (
        f"*/10 * * * * bash {tools_dir}/ensure_env.sh {base_dir} "
        f"&& PYTHONPATH={tools_dir} python3 {tools_dir}/katbot_signal_trigger.py"
        f" >> /tmp/katbot_trigger.log 2>&1"
    )

    print(f"""
--- Next Steps ---

1. Test with dry-run (no alerts, no workflow):
   PYTHONPATH={tools_dir} python3 {tools_dir}/katbot_signal_trigger.py --dry-run

2. Force a test fire (bypasses dedup):
   PYTHONPATH={tools_dir} python3 {tools_dir}/katbot_signal_trigger.py --force

3. Schedule on a 10-minute cadence (add to crontab):
   {cron_line}

   To edit crontab: crontab -e
""")


if __name__ == "__main__":
    main()
