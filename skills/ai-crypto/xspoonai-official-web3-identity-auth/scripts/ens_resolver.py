#!/usr/bin/env python3
"""ENS Name Resolution."""

import os
from web3 import Web3
from ens import ENS
from spoon_ai.tools.base import BaseTool
from pydantic import Field

ENS_REGISTRY = "0x00000000000C2E074eC69A0dFb2997BA6C7d2e1e"


class ENSResolverTool(BaseTool):
    """Resolve ENS names to addresses and reverse lookup."""

    name: str = "ens_resolver"
    description: str = "Resolve ENS names to addresses and reverse lookup"
    parameters: dict = Field(default={
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": ["resolve", "reverse", "records"]},
            "input": {"type": "string", "description": "ENS name or address"}
        },
        "required": ["action", "input"]
    })

    def __init__(self):
        super().__init__()
        rpc = os.getenv("ETHEREUM_RPC", "https://eth.llamarpc.com")
        self.w3 = Web3(Web3.HTTPProvider(rpc))
        self.ns = ENS.from_web3(self.w3)

    async def execute(self, action: str, input: str) -> str:
        if action == "resolve":
            return self._resolve_name(input)
        elif action == "reverse":
            return self._reverse_lookup(input)
        elif action == "records":
            return self._get_records(input)
        return f"Unknown action: {action}"

    def _resolve_name(self, name: str) -> str:
        """Resolve ENS name to address."""
        try:
            address = self.ns.address(name)
            if address:
                return f"{name} -> {address}"
            return f"No address found for {name}"
        except Exception as e:
            return f"Error: {str(e)}"

    def _reverse_lookup(self, address: str) -> str:
        """Reverse lookup address to ENS name."""
        try:
            name = self.ns.name(address)
            if name:
                return f"{address} -> {name}"
            return f"No ENS name for {address}"
        except Exception as e:
            return f"Error: {str(e)}"

    def _get_records(self, name: str) -> str:
        """Get ENS text records."""
        try:
            resolver = self.ns.resolver(name)
            if not resolver:
                return f"No resolver for {name}"

            records = {}
            text_keys = ["email", "url", "avatar", "description",
                        "com.twitter", "com.github", "com.discord"]

            for key in text_keys:
                try:
                    value = resolver.functions.text(
                        self.ns.namehash(name), key
                    ).call()
                    if value:
                        records[key] = value
                except:
                    pass

            if records:
                result = f"ENS Records for {name}:\n"
                for k, v in records.items():
                    result += f"  {k}: {v}\n"
                return result

            return f"No text records for {name}"

        except Exception as e:
            return f"Error: {str(e)}"


async def main():
    tool = ENSResolverTool()

    # Resolve vitalik.eth
    result = await tool.execute(action="resolve", input="vitalik.eth")
    print(result)

    # Get records
    result = await tool.execute(action="records", input="vitalik.eth")
    print(result)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
