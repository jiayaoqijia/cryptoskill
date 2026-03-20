"""
KryptoGO Meme Trader - Reference Trading Workflow

This script demonstrates the full trading workflow:
  discover signal -> analyze token -> assess risk -> execute trade -> monitor position

Requirements:
  - Python 3.10+
  - pip install requests solders

Environment variables (stored in .env, never logged or printed):
  - KRYPTOGO_API_KEY: Your KryptoGO Agent API key
  - SOLANA_PRIVATE_KEY: Base58-encoded Solana private key
  - SOLANA_WALLET_ADDRESS: Agent wallet public address

SECURITY WARNING:
  - NEVER log, print, or expose SOLANA_PRIVATE_KEY in any output.
  - NEVER commit .env to version control.
  - Signing happens locally; the private key is never sent to any server.
"""

import json
import os
import sys
import time
import base64

import requests
from solders.keypair import Keypair
from solders.transaction import VersionedTransaction

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

API_BASE = "https://wallet-data.kryptogo.app"
API_KEY = os.environ.get("KRYPTOGO_API_KEY")
PRIVATE_KEY = os.environ.get("SOLANA_PRIVATE_KEY")  # NEVER log this value
WALLET_ADDRESS = os.environ.get("SOLANA_WALLET_ADDRESS")

if not API_KEY:
    sys.exit("ERROR: KRYPTOGO_API_KEY environment variable is not set.")
if not PRIVATE_KEY:
    sys.exit("ERROR: SOLANA_PRIVATE_KEY environment variable is not set.")
if not WALLET_ADDRESS:
    sys.exit("ERROR: SOLANA_WALLET_ADDRESS environment variable is not set.")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

SOL_MINT = "So11111111111111111111111111111112"
LAMPORTS_PER_SOL = 1_000_000_000

# ---------------------------------------------------------------------------
# User Preferences (load from memory/trading-preferences.json if available)
# ---------------------------------------------------------------------------

DEFAULT_PREFERENCES = {
    "max_position_size": 0.1,       # Max SOL per trade
    "stop_loss_pct": 30,            # Stop loss percentage
    "take_profit_pct": 100,         # Take profit percentage
    "min_market_cap": 500_000,      # Minimum market cap filter (USD)
    "scan_count": 10,               # Trending tokens per scan
    "risk_tolerance": "moderate",   # conservative / moderate / aggressive
    "chains": ["solana"],           # Chains to scan
}


def load_preferences(path="memory/trading-preferences.json"):
    """Load user trading preferences, falling back to defaults."""
    prefs = dict(DEFAULT_PREFERENCES)
    if os.path.exists(path):
        with open(path) as f:
            prefs.update(json.load(f))
    return prefs


# ---------------------------------------------------------------------------
# Trade Journal — Learning & Adaptation
# ---------------------------------------------------------------------------

JOURNAL_PATH = "memory/trading-journal.json"
LESSONS_PATH = "memory/trading-lessons.md"
REVIEWS_DIR = "memory/strategy-reviews"


def _load_journal():
    """Load trade journal from disk."""
    if os.path.exists(JOURNAL_PATH):
        with open(JOURNAL_PATH) as f:
            return json.load(f)
    return {"trades": []}


def _save_journal(journal):
    """Save trade journal to disk."""
    os.makedirs(os.path.dirname(JOURNAL_PATH), exist_ok=True)
    with open(JOURNAL_PATH, "w") as f:
        json.dump(journal, f, indent=2)


def log_trade_entry(token_mint, symbol, action, amount_sol, token_amount,
                    price, market_cap, entry_reasoning, chain_id="501"):
    """Log a new trade (BUY) to the journal. Call immediately after execution."""
    journal = _load_journal()
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    trade_id = f"{ts}_{symbol}"

    entry = {
        "id": trade_id,
        "token_mint": token_mint,
        "symbol": symbol,
        "chain_id": chain_id,
        "action": action,
        "amount_sol": amount_sol,
        "token_amount": token_amount,
        "price_at_entry": price,
        "market_cap_at_entry": market_cap,
        "timestamp": ts,
        "entry_reasoning": entry_reasoning,
        "outcome": None,
    }
    journal["trades"].append(entry)
    _save_journal(journal)
    return trade_id


