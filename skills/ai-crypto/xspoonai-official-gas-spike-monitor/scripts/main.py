#!/usr/bin/env python3
"""Monitor and alert on network gas price spikes with real data"""
import json
import argparse
import sys
import urllib.request
import urllib.error
from datetime import datetime


# Network RPC endpoints for live gas price fetching
RPC_ENDPOINTS = {
    "ethereum": "https://eth.llamarpc.com",
    "polygon": "https://polygon-rpc.com",
    "arbitrum": "https://arb1.arbitrum.io/rpc",
    "optimism": "https://mainnet.optimism.io",
    "bsc": "https://bsc-dataseed1.binance.org",
}


def format_success(data):
    return json.dumps({"ok": True, "data": data}, ensure_ascii=False)


def format_error(error, details=None):
    result = {"ok": False, "error": error}
    if details:
        result["details"] = details
    return json.dumps(result, ensure_ascii=False)


def fetch_live_gas_price(network):
    """Fetch live gas price from Ethereum RPC endpoint."""
    try:
        rpc_url = RPC_ENDPOINTS.get(network.lower())
        if not rpc_url:
            raise ValueError(f"Network {network} not supported")
        
        payload = json.dumps({
            "jsonrpc": "2.0",
            "method": "eth_gasPrice",
            "params": [],
            "id": 1
        }).encode()
        
        req = urllib.request.Request(
            rpc_url,
            data=payload,
            headers={"Content-Type": "application/json"}
        )
        
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            
            if "result" in data:
                # Convert from Wei to Gwei (1 Gwei = 10^9 Wei)
                gas_price_wei = int(data["result"], 16)
                gas_price_gwei = gas_price_wei / 1e9
                return round(gas_price_gwei, 4)
            else:
                raise ValueError("Invalid RPC response")
    
    except urllib.error.URLError as e:
        raise ValueError(f"RPC endpoint unreachable: {e}")
    except Exception as e:
        raise ValueError(f"Failed to fetch live gas price: {e}")


def validate_params(params):
    """Validate input parameters."""
    network = params.get("network")
    
    if not network:
        raise ValueError("network is required")
    
    # Check for either current_gas_gwei or use_live_prices flag
    current_gas = params.get("current_gas_gwei")
    use_live = params.get("use_live_prices", False)
    
    baseline_gas = params.get("baseline_gas_gwei")
    if baseline_gas is None and not params.get("average_baseline"):
        raise ValueError("baseline_gas_gwei or average_baseline is required")
    
    if current_gas is None and not use_live:
        raise ValueError("current_gas_gwei is required or set use_live_prices=true")
    
    if current_gas is not None and not isinstance(current_gas, (int, float)):
        raise ValueError("current_gas_gwei must be a number")
    
    if baseline_gas is not None and (not isinstance(baseline_gas, (int, float)) or baseline_gas <= 0):
        raise ValueError("baseline_gas_gwei must be a positive number")
    
    return True


def monitor_gas_spike(params):
    """Monitor network gas prices with real data and optional live fetching."""
    validate_params(params)
    
    network = params.get("network")
    spike_threshold = params.get("spike_threshold_percentage", 25)
    use_live = params.get("use_live_prices", False)
    
    # Get current gas price
    if use_live:
        current_gas = fetch_live_gas_price(network)
        price_source = "live_rpc"
    else:
        current_gas = params.get("current_gas_gwei")
        price_source = "provided"
    
    # Get baseline gas price
    baseline_gas = params.get("baseline_gas_gwei")
    if baseline_gas is None:
        # Use average baseline if provided
        baseline_gas = params.get("average_baseline", 30)  # Default to 30 Gwei
    
    # Calculate spike metrics
    spike_percentage = ((current_gas - baseline_gas) / baseline_gas) * 100
    is_spike = spike_percentage >= spike_threshold
    
    # Calculate gas price status
    if spike_percentage > 50:
        status = "critical"
    elif spike_percentage > spike_threshold:
        status = "elevated"
    else:
        status = "normal"
    
    result = {
        "network": network,
        "current_gas_gwei": round(current_gas, 4),
        "baseline_gas_gwei": round(baseline_gas, 4),
        "spike_percentage": round(spike_percentage, 2),
        "spike_threshold_percentage": spike_threshold,
        "is_spike": is_spike,
        "status": status,
        "alert_triggered": is_spike,
        "price_source": price_source,
        "recommendation": get_recommendation(status),
        "check_timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    return result


def get_recommendation(status):
    """Get recommendation based on gas status."""
    recommendations = {
        "critical": "⚠️ CRITICAL: Gas prices extremely high. Wait for network congestion to clear.",
        "elevated": "⚠️ ELEVATED: Gas prices above normal. Consider batching transactions or using L2.",
        "normal": "✓ Normal: Gas prices within acceptable range."
    }
    return recommendations.get(status, "Unknown status")


def main():
    parser = argparse.ArgumentParser(description='Monitor network gas price spikes')
    parser.add_argument('--params', type=str, required=True, help='JSON parameters')
    
    args = parser.parse_args()
    
    try:
        params = json.loads(args.params)
        result = monitor_gas_spike(params)
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
