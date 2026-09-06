#!/usr/bin/env python3
"""
Flashbots Relay - Submit transactions via Flashbots Protect

This script submits transactions through Flashbots to avoid MEV attacks
by bypassing the public mempool.
"""

import json
import sys
import os
from typing import Dict, Any
import requests
from eth_account import Account
from eth_account.messages import encode_defunct
from web3 import Web3

# API Configuration
FLASHBOTS_RELAY_URL = os.getenv("FLASHBOTS_RELAY_URL", "https://relay.flashbots.net")
PRIVATE_KEY = os.getenv("PRIVATE_KEY", "")
ALCHEMY_API_KEY = os.getenv("ALCHEMY_API_KEY", "")

# Chain configurations
CHAIN_CONFIGS = {
    "ethereum": {
        "chain_id": 1,
        "rpc_url": f"https://eth-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}",
        "flashbots_relay": "https://relay.flashbots.net"
    }
}


def sign_flashbots_bundle(bundle_data: Dict, private_key: str) -> str:
    """
    Sign Flashbots bundle with private key
    
    Args:
        bundle_data: Bundle data to sign
        private_key: Signer private key
        
    Returns:
        Signature
    """
    try:
        account = Account.from_key(private_key)
        message = encode_defunct(text=json.dumps(bundle_data))
        signed_message = account.sign_message(message)
        return signed_message.signature.hex()
    except Exception as e:
        raise Exception(f"Failed to sign bundle: {str(e)}")


def submit_flashbots_bundle(
    tx_data: Dict,
    max_priority_fee: int,
    chain: str
) -> Dict[str, Any]:
    """
    Submit transaction bundle to Flashbots
    
    Args:
        tx_data: Transaction data
        max_priority_fee: Maximum priority fee in wei
        chain: Blockchain network
        
    Returns:
        Submission result
    """
    if not PRIVATE_KEY:
        return {
            "success": False,
            "error": "PRIVATE_KEY environment variable not set"
        }
    
    config = CHAIN_CONFIGS.get(chain)
    if not config:
        return {
            "success": False,
            "error": f"Flashbots not supported on {chain}"
        }
    
    try:
        # Initialize Web3
        w3 = Web3(Web3.HTTPProvider(config["rpc_url"]))
        
        # Get current block number
        current_block = w3.eth.block_number
        target_block = current_block + 1
        
        # Build transaction
        account = Account.from_key(PRIVATE_KEY)
        
        # Get nonce
        nonce = w3.eth.get_transaction_count(account.address)
        
        # Get gas price
        gas_price = w3.eth.gas_price
        
        # Build transaction dict
        transaction = {
            "from": account.address,
            "to": tx_data.get("to"),
            "value": int(tx_data.get("value", "0x0"), 16) if isinstance(tx_data.get("value"), str) else tx_data.get("value", 0),
            "gas": int(tx_data.get("gas", "0x30000"), 16) if isinstance(tx_data.get("gas"), str) else tx_data.get("gas", 200000),
            "maxFeePerGas": gas_price + max_priority_fee,
            "maxPriorityFeePerGas": max_priority_fee,
            "nonce": nonce,
            "chainId": config["chain_id"],
            "data": tx_data.get("data", "0x")
        }
        
        # Sign transaction
        signed_tx = account.sign_transaction(transaction)
        
        # Create bundle
        bundle = [
            {
                "signed_transaction": signed_tx.rawTransaction.hex()
            }
        ]
        
        # Prepare Flashbots request
        flashbots_params = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "eth_sendBundle",
            "params": [
                {
                    "txs": [tx["signed_transaction"] for tx in bundle],
                    "blockNumber": hex(target_block),
                    "minTimestamp": 0,
                    "maxTimestamp": 0
                }
            ]
        }
        
        # Sign the request
        signature = sign_flashbots_bundle(flashbots_params["params"][0], PRIVATE_KEY)
        
        # Submit to Flashbots
        headers = {
            "Content-Type": "application/json",
            "X-Flashbots-Signature": f"{account.address}:{signature}"
        }
        
        response = requests.post(
            config["flashbots_relay"],
            json=flashbots_params,
            headers=headers,
            timeout=30
        )
        
        result = response.json()
        
        if "error" in result:
            return {
                "success": False,
                "error": result["error"].get("message", "Flashbots submission failed")
            }
        
        return {
            "success": True,
            "bundle_hash": result.get("result", {}).get("bundleHash", "pending"),
            "target_block": target_block,
            "status": "submitted",
            "message": "Transaction submitted via Flashbots Protect",
            "protection_enabled": True,
            "no_revert_protection": True,
            "tx_hash": signed_tx.hash.hex()
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Flashbots submission error: {str(e)}"
        }


