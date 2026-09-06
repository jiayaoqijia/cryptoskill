#!/usr/bin/env python3
"""
Contract Source Analyzer
Fetches verified Solidity source code from Sourcify and performs
regex-based static analysis for common vulnerability patterns.

Author: Nihal Nihalani
Version: 1.0.0
"""

import json
import sys
import urllib.request
import urllib.error
import re

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


def fetch_json(url: str, timeout: int = 30) -> dict:
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
            f"Supported: {', '.join(sorted(set(CHAIN_IDS.values())))}"
        )
    return chain_id


def fetch_sourcify_contract(address: str, chain_id: str) -> dict:
    """Fetch verified contract data from Sourcify V2 API."""
    url = (
        f"{SOURCIFY_API}/v2/contract/{chain_id}/{address}"
        f"?fields=sources,compilation"
    )
    data = fetch_json(url)
    if data is None:
        raise ValueError(
            f"Contract not verified on Sourcify. "
            "Source code analysis requires verified source. "
            "Try contract_security_audit.py for unverified contracts."
        )
    return data


# Vulnerability patterns: (pattern_name, severity, regex, description, recommendation)
VULNERABILITY_PATTERNS = [
    (
        "reentrancy",
        "CRITICAL",
        r"\.call\{[^}]*value\s*:",
        "External call with value transfer (potential reentrancy)",
        "Use checks-effects-interactions pattern or ReentrancyGuard",
    ),
    (
        "reentrancy_call",
        "CRITICAL",
        r"\.call\(",
        "Low-level .call() usage (potential reentrancy if before state change)",
        "Use checks-effects-interactions pattern; update state before external calls",
    ),
    (
        "selfdestruct",
        "CRITICAL",
        r"\bselfdestruct\s*\(",
        "Contract can be permanently destroyed",
        "Remove selfdestruct unless absolutely necessary; consider access control",
    ),
    (
        "suicide",
        "CRITICAL",
        r"\bsuicide\s*\(",
        "Deprecated destruction function (equivalent to selfdestruct)",
        "Remove suicide function entirely",
    ),
    (
        "delegatecall",
        "CRITICAL",
        r"\.delegatecall\s*\(",
        "delegatecall can execute arbitrary code in this contract's context",
        "Ensure delegatecall target is trusted and immutable",
    ),
    (
        "tx_origin",
        "HIGH",
        r"\btx\.origin\b",
        "tx.origin used (vulnerable to phishing attacks)",
        "Use msg.sender instead of tx.origin for authorization",
    ),
    (
        "unchecked_call",
        "HIGH",
        r"(?:address\([^)]*\)|[a-zA-Z_]\w*)\.call\{[^}]*\}\([^)]*\)\s*;",
        "Low-level call without checking return value",
        "Always check the return value of low-level calls",
    ),
    (
        "unprotected_initializer",
        "HIGH",
        r"function\s+initialize\s*\([^)]*\)\s+(?:public|external)\b",
        "Initializer function may be callable by anyone",
        "Use OpenZeppelin Initializable modifier or access control",
    ),
    (
        "floating_pragma",
        "MEDIUM",
        r"pragma\s+solidity\s+[\^~>]",
        "Compiler version not locked (floating pragma)",
        "Lock compiler version (e.g., 'pragma solidity 0.8.19;')",
    ),
    (
        "timestamp_dependence",
        "MEDIUM",
        r"\bblock\.timestamp\b",
        "Block timestamp used (can be manipulated by miners within ~15s)",
        "Avoid using block.timestamp for critical logic or randomness",
    ),
    (
        "block_number_dependence",
        "MEDIUM",
        r"\bblock\.number\b.*(?:random|seed|lottery|winner)",
        "Block number used for randomness (predictable)",
        "Use Chainlink VRF or commit-reveal for randomness",
    ),
    (
        "assembly_usage",
        "LOW",
        r"\bassembly\s*\{",
        "Inline assembly used (bypasses Solidity safety checks)",
        "Ensure assembly is reviewed by security experts",
    ),
    (
        "transfer_gas",
        "LOW",
        r"\.transfer\s*\(",
        "transfer() has fixed 2300 gas stipend (may fail with smart contract recipients)",
        "Consider using call{value: amount}('') with reentrancy guard instead",
    ),
    (
        "send_gas",
        "LOW",
        r"\.send\s*\(",
        "send() has fixed 2300 gas stipend and returns bool",
        "Consider using call{value: amount}('') with reentrancy guard instead",
    ),
    (
        "ecrecover",
        "MEDIUM",
        r"\becrecover\s*\(",
        "ecrecover can return zero address for invalid signatures",
        "Check that ecrecover result is not address(0)",
    ),
]


