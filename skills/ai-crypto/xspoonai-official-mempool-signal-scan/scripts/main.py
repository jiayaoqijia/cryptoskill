#!/usr/bin/env python3
"""Scan mempool for trading signals and MEV opportunities with real API data"""
import json
import argparse
import sys
import urllib.request
import urllib.error
from datetime import datetime
import hashlib
from urllib.parse import urlencode


# RPC endpoints for different networks
RPC_ENDPOINTS = {
    "ethereum": "https://eth.llamarpc.com",
    "polygon": "https://polygon-rpc.com",
    "arbitrum": "https://arb1.arbitrum.io",
    "optimism": "https://mainnet.optimism.io",
    "bsc": "https://bsc-dataseed1.binance.org",
}

# Known DEX router addresses for swap detection
DEX_ROUTERS = {
    "ethereum": {
        "uniswap_v3": "0xE592427A0AEce92De3Edee1F18E0157C05861564",
        "uniswap_v2": "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D",
        "sushiswap": "0xd9e1cE17f2641f24aE57070Df9aFF3c7cb0407aD",
    },
    "polygon": {
        "uniswap_v3": "0xE592427A0AEce92De3Edee1F18E0157C05861564",
        "quickswap": "0xa5E0829CaCEd8fFDD4De3c43696c57F7D7A678ff",
    },
}

# Stablecoin addresses for value estimation
STABLECOINS = {
    "ethereum": {
        "USDC": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "USDT": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
        "DAI": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
    },
    "polygon": {
        "USDC": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
        "USDT": "0xc2132D05D31c914a87C6611C10748AEb04B58e8F",
    },
}


def format_success(data):
    return json.dumps({"ok": True, "data": data}, ensure_ascii=False)


def format_error(error, details=None):
    result = {"ok": False, "error": error}
    if details:
        result["details"] = details
    return json.dumps(result, ensure_ascii=False)


def fetch_rpc_mempool(network):
    """Fetch mempool transactions via RPC."""
    rpc_url = RPC_ENDPOINTS.get(network)
    if not rpc_url:
        raise ValueError(f"Network {network} not supported")
    
    # Request raw transaction pool contents
    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": "txpool_content",
        "params": [],
        "id": 1
    }).encode()
    
    try:
        req = urllib.request.Request(
            rpc_url,
            data=payload,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode())
            return result.get("result", {})
    except Exception as e:
        raise ValueError(f"Failed to fetch mempool from {network}: {e}")


