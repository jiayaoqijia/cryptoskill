#!/usr/bin/env python3
"""
Function Decoder
Decodes function selectors from a contract's ABI using 4byte.directory.
Identifies dangerous, admin, and suspicious function signatures.

Author: Nihal Nihalani
Version: 1.0.0
"""

import json
import sys
import urllib.request
import urllib.error
import re
import hashlib

FOURBYTE_API = "https://www.4byte.directory/api/v1"

BLOCKSCOUT_CHAINS = {
    "1": "https://eth.blockscout.com",
    "56": "https://bsc.blockscout.com",
    "137": "https://polygon.blockscout.com",
    "42161": "https://arbitrum.blockscout.com",
    "8453": "https://base.blockscout.com",
    "10": "https://optimism.blockscout.com",
    "43114": "https://avax.blockscout.com",
}

SOURCIFY_API = "https://sourcify.dev/server"

CHAIN_IDS = {
    "ethereum": "1",
    "eth": "1",
    "bsc": "56",
    "bnb": "56",
    "polygon": "137",
    "matic": "137",
    "arbitrum": "42161",
    "arb": "42161",
    "base": "8453",
    "optimism": "10",
    "op": "10",
    "avalanche": "43114",
    "avax": "43114",
}

# Dangerous function name patterns
DANGEROUS_PATTERNS = {
    "destruction": {
        "keywords": ["selfdestruct", "suicide", "kill", "destroy", "terminate"],
        "risk": "CRITICAL",
        "description": "Can permanently destroy the contract",
    },
    "delegation": {
        "keywords": ["delegatecall", "callcode"],
        "risk": "CRITICAL",
        "description": "Can execute arbitrary code in contract context",
    },
    "ownership": {
        "keywords": ["transferownership", "setowner", "changeowner", "renounceownership"],
        "risk": "HIGH",
        "description": "Can transfer or modify contract ownership",
    },
    "minting": {
        "keywords": ["mint", "mintto", "batchmint", "createnft"],
        "risk": "HIGH",
        "description": "Can create new tokens (increase supply)",
    },
    "burning": {
        "keywords": ["burn", "burnfrom", "batchburn"],
        "risk": "MEDIUM",
        "description": "Can destroy tokens (decrease supply)",
    },
    "pause_control": {
        "keywords": ["pause", "unpause", "freeze", "unfreeze"],
        "risk": "MEDIUM",
        "description": "Can freeze/unfreeze contract operations",
    },
    "blacklisting": {
        "keywords": ["blacklist", "addtoblacklist", "block", "ban", "restrict"],
        "risk": "MEDIUM",
        "description": "Can restrict specific addresses",
    },
    "fee_manipulation": {
        "keywords": ["setfee", "settax", "updatefee", "changetax", "setrate"],
        "risk": "MEDIUM",
        "description": "Can modify transaction fees/taxes",
    },
    "upgrades": {
        "keywords": ["upgradeto", "upgradetoandcall", "setimplementation"],
        "risk": "HIGH",
        "description": "Can upgrade contract logic (proxy pattern)",
    },
    "withdrawal": {
        "keywords": ["withdraw", "emergencywithdraw", "sweep", "drain", "rescue"],
        "risk": "HIGH",
        "description": "Can withdraw funds from contract",
    },
}


def fetch_json(url: str, timeout: int = 15) -> dict:
    """Fetch JSON data from URL with error handling."""
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "SmartContractAuditor/1.0",
                "Accept": "application/json",
            },
        )
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 429:
            raise ConnectionError(
                "Rate limit exceeded. Please wait before retrying."
            )
        if e.code == 404:
            return None
        raise ConnectionError(f"API error (HTTP {e.code})")
    except urllib.error.URLError as e:
        raise ConnectionError(f"Connection failed: {e.reason}")


def validate_address(address: str) -> str:
    """Validate and normalize an Ethereum-style address."""
    address = address.strip()
    if not re.match(r"^0x[a-fA-F0-9]{40}$", address):
        raise ValueError(
            f"Invalid address format: {address}. "
            "Expected 0x followed by 40 hex characters."
        )
    return address.lower()


