#!/usr/bin/env python3
"""
Wallet Approval Audit
Audits a wallet's ERC20 token approvals to find unlimited or dangerous
approvals that could drain funds. Uses Blockscout API for approval data
and GoPlus for spender security checks.

Author: Nihal Nihalani
Version: 1.0.0
"""

import json
import sys
import urllib.request
import urllib.error
import re

GOPLUS_API = "https://api.gopluslabs.io/api/v1"

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

BLOCKSCOUT_CHAINS = {
    "1": "https://eth.blockscout.com",
    "56": "https://bsc.blockscout.com",
    "137": "https://polygon.blockscout.com",
    "42161": "https://arbitrum.blockscout.com",
    "8453": "https://base.blockscout.com",
    "10": "https://optimism.blockscout.com",
    "43114": "https://avax.blockscout.com",
}

SUPPORTED_CHAINS = sorted(set(CHAIN_IDS.keys()))

# Maximum allowance that indicates "unlimited" approval
# This is the max uint256 value
MAX_UINT256 = 2**256 - 1
UNLIMITED_THRESHOLD = MAX_UINT256 // 2  # Anything above half of max is "unlimited"


def fetch_json(url: str, timeout: int = 25) -> dict:
    """Fetch JSON data from a URL with error handling."""
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "DeFiSafetyShield/1.0",
                "Accept": "application/json",
            },
        )
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 429:
            raise ConnectionError(
                "Rate limit exceeded. Please wait 1-2 minutes before retrying."
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
    """Validate chain name and return chain ID."""
    chain_lower = chain.lower().strip()
    chain_id = CHAIN_IDS.get(chain_lower)
    if not chain_id:
        raise ValueError(
            f"Unsupported chain: {chain}. "
            f"Supported: {', '.join(SUPPORTED_CHAINS)}"
        )
    return chain_id


def fetch_approvals_blockscout(wallet: str, chain_id: str) -> list:
    """Fetch token approval events from Blockscout."""
    base_url = BLOCKSCOUT_CHAINS.get(chain_id)
    if not base_url:
        raise ConnectionError(
            f"Blockscout not available for chain ID {chain_id}. "
            "Try ethereum, bsc, polygon, arbitrum, base, optimism, or avalanche."
        )

    url = (
        f"{base_url}/api/v2/addresses/{wallet}/token-transfers"
        f"?type=ERC-20&filter=approval"
    )

    try:
        data = fetch_json(url)
        if data and "items" in data:
            return data["items"]
    except ConnectionError:
        pass

    return []


def check_spender_security(spender: str, chain_id: str) -> dict:
    """Check if a spender contract is safe using GoPlus and Blockscout."""
    result = {
        "is_verified": None,
        "is_malicious": False,
        "contract_name": None,
        "flags": [],
    }

    # Check GoPlus address security
    try:
        goplus_url = f"{GOPLUS_API}/address_security/{spender}?chain_id={chain_id}"
        data = fetch_json(goplus_url)
        if data and data.get("code") == 1:
            sec = data.get("result", {})
            malicious_keys = [
                "cybercrime", "money_laundering", "phishing_activities",
                "stealing_attack", "honeypot_related_address",
            ]
            for key in malicious_keys:
                if sec.get(key) == "1":
                    result["is_malicious"] = True
                    result["flags"].append(key.replace("_", " ").title())
    except ConnectionError:
        pass

    # Check Blockscout for contract info
    base_url = BLOCKSCOUT_CHAINS.get(chain_id)
    if base_url:
        try:
            contract_url = f"{base_url}/api/v2/smart-contracts/{spender}"
            data = fetch_json(contract_url)
            if data and isinstance(data, dict):
                result["is_verified"] = data.get("is_verified", False)
                result["contract_name"] = data.get("name")
        except ConnectionError:
            pass

    return result


def classify_allowance(value_str: str, decimals: int = 18) -> dict:
    """Classify a token allowance value."""
    try:
        value = int(value_str)
    except (ValueError, TypeError):
        return {"raw": value_str, "classification": "unknown", "risk": "MEDIUM"}

    if value == 0:
        return {"raw": "0", "classification": "revoked", "risk": "SAFE"}

    if value >= UNLIMITED_THRESHOLD:
        return {
            "raw": value_str,
            "classification": "unlimited",
            "risk": "HIGH",
            "detail": "Unlimited approval - spender can transfer ALL your tokens",
        }

    # Try to format with decimals
    try:
        human_readable = value / (10 ** decimals)
        if human_readable > 1_000_000:
            formatted = f"{human_readable:,.0f}"
        else:
            formatted = f"{human_readable:,.4f}"
    except (OverflowError, ZeroDivisionError):
        formatted = value_str

    if value >= 10 ** (decimals + 6):  # More than 1M tokens
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return {
        "raw": value_str,
        "formatted": formatted,
        "classification": "limited",
        "risk": risk,
    }


def audit_approvals(wallet_address: str, chain: str = "ethereum") -> dict:
    """Audit all token approvals for a wallet."""
    wallet_address = validate_address(wallet_address)
    chain_id = validate_chain(chain)

    # Fetch approval events from Blockscout
    raw_approvals = fetch_approvals_blockscout(wallet_address, chain_id)

    if not raw_approvals:
        return {
            "success": True,
            "scan_type": "approval_audit",
            "wallet_address": wallet_address,
            "chain": chain,
            "chain_id": chain_id,
            "total_approvals": 0,
            "risk_score": 0,
            "risk_level": "SAFE",
            "summary": (
                "No token approvals found for this wallet on this chain. "
                "Either the wallet has no approvals, or the data is not yet indexed."
            ),
            "approvals": [],
            "recommendations": [
                "If you expected approvals, try checking on a different chain",
                "Approvals may take time to be indexed by Blockscout",
            ],
        }

    # Process approvals - deduplicate by (token, spender) keeping latest
    seen = {}
    for item in raw_approvals:
        token = item.get("token", {})
        token_address = token.get("address", "").lower()
        # The 'to' field in an approval is the spender
        spender = (item.get("to", {}) or {}).get("hash", "").lower()

        if not token_address or not spender:
            continue

        key = f"{token_address}:{spender}"
        # Keep the most recent approval
        existing = seen.get(key)
        if not existing:
            seen[key] = item
        else:
            existing_block = int((existing.get("block_number") or 0))
            current_block = int((item.get("block_number") or 0))
            if current_block > existing_block:
                seen[key] = item

    # Analyze each unique approval
    approvals = []
    unlimited_count = 0
    high_risk_count = 0
    checked_spenders = {}

    for key, item in seen.items():
        token = item.get("token", {})
        token_address = token.get("address", "").lower()
        token_name = token.get("name", "Unknown")
        token_symbol = token.get("symbol", "???")
        token_decimals = int(token.get("decimals", "18") or "18")

        spender = (item.get("to", {}) or {}).get("hash", "").lower()
        total_value = item.get("total", {})
        value_str = total_value.get("value", "0") if isinstance(total_value, dict) else str(total_value)

        # Classify the allowance
        allowance = classify_allowance(value_str, token_decimals)

        # Skip revoked approvals
        if allowance["classification"] == "revoked":
            continue

        if allowance["classification"] == "unlimited":
            unlimited_count += 1

        # Check spender security (cache results)
        if spender not in checked_spenders:
            checked_spenders[spender] = check_spender_security(spender, chain_id)
        spender_info = checked_spenders[spender]

        # Determine risk for this approval
        approval_risk = "LOW"
        risk_reasons = []

        if allowance["classification"] == "unlimited":
            approval_risk = "HIGH"
            risk_reasons.append("Unlimited approval - spender can take all tokens")

        if spender_info.get("is_malicious"):
            approval_risk = "CRITICAL"
            risk_reasons.append(f"Spender flagged as malicious: {', '.join(spender_info['flags'])}")
            high_risk_count += 1

        if spender_info.get("is_verified") is False:
            if approval_risk != "CRITICAL":
                approval_risk = "HIGH" if allowance["classification"] == "unlimited" else "MEDIUM"
            risk_reasons.append("Spender contract is NOT verified on Blockscout")

        approvals.append({
            "token": {
                "address": token_address,
                "name": token_name,
                "symbol": token_symbol,
            },
            "spender": {
                "address": spender,
                "contract_name": spender_info.get("contract_name"),
                "is_verified": spender_info.get("is_verified"),
                "is_malicious": spender_info.get("is_malicious", False),
                "flags": spender_info.get("flags", []),
            },
            "allowance": allowance,
            "risk": approval_risk,
            "risk_reasons": risk_reasons,
            "block_number": item.get("block_number"),
            "tx_hash": item.get("transaction_hash"),
        })

    # Sort by risk (CRITICAL first, then HIGH, MEDIUM, LOW)
    risk_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "SAFE": 4}
    approvals.sort(key=lambda a: risk_order.get(a["risk"], 5))

    # Calculate overall risk score
    score = 0
    if high_risk_count > 0:
        score += min(high_risk_count * 3, 6)
    if unlimited_count > 5:
        score += 3
    elif unlimited_count > 2:
        score += 2
    elif unlimited_count > 0:
        score += 1

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

    # Summary
    if high_risk_count > 0:
        summary = (
            f"DANGER: {high_risk_count} approval(s) to malicious or unverified contracts detected. "
            f"Found {unlimited_count} unlimited approval(s) across {len(approvals)} active approval(s). "
            "Revoke dangerous approvals immediately."
        )
    elif unlimited_count > 5:
        summary = (
            f"HIGH RISK: {unlimited_count} unlimited approvals found. "
            "Each unlimited approval gives a contract permission to spend ALL of that token. "
            "Consider revoking unused approvals."
        )
    elif unlimited_count > 0:
        summary = (
            f"Found {unlimited_count} unlimited approval(s) out of {len(approvals)} total. "
            "Review each approval and revoke any that are no longer needed."
        )
    else:
        summary = (
            f"Found {len(approvals)} active approval(s), all with limited amounts. "
            "No critical risks detected."
        )

    # Recommendations
    recommendations = []
    if high_risk_count > 0:
        recommendations.append(
            "URGENT: Revoke approvals to flagged malicious contracts immediately using revoke.cash or etherscan"
        )
    if unlimited_count > 0:
        recommendations.append(
            f"Revoke {unlimited_count} unlimited approval(s) - use revoke.cash, etherscan token approval checker, or the protocol's UI"
        )
    recommendations.append(
        "Use limited approvals instead of unlimited when possible"
    )
    recommendations.append(
        "Regularly audit your approvals (monthly recommended)"
    )
    recommendations.append(
        "Consider using a separate wallet for DeFi interactions to limit exposure"
    )

    return {
        "success": True,
        "scan_type": "approval_audit",
        "wallet_address": wallet_address,
        "chain": chain,
        "chain_id": chain_id,
        "total_approvals": len(approvals),
        "unlimited_approvals": unlimited_count,
        "high_risk_approvals": high_risk_count,
        "risk_score": score,
        "risk_level": level,
        "summary": summary,
        "approvals": approvals,
        "recommendations": recommendations,
    }


def main() -> None:
    """Main entry point. Reads JSON from stdin."""
    try:
        input_data = json.loads(sys.stdin.read())

        wallet_address = input_data.get("wallet_address", "")
        chain = input_data.get("chain", "ethereum")

        if not wallet_address:
            print(json.dumps({
                "error": "Missing required parameter: 'wallet_address'",
                "usage": {
                    "wallet_address": "0xYourWalletAddress",
                    "chain": "ethereum (optional, default: ethereum)",
                },
                "supported_chains": SUPPORTED_CHAINS,
            }))
            sys.exit(1)

        result = audit_approvals(wallet_address, chain)
        print(json.dumps(result, indent=2))

    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON input. Send valid JSON via stdin."}))
        sys.exit(1)
    except (ValueError, ConnectionError) as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": f"Unexpected error: {type(e).__name__}"}))
        sys.exit(1)


if __name__ == "__main__":
    main()
