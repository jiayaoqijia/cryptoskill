#!/usr/bin/env python3
"""
Contract Security Audit
Comprehensive security audit combining GoPlus Security, Sourcify verification,
and Blockscout contract metadata into a unified security report.

Author: Nihal Nihalani
Version: 1.0.0
"""

import json
import sys
import urllib.request
import urllib.error
import re

GOPLUS_API = "https://api.gopluslabs.io/api/v1"
SOURCIFY_API = "https://sourcify.dev/server"

BLOCKSCOUT_CHAINS = {
    "1": "https://eth.blockscout.com",
    "56": "https://bsc.blockscout.com",
    "137": "https://polygon.blockscout.com",
    "42161": "https://arbitrum.blockscout.com",
    "8453": "https://base.blockscout.com",
    "10": "https://optimism.blockscout.com",
    "43114": "https://avax.blockscout.com",
}

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


def fetch_goplus_security(address: str, chain_id: str) -> dict:
    """Fetch contract/token security data from GoPlus."""
    url = (
        f"{GOPLUS_API}/token_security/{chain_id}"
        f"?contract_addresses={address}"
    )
    try:
        data = fetch_json(url)
        if data and data.get("code") == 1:
            result = data.get("result", {})
            return result.get(address, result.get(address.lower(), {}))
    except ConnectionError:
        pass
    return {}


def fetch_goplus_address_security(address: str) -> dict:
    """Check if the contract address has security flags."""
    url = f"{GOPLUS_API}/address_security/{address}"
    try:
        data = fetch_json(url)
        if data and data.get("code") == 1:
            return data.get("result", {})
    except ConnectionError:
        pass
    return {}


def fetch_sourcify_status(address: str, chain_id: str) -> dict:
    """Check Sourcify verification status."""
    url = f"{SOURCIFY_API}/v2/contract/{chain_id}/{address}"
    try:
        data = fetch_json(url)
        if data and isinstance(data, dict):
            return {
                "verified": True,
                "match": data.get("match", "unknown"),
                "verified_at": data.get("verifiedAt"),
            }
    except ConnectionError:
        pass
    return {"verified": False, "match": None, "verified_at": None}


def fetch_sourcify_compilation(address: str, chain_id: str) -> dict:
    """Fetch compilation details from Sourcify."""
    url = (
        f"{SOURCIFY_API}/v2/contract/{chain_id}/{address}"
        f"?fields=compilation,deployment"
    )
    try:
        data = fetch_json(url)
        if data and isinstance(data, dict):
            return {
                "compilation": data.get("compilation", {}),
                "deployment": data.get("deployment", {}),
            }
    except ConnectionError:
        pass
    return {"compilation": {}, "deployment": {}}


def fetch_blockscout_contract(address: str, chain_id: str) -> dict:
    """Fetch contract metadata from Blockscout."""
    base_url = BLOCKSCOUT_CHAINS.get(chain_id)
    if not base_url:
        return {}

    url = f"{base_url}/api/v2/smart-contracts/{address}"
    try:
        data = fetch_json(url)
        if data and isinstance(data, dict):
            return data
    except ConnectionError:
        pass
    return {}


def fetch_blockscout_address(address: str, chain_id: str) -> dict:
    """Fetch address info from Blockscout."""
    base_url = BLOCKSCOUT_CHAINS.get(chain_id)
    if not base_url:
        return {}

    url = f"{base_url}/api/v2/addresses/{address}"
    try:
        data = fetch_json(url)
        if data and isinstance(data, dict):
            return data
    except ConnectionError:
        pass
    return {}


