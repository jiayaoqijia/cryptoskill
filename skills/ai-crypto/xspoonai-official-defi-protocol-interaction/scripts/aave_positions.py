#!/usr/bin/env python3
"""
Aave V3 Positions Script
Fetches lending/borrowing positions from Aave V3
"""

import json
import sys
import os

try:
    from web3 import Web3
except ImportError:
    print(json.dumps({"error": "web3 package not installed. Run: pip install web3"}))
    sys.exit(1)

# Aave V3 Pool Data Provider ABI (minimal)
POOL_DATA_PROVIDER_ABI = [
    {
        "inputs": [{"name": "user", "type": "address"}],
        "name": "getUserReservesData",
        "outputs": [
            {
                "components": [
                    {"name": "underlyingAsset", "type": "address"},
                    {"name": "scaledATokenBalance", "type": "uint256"},
                    {"name": "usageAsCollateralEnabledOnUser", "type": "bool"},
                    {"name": "scaledVariableDebt", "type": "uint256"}
                ],
                "name": "",
                "type": "tuple[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

# Aave V3 Pool ABI (minimal)
POOL_ABI = [
    {
        "inputs": [{"name": "user", "type": "address"}],
        "name": "getUserAccountData",
        "outputs": [
            {"name": "totalCollateralBase", "type": "uint256"},
            {"name": "totalDebtBase", "type": "uint256"},
            {"name": "availableBorrowsBase", "type": "uint256"},
            {"name": "currentLiquidationThreshold", "type": "uint256"},
            {"name": "ltv", "type": "uint256"},
            {"name": "healthFactor", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

# ERC20 ABI
ERC20_ABI = [
    {"inputs": [], "name": "decimals", "outputs": [{"type": "uint8"}], "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "symbol", "outputs": [{"type": "string"}], "stateMutability": "view", "type": "function"}
]

# Chain configurations
# RPC URLs sourced from Chainlist.org (https://chainlist.org)
AAVE_V3_CONFIG = {
    "ethereum": {
        "rpc": os.getenv("RPC_URL", "https://eth.llamarpc.com"),
        "pool": "0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2",
        "pool_data_provider": "0x7B4EB56E7CD4b454BA8ff71E4518426369a138a3"
    },
    "polygon": {
        "rpc": os.getenv("POLYGON_RPC_URL", "https://polygon-rpc.com"),
        "pool": "0x794a61358D6845594F94dc1DB02A252b5b4814aD",
        "pool_data_provider": "0x69FA688f1Dc47d4B5d8029D5a35FB7a548310654"
    },
    "arbitrum": {
        "rpc": os.getenv("ARBITRUM_RPC_URL", "https://arb1.arbitrum.io/rpc"),
        "pool": "0x794a61358D6845594F94dc1DB02A252b5b4814aD",
        "pool_data_provider": "0x69FA688f1Dc47d4B5d8029D5a35FB7a548310654"
    },
    "optimism": {
        "rpc": os.getenv("OPTIMISM_RPC_URL", "https://mainnet.optimism.io"),
        "pool": "0x794a61358D6845594F94dc1DB02A252b5b4814aD",
        "pool_data_provider": "0x69FA688f1Dc47d4B5d8029D5a35FB7a548310654"
    }
}


def get_aave_positions(wallet: str, chain: str) -> dict:
    """Get Aave V3 positions for a wallet"""
    config = AAVE_V3_CONFIG.get(chain)
    if not config:
        raise ValueError(f"Unsupported chain: {chain}")

    w3 = Web3(Web3.HTTPProvider(config["rpc"]))

    if not w3.is_connected():
        raise ConnectionError(f"Failed to connect to {chain} RPC")

    wallet = Web3.to_checksum_address(wallet)

    # Get pool contract
    pool = w3.eth.contract(
        address=Web3.to_checksum_address(config["pool"]),
        abi=POOL_ABI
    )

    # Get user account data
    account_data = pool.functions.getUserAccountData(wallet).call()

    # Parse account data (values are in base currency with 8 decimals)
    total_collateral_usd = account_data[0] / 1e8
    total_debt_usd = account_data[1] / 1e8
    available_borrows_usd = account_data[2] / 1e8
    liquidation_threshold = account_data[3] / 100  # Percentage
    ltv = account_data[4] / 100  # Percentage
    health_factor = account_data[5] / 1e18 if account_data[5] < 2**256 - 1 else float('inf')

    # Calculate liquidation price (simplified)
    net_worth = total_collateral_usd - total_debt_usd

    return {
        "success": True,
        "chain": chain,
        "wallet": wallet,
        "protocol": "Aave V3",
        "account_summary": {
            "total_collateral_usd": round(total_collateral_usd, 2),
            "total_debt_usd": round(total_debt_usd, 2),
            "available_borrows_usd": round(available_borrows_usd, 2),
            "net_worth_usd": round(net_worth, 2),
            "ltv_percent": round(ltv, 2),
            "liquidation_threshold_percent": round(liquidation_threshold, 2),
            "health_factor": round(health_factor, 4) if health_factor != float('inf') else "Safe (no debt)"
        },
        "risk_assessment": {
            "status": get_risk_status(health_factor),
            "liquidation_risk": "HIGH" if health_factor < 1.1 else "MEDIUM" if health_factor < 1.5 else "LOW",
            "recommendation": get_recommendation(health_factor)
        }
    }


def get_risk_status(health_factor: float) -> str:
    """Get risk status based on health factor"""
    if health_factor == float('inf'):
        return "SAFE - No active loans"
    elif health_factor >= 2.0:
        return "HEALTHY"
    elif health_factor >= 1.5:
        return "MODERATE"
    elif health_factor >= 1.1:
        return "AT RISK"
    else:
        return "CRITICAL - Liquidation imminent"


def get_recommendation(health_factor: float) -> str:
    """Get recommendation based on health factor"""
    if health_factor == float('inf'):
        return "Position is safe. Consider borrowing against your collateral if needed."
    elif health_factor >= 2.0:
        return "Position is healthy. Continue monitoring."
    elif health_factor >= 1.5:
        return "Consider adding more collateral or repaying some debt."
    elif health_factor >= 1.1:
        return "URGENT: Add collateral or repay debt immediately to avoid liquidation."
    else:
        return "CRITICAL: Position at high risk of liquidation. Take immediate action."


def main():
    try:
        input_data = json.loads(sys.stdin.read())

        wallet = input_data.get("wallet")
        chain = input_data.get("chain", "ethereum")

        if not wallet:
            print(json.dumps({"error": "Missing required parameter: wallet"}))
            sys.exit(1)

        result = get_aave_positions(wallet, chain)
        print(json.dumps(result, indent=2))

    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
