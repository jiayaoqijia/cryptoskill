#!/usr/bin/env python3
"""
Bridge Status Script
Checks the status of bridge transactions
"""

import json
import sys
import os
import urllib.request
import urllib.error
from typing import Dict, Optional
from datetime import datetime

# Chain configurations for explorers
# RPC URLs sourced from Chainlist.org (https://chainlist.org)
CHAIN_EXPLORERS = {
    "ethereum": {
        "rpc_url": "https://eth.llamarpc.com",
        "api_url": "https://api.etherscan.io/api",
        "api_key_env": "ETHERSCAN_API_KEY",
        "name": "Etherscan"
    },
    "polygon": {
        "rpc_url": "https://polygon-rpc.com",
        "api_url": "https://api.polygonscan.com/api",
        "api_key_env": "POLYGONSCAN_API_KEY",
        "name": "Polygonscan"
    },
    "arbitrum": {
        "rpc_url": "https://arb1.arbitrum.io/rpc",
        "api_url": "https://api.arbiscan.io/api",
        "api_key_env": "ARBISCAN_API_KEY",
        "name": "Arbiscan"
    },
    "optimism": {
        "rpc_url": "https://mainnet.optimism.io",
        "api_url": "https://api-optimistic.etherscan.io/api",
        "api_key_env": "OPTIMISM_API_KEY",
        "name": "Optimistic Etherscan"
    },
    "base": {
        "rpc_url": "https://mainnet.base.org",
        "api_url": "https://api.basescan.org/api",
        "api_key_env": "BASESCAN_API_KEY",
        "name": "Basescan"
    },
    "bsc": {
        "rpc_url": "https://bsc-dataseed.bnbchain.org",
        "api_url": "https://api.bscscan.com/api",
        "api_key_env": "BSCSCAN_API_KEY",
        "name": "BscScan"
    },
    "zksync": {
        "rpc_url": "https://mainnet.era.zksync.io",
        "api_url": "https://block-explorer-api.mainnet.zksync.io/api",
        "api_key_env": "ZKSYNC_API_KEY",
        "name": "zkSync Explorer"
    },
    "linea": {
        "rpc_url": "https://rpc.linea.build",
        "api_url": "https://api.lineascan.build/api",
        "api_key_env": "LINEASCAN_API_KEY",
        "name": "Lineascan"
    }
}

# Bridge-specific status endpoints
BRIDGE_STATUS_INFO = {
    "stargate": {
        "explorer_url": "https://layerzeroscan.com/tx/",
        "typical_time": "2-5 minutes",
        "status_check": "LayerZero Scan"
    },
    "wormhole": {
        "explorer_url": "https://wormholescan.io/#/tx/",
        "typical_time": "15-30 minutes",
        "status_check": "Wormhole Scan"
    },
    "across": {
        "explorer_url": "https://across.to/transactions",
        "typical_time": "2-10 minutes",
        "status_check": "Across Explorer"
    },
    "hop": {
        "explorer_url": "https://explorer.hop.exchange/",
        "typical_time": "5-15 minutes",
        "status_check": "Hop Explorer"
    }
}


def fetch_api(base_url: str, params: dict, api_key: Optional[str] = None) -> dict:
    """Fetch data from API"""
    if api_key:
        params["apikey"] = api_key

    query = "&".join(f"{k}={v}" for k, v in params.items())
    url = f"{base_url}?{query}"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "BridgeStatus/1.0"})
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except urllib.error.URLError as e:
        raise ConnectionError(f"Failed to fetch data: {e}")


