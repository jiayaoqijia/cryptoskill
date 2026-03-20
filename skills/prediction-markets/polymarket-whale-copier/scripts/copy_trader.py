#!/usr/bin/env python3
"""
Polymarket Whale Copier - Copy trade any wallet automatically
"""

import os
import sys
import json
import time
import hashlib
import argparse
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

# Configuration
DEFAULT_CONFIG = {
    "target_wallet": "",
    "copy_percent": 10,
    "min_trade_usd": 5,
    "max_trade_usd": 50,
    "min_shares": 5,
    "buy_only": True,
    "check_interval_sec": 60,
    "dry_run": True
}

SCRIPT_DIR = Path(__file__).parent
CONFIG_FILE = SCRIPT_DIR / "config.json"
LOG_FILE = SCRIPT_DIR / "trades.log"
STATE_FILE = SCRIPT_DIR / "state.json"

class WhaleCopier:
    def __init__(self, config):
        self.config = config
        self.target = config["target_wallet"].lower()
        self.copy_pct = config["copy_percent"] / 100
        self.min_usd = config["min_trade_usd"]
        self.max_usd = config["max_trade_usd"]
        self.min_shares = config["min_shares"]
        self.buy_only = config["buy_only"]
        self.dry_run = config["dry_run"]
        self.interval = config["check_interval_sec"]
        
        self.private_key = os.environ.get("POLYMARKET_KEY", "")
        self.our_wallet = self._derive_wallet() if self.private_key else None
        self.seen_trades = self._load_state()
        
    def _derive_wallet(self):
        """Derive wallet address from private key (simplified)"""
        try:
            # In production, use proper eth library
            # This is a placeholder - real implementation needs web3
            return "0x" + hashlib.sha256(self.private_key.encode()).hexdigest()[:40]
        except:
            return None
    
    def _load_state(self):
        """Load seen trade hashes"""
        try:
            if STATE_FILE.exists():
                return set(json.loads(STATE_FILE.read_text()))
        except:
            pass
        return set()
    
    def _save_state(self):
        """Save seen trade hashes"""
        STATE_FILE.write_text(json.dumps(list(self.seen_trades)[-1000:]))
    
    def _log(self, msg):
        """Log message to console and file"""
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{ts}] {msg}"
        print(line)
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    
    def _fetch_json(self, url, timeout=15):
        """Fetch JSON from URL"""
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "WhaleCopier/1.0"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode())
        except Exception as e:
            self._log(f"⚠️ Fetch error: {e}")
            return None
    
    def get_balance(self):
        """Get our USDC balance on Polygon"""
        if not self.our_wallet:
            return 0
        
        usdc = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
        payload = {
            "jsonrpc": "2.0",
            "method": "eth_call",
            "params": [{"to": usdc, "data": f"0x70a08231000000000000000000000000{self.our_wallet[2:]}"}, "latest"],
            "id": 1
        }
        
        try:
            req = urllib.request.Request(
                "https://polygon-rpc.com",
                data=json.dumps(payload).encode(),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                result = json.loads(resp.read().decode())
                return int(result.get("result", "0x0"), 16) / 1e6
        except:
            return 0
    
    def get_target_trades(self, limit=20):
        """Get recent trades from target wallet"""
        url = f"https://data-api.polymarket.com/trades?user={self.target}&limit={limit}"
        return self._fetch_json(url) or []
    
    def get_our_positions(self):
        """Get our current positions"""
        if not self.our_wallet:
            return {}
        url = f"https://data-api.polymarket.com/positions?user={self.our_wallet}"
        positions = self._fetch_json(url) or []
        return {p.get("asset_id"): p for p in positions}
    
    def _trade_hash(self, trade):
        """Generate unique hash for a trade"""
        key = f"{trade.get('id', '')}-{trade.get('timestamp', '')}"
        return hashlib.md5(key.encode()).hexdigest()
    
    def should_copy(self, trade):
        """Determine if we should copy this trade"""
        side = trade.get("side", "").upper()
        size = float(trade.get("size", 0))
        price = float(trade.get("price", 0))
        value = size * price
        
        # Skip sells if buy_only
        if self.buy_only and side != "BUY":
            return False, "SELL (buy_only enabled)"
        
        # Skip tiny trades
        if value < self.min_usd:
            return False, f"Too small (${value:.2f} < ${self.min_usd})"
        
        return True, "OK"
    
    def calculate_copy_size(self, trade):
        """Calculate our copy size"""
        size = float(trade.get("size", 0))
        price = float(trade.get("price", 0))
        
        # Calculate our size
        our_size = size * self.copy_pct
        our_value = our_size * price
        
        # Apply limits
        if our_value > self.max_usd:
            our_size = self.max_usd / price
            our_value = self.max_usd
        
        if our_size < self.min_shares:
            our_size = self.min_shares
            our_value = our_size * price
        
        return round(our_size, 1), round(our_value, 2)
    
    def execute_trade(self, trade, our_size, our_value):
        """Execute the copy trade"""
        if self.dry_run:
            self._log(f"🧪 DRY RUN: Would buy {our_size} shares @ ${trade.get('price')} = ${our_value}")
            return True
        
        # Real execution would go here
        # Requires CLOB API integration
        self._log(f"⚠️ Live trading not implemented - use Polymarket CLOB API")
        return False
    
    def process_trades(self):
        """Process new trades from target"""
        trades = self.get_target_trades()
        if not trades:
            return 0
        
        new_count = 0
        for trade in trades:
            trade_hash = self._trade_hash(trade)
            
            if trade_hash in self.seen_trades:
                continue
            
            self.seen_trades.add(trade_hash)
            new_count += 1
            
            # Check if we should copy
            should, reason = self.should_copy(trade)
            if not should:
                self._log(f"⏭️ Skip: {reason}")
                continue
            
            # Calculate copy size
            our_size, our_value = self.calculate_copy_size(trade)
            
            # Log the trade
            side = trade.get("side", "?")
            size = float(trade.get("size", 0))
            price = float(trade.get("price", 0))
            outcome = trade.get("outcome", "?")
            
            self._log(f"📈 Whale {side}: {size:.0f} shares @ ${price:.3f} = ${size*price:.2f}")
            self._log(f"   → Outcome: {outcome}")
            self._log(f"   → Our copy: {our_size} shares = ${our_value}")
            
            # Execute
            self.execute_trade(trade, our_size, our_value)
        
        self._save_state()
        return new_count
    
    def run(self):
        """Main loop"""
        self._log("=" * 60)
        self._log("🐋 POLYMARKET WHALE COPIER STARTING")
        self._log(f"🎯 Target: {self.target[:10]}...{self.target[-6:]}")
        self._log(f"📊 Copy: {self.copy_pct*100:.0f}% | Limits: ${self.min_usd}-${self.max_usd}")
        self._log(f"🧪 Dry run: {self.dry_run}")
        
        balance = self.get_balance()
        self._log(f"💵 Balance: ${balance:.2f} USDC")
        
        cycle = 0
        while True:
            cycle += 1
            self._log(f"\n🔄 Cycle #{cycle}")
            
            try:
                new = self.process_trades()
                self._log(f"📊 Processed {new} new trades")
            except Exception as e:
                self._log(f"❌ Error: {e}")
            
            self._log(f"⏱️ Waiting {self.interval}s...")
            time.sleep(self.interval)


def main():
    parser = argparse.ArgumentParser(description="Copy trade Polymarket whales")
    parser.add_argument("--target", help="Target wallet address")
    parser.add_argument("--percent", type=float, help="Copy percentage (1-100)")
    parser.add_argument("--min", type=float, help="Minimum trade USD")
    parser.add_argument("--max", type=float, help="Maximum trade USD")
    parser.add_argument("--live", action="store_true", help="Enable live trading")
    parser.add_argument("--interval", type=int, help="Check interval seconds")
    args = parser.parse_args()
    
    # Load config
    config = DEFAULT_CONFIG.copy()
    if CONFIG_FILE.exists():
        config.update(json.loads(CONFIG_FILE.read_text()))
    
    # Override with args
    if args.target:
        config["target_wallet"] = args.target
    if args.percent:
        config["copy_percent"] = args.percent
    if args.min:
        config["min_trade_usd"] = args.min
    if args.max:
        config["max_trade_usd"] = args.max
    if args.live:
        config["dry_run"] = False
    if args.interval:
        config["check_interval_sec"] = args.interval
    
    # Validate
    if not config["target_wallet"]:
        print("❌ No target wallet specified. Use --target or config.json")
        sys.exit(1)
    
    # Run
    copier = WhaleCopier(config)
    try:
        copier.run()
    except KeyboardInterrupt:
        print("\n👋 Stopped")


if __name__ == "__main__":
    main()
