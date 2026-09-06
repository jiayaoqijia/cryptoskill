---
name: web3-defi-protocols
description: Integrate DeFi protocols into SpoonOS agents. Use when building lending integrations (Aave, Compound), DEX aggregators (1inch, CoW Protocol), or yield strategies.
---

# DeFi Protocol Integration

Connect SpoonOS agents to major DeFi protocols.

## Supported Protocols

| Protocol | Type | Chains |
|----------|------|--------|
| Aave V3 | Lending | ETH, Polygon, Arbitrum, Optimism, Base |
| Compound V3 | Lending | ETH, Polygon, Arbitrum, Base |
| 1inch | DEX Aggregator | All major EVM |
| CoW Protocol | MEV-protected swaps | ETH, Gnosis |
| Uniswap V3 | DEX | All major EVM |

## Aave V3 Integration

### Contract Addresses

```python
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
```

### Aave Tool Implementation

```python
# scripts/aave_lending.py
from spoon_ai.tools.base import BaseTool
from pydantic import Field
from web3 import Web3
import json

AAVE_POOL_ABI = [...]  # See references/aave-abi.md

class AaveLendingTool(BaseTool):
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
            "asset": {"type": "string", "description": "Token symbol (USDC, WETH, etc.)"},
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

    async def _get_positions(self, chain: str) -> str:
        """Get user's Aave positions."""
        addresses = AAVE_V3_ADDRESSES[chain]
        w3 = Web3(Web3.HTTPProvider(RPC_URLS[chain]))

        pool_data = w3.eth.contract(
            address=addresses["pool_data_provider"],
            abi=POOL_DATA_PROVIDER_ABI
        )

        user_address = os.getenv("WALLET_ADDRESS")
        reserves = pool_data.functions.getUserReservesData(
            addresses["pool"],
            user_address
        ).call()

        positions = []
        for reserve in reserves:
            if reserve[1] > 0 or reserve[2] > 0:  # supplied or borrowed
                positions.append({
                    "asset": reserve[0],
                    "supplied": reserve[1] / 1e18,
                    "borrowed": reserve[2] / 1e18
                })

        return json.dumps({"positions": positions}, indent=2)
```

## 1inch Integration

### API Configuration

```python
ONEINCH_API = {
    "base_url": "https://api.1inch.dev",
    "swap_endpoint": "/swap/v6.0/{chain_id}/swap",
    "quote_endpoint": "/swap/v6.0/{chain_id}/quote",
    "tokens_endpoint": "/swap/v6.0/{chain_id}/tokens"
}

CHAIN_IDS = {
    "ethereum": 1,
    "polygon": 137,
    "arbitrum": 42161,
    "optimism": 10,
    "base": 8453
}
```

### 1inch Swap Tool

```python
# scripts/oneinch_swap.py
import aiohttp
import os
from spoon_ai.tools.base import BaseTool
from pydantic import Field

class OneInchSwapTool(BaseTool):
    name: str = "oneinch_swap"
    description: str = "Get swap quotes and execute via 1inch aggregator"
    parameters: dict = Field(default={
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": ["quote", "swap"]},
            "from_token": {"type": "string", "description": "Source token address"},
            "to_token": {"type": "string", "description": "Destination token address"},
            "amount": {"type": "string", "description": "Amount in wei"},
            "chain": {"type": "string", "default": "ethereum"},
            "slippage": {"type": "number", "default": 1, "description": "Slippage %"}
        },
        "required": ["action", "from_token", "to_token", "amount"]
    })

    async def execute(self, action: str, from_token: str, to_token: str,
                      amount: str, chain: str = "ethereum", slippage: float = 1) -> str:
        chain_id = CHAIN_IDS[chain]
        api_key = os.getenv("ONEINCH_API_KEY")

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        if action == "quote":
            url = f"{ONEINCH_API['base_url']}/swap/v6.0/{chain_id}/quote"
            params = {
                "src": from_token,
                "dst": to_token,
                "amount": amount
            }
        else:
            url = f"{ONEINCH_API['base_url']}/swap/v6.0/{chain_id}/swap"
            params = {
                "src": from_token,
                "dst": to_token,
                "amount": amount,
                "from": os.getenv("WALLET_ADDRESS"),
                "slippage": slippage
            }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as resp:
                if resp.status != 200:
                    error = await resp.text()
                    return f"Error: {error}"

                data = await resp.json()

                if action == "quote":
                    return self._format_quote(data)
                else:
                    return self._format_swap(data)

    def _format_quote(self, data: dict) -> str:
        return f"""
1inch Quote:
- From: {data['srcToken']['symbol']}
- To: {data['dstToken']['symbol']}
- Input: {int(data['srcAmount']) / 10**data['srcToken']['decimals']:.6f}
- Output: {int(data['dstAmount']) / 10**data['dstToken']['decimals']:.6f}
- Gas: {data.get('gas', 'N/A')}
"""
```

## CoW Protocol Integration

### MEV-Protected Swaps

