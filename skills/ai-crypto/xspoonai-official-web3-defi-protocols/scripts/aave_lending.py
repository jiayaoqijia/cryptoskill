#!/usr/bin/env python3
"""Aave V3 Lending Integration."""

import os
import json
from web3 import Web3
from spoon_ai.tools.base import BaseTool
from pydantic import Field

# Contract addresses by chain
AAVE_V3_ADDRESSES = {
    "ethereum": {
        "pool": "0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2",
        "pool_data_provider": "0x7B4EB56E7CD4b454BA8ff71E4518426369a138a3",
        "oracle": "0x54586bE62E3c3580375aE3723C145253060Ca0C2"
    },
    "polygon": {
        "pool": "0x794a61358D6845594F94dc1DB02A252b5b4814aD",
        "pool_data_provider": "0x69FA688f1Dc47d4B5d8029D5a35FB7a548310654",
        "oracle": "0xb023e699F5a33916Ea823A16485e259257cA8Bd1"
    },
    "arbitrum": {
        "pool": "0x794a61358D6845594F94dc1DB02A252b5b4814aD",
        "pool_data_provider": "0x69FA688f1Dc47d4B5d8029D5a35FB7a548310654",
        "oracle": "0xb56c2F0B653B2e0b10C9b928C8580Ac5Df02C7C7"
    },
    "base": {
        "pool": "0xA238Dd80C259a72e81d7e4664a9801593F98d1c5",
        "pool_data_provider": "0x2d8A3C5677189723C4cB8873CfC9C8976FDF38Ac",
        "oracle": "0x2Cc0Fc26eD4563A5ce5e8bdcfe1A2878676Ae156"
    }
}

RPC_URLS = {
    "ethereum": "https://eth.llamarpc.com",
    "polygon": "https://polygon-rpc.com",
    "arbitrum": "https://arb1.arbitrum.io/rpc",
    "base": "https://mainnet.base.org"
}


class AaveLendingTool(BaseTool):
    """Aave V3 lending operations."""

    name: str = "aave_lending"
    description: str = "Supply, borrow, repay on Aave V3"
    parameters: dict = Field(default={
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["supply", "borrow", "repay", "withdraw", "positions"],
                "description": "Lending action to perform"
            },
            "asset": {"type": "string", "description": "Token symbol"},
            "amount": {"type": "string", "description": "Amount in token units"},
            "chain": {"type": "string", "default": "ethereum"}
        },
        "required": ["action"]
    })

    async def execute(self, action: str, asset: str = None,
                      amount: str = None, chain: str = "ethereum") -> str:
        if action == "positions":
            return await self._get_positions(chain)
        elif action == "supply":
            return await self._supply(asset, amount, chain)
        elif action == "borrow":
            return await self._borrow(asset, amount, chain)
        elif action == "repay":
            return await self._repay(asset, amount, chain)
        elif action == "withdraw":
            return await self._withdraw(asset, amount, chain)
        return f"Unknown action: {action}"

    async def _get_positions(self, chain: str) -> str:
        """Get user's Aave positions."""
        addresses = AAVE_V3_ADDRESSES.get(chain)
        if not addresses:
            return f"Chain {chain} not supported"

        w3 = Web3(Web3.HTTPProvider(RPC_URLS[chain]))
        user_address = os.getenv("WALLET_ADDRESS")

        # Simplified - actual implementation needs ABI
        return f"Aave positions on {chain} for {user_address}"

    async def _supply(self, asset: str, amount: str, chain: str) -> str:
        return f"Supply {amount} {asset} to Aave on {chain}"

    async def _borrow(self, asset: str, amount: str, chain: str) -> str:
        return f"Borrow {amount} {asset} from Aave on {chain}"

    async def _repay(self, asset: str, amount: str, chain: str) -> str:
        return f"Repay {amount} {asset} on Aave on {chain}"

    async def _withdraw(self, asset: str, amount: str, chain: str) -> str:
        return f"Withdraw {amount} {asset} from Aave on {chain}"


async def main():
    tool = AaveLendingTool()
    result = await tool.execute(action="positions", chain="ethereum")
    print(result)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
