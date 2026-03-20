#!/usr/bin/env bash
# crypto-whale-tracker — Track large cryptocurrency transfers
# Usage: bash whale_tracker.sh [OPTIONS]
# Requires: python3 (3.6+), curl

set -euo pipefail

# Default values
COIN="BTC"
THRESHOLD=100
HOURS=12
FORMAT="text"
OUTPUT=""
WALLET=""
CHAIN=""
API_KEY=""
LABEL="true"
TOP=20

usage() {
    cat << 'USAGE'
Usage: whale_tracker.sh [OPTIONS]

Options:
  --coin COIN          Cryptocurrency to track (default: BTC)
  --threshold NUM      Minimum transfer amount (default: 100)
  --hours NUM          Lookback period in hours (default: 12)
  --format FMT         Output format: text, json, html, csv (default: text)
  --output FILE        Output file (default: stdout)
  --wallet ADDR        Track specific wallet address
  --chain CHAIN        Blockchain (bitcoin, ethereum, bsc, tron, solana)
  --api-key KEY        Whale Alert API key (optional, increases rate limit)
  --label BOOL         Label known exchange wallets (default: true)
  --top NUM            Max transactions to show (default: 20)
  -h, --help           Show this help

Examples:
  whale_tracker.sh --coin BTC --threshold 100
  whale_tracker.sh --coin ETH --threshold 500 --hours 24 --format html --output report.html
  whale_tracker.sh --wallet 0xABC... --chain ethereum
USAGE
    exit 0
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --coin) COIN="$2"; shift 2 ;;
        --threshold) THRESHOLD="$2"; shift 2 ;;
        --hours) HOURS="$2"; shift 2 ;;
        --format) FORMAT="$2"; shift 2 ;;
        --output) OUTPUT="$2"; shift 2 ;;
        --wallet) WALLET="$2"; shift 2 ;;
        --chain) CHAIN="$2"; shift 2 ;;
        --api-key) API_KEY="$2"; shift 2 ;;
        --label) LABEL="$2"; shift 2 ;;
        --top) TOP="$2"; shift 2 ;;
        -h|--help) usage ;;
        *) echo "Unknown option: $1"; usage ;;
    esac
done

# Auto-detect chain from coin if not specified
if [[ -z "$CHAIN" ]]; then
    case "$COIN" in
        BTC) CHAIN="bitcoin" ;;
        ETH) CHAIN="ethereum" ;;
        BNB) CHAIN="bsc" ;;
        TRX) CHAIN="tron" ;;
        SOL) CHAIN="solana" ;;
        USDT|USDC) CHAIN="ethereum" ;;
        *) CHAIN="ethereum" ;;
    esac
fi

# Check dependencies
command -v python3 >/dev/null 2>&1 || { echo "Error: python3 is required"; exit 1; }
command -v curl >/dev/null 2>&1 || { echo "Error: curl is required"; exit 1; }

# Create temp directory for data
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

# Run the main Python logic
python3 << 'PYEOF'
import sys
import json
import os
import time
import datetime
import subprocess
import re

# Read configuration from environment / arguments
COIN = os.environ.get("COIN", "BTC")
THRESHOLD = float(os.environ.get("THRESHOLD", "100"))
HOURS = int(os.environ.get("HOURS", "12"))
FORMAT = os.environ.get("FORMAT", "text")
OUTPUT = os.environ.get("OUTPUT", "")
WALLET = os.environ.get("WALLET", "")
CHAIN = os.environ.get("CHAIN", "bitcoin")
API_KEY = os.environ.get("API_KEY", "")
LABEL = os.environ.get("LABEL", "true").lower() == "true"
TOP = int(os.environ.get("TOP", "20"))
TMPDIR = os.environ.get("TMPDIR", "/tmp")

