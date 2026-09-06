#!/usr/bin/env python3
"""
Gas Price Oracle - Fee history analysis for cost optimization.
Author: SpoonOS Contributor
Version: 1.0.0
"""

import os
import json
import sys
import subprocess
import statistics
from typing import List, Dict, Any

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

class GasTrackerTool(BaseTool):
    name: str = "gas_tracker"
    description: str = "Analyzes gas fees and recommends transaction prices."
    parameters: dict = Field(default={
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["get_recommendation", "check_status"],
                "default": "get_recommendation"
            },
            "rpc_url": {
                "type": "string",
                "description": "RPC URL"
            },
            "blocks": {
                "type": "integer",
                "default": 20,
                "description": "Number of blocks to analyze"
            }
        }
    })

    async def execute(self, action: str = "get_recommendation", rpc_url: str = None, blocks: int = 20) -> str:
        rpc_url = rpc_url or os.environ.get("WEB3_RPC_URL")
        if not rpc_url:
            return "Error: WEB3_RPC_URL required."

        try:
            w3 = Web3(Web3.HTTPProvider(rpc_url))
            if not w3.is_connected():
                return f"Error: Could not connect to RPC {rpc_url}"

            # Fetch fee history
            # percentiles to fetch reward history (priority fees)
            history = w3.eth.fee_history(blocks, 'latest', reward_percentiles=[25, 50, 75])
            
            base_fees = history['baseFeePerGas']
            rewards = history['reward'] # list of list
            
            # Convert to Gwei
            to_gwei = lambda x: x / 10**9
            
            latest_base = to_gwei(base_fees[-1])
            avg_base = statistics.mean([to_gwei(x) for x in base_fees[:-1]]) # last one is next block base fee
            
            # Calculate avg priority fees for slow/avg/fast
            priority_slow = statistics.mean([to_gwei(r[0]) for r in rewards])
            priority_avg = statistics.mean([to_gwei(r[1]) for r in rewards])
            priority_fast = statistics.mean([to_gwei(r[2]) for r in rewards])
            
            trend = "stable"
            if latest_base > avg_base * 1.1:
                trend = "rising"
            elif latest_base < avg_base * 0.9:
                trend = "falling"

            result = {
                "status": "success",
                "network_trend": trend,
                "current_base_fee_gwei": round(latest_base, 2),
                "recommendations_gwei": {
                    "slow": round(latest_base + priority_slow, 2),
                    "standard": round(latest_base + priority_avg, 2),
                    "fast": round(latest_base + priority_fast, 2)
                },
                "details": {
                    "avg_historical_base": round(avg_base, 2),
                    "analyzed_blocks": blocks
                }
            }
            
            return json.dumps(result, indent=2)

        except Exception as e:
            return f"Error fetching gas info: {e}"

if __name__ == "__main__":
    import asyncio
    async def main():
        tool = GasTrackerTool()
        # Mock run usually
        print("Gas Tracker Tool (Needs RPC to run for real)")
        # res = await tool.execute(rpc_url="https://eth.llamarpc.com")
        # print(res)
    asyncio.run(main())
