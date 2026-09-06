#!/usr/bin/env python3
"""
Phishing Detector
Analyzes URLs, domains, and contract addresses for known phishing patterns
and scam indicators using GoPlus Security API and pattern-based detection.

Author: Nihal Nihalani
Version: 1.0.0
"""

import json
import sys
import urllib.request
import urllib.error
import urllib.parse
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

# Known legitimate DeFi domains for lookalike detection
LEGITIMATE_DOMAINS = {
    "uniswap.org",
    "app.uniswap.org",
    "aave.com",
    "app.aave.com",
    "curve.fi",
    "compound.finance",
    "app.compound.finance",
    "lido.fi",
    "makerdao.com",
    "sushi.com",
    "app.sushi.com",
    "pancakeswap.finance",
    "1inch.io",
    "app.1inch.io",
    "balancer.fi",
    "app.balancer.fi",
    "yearn.fi",
    "convexfinance.com",
    "stargate.finance",
    "gmx.io",
    "dydx.exchange",
    "opensea.io",
    "blur.io",
    "metamask.io",
    "etherscan.io",
    "bscscan.com",
    "polygonscan.com",
    "arbiscan.io",
    "basescan.org",
}

# Suspicious TLDs commonly used in phishing
SUSPICIOUS_TLDS = {
    ".xyz", ".top", ".club", ".work", ".buzz", ".tk", ".ml",
    ".ga", ".cf", ".gq", ".pw", ".cc", ".ws", ".icu",
    ".monster", ".surf", ".cam", ".click", ".link",
}

# Common phishing patterns in URLs
PHISHING_URL_PATTERNS = [
    r"(?i)(connect|verify|validate|sync|update|secure|claim|airdrop|reward)-?(wallet|metamask|trust|account)",
    r"(?i)(metamask|trustwallet|phantom|ledger|trezor)\.(com|org|net|io)\.([\w]+)",
    r"(?i)(free|bonus|reward|claim|airdrop|gift).*\.(xyz|top|club|work|buzz)",
    r"(?i)dapp[s]?[-.]?(connect|verify|validate|sync)",
    r"(?i)(wallet|token|nft)[-.]?(claim|reward|airdrop|mint)",
]

# Typosquatting patterns for known protocols
TYPOSQUAT_PATTERNS = {
    "uniswap": [
        r"(?i)un[i1]sw[a@]p", r"(?i)uniswop", r"(?i)uniswep",
        r"(?i)uniswapp", r"(?i)un1swap", r"(?i)uniswqp",
    ],
    "aave": [
        r"(?i)a[a@]ve", r"(?i)aav[e3]", r"(?i)aavee",
    ],
    "opensea": [
        r"(?i)open[s5]ea", r"(?i)opensee", r"(?i)0pensea",
    ],
    "metamask": [
        r"(?i)met[a@]m[a@]sk", r"(?i)metamasc", r"(?i)metarnask",
        r"(?i)m3tamask",
    ],
    "pancakeswap": [
        r"(?i)pancak[e3]swap", r"(?i)panc[a@]keswap",
    ],
}


def fetch_json(url: str, timeout: int = 15) -> dict:
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


def is_url(target: str) -> bool:
    """Check if target looks like a URL."""
    return bool(re.match(r"^https?://", target, re.IGNORECASE)) or "." in target and "/" in target


def is_address(target: str) -> bool:
    """Check if target looks like an Ethereum address."""
    return bool(re.match(r"^0x[a-fA-F0-9]{40}$", target.strip()))


