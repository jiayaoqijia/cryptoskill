#!/usr/bin/env python3
"""
MEV Risk Scorer - Calculate comprehensive MEV risk score

This script calculates an overall MEV risk score based on multiple factors
including liquidity, gas competition, historical MEV activity, and timing.
"""

import json
import sys
import os
from typing import Dict, Any
from datetime import datetime
import requests

# API Configuration
ALCHEMY_API_KEY = os.getenv("ALCHEMY_API_KEY", "")

# Chain configurations
CHAIN_CONFIGS = {
    "ethereum": {
        "alchemy_url": f"https://eth-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}"
    },
    "polygon": {
        "alchemy_url": f"https://polygon-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}"
    }
}


def calculate_liquidity_risk(tx_value: float, pool_liquidity: float = None) -> int:
    """
    Calculate risk based on transaction size vs liquidity
    
    Args:
        tx_value: Transaction value in ETH
        pool_liquidity: Pool liquidity in USD (optional)
        
    Returns:
        Risk score (0-100)
    """
    if pool_liquidity is None:
        # Estimate based on transaction size
        if tx_value > 100:
            return 90
        elif tx_value > 50:
            return 75
        elif tx_value > 10:
            return 50
        elif tx_value > 1:
            return 25
        else:
            return 10
    
    # Calculate ratio
    tx_value_usd = tx_value * 3750  # Assume $3750 ETH
    ratio = tx_value_usd / pool_liquidity
    
    if ratio > 0.05:  # >5% of pool
        return 95
    elif ratio > 0.02:  # >2% of pool
        return 75
    elif ratio > 0.01:  # >1% of pool
        return 50
    elif ratio > 0.005:  # >0.5% of pool
        return 30
    else:
        return 15


def calculate_gas_competition_risk(current_gas_price: float) -> int:
    """
    Calculate risk based on current gas prices
    
    Args:
        current_gas_price: Current gas price in gwei
        
    Returns:
        Risk score (0-100)
    """
    if current_gas_price > 100:
        return 90
    elif current_gas_price > 50:
        return 70
    elif current_gas_price > 30:
        return 50
    elif current_gas_price > 20:
        return 30
    else:
        return 15


def calculate_historical_mev_risk(contract_address: str = None) -> int:
    """
    Calculate risk based on historical MEV activity
    
    Args:
        contract_address: Target contract address
        
    Returns:
        Risk score (0-100)
    """
    # In production, query historical MEV data
    # For now, use heuristics based on contract type
    
    if not contract_address:
        return 40
    
    # Common DEX routers have high MEV activity
    known_high_mev_contracts = [
        "0x7a250d5630b4cf539739df2c5dacb4c659f2488d",  # Uniswap V2 Router
        "0xe592427a0aece92de3edee1f18e0157c05861564",  # Uniswap V3 Router
        "0xdef1c0ded9bec7f1a1670819833240f027b25eff",  # 0x Exchange Proxy
    ]
    
    if contract_address.lower() in known_high_mev_contracts:
        return 80
    else:
        return 40


def calculate_time_of_day_risk() -> int:
    """
    Calculate risk based on time of day (UTC)
    
    Returns:
        Risk score (0-100)
    """
    current_hour = datetime.utcnow().hour
    
    # Peak hours (12:00-20:00 UTC) have higher MEV activity
    if 12 <= current_hour < 20:
        return 60
    # Off-peak hours
    elif 0 <= current_hour < 6:
        return 25
    else:
        return 40


def get_current_gas_price(chain: str) -> float:
    """
    Get current gas price
    
    Args:
        chain: Blockchain network
        
    Returns:
        Gas price in gwei
    """
    config = CHAIN_CONFIGS.get(chain, CHAIN_CONFIGS["ethereum"])
    
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "eth_gasPrice",
            "params": []
        }
        
        response = requests.post(config["alchemy_url"], json=payload, timeout=5)
        data = response.json()
        
        gas_price_wei = int(data.get("result", "0x0"), 16)
        return gas_price_wei / 1e9
        
    except Exception as e:
        print(f"Error fetching gas price: {e}", file=sys.stderr)
        return 30.0  # Default


def calculate_mev_risk_score(
    liquidity_risk: int,
    gas_competition_risk: int,
    historical_mev_risk: int,
    time_of_day_risk: int
) -> Dict[str, Any]:
    """
    Calculate overall MEV risk score from components
    """
    # Calculate weighted overall risk score
    overall_risk_score = int(
        liquidity_risk * 0.35 +
        gas_competition_risk * 0.25 +
        historical_mev_risk * 0.30 +
        time_of_day_risk * 0.10
    )
    
    # Determine risk level
    if overall_risk_score >= 70:
        risk_level = "HIGH"
        explanation = "High MEV risk due to large transaction size and high network activity"
    elif overall_risk_score >= 40:
        risk_level = "MEDIUM"
        explanation = "Medium MEV risk - consider using Flashbots for protection"
    else:
        risk_level = "LOW"
        explanation = "Low MEV risk - transaction appears safe to submit normally"
        
    return {
        "overall_risk_score": overall_risk_score,
        "risk_level": risk_level,
        "explanation": explanation
    }

def main():
    """Main execution function"""
    try:
        # Read input from stdin
        input_data = json.loads(sys.stdin.read())
        
        tx_data = input_data.get("tx_data", {})
        chain = input_data.get("chain", "ethereum")
        current_gas_price = input_data.get("current_gas_price")
        
        # Extract transaction value
        tx_value = tx_data.get("value", "0x0")
        if isinstance(tx_value, str):
            tx_value = int(tx_value, 16) / 1e18
        else:
            tx_value = tx_value / 1e18 if tx_value > 0 else 0
        
        # Get current gas price if not provided
        if current_gas_price is None:
            current_gas_price = get_current_gas_price(chain)
        else:
            current_gas_price = current_gas_price / 1e9  # Convert to gwei
        
        # Calculate individual risk factors
        liquidity_risk = calculate_liquidity_risk(tx_value)
        gas_competition_risk = calculate_gas_competition_risk(current_gas_price)
        historical_mev_risk = calculate_historical_mev_risk(tx_data.get("to"))
        time_of_day_risk = calculate_time_of_day_risk()
        
        # Calculate overall score
        risk_result = calculate_mev_risk_score(
            liquidity_risk,
            gas_competition_risk,
            historical_mev_risk,
            time_of_day_risk
        )
        
        # Build result
        result = {
            "success": True,
            **risk_result,
            "risk_factors": {
                "liquidity_risk": liquidity_risk,
                "gas_competition": gas_competition_risk,
                "historical_mev": historical_mev_risk,
                "time_of_day": time_of_day_risk
            },
            "current_gas_price_gwei": round(current_gas_price, 2),
            "transaction_value_eth": round(tx_value, 4)
        }
        
        print(json.dumps(result, indent=2))
        
    except json.JSONDecodeError:
        print(json.dumps({
            "error": "Invalid JSON input",
            "success": False
        }))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({
            "error": f"Unexpected error: {str(e)}",
            "success": False
        }))
        sys.exit(1)

if __name__ == "__main__":
    main()