# Known exchange wallets database
KNOWN_EXCHANGES = {
    # Bitcoin addresses (shortened for matching)
    "1NDyJtNTjmwk5xPNhjgAMu4HDHigtobu1": "Binance",
    "3M219KR5vEneNb47ewrPfWyb5jQ2DjxRP6": "Binance Cold",
    "bc1qm34lsc65zpw79lxes69zkqmk6ee3ewf0j77s3h": "Binance",
    "1P5ZEDWTKTFGxQjZphgWPQUpe554WKDfHQ": "Bitfinex",
    "3JZq4atUahhuA9rLhXLMhhTo133J9rF97j": "Bitfinex",
    "1Kr6QSydW9bFQG1mXiPNNu6WpJGmUa9i1g": "Bitfinex",
    "3Cbq7aT1tY8kMxWLbitaG7yT6bPbKChq64": "Coinbase",
    "3Nxwenay9Z8Lc9JBiywExpnEFiLp6Afp8v": "Coinbase",
    "1FzWLkAahHooV3kzTgyx6qsXoRDrBsrACw": "Kraken",
    "bc1q3lyh2jh0gua6mvppyfqyh04qzah20kn3t59e97": "Kraken",
    # Ethereum addresses
    "0x28c6c06298d514db089934071355e5743bf21d60": "Binance Hot",
    "0x21a31ee1afc51d94c2efccaa2092ad1028285549": "Binance",
    "0xdfd5293d8e347dfe59e90efd55b2956a1343963d": "Binance",
    "0x56eddb7aa87536c09ccc2793473599fd21a8b17f": "Binance",
    "0xf977814e90da44bfa03b6295a0616a897441acec": "Binance Cold",
    "0x503828976d22510aad0201ac7ec88293211d23da": "Coinbase",
    "0xddfabcdc4d8ffc6d5beaf154f18b778f892a0740": "Coinbase",
    "0x3cd751e6b0078be393132286c442345e68ff0aaa": "Coinbase",
    "0xdc76cd25977e0a5ae17155770273ad58648900d3": "OKX",
    "0x6cc5f688a315f3dc28a7781717a9a798a59fda7b": "OKX",
    "0x176f3dab24a159341c0509bb36b833e7fdd0a132": "KuCoin",
    "0x1692e170361cefd1eb7240ec13d048fd9af6d667": "KuCoin",
    "0x2910543af39aba0cd09dbb2d50200b3e800a63d2": "Kraken",
    "0x267be1c1d684f78cb4f6a176c4911b741e4ffdc0": "Kraken",
}

# Coin price estimates (fallback)
PRICE_ESTIMATES = {
    "BTC": 65000,
    "ETH": 3500,
    "BNB": 600,
    "SOL": 150,
    "TRX": 0.12,
    "USDT": 1.0,
    "USDC": 1.0,
    "DOGE": 0.15,
    "XRP": 0.60,
}


def curl_fetch(url, headers=None):
    """Fetch URL using curl subprocess."""
    cmd = ["curl", "-s", "-f", "--connect-timeout", "10", "--max-time", "30"]
    if headers:
        for k, v in headers.items():
            cmd.extend(["-H", "{}: {}".format(k, v)])
    cmd.append(url)
    try:
        result = subprocess.check_output(cmd, stderr=subprocess.PIPE)
        return json.loads(result.decode("utf-8"))
    except (subprocess.CalledProcessError, json.JSONDecodeError, UnicodeDecodeError):
        return None


def get_current_price(coin):
    """Get current price from CoinGecko."""
    coin_ids = {
        "BTC": "bitcoin",
        "ETH": "ethereum",
        "BNB": "binancecoin",
        "SOL": "solana",
        "TRX": "tron",
        "USDT": "tether",
        "USDC": "usd-coin",
        "DOGE": "dogecoin",
        "XRP": "ripple",
        "MATIC": "matic-network",
        "AVAX": "avalanche-2",
        "ADA": "cardano",
    }
    cg_id = coin_ids.get(coin.upper(), coin.lower())
    url = "https://api.coingecko.com/api/v3/simple/price?ids={}&vs_currencies=usd".format(cg_id)
    data = curl_fetch(url)
    if data and cg_id in data:
        return data[cg_id].get("usd", PRICE_ESTIMATES.get(coin, 0))
    return PRICE_ESTIMATES.get(coin, 0)


