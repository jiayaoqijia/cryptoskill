#!/usr/bin/env python3
"""
Auto-redeem resolved Polymarket positions
"""

import os
import json
import urllib.request
from datetime import datetime

def fetch_json(url, timeout=15):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "AutoRedeem/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print(f"⚠️ Error: {e}")
        return None

def get_positions(wallet):
    """Get all positions for wallet"""
    url = f"https://data-api.polymarket.com/positions?user={wallet}"
    return fetch_json(url) or []

def main():
    wallet = os.environ.get("POLYMARKET_WALLET", "")
    
    if not wallet:
        print("❌ Set POLYMARKET_WALLET environment variable")
        return
    
    print(f"🔍 Checking positions for {wallet[:10]}...")
    positions = get_positions(wallet)
    
    resolved = [p for p in positions if p.get("resolved")]
    pending = [p for p in positions if not p.get("resolved")]
    
    print(f"\n📊 Total: {len(positions)} positions")
    print(f"✅ Resolved (redeemable): {len(resolved)}")
    print(f"⏳ Pending: {len(pending)}")
    
    if resolved:
        print("\n🎯 Positions to redeem:")
        for p in resolved:
            title = p.get("title", "Unknown")[:50]
            size = p.get("size", 0)
            print(f"  - {title}: {size} shares")
        
        print("\n⚠️ To redeem, use Polymarket CLOB API with your private key")
    else:
        print("\n✨ No positions to redeem right now")

if __name__ == "__main__":
    main()
