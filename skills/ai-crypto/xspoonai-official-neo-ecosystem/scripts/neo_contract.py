#!/usr/bin/env python3
"""
Neo N3 Contract Script
Query and invoke Neo N3 smart contracts via RPC
"""

import json
import sys
import urllib.request
import urllib.error
from typing import Optional, Dict, List, Any

# Network configurations
NETWORK_CONFIG = {
    "mainnet": {
        "rpc_url": "https://mainnet1.neo.coz.io:443",
        "network_id": 860833102
    },
    "testnet": {
        "rpc_url": "https://testnet1.neo.coz.io:443",
        "network_id": 894710606
    }
}

# Well-known contracts
KNOWN_CONTRACTS = {
    "NeoToken": "0xef4073a0f2b305a38ec4050e4d3d28bc40ea63f5",
    "GasToken": "0xd2a4cff31913016155e38e474a2c06d08be276cf",
    "PolicyContract": "0xcc5e4edd9f5f8dba8bb65734541df7a1c081c67b",
    "ContractManagement": "0xfffdc93764dbaddd97c48f252a53ea4643faa3fd",
    "RoleManagement": "0x49cf4e5378ffcd4dec034fd98a174c5491e395e2",
    "OracleContract": "0xfe924b7cfe89ddd271abaf7210a80a7e11178758",
    "LedgerContract": "0xda65b600f7124ce6c79950c1772a36403104f2be",
    "CryptoLib": "0x726cb6e0cd8628a1350a611384688911ab75f51b"
}


def rpc_call(url: str, method: str, params: list) -> dict:
    """Make a JSON-RPC call to Neo node"""
    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1
    }).encode("utf-8")

    try:
        req = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=60) as response:
            return json.loads(response.read().decode())
    except urllib.error.URLError as e:
        raise ConnectionError(f"RPC call failed: {e}")


def format_param(param: Any) -> Dict:
    """Format a parameter for invokefunction"""
    if isinstance(param, str):
        if param.startswith("0x") and len(param) == 42:
            # Script hash
            return {"type": "Hash160", "value": param[2:]}
        elif param.startswith("N") and len(param) == 34:
            # Address - convert to script hash format
            return {"type": "Hash160", "value": param}
        else:
            # String
            return {"type": "String", "value": param}
    elif isinstance(param, int):
        return {"type": "Integer", "value": str(param)}
    elif isinstance(param, bool):
        return {"type": "Boolean", "value": param}
    elif isinstance(param, list):
        return {"type": "Array", "value": [format_param(p) for p in param]}
    else:
        return {"type": "String", "value": str(param)}


def invoke_function(
    contract_hash: str,
    method: str,
    params: List[Any],
    network: str = "mainnet"
) -> Dict:
    """Invoke a contract function (read-only)"""
    config = NETWORK_CONFIG.get(network)
    if not config:
        raise ValueError(f"Unknown network: {network}")

    # Format parameters
    formatted_params = [format_param(p) for p in params]

    result = rpc_call(
        config["rpc_url"],
        "invokefunction",
        [contract_hash, method, formatted_params]
    )

    if "error" in result:
        raise ValueError(result["error"].get("message", "RPC error"))

    return result.get("result", {})


def get_contract_state(contract_hash: str, network: str = "mainnet") -> Dict:
    """Get contract state/info"""
    config = NETWORK_CONFIG.get(network)
    if not config:
        raise ValueError(f"Unknown network: {network}")

    result = rpc_call(
        config["rpc_url"],
        "getcontractstate",
        [contract_hash]
    )

    if "error" in result:
        raise ValueError(result["error"].get("message", "Contract not found"))

    return result.get("result", {})


def get_native_contracts(network: str = "mainnet") -> List[Dict]:
    """Get list of native contracts"""
    config = NETWORK_CONFIG.get(network)
    if not config:
        raise ValueError(f"Unknown network: {network}")

    result = rpc_call(
        config["rpc_url"],
        "getnativecontracts",
        []
    )

    if "error" in result:
        raise ValueError(result["error"].get("message", "RPC error"))

    return result.get("result", [])


