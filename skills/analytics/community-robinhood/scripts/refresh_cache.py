#!/usr/bin/env python3
"""
Robinhood Portfolio Cache Refresh Script

Reads Robinhood data via MCP tools or robin_stocks directly, then writes:
  1. Local JSON cache (default: ~/.hermes/data/robinhood/portfolio_cache.json)
  2. Optional: Dated markdown snapshot in Obsidian vault
  3. Optional: latest.md with computed deltas vs previous snapshot

Usage:
  python3 refresh_cache.py [--force] [--json-only] [--cache-dir DIR] [--vault-path DIR]

The script can run standalone with robin_stocks OR be called by an agent
after fetching data via MCP tools (use refresh_from_mcp_data()).

Environment Variables:
  ROBINHOOD_USERNAME  - Required for direct robin_stocks login
  ROBINHOOD_PASSWORD  - Required for direct robin_stocks login
  ROBINHOOD_TOTP_SECRET  - Optional, for authenticator app 2FA
  ROBINHOOD_CACHE_DIR    - Override default cache directory
  ROBINHOOD_VAULT_PATH   - Override default Obsidian vault path
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Default paths (overridable via CLI args or env vars)
# ---------------------------------------------------------------------------

DEFAULT_CACHE_DIR = Path(os.environ.get(
    "ROBINHOOD_CACHE_DIR",
    str(Path.home() / ".hermes" / "data" / "robinhood"),
))
DEFAULT_VAULT_PATH = Path(os.environ.get(
    "ROBINHOOD_VAULT_PATH",
    str(Path.home() / "Library" / "Mobile Documents" / "iCloud~md~obsidian" / "Documents" / "hermes-vault"),
))

CACHE_FILE = None  # Set in main() after parsing args
VAULT_PATH = None

# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------


def ensure_cache_dir(cache_dir: Path):
    cache_dir.mkdir(parents=True, exist_ok=True)


def load_existing_cache(cache_file: Path):
    if cache_file.exists():
        with open(cache_file) as f:
            return json.load(f)
    return None


def save_cache(data: dict, cache_file: Path, cache_dir: Path):
    ensure_cache_dir(cache_dir)
    data["last_updated"] = datetime.now(timezone.utc).isoformat()
    with open(cache_file, "w") as f:
        json.dump(data, f, indent=2, default=str)
    print(f"Cache saved to {cache_file}")
    print(f"Last updated: {data['last_updated']}")


def is_cache_stale(cache_file: Path, max_age_minutes: int = 15):
    """Check if cache is older than max_age_minutes."""
    cache = load_existing_cache(cache_file)
    if not cache or "last_updated" not in cache:
        return True
    last = datetime.fromisoformat(cache["last_updated"])
    now = datetime.now(timezone.utc)
    age = (now - last).total_seconds() / 60
    return age > max_age_minutes


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------


def _fmt_currency(value):
    if value is None:
        return "N/A"
    return f"${value:,.2f}"


def _fmt_pct(value):
    if value is None:
        return "N/A"
    return f"{value:+.2f}%"


# ---------------------------------------------------------------------------
# Obsidian vault integration (optional)
# ---------------------------------------------------------------------------


def _find_previous_snapshot(snapshots_dir: Path):
    if not snapshots_dir.exists():
        return None
    snapshots = sorted(snapshots_dir.glob("*.md"))
    return snapshots[-1] if snapshots else None


def _parse_snapshot_file(path: Path):
    with open(path) as f:
        content = f.read()
    if "```json" in content:
        json_block = content.split("```json")[1].split("```")[0].strip()
        return json.loads(json_block)
    return None


def compute_deltas(current: dict, previous: dict):
    """Compute differences between current and previous portfolio state."""
    deltas = {
        "new_positions": [],
        "closed_positions": [],
        "price_changes": [],
        "allocation_changes": [],
        "equity_change": 0,
        "equity_change_pct": 0,
    }

    if not previous:
        return deltas

    # Equity delta
    curr_equity = current.get("portfolio", {}).get("total_equity", 0)
    prev_equity = previous.get("portfolio", {}).get("total_equity", 0)
    if prev_equity:
        deltas["equity_change"] = round(curr_equity - prev_equity, 2)
        deltas["equity_change_pct"] = round((curr_equity - prev_equity) / prev_equity * 100, 2)

    curr_positions = {p["symbol"]: p for p in current.get("positions", [])}
    prev_positions = {p["symbol"]: p for p in previous.get("positions", [])}

    # New positions
    for sym, pos in curr_positions.items():
        if sym not in prev_positions:
            deltas["new_positions"].append(pos)

    # Closed positions
    for sym, pos in prev_positions.items():
        if sym not in curr_positions:
            deltas["closed_positions"].append(pos)

    # Price & allocation changes for existing positions
    for sym, curr in curr_positions.items():
        if sym in prev_positions:
            prev = prev_positions[sym]
            price_delta = curr["current_price"] - prev["current_price"]
            price_delta_pct = (price_delta / prev["current_price"] * 100) if prev["current_price"] else 0
            alloc_delta = curr.get("percentage", 0) - prev.get("percentage", 0)

            if abs(price_delta_pct) >= 5 or abs(alloc_delta) >= 1:
                deltas["price_changes"].append({
                    "symbol": sym,
                    "old_price": prev["current_price"],
                    "new_price": curr["current_price"],
                    "price_delta": round(price_delta, 2),
                    "price_delta_pct": round(price_delta_pct, 2),
                    "old_alloc": prev.get("percentage", 0),
                    "new_alloc": curr.get("percentage", 0),
                    "alloc_delta": round(alloc_delta, 2),
                })

    return deltas


def write_obsidian_snapshot(data: dict, vault_path: Path):
    """Write portfolio snapshot to Obsidian vault."""
    ephemeral_dir = vault_path / "_ephemeral" / "portfolio"
    snapshots_dir = ephemeral_dir / "snapshots"
    latest_file = ephemeral_dir / "latest.md"

    snapshots_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now(timezone.utc)
    now_local = datetime.now()
    timestamp = now_local.strftime("%Y-%m-%d-%H%M")
    date_str = now_local.strftime("%Y-%m-%d")
    time_str = now_local.strftime("%H:%M")

    portfolio = data.get("portfolio", {})
    positions = data.get("positions", [])
    options = data.get("options", [])
    dividends = data.get("dividends_ytd", [])

    # Find previous snapshot for deltas
    prev_snapshot_path = _find_previous_snapshot(snapshots_dir)
    previous = _parse_snapshot_file(prev_snapshot_path) if prev_snapshot_path else None
    deltas = compute_deltas(data, previous)

    # --- Dated Snapshot ---
    snapshot_file = snapshots_dir / f"{timestamp}.md"

    pos_rows = []
    for p in positions:
        pos_rows.append(
            f"| {p['symbol']} | {p.get('name', '')} | {p['quantity']} | {_fmt_currency(p['avg_cost'])} | "
            f"{_fmt_currency(p['current_price'])} | {_fmt_currency(p['market_value'])} | "
            f"{_fmt_currency(p['total_return'])} | {_fmt_pct(p['total_return_pct'])} | {p.get('percentage', 'N/A')}% |"
        )
    positions_table = "\n".join(pos_rows) if pos_rows else "| — | No open positions | — | — | — | — | — | — | — |"

    opt_rows = []
    for o in options:
        opt_rows.append(
            f"| {o['symbol']} | {o['type']} | {o.get('strike', 'N/A')} | {o.get('expiration', 'N/A')} | "
            f"{o['quantity']} | {_fmt_currency(o['avg_cost'])} | {_fmt_currency(o.get('market_value', 'N/A'))} |"
        )
    options_table = "\n".join(opt_rows) if opt_rows else "| — | No open options | — | — | — | — | — |"

    div_rows = []
    for d in dividends:
        div_rows.append(f"| {d['symbol']} | {_fmt_currency(d['amount'])} | {d.get('pay_date', 'N/A')} |")
    dividends_table = "\n".join(div_rows) if div_rows else "| — | No dividends YTD | — |"

    snapshot_content = f"""---
