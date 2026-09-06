# Smart Contract Auditor

A zero-configuration smart contract security auditing toolkit for SpoonOS agents. Performs source code vulnerability analysis, function signature intelligence, multi-source security audits, and ABI risk assessment — all using **free APIs with no API keys required**.

## Why This Skill?

Smart contract exploits caused over $1.7B in losses in 2023 alone. Most security tools require paid subscriptions (Slither Pro, MythX, Certora) or complex local setup (Foundry, Hardhat). Smart Contract Auditor brings **enterprise-grade security analysis** to SpoonOS agents with zero setup — the **first skill in the Enterprise & Team Skills code-review track**.

### What Makes It Different

| Feature | This Skill | Existing Tools |
|---------|-----------|----------------|
| API Keys Required | **None** | Etherscan key, Tenderly key |
| Local Setup | **Zero** | Node.js, Python venv, Foundry |
| Source Code Analysis | **Sourcify-powered** | Local tooling only |
| Function Intelligence | **4byte.directory** | Manual ABI reading |
| Multi-Source Security | **GoPlus + Sourcify + Blockscout** | Single source |
| ABI Risk Analysis | **Automated categorization** | Manual review |
| Multi-Chain | **7+ EVM chains** | Usually single chain |

### Data Sources

| API | What It Provides | Auth | Rate Limit |
|-----|-----------------|------|------------|
| [Sourcify](https://sourcify.dev) | Verified source code, ABI, compiler metadata, deployment info | None | Generous |
| [4byte.directory](https://www.4byte.directory) | Function selector decoding, signature database | None | No limit |
| [Blockscout](https://eth.blockscout.com) | Contract metadata, proxy detection, ABI, creator info | None | 5 req/sec |
| [GoPlus Security](https://gopluslabs.io) | Token/contract security intelligence, honeypot detection | None | 30 req/min |

## Quick Start

### For Vibe Coding (Claude Code / SpoonOS Skills)

```bash
cp -r smart-contract-auditor/ .claude/skills/smart-contract-auditor/
# Or: cp -r smart-contract-auditor/ .agent/skills/smart-contract-auditor/
```

### For SpoonReactSkill Agent

```python
from spoon_ai.agents import SpoonReactSkill

agent = SpoonReactSkill(
    name="contract_auditor",
    skill_paths=["enterprise-skills/code-review/smart-contract-auditor"],
    scripts_enabled=True
)
await agent.activate_skill("smart-contract-auditor")
result = await agent.run("Audit this contract: 0xdAC17F958D2ee523a2206206994597C13D831ec7")
```

### Direct Script Execution

```bash
# Scan source code for vulnerabilities
echo '{"contract_address": "0xdAC17F958D2ee523a2206206994597C13D831ec7", "chain": "ethereum"}' | python3 scripts/contract_source_analyzer.py

# Decode and analyze functions
echo '{"contract_address": "0xdAC17F958D2ee523a2206206994597C13D831ec7", "chain": "ethereum"}' | python3 scripts/function_decoder.py

# Run comprehensive security audit
echo '{"contract_address": "0xdAC17F958D2ee523a2206206994597C13D831ec7", "chain": "ethereum"}' | python3 scripts/contract_security_audit.py

# Analyze ABI for access control risks
echo '{"contract_address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", "chain": "ethereum"}' | python3 scripts/abi_risk_analyzer.py
```

## Scripts

| Script | Purpose | APIs Used |
|--------|---------|-----------|
| [contract_source_analyzer.py](scripts/contract_source_analyzer.py) | Source code vulnerability scanning | Sourcify |
| [function_decoder.py](scripts/function_decoder.py) | Function selector decoding + dangerous function detection | Blockscout + 4byte.directory |
| [contract_security_audit.py](scripts/contract_security_audit.py) | Multi-source comprehensive security audit | GoPlus + Sourcify + Blockscout |
| [abi_risk_analyzer.py](scripts/abi_risk_analyzer.py) | ABI access control and privilege risk analysis | Blockscout + Sourcify |

## Detailed API Documentation

### contract_source_analyzer.py

Fetches verified Solidity source code from Sourcify and performs regex-based static analysis for 12+ vulnerability patterns.

**Input:**
```json
{
  "contract_address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
  "chain": "ethereum"
}
```

**Output:**
```json
{
  "success": true,
  "scan_type": "source_analysis",
  "contract": {
    "address": "0xdac17f958d2ee523a2206206994597c13d831ec7",
    "name": "TetherToken",
    "chain": "ethereum",
    "compiler_version": "v0.4.18+commit.9cf6e910",
    "verification_status": "partial"
  },
  "source_files": ["TetherToken.sol"],
  "findings": [
    {
      "severity": "MEDIUM",
      "pattern": "floating_pragma",
      "description": "Compiler version not locked",
      "detail": "pragma solidity ^0.4.17",
      "line": 1,
      "recommendation": "Lock compiler version to avoid unexpected behavior"
    }
  ],
  "risk_assessment": {
    "score": 3,
    "level": "LOW",
    "total_findings": 2,
    "critical": 0,
    "high": 0,
    "medium": 1,
    "low": 1,
    "info": 0
  }
}
```

**Vulnerability Patterns Detected:**

| Pattern | Severity | Description |
|---------|----------|-------------|
| Reentrancy | CRITICAL | External call before state update |
| selfdestruct | CRITICAL | Contract destruction capability |
| delegatecall | CRITICAL | Arbitrary code execution via delegation |
| tx.origin | HIGH | Authentication bypass risk |
| Unchecked call | HIGH | Unhandled low-level call return value |
| Unprotected initializer | HIGH | Initializer callable by anyone |
| Floating pragma | MEDIUM | Unlocked compiler version |
| Timestamp dependence | MEDIUM | Block timestamp in critical logic |
| Assembly usage | LOW | Inline assembly blocks |
| transfer/send | LOW | Fixed gas stipend (2300 gas) |

### function_decoder.py

Decodes function selectors from a contract's ABI and identifies dangerous/admin functions using 4byte.directory intelligence.

**Input:**
```json
{
  "contract_address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
  "chain": "ethereum"
}
```

**Output:**
```json
{
  "success": true,
  "scan_type": "function_analysis",
  "contract": {
    "address": "0xdac17f958d2ee523a2206206994597c13d831ec7",
    "name": "TetherToken",
    "chain": "ethereum"
  },
  "functions": {
    "total": 25,
    "read_only": 12,
    "state_changing": 13,
    "admin": 5,
    "dangerous": 0
  },
  "dangerous_functions": [],
  "admin_functions": [
    {
      "name": "pause",
      "selector": "0x8456cb59",
      "category": "pause_control",
      "risk": "Can freeze all token transfers"
    }
  ],
  "risk_assessment": {
    "score": 3,
    "level": "LOW"
  }
}
```

**Function Categories:**

| Category | Risk | Examples |
|----------|------|---------|
| Destruction | CRITICAL | selfdestruct, suicide, kill |
| Delegation | CRITICAL | delegatecall, callcode |
| Ownership | HIGH | transferOwnership, setOwner |
| Minting | HIGH | mint, mintTo, batchMint |
| Pause Control | MEDIUM | pause, unpause, freeze |
| Blacklisting | MEDIUM | blacklist, addToBlacklist |
| Fee Manipulation | MEDIUM | setFee, setTax, updateFee |
| Upgrades | HIGH | upgradeTo, upgradeToAndCall |

### contract_security_audit.py

Comprehensive security audit combining GoPlus security intelligence, Sourcify verification, and Blockscout metadata.

**Input:**
```json
{
  "contract_address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
  "chain": "ethereum"
}
```

**Output:**
```json
{
  "success": true,
  "scan_type": "security_audit",
  "contract": {
    "address": "0xdac17f958d2ee523a2206206994597c13d831ec7",
    "chain": "ethereum",
    "chain_id": "1"
  },
  "verification": {
    "sourcify_status": "partial",
    "blockscout_verified": true,
    "contract_name": "TetherToken",
    "compiler": "v0.4.18+commit.9cf6e910"
  },
  "goplus_security": {
    "is_honeypot": false,
    "has_malicious_behavior": false,
    "is_proxy": false,
    "is_open_source": true,
    "buy_tax": 0.0,
    "sell_tax": 0.0,
    "flags": ["Token has blacklist function", "Token is mintable"]
  },
  "contract_metadata": {
    "is_proxy": false,
    "proxy_type": null,
    "implementations": [],
    "creator": "0x36928500Bc1dCd7af6a2B...",
    "is_scam": false
  },
  "risk_assessment": {
    "score": 2,
    "level": "LOW",
    "factors": [
      {"factor": "Verified source code", "impact": "0 (positive)"},
      {"factor": "Blacklist capability", "impact": "+1"},
      {"factor": "Mintable token", "impact": "+1"}
    ]
  },
  "recommendations": [
    "Review blacklist function usage",
    "Monitor minting events for unexpected supply changes"
  ]
}
```

### abi_risk_analyzer.py

Deep ABI analysis for access control patterns, admin functions, upgrade mechanisms, and privilege escalation risks.

**Input:**
```json
{
  "contract_address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
  "chain": "ethereum"
}
```

**Output:**
```json
{
  "success": true,
  "scan_type": "abi_risk_analysis",
  "contract": {
    "address": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
    "name": "FiatTokenProxy",
    "chain": "ethereum"
  },
  "abi_summary": {
    "total_functions": 30,
    "read_only": 15,
    "state_changing": 15,
    "events": 8,
    "errors": 0
  },
  "access_control": {
    "pattern": "Role-Based (Custom)",
    "admin_functions": 8,
    "has_ownership": true,
    "has_roles": true,
    "is_upgradeable": true
  },
  "admin_inventory": [
    {
      "name": "updateMasterMinter",
      "inputs": ["address"],
      "risk": "HIGH",
      "description": "Can change minting authority"
    }
  ],
  "risk_assessment": {
    "score": 4,
    "level": "MEDIUM",
    "factors": [
      {"factor": "Proxy contract (upgradeable)", "impact": "+2"},
      {"factor": "8 admin functions", "impact": "+1"},
      {"factor": "Multiple role types", "impact": "+1"}
    ]
  }
}
```

## Risk Scoring System

All scripts use a unified 0-10 risk scoring system:

| Level | Score | Action |
|-------|-------|--------|
| SAFE | 0-1 | No significant risks detected |
| LOW | 2-3 | Minor concerns, generally safe |
| MEDIUM | 4-5 | Proceed with caution |
| HIGH | 6-7 | Significant risks — not recommended |
| CRITICAL | 8-10 | Likely malicious or highly dangerous — avoid |

## Supported Chains

| Chain | ID | Sourcify | Blockscout | GoPlus | 4byte |
|-------|----|----------|------------|--------|-------|
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
| *(none)* | — | **No environment variables needed** |

All APIs used are free and require no authentication.

## Error Handling

All scripts return structured error responses:

```json
{"error": "Invalid address format: xyz. Expected 0x followed by 40 hex characters."}
{"error": "Contract not verified on Sourcify. Try contract_security_audit.py for unverified contracts."}
{"error": "Rate limit exceeded. Please wait 1-2 minutes before retrying."}
```

| Error | Cause | Solution |
|-------|-------|----------|
| Invalid address | Wrong format | Use 0x + 40 hex chars |
| Not verified | Source not on Sourcify | Use security_audit or abi_analyzer instead |
| Rate limit | Too many requests | Wait 1-2 minutes |
| Connection failed | Network issues | Check internet connection |

## Security Design

This skill follows strict security principles:

1. **Read-Only** — NEVER sends transactions, signs messages, or modifies blockchain state
2. **No Keys Required** — Zero API keys, zero private keys, zero wallet connections
3. **No Data Storage** — No user data persisted beyond the API call
4. **Input Validation** — Regex validation on all addresses, chain whitelist
5. **Safe Errors** — No stack traces or internal details in error messages
6. **Multi-Source** — Cross-references Sourcify, Blockscout, GoPlus, and 4byte.directory
7. **Conservative** — Flags suspicious patterns even when unconfirmed

## Use Cases

1. **Before interacting with a contract** — Verify source code and check for vulnerabilities
2. **Due diligence on DeFi protocols** — Comprehensive security audit before depositing
3. **Code review assistance** — Automated vulnerability scanning for Solidity developers
4. **Admin function inventory** — Identify centralization risks in governance tokens
5. **Proxy contract analysis** — Detect upgrade mechanisms and implementation contracts

## Composability

This skill composes well with other SpoonOS skills:

- **+ DeFi Safety Shield**: Combine contract audit with token risk + approval analysis
- **+ Market Intelligence**: Security check before acting on trading signals
- **+ On-Chain Analysis**: Pair security audit with transaction/wallet profiling
- **+ DeFi Operations**: Verify protocol contracts before executing trades

## License

MIT License
