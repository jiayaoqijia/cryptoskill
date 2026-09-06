#!/usr/bin/env python3
"""
Token Risk Scanner
Scans a token contract for honeypot indicators, rug pull risks,
tax manipulation, and ownership dangers using the GoPlus Security API.

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

SUPPORTED_CHAINS = sorted(set(CHAIN_IDS.keys()))


def fetch_json(url: str, timeout: int = 20) -> dict:
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


def scan_token(address: str, chain: str = "ethereum") -> dict:
    """Scan a token contract for risks using GoPlus Security API."""
    address = validate_address(address)
    chain_id = validate_chain(chain)

    url = (
        f"{GOPLUS_API}/token_security/{chain_id}"
        f"?contract_addresses={address}"
    )

    data = fetch_json(url)
    if not data or data.get("code") != 1:
        raise ConnectionError(
            "GoPlus API returned an unexpected response. "
            "The token may not be indexed yet. Try again later."
        )

    result = data.get("result", {})
    token_data = result.get(address, result.get(address.lower(), {}))

    if not token_data:
        return {
            "success": True,
            "scan_type": "token_risk",
            "address": address,
            "chain": chain,
            "chain_id": chain_id,
            "token_found": False,
            "risk_score": 5,
            "risk_level": "MEDIUM",
            "summary": (
                "Token not found in GoPlus database. This could mean the "
                "token is very new, has low liquidity, or is not yet indexed. "
                "Proceed with extreme caution."
            ),
            "findings": [],
            "recommendations": [
                "Token is not indexed by GoPlus - this is unusual for legitimate tokens",
                "Verify the contract address is correct",
                "Check if the token has any trading activity on DEXes",
                "Do NOT invest significant funds until the token is indexed",
            ],
        }

    # Analyze the token data
    findings = []
    score = 0

    # --- Critical risks (score += 3-4 each) ---
    if token_data.get("is_honeypot") == "1":
        score += 4
        findings.append({
            "severity": "CRITICAL",
            "category": "honeypot",
            "finding": "Honeypot detected",
            "detail": "This token cannot be sold after buying. Your funds will be permanently trapped.",
        })

    if token_data.get("hidden_owner") == "1":
        score += 3
        findings.append({
            "severity": "CRITICAL",
            "category": "ownership",
            "finding": "Hidden owner detected",
            "detail": "The contract has a concealed ownership mechanism. The real owner can execute privileged functions.",
        })

    if token_data.get("owner_change_balance") == "1":
        score += 3
        findings.append({
            "severity": "CRITICAL",
            "category": "balance_manipulation",
            "finding": "Owner can modify balances",
            "detail": "The contract owner can arbitrarily change token balances, potentially draining your holdings.",
        })

    if token_data.get("can_take_back_ownership") == "1":
        score += 3
        findings.append({
            "severity": "CRITICAL",
            "category": "ownership",
            "finding": "Ownership can be reclaimed",
            "detail": "Even if ownership appears renounced, it can be taken back. Renounced ownership is fake.",
        })

    if token_data.get("selfdestruct") == "1":
        score += 3
        findings.append({
            "severity": "CRITICAL",
            "category": "destruction",
            "finding": "Self-destruct capability",
            "detail": "The contract can be destroyed, permanently locking all tokens inside.",
        })

    if token_data.get("external_call") == "1":
        score += 2
        findings.append({
            "severity": "HIGH",
            "category": "external_call",
            "finding": "External call risk",
            "detail": "Contract makes external calls that could be manipulated to change behavior.",
        })

    # --- High risks (score += 2 each) ---
    sell_tax = float(token_data.get("sell_tax", "0") or "0") * 100
    buy_tax = float(token_data.get("buy_tax", "0") or "0") * 100

    if sell_tax > 50:
        score += 3
        findings.append({
            "severity": "CRITICAL",
            "category": "tax",
            "finding": f"Extreme sell tax: {sell_tax:.1f}%",
            "detail": "Selling this token will cost more than half your value. This is a strong scam indicator.",
        })
    elif sell_tax > 10:
        score += 2
        findings.append({
            "severity": "HIGH",
            "category": "tax",
            "finding": f"High sell tax: {sell_tax:.1f}%",
            "detail": "Selling this token incurs a significant tax that reduces your proceeds.",
        })
    elif sell_tax > 5:
        score += 1
        findings.append({
            "severity": "MEDIUM",
            "category": "tax",
            "finding": f"Moderate sell tax: {sell_tax:.1f}%",
            "detail": "Selling incurs a noticeable tax. This may be by design but warrants attention.",
        })

    if buy_tax > 50:
        score += 3
        findings.append({
            "severity": "CRITICAL",
            "category": "tax",
            "finding": f"Extreme buy tax: {buy_tax:.1f}%",
            "detail": "Buying this token costs more than half in taxes. Strong scam indicator.",
        })
    elif buy_tax > 10:
        score += 2
        findings.append({
            "severity": "HIGH",
            "category": "tax",
            "finding": f"High buy tax: {buy_tax:.1f}%",
            "detail": "Buying this token incurs a significant tax.",
        })
    elif buy_tax > 5:
        score += 1
        findings.append({
            "severity": "MEDIUM",
            "category": "tax",
            "finding": f"Moderate buy tax: {buy_tax:.1f}%",
            "detail": "Buying incurs a noticeable tax.",
        })

    if token_data.get("slippage_modifiable") == "1":
        score += 2
        findings.append({
            "severity": "HIGH",
            "category": "tax",
            "finding": "Tax rates can be modified",
            "detail": "The owner can change buy/sell tax rates at any time. Taxes could be raised to 100% after you buy.",
        })

    if token_data.get("is_anti_whale") == "1":
        findings.append({
            "severity": "LOW",
            "category": "restriction",
            "finding": "Anti-whale mechanism",
            "detail": "Transaction size limits are in place. This can be legitimate or used to trap large holders.",
        })

    if token_data.get("anti_whale_modifiable") == "1":
        score += 1
        findings.append({
            "severity": "MEDIUM",
            "category": "restriction",
            "finding": "Anti-whale limits are modifiable",
            "detail": "The owner can change transaction limits, potentially restricting your ability to sell.",
        })

    # --- Medium risks (score += 1 each) ---
    if token_data.get("is_blacklisted") == "1":
        score += 1
        findings.append({
            "severity": "MEDIUM",
            "category": "blacklist",
            "finding": "Blacklist function exists",
            "detail": "The contract can blacklist addresses, preventing them from trading.",
        })

    if token_data.get("transfer_pausable") == "1":
        score += 1
        findings.append({
            "severity": "MEDIUM",
            "category": "pause",
            "finding": "Transfers can be paused",
            "detail": "The owner can freeze all token transfers at any time.",
        })

    if token_data.get("is_mintable") == "1":
        score += 1
        findings.append({
            "severity": "MEDIUM",
            "category": "supply",
            "finding": "Token is mintable",
            "detail": "New tokens can be minted, potentially diluting existing holders.",
        })

    if token_data.get("is_proxy") == "1":
        score += 1
        findings.append({
            "severity": "MEDIUM",
            "category": "proxy",
            "finding": "Proxy contract (upgradeable)",
            "detail": "The contract logic can be changed at any time through an upgrade.",
        })

    if token_data.get("is_open_source") != "1":
        score += 2
        findings.append({
            "severity": "HIGH",
            "category": "transparency",
            "finding": "Source code not verified",
            "detail": "Contract source code is not publicly verified. Cannot inspect what the contract does.",
        })

    # --- Positive signals (reduce score) ---
    if token_data.get("trust_list") == "1":
        score = max(0, score - 3)
        findings.append({
            "severity": "INFO",
            "category": "trust",
            "finding": "On GoPlus trusted list",
            "detail": "This token is recognized and trusted by GoPlus Security.",
        })

    if token_data.get("is_open_source") == "1":
        findings.append({
            "severity": "INFO",
            "category": "transparency",
            "finding": "Source code verified",
            "detail": "Contract source code is publicly available and verified.",
        })

    if token_data.get("is_in_dex") == "1":
        findings.append({
            "severity": "INFO",
            "category": "liquidity",
            "finding": "Listed on DEX",
            "detail": "Token has active DEX liquidity pools.",
        })

    owner_address = token_data.get("owner_address", "")
    if owner_address == "0x0000000000000000000000000000000000000000":
        findings.append({
            "severity": "INFO",
            "category": "ownership",
            "finding": "Ownership renounced",
            "detail": "Contract ownership has been renounced to the zero address.",
        })

    # Cap score at 10
    score = min(score, 10)

    # Determine risk level
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

    # Generate summary
    critical_count = sum(1 for f in findings if f["severity"] == "CRITICAL")
    high_count = sum(1 for f in findings if f["severity"] == "HIGH")

    if score >= 8:
        summary = (
            f"CRITICAL RISK: {critical_count} critical issue(s) detected. "
            "This token is very likely a scam or honeypot. Do NOT interact."
        )
    elif score >= 6:
        summary = (
            f"HIGH RISK: {high_count} high-severity issue(s) found. "
            "Interacting with this token carries significant risk."
        )
    elif score >= 4:
        summary = (
            "MEDIUM RISK: Some concerning features detected. "
            "Review findings carefully before proceeding."
        )
    elif score >= 2:
        summary = (
            "LOW RISK: Minor concerns found but no major red flags. "
            "Generally safe, but review the findings."
        )
    else:
        summary = (
            "SAFE: No significant risks detected. "
            "The token appears legitimate based on available data."
        )

    # Generate recommendations
    recommendations = []
    if critical_count > 0:
        recommendations.append(
            "AVOID this token entirely - critical risks detected"
        )
    if token_data.get("is_honeypot") == "1":
        recommendations.append(
            "Do NOT buy - this is a confirmed honeypot (cannot sell)"
        )
    if sell_tax > 10 or buy_tax > 10:
        recommendations.append(
            f"Account for taxes in your calculations: "
            f"buy tax {buy_tax:.1f}%, sell tax {sell_tax:.1f}%"
        )
    if token_data.get("slippage_modifiable") == "1":
        recommendations.append(
            "Be aware that tax rates can change at any time"
        )
    if token_data.get("is_open_source") != "1":
        recommendations.append(
            "Source code is unverified - consider using only verified contracts"
        )
    if token_data.get("is_proxy") == "1":
        recommendations.append(
            "Contract is upgradeable - behavior can change without notice"
        )
    if token_data.get("is_mintable") == "1":
        recommendations.append(
            "Monitor minting events - new supply can dilute your holdings"
        )
    if not recommendations:
        recommendations.append(
            "No immediate action required, but always DYOR"
        )

    # Token metadata
    token_info = {
        "name": token_data.get("token_name", "Unknown"),
        "symbol": token_data.get("token_symbol", "Unknown"),
        "holder_count": token_data.get("holder_count", "Unknown"),
        "total_supply": token_data.get("total_supply", "Unknown"),
        "creator": token_data.get("creator_address", "Unknown"),
        "owner": token_data.get("owner_address", "Unknown"),
    }

    # Top holders
    holders = []
    for holder in token_data.get("holders", [])[:5]:
        pct = float(holder.get("percent", 0)) * 100
        holders.append({
            "address": holder.get("address", "Unknown"),
            "percent": round(pct, 2),
            "is_locked": holder.get("is_locked") == 1,
            "is_contract": holder.get("is_contract") == 1,
        })

    # DEX info
    dex_info = []
    for dex in token_data.get("dex", [])[:5]:
        dex_info.append({
            "name": dex.get("name", "Unknown"),
            "liquidity": dex.get("liquidity", "0"),
            "pair": dex.get("pair", "Unknown"),
        })

    return {
        "success": True,
        "scan_type": "token_risk",
        "address": address,
        "chain": chain,
        "chain_id": chain_id,
        "token_found": True,
        "token_info": token_info,
        "risk_score": score,
        "risk_level": level,
        "summary": summary,
        "taxes": {
            "buy_tax_percent": round(buy_tax, 2),
            "sell_tax_percent": round(sell_tax, 2),
            "tax_modifiable": token_data.get("slippage_modifiable") == "1",
        },
        "findings": findings,
        "top_holders": holders,
        "dex_info": dex_info,
        "recommendations": recommendations,
    }


def main() -> None:
    """Main entry point. Reads JSON from stdin."""
    try:
        input_data = json.loads(sys.stdin.read())

        address = input_data.get("address", "")
        chain = input_data.get("chain", "ethereum")

        if not address:
            print(json.dumps({
                "error": "Missing required parameter: 'address'",
                "usage": {
                    "address": "0xTokenContractAddress",
                    "chain": "ethereum (optional, default: ethereum)",
                },
                "supported_chains": SUPPORTED_CHAINS,
            }))
            sys.exit(1)

        result = scan_token(address, chain)
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