def log_trade_exit(trade_id, exit_price, exit_reason, pnl_sol, pnl_pct,
                   holding_hours, cluster_ratio_at_exit, lesson):
    """Update a journal entry with exit outcome. Call when a position is closed."""
    journal = _load_journal()
    for trade in journal["trades"]:
        if trade["id"] == trade_id:
            trade["outcome"] = {
                "exit_price": exit_price,
                "exit_timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "exit_reason": exit_reason,
                "pnl_sol": pnl_sol,
                "pnl_pct": pnl_pct,
                "holding_duration_hours": holding_hours,
                "cluster_ratio_at_exit": cluster_ratio_at_exit,
                "lesson": lesson,
            }
            break
    _save_journal(journal)

    # If loss >20%, append to lessons file
    if pnl_pct < -20:
        _log_lesson(trade_id, pnl_pct, lesson, exit_reason)


def _log_lesson(trade_id, pnl_pct, lesson, loss_type):
    """Append a loss post-mortem to trading-lessons.md."""
    os.makedirs(os.path.dirname(LESSONS_PATH), exist_ok=True)
    ts = time.strftime("%Y-%m-%d", time.gmtime())
    entry = (
        f"\n## {ts} — {trade_id} (PnL: {pnl_pct:+.1f}%)\n\n"
        f"- **Type:** {loss_type}\n"
        f"- **Lesson:** {lesson}\n"
    )
    with open(LESSONS_PATH, "a") as f:
        f.write(entry)


def get_journal_stats():
    """Calculate aggregate trading statistics for strategy review."""
    journal = _load_journal()
    closed = [t for t in journal["trades"] if t.get("outcome")]

    if not closed:
        return None

    wins = [t for t in closed if t["outcome"]["pnl_pct"] > 0]
    losses = [t for t in closed if t["outcome"]["pnl_pct"] <= 0]

    avg_win = sum(t["outcome"]["pnl_pct"] for t in wins) / len(wins) if wins else 0
    avg_loss = sum(t["outcome"]["pnl_pct"] for t in losses) / len(losses) if losses else 0
    avg_hold_win = sum(t["outcome"]["holding_duration_hours"] for t in wins) / len(wins) if wins else 0
    avg_hold_loss = sum(t["outcome"]["holding_duration_hours"] for t in losses) / len(losses) if losses else 0

    # Win rate by signal source
    source_stats = {}
    for t in closed:
        src = t.get("entry_reasoning", {}).get("signal_source", "unknown")
        if src not in source_stats:
            source_stats[src] = {"wins": 0, "total": 0}
        source_stats[src]["total"] += 1
        if t["outcome"]["pnl_pct"] > 0:
            source_stats[src]["wins"] += 1

    # Loss type distribution
    loss_types = {}
    for t in losses:
        lt = t["outcome"].get("exit_reason", "unknown")
        loss_types[lt] = loss_types.get(lt, 0) + 1

    return {
        "total_trades": len(closed),
        "win_rate": len(wins) / len(closed) * 100,
        "avg_win_pct": avg_win,
        "avg_loss_pct": avg_loss,
        "avg_hold_hours_win": avg_hold_win,
        "avg_hold_hours_loss": avg_hold_loss,
        "total_pnl_sol": sum(t["outcome"]["pnl_sol"] for t in closed),
        "source_win_rates": {
            src: s["wins"] / s["total"] * 100
            for src, s in source_stats.items()
        },
        "loss_type_counts": loss_types,
        "best_trade": max(closed, key=lambda t: t["outcome"]["pnl_pct"]),
        "worst_trade": min(closed, key=lambda t: t["outcome"]["pnl_pct"]),
    }


