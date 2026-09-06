# DeFi Safety Shield

A zero-configuration DeFi safety monitoring toolkit for SpoonOS agents. Scan tokens for rug pulls and honeypots, detect phishing URLs and scam addresses, audit wallet token approvals, and score protocol risk -- all using **free APIs with no API keys required**.

## Why This Skill?

DeFi users lose billions each year to scams, rug pulls, phishing attacks, and exploited protocols. Most safety tools require paid subscriptions, browser extensions, or manual multi-site checking. DeFi Safety Shield brings **comprehensive DeFi risk assessment** to SpoonOS agents with zero setup -- a complete safety net for anyone interacting with DeFi.

### The Problem

| Threat | 2023 Losses | How Users Get Caught |
|--------|------------|---------------------|
| Rug Pulls | $2.1B+ | Buying tokens without checking contract code |
| Phishing | $374M+ | Clicking fake DeFi links that steal wallet approvals |
| Approval Exploits | $200M+ | Unlimited token approvals to malicious contracts |
| Protocol Hacks | $1.7B+ | Depositing into unaudited or vulnerable protocols |

### Current Workflow vs. DeFi Safety Shield

| Task | Manual Approach | With DeFi Safety Shield |
|------|----------------|------------------------|
| Check token safety | Open GoPlus, Honeypot.is, TokenSniffer, read Etherscan | `echo '{"address": "0x..."}' \| python3 token_risk_scanner.py` |
| Verify a DeFi link | Google the project, compare URLs manually, check Twitter | `echo '{"target": "https://..."}' \| python3 phishing_detector.py` |
| Audit wallet approvals | Visit revoke.cash, manually review each approval | `echo '{"wallet_address": "0x..."}' \| python3 wallet_approval_audit.py` |
| Evaluate protocol risk | Check DeFiLlama TVL, search for audits, Google hacks | `echo '{"protocol": "aave"}' \| python3 protocol_risk_scorer.py` |
| Multi-chain checks | Repeat all above per chain | Just pass `"chain": "polygon"` |
| **Time per check** | **15-30 minutes** | **Under 30 seconds** |

### Data Sources

