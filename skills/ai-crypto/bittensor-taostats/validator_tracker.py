#!/usr/bin/env python3
"""
Validator Performance Tracker
Monitor validator performance changes over 24 hours
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from taostats_client import TaostatsAPI

# Key subnets to monitor
SUBNETS = [33, 1, 13, 12, 0]

def get_validator_performance(netuid: int):
    """Get validator yield data for subnet"""
    api = TaostatsAPI(open(Path.home() / ".openclaw/workspace/.taostats").read().split("=")[1].strip())
    
    try:
        result = api.get_json(f"dtao/validator/yield/latest/v1?netuid={netuid}")
        validators = result.get('data', [])
        
        if not validators:
            return None
        
        # Sort by 7-day APY
        validators.sort(key=lambda x: float(x.get('seven_day_apy', 0)), reverse=True)
        
        return validators[:5]  # Top 5
    except Exception as e:
        print(f"Error fetching SN{netuid}: {e}")
        return None

def main():
    print("=" * 70)
    print("VALIDATOR PERFORMANCE TRACKER")
    print("=" * 70)
    print(f"Time: {datetime.now().isoformat()}")
    print()
    
    for netuid in SUBNETS:
        validators = get_validator_performance(netuid)
        
        if validators:
            print(f"\nSN{netuid} - Top Validators by 7-Day APY:")
            print("-" * 70)
            print(f"{'Rank':<5} {'Name':<25} {'7D APY':<10} {'1D APY':<10} {'Commission':<10}")
            print("-" * 70)
            
            for i, v in enumerate(validators[:5], 1):
                name = v.get('name', v.get('hotkey', {}).get('ss58', 'Unknown')[:20])
                name = name[:24] if name else "Unknown"
                apy_7d = float(v.get('seven_day_apy', 0)) * 100
                apy_1d = float(v.get('one_day_apy', 0)) * 100
                take = float(v.get('take', 0)) * 100
                
                print(f"{i:<5} {name:<25} {apy_7d:>9.2f}% {apy_1d:>9.2f}% {take:>9.2f}%")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
