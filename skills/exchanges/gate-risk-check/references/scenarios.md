# gate-info-riskcheck — Scenarios & Prompt Examples

## Scenario 1: Token security check with symbol + chain (English)

**Context**: User asks if a token is safe and provides chain.

**Prompt Examples**:
- "Is PEPE safe on eth"
- "Check the risk of this coin on base"
- "Any issues with SHIB contract on bsc"

**Expected Behavior**:
1. Extract token (e.g. PEPE), chain (eth). Call in parallel: `info_compliance_check_token_security`(token=PEPE, chain=eth, scope=full), `info_coin_get_coin_info`(query=PEPE).
2. Output **7-section Contract Security Report**: Risk Overview, High-Risk Item Details, Tax Analysis, Holder Concentration, Name Risk, Project Basic Info, Overall Assessment + Risk Warnings. If honeypot detected, show Critical Risk warning prominently.

## Scenario 2: Contract address + chain (Chinese)

**Context**: User provides contract address and chain.

**Prompt Examples**:
- "Is this contract 0x... safe on eth"
- "Check this contract 0x... on base"

**Expected Behavior**:
1. Extract address, chain. Call `info_compliance_check_token_security`(address=0x..., chain=eth) and `info_coin_get_coin_info` (if symbol derivable). Generate same 7-section report.
2. Data unavailable for a section → mark "Data unavailable"; do not fabricate.

## Scenario 3: Token without chain (prompt for chain)

**Context**: User asks about token risk but does not specify chain.

**Prompt Examples**:
- "Is this token safe"
- "Is PEPE safe"

**Expected Behavior**:
1. Prompt user: "Please specify the chain (e.g., eth, bsc, solana, base, arb)".
2. Do not call tools until chain is provided.

## Scenario 4: Address risk (degraded mode)

**Context**: User asks if an address is safe.

**Prompt Examples**:
- "Is this address safe 0x..."
- "Is this a blacklisted address"

**Expected Behavior**:
1. Call `info_onchain_get_address_info`(address, chain). Do not call `info_compliance_check_address_risk` (not available).
2. Inform user: "Address compliance risk detection is under development. Currently only basic address information is available. For token contract security checks, please provide the token name or contract address." Optionally show basic address info and route to `gate-info-addresstracker` for full tracking.

## Scenario 5: Major coin (BTC/ETH) — guide to specify wrapped/meme

**Context**: User asks if BTC or ETH is safe.

**Prompt Examples**:
- "Is BTC safe"
- "Check ETH contract risk"

**Expected Behavior**:
1. Inform: "Major coins typically have no contract security risks. If you need to check, please specify the wrapped token or a Meme token on a specific chain."
2. Do not run full token security check for native BTC/ETH without clarification.