| API | What It Provides | Auth | Rate Limit |
|-----|-----------------|------|------------|
| [GoPlus Security](https://gopluslabs.io) | Token security, address risk, phishing site DB | None | 30 req/min |
| [DeFiLlama](https://defillama.com) | Protocol TVL, categories, chain coverage | None | Generous |
| [Blockscout](https://eth.blockscout.com) | Token approvals, contract verification, metadata | None | 5 req/sec |

## Quick Start

### For Vibe Coding (Claude Code / SpoonOS Skills)

```bash
cp -r defi-safety-shield/ .claude/skills/defi-safety-shield/
# Or: cp -r defi-safety-shield/ .agent/skills/defi-safety-shield/
```

### For SpoonReactSkill Agent

```python
from spoon_ai.agents import SpoonReactSkill

agent = SpoonReactSkill(
    name="defi_safety",
    skill_paths=["ai-productivity/monitoring/defi-safety-shield"],
    scripts_enabled=True
)
await agent.activate_skill("defi-safety-shield")
result = await agent.run("Is this token safe? 0xdAC17F958D2ee523a2206206994597C13D831ec7")
```

### Direct Script Execution

```bash
# Scan a token for risks
echo '{"address": "0xdAC17F958D2ee523a2206206994597C13D831ec7", "chain": "ethereum"}' | python3 scripts/token_risk_scanner.py

# Check a URL for phishing
echo '{"target": "https://app.uniswop.org"}' | python3 scripts/phishing_detector.py

# Audit wallet approvals
echo '{"wallet_address": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045", "chain": "ethereum"}' | python3 scripts/wallet_approval_audit.py

# Score protocol safety
echo '{"protocol": "aave"}' | python3 scripts/protocol_risk_scorer.py
```

## Scripts

| Script | Purpose | APIs Used |
|--------|---------|-----------|
| [token_risk_scanner.py](scripts/token_risk_scanner.py) | Token honeypot, rug pull, and tax analysis | GoPlus Security |
| [phishing_detector.py](scripts/phishing_detector.py) | URL phishing detection and address scam checking | GoPlus Security + Pattern Analysis |
| [wallet_approval_audit.py](scripts/wallet_approval_audit.py) | Wallet token approval risk assessment | Blockscout + GoPlus Security |
| [protocol_risk_scorer.py](scripts/protocol_risk_scorer.py) | DeFi protocol TVL and safety scoring | DeFiLlama + Local Audit DB |

## Detailed API Documentation

### token_risk_scanner.py

Scans a token contract for honeypot indicators, rug pull risks, tax manipulation, and ownership dangers using the GoPlus Security API.

**Input:**
```json
{
  "address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
  "chain": "ethereum"
}
```

**Output:**
```json
{
  "success": true,
  "scan_type": "token_risk",
  "address": "0xdac17f958d2ee523a2206206994597c13d831ec7",
  "chain": "ethereum",
  "chain_id": "1",
  "token_found": true,
  "token_info": {
    "name": "Tether USD",
    "symbol": "USDT",
    "holder_count": "5234567",
    "total_supply": "40000000000000000",
    "creator": "0x...",
    "owner": "0x..."
  },
  "risk_score": 3,
  "risk_level": "LOW",
  "summary": "LOW RISK: Minor concerns found but no major red flags...",
  "taxes": {
    "buy_tax_percent": 0.0,
    "sell_tax_percent": 0.0,
    "tax_modifiable": false
  },
  "findings": [
    {
      "severity": "MEDIUM",
      "category": "blacklist",
      "finding": "Blacklist function exists",
      "detail": "The contract can blacklist addresses, preventing them from trading."
    }
  ],
  "top_holders": [
    {"address": "0x...", "percent": 12.5, "is_locked": false, "is_contract": true}
  ],
  "dex_info": [
    {"name": "Uniswap V3", "liquidity": "250000000", "pair": "USDT/WETH"}
  ],
  "recommendations": [
    "No immediate action required, but always DYOR"
  ]
}
```

**Checks Performed:**

| Check | Severity | Description |
|-------|----------|-------------|
| Honeypot | CRITICAL | Cannot sell tokens after buying |
| Hidden owner | CRITICAL | Concealed ownership mechanism |
| Balance manipulation | CRITICAL | Owner can change balances |
| Ownership reclaimable | CRITICAL | Renounced ownership is fake |
| Self-destruct | CRITICAL | Contract can be destroyed |
| Extreme tax (>50%) | CRITICAL | Buy or sell tax above 50% |
| High tax (>10%) | HIGH | Noticeable buy or sell tax |
| Tax modifiable | HIGH | Owner can change tax rates |
| Source unverified | HIGH | Contract code not public |
| External calls | HIGH | Potentially manipulable calls |
| Blacklist | MEDIUM | Can freeze specific addresses |
| Pausable | MEDIUM | Can freeze all transfers |
| Mintable | MEDIUM | New tokens can be created |
| Proxy | MEDIUM | Contract logic is upgradeable |
| Moderate tax (>5%) | MEDIUM | Noticeable but not extreme tax |
| Anti-whale modifiable | MEDIUM | Transaction limits can change |
| Anti-whale | LOW | Transaction size limits exist |
| Trusted list | INFO | Token on GoPlus trusted list (reduces score) |
| Verified source | INFO | Source code is public |
| DEX listed | INFO | Active DEX liquidity |
| Ownership renounced | INFO | Owner is zero address |

### phishing_detector.py

Analyzes URLs for phishing patterns and checks addresses against the GoPlus scam database. Combines API lookups with local pattern-based detection.

**Input (URL check):**
```json
{
  "target": "https://app.uniswop.org"
}
```

**Input (address check):**
```json
{
  "target": "0x1234567890abcdef1234567890abcdef12345678",
  "chain": "ethereum"
}
```

**Output (URL phishing detected):**
```json
{
  "success": true,
  "scan_type": "phishing_detection",
  "target_type": "url",
  "target": "https://app.uniswop.org",
  "is_phishing": true,
  "confidence": 80,
  "risk_score": 8,
  "risk_level": "CRITICAL",
  "summary": "PHISHING DETECTED: This URL shows strong signs of being a phishing site...",
  "goplus_check": {
    "checked": true,
    "flagged": true
  },
  "risk_indicators": [
    {
      "severity": "CRITICAL",
      "indicator": "Typosquatting: uniswap",
      "detail": "Domain 'uniswop.org' appears to impersonate uniswap."
    }
  ],
  "recommendations": [
    "Do NOT interact with this URL",
    "Do NOT connect your wallet",
    "Report this site to the legitimate project's team"
  ]
}
```

**Detection Methods:**

| Method | What It Catches |
|--------|----------------|
| GoPlus phishing DB | Known phishing sites from community reports |
| Typosquatting detection | Lookalike domains for Uniswap, Aave, OpenSea, MetaMask, PancakeSwap |
| Suspicious TLD check | .xyz, .top, .club, .buzz, .tk, and 15+ risky TLDs |
| URL pattern matching | "connect-wallet", "claim-airdrop", "verify-account" patterns |
| IP address domains | Raw IP addresses instead of domain names |
| Excessive subdomains | Domains with 5+ levels used to hide the real host |
| Malicious URL schemes | javascript: and data: URI schemes |
| GoPlus address security | For address targets: cybercrime, phishing, theft flags |

### wallet_approval_audit.py

Audits a wallet's ERC20 token approvals to find unlimited or dangerous approvals that could drain funds. Uses Blockscout for approval data and GoPlus for spender verification.

**Input:**
```json
{
  "wallet_address": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
  "chain": "ethereum"
}
```

**Output:**
```json
{
  "success": true,
  "scan_type": "approval_audit",
  "wallet_address": "0xd8da6bf26964af9d7eed9e03e53415d37aa96045",
  "chain": "ethereum",
  "chain_id": "1",
  "total_approvals": 12,
  "unlimited_approvals": 3,
  "high_risk_approvals": 0,
  "risk_score": 2,
  "risk_level": "LOW",
  "summary": "Found 3 unlimited approval(s) out of 12 total...",
  "approvals": [
    {
      "token": {
        "address": "0xa0b86991...",
        "name": "USD Coin",
        "symbol": "USDC"
      },
      "spender": {
        "address": "0x68b3465...",
        "contract_name": "SwapRouter02",
        "is_verified": true,
        "is_malicious": false,
        "flags": []
      },
      "allowance": {
        "raw": "115792089237316195423570985008687907853269984665640564039457584007913129639935",
        "classification": "unlimited",
        "risk": "HIGH",
        "detail": "Unlimited approval - spender can transfer ALL your tokens"
      },
      "risk": "HIGH",
      "risk_reasons": ["Unlimited approval - spender can take all tokens"],
      "block_number": 18500000,
      "tx_hash": "0x..."
    }
  ],
  "recommendations": [
    "Revoke 3 unlimited approval(s) - use revoke.cash or etherscan",
    "Use limited approvals instead of unlimited when possible",
    "Regularly audit your approvals (monthly recommended)"
  ]
}
```

**Risk Classification:**

| Allowance Type | Risk | Description |
|----------------|------|-------------|
| Revoked (0) | SAFE | No approval, no risk |
| Limited (reasonable) | LOW | Approval for a specific amount |
| Limited (very large) | MEDIUM | Over 1M tokens approved |
| Unlimited (max uint256) | HIGH | Spender can take everything |
| Any + malicious spender | CRITICAL | Spender flagged by GoPlus |
| Any + unverified spender | MEDIUM-HIGH | Spender contract not verified |

### protocol_risk_scorer.py

Evaluates DeFi protocol safety using TVL data from DeFiLlama, a curated audit database, and known exploit history.

**Input:**
```json
{
  "protocol": "aave"
}
```

**Output:**
```json
{
  "success": true,
  "scan_type": "protocol_risk",
  "protocol": {
    "name": "Aave",
    "slug": "aave",
    "category": "Lending",
    "url": "https://aave.com",
    "chains": ["Ethereum", "Polygon", "Avalanche", "Arbitrum", "Optimism", "Base"]
  },
  "tvl": {
    "current": "$12.5B",
    "current_raw": 12500000000,
    "trend": "stable",
    "change_7d_percent": 1.2,
    "change_30d_percent": 5.8
  },
  "audits": {
    "has_known_audits": true,
    "auditors": ["Trail of Bits", "OpenZeppelin", "SigmaPrime", "Certora"],
    "audit_count": 4
  },
  "exploits": {
    "has_known_exploits": false,
    "exploits": [],
    "exploit_count": 0
  },
  "risk_score": 1,
  "risk_level": "SAFE",
  "summary": "SAFE: Aave is a well-established protocol with strong TVL, multiple audits, and no major known issues.",
  "risk_factors": [
    {"factor": "Strong TVL", "impact": "0 (positive)", "detail": "TVL is $12.5B"},
    {"factor": "Multiple audits", "impact": "-1 (positive)", "detail": "Audited by Trail of Bits, OpenZeppelin, SigmaPrime"}
  ],
  "recommendations": [
    "Protocol appears solid, but always diversify across protocols",
    "Monitor the protocol's official channels for security updates"
  ]
}
```

**Scoring Factors:**

| Factor | Score Impact | Trigger |
|--------|-------------|---------|
| Very low TVL (<$100K) | +3 | Near-zero user confidence |
| Low TVL (<$1M) | +2 | Limited battle-testing |
| Moderate TVL (<$10M) | +1 | Growing but still early |
| Strong TVL (>$10M) | 0 | Well-funded protocol |
| Severe TVL drop (>30% / 7d) | +3 | Possible security incident |
| Significant TVL drop (>15% / 7d) | +2 | Users withdrawing fast |
| TVL declining (>5% / 7d) | +1 | Mild outflow |
| No known audits | +2 | Unaudited code |
| Multiple audits (3+) | -1 | Strong security posture |
| Exploits (unrecovered funds) | +2 | Past security failure |
| Exploits (funds recovered) | +1 | Past incident, handled well |
| Single chain deployment | +1 | Limited diversity |

**Protocols with Audit Data:**
Aave, Uniswap, Compound, MakerDAO, Lido, Curve, Convex, Rocket Pool, Frax, Instadapp, Yearn, Balancer, SushiSwap, PancakeSwap, GMX, dYdX, 1inch, Stargate, EigenLayer, Pendle, Morpho, Euler

**Protocols with Exploit History:**
Euler, Curve, Balancer, Harvest Finance, Beanstalk, Ronin, Wormhole, Nomad, Mango Markets

## Risk Scoring System

All four scripts use a unified 0-10 risk scoring system:

| Level | Score | Color | Action |
|-------|-------|-------|--------|
| SAFE | 0-1 | Green | No significant risks detected |
| LOW | 2-3 | Blue | Minor concerns, generally safe |
| MEDIUM | 4-5 | Yellow | Proceed with caution, review findings |
| HIGH | 6-7 | Orange | Significant risks -- not recommended |
| CRITICAL | 8-10 | Red | Likely malicious or extremely dangerous -- avoid |

## Supported Chains

| Chain | ID | Token Scan | Phishing | Approvals | Protocol |
|-------|----|-----------|----------|-----------|----------|
| Ethereum | 1 | Yes | Yes | Yes | Yes |
| BSC | 56 | Yes | Yes | Yes | Yes |
| Polygon | 137 | Yes | Yes | Yes | Yes |
| Arbitrum | 42161 | Yes | Yes | Yes | Yes |
| Base | 8453 | Yes | Yes | Yes | Yes |
| Optimism | 10 | Yes | Yes | Yes | Yes |
| Avalanche | 43114 | Yes | Yes | Yes | Yes |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| *(none)* | -- | **No environment variables needed** |

All APIs used are free and require no authentication. Zero configuration.

## Error Handling

All scripts return structured JSON error responses:

```json
{"error": "Invalid address format: xyz. Expected 0x followed by 40 hex characters."}
{"error": "Unsupported chain: solana. Supported: arb, avalanche, avax, base, bnb, bsc, eth, ethereum, matic, op, optimism, polygon"}
{"error": "Rate limit exceeded. Please wait 1-2 minutes before retrying."}
{"error": "Protocol 'nonexistent' not found on DeFiLlama. Check the protocol name or try its DeFiLlama slug."}
```

| Error | Cause | Solution |
|-------|-------|----------|
| Invalid address | Wrong format | Use 0x + 40 hex characters |
| Unsupported chain | Chain not in supported list | Use one of the 7 supported chains |
| Rate limit | Too many requests | Wait 1-2 minutes |
| Connection failed | Network issues | Check internet connection |
| Protocol not found | Wrong name or slug | Try the DeFiLlama slug |
| Token not found | Not indexed by GoPlus | Token may be too new or low-activity |

## Security Design Principles

This skill follows strict security principles:

1. **Read-Only** -- NEVER sends transactions, signs messages, or modifies blockchain state
2. **No Keys Required** -- Zero API keys, zero private keys, zero wallet connections
3. **No Data Storage** -- No user data persisted beyond the script execution
4. **Input Validation** -- Regex validation on all addresses, chain whitelist enforcement
5. **Safe Errors** -- No stack traces or internal details exposed in error messages
6. **Multi-Source** -- Cross-references GoPlus, DeFiLlama, and Blockscout for comprehensive coverage
7. **Conservative Scoring** -- Flags suspicious patterns even when unconfirmed
8. **Standard Library Only** -- Uses only Python standard library (no pip install needed)
9. **Timeout Protection** -- All API calls have configurable timeouts to prevent hangs

## Use Cases

### 1. Pre-Trade Token Check
Before buying a new token, scan it for honeypot indicators and hidden taxes.
```bash
echo '{"address": "0x...", "chain": "ethereum"}' | python3 scripts/token_risk_scanner.py
```

### 2. Link Verification
When someone shares a DeFi link, verify it is not a phishing site before connecting your wallet.
```bash
echo '{"target": "https://app.uniswap.org"}' | python3 scripts/phishing_detector.py
```

### 3. Wallet Hygiene
Periodically audit your wallet's token approvals and revoke any that are unnecessary.
```bash
echo '{"wallet_address": "0x...", "chain": "ethereum"}' | python3 scripts/wallet_approval_audit.py
```

### 4. Protocol Due Diligence
Before depositing into a DeFi protocol, evaluate its TVL trends, audit history, and exploit record.
```bash
echo '{"protocol": "curve-dex"}' | python3 scripts/protocol_risk_scorer.py
```

### 5. Scam Address Verification
When asked to send funds to an unknown address, check if it is flagged as malicious.
```bash
echo '{"target": "0x...", "chain": "ethereum"}' | python3 scripts/phishing_detector.py
```

### 6. Multi-Chain Monitoring
Run the same checks across different chains for cross-chain token deployments.
```bash
for chain in ethereum bsc polygon arbitrum; do
  echo "{\"address\": \"0x...\", \"chain\": \"$chain\"}" | python3 scripts/token_risk_scanner.py
done
```

## Composability

This skill composes well with other SpoonOS skills:

- **+ Smart Contract Auditor**: After token_risk_scanner flags a contract, run a deep source code audit
- **+ Market Intelligence**: Check token safety before acting on market signals
- **+ On-Chain Analysis**: Combine approval audit with transaction history analysis
- **+ DeFi Operations**: Run protocol_risk_scorer before executing yield farming strategies
- **+ Wallet Skills**: Integrate approval auditing into regular wallet management workflows

### Pipeline Example

```bash
# Step 1: Check if the token is safe
echo '{"address": "0x...", "chain": "ethereum"}' | python3 scripts/token_risk_scanner.py

# Step 2: If safe, check the protocol behind it
echo '{"protocol": "protocol-name"}' | python3 scripts/protocol_risk_scorer.py

# Step 3: Before approving, ensure your wallet is clean
echo '{"wallet_address": "0x...", "chain": "ethereum"}' | python3 scripts/wallet_approval_audit.py
```

## License

MIT License