snapshot_time: {now.isoformat()}
date: {date_str}
time: {time_str}
total_equity: {portfolio.get('total_equity', 0)}
day_change: {portfolio.get('day_change', 0)}
day_change_pct: {portfolio.get('day_change_pct', 0)}
buying_power: {portfolio.get('buying_power', 0)}
positions_count: {len(positions)}
options_count: {len(options)}
dividends_ytd: {sum(d['amount'] for d in dividends):.2f}
type: portfolio-snapshot
---

# Portfolio Snapshot — {date_str} {time_str}

## Summary

| Metric | Value |
|--------|-------|
| Total Equity | {_fmt_currency(portfolio.get('total_equity'))} |
| Day Change | {_fmt_currency(portfolio.get('day_change'))} ({_fmt_pct(portfolio.get('day_change_pct'))}) |
| Buying Power | {_fmt_currency(portfolio.get('buying_power'))} |
| Previous Close | {_fmt_currency(portfolio.get('previous_close'))} |
| Positions | {len(positions)} |
| Options | {len(options)} |
| Dividends YTD | {_fmt_currency(sum(d['amount'] for d in dividends))} |

## Positions

| Symbol | Name | Qty | Avg Cost | Current | Market Value | Total Return | Return % | Allocation |
|--------|------|-----|----------|---------|--------------|--------------|----------|------------|
{positions_table}