def save_strategy_review(stats, insights, proposals):
    """Save a periodic strategy review to memory/strategy-reviews/."""
    os.makedirs(REVIEWS_DIR, exist_ok=True)
    date = time.strftime("%Y-%m-%d", time.gmtime())
    path = os.path.join(REVIEWS_DIR, f"{date}.md")

    content = f"# Strategy Review — {date}\n\n"
    content += "## Performance Summary\n\n"
    content += f"- Total trades: {stats['total_trades']}\n"
    content += f"- Win rate: {stats['win_rate']:.1f}%\n"
    content += f"- Avg win: {stats['avg_win_pct']:+.1f}% | Avg loss: {stats['avg_loss_pct']:+.1f}%\n"
    content += f"- Total PnL: {stats['total_pnl_sol']:+.4f} SOL\n"
    content += f"- Avg hold (wins): {stats['avg_hold_hours_win']:.1f}h | (losses): {stats['avg_hold_hours_loss']:.1f}h\n\n"

    content += "## Win Rate by Source\n\n"
    for src, rate in stats["source_win_rates"].items():
        content += f"- {src}: {rate:.0f}%\n"

    content += "\n## Insights\n\n"
    for insight in insights:
        content += f"- {insight}\n"

    content += "\n## Proposed Changes\n\n"
    for proposal in proposals:
        content += f"- [ ] {proposal}\n"

    content += "\n---\n*Generated by kryptogo-meme-trader agent*\n"

    with open(path, "w") as f:
        f.write(content)
    return path


PREFERENCES = load_preferences()

# ---------------------------------------------------------------------------
# Analysis helpers
# ---------------------------------------------------------------------------


def get_token_overview(token_address):
    """Get token metadata: name, price, market cap, holders, risk level."""
    resp = requests.get(
        f"{API_BASE}/token-overview",
        params={"address": token_address},
        headers=HEADERS,
    )
    resp.raise_for_status()
    return resp.json()


def analyze_token(token_mint):
    """Get full cluster analysis: clusters, top holders, address metadata."""
    resp = requests.get(f"{API_BASE}/analyze/{token_mint}", headers=HEADERS)
    resp.raise_for_status()
    return resp.json()


def get_cluster_changes(token_mint, include_top_holders=True):
    """Get cluster holding ratio and changes across time periods."""
    resp = requests.get(
        f"{API_BASE}/analyze-cluster-change/{token_mint}",
        params={"include_top_holders": str(include_top_holders).lower()},
        headers=HEADERS,
    )
    resp.raise_for_status()
    return resp.json()


def get_wallet_labels(token_mint, wallets):
    """Get behavior labels for wallets: smart_money, whale, blue_chip_profit, high_frequency."""
    resp = requests.post(
        f"{API_BASE}/wallet-labels",
        json={"token_mint": token_mint, "wallets": wallets},
        headers=HEADERS,
    )
    resp.raise_for_status()
    return resp.json()


def get_token_wallet_labels(token_mint):
    """Get token-specific labels: developer, sniper, bundle, new_wallet."""
    resp = requests.post(
        f"{API_BASE}/token-wallet-labels",
        json={"token_mint": token_mint},
        headers=HEADERS,
    )
    resp.raise_for_status()
    return resp.json()


# ---------------------------------------------------------------------------
# Risk assessment
# ---------------------------------------------------------------------------


def assess_sell_pressure(token_mint, clusters, token_labels):
    """
    Evaluate sell pressure from low-cost position holders.

    Returns risk_level: 'low', 'medium', 'high'
    """
    risky_labels = {"developer", "sniper", "bundle", "new_wallet"}
    risky_addresses = set()

    label_data = token_labels.get("data", {})
    for address, labels in label_data.items():
        for label in labels:
            if label["label_type"] in risky_labels:
                risky_addresses.add(address)

    total_risky_balance = 0
    total_cluster_balance = 0

    for cluster in clusters.get("clusters", []):
        cluster_balance = float(cluster["total_balance"])
        total_cluster_balance += cluster_balance
        for wallet in cluster["wallets"]:
            if wallet["address"] in risky_addresses:
                total_risky_balance += float(wallet["token_balance"])

    if total_cluster_balance == 0:
        return "low"

    risky_ratio = total_risky_balance / total_cluster_balance

    if risky_ratio > 0.3:
        return "high"    # >30% of cluster holdings are low-cost tokens
    elif risky_ratio > 0.1:
        return "medium"  # 10-30% -- some risk
    else:
        return "low"     # <10% -- low-cost tokens mostly cleared


