#!/usr/bin/env python3
"""
katbot_workflow.py — Signal-driven research → recommendation workflow.

Accepts a signal context (type, tokens, rationale) either from
katbot_signal_trigger.py or from CLI flags for manual runs.

Flow:
  signal context
    → market-intel enrichment (sentiment + whale flow)
    → reuse non-expired research result OR run_research + poll_research
    → print research summary + apply-research prompt (NEVER auto-applies)
    → request_recommendation (with signal + intel + research context)
    → poll_recommendation
    → print result (execution requires user confirmation)
"""
import sys
import os
import json
import argparse
import pathlib

_TOOLS_DIR = str(pathlib.Path(__file__).parent.resolve())

from katbot_client import (
    get_token, get_config,
    run_research, poll_research, list_research_results,
    get_aggregated_sentiment, get_whale_flow,
    request_recommendation, poll_recommendation,
)


def _warn(msg: str):
    print(f"[WARNING] {msg}", file=sys.stderr)


def _enrich(token: str, candidate_tokens: list) -> dict:
    """Fetch sentiment and whale-flow for candidate tokens. Degrades gracefully."""
    enrichment = {"sentiment": {}, "whale_flow": {}}
    try:
        sentiment_data = get_aggregated_sentiment(token)
        if isinstance(sentiment_data, list):
            for item in sentiment_data:
                sym = item.get("symbol") or item.get("token")
                if sym:
                    enrichment["sentiment"][sym] = item
    except Exception as e:
        _warn(f"Market-intelligence sentiment unavailable: {e}")

    try:
        whale_data = get_whale_flow(token)
        if isinstance(whale_data, list):
            for item in whale_data:
                sym = item.get("symbol") or item.get("token")
                if sym:
                    enrichment["whale_flow"][sym] = item
    except Exception as e:
        _warn(f"Market-intelligence whale-flow unavailable: {e}")

    return enrichment


def _summarize_enrichment(enrichment: dict, tokens: list) -> str:
    parts = []
    for sym in tokens:
        sent = enrichment["sentiment"].get(sym)
        whale = enrichment["whale_flow"].get(sym)
        line = f"{sym}:"
        if sent:
            score = sent.get("score") or sent.get("sentiment_score", "?")
            direction = sent.get("direction", "")
            line += f" sentiment={score} ({direction})"
        if whale:
            net = whale.get("net_flow_usd") or whale.get("net_flow", "?")
            wdir = whale.get("direction", "")
            line += f" whale_net_flow=${net} ({wdir})"
        if sent or whale:
            parts.append(line)
    return "; ".join(parts) if parts else "no enrichment data"


def _pick_research_result(results: list, signal_tokens: list) -> dict | None:
    """Return the first non-expired research result that overlaps with signal tokens, or most recent."""
    if not results:
        return None
    # Prefer results that mention any of the signal tokens
    for r in results:
        result_symbols = r.get("symbols") or r.get("tokens_selected") or []
        if any(t in result_symbols for t in signal_tokens):
            return r
    return results[0]


