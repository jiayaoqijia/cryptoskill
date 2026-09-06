#!/usr/bin/env python3
"""
Sandwich Attack Detector - Analyze transactions for sandwich attack patterns

This script detects sandwich attacks by analyzing transaction sequences,
identifying frontrun/backrun patterns, and calculating victim losses.
"""

import json
import sys
import os
from typing import Dict, List, Any, Optional
import requests
from datetime import datetime

# API Configuration
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY", "")
ALCHEMY_API_KEY = os.getenv("ALCHEMY_API_KEY", "")

# Chain configurations
CHAIN_CONFIGS = {
    "ethereum": {
        "chain_id": 1,
        "alchemy_url": f"https://eth-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}",
        "etherscan_url": "https://api.etherscan.io/api",
        "etherscan_key": ETHERSCAN_API_KEY
    },
    "polygon": {
        "chain_id": 137,
        "alchemy_url": f"https://polygon-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}",
        "etherscan_url": "https://api.polygonscan.com/api",
        "etherscan_key": ETHERSCAN_API_KEY
    }
}

# Known MEV bot addresses (sample list)
KNOWN_MEV_BOTS = [
    "0xa57Bd00134B2850B2a1c55860c9e9ea100fDd6CF",  # MEV Bot 1
    "0x000000000035B5e5ad9019092C665357240f594e",  # MEV Bot 2
    "0x00000000003b3cc22aF3aE1EAc0440BcEe416B40",  # MEV Bot 3
]


def get_transaction_details(tx_hash: str, chain: str) -> Optional[Dict]:
    """
    Fetch transaction details from Alchemy (JSON-RPC)
    
    Args:
        tx_hash: Transaction hash
        chain: Blockchain network
        
    Returns:
        Transaction details or None
    """
    config = CHAIN_CONFIGS.get(chain, CHAIN_CONFIGS["ethereum"])
    
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "eth_getTransactionByHash",
            "params": [tx_hash]
        }
        
        response = requests.post(config["alchemy_url"], json=payload, timeout=10)
        data = response.json()
        
        # Check if result exists and is not None (Alchemy returns None for not found)
        if data.get("result"):
            return data["result"]
        return None
        
    except Exception as e:
        print(f"Error fetching transaction: {e}", file=sys.stderr)
        return None


def get_transaction_receipt(tx_hash: str, chain: str) -> Optional[Dict]:
    """
    Fetch transaction receipt from Alchemy (JSON-RPC)
    
    Args:
        tx_hash: Transaction hash
        chain: Blockchain network
        
    Returns:
        Transaction receipt or None
    """
    config = CHAIN_CONFIGS.get(chain, CHAIN_CONFIGS["ethereum"])
    
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "eth_getTransactionReceipt",
            "params": [tx_hash]
        }
        
        response = requests.post(config["alchemy_url"], json=payload, timeout=10)
        data = response.json()
        
        if data.get("result"):
            return data["result"]
        return None
        
    except Exception as e:
        print(f"Error fetching receipt: {e}", file=sys.stderr)
        return None


def get_block_transactions(block_number: int, chain: str) -> List[Dict]:
    """
    Get all transactions in a block
    
    Args:
        block_number: Block number
        chain: Blockchain network
        
    Returns:
        List of transactions
    """
    config = CHAIN_CONFIGS.get(chain, CHAIN_CONFIGS["ethereum"])
    
    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "eth_getBlockByNumber",
            "params": [hex(block_number), True]
        }
        
        response = requests.post(config["alchemy_url"], json=payload, timeout=10)
        data = response.json()
        
        if data.get("result"):
            return data["result"].get("transactions", [])
        return []
        
    except Exception as e:
        print(f"Error fetching block: {e}", file=sys.stderr)
        return []