# ---------------------------------------------------------------------------
# Trading helpers
# ---------------------------------------------------------------------------


def sign_transaction(unsigned_tx_b64, private_key_b58):
    """
    Sign a base64-encoded unsigned V0 transaction.

    SECURITY: private_key_b58 is used locally only -- never sent over the network.
    """
    tx_bytes = base64.b64decode(unsigned_tx_b64)
    tx = VersionedTransaction.from_bytes(tx_bytes)
    keypair = Keypair.from_base58_string(private_key_b58)
    signed_tx = VersionedTransaction(tx.message, [keypair])
    return base64.b64encode(bytes(signed_tx)).decode()


def build_swap(input_mint, output_mint, amount, slippage_bps=300):
    """Build an unsigned swap transaction via the DEX aggregator.

    Always passes wallet_address so the returned transaction uses the agent's
    wallet as fee payer / signer (required for local signing).
    """
    resp = requests.post(
        f"{API_BASE}/agent/swap",
        headers=HEADERS,
        json={
            "input_mint": input_mint,
            "output_mint": output_mint,
            "amount": amount,
            "slippage_bps": slippage_bps,
            "wallet_address": WALLET_ADDRESS,
        },
    )
    resp.raise_for_status()
    data = resp.json()

    # Verify the transaction was built for our wallet
    if data.get("fee_payer") and data["fee_payer"] != WALLET_ADDRESS:
        raise ValueError(
            f"Transaction fee_payer mismatch: expected {WALLET_ADDRESS}, "
            f"got {data['fee_payer']}. Do not sign this transaction."
        )

    return data


def submit_transaction(signed_tx_b64):
    """Submit a signed transaction to the Solana network."""
    resp = requests.post(
        f"{API_BASE}/agent/submit",
        headers=HEADERS,
        json={"signed_transaction": signed_tx_b64},
    )
    resp.raise_for_status()
    return resp.json()


def safe_execute_trade(input_mint, output_mint, amount, slippage_bps=300):
    """Execute a trade with error handling and price impact validation."""
    try:
        swap = build_swap(input_mint, output_mint, amount, slippage_bps)
    except requests.HTTPError as e:
        if e.response.status_code == 402:
            data = e.response.json()
            print(f"Quota exceeded. Limit: {data.get('daily_limit')}, Tier: {data.get('tier')}")
            return None
        if e.response.status_code == 502:
            print("External service error. Retrying in 10s...")
            time.sleep(10)
            try:
                swap = build_swap(input_mint, output_mint, amount, slippage_bps)
            except requests.HTTPError:
                print("Retry failed.")
                return None
        else:
            raise

    price_impact = float(swap["quote"]["price_impact_pct"])
    if price_impact > 10.0:
        print(f"DANGER: Price impact {price_impact}%. Aborting.")
        return None
    if price_impact > 5.0:
        print(f"WARNING: Price impact {price_impact}%. Proceeding with caution.")

    # SECURITY: private key is used locally for signing, never sent to any server
    try:
        signed_tx = sign_transaction(swap["transaction"], PRIVATE_KEY)
        return submit_transaction(signed_tx)
    except requests.HTTPError as e:
        if e.response.status_code == 502:
            print("Failed to send transaction to Solana network.")
        else:
            raise
        return None


# ---------------------------------------------------------------------------
# Portfolio
# ---------------------------------------------------------------------------