def submit_via_flashbots_rpc(
    tx_data: Dict,
    max_priority_fee: int,
    chain: str
) -> Dict[str, Any]:
    """
    Submit transaction via Flashbots Protect RPC (simpler method)
    
    Args:
        tx_data: Transaction data
        max_priority_fee: Maximum priority fee
        chain: Blockchain network
        
    Returns:
        Submission result
    """
    if not PRIVATE_KEY:
        return {
            "success": False,
            "error": "PRIVATE_KEY environment variable not set",
            "recommendation": "Set PRIVATE_KEY to use Flashbots protection"
        }
    
    # Flashbots Protect RPC endpoint
    flashbots_rpc = "https://rpc.flashbots.net"
    
    try:
        # Initialize Web3 with Flashbots RPC
        w3 = Web3(Web3.HTTPProvider(flashbots_rpc))
        
        account = Account.from_key(PRIVATE_KEY)
        nonce = w3.eth.get_transaction_count(account.address)
        
        # Build transaction
        transaction = {
            "from": account.address,
            "to": tx_data.get("to"),
            "value": int(tx_data.get("value", "0x0"), 16) if isinstance(tx_data.get("value"), str) else tx_data.get("value", 0),
            "gas": int(tx_data.get("gas", "0x30000"), 16) if isinstance(tx_data.get("gas"), str) else tx_data.get("gas", 200000),
            "maxPriorityFeePerGas": max_priority_fee,
            "nonce": nonce,
            "chainId": 1,
            "data": tx_data.get("data", "0x")
        }
        
        # Estimate gas
        try:
            gas_estimate = w3.eth.estimate_gas(transaction)
            transaction["gas"] = gas_estimate
        except:
            pass  # Use provided gas
        
        # Get max fee
        base_fee = w3.eth.get_block("latest")["baseFeePerGas"]
        transaction["maxFeePerGas"] = base_fee * 2 + max_priority_fee
        
        # Sign and send
        signed_tx = account.sign_transaction(transaction)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        return {
            "success": True,
            "tx_hash": tx_hash.hex(),
            "status": "submitted",
            "message": "Transaction submitted via Flashbots Protect RPC",
            "protection_enabled": True,
            "no_revert_protection": True
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Flashbots RPC error: {str(e)}"
        }


def main():
    """Main execution function"""
    try:
        # Read input from stdin
        input_data = json.loads(sys.stdin.read())
        
        tx_data = input_data.get("tx_data", {})
        max_priority_fee = input_data.get("max_priority_fee", 2000000000)  # 2 gwei
        chain = input_data.get("chain", "ethereum")
        
        # Validate input
        if not tx_data:
            print(json.dumps({
                "error": "Missing tx_data parameter",
                "success": False
            }))
            sys.exit(1)
        
        if chain != "ethereum":
            print(json.dumps({
                "error": f"Flashbots only supported on Ethereum mainnet, not {chain}",
                "success": False,
                "recommendation": "Use Ethereum mainnet or submit transaction normally"
            }))
            sys.exit(1)
        
        # Try Flashbots Protect RPC (simpler method)
        result = submit_via_flashbots_rpc(tx_data, max_priority_fee, chain)
        
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