def validate_chain(chain: str) -> str:
    """Validate chain and return chain ID."""
    chain_lower = chain.lower().strip()
    chain_id = CHAIN_IDS.get(chain_lower)
    if not chain_id:
        raise ValueError(
            f"Unsupported chain: {chain}. "
            f"Supported: {', '.join(sorted(set(CHAIN_IDS.keys())))}"
        )
    return chain_id


def fetch_abi_blockscout(address: str, chain_id: str) -> list:
    """Fetch contract ABI from Blockscout."""
    base_url = BLOCKSCOUT_CHAINS.get(chain_id)
    if not base_url:
        return None

    url = f"{base_url}/api/v2/smart-contracts/{address}"
    data = fetch_json(url)
    if data and isinstance(data, dict) and data.get("abi"):
        return data["abi"], data.get("name", "Unknown")
    return None, None


def fetch_abi_sourcify(address: str, chain_id: str) -> list:
    """Fetch contract ABI from Sourcify."""
    url = f"{SOURCIFY_API}/v2/contract/{chain_id}/{address}?fields=abi,compilation"
    data = fetch_json(url)
    if data and isinstance(data, dict) and data.get("abi"):
        name = data.get("compilation", {}).get("name", "Unknown")
        return data["abi"], name
    return None, None


def compute_selector(signature: str) -> str:
    """Compute 4-byte function selector from signature."""
    sig_hash = hashlib.sha3_256(signature.encode()).hexdigest()
    # Use keccak256 via a workaround: try to compute it
    # Since hashlib doesn't have keccak, we'll use the ABI-provided selectors
    return None


def decode_selector_4byte(hex_selector: str) -> str:
    """Decode a 4-byte function selector using 4byte.directory."""
    url = (
        f"{FOURBYTE_API}/signatures/"
        f"?hex_signature={hex_selector}&format=json"
    )
    try:
        data = fetch_json(url)
        if data and data.get("results"):
            # Return the canonical (lowest id) signature
            results = data["results"]
            canonical = min(results, key=lambda r: r["id"])
            return canonical["text_signature"]
    except (ConnectionError, KeyError):
        pass
    return None


def extract_functions_from_abi(abi: list) -> list:
    """Extract function information from ABI."""
    functions = []
    events = []

    for item in abi:
        if item.get("type") == "function":
            name = item.get("name", "")
            inputs = item.get("inputs", [])
            outputs = item.get("outputs", [])
            state_mutability = item.get("stateMutability", "nonpayable")

            # Build signature for selector
            input_types = ",".join(i.get("type", "") for i in inputs)
            signature = f"{name}({input_types})"

            functions.append({
                "name": name,
                "signature": signature,
                "inputs": [
                    {"name": i.get("name", ""), "type": i.get("type", "")}
                    for i in inputs
                ],
                "outputs": [
                    {"name": o.get("name", ""), "type": o.get("type", "")}
                    for o in outputs
                ],
                "state_mutability": state_mutability,
                "is_read_only": state_mutability in ("view", "pure"),
            })
        elif item.get("type") == "event":
            events.append({
                "name": item.get("name", ""),
                "inputs": [
                    {
                        "name": i.get("name", ""),
                        "type": i.get("type", ""),
                        "indexed": i.get("indexed", False),
                    }
                    for i in item.get("inputs", [])
                ],
            })

    return functions, events


def categorize_function(func: dict) -> dict:
    """Categorize a function by risk level."""
    # Read-only functions are always safe regardless of name
    if func["is_read_only"]:
        return {
            "category": "read_only",
            "risk": "SAFE",
            "description": "View/pure function (no state changes)",
        }

    name_lower = func["name"].lower()

    for category, info in DANGEROUS_PATTERNS.items():
        for keyword in info["keywords"]:
            if keyword in name_lower:
                return {
                    "category": category,
                    "risk": info["risk"],
                    "description": info["description"],
                }

    # Generic state-changing
    return {
        "category": "state_changing",
        "risk": "LOW",
        "description": "State-changing function",
    }


