#!/usr/bin/env python3
"""
KryptoGO Meme Trader — Swap Executor

Builds, signs locally, and submits a token swap transaction via the
KryptoGO Agent Trading API (Solana only).

Usage:
  python3 scripts/swap.py <output_mint> [amount_sol]
  python3 scripts/swap.py <output_mint> [amount_sol] --sell
  python3 scripts/swap.py <output_mint> [amount_sol] --slippage 500

Examples:
  # Buy 0.1 SOL worth of a token
  python3 scripts/swap.py So11...token_mint_address 0.1

  # Sell tokens back to SOL (--sell flag)
  python3 scripts/swap.py So11...token_mint_address 1000000 --sell

  # Custom slippage (basis points, default: 300 = 3%)
  python3 scripts/swap.py So11...token_mint_address 0.1 --slippage 500

Environment (must be sourced before running):
  KRYPTOGO_API_KEY       - API key for authentication
  SOLANA_WALLET_ADDRESS  - Agent wallet public address
  SOLANA_PRIVATE_KEY     - Agent wallet private key (base58, never sent to server)

SECURITY:
  - This script does NOT read .env directly. Credentials must be loaded into
    the environment by the caller (e.g., `source ~/.openclaw/workspace/.env`).
  - Private key is used ONLY for local signing
  - Key is never sent to any server or logged to output
  - Transaction is signed locally with `solders` library
"""

import argparse
import base64
import json
import os
import sys
import time
import datetime
from decimal import Decimal, getcontext

import requests

# Set decimal precision high enough for crypto
getcontext().prec = 28

# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------

API_BASE = "https://wallet-data.kryptogo.app"
API_KEY = os.environ.get("KRYPTOGO_API_KEY")
WALLET = os.environ.get("SOLANA_WALLET_ADDRESS")
PRIVATE_KEY = os.environ.get("SOLANA_PRIVATE_KEY")

SOL_MINT = "So11111111111111111111111111111112"

if not all([API_KEY, WALLET, PRIVATE_KEY]):
    sys.exit("ERROR: Missing required env vars. Run 'source ~/.openclaw/workspace/.env' before running this script.")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

parser = argparse.ArgumentParser(description="KryptoGO Swap Executor")
parser.add_argument("token_mint", help="Token mint address to buy or sell")
parser.add_argument(
    "amount",
    type=str,  # Capture as string to preserve precision for Decimal
    nargs="?",
    default="0.1",
    help="Amount in SOL (buy) or token units (sell). Default: 0.1 SOL",
)
parser.add_argument(
    "--sell",
    action="store_true",
    help="Sell tokens back to SOL (default is buy)",
)
parser.add_argument(
    "--slippage",
    type=int,
    default=500,
    help="Slippage tolerance in basis points (default: 500 = 5%%)",
)
parser.add_argument(
    "--max-impact",
    type=float,
    default=10.0,
    help="Max price impact %% before aborting (default: 10)",
)
args = parser.parse_args()

# ---------------------------------------------------------------------------
# Step 1: Build swap transaction
# ---------------------------------------------------------------------------

# Fetch token info for journal
token_info = {}
try:
    resp = requests.get(
        f"{API_BASE}/token-overview",
        params={"address": args.token_mint},
        headers=HEADERS,
        timeout=5
    )
    if resp.status_code == 200:
        token_info = resp.json()
except Exception as e:
    print(f"Warning: Could not fetch token info: {e}")

token_symbol = token_info.get("symbol", "UNKNOWN")
decimals = token_info.get("decimals")
current_price = token_info.get("price", 0)

# Use Decimal for precise arithmetic
amount_dec = Decimal(args.amount)

if args.sell:
    if decimals is None:
        sys.exit("ABORT: Could not determine token decimals. Refusing to sell with unknown precision.")
    input_mint = args.token_mint
    output_mint = SOL_MINT
    # Exact calculation: amount * 10^decimals
    amount_raw = int(amount_dec * (Decimal(10) ** decimals))
    print(f"=== SELL: {args.amount} {token_symbol} ({amount_raw} raw units) → SOL ===")
else:
    input_mint = SOL_MINT
    output_mint = args.token_mint
    # Exact calculation: amount * 10^9 (SOL decimals)
    amount_raw = int(amount_dec * Decimal(1_000_000_000))
    print(f"=== BUY: {args.amount} SOL ({amount_raw} lamports) → {token_symbol} (price: ${current_price}) ===")

print("\nStep 1: Building swap transaction...")
swap_resp = requests.post(
    f"{API_BASE}/agent/swap",
    headers=HEADERS,
    json={
        "input_mint": input_mint,
        "output_mint": output_mint,
        "amount": amount_raw,
        "slippage_bps": args.slippage,
        "wallet_address": WALLET,
    },
)

if swap_resp.status_code != 200:
    sys.exit(f"Swap build failed (HTTP {swap_resp.status_code}): {swap_resp.text}")

swap_data = swap_resp.json()
fee_payer = swap_data.get("fee_payer")
price_impact = float(swap_data.get("quote", {}).get("price_impact_pct", 0))