## Options

| Symbol | Type | Strike | Expiration | Qty | Avg Cost | Market Value |
|--------|------|--------|------------|-----|----------|--------------|
{options_table}

## Dividends YTD

| Symbol | Amount | Pay Date |
|--------|--------|----------|
{dividends_table}

## Raw Data

```json
{json.dumps(data, indent=2, default=str)}
```
"""

    with open(snapshot_file, "w") as f:
        f.write(snapshot_content)
    print(f"Snapshot saved to {snapshot_file}")

    # --- latest.md with Deltas ---
    delta_sections = []

    if deltas["equity_change"] != 0:
        delta_sections.append(
            f"- **Equity Change:** {_fmt_currency(deltas['equity_change'])} ({_fmt_pct(deltas['equity_change_pct'])}) since last snapshot"
        )

    if deltas["new_positions"]:
        delta_sections.append("### 🆕 New Positions")
        for p in deltas["new_positions"]:
            delta_sections.append(f"- **{p['symbol']}** — {p['quantity']} shares @ {_fmt_currency(p['avg_cost'])}")

    if deltas["closed_positions"]:
        delta_sections.append("### ❌ Closed Positions")
        for p in deltas["closed_positions"]:
            delta_sections.append(
                f"- **{p['symbol']}** — realized P&L: {_fmt_currency(p['total_return'])} ({_fmt_pct(p['total_return_pct'])})"
            )

    if deltas["price_changes"]:
        delta_sections.append("### 📊 Significant Moves (>5% or >1% allocation shift)")
        for c in deltas["price_changes"]:
            delta_sections.append(
                f"- **{c['symbol']}**: {_fmt_currency(c['old_price'])} → {_fmt_currency(c['new_price'])} "
                f"({_fmt_pct(c['price_delta_pct'])}) | Allocation: {c['old_alloc']}% → {c['new_alloc']}%"
            )

    if not any([deltas["new_positions"], deltas["closed_positions"], deltas["price_changes"], deltas["equity_change"]]):
        delta_sections.append("- _No significant changes since last snapshot._")

    delta_content = "\n\n".join(delta_sections)

    latest_content = f"""---
snapshot_time: {now.isoformat()}
date: {date_str}
time: {time_str}
total_equity: {portfolio.get('total_equity', 0)}
day_change: {portfolio.get('day_change', 0)}
day_change_pct: {portfolio.get('day_change_pct', 0)}
buying_power: {portfolio.get('buying_power', 0)}
positions_count: {len(positions)}
options_count: {len(options)}
dividends_ytd: {sum(d['amount'] for d in dividends):.2f}
type: portfolio-snapshot
---

# Latest Portfolio — {date_str} {time_str}

> This file is **overwritten** on every portfolio pull. For historical records, see `snapshots/`.
> Last snapshot: `{timestamp}.md`

## Summary

| Metric | Value |
|--------|-------|
| Total Equity | {_fmt_currency(portfolio.get('total_equity'))} |
| Day Change | {_fmt_currency(portfolio.get('day_change'))} ({_fmt_pct(portfolio.get('day_change_pct'))}) |
| Buying Power | {_fmt_currency(portfolio.get('buying_power'))} |
| Previous Close | {_fmt_currency(portfolio.get('previous_close'))} |
| Positions | {len(positions)} |
| Options | {len(options)} |
| Dividends YTD | {_fmt_currency(sum(d['amount'] for d in dividends))} |