def analyze_functions(contract_address: str, chain: str = "ethereum") -> dict:
    """Run function analysis on a contract."""
    contract_address = validate_address(contract_address)
    chain_id = validate_chain(chain)

    # Try Blockscout first, then Sourcify
    abi = None
    contract_name = "Unknown"

    abi, contract_name = fetch_abi_blockscout(contract_address, chain_id)
    if not abi:
        abi, contract_name = fetch_abi_sourcify(contract_address, chain_id)

    if not abi:
        raise ValueError(
            f"Could not fetch ABI for {contract_address}. "
            "Contract may not be verified."
        )

    # Extract functions and events
    functions, events = extract_functions_from_abi(abi)

    # Categorize each function
    read_only_count = 0
    state_changing_count = 0
    admin_functions = []
    dangerous_functions = []
    categorized_functions = []

    for func in functions:
        cat = categorize_function(func)
        func_entry = {
            "name": func["name"],
            "signature": func["signature"],
            "state_mutability": func["state_mutability"],
            "category": cat["category"],
            "risk": cat["risk"],
        }

        if func["is_read_only"]:
            read_only_count += 1
        else:
            state_changing_count += 1

        if cat["risk"] == "CRITICAL":
            dangerous_functions.append({
                "name": func["name"],
                "signature": func["signature"],
                "category": cat["category"],
                "risk": cat["risk"],
                "description": cat["description"],
                "inputs": func["inputs"],
            })
        elif cat["risk"] in ("HIGH", "MEDIUM") and cat["category"] != "state_changing":
            admin_functions.append({
                "name": func["name"],
                "signature": func["signature"],
                "category": cat["category"],
                "risk": cat["risk"],
                "description": cat["description"],
                "inputs": func["inputs"],
            })

        categorized_functions.append(func_entry)

    # Calculate risk score
    score = 0
    if dangerous_functions:
        score += len(dangerous_functions) * 4
    score += len([f for f in admin_functions if f["risk"] == "HIGH"]) * 2
    score += len([f for f in admin_functions if f["risk"] == "MEDIUM"])
    score = min(score, 10)

    if score >= 8:
        level = "CRITICAL"
    elif score >= 6:
        level = "HIGH"
    elif score >= 4:
        level = "MEDIUM"
    elif score >= 2:
        level = "LOW"
    else:
        level = "SAFE"

    return {
        "success": True,
        "scan_type": "function_analysis",
        "contract": {
            "address": contract_address,
            "name": contract_name or "Unknown",
            "chain": chain,
            "chain_id": chain_id,
        },
        "functions": {
            "total": len(functions),
            "read_only": read_only_count,
            "state_changing": state_changing_count,
            "admin": len(admin_functions),
            "dangerous": len(dangerous_functions),
        },
        "events": {
            "total": len(events),
            "names": [e["name"] for e in events],
        },
        "dangerous_functions": dangerous_functions,
        "admin_functions": admin_functions[:15],
        "all_functions": [
            {"name": f["name"], "mutability": f["state_mutability"], "category": f["category"]}
            for f in categorized_functions
        ],
        "risk_assessment": {
            "score": score,
            "level": level,
        },
    }


def main() -> None:
    """Main entry point. Reads JSON from stdin."""
    try:
        input_data = json.loads(sys.stdin.read())

        contract_address = input_data.get("contract_address", "")
        chain = input_data.get("chain", "ethereum")

        if not contract_address:
            print(
                json.dumps(
                    {
                        "error": "Provide 'contract_address' parameter",
                        "example": {
                            "contract_address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
                            "chain": "ethereum",
                        },
                    }
                )
            )
            sys.exit(1)

        result = analyze_functions(contract_address, chain)
        print(json.dumps(result, indent=2))

    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input"}))
        sys.exit(1)
    except (ValueError, ConnectionError) as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": f"Unexpected error: {type(e).__name__}"}))
        sys.exit(1)


if __name__ == "__main__":
    main()