print(f"  Fee payer: {fee_payer}")
print(f"  Price impact: {price_impact}%")
print(f"  Platform fee: {swap_data.get('platform_fee_lamports', '?')} lamports")

# Verify fee payer matches our wallet
if fee_payer and fee_payer != WALLET:
    sys.exit(f"ABORT: Fee payer mismatch! Expected {WALLET}, got {fee_payer}")

# Check price impact
if abs(price_impact) > args.max_impact:
    sys.exit(f"ABORT: Price impact {price_impact}% exceeds max {args.max_impact}%")
elif abs(price_impact) > 5:
    print(f"  ⚠ WARNING: Price impact {price_impact}% is high (>5%)")

# Extract estimated output amount for journal
estimated_out_amount = 0
try:
    quote = swap_data.get("quote", {})
    # Look for outAmount in quote (structure varies, usually outAmount or amount_out)
    raw_out = quote.get("outAmount") or quote.get("amount_out") or quote.get("out_amount")
    if raw_out and decimals is not None:
        estimated_out_amount = float(raw_out) / (10 ** decimals)
except Exception:
    pass

# ---------------------------------------------------------------------------
# Step 2: Sign locally
# ---------------------------------------------------------------------------

print("\nStep 2: Signing transaction locally...")
from solders.keypair import Keypair
from solders.transaction import VersionedTransaction

tx_bytes = base64.b64decode(swap_data["transaction"])
tx = VersionedTransaction.from_bytes(tx_bytes)
keypair = Keypair.from_base58_string(PRIVATE_KEY)
signed_tx = VersionedTransaction(tx.message, [keypair])
signed_tx_b64 = base64.b64encode(bytes(signed_tx)).decode()
print("  Signed successfully.")

# ---------------------------------------------------------------------------
# Step 3: Submit
# ---------------------------------------------------------------------------

print("\nStep 3: Submitting signed transaction...")
submit_resp = requests.post(
    f"{API_BASE}/agent/submit",
    headers=HEADERS,
    json={"signed_transaction": signed_tx_b64},
)

if submit_resp.status_code != 200:
    sys.exit(f"Submit failed (HTTP {submit_resp.status_code}): {submit_resp.text}")

result = submit_resp.json()
tx_hash = result.get("tx_hash", result.get("signature", "?"))
print(f"\n  Status: {result.get('status', '?')}")
print(f"  Tx Hash: {tx_hash}")
print(f"  Explorer: https://solscan.io/tx/{tx_hash}")

# ---------------------------------------------------------------------------
# Step 4: Persist to Trading Journal
# ---------------------------------------------------------------------------

journal_path = os.path.expanduser("~/.openclaw/workspace/memory/trading-journal.json")

# Ensure directory exists
os.makedirs(os.path.dirname(journal_path), exist_ok=True)

# Load existing journal
try:
    if os.path.exists(journal_path):
        with open(journal_path, "r") as f:
            journal_data = json.load(f)
    else:
        journal_data = {"trades": []}
except Exception as e:
    print(f"Warning: Could not read journal file: {e}. Creating new.")
    journal_data = {"trades": []}

# Construct log entry
timestamp_ms = int(time.time() * 1000)
iso_time = datetime.datetime.now().isoformat()

if not args.sell:
    # BUY -> Create OPEN position
    
    # Calculate effective entry price in SOL (not USD)
    entry_price_sol = 0
    if estimated_out_amount > 0:
        entry_price_sol = float(amount_dec) / estimated_out_amount
        
    new_trade = {
        "id": f"{iso_time}_{token_symbol}",
        "token_mint": args.token_mint,
        "symbol": token_symbol,
        "chain_id": "501", # Default Solana
        "action": "BUY",
        "amount_sol": float(amount_dec),
        "token_amount": estimated_out_amount,
        "price_at_entry_sol": entry_price_sol,
        "price_at_entry_usd": current_price, # USD price from API
        "tx_hash": tx_hash,
        "status": "OPEN",
        "timestamp": iso_time,
        "timestamp_ms": timestamp_ms
    }
    journal_data["trades"].append(new_trade)
    print(f"\nLogged BUY trade to journal: {new_trade['id']}")
    print(f"  Entry Price: {entry_price_sol:.9f} SOL / ${current_price} USD")

else:
    # SELL -> Find open position and close it (or just log sell event)
    # Simple logic: Log a separate SELL entry. Advanced logic: Update corresponding BUY.
    # For now, append a SELL entry so humans can see it.
    sell_entry = {
        "id": f"{iso_time}_{token_symbol}_SELL",
        "token_mint": args.token_mint,
        "symbol": token_symbol,
        "chain_id": "501",
        "action": "SELL",
        "amount_sol": 0, # Unknown without price at exit
        "tx_hash": tx_hash,
        "status": "CLOSED",
        "timestamp": iso_time,
        "timestamp_ms": timestamp_ms
    }
    journal_data["trades"].append(sell_entry)
    print(f"\nLogged SELL trade to journal: {sell_entry['id']}")

# Save journal
try:
    with open(journal_path, "w") as f:
        json.dump(journal_data, f, indent=2)
    print(f"Journal updated at {journal_path}")
except Exception as e:
    print(f"ERROR: Failed to write journal: {e}")