def analyze_url_patterns(url: str) -> list:
    """Analyze a URL for phishing patterns without making API calls."""
    indicators = []

    try:
        parsed = urllib.parse.urlparse(url if "://" in url else f"https://{url}")
        domain = parsed.netloc.lower()
        path = parsed.path.lower()
        full_url = f"{domain}{path}"
    except Exception:
        indicators.append({
            "severity": "MEDIUM",
            "indicator": "Malformed URL",
            "detail": "The URL could not be properly parsed.",
        })
        return indicators

    # Check suspicious TLDs
    for tld in SUSPICIOUS_TLDS:
        if domain.endswith(tld):
            indicators.append({
                "severity": "MEDIUM",
                "indicator": f"Suspicious TLD: {tld}",
                "detail": f"The domain uses {tld}, which is commonly associated with phishing sites.",
            })
            break

    # Check for phishing URL patterns
    for pattern in PHISHING_URL_PATTERNS:
        if re.search(pattern, full_url):
            indicators.append({
                "severity": "HIGH",
                "indicator": "Phishing URL pattern",
                "detail": f"URL matches a known phishing pattern: {pattern.split(')')[0]}...",
            })

    # Check for typosquatting of known protocols
    for protocol, patterns in TYPOSQUAT_PATTERNS.items():
        # Skip if domain is the actual legitimate one
        if protocol in domain:
            is_legit = any(domain == d or domain.endswith(f".{d}") for d in LEGITIMATE_DOMAINS)
            if is_legit:
                continue

        for pattern in patterns:
            if re.search(pattern, domain):
                # Make sure it's not the actual legitimate domain
                is_legit = any(domain == d or domain.endswith(f".{d}") for d in LEGITIMATE_DOMAINS)
                if not is_legit:
                    indicators.append({
                        "severity": "CRITICAL",
                        "indicator": f"Typosquatting: {protocol}",
                        "detail": f"Domain '{domain}' appears to impersonate {protocol}.",
                    })
                    break

    # Check for IP address domains
    if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", domain):
        indicators.append({
            "severity": "HIGH",
            "indicator": "IP address domain",
            "detail": "Using raw IP address instead of domain name is a common phishing tactic.",
        })

    # Check for excessive subdomains
    parts = domain.split(".")
    if len(parts) > 4:
        indicators.append({
            "severity": "MEDIUM",
            "indicator": "Excessive subdomains",
            "detail": f"Domain has {len(parts)} levels, which can be used to hide the real domain.",
        })

    # Check for suspicious path keywords
    suspicious_path_words = [
        "claim", "airdrop", "reward", "connect-wallet", "verify-wallet",
        "sync-wallet", "validate", "secure-account", "unlock",
    ]
    for word in suspicious_path_words:
        if word in path:
            indicators.append({
                "severity": "MEDIUM",
                "indicator": f"Suspicious path: {word}",
                "detail": f"URL path contains '{word}', commonly used in phishing attacks.",
            })

    # Check for data URIs or javascript in URL
    if "javascript:" in url.lower() or "data:" in url.lower():
        indicators.append({
            "severity": "CRITICAL",
            "indicator": "Malicious URL scheme",
            "detail": "URL contains javascript: or data: scheme, which can execute malicious code.",
        })

    return indicators


def check_url_goplus(url: str) -> dict:
    """Check URL against GoPlus phishing site database."""
    encoded_url = urllib.parse.quote(url, safe="")
    api_url = f"{GOPLUS_API}/phishing_site?url={encoded_url}"

    try:
        data = fetch_json(api_url)
        if data and data.get("code") == 1:
            result = data.get("result", {})
            return {
                "checked": True,
                "is_phishing": result.get("phishing_site") == 1,
                "website_contract_security": result.get("website_contract_security", []),
            }
    except ConnectionError:
        pass

    return {"checked": False, "is_phishing": None}


def check_address_goplus(address: str, chain_id: str) -> dict:
    """Check address against GoPlus address security database."""
    api_url = f"{GOPLUS_API}/address_security/{address}?chain_id={chain_id}"

    try:
        data = fetch_json(api_url)
        if data and data.get("code") == 1:
            result = data.get("result", {})
            flags = []

            flag_checks = {
                "cybercrime": "Associated with cybercrime activities",
                "money_laundering": "Flagged for money laundering",
                "financial_crime": "Involved in financial crimes",
                "darkweb_transactions": "Has darkweb transaction history",
                "phishing_activities": "Known phishing address",
                "stealing_attack": "Involved in theft/exploit attacks",
                "blackmail_activities": "Associated with blackmail",
                "sanctioned": "On sanctions list",
                "malicious_mining_activities": "Malicious mining activity",
                "mixer_usage": "Uses crypto mixers/tumblers",
                "honeypot_related_address": "Related to honeypot scams",
                "fake_kyc": "Uses fake KYC credentials",
                "blacklist_doubt": "On blacklist watchlists",
            }

            for key, label in flag_checks.items():
                if result.get(key) == "1":
                    flags.append(label)

            return {
                "checked": True,
                "is_malicious": len(flags) > 0,
                "flags": flags,
                "data_source": result.get("data_source", ""),
            }
    except ConnectionError:
        pass

    return {"checked": False, "is_malicious": None, "flags": []}


def detect_phishing(target: str, chain: str = "ethereum") -> dict:
    """Run phishing detection on a URL or address."""
    target = target.strip()

    if is_address(target):
        return detect_address_phishing(target, chain)
    else:
        return detect_url_phishing(target)