def get_portfolio(wallet_address=None):
    """
    Fetch portfolio state.

    The API key is tied to your KryptoGO account (for billing and tier).
    The agent trades with its OWN wallet (generated during setup), separate
    from the wallet you used to log into kryptogo.xyz.
    Always pass the agent's wallet address.
    """
    params = {}
    if wallet_address:
        params["wallet_address"] = wallet_address
    resp = requests.get(f"{API_BASE}/agent/portfolio", headers=HEADERS, params=params)
    resp.raise_for_status()
    return resp.json()


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------


def scan_trending_tokens(chain_id="501", sort_by="5", period="2", **filters):
    """
    Scan for trending tokens. Returns list of tokens sorted by the chosen metric.

    sort_by: 1=mcap, 2=holders, 3=liquidity, 4=txCount, 5=volume, 6=change
    period:  1=5min, 2=1h, 3=4h, 4=24h
    filters: marketCapMin, marketCapMax, holdersMin, volumeMin, tokenAgeMax, tokenAgeType, etc.
    """
    scan_count = PREFERENCES.get("scan_count", 10)
    params = {
        "chain_id": chain_id,
        "sort_by": sort_by,
        "period": period,
        "page_size": str(scan_count),
        **filters,
    }
    resp = requests.get(f"{API_BASE}/agent/trending-tokens", headers=HEADERS, params=params)
    resp.raise_for_status()
    return resp.json()["tokens"]


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------


def check_rug_risk(token_mint):
    """
    Check for rug pull risks using RugCheck.xyz API.
    Returns: (is_safe: bool, reason: str)
    """
    try:
        url = f"https://api.rugcheck.xyz/v1/tokens/{token_mint}/report/summary"
        resp = requests.get(url, timeout=2)
        
        if resp.status_code != 200:
            print(f"Warning: RugCheck API unavailable ({resp.status_code}). Proceeding with caution.")
            return True, "API_UNAVAILABLE" 

        data = resp.json()
        
        # 1. Check Risk Score
        score = data.get("score", 0)
        # 5000 is a high threshold, many legit memes are 1000-3000 initially
        if score > 5000:
            return False, f"High Risk Score: {score}"

        # 2. Check Specific Danger Risks
        risks = data.get("risks", [])
        danger_signals = []
        for r in risks:
            if r.get("level") == "danger":
                name = r.get("name", "")
                # Critical rug indicators that are instant rejects
                if "Mint Authority" in name:
                    danger_signals.append("Mint Authority Enabled")
                elif "Freeze Authority" in name:
                    danger_signals.append("Freeze Authority Enabled")
                elif "LP Unlocked" in name:
                    danger_signals.append("LP Not Locked/Burned")
                elif "Low Liquidity" in name:
                    danger_signals.append("Low Liquidity")
                elif "High ownership" in name or "Single holder" in name:
                    # KryptoGO cluster analysis handles this better, but good as a secondary check
                    pass 

        if danger_signals:
            return False, f"Rug Risks: {', '.join(danger_signals)}"
        
        return True, "Safe"
        
    except Exception as e:
        print(f"Warning: RugCheck check failed: {e}")
        return True, "CHECK_ERROR"