```python
# scripts/cow_swap.py
import aiohttp
from spoon_ai.tools.base import BaseTool
from pydantic import Field
from eth_account import Account
from eth_account.messages import encode_typed_data

COW_API = {
    "ethereum": "https://api.cow.fi/mainnet",
    "gnosis": "https://api.cow.fi/xdai"
}

class CowSwapTool(BaseTool):
    name: str = "cow_swap"
    description: str = "MEV-protected swaps via CoW Protocol"
    parameters: dict = Field(default={
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": ["quote", "order"]},
            "sell_token": {"type": "string"},
            "buy_token": {"type": "string"},
            "sell_amount": {"type": "string"},
            "chain": {"type": "string", "default": "ethereum"}
        },
        "required": ["action", "sell_token", "buy_token", "sell_amount"]
    })

    async def execute(self, action: str, sell_token: str, buy_token: str,
                      sell_amount: str, chain: str = "ethereum") -> str:
        base_url = COW_API[chain]

        if action == "quote":
            return await self._get_quote(base_url, sell_token, buy_token, sell_amount)
        else:
            return await self._create_order(base_url, sell_token, buy_token, sell_amount)

    async def _get_quote(self, base_url: str, sell_token: str,
                         buy_token: str, sell_amount: str) -> str:
        url = f"{base_url}/api/v1/quote"

        payload = {
            "sellToken": sell_token,
            "buyToken": buy_token,
            "sellAmountBeforeFee": sell_amount,
            "kind": "sell",
            "from": os.getenv("WALLET_ADDRESS"),
            "receiver": os.getenv("WALLET_ADDRESS")
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                if resp.status != 200:
                    return f"Error: {await resp.text()}"

                data = await resp.json()
                return f"""
CoW Protocol Quote:
- Sell: {int(data['quote']['sellAmount']) / 1e18:.6f}
- Buy: {int(data['quote']['buyAmount']) / 1e18:.6f}
- Fee: {int(data['quote']['feeAmount']) / 1e18:.6f}
- Valid until: {data['quote']['validTo']}
- MEV Protected: Yes
"""
```

## Yield Strategy Tools

### APY Aggregator

```python
# scripts/yield_finder.py
import aiohttp
from spoon_ai.tools.base import BaseTool
from pydantic import Field

DEFI_LLAMA_API = "https://yields.llama.fi"

class YieldFinderTool(BaseTool):
    name: str = "yield_finder"
    description: str = "Find best DeFi yields across protocols"
    parameters: dict = Field(default={
        "type": "object",
        "properties": {
            "token": {"type": "string", "description": "Token symbol"},
            "chain": {"type": "string", "default": "all"},
            "min_tvl": {"type": "number", "default": 1000000},
            "top_n": {"type": "integer", "default": 5}
        },
        "required": ["token"]
    })

    async def execute(self, token: str, chain: str = "all",
                      min_tvl: float = 1000000, top_n: int = 5) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{DEFI_LLAMA_API}/pools") as resp:
                if resp.status != 200:
                    return f"Error fetching yields"

                pools = await resp.json()

        # Filter by token and criteria
        filtered = [
            p for p in pools["data"]
            if token.upper() in p.get("symbol", "").upper()
            and p.get("tvlUsd", 0) >= min_tvl
            and (chain == "all" or p.get("chain", "").lower() == chain.lower())
        ]

        # Sort by APY
        filtered.sort(key=lambda x: x.get("apy", 0), reverse=True)

        result = f"Top {top_n} yields for {token}:\n\n"
        for i, pool in enumerate(filtered[:top_n], 1):
            result += f"""{i}. {pool['project']} ({pool['chain']})
   - APY: {pool['apy']:.2f}%
   - TVL: ${pool['tvlUsd']:,.0f}
   - Pool: {pool['symbol']}

"""

        return result
```

## Token Addresses

### Common Tokens

```python
TOKENS = {
    "ethereum": {
        "USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "USDT": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
        "DAI": "0x6B175474E89094C44Da98b954EeacdeCB5BE3830",
        "WETH": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        "WBTC": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",
        "AAVE": "0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9"
    },
    "polygon": {
        "USDC": "0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359",  # Native USDC
        "USDT": "0xc2132D05D31c914a87C6611C10748AEb04B58e8F",
        "WETH": "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619",
        "WPOL": "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270"
    },
    "arbitrum": {
        "USDC": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",  # Native
        "USDT": "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9",
        "WETH": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
        "ARB": "0x912CE59144191C1204E64559FE8253a0e49E6548"
    },
    "base": {
        "USDC": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
        "WETH": "0x4200000000000000000000000000000000000006",
        "cbETH": "0x2Ae3F1Ec7F1F5012CFEab0185bfc7aa3cf0DEc22"
    }
}
```

## Environment Variables

```bash
# API Keys
ONEINCH_API_KEY=...

# RPC URLs
ETHEREUM_RPC=https://eth.llamarpc.com
POLYGON_RPC=https://polygon-rpc.com
ARBITRUM_RPC=https://arb1.arbitrum.io/rpc

# Wallet
PRIVATE_KEY=0x...
WALLET_ADDRESS=0x...
```

## References

- `references/aave-abi.md` - Aave V3 contract ABIs
- `references/defi-addresses.md` - Protocol addresses by chain
- `references/token-lists.md` - Verified token addresses