def scan_source_code(source_code: str, filename: str) -> list:
    """Scan source code for vulnerability patterns."""
    findings = []
    lines = source_code.split("\n")

    for pattern_name, severity, regex, description, recommendation in VULNERABILITY_PATTERNS:
        for line_num, line in enumerate(lines, 1):
            # Skip comments
            stripped = line.strip()
            if stripped.startswith("//") or stripped.startswith("*") or stripped.startswith("/*"):
                continue

            if re.search(regex, line):
                findings.append({
                    "severity": severity,
                    "pattern": pattern_name,
                    "description": description,
                    "detail": stripped[:120],
                    "file": filename,
                    "line": line_num,
                    "recommendation": recommendation,
                })

    return findings


def deduplicate_findings(findings: list) -> list:
    """Remove duplicate findings (same pattern + same line)."""
    seen = set()
    deduped = []
    for f in findings:
        key = (f["pattern"], f["file"], f["line"])
        if key not in seen:
            seen.add(key)
            deduped.append(f)
    return deduped


def calculate_risk_score(findings: list) -> dict:
    """Calculate risk score from findings based on unique patterns found."""
    severity_weights = {
        "CRITICAL": 4,
        "HIGH": 3,
        "MEDIUM": 2,
        "LOW": 1,
        "INFO": 0,
    }
    severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}

    for f in findings:
        severity_counts[f["severity"]] = severity_counts.get(f["severity"], 0) + 1

    # Score based on unique patterns (not individual occurrences)
    # This prevents inflated scores from repeated patterns like assembly usage
    seen_patterns = set()
    score = 0
    for f in findings:
        pattern_key = f["pattern"]
        if pattern_key not in seen_patterns:
            seen_patterns.add(pattern_key)
            score += severity_weights.get(f["severity"], 0)

    # Normalize to 0-10 scale
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
        "score": score,
        "level": level,
        "total_findings": len(findings),
        "critical": severity_counts["CRITICAL"],
        "high": severity_counts["HIGH"],
        "medium": severity_counts["MEDIUM"],
        "low": severity_counts["LOW"],
        "info": severity_counts["INFO"],
    }


def analyze_contract(contract_address: str, chain: str = "ethereum") -> dict:
    """Run source code vulnerability analysis on a verified contract."""
    contract_address = validate_address(contract_address)
    chain_id = validate_chain(chain)

    # Fetch verified source from Sourcify
    contract_data = fetch_sourcify_contract(contract_address, chain_id)

    # Extract compilation info
    compilation = contract_data.get("compilation", {})
    contract_name = compilation.get("name", "Unknown")
    compiler_version = compilation.get("compilerVersion", "Unknown")

    # Determine verification match quality
    match_type = contract_data.get("match", "unknown")
    if match_type == "exact_match":
        verification_status = "exact"
    elif match_type == "match":
        verification_status = "partial"
    else:
        verification_status = match_type

    # Extract and scan source files
    sources = contract_data.get("sources", {})
    all_findings = []
    source_file_names = []

    for filename, file_data in sources.items():
        content = ""
        if isinstance(file_data, dict):
            content = file_data.get("content", "")
        elif isinstance(file_data, str):
            content = file_data

        if not content:
            continue

        # Only scan .sol files
        if not filename.endswith(".sol"):
            continue

        source_file_names.append(filename)
        findings = scan_source_code(content, filename)
        all_findings.extend(findings)

    # Deduplicate
    all_findings = deduplicate_findings(all_findings)

    # Sort by severity
    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "INFO": 4}
    all_findings.sort(key=lambda x: severity_order.get(x["severity"], 5))

    # Limit to top 30 findings
    all_findings = all_findings[:30]

    # Calculate risk
    risk = calculate_risk_score(all_findings)

    return {
        "success": True,
        "scan_type": "source_analysis",
        "contract": {
            "address": contract_address,
            "name": contract_name,
            "chain": chain,
            "chain_id": chain_id,
            "compiler_version": compiler_version,
            "verification_status": verification_status,
        },
        "source_files": source_file_names,
        "source_file_count": len(source_file_names),
        "findings": all_findings,
        "risk_assessment": risk,
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

        result = analyze_contract(contract_address, chain)
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