def analyze_goplus_data(goplus: dict) -> dict:
    """Analyze GoPlus security data and extract findings."""
    flags = []
    warnings = []
    info = []
    score = 0

    if not goplus:
        return {
            "available": False,
            "flags": [],
            "warnings": [],
            "info": [],
            "score_contribution": 0,
        }

    # Critical flags
    if goplus.get("is_honeypot") == "1":
        score += 4
        flags.append("HONEYPOT: Cannot sell tokens after buying")

    if goplus.get("hidden_owner") == "1":
        score += 3
        flags.append("Hidden owner detected")

    if goplus.get("selfdestruct") == "1":
        score += 3
        flags.append("Contract has selfdestruct capability")

    if goplus.get("owner_change_balance") == "1":
        score += 3
        flags.append("Owner can modify token balances")

    if goplus.get("can_take_back_ownership") == "1":
        score += 3
        flags.append("Owner can reclaim ownership after renouncing")

    # High-severity warnings
    sell_tax = float(goplus.get("sell_tax", "0") or "0") * 100
    buy_tax = float(goplus.get("buy_tax", "0") or "0") * 100

    if sell_tax > 10:
        score += 2
        warnings.append(f"High sell tax: {sell_tax:.1f}%")
    elif sell_tax > 5:
        score += 1
        warnings.append(f"Moderate sell tax: {sell_tax:.1f}%")

    if buy_tax > 10:
        score += 2
        warnings.append(f"High buy tax: {buy_tax:.1f}%")
    elif buy_tax > 5:
        score += 1
        warnings.append(f"Moderate buy tax: {buy_tax:.1f}%")

    if goplus.get("is_blacklisted") == "1":
        score += 1
        warnings.append("Token has blacklist function")

    if goplus.get("transfer_pausable") == "1":
        score += 1
        warnings.append("Transfers can be paused")

    if goplus.get("is_mintable") == "1":
        score += 1
        warnings.append("Token is mintable")

    if goplus.get("slippage_modifiable") == "1":
        score += 2
        warnings.append("Owner can modify tax rates")

    if goplus.get("is_proxy") == "1":
        warnings.append("Contract uses proxy pattern")

    if goplus.get("is_open_source") != "1":
        score += 2
        warnings.append("Contract source code NOT verified on GoPlus")

    # Positive signals
    if goplus.get("is_open_source") == "1":
        info.append("Source code verified (GoPlus)")

    if goplus.get("trust_list") == "1":
        score = max(0, score - 3)
        info.append("Token on GoPlus trusted list")

    if goplus.get("is_in_dex") == "1":
        info.append("Listed on DEX")

    return {
        "available": True,
        "is_honeypot": goplus.get("is_honeypot") == "1",
        "is_open_source": goplus.get("is_open_source") == "1",
        "is_proxy": goplus.get("is_proxy") == "1",
        "is_mintable": goplus.get("is_mintable") == "1",
        "has_blacklist": goplus.get("is_blacklisted") == "1",
        "transfer_pausable": goplus.get("transfer_pausable") == "1",
        "buy_tax_percent": round(buy_tax, 2),
        "sell_tax_percent": round(sell_tax, 2),
        "flags": flags,
        "warnings": warnings,
        "info": info,
        "score_contribution": min(score, 10),
    }


