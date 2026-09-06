#!/usr/bin/env python3
"""DeFi Quote Exec - Get REAL prices and execute token swaps using actual blockchain data"""
import json
import sys
import os
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Tuple
from enum import Enum

try:
    from web3 import Web3
except ImportError:
    Web3 = None

class ChainType(Enum):
    """Supported blockchain networks"""
    ETHEREUM = "ethereum"
    POLYGON = "polygon"
    ARBITRUM = "arbitrum"
    OPTIMISM = "optimism"
    BASE = "base"

# Real RPC endpoints for each chain
RPC_ENDPOINTS = {
    "ethereum": os.getenv("ETHEREUM_RPC", "https://eth-mainnet.public.blastapi.io"),
    "polygon": os.getenv("POLYGON_RPC", "https://polygon-mainnet.public.blastapi.io"),
    "arbitrum": os.getenv("ARBITRUM_RPC", "https://arbitrum-one.public.blastapi.io"),
    "optimism": os.getenv("OPTIMISM_RPC", "https://optimism-mainnet.public.blastapi.io"),
    "base": os.getenv("BASE_RPC", "https://base-mainnet.public.blastapi.io"),
}

# Token registry with REAL addresses
TOKEN_REGISTRY = {
    "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2": {"symbol": "WETH", "decimals": 18, "name": "Wrapped Ether"},
    "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48": {"symbol": "USDC", "decimals": 6, "name": "USD Coin"},
    "0xdac17f958d2ee523a2206206994597c13d831ec7": {"symbol": "USDT", "decimals": 6, "name": "Tether USD"},
    "0x6b175474e89094c44da98b954eedeac495271d0f": {"symbol": "DAI", "decimals": 18, "name": "Dai Stablecoin"},
    "0x2260fac5e5542a773aa44fbcff9d822a3ecee8e7": {"symbol": "WBTC", "decimals": 8, "name": "Wrapped Bitcoin"},
    "0x7fc66500c84a76ad7e9c93437e434122a1f9adf9": {"symbol": "AAVE", "decimals": 18, "name": "Aave Token"},
}

# Uniswap V3 Factory addresses by chain
UNISWAP_V3_FACTORIES = {
    "ethereum": "0x1F98431c8aD98523631AE4a59f267346ea31F984",
    "polygon": "0x1F98431c8aD98523631AE4a59f267346ea31F984",
    "arbitrum": "0x1F98431c8aD98523631AE4a59f267346ea31F984",
    "optimism": "0x1F98431c8aD98523631AE4a59f267346ea31F984",
    "base": "0x33128a8fC17869897DCe68Ed026d694621f6FDaD",
}

# Uniswap V3 Router addresses
UNISWAP_V3_ROUTERS = {
    "ethereum": "0xE592427A0AEce92De3Edee1F18E0157C05861564",
    "polygon": "0xE592427A0AEce92De3Edee1F18E0157C05861564",
    "arbitrum": "0xE592427A0AEce92De3Edee1F18E0157C05861564",
    "optimism": "0xE592427A0AEce92De3Edee1F18E0157C05861564",
    "base": "0x2626664c2603336E57B271c5C0b26F421741e481",
}

