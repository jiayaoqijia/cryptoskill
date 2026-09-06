#!/usr/bin/env python3
"""NFT Minter Agent Template."""

import os
from spoon_ai.agents import SpoonReactMCP
from spoon_ai.chat import ChatBot
from spoon_ai.tools import ToolManager
from spoon_ai.tools.base import BaseTool
from pydantic import Field


class MetadataGeneratorTool(BaseTool):
    """Generate ERC-721/1155 compliant metadata."""

    name: str = "generate_metadata"
    description: str = "Generate NFT metadata following standards"
    parameters: dict = Field(default={
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "description": {"type": "string"},
            "image_uri": {"type": "string"},
            "attributes": {"type": "array", "items": {"type": "object"}}
        },
        "required": ["name", "description", "image_uri"]
    })

    async def execute(self, name: str, description: str,
                      image_uri: str, attributes: list = None) -> str:
        import json

        metadata = {
            "name": name,
            "description": description,
            "image": image_uri,
            "attributes": attributes or []
        }

        return json.dumps(metadata, indent=2)


class IPFSUploadTool(BaseTool):
    """Upload files to IPFS via Pinata."""

    name: str = "ipfs_upload"
    description: str = "Upload file or JSON to IPFS via Pinata"
    parameters: dict = Field(default={
        "type": "object",
        "properties": {
            "content": {"type": "string", "description": "File path or JSON string"},
            "content_type": {"type": "string", "enum": ["file", "json"]}
        },
        "required": ["content", "content_type"]
    })

    async def execute(self, content: str, content_type: str) -> str:
        import aiohttp

        pinata_jwt = os.getenv("PINATA_JWT")
        url = "https://api.pinata.cloud/pinning/pinJSONToIPFS"

        headers = {"Authorization": f"Bearer {pinata_jwt}"}

        if content_type == "json":
            import json
            payload = {"pinataContent": json.loads(content)}

            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return f"ipfs://{data['IpfsHash']}"
                    return f"Error: {await resp.text()}"

        return "File upload not implemented in example"


class ContractDeployTool(BaseTool):
    """Deploy or interact with NFT contracts."""

    name: str = "nft_contract"
    description: str = "Deploy NFT contract or mint tokens"
    parameters: dict = Field(default={
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": ["deploy", "mint", "set_uri"]},
            "contract_address": {"type": "string"},
            "token_uri": {"type": "string"},
            "to_address": {"type": "string"}
        },
        "required": ["action"]
    })

    async def execute(self, action: str, contract_address: str = None,
                      token_uri: str = None, to_address: str = None) -> str:
        if action == "mint":
            return f"Minted NFT to {to_address} with URI {token_uri}"
        elif action == "deploy":
            return "Contract deployed at 0x..."
        return f"Action {action} completed"


class NFTMinterAgent(SpoonReactMCP):
    """NFT creation and deployment agent."""

    name = "nft_minter"
    description = "NFT creation and deployment agent"

    system_prompt = """You are an NFT creation assistant.

    WORKFLOW:
    1. Generate or process artwork metadata
    2. Upload assets to IPFS via Pinata
    3. Deploy or interact with NFT contracts
    4. Mint tokens with proper metadata URI

    STANDARDS:
    - Follow ERC-721/ERC-1155 metadata standards
    - Validate image dimensions and formats
    - Ensure IPFS pinning before minting
    """

    def __init__(self):
        super().__init__(
            llm=ChatBot(model_name="gpt-4o"),
            tools=ToolManager([
                MetadataGeneratorTool(),
                IPFSUploadTool(),
                ContractDeployTool()
            ])
        )


async def main():
    agent = NFTMinterAgent()
    result = await agent.run("Create NFT metadata for 'Crypto Art #1'")
    print(result)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