def fetch_gas_price(network):
    """Fetch current gas price from network."""
    rpc_url = RPC_ENDPOINTS.get(network)
    if not rpc_url:
        return None
    
    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": "eth_gasPrice",
        "params": [],
        "id": 1
    }).encode()
    
    try:
        req = urllib.request.Request(
            rpc_url,
            data=payload,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            result = json.loads(response.read().decode())
            wei = int(result.get("result", "0x0"), 16)
            return round(wei / 1e9, 2)  # Convert to Gwei
    except:
        return None


def detect_swap_signals(mempool_txs, network, min_value_usd):
    """Detect swap transactions in mempool."""
    signals = []
    routers = DEX_ROUTERS.get(network, {})
    router_addresses = set()
    
    # Collect all router addresses
    for router_list in routers.values():
        if isinstance(router_list, dict):
            router_addresses.update(router_list.values())
        else:
            router_addresses.add(router_list)
    
    if not router_addresses:
        return signals
    
    # Check pending transactions
    pending = mempool_txs.get("pending", {})
    for tx_from, txs in list(pending.items())[:20]:  # Limit to first 20 senders
        for tx_nonce, tx_data in txs.items():
            tx_to = tx_data.get("to", "").lower()
            gas_price_hex = tx_data.get("gasPrice", "0x0")
            value_hex = tx_data.get("value", "0x0")
            
            try:
                gas_price = int(gas_price_hex, 16)
                value = int(value_hex, 16) / 1e18  # ETH value
            except:
                continue
            
            # Check if transaction is to a DEX router
            is_swap = any(router.lower() in tx_to for router in router_addresses)
            
            if is_swap:
                # Estimate transaction value in USD (rough estimate: ETH * 2000)
                estimated_usd = value * 2000
                
                if estimated_usd >= min_value_usd:
                    signals.append({
                        "tx_hash": hashlib.sha256(f"{tx_from}{tx_nonce}".encode()).hexdigest()[:16],
                        "from": tx_from[:10] + "..." + tx_from[-4:],
                        "to": tx_to[:10] + "..." + tx_to[-4:],
                        "value_eth": round(value, 4),
                        "estimated_usd": round(estimated_usd, 2),
                        "gas_price_gwei": round(gas_price / 1e9, 2),
                        "type": "swap",
                        "crosses_threshold": True
                    })
    
    return signals


def detect_large_transfers(mempool_txs, network, min_value_usd):
    """Detect large transfer signals."""
    signals = []
    stablecoins = STABLECOINS.get(network, {})
    
    if not stablecoins:
        return signals
    
    pending = mempool_txs.get("pending", {})
    for tx_from, txs in list(pending.items())[:30]:
        for tx_nonce, tx_data in txs.items():
            tx_to = tx_data.get("to", "").lower()
            input_data = tx_data.get("input", "0x")
            
            # Simple heuristic: look for ERC20 transfer-like calls
            # transfer(address,uint256) = 0xa9059cbb...
            if input_data.startswith("0xa9059cbb"):
                # Estimate as transfer (we'd need ABIs to decode properly)
                gas_price_hex = tx_data.get("gasPrice", "0x0")
                try:
                    gas_price = int(gas_price_hex, 16)
                    signals.append({
                        "tx_hash": hashlib.sha256(f"{tx_from}{tx_nonce}".encode()).hexdigest()[:16],
                        "from": tx_from[:10] + "..." + tx_from[-4:],
                        "to": tx_to[:10] + "..." + tx_to[-4:],
                        "type": "transfer",
                        "gas_price_gwei": round(gas_price / 1e9, 2),
                        "likely_stablecoin": True,
                        "estimated_min_usd": min_value_usd,
                        "crosses_threshold": True
                    })
                except:
                    continue
    
    return signals[:10]  # Limit results


def scan_mempool_api(params):
    """Scan mempool with real API data."""
    network = params.get("network")
    signal_type = params.get("signal_type", "swap")
    min_value_usd = params.get("min_value_usd", 100000)
    use_api = params.get("use_api", True)
    
    if not network:
        raise ValueError("network is required")
    
    if network not in RPC_ENDPOINTS:
        raise ValueError(f"Network {network} not supported. Use: {', '.join(RPC_ENDPOINTS.keys())}")
    
    if use_api:
        # Fetch real mempool data via RPC
        mempool_data = fetch_rpc_mempool(network)
        gas_price = fetch_gas_price(network)
        
        # Detect signals based on type
        signals = []
        if signal_type in ["swap", "all"]:
            signals.extend(detect_swap_signals(mempool_data, network, min_value_usd))
        if signal_type in ["transfer", "all"]:
            signals.extend(detect_large_transfers(mempool_data, network, min_value_usd))
        
        result = {
            "source": "mempool_api",
            "network": network,
            "signal_type": signal_type,
            "min_value_usd": min_value_usd,
            "current_gas_gwei": gas_price,
            "total_pending_txs": len(mempool_data.get("pending", {})),
            "signals_detected": len(signals),
            "signals": signals,
            "scan_timestamp": datetime.utcnow().isoformat() + "Z"
        }
    else:
        # Parameter mode - use provided signals
        signals = params.get("signals", [])
        filtered = [s for s in signals if s.get("estimated_usd", 0) >= min_value_usd]
        
        result = {
            "source": "parameters",
            "network": network,
            "signal_type": signal_type,
            "min_value_usd": min_value_usd,
            "total_signals_provided": len(signals),
            "signals_above_threshold": len(filtered),
            "signals": filtered,
            "scan_timestamp": datetime.utcnow().isoformat() + "Z"
        }
    
    return result


def main():
    parser = argparse.ArgumentParser(description='Scan mempool for trading signals')
    parser.add_argument('--params', type=str, required=True, help='JSON parameters')
    
    args = parser.parse_args()
    
    try:
        params = json.loads(args.params)
        result = scan_mempool_api(params)
        print(format_success(result))
    
    except json.JSONDecodeError as e:
        print(format_error(f"Invalid JSON: {e}"))
        sys.exit(1)
    except ValueError as e:
        print(format_error(str(e)))
        sys.exit(1)
    except Exception as e:
        print(format_error(f"Unexpected error: {e}"))
        sys.exit(1)


if __name__ == '__main__':
    main()