def run_workflow(token: str, portfolio_id: int,
                 signal_type: str,
                 signal_tokens: list,
                 rationale: str,
                 risk_profile: str = None,
                 time_horizon: str = None,
                 reuse_research: bool = True,
                 enrich: bool = True) -> dict:
    """Execute the full research → recommendation workflow.

    Returns the recommendation poll result dict.
    """
    print(f"\n=== Katbot Workflow: {signal_type.upper()} signal ===")
    print(f"Signal tokens : {', '.join(signal_tokens) if signal_tokens else 'none specified'}")
    print(f"Rationale     : {rationale or 'manual run'}")

    # Step 1: Market-intel enrichment
    enrichment_summary = "enrichment skipped"
    if enrich and signal_tokens:
        print("\n[1/4] Fetching market-intelligence enrichment...")
        enrichment = _enrich(token, signal_tokens)
        enrichment_summary = _summarize_enrichment(enrichment, signal_tokens)
        print(f"      Intel : {enrichment_summary}")
    else:
        print("\n[1/4] Enrichment skipped (--no-enrich or no tokens).")

    # Step 2: Research
    research_result = None
    if reuse_research:
        print("\n[2/4] Checking for non-expired research results...")
        try:
            existing = list_research_results(token, portfolio_id)
            research_result = _pick_research_result(
                existing if isinstance(existing, list) else [],
                signal_tokens,
            )
        except Exception as e:
            _warn(f"Could not list research results: {e}")

    if research_result:
        result_id = research_result.get("id") or research_result.get("result_id")
        result_symbols = research_result.get("symbols") or research_result.get("tokens_selected") or []
        print(f"      Reusing research result #{result_id}: {result_symbols}")
    else:
        print("\n[2/4] Running fresh research...")
        focus = signal_tokens[0] if signal_tokens else None
        try:
            ticket = run_research(token, portfolio_id,
                                  symbol=focus,
                                  time_horizon=time_horizon,
                                  risk_profile=risk_profile)
            ticket_id = ticket.get("ticket_id")
            print(f"      Research ticket: {ticket_id} — polling (up to 120s)...")
            research_result = poll_research(token, portfolio_id, ticket_id, max_wait=120)
        except Exception as e:
            print(f"[ERROR] Research failed: {e}", file=sys.stderr)
            sys.exit(1)

        result_id = (research_result.get("result", {}) or {}).get("id") or research_result.get("result_id")
        result_symbols = (
            (research_result.get("result", {}) or {}).get("symbols")
            or research_result.get("symbols")
            or signal_tokens
        )
        print(f"      Research complete. Result #{result_id}: {result_symbols}")

    # Step 3: Print apply-research prompt (NEVER auto-applies)
    apply_cmd = (
        f"PYTHONPATH={_TOOLS_DIR} python3 {_TOOLS_DIR}/katbot_client.py "
        f"apply-research-result {result_id}"
    ) if result_id else "(result ID unavailable)"
    print(f"""
[3/4] Research result ready.
      To apply this token selection to your portfolio, run:
        {apply_cmd}
      ⚠️  This will mutate portfolio.tokens_selected. Confirm with the user first.
""")

    # Step 4: Request recommendation
    rationale_excerpt = str(research_result)[:200] if research_result else rationale or ""
    message = (
        f"Signal={signal_type}. "
        f"Tokens={', '.join(str(t) for t in result_symbols)}. "
        f"Intel: {enrichment_summary}. "
        f"Research #{result_id}: {rationale_excerpt}. "
        f"Recommend a trade setup with entry, TP, SL, and leverage."
    )

    print("[4/4] Requesting recommendation from agent...")
    try:
        ticket = request_recommendation(token, portfolio_id, message)
        ticket_id = ticket.get("ticket_id")
        print(f"      Recommendation ticket: {ticket_id} — polling (up to 60s)...")
        rec_result = poll_recommendation(token, ticket_id, max_wait=60)
    except Exception as e:
        print(f"[ERROR] Recommendation failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\n=== Recommendation Result ===")
    print(json.dumps(rec_result, indent=2, default=str))
    print("""
⚠️  Execution requires explicit user confirmation.
    To execute, call: execute_recommendation(token, portfolio_id, rec_id)
    or CLI: PYTHONPATH={tools} python3 katbot_client.py execute <rec_id>
""")
    return rec_result


def main():
    parser = argparse.ArgumentParser(
        description="Signal-driven research → recommendation workflow."
    )
    parser.add_argument("--portfolio-id", type=int,
                        help="Portfolio ID (default: from katbot_config.json)")
    parser.add_argument("--signal-type",
                        choices=["momentum", "volume_breakout", "whale_activity", "trending", "manual"],
                        default="manual",
                        help="Signal type that triggered this workflow")
    parser.add_argument("--tokens", default="",
                        help="Comma-separated candidate token symbols (e.g. BTC,ETH)")
    parser.add_argument("--rationale", default="",
                        help="Rationale text from signal trigger")
    parser.add_argument("--risk-profile", choices=["low", "medium", "high"], default=None)
    parser.add_argument("--time-horizon", choices=["short", "medium", "long"], default=None)
    parser.add_argument("--no-reuse-research", dest="reuse_research",
                        action="store_false", default=True,
                        help="Always run fresh research (ignore existing results)")
    parser.add_argument("--no-enrich", dest="enrich",
                        action="store_false", default=True,
                        help="Skip market-intelligence enrichment step")
    args = parser.parse_args()

    token = get_token()

    portfolio_id = args.portfolio_id
    if not portfolio_id:
        config = get_config()
        portfolio_id = config.get("portfolio_id")
    if not portfolio_id:
        print("ERROR: --portfolio-id required or must be set in katbot_config.json")
        sys.exit(1)

    signal_tokens = [t.strip() for t in args.tokens.split(",") if t.strip()] if args.tokens else []

    run_workflow(
        token=token,
        portfolio_id=portfolio_id,
        signal_type=args.signal_type,
        signal_tokens=signal_tokens,
        rationale=args.rationale,
        risk_profile=args.risk_profile,
        time_horizon=args.time_horizon,
        reuse_research=args.reuse_research,
        enrich=args.enrich,
    )


if __name__ == "__main__":
    main()