def audit_contract(contract_address: str, chain: str = "ethereum") -> dict:
    """Run comprehensive security audit."""
    contract_address = validate_address(contract_address)
    chain_id = validate_chain(chain)

    # Fetch data from all sources
    goplus = fetch_goplus_security(contract_address, chain_id)
    goplus_address = fetch_goplus_address_security(contract_address)
    sourcify_status = fetch_sourcify_status(contract_address, chain_id)
    sourcify_details = fetch_sourcify_compilation(contract_address, chain_id)
    blockscout_contract = fetch_blockscout_contract(contract_address, chain_id)
    blockscout_address = fetch_blockscout_address(contract_address, chain_id)

    # Analyze GoPlus data
    goplus_analysis = analyze_goplus_data(goplus)

    # Analyze address security
    address_flags = []
    for key, label in [
        ("phishing_activities", "Phishing activity detected"),
        ("cybercrime", "Associated with cybercrime"),
        ("money_laundering", "Money laundering flag"),
        ("stealing_attack", "Theft attack involvement"),
        ("blackmail_activities", "Blackmail activity"),
    ]:
        if goplus_address.get(key) == "1":
            address_flags.append(label)

    # Build verification section
    verification = {
        "sourcify_verified": sourcify_status.get("verified", False),
        "sourcify_match": sourcify_status.get("match"),
        "sourcify_verified_at": sourcify_status.get("verified_at"),
        "blockscout_verified": blockscout_contract.get("is_verified", False),
    }

    # Build contract metadata
    compilation = sourcify_details.get("compilation", {})
    deployment = sourcify_details.get("deployment", {})

    contract_name = (
        compilation.get("name")
        or blockscout_contract.get("name")
        or "Unknown"
    )
    compiler_version = (
        compilation.get("compilerVersion")
        or blockscout_contract.get("compiler_version")
        or "Unknown"
    )

    # Proxy detection
    proxy_info = {
        "is_proxy": False,
        "proxy_type": None,
        "implementations": [],
    }
    if blockscout_contract.get("proxy_type"):
        proxy_info["is_proxy"] = True
        proxy_info["proxy_type"] = blockscout_contract["proxy_type"]
        proxy_info["implementations"] = [
            {
                "address": impl.get("address_hash", ""),
                "name": impl.get("name", "Unknown"),
            }
            for impl in blockscout_contract.get("implementations", [])
        ]
    elif goplus.get("is_proxy") == "1":
        proxy_info["is_proxy"] = True

    # Creator info
    creator = (
        deployment.get("deployer")
        or blockscout_address.get("creator_address_hash")
        or "Unknown"
    )

    # Calculate combined risk score
    score = 0
    factors = []

    # GoPlus score contribution
    goplus_score = goplus_analysis.get("score_contribution", 0)
    if goplus_score > 0:
        score += goplus_score
        factors.append({
            "factor": "GoPlus security flags",
            "impact": f"+{goplus_score}",
            "detail": "; ".join(
                goplus_analysis.get("flags", []) + goplus_analysis.get("warnings", [])
            )[:200],
        })

    # Verification score
    if not sourcify_status.get("verified") and not blockscout_contract.get("is_verified"):
        score += 3
        factors.append({
            "factor": "Unverified source code",
            "impact": "+3",
            "detail": "No verified source on Sourcify or Blockscout",
        })
    elif sourcify_status.get("match") == "exact_match":
        factors.append({
            "factor": "Exact source match (Sourcify)",
            "impact": "0 (positive signal)",
            "detail": "Byte-for-byte source code match",
        })
    elif sourcify_status.get("verified"):
        score += 1
        factors.append({
            "factor": "Partial source match (Sourcify)",
            "impact": "+1",
            "detail": "Source verified but metadata hash differs",
        })

    # Proxy risk
    if proxy_info["is_proxy"]:
        if not proxy_info["implementations"]:
            score += 2
            factors.append({
                "factor": "Proxy with unknown implementation",
                "impact": "+2",
                "detail": "Contract is a proxy but implementation not identified",
            })
        else:
            score += 1
            factors.append({
                "factor": "Proxy contract",
                "impact": "+1",
                "detail": f"Implementation: {proxy_info['implementations'][0].get('name', 'Unknown')}",
            })

    # Address security
    if address_flags:
        score += 4
        factors.append({
            "factor": "Address security flags",
            "impact": "+4",
            "detail": "; ".join(address_flags),
        })

    # Scam flag from Blockscout
    if blockscout_address.get("is_scam"):
        score += 4
        factors.append({
            "factor": "Marked as scam (Blockscout)",
            "impact": "+4",
            "detail": "Address is flagged as scam on Blockscout",
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

    # Generate recommendations
    recommendations = []
    if goplus_analysis.get("flags"):
        recommendations.append(
            "CRITICAL: GoPlus detected serious security issues — avoid interacting"
        )
    if not sourcify_status.get("verified") and not blockscout_contract.get("is_verified"):
        recommendations.append(
            "Source code is unverified — cannot audit contract logic"
        )
    if proxy_info["is_proxy"]:
        recommendations.append(
            "Contract is upgradeable — implementation can change at any time"
        )
    if goplus_analysis.get("warnings"):
        recommendations.append(
            f"Review {len(goplus_analysis['warnings'])} warning(s) in GoPlus analysis"
        )
    if address_flags:
        recommendations.append(
            "Address has security flags — exercise extreme caution"
        )
    if not recommendations:
        recommendations.append("No significant risks detected")

    return {
        "success": True,
        "scan_type": "security_audit",
        "contract": {
            "address": contract_address,
            "name": contract_name,
            "chain": chain,
            "chain_id": chain_id,
            "compiler": compiler_version,
            "creator": creator,
        },
        "verification": verification,
        "proxy": proxy_info,
        "goplus_security": goplus_analysis,
        "address_security": {
            "flags": address_flags if address_flags else None,
            "is_scam": blockscout_address.get("is_scam", False),
        },
        "risk_assessment": {
            "score": score,
            "level": level,
            "factors": factors,
        },
        "recommendations": recommendations,
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

        result = audit_contract(contract_address, chain)
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