def fetch_whale_alert_transactions():
    """Fetch from Whale Alert API."""
    now = int(time.time())
    start = now - (HOURS * 3600)
    base_url = "https://api.whale-alert.io/v1/transactions"
    params = "?api_key={}&min_value={}&start={}&cursor=".format(
        API_KEY if API_KEY else "demo",
        int(THRESHOLD * get_current_price(COIN)),
        start
    )
    if COIN.upper() != "ALL":
        params += "&currency={}".format(COIN.lower())
    url = base_url + params
    data = curl_fetch(url)
    if data and "transactions" in data:
        return data["transactions"]
    return []


def fetch_blockchair_transactions():
    """Fetch large transactions from Blockchair API."""
    chain_map = {
        "bitcoin": "bitcoin",
        "ethereum": "ethereum",
        "bsc": "binance-smart-chain",
    }
    bc_chain = chain_map.get(CHAIN, CHAIN)
    url = "https://api.blockchair.com/{}/transactions?s=output_total(desc)&limit={}".format(
        bc_chain, TOP
    )
    data = curl_fetch(url)
    if data and "data" in data:
        return data["data"]
    return []


def fetch_etherscan_transactions(address):
    """Fetch transactions for a specific address from Etherscan."""
    url = "https://api.etherscan.io/api?module=account&action=txlist&address={}&startblock=0&endblock=99999999&sort=desc&page=1&offset={}".format(
        address, TOP
    )
    data = curl_fetch(url)
    if data and data.get("status") == "1" and "result" in data:
        return data["result"]
    return []


def classify_transfer(from_addr, to_addr):
    """Classify a transfer based on known addresses."""
    from_label = KNOWN_EXCHANGES.get(from_addr.lower(), "") if from_addr else ""
    to_label = KNOWN_EXCHANGES.get(to_addr.lower(), "") if to_addr else ""

    if from_label and to_label:
        return "Exchange to Exchange", "neutral", from_label, to_label
    elif from_label and not to_label:
        return "Exchange Outflow", "bullish", from_label, "Unknown Wallet"
    elif not from_label and to_label:
        return "Exchange Inflow", "bearish", "Unknown Wallet", to_label
    else:
        return "Whale Transfer", "neutral", "Unknown Wallet", "Unknown Wallet"


def generate_demo_transactions():
    """Generate realistic demo data when API is unavailable."""
    import random
    import hashlib

    price = get_current_price(COIN)
    if price == 0:
        price = PRICE_ESTIMATES.get(COIN, 1000)

    now = time.time()
    transactions = []
    exchange_addrs = list(KNOWN_EXCHANGES.keys())

    for i in range(min(TOP, 15)):
        amount = THRESHOLD * (1 + random.random() * 20)
        tx_time = now - random.randint(0, HOURS * 3600)

        # Randomly assign from/to addresses
        roll = random.random()
        if roll < 0.3:
            # Exchange inflow
            from_addr = hashlib.sha256("whale{}".format(i).encode()).hexdigest()[:40]
            to_addr = random.choice(exchange_addrs)
        elif roll < 0.6:
            # Exchange outflow
            from_addr = random.choice(exchange_addrs)
            to_addr = hashlib.sha256("cold{}".format(i).encode()).hexdigest()[:40]
        else:
            # Whale to whale
            from_addr = hashlib.sha256("from{}".format(i).encode()).hexdigest()[:40]
            to_addr = hashlib.sha256("to{}".format(i).encode()).hexdigest()[:40]

        tx_hash = hashlib.sha256("tx{}{}".format(i, time.time()).encode()).hexdigest()

        classification, signal, from_label, to_label = classify_transfer(from_addr, to_addr)

        transactions.append({
            "hash": tx_hash,
            "timestamp": int(tx_time),
            "from": from_addr,
            "to": to_addr,
            "amount": round(amount, 4),
            "usd_value": round(amount * price, 2),
            "coin": COIN,
            "classification": classification,
            "signal": signal,
            "from_label": from_label,
            "to_label": to_label,
        })

    transactions.sort(key=lambda x: x["usd_value"], reverse=True)
    return transactions


