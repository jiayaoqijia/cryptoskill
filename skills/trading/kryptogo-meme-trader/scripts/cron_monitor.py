#!/usr/bin/env python3
"""
CRON SCRIPT: stop-loss-tp
Runs every 5 minutes to check portfolio for stop-loss or take-profit conditions.
"""

import sys
import os
import json
import subprocess

# Add parent directory to path so we can import 'examples.trading-workflow' or similar
# The trading-workflow.py is in ../examples/ relative to this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
EXAMPLES_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), 'examples')
SWAP_SCRIPT_PATH = os.path.join(SCRIPT_DIR, 'swap.py')
WORKFLOW_PATH = os.path.join(EXAMPLES_DIR, "trading-workflow.py")

sys.path.append(EXAMPLES_DIR)

# Credentials must be pre-loaded in the environment (source ~/.openclaw/workspace/.env)
# Verify critical env vars
if not os.getenv("KRYPTOGO_API_KEY") or not os.getenv("SOLANA_WALLET_ADDRESS"):
    print("ERROR: Missing KRYPTOGO_API_KEY or SOLANA_WALLET_ADDRESS. Run 'source ~/.openclaw/workspace/.env' first.")
    sys.exit(1)

# Monkey-patch safe_execute_trade to use swap.py
def patched_safe_execute_trade(input_mint, output_mint, amount, slippage_bps=300):
    """
    Patched execution using external swap.py script to avoid signer mismatch.
    """
    print(f"--- PATCHED EXECUTION: Calling swap.py ---")
    
    SOL_MINT = "So11111111111111111111111111111112"
    cmd = ["python3", SWAP_SCRIPT_PATH]
    
    if input_mint == SOL_MINT:
        # BUY
        token_mint = output_mint
        amount_sol = amount / 1_000_000_000
        cmd.extend([token_mint, str(amount_sol)])
        print(f"Executing BUY: {amount_sol} SOL -> {token_mint}")
        
    elif output_mint == SOL_MINT:
        # SELL
        token_mint = input_mint
        # For sell, swap.py expects amount in SOL if buying, or token units if selling?
        # Let's check swap.py again.
        # It takes "amount" as a float.
        # If --sell is present: amount = int(args.amount * (10 ** decimals))
        # So args.amount MUST be human readable float.
        
        # But 'amount' passed here from trading-workflow.py is RAW INTEGER (lamports/units).
        # We need to convert it back to human readable float.
        
        try:
            import requests
            headers = {"Authorization": f"Bearer {os.getenv('KRYPTOGO_API_KEY')}"}
            resp = requests.get(
                f"https://wallet-data.kryptogo.app/token-overview",
                params={"address": token_mint},
                headers=headers
            )
            data = resp.json()
            decimals = data.get("decimals")
            if decimals is None:
                print(f"ABORT: Could not determine decimals for {token_mint}. Refusing to sell with unknown precision.")
                return None
            human_amount = amount / (10 ** decimals)

            cmd.extend([token_mint, str(human_amount), "--sell"])
            print(f"Executing SELL: {human_amount} tokens ({amount} raw) -> SOL")

        except Exception as e:
            print(f"ABORT: Failed to fetch decimals for sell: {e}.")
            return None

    else:
        print("Error: swap.py only supports SOL pairs.")
        return None

    cmd.extend(["--slippage", str(slippage_bps)])
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("swap.py output:", result.stdout)
        return {"status": "success", "explorer_url": "check_swap_py_logs", "tx_hash": "check_swap_py_logs"}
        
    except subprocess.CalledProcessError as e:
        print("swap.py failed:", e.stderr)
        return None

try:
    # Import the trading workflow module
    import importlib.util
    spec = importlib.util.spec_from_file_location("trading_workflow", WORKFLOW_PATH)
    tw = importlib.util.module_from_spec(spec)
    sys.modules["trading_workflow"] = tw
    
    # APPLY PATCH BEFORE LOAD
    tw.safe_execute_trade = patched_safe_execute_trade
    
    spec.loader.exec_module(tw)
    
    # RE-APPLY PATCH AFTER LOAD (just in case)
    tw.safe_execute_trade = patched_safe_execute_trade
    
    # 1. Check Portfolio & Monitor Positions
    print("Checking portfolio for stop-loss / take-profit conditions...")
    actions = tw.monitor_positions()
    
    if not actions:
        print("No actions needed. All positions within thresholds.")
        sys.exit(0)

    # 2. Execute Actions
    for action in actions:
        mint = action["mint"]
        symbol = action["symbol"]
        act_type = action["action"]
        reason = action["reason"]
        
        print(f"Action triggered: {act_type} {symbol} ({reason})")
        
        # We need pnl_pct and holding_hours for logging
        portfolio = tw.get_portfolio(os.getenv("SOLANA_WALLET_ADDRESS"))
        token_data = next((t for t in portfolio.get("tokens", []) if t["mint"] == mint), None)
        
        pnl_pct = 0.0
        pnl_sol = 0.0
        holding_hours = 0.0
        
        if token_data:
            # Recalculate PnL/holding metrics for the log
            unrealized_pnl = float(token_data.get("unrealized_pnl", "0"))
            avg_cost = float(token_data.get("holding_avg_cost", "0"))
            balance = float(token_data.get("balance", "0"))
            cost_basis = avg_cost * balance
            if cost_basis > 0:
                pnl_pct = (unrealized_pnl / cost_basis * 100)
            pnl_sol = unrealized_pnl # assuming raw value is USD or SOL? API usually returns USD for PnL
            holding_hours = int(float(token_data.get("avg_holding_seconds", "0"))) / 3600

        if act_type in ["SELL", "TAKE_PROFIT"]:
            print(f"Executing SELL for {symbol}...")
            # execute_exit calls safe_execute_trade, which is now patched!
            result = tw.execute_exit(mint, symbol, act_type, reason, pnl_pct, pnl_sol, holding_hours)
            if result:
                print(f"SUCCESS: Sold {symbol}. Tx: {result.get('tx_hash', 'N/A')}")
            else:
                print(f"FAILED: Could not execute sell for {symbol}.")
        
        elif act_type == "REDUCE":
            print(f"Recommendation: REDUCE {symbol} (Distribution detected). Auto-reduce not implemented yet.")
            
        elif act_type == "REVIEW":
            print(f"Recommendation: REVIEW {symbol} (Stale position > 24h).")

except Exception as e:
    print(f"CRITICAL ERROR in cron_monitor: {e}")
    sys.exit(1)