def parse_stack_item(item: Dict) -> Any:
    """Parse a stack item from invoke result"""
    item_type = item.get("type", "")
    value = item.get("value")

    if item_type == "Integer":
        return int(value) if value else 0
    elif item_type == "Boolean":
        return value
    elif item_type == "ByteString":
        # Try to decode as string, fall back to hex
        try:
            import base64
            decoded = base64.b64decode(value)
            return decoded.decode("utf-8")
        except:
            return value
    elif item_type == "Array":
        return [parse_stack_item(v) for v in (value or [])]
    elif item_type == "Map":
        result = {}
        for entry in (value or []):
            key = parse_stack_item(entry.get("key", {}))
            val = parse_stack_item(entry.get("value", {}))
            result[str(key)] = val
        return result
    elif item_type == "Struct":
        return [parse_stack_item(v) for v in (value or [])]
    else:
        return value


def query_contract(
    contract_hash: str,
    method: str,
    params: List[Any] = None,
    network: str = "mainnet"
) -> Dict:
    """Query a contract method"""
    params = params or []

    # Resolve known contract names
    if contract_hash in KNOWN_CONTRACTS:
        contract_hash = KNOWN_CONTRACTS[contract_hash]

    # Get contract info
    try:
        contract_info = get_contract_state(contract_hash, network)
    except:
        contract_info = None

    # Invoke the function
    invoke_result = invoke_function(contract_hash, method, params, network)

    # Parse the result
    stack = invoke_result.get("stack", [])
    parsed_result = [parse_stack_item(item) for item in stack]

    return {
        "success": True,
        "network": network,
        "contract": {
            "hash": contract_hash,
            "name": contract_info.get("manifest", {}).get("name") if contract_info else None
        },
        "method": method,
        "params": params,
        "invoke_result": {
            "state": invoke_result.get("state"),
            "gas_consumed": invoke_result.get("gasconsumed"),
            "exception": invoke_result.get("exception"),
            "stack": stack,
            "parsed": parsed_result[0] if len(parsed_result) == 1 else parsed_result
        }
    }


def get_contract_info(contract_hash: str, network: str = "mainnet") -> Dict:
    """Get detailed contract information"""
    # Resolve known contract names
    if contract_hash in KNOWN_CONTRACTS:
        contract_hash = KNOWN_CONTRACTS[contract_hash]

    contract_state = get_contract_state(contract_hash, network)

    manifest = contract_state.get("manifest", {})
    nef = contract_state.get("nef", {})

    # Extract ABI methods
    abi = manifest.get("abi", {})
    methods = abi.get("methods", [])
    events = abi.get("events", [])

    return {
        "success": True,
        "network": network,
        "contract": {
            "hash": contract_hash,
            "id": contract_state.get("id"),
            "name": manifest.get("name"),
            "update_counter": contract_state.get("updatecounter"),
            "nef": {
                "compiler": nef.get("compiler"),
                "source": nef.get("source"),
                "checksum": nef.get("checksum")
            }
        },
        "manifest": {
            "supported_standards": manifest.get("supportedstandards", []),
            "groups": manifest.get("groups", []),
            "permissions": manifest.get("permissions", []),
            "trusts": manifest.get("trusts", [])
        },
        "abi": {
            "methods": [
                {
                    "name": m.get("name"),
                    "parameters": m.get("parameters", []),
                    "return_type": m.get("returntype"),
                    "safe": m.get("safe", False)
                }
                for m in methods
            ],
            "events": [
                {
                    "name": e.get("name"),
                    "parameters": e.get("parameters", [])
                }
                for e in events
            ]
        }
    }


def main():
    try:
        input_data = json.loads(sys.stdin.read())

        action = input_data.get("action", "query")
        contract_hash = input_data.get("contract_hash")
        method = input_data.get("method")
        params = input_data.get("params", [])
        network = input_data.get("network", "mainnet")

        if action == "info":
            if not contract_hash:
                print(json.dumps({"error": "Missing contract_hash"}))
                sys.exit(1)
            result = get_contract_info(contract_hash, network)

        elif action == "native":
            contracts = get_native_contracts(network)
            result = {
                "success": True,
                "network": network,
                "native_contracts": [
                    {
                        "name": c.get("manifest", {}).get("name"),
                        "hash": c.get("hash"),
                        "id": c.get("id")
                    }
                    for c in contracts
                ]
            }

        else:  # query
            if not contract_hash or not method:
                print(json.dumps({"error": "Missing contract_hash or method"}))
                sys.exit(1)
            result = query_contract(contract_hash, method, params, network)

        print(json.dumps(result, indent=2))

    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input"}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
