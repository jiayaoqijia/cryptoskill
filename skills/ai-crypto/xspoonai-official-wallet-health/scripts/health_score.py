#!/usr/bin/env python3
"""
Wallet Health Analyzer - Security scoring for web3 addresses.
Author: SpoonOS Contributor
Version: 1.0.0
"""

import os
import json
import sys
import subprocess
from typing import Dict, Any

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

class WalletHealthTool(BaseTool):
    name: str = "wallet_health"
    description: str = "Analyzes a wallet's on-chain activity."
    parameters: dict = Field(default={
        "type": "object",
        "properties": {
            "target_address": {
                "type": "string",
                "description": "Wallet to analyze"
            },
            "rpc_url": {
                "type": "string",
                "description": "RPC URL"
            }
        },
        "required": ["target_address"]
    })

    async def execute(self, target_address: str, rpc_url: str = None) -> str:
        rpc_url = rpc_url or os.environ.get("WEB3_RPC_URL")
        if not rpc_url:
            return "Error: WEB3_RPC_URL required."

        try:
            w3 = Web3(Web3.HTTPProvider(rpc_url))
            if not w3.is_connected():
                return f"Error: Could not connect to RPC {rpc_url}"

            target_address = w3.to_checksum_address(target_address)
            
            # Fetch Data
            code = w3.eth.get_code(target_address)
            is_contract = len(code) > 0
            
            balance_wei = w3.eth.get_balance(target_address)
            balance_eth = balance_wei / 10**18
            
            nonce = w3.eth.get_transaction_count(target_address)
            
            # Scoring Logic (Heuristic)
            score = 0
            reasons = []
            
            if is_contract:
                score += 50
                reasons.append("Is a Smart Contract")
            else:
                # EOA Logic
                
                # Activity Score (0-40)
                if nonce > 100:
                    score += 40
                elif nonce > 10:
                    score += 20
                else: 
                    score += 5
                    reasons.append("Low Activity")

                # Wealth Score (0-30)
                if balance_eth > 1.0:
                    score += 30
                elif balance_eth > 0.1:
                    score += 15
                else:
                    reasons.append("Low Balance")
                    
                # Base Trust (0-30) - Age would be better, but nonce is a proxy
                if nonce > 0:
                    score += 30 # At least it's active
            
            verdict = "Neutral"
            if score > 80: verdict = "Trusted / High Reputation"
            elif score > 50: verdict = "Established"
            elif score < 20: verdict = "New / Empty / Risky"

            result = {
                "address": target_address,
                "type": "Contract" if is_contract else "EOA",
                "metrics": {
                    "balance": round(balance_eth, 4),
                    "txn_count": nonce
                },
                "score": score,
                "verdict": verdict,
                "flags": reasons
            }
            
            return json.dumps(result, indent=2)

        except Exception as e:
            return f"Error analyzing wallet: {e}"

if __name__ == "__main__":
    import asyncio
    async def main():
        tool = WalletHealthTool()
        print("Wallet Health Tool Standalone")
        # res = await tool.execute(target_address="0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045", rpc_url="https://eth.llamarpc.com")
        # print(res)
    asyncio.run(main())