def detect_url_phishing(url: str) -> dict:
    """Detect phishing for a URL target."""
    # Normalize URL
    if not url.startswith("http://") and not url.startswith("https://"):
        url = f"https://{url}"

    indicators = analyze_url_patterns(url)
    goplus_result = check_url_goplus(url)

    if goplus_result.get("is_phishing"):
        indicators.insert(0, {
            "severity": "CRITICAL",
            "indicator": "GoPlus confirmed phishing site",
            "detail": "This URL is flagged as a phishing site in the GoPlus security database.",
        })

    # Calculate risk score
    score = 0
    for ind in indicators:
        if ind["severity"] == "CRITICAL":
            score += 4
        elif ind["severity"] == "HIGH":
            score += 2
        elif ind["severity"] == "MEDIUM":
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

    is_phishing = score >= 6 or goplus_result.get("is_phishing", False)

    # Generate summary
    if is_phishing:
        summary = (
            "PHISHING DETECTED: This URL shows strong signs of being a phishing site. "
            "Do NOT connect your wallet or enter any credentials."
        )
    elif score >= 4:
        summary = (
            "SUSPICIOUS: This URL has some concerning characteristics. "
            "Verify the domain carefully before interacting."
        )
    elif score >= 2:
        summary = (
            "MINOR CONCERNS: A few low-severity indicators found. "
            "Double-check the URL is correct before proceeding."
        )
    else:
        summary = (
            "NO ISSUES DETECTED: No phishing indicators found. "
            "However, always verify you are on the official site."
        )

    # Recommendations
    recommendations = []
    if is_phishing:
        recommendations.append("Do NOT interact with this URL")
        recommendations.append("Do NOT connect your wallet")
        recommendations.append("Do NOT enter any personal information or seed phrases")
        recommendations.append("Report this site to the legitimate project's team")
    elif score >= 4:
        recommendations.append("Verify the domain matches the official project website")
        recommendations.append("Check the URL in your browser's address bar carefully")
        recommendations.append("Use bookmarks for frequently visited DeFi sites")
    else:
        recommendations.append("Always bookmark official DeFi sites")
        recommendations.append("Verify the URL in your browser before connecting your wallet")

    return {
        "success": True,
        "scan_type": "phishing_detection",
        "target_type": "url",
        "target": url,
        "is_phishing": is_phishing,
        "confidence": min(score * 10, 100),
        "risk_score": score,
        "risk_level": level,
        "summary": summary,
        "goplus_check": {
            "checked": goplus_result.get("checked", False),
            "flagged": goplus_result.get("is_phishing", False),
        },
        "risk_indicators": indicators,
        "recommendations": recommendations,
    }


def detect_address_phishing(address: str, chain: str) -> dict:
    """Detect phishing/scam for an address target."""
    address = address.lower().strip()
    chain_id = CHAIN_IDS.get(chain.lower(), "1")

    goplus_result = check_address_goplus(address, chain_id)

    indicators = []
    if goplus_result.get("is_malicious"):
        for flag in goplus_result.get("flags", []):
            indicators.append({
                "severity": "CRITICAL",
                "indicator": flag,
                "detail": f"GoPlus has flagged this address for: {flag}",
            })

    # Calculate risk score
    score = len(indicators) * 3
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

    is_malicious = goplus_result.get("is_malicious", False)

    if is_malicious:
        summary = (
            "MALICIOUS ADDRESS: This address has been flagged for malicious activity. "
            "Do NOT send funds to or interact with this address."
        )
    elif not goplus_result.get("checked"):
        summary = (
            "UNABLE TO VERIFY: Could not check this address against security databases. "
            "Proceed with caution and verify independently."
        )
    else:
        summary = (
            "NO FLAGS DETECTED: This address has no known security flags. "
            "However, absence of flags does not guarantee safety."
        )

    recommendations = []
    if is_malicious:
        recommendations.append("Do NOT send funds to this address")
        recommendations.append("Do NOT approve token spending for this address")
        recommendations.append("If you have interacted, revoke any approvals immediately")
    else:
        recommendations.append("Verify the address through official channels before sending funds")
        recommendations.append("Start with a small test transaction when interacting with new addresses")

    return {
        "success": True,
        "scan_type": "phishing_detection",
        "target_type": "address",
        "target": address,
        "chain": chain,
        "chain_id": chain_id,
        "is_phishing": is_malicious,
        "confidence": min(score * 10, 100) if goplus_result.get("checked") else 0,
        "risk_score": score,
        "risk_level": level,
        "summary": summary,
        "goplus_check": {
            "checked": goplus_result.get("checked", False),
            "flagged": is_malicious,
            "flags": goplus_result.get("flags", []),
        },
        "risk_indicators": indicators,
        "recommendations": recommendations,
    }


def main() -> None:
    """Main entry point. Reads JSON from stdin."""
    try:
        input_data = json.loads(sys.stdin.read())

        target = input_data.get("target", "")
        chain = input_data.get("chain", "ethereum")

        if not target:
            print(json.dumps({
                "error": "Missing required parameter: 'target'",
                "usage": {
                    "target": "URL (https://suspicious-site.com) or address (0x...)",
                    "chain": "ethereum (optional, for address checks only)",
                },
                "examples": [
                    {"target": "https://app.uniswop.org"},
                    {"target": "0x1234567890abcdef1234567890abcdef12345678", "chain": "ethereum"},
                ],
            }))
            sys.exit(1)

        result = detect_phishing(target, chain)
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