def analyze_and_trade(token_mint, max_position_sol=None):
    """
    Full pipeline: check balance -> analyze token -> assess risk -> execute trade.

    G4 fix: Portfolio balance check at start to ensure sufficient SOL.
    G5 fix: Private key security warnings in comments.
    G6 fix: Uses scan_count from user preferences instead of hardcoded page_size.
    G7 fix: RugCheck integration for LP security.
    """
    if max_position_sol is None:
        max_position_sol = PREFERENCES.get("max_position_size", 0.1)

    # G4: Check portfolio balance before attempting any trade
    portfolio = get_portfolio(WALLET_ADDRESS)
    sol_balance = float(portfolio.get("sol_balance", "0"))
    min_required = max_position_sol + 0.01  # position + gas buffer
    if sol_balance < min_required:
        print(f"Insufficient SOL balance: {sol_balance:.4f} SOL (need {min_required:.4f}). Skipping.")
        return None

    # Step 1: Token overview
    overview = get_token_overview(token_mint)
    mcap = float(overview.get("market_cap") or 0)
    min_mcap = PREFERENCES.get("min_market_cap", 500_000)
    if mcap < min_mcap:
        print(f"Market cap ${mcap:,.0f} below minimum ${min_mcap:,.0f}. Skipping.")
        return None

    # [NEW] Step 1.5: Quick Rug Check (Fail Fast)
    is_safe, risk_reason = check_rug_risk(token_mint)
    if not is_safe:
        print(f"RUG CHECK FAILED: {risk_reason}. Skipping.")
        return None
    print(f"Rug Check Passed: {risk_reason}")

    # Step 2: Cluster analysis
    cluster_changes = get_cluster_changes(token_mint)
    cluster_ratio = cluster_changes["cluster_ratio"]
    change_1d = cluster_changes["changes"].get("1d", 0)
    change_7d = cluster_changes["changes"].get("7d", 0)

    print(f"Cluster ratio: {cluster_ratio:.1%}, 1d change: {change_1d:+.2%}, 7d change: {change_7d:+.2%}")

    if cluster_ratio < 0.20:
        print("Cluster ratio too low (<20%). No clear major holder.")
        return None

    # Step 2b: Scam detection -- check if any single cluster holds >50%
    clusters = analyze_token(token_mint)
    total_supply = float(overview.get("total_supply") or overview.get("circulating_supply") or 0)
    if total_supply > 0:
        for cluster in clusters.get("clusters", []):
            cluster_pct = float(cluster["total_balance"]) / total_supply
            if cluster_pct > 0.50:
                print(f"SCAM WARNING: Single cluster holds {cluster_pct:.0%} of supply. Skipping.")
                return None

    if change_1d < 0 and change_7d < 0:
        print("Clusters are distributing (negative 1d and 7d changes). Avoid.")
        return None

    # Step 3: Get token-specific labels
    token_labels = get_token_wallet_labels(token_mint)

    # Step 4: Risk assessment
    risk = assess_sell_pressure(token_mint, clusters, token_labels)
    if risk == "high":
        print("HIGH RISK: Developer/sniper/bundle holders still active. Skipping.")
        return None

    # Step 5: Get wallet labels for top cluster addresses
    top_cluster_wallets = []
    for cluster in clusters.get("clusters", [])[:5]:
        for w in cluster["wallets"]:
            top_cluster_wallets.append(w["address"])

    if top_cluster_wallets:
        labels = get_wallet_labels(token_mint, top_cluster_wallets[:50])
        smart_money_count = sum(
            1 for addr_labels in labels.get("data", {}).values()
            for lbl in addr_labels if lbl["label_type"] == "smart_money"
        )
        print(f"Smart money wallets in top clusters: {smart_money_count}")

    # Step 6: All checks passed -- execute trade
    symbol = overview.get("symbol", token_mint[:8])
    print(f"\nAnalysis passed. Buying {symbol} with {max_position_sol} SOL")

    amount_lamports = int(max_position_sol * LAMPORTS_PER_SOL)
    # SECURITY: sign_transaction uses PRIVATE_KEY locally; it is never sent to the server
    result = safe_execute_trade(SOL_MINT, token_mint, amount_lamports, slippage_bps=300)

    if result:
        print(f"Trade executed: {result['explorer_url']}")

        # Log trade to journal for learning
        trade_id = log_trade_entry(
            token_mint=token_mint,
            symbol=symbol,
            action="BUY",
            amount_sol=max_position_sol,
            token_amount=0,  # fill from result if available
            price=float(overview.get("price", 0)),
            market_cap=mcap,
            entry_reasoning={
                "cluster_ratio": cluster_ratio,
                "cluster_change_1d": change_1d,
                "cluster_change_7d": change_7d,
                "smart_money_count": smart_money_count if 'smart_money_count' in dir() else 0,
                "dev_exited": True,  # passed risk check
                "sniper_cleared": True,  # passed risk check
                "signal_source": "trending_tokens",  # or "signal_dashboard"
                "risk_level": risk,
            },
        )
        result["trade_id"] = trade_id
        print(f"Trade logged to journal: {trade_id}")

    return result


