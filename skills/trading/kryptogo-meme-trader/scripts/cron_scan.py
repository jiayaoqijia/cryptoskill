#!/usr/bin/env python3
"""
CRON SCRIPT: discovery-scan
Runs every 30 minutes to discover and analyze new tokens.
"""

import sys
import os
import importlib.util
import subprocess

# Define paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# skill root is parent of scripts/
SKILL_ROOT = os.path.dirname(SCRIPT_DIR)
EXAMPLES_DIR = os.path.join(SKILL_ROOT, 'examples')
WORKFLOW_PATH = os.path.join(EXAMPLES_DIR, 'trading-workflow.py')
SWAP_SCRIPT_PATH = os.path.join(SCRIPT_DIR, 'swap.py')

# Add examples dir to sys.path to allow imports if needed
sys.path.append(EXAMPLES_DIR)

# Credentials must be pre-loaded in the environment (source ~/.openclaw/workspace/.env)
# Verify critical env vars
if not os.getenv("KRYPTOGO_API_KEY") or not os.getenv("SOLANA_WALLET_ADDRESS"):
    print("ERROR: Missing KRYPTOGO_API_KEY or SOLANA_WALLET_ADDRESS. Run 'source ~/.openclaw/workspace/.env' first.")
    sys.exit(1)

if not os.path.exists(WORKFLOW_PATH):
    print(f"ERROR: Workflow script not found at {WORKFLOW_PATH}")
    sys.exit(1)

# Monkey-patch safe_execute_trade to use swap.py
def patched_safe_execute_trade(input_mint, output_mint, amount, slippage_bps=300):
    """
    Patched execution using external swap.py script to avoid signer mismatch.
    """
    print(f"--- PATCHED EXECUTION: Calling swap.py ---")
    
    # Determine if BUY or SELL
    # Input SOL -> Output Token = BUY
    # Input Token -> Output SOL = SELL
    
    SOL_MINT = "So11111111111111111111111111111112"
    
    cmd = ["python3", SWAP_SCRIPT_PATH]
    
    if input_mint == SOL_MINT:
        # BUY: output_mint is the token to buy
        token_mint = output_mint
        # Amount passed to safe_execute_trade is usually in Lamports for SOL
        # swap.py expects SOL (float) for BUY
        amount_sol = amount / 1_000_000_000
        
        cmd.extend([token_mint, str(amount_sol)])
        print(f"Executing BUY via swap.py: {amount_sol} SOL -> {token_mint}")
        
    elif output_mint == SOL_MINT:
        # SELL: input_mint is the token to sell
        token_mint = input_mint
        
        # Amount passed to safe_execute_trade is in RAW UNITS (integer)
        # swap.py with --sell expects HUMAN READABLE units (float)
        # We must fetch decimals to convert.
        
        try:
            import requests
            headers = {"Authorization": f"Bearer {os.environ.get('KRYPTOGO_API_KEY')}"}
            # Use quicknode or kryptogo api to get decimals
            # We'll try KryptoGO token-overview first as it's used elsewhere
            print(f"Fetching decimals for {token_mint} to prepare SELL...")
            resp = requests.get(
                "https://wallet-data.kryptogo.app/token-overview",
                params={"address": token_mint},
                headers=headers,
                timeout=10
            )
            data = resp.json()
            decimals = data.get("decimals")
            if decimals is None:
                print(f"ABORT: Could not determine decimals for {token_mint}. Refusing to sell with unknown precision.")
                return None

            # Convert raw amount to human readable
            human_amount = amount / (10 ** decimals)

            cmd.extend([token_mint, str(human_amount), "--sell"])
            print(f"Executing SELL via swap.py: {human_amount} tokens ({amount} raw) -> SOL")

        except Exception as e:
            print(f"ABORT: Failed to fetch decimals for sell: {e}.")
            return None

    else:
        print("Error: swap.py only supports SOL pairs.")
        return None

    # Add slippage
    cmd.extend(["--slippage", str(slippage_bps)])
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("swap.py output:", result.stdout)
        
        # Parse output for explorer URL or fake a return object that trading-workflow expects
        # trading-workflow expects a dict with 'explorer_url' or similar
        # safe_execute_trade returns submit_transaction response (json)
        
        return {"status": "success", "explorer_url": "check_swap_py_logs", "tx_hash": "check_swap_py_logs"}
        
    except subprocess.CalledProcessError as e:
        print("swap.py failed:", e.stderr)
        return None

try:
    # Import the trading workflow module dynamically
    spec = importlib.util.spec_from_file_location("trading_workflow", WORKFLOW_PATH)
    tw = importlib.util.module_from_spec(spec)
    sys.modules["trading_workflow"] = tw
    
    # APPLY PATCH
    tw.safe_execute_trade = patched_safe_execute_trade
    
    spec.loader.exec_module(tw)
    
    # Run Discovery Pipeline
    print(f"Starting discovery scan using logic from {WORKFLOW_PATH}...")
    # NOTE: We re-patch again just in case exec_module overwrote it (unlikely but safe)
    tw.safe_execute_trade = patched_safe_execute_trade
    
    result = tw.discover_and_analyze()
    
    if result:
        print("Discovery scan completed with a trade execution.")
    else:
        print("Discovery scan completed. No trades executed.")

except Exception as e:
    print(f"CRITICAL ERROR in cron_scan: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
