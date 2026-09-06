#!/usr/bin/env python3
"""
Token Allowance Manager - Manage ERC20 approvals.
Author: SpoonOS Contributor
Version: 1.0.0
"""

import os
import json
import sys
import subprocess
from typing import Optional, Dict, Any

# Ensure web3 is installed
try:
    from web3 import Web3
except ImportError:
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "web3"])
        from web3 import Web3
    except Exception as e:
        print(f"Error installing web3: {e}")
        sys.exit(1)

# Attempt to import BaseTool, handle running standalone for testing
try:
    from spoon_ai.tools.base import BaseTool
except ImportError:
    from pydantic import BaseModel, Field
    class BaseTool(BaseModel):
        name: str
        description: str
        parameters: dict
        async def execute(self, **kwargs): pass

from pydantic import Field

ERC20_ABI = [
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}, {"name": "_spender", "type": "address"}],
        "name": "allowance",
        "outputs": [{"name": "", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [{"name": "_spender", "type": "address"}, {"name": "_value", "type": "uint256"}],
        "name": "approve",
        "outputs": [{"name": "", "type": "bool"}],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
    }
]

class AllowanceTool(BaseTool):
    name: str = "manage_allowance"
    description: str = "Check, approve, or revoke ERC20 token allowances."
    parameters: dict = Field(default={
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["check", "approve", "revoke"],
                "description": "Action to perform"
            },
            "token_address": {
                "type": "string",
                "description": "ERC20 token contract address"
            },
            "spender_address": {
                "type": "string",
                "description": "Address of the spender (e.g. Protocol Contract)"
            },
            "amount": {
                "type": "number",
                "description": "Amount to approve (for 'approve' action)"
            },
            "infinite": {
                "type": "boolean",
                "description": "Approve max uint256 value",
                "default": False
            },
            "rpc_url": {
                "type": "string",
                "description": "RPC URL"
            },
            "private_key": {
                "type": "string",
                "description": "Private Key"
            }
        },
        "required": ["action", "token_address", "spender_address"]
    })

    async def execute(self, action: str, token_address: str, spender_address: str, amount: float = 0.0, infinite: bool = False, rpc_url: str = None, private_key: str = None) -> str:
        """
        Executes the allowance action.
        """
        rpc_url = rpc_url or os.environ.get("WEB3_RPC_URL")
        if not rpc_url:
            return "Error: WEB3_RPC_URL environment variable or argument required."

        try:
            w3 = Web3(Web3.HTTPProvider(rpc_url))
            if not w3.is_connected():
                return f"Error: Could not connect to RPC URL: {rpc_url}"

            token_address = w3.to_checksum_address(token_address)
            spender_address = w3.to_checksum_address(spender_address)
            contract = w3.eth.contract(address=token_address, abi=ERC20_ABI)

            # Get decimals for conversion
            try:
                decimals = contract.functions.decimals().call()
            except:
                decimals = 18 # Default fallback

            if action == "check":
                # Need a 'from' address to check? Actually allowance takes owner and spender.
                # If checking "my" allowance, we need a wallet address.
                # Assuming private key is provided or we just check generic if provided?
                # Actually, standard allowance check requires owner. 
                # Let's derive owner from private key if available, else error.
                
                owner_address = None
                if private_key:
                     account = w3.eth.account.from_key(private_key)
                     owner_address = account.address
                elif os.environ.get("WALLET_ADDRESS"):
                    owner_address = w3.to_checksum_address(os.environ.get("WALLET_ADDRESS"))
                else: 
                     # If we can't derive owner, we can't check allowance for "me".
                     # Implied context: User wants to check "my" allowance.
                     pass 

                if not owner_address:
                     return "Error: Cannot check allowance without 'private_key' or 'WALLET_ADDRESS' env var to identify the owner."

                raw_allowance = contract.functions.allowance(owner_address, spender_address).call()
                formatted_allowance = raw_allowance / (10 ** decimals)
                
                return json.dumps({
                    "action": "check",
                    "token": token_address,
                    "spender": spender_address,
                    "owner": owner_address,
                    "allowance_raw": raw_allowance,
                    "allowance_formatted": formatted_allowance
                }, indent=2)

            elif action in ["approve", "revoke"]:
                private_key = private_key or os.environ.get("PRIVATE_KEY")
                if not private_key:
                    return "Error: Private Key required for approve/revoke."
                
                account = w3.eth.account.from_key(private_key)
                
                if action == "revoke":
                    amount_wei = 0
                elif infinite:
                    amount_wei = 2**256 - 1
                else:
                    amount_wei = int(amount * (10 ** decimals))

                # Build tx
                nonce = w3.eth.get_transaction_count(account.address)
                tx = contract.functions.approve(spender_address, amount_wei).build_transaction({
                    'from': account.address,
                    'nonce': nonce,
                    'gasPrice': w3.eth.gas_price
                })
                
                # Estimate gas usually needed, but build_transaction does basic est.
                
                signed_tx = w3.eth.account.sign_transaction(tx, private_key)
                tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
                
                # Wait for receipt
                receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
                
                return json.dumps({
                    "action": action,
                    "status": "success",
                    "transaction_hash": tx_hash.hex(),
                    "block_number": receipt.blockNumber,
                    "amount_approved": "MAX" if infinite else amount
                }, indent=2)
            
            else:
                return f"Error: Unknown action {action}"

        except Exception as e:
            return f"Error managing allowance: {str(e)}"

if __name__ == "__main__":
    import asyncio
    
    async def main():
        tool = AllowanceTool()
        if len(sys.argv) < 2:
            print("Usage: python allowance.py [check|approve|revoke] ...")
            print("Note: Runs in dry-run/error mode without valid RPC/Keys")
            # Just instantiate to verify import
            return

        # Simple CLI wrapper could go here, but for now just exit
        print("CLI testing not implemented, use within agent.")

    asyncio.run(main())