def check_account_tier():
    """Check agent account tier."""
    try:
        resp = requests.get(f"{API_BASE}/agent/account", headers=HEADERS, timeout=5)
        if resp.status_code == 200:
            return resp.json().get("tier", "free").lower()
    except Exception:
        pass
    return "free"


def scan_signal_dashboard(chain_id="501"):
    """Scan signal dashboard for Pro/Alpha users."""
    scan_count = PREFERENCES.get("scan_count", 10)
    params = {
        "chain_id": chain_id,
        "sort_by": "signal_count",
        "page_size": str(scan_count)
    }
    try:
        resp = requests.get(f"{API_BASE}/signal-dashboard", headers=HEADERS, params=params)
        resp.raise_for_status()
        # Adapt response to match trending tokens structure if needed
        data = resp.json()
        if isinstance(data, list):
            return data
        return data.get("tokens", []) or data.get("signals", [])
    except Exception as e:
        print(f"Warning: Signal Dashboard scan failed: {e}")
        return []


def discover_and_analyze():
    """Scan tokens (Signals for Pro+, Trending for Free) and trade."""
    max_position_sol = PREFERENCES.get("max_position_size", 0.1)
    min_mcap = PREFERENCES.get("min_market_cap", 500_000)

    tier = check_account_tier()
    print(f"Account Tier: {tier.upper()}")

    tokens = []
    if tier in ["pro", "alpha"]:
        print("Scanning Signal Dashboard (Pro/Alpha exclusive)...")
        tokens = scan_signal_dashboard()
        if not tokens:
            print("No signals found. Falling back to Trending Tokens.")
            tokens = scan_trending_tokens(
                marketCapMin=str(int(min_mcap / 5)),
                marketCapMax="5000000",
                holdersMin="50",
                volumeMin="10000",
                tokenAgeMax="7",
                tokenAgeType="3",
            )
    else:
        print("Scanning Trending Tokens...")
        tokens = scan_trending_tokens(
            marketCapMin=str(int(min_mcap / 5)),
            marketCapMax="5000000",
            holdersMin="50",
            volumeMin="10000",
            tokenAgeMax="7",
            tokenAgeType="3",
        )

    for token in tokens:
        # Normalized field access (signals might have different keys)
        mint = token.get("tokenContractAddress") or token.get("address") or token.get("mint") or token.get("contract_address") or token.get("token_address")
        chain_id = str(token.get("chain_id") or token.get("chainId") or "501")
        symbol = token.get("tokenSymbol") or token.get("symbol")
        mcap = float(token.get("marketCap") or token.get("market_cap") or 0)
        volume = float(token.get("volume") or token.get("volume_24h") or 0)
        change = float(token.get("change") or token.get("price_change_24h") or 0)

        print(f"Scanning {symbol}: mcap=${mcap:,.0f}, vol=${volume:,.0f}, change={change:+.1f}% (mint: {mint}, chain: {chain_id})")

        if not mint:
            print("Skipping token with missing mint address.")
            continue
        
        # Skip non-Solana tokens for trading (swap.py only supports Solana)
        if chain_id != "501":
            print(f"Skipping non-Solana token on chain {chain_id}")
            continue

        if change < 0:
            continue  # Skip tokens with negative momentum

        result = analyze_and_trade(mint, max_position_sol)
        if result:
            return result  # Stop after first successful trade

    print("No tokens passed all criteria.")
    return None


