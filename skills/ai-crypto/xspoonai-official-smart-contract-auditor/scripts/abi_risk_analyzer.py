#!/usr/bin/env python3
"""
ABI Risk Analyzer
Deep analysis of contract ABI for access control patterns, admin functions,
upgrade mechanisms, and privilege escalation risks.

Author: Nihal Nihalani
Version: 1.0.0
"""

import json
import sys
import urllib.request
import urllib.error
import re

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

# Admin/privileged function name patterns
ADMIN_PATTERNS = [
    # Ownership
    ("transferOwnership", "ownership", "HIGH", "Transfers contract ownership"),
    ("renounceOwnership", "ownership", "MEDIUM", "Renounces ownership permanently"),
    ("setOwner", "ownership", "HIGH", "Sets new contract owner"),
    ("changeOwner", "ownership", "HIGH", "Changes contract owner"),
    ("acceptOwnership", "ownership", "MEDIUM", "Accepts ownership transfer"),
    # Role management
    ("grantRole", "access_control", "HIGH", "Grants a role to an address"),
    ("revokeRole", "access_control", "HIGH", "Revokes a role from an address"),
    ("setRole", "access_control", "HIGH", "Sets role for an address"),
    ("addAdmin", "access_control", "HIGH", "Adds an admin"),
    ("removeAdmin", "access_control", "HIGH", "Removes an admin"),
    ("setAdmin", "access_control", "HIGH", "Sets admin address"),
    # Minting
    ("mint", "minting", "HIGH", "Can create new tokens"),
    ("mintTo", "minting", "HIGH", "Can mint tokens to specific address"),
    ("batchMint", "minting", "HIGH", "Can batch mint tokens"),
    ("configureMinter", "minting", "HIGH", "Can configure minting authority"),
    ("updateMasterMinter", "minting", "HIGH", "Can change master minter"),
    # Burning
    ("burn", "burning", "MEDIUM", "Can destroy tokens"),
    ("burnFrom", "burning", "MEDIUM", "Can burn tokens from other addresses"),
    # Pausing
    ("pause", "pause_control", "MEDIUM", "Can freeze contract operations"),
    ("unpause", "pause_control", "MEDIUM", "Can unfreeze contract operations"),
    ("freeze", "pause_control", "MEDIUM", "Can freeze operations"),
    # Blacklisting
    ("blacklist", "blacklisting", "MEDIUM", "Can blacklist addresses"),
    ("unBlacklist", "blacklisting", "MEDIUM", "Can remove blacklist"),
    ("addToBlacklist", "blacklisting", "MEDIUM", "Can add to blacklist"),
    ("block", "blacklisting", "MEDIUM", "Can block addresses"),
    # Fee/tax control
    ("setFee", "fee_control", "HIGH", "Can modify fees"),
    ("setTax", "fee_control", "HIGH", "Can modify taxes"),
    ("updateFee", "fee_control", "HIGH", "Can update fee structure"),
    ("setSwapFee", "fee_control", "HIGH", "Can set swap fees"),
    # Upgrades
    ("upgradeTo", "upgrade", "CRITICAL", "Can upgrade contract implementation"),
    ("upgradeToAndCall", "upgrade", "CRITICAL", "Can upgrade and call initialization"),
    ("setImplementation", "upgrade", "CRITICAL", "Can set new implementation"),
    # Withdrawal
    ("withdraw", "withdrawal", "HIGH", "Can withdraw funds"),
    ("withdrawAll", "withdrawal", "CRITICAL", "Can withdraw all funds"),
    ("emergencyWithdraw", "withdrawal", "CRITICAL", "Emergency fund withdrawal"),
    ("sweep", "withdrawal", "HIGH", "Can sweep tokens from contract"),
    ("rescueTokens", "withdrawal", "HIGH", "Can rescue tokens"),
    # Configuration
    ("setRouter", "configuration", "HIGH", "Can change router address"),
    ("setFactory", "configuration", "HIGH", "Can change factory address"),
    ("setOracle", "configuration", "HIGH", "Can change oracle address"),
    ("setTreasury", "configuration", "HIGH", "Can change treasury address"),
    ("setBaseURI", "configuration", "MEDIUM", "Can change NFT metadata URI"),
    # Destruction
    ("selfdestruct", "destruction", "CRITICAL", "Can destroy the contract"),
    ("kill", "destruction", "CRITICAL", "Can destroy the contract"),
]

# Access control pattern indicators
ACCESS_CONTROL_EVENTS = {
    "OwnershipTransferred": "Ownable",
    "RoleGranted": "AccessControl",
    "RoleRevoked": "AccessControl",
    "RoleAdminChanged": "AccessControl",
    "AdminChanged": "TransparentProxy",
    "Upgraded": "UUPSProxy",
    "BeaconUpgraded": "BeaconProxy",
}


def fetch_json(url: str, timeout: int = 20) -> dict:
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


