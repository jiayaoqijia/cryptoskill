#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import requests

# Credentials must be pre-loaded in the environment (source ~/.openclaw/workspace/.env)
API_KEY = os.environ.get("KRYPTOGO_API_KEY")
WALLET = os.environ.get("SOLANA_WALLET_ADDRESS")

if not API_KEY or not WALLET:
    print("ERROR: Missing KRYPTOGO_API_KEY or SOLANA_WALLET_ADDRESS.")
    print("Run 'source ~/.openclaw/workspace/.env' before running this script.")
    sys.exit(1)

# Config
PREFS_PATH = os.path.expanduser("~/.openclaw/workspace/memory/trading-preferences.json")
STOP_LOSS_PCT = 30
TAKE_PROFIT_PCT = 100

if os.path.exists(PREFS_PATH):
    try:
        with open(PREFS_PATH) as f:
            prefs = json.load(f)
            STOP_LOSS_PCT = prefs.get("stop_loss_pct", 30)
            TAKE_PROFIT_PCT = prefs.get("take_profit_pct", 100)
    except:
        pass

print(f"Monitor Config: SL={STOP_LOSS_PCT}%, TP={TAKE_PROFIT_PCT}%")

# Fetch Portfolio
try:
    resp = requests.get(
        "https://wallet-data.kryptogo.app/agent/portfolio",
        headers={"Authorization": f"Bearer {API_KEY}"},
        params={"wallet_address": WALLET},
        timeout=10
    )
    if resp.status_code != 200:
        print(f"Error fetching portfolio: {resp.status_code} {resp.text}")
        exit(1)

    data = resp.json()
    tokens = data.get("tokens", [])
    
    # Filter for active tokens
    active_positions = [t for t in tokens if float(t.get("balance", 0)) > 0]
    
    if not active_positions:
        print("No open positions.")
        exit(0)
        
    for pos in active_positions:
        symbol = pos.get("symbol", "Unknown")
        mint = pos.get("mint")
        balance = float(pos.get("balance", 0))
        
        # PnL from API
        # API returns realized/unrealized PnL in USD. 
        # We need unrealized PnL percentage.
        # Check if API provides pct directly, otherwise calc.
        
        unrealized_pnl_usd = float(pos.get("unrealized_pnl", 0))
        usd_value = float(pos.get("usd_value", 0))
        
        # Calculate cost basis to get %
        cost_basis = usd_value - unrealized_pnl_usd
        
        pnl_pct = 0
        if cost_basis > 0:
            pnl_pct = (unrealized_pnl_usd / cost_basis) * 100
        
        # Fallback: if cost_basis is 0 or weird, maybe use journal? 
        # For now rely on API logic.
            
        print(f"Position: {symbol} | Value: ${usd_value:.2f} | PnL: {pnl_pct:.2f}% (${unrealized_pnl_usd:.2f})")
        
        action = None
        
        # CLUSTER DUMP CHECK
        try:
            cluster_resp = requests.get(
                f"https://wallet-data.kryptogo.app/analyze-cluster-change/{mint}",
                headers={"Authorization": f"Bearer {API_KEY}"},
                timeout=5
            )
            if cluster_resp.status_code == 200:
                c_data = cluster_resp.json()
                cluster_ratio = c_data.get("cluster_ratio", 0)
                changes = c_data.get("changes", {})
                change_1h = changes.get("1h", 0)
                change_15m = changes.get("15m", 0)
                
                # Rule 1: Hard Dump (1h drop > 5%)
                if change_1h <= -0.05:
                    print(f"  ⚠️ ALERT: Cluster dumping! 1h change: {change_1h*100:.1f}%")
                    action = "CLUSTER_DUMP"
                
                # Rule 1.5: Flash Dump (15m drop > 2.5%) - Faster reaction for new coins
                if change_15m <= -0.025:
                    print(f"  ⚠️ ALERT: Flash dump detected! 15m change: {change_15m*100:.1f}%")
                    action = "CLUSTER_FLASH_DUMP"
                
                # Rule 2: Loss of Control (Ratio < 15%)
                if cluster_ratio < 0.15 and pnl_pct < 20: # Only if profit is low
                     print(f"  ⚠️ ALERT: Cluster control lost! Ratio: {cluster_ratio*100:.1f}%")
                     action = "CLUSTER_LOST"
        except Exception:
            pass

        if pnl_pct <= -STOP_LOSS_PCT:
            action = "STOP_LOSS"
        elif pnl_pct >= TAKE_PROFIT_PCT:
            action = "TAKE_PROFIT"
            
        if action:
            print(f"⚠️ Triggering {action} for {symbol} ({mint})...")
            
            # Call swap.py to execute sell
            # Ensure path is absolute or relative to workspace root
            script_path = os.path.expanduser("~/.openclaw/workspace/skills/kryptogo-meme-trader/scripts/swap.py")
            
            cmd = [
                "python3", 
                script_path, 
                mint, 
                str(balance), 
                "--sell"
            ]
            print(f"Running: {' '.join(cmd)}")
            subprocess.run(cmd)
            
except Exception as e:
    print(f"Error checking portfolio: {e}")
