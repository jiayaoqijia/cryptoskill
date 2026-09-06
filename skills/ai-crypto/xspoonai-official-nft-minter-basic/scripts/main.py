#!/usr/bin/env python3
"""NFT Minter Basic - Build Real ERC721 Mint Transactions from Blockchain"""
import json
import sys
import os
from datetime import datetime, timezone
from typing import Dict, Optional, Any
from eth_abi import encode as eth_encode

try:
    from web3 import Web3
    from eth_utils import is_checksum_address, keccak
except ImportError:
    Web3 = None

# RPC endpoint
RPC_URL = os.getenv("ETHEREUM_RPC", "https://eth-mainnet.public.blastapi.io")

# ERC721 ABI (minimal for mint operations)
ERC721_ABI = [
    {
        "inputs": [{"name": "tokenId", "type": "uint256"}],
        "name": "ownerOf",
        "outputs": [{"name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "totalSupply",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "name",
        "outputs": [{"name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function"
    }
]

def get_web3_client() -> Optional[Web3]:
    """Create and return Web3 client connected to RPC"""
    if Web3 is None:
        return None
    try:
        w3 = Web3(Web3.HTTPProvider(RPC_URL, request_kwargs={"timeout": 30}))
        if not w3.is_connected():
            return None
        return w3
    except Exception:
        return None

def build_mint_transaction(w3: Web3, contract_address: str, to_address: str, uri: str) -> Dict[str, Any]:
    """Build a real ERC721 mint transaction"""
    try:
        # Validate addresses
        try:
            contract_address = Web3.to_checksum_address(contract_address)
            to_address = Web3.to_checksum_address(to_address)
        except Exception:
            return {
                "success": False,
                "error": "validation_error",
                "message": "Invalid Ethereum address format"
            }
        
        # Validate URI
        if not uri or len(uri) == 0:
            return {
                "success": False,
                "error": "validation_error",
                "message": "URI must not be empty"
            }
        
        # Get current block info
        current_block = w3.eth.block_number
        current_timestamp = datetime.now(timezone.utc).isoformat()
        
        # Create contract instance
        contract = w3.eth.contract(address=contract_address, abi=ERC721_ABI)
        
        # Query contract info
        try:
            contract_name = contract.functions.name().call()
        except Exception:
            contract_name = "Unknown"
        
        try:
            contract_symbol = contract.functions.symbol().call()
        except Exception:
            contract_symbol = "UNKNOWN"
        
        try:
            total_supply = contract.functions.totalSupply().call()
            next_token_id = total_supply + 1
        except Exception:
            next_token_id = 1
        
        # Build safeMint(address, string) call data
        # Function signature: safeMint(address to, string memory uri)
        # Selector: 0x50bb4e7f (keccak256("safeMint(address,string)"))
        # For simplicity, show standard mint(address) with next token ID
        
        # Standard ERC721 mint function selector
        # mint(address) = 0x6a627842
        # or safeMint(address,string) = 0x50bb4e7f
        
        # Build transaction data
        mint_call_data = "0x50bb4e7f"  # safeMint(address,string) selector
        
        # Encode parameters: address (32 bytes) + string offset (32 bytes) + string length + string data
        # Address: to_address (padded to 32 bytes)
        address_encoded = to_address[2:].lower().zfill(64)
        # String offset pointer (from data start)
        offset = "0000000000000000000000000000000000000000000000000000000000000040"
        # String length (32 bytes)
        uri_length = hex(len(uri))[2:].zfill(64)
        # String data (padded to multiple of 32)
        uri_bytes = uri.encode().hex()
        # Pad to multiple of 32 bytes (64 hex chars)
        padding_needed = (32 - (len(uri) % 32)) % 32
        uri_padded = uri_bytes + "00" * padding_needed
        
        call_data = mint_call_data + address_encoded + offset + uri_length + uri_padded
        
        # Estimate gas (typical safeMint: 60000-100000 wei)
        estimated_gas = 80000
        
        return {
            "success": True,
            "contract": contract_address,
            "contract_name": contract_name,
            "contract_symbol": contract_symbol,
            "next_token_id": next_token_id,
            "recipient": to_address,
            "uri": uri,
            "transaction": {
                "from": "0x0000000000000000000000000000000000000000",  # Placeholder - user would sign with their key
                "to": contract_address,
                "function": "safeMint(address,string)",
                "function_selector": "0x50bb4e7f",
                "parameters": {
                    "to": to_address,
                    "uri": uri
                },
                "data": call_data,
                "estimated_gas": estimated_gas,
                "gas_price_gwei": 50,  # Estimated current price
                "total_estimated_cost_eth": (estimated_gas * 50 * 1e-9)  # gas * gasPrice
            },
            "block_number": current_block,
            "rpc_used": RPC_URL,
            "timestamp": current_timestamp,
            "note": "Transaction not signed or sent - requires private key to execute on blockchain"
        }
    except Exception as e:
        return {
            "success": False,
            "error": "system_error",
            "message": f"Error building mint transaction: {str(e)}"
        }

def main():
    try:
        input_data = json.loads(sys.stdin.read())
        
        # Validate required parameters
        contract = input_data.get("contract")
        to = input_data.get("to")
        uri = input_data.get("uri")
        
        if not all([contract, to, uri]):
            result = {
                "success": False,
                "error": "validation_error",
                "message": "Required parameters: 'contract' (address), 'to' (address), 'uri' (string)"
            }
            print(json.dumps(result, indent=2))
            return
        
        # Check for dependencies
        if Web3 is None:
            result = {
                "success": False,
                "error": "dependency_error",
                "message": "web3.py and eth_utils packages are required but not installed"
            }
            print(json.dumps(result, indent=2))
            return
        
        # Get Web3 client
        w3 = get_web3_client()
        if not w3:
            result = {
                "success": False,
                "error": "connection_error",
                "message": f"Failed to connect to blockchain RPC: {RPC_URL}"
            }
            print(json.dumps(result, indent=2))
            return
        
        # Build mint transaction
        result = build_mint_transaction(w3, contract, to, uri)
        print(json.dumps(result, indent=2))
    
    except json.JSONDecodeError:
        result = {
            "success": False,
            "error": "validation_error",
            "message": "Invalid JSON input"
        }
        print(json.dumps(result, indent=2))
    except Exception as e:
        result = {
            "success": False,
            "error": "system_error",
            "message": f"Unexpected error: {str(e)}"
        }
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