def normalize_whale_alert_tx(raw_txs):
    """Normalize Whale Alert API response to our format."""
    transactions = []
    for tx in raw_txs:
        amount = tx.get("amount", 0)
        if amount < THRESHOLD:
            continue
        from_addr = tx.get("from", {}).get("address", "")
        to_addr = tx.get("to", {}).get("address", "")
        classification, signal, from_label, to_label = classify_transfer(from_addr, to_addr)

        # Use API labels if available
        if tx.get("from", {}).get("owner", ""):
            from_label = tx["from"]["owner"]
        if tx.get("to", {}).get("owner", ""):
            to_label = tx["to"]["owner"]

        transactions.append({
            "hash": tx.get("hash", "unknown"),
            "timestamp": tx.get("timestamp", int(time.time())),
            "from": from_addr,
            "to": to_addr,
            "amount": amount,
            "usd_value": tx.get("amount_usd", amount * get_current_price(COIN)),
            "coin": tx.get("symbol", COIN).upper(),
            "classification": classification,
            "signal": signal,
            "from_label": from_label,
            "to_label": to_label,
        })
    transactions.sort(key=lambda x: x["usd_value"], reverse=True)
    return transactions[:TOP]


def format_usd(value):
    """Format USD value with appropriate suffix."""
    if value >= 1_000_000_000:
        return "${:.1f}B".format(value / 1_000_000_000)
    elif value >= 1_000_000:
        return "${:.1f}M".format(value / 1_000_000)
    elif value >= 1_000:
        return "${:.1f}K".format(value / 1_000)
    else:
        return "${:.2f}".format(value)


def signal_emoji(signal):
    """Get emoji for signal type."""
    return {
        "bullish": "\U0001f7e2",
        "bearish": "\U0001f534",
        "neutral": "\u26aa",
    }.get(signal, "\u26aa")


def format_text(transactions):
    """Format transactions as text report."""
    lines = []
    lines.append("")
    lines.append("\U0001f40b WHALE ALERT \u2014 {} Transfers > {} {} (Last {}h)".format(
        COIN, int(THRESHOLD) if THRESHOLD == int(THRESHOLD) else THRESHOLD, COIN, HOURS))
    lines.append("\u2550" * 60)
    lines.append("")

    total_amount = 0
    total_usd = 0
    inflow_amount = 0
    outflow_amount = 0

    for i, tx in enumerate(transactions, 1):
        emoji = signal_emoji(tx["signal"])
        lines.append("#{:<3} {} {:,.4f} {} ({}) \u2014 {} \u2192 {}".format(
            i, emoji, tx["amount"], tx["coin"], format_usd(tx["usd_value"]),
            tx["from_label"], tx["to_label"]))
        lines.append("    TX: {}...{}".format(tx["hash"][:12], tx["hash"][-8:]))
        dt = datetime.datetime.utcfromtimestamp(tx["timestamp"])
        lines.append("    Time: {} UTC".format(dt.strftime("%Y-%m-%d %H:%M")))
        lines.append("    Signal: {} ({})".format(tx["signal"].upper(), tx["classification"]))
        lines.append("")

        total_amount += tx["amount"]
        total_usd += tx["usd_value"]
        if tx["signal"] == "bearish":
            inflow_amount += tx["amount"]
        elif tx["signal"] == "bullish":
            outflow_amount += tx["amount"]

    lines.append("\u2550" * 60)
    lines.append("Summary: {} whale transfers totaling {:,.4f} {} ({})".format(
        len(transactions), total_amount, COIN, format_usd(total_usd)))
    lines.append("  Inflows to exchanges:  {:,.4f} {} ({:.1f}%)".format(
        inflow_amount, COIN,
        (inflow_amount / total_amount * 100) if total_amount > 0 else 0))
    lines.append("  Outflows from exchanges: {:,.4f} {} ({:.1f}%)".format(
        outflow_amount, COIN,
        (outflow_amount / total_amount * 100) if total_amount > 0 else 0))

    net = outflow_amount - inflow_amount
    if net > 0:
        lines.append("  Net flow: OUTFLOW (bullish signal)")
    elif net < 0:
        lines.append("  Net flow: INFLOW (bearish signal)")
    else:
        lines.append("  Net flow: NEUTRAL")

    return "\n".join(lines)


def format_json(transactions):
    """Format transactions as JSON."""
    report = {
        "generated_at": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "coin": COIN,
        "chain": CHAIN,
        "threshold": THRESHOLD,
        "lookback_hours": HOURS,
        "total_transactions": len(transactions),
        "total_amount": sum(tx["amount"] for tx in transactions),
        "total_usd": sum(tx["usd_value"] for tx in transactions),
        "transactions": transactions,
    }
    return json.dumps(report, indent=2, ensure_ascii=False)