## Changes Since Last Snapshot

{delta_content}

## Positions

| Symbol | Name | Qty | Avg Cost | Current | Market Value | Total Return | Return % | Allocation |
|--------|------|-----|----------|---------|--------------|--------------|----------|------------|
{positions_table}

## Options

| Symbol | Type | Strike | Expiration | Qty | Avg Cost | Market Value |
|--------|------|--------|------------|-----|----------|--------------|
{options_table}

## Dividends YTD

| Symbol | Amount | Pay Date |
|--------|--------|----------|
{dividends_table}
"""

    with open(latest_file, "w") as f:
        f.write(latest_content)
    print(f"Latest portfolio updated at {latest_file}")


# ---------------------------------------------------------------------------
# Direct robin_stocks refresh (no MCP needed)
# ---------------------------------------------------------------------------


def refresh_via_robin_stocks(cache_file: Path, cache_dir: Path, vault_path: Path = None):
    """
    Direct refresh using robin_stocks (no MCP needed).
    Requires: pip install robin_stocks pyotp
    Env vars: ROBINHOOD_USERNAME, ROBINHOOD_PASSWORD, ROBINHOOD_TOTP_SECRET (optional)
    """
    try:
        import robin_stocks.robinhood as rh
    except ImportError:
        print("ERROR: robin_stocks not installed. Run: pip install robin_stocks")
        sys.exit(1)

    username = os.environ.get("ROBINHOOD_USERNAME")
    password = os.environ.get("ROBINHOOD_PASSWORD")
    totp_secret = os.environ.get("ROBINHOOD_TOTP_SECRET")

    if not username or not password:
        print("ERROR: Set ROBINHOOD_USERNAME and ROBINHOOD_PASSWORD env vars")
        sys.exit(1)

    # Login
    if totp_secret:
        import pyotp
        totp = pyotp.TOTP(totp_secret)
        mfa = totp.now()
        rh.login(username, password, mfa_code=mfa)
    else:
        rh.login(username, password)

    # Portfolio overview
    profile = rh.load_portfolio_profile()
    account = rh.load_account_profile()
    portfolio = {
        "total_equity": float(profile.get("equity", 0)),
        "buying_power": float(account.get("buying_power", 0)),
        "day_change": float(profile.get("equity_change", 0)),
        "day_change_pct": float(profile.get("equity_change_pct", 0)),
    }

    # Positions
    positions = []
    raw_positions = rh.get_open_stock_positions()
    for pos in raw_positions:
        symbol = pos.get("symbol") or _get_symbol_from_instrument(rh, pos.get("instrument", ""))
        qty = float(pos.get("quantity", 0))
        avg_cost = float(pos.get("average_buy_price", 0))
        if qty > 0:
            quote = rh.get_latest_price(symbol)
            current_price = float(quote[0]) if quote and quote[0] else 0
            market_value = qty * current_price
            total_return = market_value - (qty * avg_cost)
            total_return_pct = (total_return / (qty * avg_cost) * 100) if avg_cost > 0 else 0
            positions.append({
                "symbol": symbol,
                "quantity": qty,
                "avg_cost": avg_cost,
                "current_price": current_price,
                "market_value": round(market_value, 2),
                "total_return": round(total_return, 2),
                "total_return_pct": round(total_return_pct, 2),
            })

    # Options positions
    options = []
    raw_options = rh.get_open_option_positions()
    for opt in raw_options:
        chain = rh.get_option_instrument_data_by_id(opt.get("option_id", ""))
        options.append({
            "symbol": opt.get("chain_symbol", ""),
            "type": chain.get("type", ""),
            "strike": float(chain.get("strike_price", 0)),
            "expiration": chain.get("expiration_date", ""),
            "quantity": abs(float(opt.get("quantity", 0))),
            "avg_cost": float(opt.get("average_price", 0)),
            "current_price": float(opt.get("market_value", 0)) / abs(float(opt.get("quantity", 1))),
            "market_value": float(opt.get("market_value", 0)),
        })

    # Watchlist
    watchlist_items = rh.get_all_watchlists()
    watchlist = []
    for wl in watchlist_items.get("results", []):
        items = rh.get_watchlist_by_name(wl.get("display_name", ""))
        for item in items.get("results", []):
            sym = item.get("symbol")
            if sym:
                watchlist.append(sym)
    watchlist = list(set(watchlist))

    # Dividends YTD
    dividends = []
    raw_divs = rh.get_dividends()
    current_year = str(datetime.now().year)
    for div in raw_divs.get("results", []):
        pay_date = div.get("pay_date", "")
        if pay_date and current_year in pay_date:
            dividends.append({
                "symbol": _get_symbol_from_instrument(rh, div.get("instrument", "")),
                "amount": float(div.get("amount", 0)),
                "pay_date": pay_date,
            })

    cache = {
        "portfolio": portfolio,
        "positions": positions,
        "options": options,
        "watchlist": watchlist,
        "dividends_ytd": dividends,
    }

    rh.logout()
    save_cache(cache, cache_file, cache_dir)

    if vault_path:
        write_obsidian_snapshot(cache, vault_path)
    else:
        print("(Obsidian vault not configured — skipping snapshot write)")

    return cache


def _get_symbol_from_instrument(rh, url):
    """Extract symbol from Robinhood instrument URL."""
    if not url:
        return ""
    try:
        data = rh.request_get(url)
        return data.get("symbol", "")
    except Exception:
        return ""


# ---------------------------------------------------------------------------
# Agent-driven refresh (MCP data)
# ---------------------------------------------------------------------------


def refresh_from_mcp_data(data: dict, cache_file: Path, cache_dir: Path, vault_path: Path = None):
    """
    Write cache from MCP tool results AND optionally update Obsidian snapshots.
    Called by the agent after fetching data from MCP tools.

    Args:
        data: dict with keys: portfolio, positions, options, watchlist, dividends_ytd
        cache_file: Path to the cache JSON file
        cache_dir: Path to the cache directory
        vault_path: Path to Obsidian vault (None to skip)
    """
    save_cache(data, cache_file, cache_dir)

    if vault_path:
        write_obsidian_snapshot(data, vault_path)
    else:
        print("(Obsidian vault not configured — skipping snapshot write)")

    print("Portfolio cache updated.")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main():
    global CACHE_FILE, VAULT_PATH

    parser = argparse.ArgumentParser(description="Robinhood Portfolio Cache Refresh")
    parser.add_argument("--force", action="store_true", help="Force refresh even if cache is fresh")
    parser.add_argument("--json-only", action="store_true", help="Only output JSON, skip Obsidian vault writes")
    parser.add_argument("--cache-dir", default=str(DEFAULT_CACHE_DIR), help="Cache directory path")
    parser.add_argument("--vault-path", default=None, help="Obsidian vault path (enables snapshot writing)")
    parser.add_argument("--no-vault", action="store_true", help="Explicitly skip Obsidian vault writing")

    args = parser.parse_args()

    cache_dir = Path(args.cache_dir)
    cache_file = cache_dir / "portfolio_cache.json"
    ensure_cache_dir(cache_dir)

    vault_path = None
    if not args.json_only and not args.no_vault:
        if args.vault_path:
            vault_path = Path(args.vault_path)
        else:
            # Try default vault path
            default_vault = DEFAULT_VAULT_PATH
            if default_vault.exists():
                vault_path = default_vault
                print(f"Auto-detected Obsidian vault at {vault_path}")
            else:
                print("No Obsidian vault detected. Use --vault-path to specify one, or --json-only to skip.")

    if args.force or is_cache_stale(cache_file):
        print("Refreshing Robinhood cache...")
        try:
            refresh_via_robin_stocks(cache_file, cache_dir, vault_path)
        except Exception as e:
            print(f"ERROR refreshing cache: {e}")
            sys.exit(1)
    else:
        print("Cache is fresh (less than 15 min old). Use --force to refresh anyway.")
        cache = load_existing_cache(cache_file)
        if cache:
            print(f"Last updated: {cache.get('last_updated', 'unknown')}")


if __name__ == "__main__":
    main()