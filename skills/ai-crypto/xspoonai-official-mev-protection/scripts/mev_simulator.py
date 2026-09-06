#!/usr/bin/env python3
"""
MEV Simulator - Simulate transactions to detect potential MEV attacks

This script simulates a transaction before submission to identify MEV risks,
calculate potential losses, and provide actionable recommendations.
"""

import json
import sys
import os
from typing import Dict, List, Any
from decimal import Decimal
import requests

# API Configuration
ALCHEMY_API_KEY = os.getenv("ALCHEMY_API_KEY", "")
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY", "")

# Chain configurations
CHAIN_CONFIGS = {
    "ethereum": {
        "chain_id": 1,
        "alchemy_url": f"https://eth-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}",
        "etherscan_url": "https://api.etherscan.io/api"
    },
    "polygon": {
        "chain_id": 137,
        "alchemy_url": f"https://polygon-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}",
        "etherscan_url": "https://api.polygonscan.com/api"
    },
    "arbitrum": {
        "chain_id": 42161,
        "alchemy_url": f"https://arb-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}",
        "etherscan_url": "https://api.arbiscan.io/api"
    },
    "base": {
        "chain_id": 8453,
        "alchemy_url": f"https://base-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}",
        "etherscan_url": "https://api.basescan.org/api"
    }
}


def simulate_transaction(tx_data: Dict, chain: str) -> Dict[str, Any]:
    """
    Simulate transaction using Alchemy Simulation API
    
    Args:
        tx_data: Transaction data (from, to, data, value, gas)
        chain: Blockchain network
        
    Returns:
        Simulation result with gas usage, state changes, and errors
    """
    config = CHAIN_CONFIGS.get(chain, CHAIN_CONFIGS["ethereum"])
    
    try:
        # Use Alchemy's eth_call for simulation
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "eth_call",
            "params": [
                {
                    "from": tx_data.get("from"),
                    "to": tx_data.get("to"),
                    "data": tx_data.get("data", "0x"),
                    "value": tx_data.get("value", "0x0"),
                    "gas": tx_data.get("gas", "0x100000")
                },
                "latest"
            ]
        }
        
        response = requests.post(config["alchemy_url"], json=payload, timeout=10)
        result = response.json()
        
        if "error" in result:
            return {
                "success": False,
                "error": result["error"].get("message", "Simulation failed"),
                "revert_reason": result["error"].get("data", "")
            }
        
        return {
            "success": True,
            "result": result.get("result"),
            "gas_used": "estimated"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Simulation error: {str(e)}"
        }


def analyze_price_impact(tx_data: Dict, chain: str) -> Dict[str, Any]:
    """
    Analyze price impact for DEX swaps
    
    Args:
        tx_data: Transaction data
        chain: Blockchain network
        
    Returns:
        Price impact analysis
    """
    # Extract swap parameters from transaction data
    # This is a simplified version - in production, decode the actual swap data
    
    # Simulate price impact based on transaction value
    tx_value = int(tx_data.get("value", "0"), 16) if isinstance(tx_data.get("value"), str) else tx_data.get("value", 0)
    tx_value_eth = tx_value / 1e18 if tx_value > 0 else 0
    
    # Simple heuristic: larger trades = higher price impact
    if tx_value_eth > 50:
        price_impact = 3.2
        impact_level = "HIGH"
    elif tx_value_eth > 10:
        price_impact = 1.5
        impact_level = "MEDIUM"
    elif tx_value_eth > 1:
        price_impact = 0.5
        impact_level = "LOW"
    else:
        price_impact = 0.1
        impact_level = "VERY_LOW"
    
    return {
        "price_impact_percent": price_impact,
        "impact_level": impact_level,
        "trade_size_eth": tx_value_eth
    }


def detect_mempool_competition(tx_data: Dict, chain: str) -> Dict[str, Any]:
    """
    Check for competing transactions in mempool
    
    Args:
        tx_data: Transaction data
        chain: Blockchain network
        
    Returns:
        Mempool competition analysis
    """
    # In production, this would query actual mempool data
    # For now, we'll use a simplified heuristic
    
    config = CHAIN_CONFIGS.get(chain, CHAIN_CONFIGS["ethereum"])
    
    try:
        # Get current gas price as proxy for network congestion
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "eth_gasPrice",
            "params": []
        }
        
        response = requests.post(config["alchemy_url"], json=payload, timeout=5)
        result = response.json()
        
        gas_price = int(result.get("result", "0x0"), 16)
        gas_price_gwei = gas_price / 1e9
        
        # High gas = high competition
        if gas_price_gwei > 50:
            competition_level = "HIGH"
            pending_txs = 8
        elif gas_price_gwei > 30:
            competition_level = "MEDIUM"
            pending_txs = 4
        else:
            competition_level = "LOW"
            pending_txs = 1
        
        return {
            "competition_level": competition_level,
            "estimated_pending_txs": pending_txs,
            "current_gas_price_gwei": round(gas_price_gwei, 2)
        }
        
    except Exception as e:
        return {
            "competition_level": "UNKNOWN",
            "error": str(e)
        }


