#!/usr/bin/env python3
"""
Wallet Analyzer - Analyze wallet history for MEV attacks and risks

This script fetches recent transactions for a wallet address and performs:
1. Sandwich attack detection on past transactions
2. MEV risk scoring for the most recent activity
3. Frontrunning analysis for the most recent contract interaction
"""

import json
import sys
import os
import requests
from typing import Dict, List, Any
import argparse

# Import existing tools
# Assumes this script is in the same directory as other scripts
try:
    from sandwich_detector import analyze_sandwich_pattern, get_block_transactions, get_transaction_details
    from mev_risk_scorer import calculate_mev_risk_score, calculate_liquidity_risk, calculate_gas_competition_risk, calculate_historical_mev_risk, calculate_time_of_day_risk
    from frontrun_analyzer import analyze_nft_mint_frontrun
except ImportError:
    # Handle running from root directory
    sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))
    from sandwich_detector import analyze_sandwich_pattern, get_block_transactions, get_transaction_details
    from mev_risk_scorer import calculate_mev_risk_score, calculate_liquidity_risk, calculate_gas_competition_risk, calculate_historical_mev_risk, calculate_time_of_day_risk
    from frontrun_analyzer import analyze_nft_mint_frontrun

# API Configuration
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY", "")
ALCHEMY_API_KEY = os.getenv("ALCHEMY_API_KEY", "")

# Chain configurations
CHAIN_CONFIGS = {
    "ethereum": {
        "alchemy_url": f"https://eth-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}",
        "etherscan_url": "https://api.etherscan.io/api", # Keep just in case? Or remove if unused
        "etherscan_key": ETHERSCAN_API_KEY
    },
    "polygon": {
        "alchemy_url": f"https://polygon-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}",
        "etherscan_url": "https://api.polygonscan.com/api",
        "etherscan_key": ETHERSCAN_API_KEY
    }
}

def get_wallet_history(address: str, chain: str, limit: int = 5) -> List[Dict]:
    """
    Fetch recent outgoing transactions for a wallet using Alchemy
    """
    config = CHAIN_CONFIGS.get(chain, CHAIN_CONFIGS["ethereum"])
    
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "alchemy_getAssetTransfers",
            "params": [{
                "fromBlock": "0x0",
                "fromAddress": address,
                "category": ["external", "erc20", "erc721", "erc1155"],
                "withMetadata": False,
                "excludeZeroValue": False,
                "maxCount": hex(limit),
                "order": "desc"
            }]
        }
        
        response = requests.post(config["alchemy_url"], json=payload, timeout=10)
        data = response.json()
        
        if data.get("result") and data["result"].get("transfers"):
            # Normalize to match expected format (list of dicts with 'hash')
            return [{"hash": tx["hash"], "value": tx.get("value", 0)} for tx in data["result"]["transfers"]]
        else:
            print(f"Error fetching history or no transfers: {data.get('error')}", file=sys.stderr)
            return []
            
    except Exception as e:
        print(f"Error fetching wallet history: {e}", file=sys.stderr)
        return []

def analyze_wallet(address: str, chain: str = "ethereum", limit: int = 5):
    """
    Analyze wallet activity
    """
    print(f"Analyzing wallet: {address} on {chain}...")
    
    # 1. Fetch History
    transactions = get_wallet_history(address, chain, limit)
    
    if not transactions:
        print("No transactions found or error fetching history.")
        return

    print(f"Found {len(transactions)} recent transactions. analyzing for MEV...")
    
    analysis_results = {
        "wallet": address,
        "chain": chain,
        "sandwich_attacks_detected": 0,
        "total_analyzed": 0,
        "attacks": [],
        "risk_assessment": None
    }

    # 2. Analyze for Sandwich Attacks
    for tx in transactions:
        tx_hash = tx.get("hash")
        print(f"Checking potential sandwich: {tx_hash[:10]}...")
        
        # Get full tx details (needed for 'value' format consistency etc)
        tx_details = get_transaction_details(tx_hash, chain)
        if not tx_details:
            continue
            
        block_number = int(tx_details.get("blockNumber", "0x0"), 16)
        block_txs = get_block_transactions(block_number, chain)
        
        if block_txs:
            sandwich_result = analyze_sandwich_pattern(tx_details, block_txs, chain)
            if sandwich_result.get("is_sandwiched"):
                analysis_results["sandwich_attacks_detected"] += 1
                analysis_results["attacks"].append({
                    "tx_hash": tx_hash,
                    "loss_eth": sandwich_result.get("victim_loss_eth"),
                    "bot": sandwich_result.get("mev_bot_address")
                })
        
        analysis_results["total_analyzed"] += 1

    # 3. Risk Score & Frontrunning (based on most recent tx)
    if transactions:
        latest_tx_summary = transactions[0]
        print(f"Fetching full details for latest tx: {latest_tx_summary.get('hash')[:10]}...")
        latest_tx = get_transaction_details(latest_tx_summary.get("hash"), chain)
        
        if latest_tx:
            print("Calculating risk score for most recent activity...")
            
            # Convert values for scorer
            tx_value_wei = int(latest_tx.get("value", "0"), 16) if isinstance(latest_tx.get("value"), str) else latest_tx.get("value", 0)
            tx_value_eth = tx_value_wei / 1e18
            
            liquidity_risk = calculate_liquidity_risk(tx_value_eth)
            # Assume gas price from tx or default
            gas_price_hex = latest_tx.get("gasPrice", "0x0")
            gas_price_wei = int(gas_price_hex, 16) if isinstance(gas_price_hex, str) else 0
            gas_price_gwei = gas_price_wei / 1e9
            
            gas_risk = calculate_gas_competition_risk(gas_price_gwei)
            history_risk = calculate_historical_mev_risk(latest_tx.get("to"))
            time_risk = calculate_time_of_day_risk()
            
            overall_score = int(
                liquidity_risk * 0.35 +
                gas_risk * 0.25 +
                history_risk * 0.30 +
                time_risk * 0.10
            )
            
            # 4. Frontrunning Analysis
            print("Analyzing frontrunning risk...")
            contract_address = latest_tx.get("to")
            frontrun_result = None
            
            if contract_address:
                # Use gas price from tx or default to 30 gwei
                # Analyze using generic/NFT frontrun analyzer
                fr_analysis = analyze_nft_mint_frontrun(contract_address, gas_price_wei, chain)
                
                frontrun_result = {
                    "risk_level": fr_analysis.get("frontrun_risk"),
                    "risk_score": fr_analysis.get("risk_score"),
                    "estimated_success_prob": fr_analysis.get("estimated_success_probability"),
                    "recommendation": f"Recommended Gas: {fr_analysis.get('recommended_gas_price_gwei')} gwei"
                }

            analysis_results["risk_assessment"] = {
                "latest_tx_hash": latest_tx.get("hash"),
                "mev_risk_score": overall_score,
                "frontrun_risk_score": frontrun_result.get("risk_score") if frontrun_result else 0,
                "risk_factors": {
                    "liquidity_risk": liquidity_risk,
                    "gas_risk": gas_risk,
                    "contract_risk": history_risk
                },
                "frontrun_analysis": frontrun_result
            }
        else:
            print("Failed to fetch full details for latest transaction")

    # Output Results
    print(json.dumps(analysis_results, indent=2))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wallet MEV Analyzer")
    parser.add_argument("address", help="Wallet address to analyze")
    parser.add_argument("--chain", default="ethereum", help="Blockchain network")
    parser.add_argument("--limit", type=int, default=10, help="Number of transactions to analyze")
    
    args = parser.parse_args()
    
    analyze_wallet(args.address, args.chain, args.limit)