def monitor_positions():
    """Check all positions and flag candidates for selling."""
    portfolio = get_portfolio(WALLET_ADDRESS)
    actions = []
    stop_loss_pct = PREFERENCES.get("stop_loss_pct", 30)
    take_profit_pct = PREFERENCES.get("take_profit_pct", 100)

    for token in portfolio.get("tokens", []):
        mint = token["mint"]
        symbol = token["symbol"]
        unrealized_pnl = float(token.get("unrealized_pnl", "0"))
        avg_cost = float(token.get("holding_avg_cost", "0"))
        balance = float(token.get("balance", "0"))
        cost_basis = avg_cost * balance
        holding_hours = int(float(token.get("avg_holding_seconds", "0"))) / 3600

        # Check cluster changes for held tokens
        try:
            changes = get_cluster_changes(mint)
            change_4h = changes["changes"].get("4h", 0)
        except Exception:
            change_4h = 0

        # Stop loss
        if cost_basis > 0 and (unrealized_pnl / cost_basis * 100) < -stop_loss_pct:
            actions.append({"mint": mint, "symbol": symbol, "action": "SELL", "reason": "stop_loss"})

        # Distribution detected
        elif change_4h < -0.05:
            actions.append({"mint": mint, "symbol": symbol, "action": "REDUCE", "reason": "distribution_detected"})

        # Stale position
        elif holding_hours > 24 and unrealized_pnl < 0.01:
            actions.append({"mint": mint, "symbol": symbol, "action": "REVIEW", "reason": "stale_position"})

        # Take profit
        elif cost_basis > 0 and (unrealized_pnl / cost_basis * 100) > take_profit_pct:
            actions.append({"mint": mint, "symbol": symbol, "action": "TAKE_PROFIT", "reason": f"{take_profit_pct}%_gain"})

    return actions


def execute_exit(mint, symbol, action, reason, pnl_pct, pnl_sol, holding_hours):
    """Execute a sell and log the outcome to the journal."""
    # Find the matching open trade in journal
    journal = _load_journal()
    trade_id = None
    for trade in reversed(journal["trades"]):
        if trade["token_mint"] == mint and trade["outcome"] is None:
            trade_id = trade["id"]
            break

    # Execute the sell
    portfolio = get_portfolio(WALLET_ADDRESS)
    token_balance = 0
    for token in portfolio.get("tokens", []):
        if token["mint"] == mint:
            # Use raw_balance if available, otherwise fetch decimals to convert UI balance
            if "raw_balance" in token:
                 token_balance = int(token["raw_balance"])
            else:
                # Fetch decimals to convert UI balance to raw units
                overview = get_token_overview(mint)
                decimals = overview.get("decimals")
                if decimals is None:
                    print(f"ABORT: Could not determine decimals for {symbol}. Refusing to sell with unknown precision.")
                    return None
                ui_balance = float(token.get("balance", 0))
                token_balance = int(ui_balance * (10 ** decimals))
            break

    if token_balance > 0:
        result = safe_execute_trade(mint, SOL_MINT, token_balance, slippage_bps=500)
        if result and trade_id:
            # Get current cluster state for the exit record
            try:
                changes = get_cluster_changes(mint)
                cluster_at_exit = changes["cluster_ratio"]
            except Exception:
                cluster_at_exit = 0

            log_trade_exit(
                trade_id=trade_id,
                exit_price=0,  # agent should fill from actual result
                exit_reason=reason,
                pnl_sol=pnl_sol,
                pnl_pct=pnl_pct,
                holding_hours=holding_hours,
                cluster_ratio_at_exit=cluster_at_exit,
                lesson="",  # agent fills this after reflection
            )
            print(f"Exit logged: {trade_id} — {reason} ({pnl_pct:+.1f}%)")
        return result
    return None


# ---------------------------------------------------------------------------
# Entry point (for manual testing)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=== KryptoGO Meme Trader - Reference Workflow ===\n")
    print(f"Agent wallet: {WALLET_ADDRESS}")
    print(f"Preferences: {json.dumps(PREFERENCES, indent=2)}\n")

    # Check portfolio first
    portfolio = get_portfolio(WALLET_ADDRESS)
    print(f"SOL balance: {portfolio.get('sol_balance', '?')} SOL")
    print(f"Open positions: {len(portfolio.get('tokens', []))}\n")

    # Run discovery
    discover_and_analyze()