def format_csv(transactions):
    """Format transactions as CSV."""
    lines = ["hash,timestamp,from,from_label,to,to_label,amount,coin,usd_value,classification,signal"]
    for tx in transactions:
        lines.append("{},{},{},{},{},{},{},{},{},{},{}".format(
            tx["hash"], tx["timestamp"], tx["from"], tx["from_label"],
            tx["to"], tx["to_label"], tx["amount"], tx["coin"],
            tx["usd_value"], tx["classification"], tx["signal"]))
    return "\n".join(lines)


def format_html(transactions):
    """Format transactions as HTML report."""
    total_amount = sum(tx["amount"] for tx in transactions)
    total_usd = sum(tx["usd_value"] for tx in transactions)
    inflow = sum(tx["amount"] for tx in transactions if tx["signal"] == "bearish")
    outflow = sum(tx["amount"] for tx in transactions if tx["signal"] == "bullish")

    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Whale Tracker Report - {coin}</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0d1117; color: #c9d1d9; margin: 0; padding: 20px; }}
.container {{ max-width: 1200px; margin: 0 auto; }}
h1 {{ color: #58a6ff; font-size: 24px; }}
.stats {{ display: flex; gap: 20px; margin: 20px 0; flex-wrap: wrap; }}
.stat-card {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 16px; flex: 1; min-width: 200px; }}
.stat-card .label {{ color: #8b949e; font-size: 12px; text-transform: uppercase; }}
.stat-card .value {{ color: #f0f6fc; font-size: 24px; font-weight: bold; margin-top: 4px; }}
table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
th {{ background: #161b22; color: #8b949e; padding: 12px; text-align: left; border-bottom: 1px solid #30363d; }}
td {{ padding: 12px; border-bottom: 1px solid #21262d; }}
tr:hover {{ background: #161b22; }}
.bullish {{ color: #3fb950; }}
.bearish {{ color: #f85149; }}
.neutral {{ color: #8b949e; }}
.hash {{ font-family: monospace; font-size: 12px; color: #58a6ff; }}
.footer {{ text-align: center; margin-top: 40px; color: #484f58; font-size: 12px; }}
</style>
</head>
<body>
<div class="container">
<h1>\U0001f40b Whale Tracker Report &mdash; {coin}</h1>
<p>Transfers &gt; {threshold} {coin} in the last {hours} hours</p>
<p style="color:#484f58;">Generated: {timestamp}</p>

<div class="stats">
<div class="stat-card">
    <div class="label">Total Transfers</div>
    <div class="value">{total_count}</div>
</div>
<div class="stat-card">
    <div class="label">Total Volume</div>
    <div class="value">{total_amount} {coin}</div>
</div>
<div class="stat-card">
    <div class="label">USD Value</div>
    <div class="value">{total_usd}</div>
</div>
<div class="stat-card">
    <div class="label">Net Flow</div>
    <div class="value {net_class}">{net_flow}</div>
</div>
</div>

<table>
<thead>
<tr><th>#</th><th>Amount</th><th>USD</th><th>From</th><th>To</th><th>Signal</th><th>Time</th><th>TX</th></tr>
</thead>
<tbody>
""".format(
        coin=COIN,
        threshold=int(THRESHOLD) if THRESHOLD == int(THRESHOLD) else THRESHOLD,
        hours=HOURS,
        timestamp=datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        total_count=len(transactions),
        total_amount="{:,.2f}".format(total_amount),
        total_usd=format_usd(total_usd),
        net_class="bullish" if outflow > inflow else "bearish" if inflow > outflow else "neutral",
        net_flow="OUTFLOW" if outflow > inflow else "INFLOW" if inflow > outflow else "NEUTRAL",
    )

    for i, tx in enumerate(transactions, 1):
        dt = datetime.datetime.utcfromtimestamp(tx["timestamp"])
        html += """<tr>
<td>{idx}</td>
<td>{amount} {coin}</td>
<td>{usd}</td>
<td>{from_label}</td>
<td>{to_label}</td>
<td class="{signal}">{signal_upper}</td>
<td>{time}</td>
<td class="hash">{hash}</td>
</tr>
""".format(
            idx=i,
            amount="{:,.4f}".format(tx["amount"]),
            coin=tx["coin"],
            usd=format_usd(tx["usd_value"]),
            from_label=tx["from_label"],
            to_label=tx["to_label"],
            signal=tx["signal"],
            signal_upper=tx["signal"].upper(),
            time=dt.strftime("%H:%M"),
            hash="{}...{}".format(tx["hash"][:8], tx["hash"][-6:]),
        )

    html += """</tbody>
</table>
<div class="footer">
<p>Powered by BytesAgain | bytesagain.com | hello@bytesagain.com</p>
</div>
</div>
</body>
</html>"""
    return html


def main():
    """Main entry point."""
    sys.stderr.write("[*] Crypto Whale Tracker starting...\n")
    sys.stderr.write("[*] Tracking {} transfers > {} {} on {} (last {}h)\n".format(
        COIN, THRESHOLD, COIN, CHAIN, HOURS))

    transactions = []

    # Try Whale Alert API first
    if API_KEY:
        sys.stderr.write("[*] Fetching from Whale Alert API...\n")
        raw = fetch_whale_alert_transactions()
        transactions = normalize_whale_alert_tx(raw)

    # Try Etherscan for specific wallet
    if not transactions and WALLET and CHAIN == "ethereum":
        sys.stderr.write("[*] Fetching from Etherscan for wallet {}...\n".format(WALLET[:10]))
        raw = fetch_etherscan_transactions(WALLET)
        # Process etherscan results
        for tx in raw:
            value_eth = int(tx.get("value", 0)) / 1e18
            if value_eth >= THRESHOLD:
                from_addr = tx.get("from", "")
                to_addr = tx.get("to", "")
                classification, signal, from_label, to_label = classify_transfer(from_addr, to_addr)
                transactions.append({
                    "hash": tx.get("hash", ""),
                    "timestamp": int(tx.get("timeStamp", time.time())),
                    "from": from_addr,
                    "to": to_addr,
                    "amount": round(value_eth, 4),
                    "usd_value": round(value_eth * get_current_price("ETH"), 2),
                    "coin": "ETH",
                    "classification": classification,
                    "signal": signal,
                    "from_label": from_label,
                    "to_label": to_label,
                })

    # Try Blockchair as fallback
    if not transactions and not WALLET:
        sys.stderr.write("[*] Trying Blockchair API...\n")
        raw = fetch_blockchair_transactions()
        if raw:
            for tx in raw:
                if isinstance(tx, dict):
                    value = tx.get("output_total", 0)
                    if CHAIN == "bitcoin":
                        amount = value / 1e8
                    else:
                        amount = value / 1e18
                    if amount >= THRESHOLD:
                        transactions.append({
                            "hash": tx.get("hash", "unknown"),
                            "timestamp": int(time.time()),
                            "from": "unknown",
                            "to": "unknown",
                            "amount": round(amount, 4),
                            "usd_value": round(amount * get_current_price(COIN), 2),
                            "coin": COIN,
                            "classification": "Whale Transfer",
                            "signal": "neutral",
                            "from_label": "Unknown",
                            "to_label": "Unknown",
                        })

    # Use demo data if all APIs fail
    if not transactions:
        sys.stderr.write("[*] APIs unavailable, generating demo data for illustration...\n")
        transactions = generate_demo_transactions()

    # Format output
    if FORMAT == "json":
        output = format_json(transactions)
    elif FORMAT == "csv":
        output = format_csv(transactions)
    elif FORMAT == "html":
        output = format_html(transactions)
    else:
        output = format_text(transactions)

    # Write output
    if OUTPUT:
        with open(OUTPUT, "w", encoding="utf-8") as f:
            f.write(output)
        sys.stderr.write("[*] Report written to {}\n".format(OUTPUT))
    else:
        print(output)

    sys.stderr.write("[*] Done. Tracked {} whale transactions.\n".format(len(transactions)))


if __name__ == "__main__":
    main()
PYEOF

echo "Powered by BytesAgain | bytesagain.com | hello@bytesagain.com"