def fetch_abi(address: str, chain_id: str) -> tuple:
    """Fetch contract ABI from Blockscout or Sourcify."""
    contract_name = "Unknown"
    abi = None
    proxy_info = None

    # Try Blockscout first
    base_url = BLOCKSCOUT_CHAINS.get(chain_id)
    if base_url:
        url = f"{base_url}/api/v2/smart-contracts/{address}"
        data = fetch_json(url)
        if data and isinstance(data, dict) and data.get("abi"):
            abi = data["abi"]
            contract_name = data.get("name", "Unknown")
            if data.get("proxy_type"):
                proxy_info = {
                    "proxy_type": data["proxy_type"],
                    "implementations": [
                        {
                            "address": impl.get("address_hash", ""),
                            "name": impl.get("name", "Unknown"),
                        }
                        for impl in data.get("implementations", [])
                    ],
                }

    # Fallback to Sourcify
    if not abi:
        url = f"{SOURCIFY_API}/v2/contract/{chain_id}/{address}?fields=abi,compilation"
        data = fetch_json(url)
        if data and isinstance(data, dict) and data.get("abi"):
            abi = data["abi"]
            contract_name = data.get("compilation", {}).get("name", "Unknown")

    if not abi:
        raise ValueError(
            f"Could not fetch ABI for {address}. "
            "Contract may not be verified on Blockscout or Sourcify."
        )

    return abi, contract_name, proxy_info


def parse_abi(abi: list) -> dict:
    """Parse ABI into categorized components."""
    functions = []
    events = []
    errors = []

    for item in abi:
        item_type = item.get("type", "")

        if item_type == "function":
            name = item.get("name", "")
            inputs = item.get("inputs", [])
            outputs = item.get("outputs", [])
            mutability = item.get("stateMutability", "nonpayable")

            input_types = ",".join(i.get("type", "") for i in inputs)
            output_types = ",".join(o.get("type", "") for o in outputs)

            functions.append({
                "name": name,
                "signature": f"{name}({input_types})",
                "inputs": [
                    {"name": i.get("name", ""), "type": i.get("type", "")}
                    for i in inputs
                ],
                "output_types": output_types,
                "state_mutability": mutability,
                "is_read_only": mutability in ("view", "pure"),
                "is_payable": mutability == "payable",
            })

        elif item_type == "event":
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

        elif item_type == "error":
            errors.append({
                "name": item.get("name", ""),
                "inputs": [
                    {"name": i.get("name", ""), "type": i.get("type", "")}
                    for i in item.get("inputs", [])
                ],
            })

    return {"functions": functions, "events": events, "errors": errors}


def detect_access_control(events: list, functions: list) -> dict:
    """Detect access control patterns from events and functions."""
    patterns_detected = []
    event_names = {e["name"] for e in events}
    func_names = {f["name"].lower() for f in functions}

    for event_name, pattern in ACCESS_CONTROL_EVENTS.items():
        if event_name in event_names:
            patterns_detected.append(pattern)

    # Check for common role-based functions
    if "hasrole" in func_names or "getroleadmin" in func_names:
        if "AccessControl" not in patterns_detected:
            patterns_detected.append("AccessControl")

    if "owner" in func_names or "getowner" in func_names:
        if "Ownable" not in patterns_detected:
            patterns_detected.append("Ownable")

    # Deduplicate
    patterns_detected = list(set(patterns_detected))

    if not patterns_detected:
        primary = "Unknown"
    elif len(patterns_detected) == 1:
        primary = patterns_detected[0]
    else:
        primary = "Multiple (" + ", ".join(sorted(patterns_detected)) + ")"

    return {
        "pattern": primary,
        "patterns_detected": sorted(patterns_detected),
        "has_ownership": any(p in patterns_detected for p in ["Ownable"]),
        "has_roles": any(p in patterns_detected for p in ["AccessControl"]),
        "is_upgradeable": any(
            p in patterns_detected
            for p in ["UUPSProxy", "TransparentProxy", "BeaconProxy"]
        ),
    }


def find_admin_functions(functions: list) -> list:
    """Identify admin/privileged functions."""
    admin_funcs = []
    func_names_lower = {f["name"].lower(): f for f in functions}

    for pattern_name, category, risk, description in ADMIN_PATTERNS:
        name_lower = pattern_name.lower()
        if name_lower in func_names_lower:
            func = func_names_lower[name_lower]
            admin_funcs.append({
                "name": func["name"],
                "signature": func["signature"],
                "inputs": func["inputs"],
                "category": category,
                "risk": risk,
                "description": description,
                "is_payable": func["is_payable"],
            })

    # Also check for 'set*' functions that are state-changing
    for func in functions:
        name = func["name"]
        if (
            name.startswith("set")
            and not func["is_read_only"]
            and name.lower() not in {p[0].lower() for p in ADMIN_PATTERNS}
            and len(name) > 3
        ):
            admin_funcs.append({
                "name": name,
                "signature": func["signature"],
                "inputs": func["inputs"],
                "category": "configuration",
                "risk": "MEDIUM",
                "description": f"Configuration setter: {name}",
                "is_payable": func["is_payable"],
            })

    # Sort by risk
    risk_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    admin_funcs.sort(key=lambda x: risk_order.get(x["risk"], 4))

    return admin_funcs