def get_tx_status(tx_hash: str, chain: str) -> Dict:
    """Get transaction status from block explorer"""
    config = CHAIN_EXPLORERS.get(chain.lower())
    if not config:
        return {"status": "unknown", "error": f"Unsupported chain: {chain}"}

    api_key = os.getenv(config["api_key_env"]) or os.getenv("ETHERSCAN_API_KEY")

    params = {
        "module": "proxy",
        "action": "eth_getTransactionReceipt",
        "txhash": tx_hash
    }

    try:
        data = fetch_api(config["api_url"], params, api_key)
        result = data.get("result")

        if result is None:
            return {"status": "pending", "confirmations": 0}

        status_code = result.get("status", "0x0")
        block_number = int(result.get("blockNumber", "0x0"), 16)

        return {
            "status": "success" if status_code == "0x1" else "failed",
            "block_number": block_number,
            "gas_used": int(result.get("gasUsed", "0x0"), 16),
            "confirmed": True
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


def check_bridge_status(bridge: str, tx_hash: str, source_chain: str, dest_chain: str = None) -> Dict:
    """Check bridge transaction status"""
    bridge = bridge.lower()
    source_chain = source_chain.lower()

    # Get source transaction status
    source_status = get_tx_status(tx_hash, source_chain)

    bridge_info = BRIDGE_STATUS_INFO.get(bridge, {})

    result = {
        "success": True,
        "timestamp": datetime.utcnow().isoformat(),
        "bridge": bridge,
        "tx_hash": tx_hash,
        "source_chain": source_chain,
        "dest_chain": dest_chain,
        "source_transaction": {
            "status": source_status.get("status"),
            "block_number": source_status.get("block_number"),
            "confirmed": source_status.get("confirmed", False)
        },
        "bridge_status": {
            "phase": determine_phase(source_status),
            "estimated_completion": bridge_info.get("typical_time", "Unknown"),
            "explorer_url": bridge_info.get("explorer_url", "") + tx_hash if bridge_info.get("explorer_url") else None
        },
        "tracking": {
            "check_source": f"Check source tx on {CHAIN_EXPLORERS.get(source_chain, {}).get('name', source_chain)}",
            "check_bridge": f"Track via {bridge_info.get('status_check', bridge + ' explorer')}",
            "check_destination": f"Check destination on {CHAIN_EXPLORERS.get(dest_chain, {}).get('name', dest_chain or 'destination explorer')}" if dest_chain else None
        },
        "next_steps": get_next_steps(source_status, bridge)
    }

    return result


def determine_phase(source_status: Dict) -> str:
    """Determine current phase of bridge transaction"""
    status = source_status.get("status")

    if status == "pending":
        return "PENDING - Source transaction not yet confirmed"
    elif status == "failed":
        return "FAILED - Source transaction failed"
    elif status == "success":
        return "IN_PROGRESS - Source confirmed, awaiting destination"
    else:
        return "UNKNOWN"


def get_next_steps(source_status: Dict, bridge: str) -> list:
    """Get recommended next steps"""
    steps = []

    status = source_status.get("status")

    if status == "pending":
        steps.append("Wait for source transaction to be confirmed")
        steps.append("Check gas price - transaction may be stuck if gas too low")
    elif status == "failed":
        steps.append("Source transaction failed - review error and retry")
        steps.append("Ensure sufficient gas and token balance")
    elif status == "success":
        steps.append("Source confirmed - bridge is processing")
        steps.append(f"Typical completion time: {BRIDGE_STATUS_INFO.get(bridge, {}).get('typical_time', '5-30 minutes')}")
        steps.append("Check destination chain for incoming transaction")

        if bridge == "wormhole":
            steps.append("If stuck, may need to manually redeem via Wormhole Portal")
        elif bridge == "native":
            steps.append("Native bridge withdrawals may take 7 days to finalize")

    return steps


def get_bridge_health(bridge: str) -> Dict:
    """Get bridge health status"""
    # In production, this would check actual bridge status APIs
    # For now, return mock data

    return {
        "bridge": bridge,
        "status": "OPERATIONAL",
        "latency": "Normal",
        "last_incident": None,
        "note": "Check official bridge status page for real-time updates"
    }


def main():
    try:
        input_data = json.loads(sys.stdin.read())

        action = input_data.get("action", "check_tx")
        bridge = input_data.get("bridge", "stargate")
        tx_hash = input_data.get("tx_hash")
        source_chain = input_data.get("source_chain", "ethereum")
        dest_chain = input_data.get("dest_chain")

        if action == "check_tx":
            if not tx_hash:
                print(json.dumps({"error": "Missing required parameter: tx_hash"}))
                sys.exit(1)
            result = check_bridge_status(bridge, tx_hash, source_chain, dest_chain)
        elif action == "health":
            result = get_bridge_health(bridge)
        else:
            print(json.dumps({"error": f"Unknown action: {action}"}))
            sys.exit(1)

        print(json.dumps(result, indent=2))

    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