def analyze_sandwich_pattern(
    victim_tx: Dict,
    block_txs: List[Dict],
    chain: str
) -> Dict[str, Any]:
    """
    Analyze transaction for sandwich attack pattern
    
    Args:
        victim_tx: Victim transaction
        block_txs: All transactions in the block
        chain: Blockchain network
        
    Returns:
        Sandwich analysis result
    """
    victim_index = None
    victim_to = victim_tx.get("to", "").lower()
    
    # Find victim transaction index in block
    for i, tx in enumerate(block_txs):
        if tx.get("hash", "").lower() == victim_tx.get("hash", "").lower():
            victim_index = i
            break
    
    if victim_index is None:
        return {
            "is_sandwiched": False,
            "confidence": 0.0,
            "reason": "Transaction not found in block"
        }
    
    # Look for frontrun (transaction before victim)
    frontrun_tx = None
    if victim_index > 0:
        prev_tx = block_txs[victim_index - 1]
        # Check if previous tx targets same contract
        if prev_tx.get("to", "").lower() == victim_to:
            frontrun_tx = prev_tx
    
    # Look for backrun (transaction after victim)
    backrun_tx = None
    if victim_index < len(block_txs) - 1:
        next_tx = block_txs[victim_index + 1]
        # Check if next tx targets same contract
        if next_tx.get("to", "").lower() == victim_to:
            backrun_tx = next_tx
    
    # Analyze pattern
    is_sandwiched = False
    confidence = 0.0
    mev_bot_address = None
    
    if frontrun_tx and backrun_tx:
        # Check if frontrun and backrun are from same address
        frontrun_from = frontrun_tx.get("from", "").lower()
        backrun_from = backrun_tx.get("from", "").lower()
        
        if frontrun_from == backrun_from:
            is_sandwiched = True
            confidence = 0.85
            mev_bot_address = frontrun_from
            
            # Increase confidence if known MEV bot
            if frontrun_from in [addr.lower() for addr in KNOWN_MEV_BOTS]:
                confidence = 0.95
    
    # Calculate estimated losses (simplified)
    victim_value = int(victim_tx.get("value", "0x0"), 16) / 1e18
    estimated_loss = victim_value * 0.02  # Assume 2% loss
    bot_profit = estimated_loss * 0.95  # Bot keeps 95% after gas
    
    return {
        "is_sandwiched": is_sandwiched,
        "confidence": confidence,
        "frontrun_tx": frontrun_tx.get("hash") if frontrun_tx else None,
        "backrun_tx": backrun_tx.get("hash") if backrun_tx else None,
        "mev_bot_address": mev_bot_address,
        "victim_loss_eth": round(estimated_loss, 6),
        "victim_loss_usd": round(estimated_loss * 3750, 2),
        "bot_profit_eth": round(bot_profit, 6),
        "bot_profit_usd": round(bot_profit * 3750, 2),
        "pattern_details": {
            "same_pool": frontrun_tx and backrun_tx and (frontrun_tx.get("to") == backrun_tx.get("to")),
            "same_block": True,
            "sequential_positions": frontrun_tx and backrun_tx,
            "known_mev_bot": mev_bot_address in [addr.lower() for addr in KNOWN_MEV_BOTS] if mev_bot_address else False
        }
    }


def main():
    """Main execution function"""
    try:
        # Read input from stdin
        input_data = json.loads(sys.stdin.read())
        
        tx_hash = input_data.get("tx_hash")
        chain = input_data.get("chain", "ethereum")
        
        # Validate input
        if not tx_hash:
            print(json.dumps({
                "error": "Missing tx_hash parameter",
                "success": False
            }))
            sys.exit(1)
        
        # Step 1: Get transaction details
        tx_details = get_transaction_details(tx_hash, chain)
        
        if not tx_details:
            print(json.dumps({
                "error": "Transaction not found",
                "success": False
            }))
            sys.exit(1)
        
        # Step 2: Get block transactions
        block_number = int(tx_details.get("blockNumber", "0x0"), 16)
        
        if block_number == 0:
            print(json.dumps({
                "error": "Transaction not yet mined",
                "success": False
            }))
            sys.exit(1)
        
        block_txs = get_block_transactions(block_number, chain)
        
        # Step 3: Analyze sandwich pattern
        analysis = analyze_sandwich_pattern(tx_details, block_txs, chain)
        
        # Add metadata
        result = {
            "success": True,
            "tx_hash": tx_hash,
            "block_number": block_number,
            "chain": chain,
            **analysis
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