def analyze_event_coverage(functions: list, events: list) -> dict:
    """Analyze whether state-changing functions emit events."""
    state_changing = [f for f in functions if not f["is_read_only"]]
    event_names_lower = {e["name"].lower() for e in events}

    # Heuristic: check if common state-changing operations have corresponding events
    covered = 0
    uncovered = []

    for func in state_changing:
        name_lower = func["name"].lower()
        # Check if there's a corresponding event
        has_event = False
        for ename in event_names_lower:
            if name_lower in ename or ename in name_lower:
                has_event = True
                break
        if has_event:
            covered += 1
        else:
            uncovered.append(func["name"])

    total = len(state_changing)
    coverage = round(covered / total * 100, 1) if total > 0 else 100.0

    return {
        "total_state_changing": total,
        "with_events": covered,
        "without_events": len(uncovered),
        "coverage_percent": coverage,
        "uncovered_functions": uncovered[:10],
    }


def analyze_abi(contract_address: str, chain: str = "ethereum") -> dict:
    """Run comprehensive ABI risk analysis."""
    contract_address = validate_address(contract_address)
    chain_id = validate_chain(chain)

    # Fetch ABI
    abi, contract_name, proxy_info = fetch_abi(contract_address, chain_id)

    # Parse ABI
    parsed = parse_abi(abi)
    functions = parsed["functions"]
    events = parsed["events"]
    errors = parsed["errors"]

    # Detect access control patterns
    access_control = detect_access_control(events, functions)

    # Find admin functions
    admin_functions = find_admin_functions(functions)

    # Analyze event coverage
    event_coverage = analyze_event_coverage(functions, events)

    # Count function categories
    read_only = sum(1 for f in functions if f["is_read_only"])
    payable = sum(1 for f in functions if f["is_payable"])
    state_changing = len(functions) - read_only

    # Calculate risk score
    score = 0
    factors = []

    # Upgrade risk
    if access_control["is_upgradeable"]:
        score += 2
        factors.append({
            "factor": "Upgradeable contract",
            "impact": "+2",
            "detail": "Implementation can be changed by admin",
        })

    # Admin function count
    critical_admin = len([f for f in admin_functions if f["risk"] == "CRITICAL"])
    high_admin = len([f for f in admin_functions if f["risk"] == "HIGH"])

    if critical_admin > 0:
        score += critical_admin * 2
        factors.append({
            "factor": f"{critical_admin} critical admin function(s)",
            "impact": f"+{critical_admin * 2}",
            "detail": ", ".join(
                f["name"] for f in admin_functions if f["risk"] == "CRITICAL"
            ),
        })

    if high_admin > 3:
        score += 2
        factors.append({
            "factor": f"{high_admin} high-risk admin functions",
            "impact": "+2",
            "detail": "Excessive privileged functions indicate centralization risk",
        })
    elif high_admin > 0:
        score += 1
        factors.append({
            "factor": f"{high_admin} high-risk admin function(s)",
            "impact": "+1",
            "detail": ", ".join(
                f["name"] for f in admin_functions if f["risk"] == "HIGH"
            )[:120],
        })

    # Low event coverage
    if event_coverage["coverage_percent"] < 50 and state_changing > 3:
        score += 1
        factors.append({
            "factor": "Low event coverage",
            "impact": "+1",
            "detail": f"Only {event_coverage['coverage_percent']}% of state-changing functions have events",
        })

    # Payable functions
    if payable > 3:
        score += 1
        factors.append({
            "factor": f"{payable} payable functions",
            "impact": "+1",
            "detail": "Multiple functions accept ETH",
        })

    # Positive signals
    if access_control["has_roles"]:
        factors.append({
            "factor": "Role-based access control",
            "impact": "0 (positive signal)",
            "detail": "Uses granular role-based permissions",
        })

    if event_coverage["coverage_percent"] >= 80:
        factors.append({
            "factor": "Good event coverage",
            "impact": "0 (positive signal)",
            "detail": f"{event_coverage['coverage_percent']}% of state-changing functions emit events",
        })

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
        "scan_type": "abi_risk_analysis",
        "contract": {
            "address": contract_address,
            "name": contract_name,
            "chain": chain,
            "chain_id": chain_id,
        },
        "proxy": proxy_info,
        "abi_summary": {
            "total_functions": len(functions),
            "read_only": read_only,
            "state_changing": state_changing,
            "payable": payable,
            "events": len(events),
            "errors": len(errors),
        },
        "access_control": {
            "pattern": access_control["pattern"],
            "has_ownership": access_control["has_ownership"],
            "has_roles": access_control["has_roles"],
            "is_upgradeable": access_control["is_upgradeable"],
            "admin_function_count": len(admin_functions),
        },
        "admin_inventory": admin_functions[:20],
        "event_coverage": event_coverage,
        "all_functions": [
            {
                "name": f["name"],
                "mutability": f["state_mutability"],
                "is_read_only": f["is_read_only"],
            }
            for f in functions
        ],
        "risk_assessment": {
            "score": score,
            "level": level,
            "factors": factors,
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
                            "contract_address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
                            "chain": "ethereum",
                        },
                    }
                )
            )
            sys.exit(1)

        result = analyze_abi(contract_address, chain)
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