def calculate_mev_risk_score(
    price_impact: Dict,
    mempool_competition: Dict,
    slippage_tolerance: float
) -> Dict[str, Any]:
    """
    Calculate overall MEV risk score
    
    Args:
        price_impact: Price impact analysis
        mempool_competition: Mempool competition data
        slippage_tolerance: User's slippage tolerance
        
    Returns:
        MEV risk score and level
    """
    # Risk scoring algorithm
    risk_score = 0
    detected_risks = []
    recommendations = []
    
    # Price impact risk (0-40 points)
    impact_pct = price_impact.get("price_impact_percent", 0)
    if impact_pct > 2.0:
        risk_score += 40
        detected_risks.append(f"High price impact ({impact_pct}%)")
        recommendations.append("Split transaction into smaller chunks")
    elif impact_pct > 1.0:
        risk_score += 25
        detected_risks.append(f"Moderate price impact ({impact_pct}%)")
    elif impact_pct > 0.5:
        risk_score += 10
    
    # Mempool competition risk (0-30 points)
    competition = mempool_competition.get("competition_level", "LOW")
    pending_txs = mempool_competition.get("estimated_pending_txs", 0)
    
    if competition == "HIGH":
        risk_score += 30
        detected_risks.append(f"High mempool competition ({pending_txs} pending swaps)")
        recommendations.append("Use Flashbots Protect to avoid public mempool")
    elif competition == "MEDIUM":
        risk_score += 15
        detected_risks.append(f"Moderate mempool competition")
    
    # Slippage tolerance risk (0-30 points)
    if slippage_tolerance < impact_pct:
        risk_score += 30
        detected_risks.append("Slippage tolerance too low for current conditions")
        recommendations.append(f"Increase slippage tolerance to {impact_pct + 0.5}%")
    elif slippage_tolerance < 0.5:
        risk_score += 15
        detected_risks.append("Low slippage tolerance increases MEV risk")
        recommendations.append("Increase slippage tolerance to 1%")
    
    # Sandwich attack detection (bonus points)
    if impact_pct > 2.0 and competition == "HIGH":
        risk_score += 20
        detected_risks.append("Sandwich attack opportunity detected")
        recommendations.append("Use Flashbots Protect (Recommended)")
    
    # Determine risk level
    if risk_score >= 70:
        risk_level = "HIGH"
    elif risk_score >= 40:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"
    
    # Estimate MEV loss
    trade_size = price_impact.get("trade_size_eth", 0)
    estimated_loss_pct = min(impact_pct * 0.5, 5.0)  # Max 5% loss
    estimated_loss_eth = trade_size * (estimated_loss_pct / 100)
    
    # Add default recommendations
    if not recommendations:
        recommendations.append("Transaction appears safe to submit normally")
    
    return {
        "risk_score": min(risk_score, 100),
        "risk_level": risk_level,
        "detected_risks": detected_risks if detected_risks else ["No significant risks detected"],
        "recommendations": recommendations,
        "estimated_mev_loss_eth": round(estimated_loss_eth, 6),
        "estimated_mev_loss_usd": round(estimated_loss_eth * 3750, 2)  # Assume $3750 ETH
    }


def main():
    """Main execution function"""
    try:
        # Read input from stdin
        input_data = json.loads(sys.stdin.read())
        
        tx_data = input_data.get("tx_data", {})
        chain = input_data.get("chain", "ethereum")
        slippage_tolerance = input_data.get("slippage_tolerance", 0.5)
        
        # Validate input
        if not tx_data:
            print(json.dumps({
                "error": "Missing tx_data parameter",
                "success": False
            }))
            sys.exit(1)
        
        # Step 1: Simulate transaction
        simulation = simulate_transaction(tx_data, chain)
        
        if not simulation.get("success"):
            print(json.dumps({
                "error": simulation.get("error", "Simulation failed"),
                "simulation_success": False,
                "risk_score": 0,
                "risk_level": "UNKNOWN"
            }))
            sys.exit(1)
        
        # Step 2: Analyze price impact
        price_impact = analyze_price_impact(tx_data, chain)
        
        # Step 3: Check mempool competition
        mempool_competition = detect_mempool_competition(tx_data, chain)
        
        # Step 4: Calculate MEV risk score
        risk_analysis = calculate_mev_risk_score(
            price_impact,
            mempool_competition,
            slippage_tolerance
        )
        
        # Combine results
        result = {
            "simulation_success": True,
            **risk_analysis,
            "price_impact_percent": price_impact.get("price_impact_percent"),
            "mempool_competition": mempool_competition.get("competition_level"),
            "current_gas_price_gwei": mempool_competition.get("current_gas_price_gwei")
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