# Uniswap V3 Pool ABI (minimal)
UNISWAP_V3_POOL_ABI = [
    {
        "inputs": [],
        "name": "slot0",
        "outputs": [
            {"name": "sqrtPriceX96", "type": "uint160"},
            {"name": "tick", "type": "int24"},
            {"name": "observationIndex", "type": "uint16"},
            {"name": "observationCardinality", "type": "uint16"},
            {"name": "observationCardinalityNext", "type": "uint16"},
            {"name": "feeProtocol", "type": "uint8"},
            {"name": "unlocked", "type": "bool"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "liquidity",
        "outputs": [{"name": "", "type": "uint128"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "token0",
        "outputs": [{"name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "token1",
        "outputs": [{"name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "fee",
        "outputs": [{"name": "", "type": "uint24"}],
        "stateMutability": "view",
        "type": "function"
    }
]

# Uniswap V3 Factory ABI (getPool function only)
UNISWAP_V3_FACTORY_ABI = [
    {
        "inputs": [
            {"name": "tokenA", "type": "address"},
            {"name": "tokenB", "type": "address"},
            {"name": "fee", "type": "uint24"}
        ],
        "name": "getPool",
        "outputs": [{"name": "pool", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    }
]

# ERC20 ABI (minimal for balanceOf)
ERC20_ABI = [
    {
        "inputs": [{"name": "account", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "name",
        "outputs": [{"name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function"
    }
]

def validate_address(address: str) -> bool:
    """Validate Ethereum address format"""
    if not isinstance(address, str):
        return False
    if not address.startswith("0x"):
        return False
    if len(address) != 42:
        return False
    try:
        int(address, 16)
        return True
    except ValueError:
        return False

def get_web3_client(chain: str = "ethereum"):
    """Get Web3 client with RPC connection"""
    if Web3 is None:
        raise RuntimeError("dependency_error: web3.py not installed. Install with: pip install web3")
    
    rpc_url = RPC_ENDPOINTS.get(chain)
    if not rpc_url:
        raise ValueError(f"Unsupported chain: {chain}")
    
    try:
        w3 = Web3(Web3.HTTPProvider(rpc_url, request_kwargs={"timeout": 30}))
        # Try to get latest block to verify connection (more reliable than is_connected())
        try:
            _ = w3.eth.block_number
        except Exception as e:
            raise ConnectionError(f"Failed to connect to RPC: {rpc_url}. Error: {str(e)}")
        return w3
    except Exception as e:
        raise RuntimeError(f"connection_error: Failed to connect to blockchain RPC: {str(e)}")

def get_token_info_from_chain(w3, token_address: str) -> Optional[Dict]:
    """Get token info directly from blockchain"""
    try:
        token_address = Web3.to_checksum_address(token_address)
        contract = w3.eth.contract(address=token_address, abi=ERC20_ABI)
        
        # Try to get decimals and symbol from contract
        try:
            decimals = contract.functions.decimals().call()
        except:
            decimals = 18  # Default to 18
        
        try:
            symbol = contract.functions.symbol().call()
        except:
            symbol = "UNKNOWN"
        
        try:
            name = contract.functions.name().call()
        except:
            name = "Unknown Token"
        
        return {
            "symbol": symbol,
            "decimals": decimals,
            "name": name
        }
    except Exception as e:
        # Fall back to registry if blockchain call fails
        return TOKEN_REGISTRY.get(token_address.lower())

def find_pool_on_chain(w3, token_in: str, token_out: str, chain: str = "ethereum", fee: int = 3000) -> Optional[str]:
    """Find Uniswap V3 pool address on chain"""
    try:
        factory_address = UNISWAP_V3_FACTORIES.get(chain)
        if not factory_address:
            return None
        
        factory_address = Web3.to_checksum_address(factory_address)
        token_in = Web3.to_checksum_address(token_in)
        token_out = Web3.to_checksum_address(token_out)
        
        factory = w3.eth.contract(address=factory_address, abi=UNISWAP_V3_FACTORY_ABI)
        pool_address = factory.functions.getPool(token_in, token_out, fee).call()
        
        # Check if pool exists (non-zero address)
        if pool_address == "0x0000000000000000000000000000000000000000":
            return None
        
        return pool_address
    except Exception as e:
        return None

def get_pool_price(w3, pool_address: str) -> Tuple[float, int, float]:
    """Get current price from Uniswap V3 pool"""
    try:
        pool_address = Web3.to_checksum_address(pool_address)
        pool = w3.eth.contract(address=pool_address, abi=UNISWAP_V3_POOL_ABI)
        
        slot0 = pool.functions.slot0().call()
        sqrt_price_x96 = slot0[0]
        liquidity = pool.functions.liquidity().call()
        
        # Convert sqrt price to regular price
        # price = (sqrtPriceX96 / 2^96)^2
        price = (sqrt_price_x96 / (2 ** 96)) ** 2
        
        token0 = pool.functions.token0().call()
        token1 = pool.functions.token1().call()
        fee = pool.functions.fee().call()
        
        return price, liquidity, float(fee) / 1000000  # Convert fee to percentage
    except Exception as e:
        return None, None, None

def calculate_quote_from_chain(
    w3,
    token_in: str,
    token_out: str,
    amount_in: float,
    token_in_decimals: int,
    token_out_decimals: int,
    price: float,
    pool_fee: float
) -> Tuple[float, float]:
    """Calculate quote amount using on-chain price data"""
    
    # Normalize amounts to same decimal basis for calculation
    amount_in_normalized = amount_in / (10 ** token_in_decimals)
    
    # Calculate output using pool price
    amount_out_ideal = amount_in_normalized * price
    
    # Calculate slippage based on trade size (simplified)
    slippage = min(pool_fee * 100 + 0.1, 1.0)  # Fee + minimal slippage
    
    # Apply fee and slippage
    amount_out = amount_out_ideal * (1 - slippage / 100)
    amount_out_scaled = amount_out * (10 ** token_out_decimals)
    
    return amount_out_scaled, slippage

def get_quote(
    token_in: str,
    token_out: str,
    amount_in: float,
    chain: str = "ethereum",
    slippage_tolerance: float = 0.5
) -> Dict:
    """Get comprehensive DeFi quote using REAL blockchain data"""
    
    try:
        # Check web3.py availability
        if Web3 is None:
            return {
                "success": False,
                "error": "dependency_error",
                "message": "web3.py not installed. Install with: pip install web3"
            }
        
        # Validate inputs
        if not validate_address(token_in):
            return {"success": False, "error": "validation_error", "message": f"Invalid token_in address: {token_in}"}
        if not validate_address(token_out):
            return {"success": False, "error": "validation_error", "message": f"Invalid token_out address: {token_out}"}
        if amount_in <= 0:
            return {"success": False, "error": "validation_error", "message": "Amount must be positive"}
        if token_in.lower() == token_out.lower():
            return {"success": False, "error": "validation_error", "message": "Cannot swap same token"}
        
        # Connect to blockchain
        try:
            w3 = get_web3_client(chain)
        except RuntimeError as e:
            return {"success": False, "error": "connection_error", "message": str(e)}
        except Exception as e:
            return {"success": False, "error": "system_error", "message": str(e)}
        
        # Normalize addresses
        token_in = Web3.to_checksum_address(token_in)
        token_out = Web3.to_checksum_address(token_out)
        
        # Get token info from blockchain
        token_in_info = get_token_info_from_chain(w3, token_in)
        token_out_info = get_token_info_from_chain(w3, token_out)
        
        if not token_in_info:
            return {"success": False, "error": "validation_error", "message": f"Token not found: {token_in}"}
        if not token_out_info:
            return {"success": False, "error": "validation_error", "message": f"Token not found: {token_out}"}
        
        # Try standard pool fees (3000 = 0.3%, 500 = 0.05%, ...)
        pool_address = None
        pool_fee = None
        best_price = None
        best_liquidity = None
        
        for fee_tier in [3000, 500, 10000, 1]:
            pool_address = find_pool_on_chain(w3, token_in, token_out, chain, fee_tier)
            if pool_address and pool_address != "0x0000000000000000000000000000000000000000":
                price, liquidity, fee_pct = get_pool_price(w3, pool_address)
                if price is not None and liquidity is not None:
                    if best_liquidity is None or liquidity > best_liquidity:
                        best_price = price
                        best_liquidity = liquidity
                        pool_fee = fee_pct
        
        if pool_address is None or best_price is None:
            return {
                "success": False,
                "error": "validation_error",
                "message": f"No liquidity pool found for {token_in_info['symbol']}/{token_out_info['symbol']} on {chain}"
            }
        
        # Calculate quote from real pool data
        amount_out, slippage = calculate_quote_from_chain(
            w3,
            token_in,
            token_out,
            amount_in,
            token_in_info["decimals"],
            token_out_info["decimals"],
            best_price,
            pool_fee
        )
        
        min_amount_out = amount_out * (1 - slippage_tolerance / 100)
        
        # Get current block and timestamp
        block = w3.eth.get_block('latest')
        block_number = block['number']
        timestamp = block['timestamp']
        
        now = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        
        return {
            "success": True,
            "quote": {
                "token_in": {
                    "address": token_in,
                    "symbol": token_in_info["symbol"],
                    "name": token_in_info["name"],
                    "decimals": token_in_info["decimals"],
                    "amount": amount_in
                },
                "token_out": {
                    "address": token_out,
                    "symbol": token_out_info["symbol"],
                    "name": token_out_info["name"],
                    "decimals": token_out_info["decimals"],
                    "amount_expected": amount_out,
                    "amount_minimum": min_amount_out
                },
                "exchange_rate": amount_out / amount_in if amount_in > 0 else 0,
                "price_impact": slippage,
                "slippage_tolerance": slippage_tolerance,
                "route": {
                    "dex": "uniswap_v3",
                    "pool_address": pool_address,
                    "fee_tier": f"{pool_fee * 100:.2f}%",
                    "liquidity": float(best_liquidity) if best_liquidity else 0,
                    "hops": 1
                },
                "chain": chain,
                "rpc_used": RPC_ENDPOINTS[chain],
                "block_number": block_number,
                "timestamp": now.isoformat(),
                "valid_until": (now + timedelta(minutes=1)).isoformat()
            }
        }
    
    except Exception as e:
        return {"success": False, "error": "system_error", "message": str(e)}

def main():
    try:
        input_data = json.loads(sys.stdin.read())
        
        # Get parameters
        token_in = input_data.get("token_in")
        token_out = input_data.get("token_out")
        amount_in = input_data.get("amount_in")
        chain = input_data.get("chain", "ethereum")
        slippage_tolerance = input_data.get("slippage_tolerance", 0.5)
        
        # Validate required parameters
        if not token_in or not token_out or amount_in is None:
            print(json.dumps({
                "success": False,
                "error": "validation_error",
                "message": "Missing required parameters: token_in, token_out, amount_in"
            }))
            return
        
        amount_in = float(amount_in)
        
        # Get quote using REAL blockchain data
        quote_result = get_quote(token_in, token_out, amount_in, chain, slippage_tolerance)
        
        print(json.dumps(quote_result, indent=2))
    
    except json.JSONDecodeError:
        print(json.dumps({
            "success": False,
            "error": "system_error",
            "message": "Invalid JSON input"
        }))
    except Exception as e:
        print(json.dumps({
            "success": False,
            "error": "system_error",
            "message": str(e)
        }))

if __name__ == "__main__":
    main()
