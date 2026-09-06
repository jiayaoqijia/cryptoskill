#!/usr/bin/env python3
"""
Portfolio Fetcher - Fetch all ERC20 and NFT holdings from a wallet address
"""

import os
import json
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
import asyncio

try:
    from alchemy import Alchemy, Network
    import aiohttp
except ImportError:
    print("Please install dependencies: pip install alchemy-sdk aiohttp")
    exit(1)


class ChainNetwork(Enum):
    """Supported blockchain networks"""
    ETHEREUM = "ethereum"
    POLYGON = "polygon"
    ARBITRUM = "arbitrum"
    OPTIMISM = "optimism"
    AVALANCHE = "avalanche"
    BASE = "base"


@dataclass
class TokenHolding:
    """Represents a token holding"""
    address: str
    symbol: str
    name: str
    decimals: int
    balance: str
    balance_float: float
    price_usd: Optional[float] = None
    value_usd: Optional[float] = None


@dataclass
class NFTHolding:
    """Represents an NFT holding"""
    contract_address: str
    token_id: str
    name: str
    collection: str
    floor_price_usd: Optional[float] = None
    rarity_score: Optional[float] = None


class PortfolioFetcher:
    """Fetch portfolio holdings from wallet address"""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize portfolio fetcher with Alchemy API key"""
        self.api_key = api_key or os.getenv("ALCHEMY_API_KEY")
        if not self.api_key:
            raise ValueError("ALCHEMY_API_KEY environment variable not set")
        
        self.alchemy = Alchemy(self.api_key)
        self.coingecko_session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.coingecko_session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.coingecko_session:
            await self.coingecko_session.close()

    async def fetch_erc20_holdings(
        self, 
        address: str, 
        chain: str = "ethereum"
    ) -> List[TokenHolding]:
        """Fetch all ERC20 token holdings for an address"""
        try:
            # Get token balances using Alchemy
            response = self.alchemy.core.get_token_balances(address)
            
            holdings: List[TokenHolding] = []
            
            for token in response.get("tokenBalances", []):
                try:
                    # Get token metadata
                    metadata_response = self.alchemy.core.get_token_metadata(
                        token["contractAddress"]
                    )
                    
                    balance_float = int(token["tokenBalance"], 16) / (10 ** metadata_response["decimals"])
                    
                    holding = TokenHolding(
                        address=token["contractAddress"],
                        symbol=metadata_response.get("symbol", "UNKNOWN"),
                        name=metadata_response.get("name", "Unknown Token"),
                        decimals=metadata_response["decimals"],
                        balance=token["tokenBalance"],
                        balance_float=balance_float
                    )
                    holdings.append(holding)
                    
                except Exception as e:
                    print(f"Error fetching metadata for {token['contractAddress']}: {e}")
                    continue
            
            return holdings
            
        except Exception as e:
            print(f"Error fetching ERC20 holdings for {address}: {e}")
            return []

    async def fetch_nft_holdings(
        self,
        address: str,
        chain: str = "ethereum"
    ) -> List[NFTHolding]:
        """Fetch all NFT holdings for an address"""
        try:
            # Get NFTs owned by address
            response = self.alchemy.nft.get_nfts_for_owner(address)
            
            holdings: List[NFTHolding] = []
            
            for nft in response.get("ownedNfts", []):
                holding = NFTHolding(
                    contract_address=nft["contract"]["address"],
                    token_id=nft["tokenId"],
                    name=nft.get("name", "Unknown"),
                    collection=nft.get("contract", {}).get("name", "Unknown Collection")
                )
                holdings.append(holding)
            
            return holdings
            
        except Exception as e:
            print(f"Error fetching NFT holdings for {address}: {e}")
            return []

    async def fetch_token_prices(self, token_ids: List[str]) -> Dict[str, float]:
        """Fetch token prices from CoinGecko"""
        if not self.coingecko_session:
            print("Session not initialized. Use async context manager.")
            return {}
        
        try:
            if not token_ids:
                return {}
            
            # Fetch prices from CoinGecko
            url = "https://api.coingecko.com/api/v3/simple/price"
            params = {
                "ids": ",".join(token_ids),
                "vs_currencies": "usd",
                "include_market_cap": "false",
                "include_24hr_vol": "false"
            }
            
            async with self.coingecko_session.get(url, params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    prices = {}
                    for token_id, price_data in data.items():
                        prices[token_id] = price_data.get("usd", 0)
                    return prices
        
        except Exception as e:
            print(f"Error fetching token prices: {e}")
        
        return {}

    async def fetch_full_portfolio(
        self,
        address: str,
        chain: str = "ethereum",
        include_prices: bool = True
    ) -> Dict:
        """Fetch complete portfolio for address"""
        
        print(f"Fetching portfolio for {address} on {chain}...")
        
        # Fetch holdings
        erc20_holdings = await self.fetch_erc20_holdings(address, chain)
        nft_holdings = await self.fetch_nft_holdings(address, chain)
        
        portfolio = {
            "address": address,
            "chain": chain,
            "erc20_holdings": [],
            "nft_holdings": [],
            "total_value_usd": 0.0,
            "token_count": len(erc20_holdings),
            "nft_count": len(nft_holdings)
        }
        
        # Add token holdings
        for holding in erc20_holdings:
            portfolio["erc20_holdings"].append({
                "symbol": holding.symbol,
                "name": holding.name,
                "address": holding.address,
                "balance": holding.balance_float,
                "decimals": holding.decimals,
                "price_usd": holding.price_usd,
                "value_usd": holding.value_usd
            })
        
        # Add NFT holdings
        for holding in nft_holdings:
            portfolio["nft_holdings"].append({
                "collection": holding.collection,
                "token_id": holding.token_id,
                "contract_address": holding.contract_address,
                "name": holding.name,
                "floor_price_usd": holding.floor_price_usd
            })
        
        return portfolio


async def main():
    """Example usage"""
    import sys
    
    # Get address from command line or use default
    address = sys.argv[1] if len(sys.argv) > 1 else "0x742d35Cc6634C0532925a3b844Bc0e6dB1Eae543"
    chain = sys.argv[2] if len(sys.argv) > 2 else "ethereum"
    
    async with PortfolioFetcher() as fetcher:
        portfolio = await fetcher.fetch_full_portfolio(address, chain)
        print("\n" + "="*60)
        print("PORTFOLIO SUMMARY")
        print("="*60)
        print(json.dumps(portfolio, indent=2))
        print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
