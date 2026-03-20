#!/usr/bin/env python3
"""
Historical Balance Tracker
Track daily portfolio balance changes via TaoStats API
"""

import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common.config import COLDKEY, RAO_TO_TAO, get_taostats_client

def get_api():
    """Initialize API client"""
    return get_taostats_client()

def get_daily_balances(days: int = 30):
    """
    Get daily balance history for portfolio tracking
    
    Args:
        days: Number of days to look back
        
    Returns:
        List of daily balance records
    """
    api = get_api()
    
    # Calculate timestamps
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    start_timestamp = int(start_date.timestamp())
    end_timestamp = int(end_date.timestamp())
    
    print(f"Fetching balance history from {start_date.date()} to {end_date.date()}...")
    
    try:
        history = api.get_balance_history(COLDKEY, start_timestamp, end_timestamp)
        
        print(f"\n📊 Portfolio History ({len(history)} records):")
        print("-" * 80)
        print(f"{'Date':<12} {'Free τ':>12} {'Staked τ':>12} {'Total τ':>12} {'Daily Δ':>10}")
        print("-" * 80)
        
        prev_total = 0
        for record in history:
            date = record.get('timestamp', '')[:10]
            free = float(record.get('balance_free', 0)) / RAO_TO_TAO
            staked = float(record.get('balance_staked', 0)) / RAO_TO_TAO
            total = float(record.get('balance_total', 0)) / RAO_TO_TAO
            
            delta = ""
            if prev_total > 0:
                change = total - prev_total
                delta = f"{change:+.4f}"
            
            print(f"{date:<12} {free:>12.4f} {staked:>12.4f} {total:>12.4f} {delta:>10}")
            prev_total = total
        
        print("-" * 80)
        
        if history:
            first = history[0]
            last = history[-1]
            first_total = float(first.get('balance_total', 0)) / RAO_TO_TAO
            last_total = float(last.get('balance_total', 0)) / RAO_TO_TAO
            overall_change = last_total - first_total
            pct_change = (overall_change / first_total * 100) if first_total > 0 else 0
            
            print(f"\nOverall Change: {overall_change:+.4f} τ ({pct_change:+.2f}%)")
        
        return history
        
    except Exception as e:
        print(f"Error: {e}")
        return []

def export_to_csv(history: list, filename: str = None):
    """Export balance history to CSV"""
    if not filename:
        date_str = datetime.now().strftime("%Y%m%d")
        filename = f"portfolio_history_{date_str}.csv"
    
    filepath = Path("~/.openclaw/workspace/data").expanduser() / filename
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, 'w') as f:
        f.write("date,free_tao,staked_tao,total_tao,total_delta\n")
        
        prev_total = 0
        for record in history:
            date = record.get('timestamp', '')[:10]
            free = float(record.get('balance_free', 0)) / RAO_TO_TAO
            staked = float(record.get('balance_staked', 0)) / RAO_TO_TAO
            total = float(record.get('balance_total', 0)) / RAO_TO_TAO
            
            delta = total - prev_total if prev_total > 0 else 0
            
            f.write(f"{date},{free:.6f},{staked:.6f},{total:.6f},{delta:.6f}\n")
            prev_total = total
    
    print(f"\n✅ Exported to: {filepath}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Track historical portfolio balances")
    parser.add_argument("--days", type=int, default=30, help="Number of days to track")
    parser.add_argument("--export", action="store_true", help="Export to CSV")
    
    args = parser.parse_args()
    
    history = get_daily_balances(args.days)
    
    if args.export and history:
        export_to_csv(history)
