---
name: gate-info-riskcheck
version: "2026.4.3-1"
updated: "2026-04-03"
description: "Token and address risk assessment. Use this skill ONLY when the user's query is exclusively about token/contract/address security with no other analysis dimensions. Trigger phrases: is this token safe, check contract risk, is this address safe, honeypot, rug. If the query ALSO mentions fundamentals, technicals, news, sentiment, or any other analysis dimension, use gate-info-research instead — it handles multi-dimension queries in a single unified report. Address risk mode (is this address safe) is exclusive to this skill and must NOT be routed to gate-info-research."
required_credentials: []
required_env_vars: []
required_permissions: []
---

# gate-info-riskcheck

## General Rules

⚠️ STOP — You MUST read and strictly follow the shared runtime rules before proceeding.
Do NOT select or call any tool until all rules are read. These rules have the highest priority.
→ Read `../gate-runtime-rules.md`
→ Also read `../info-news-runtime-rules.md` for gate-info / gate-news shared rules (tool degradation, report standards, security, routing, and optional local maintenance when `scripts/` is present).
- **Only call MCP tools explicitly listed in this skill.** Tools not documented here must NOT be called, even if they
  exist in the MCP server.

> Security guardian Skill. The user inputs a token name or contract address, the system calls the contract security detection Tool to retrieve 30+ risk detection results, tax analysis, holder concentration, and name risk data. The LLM aggregates the results into a structured risk assessment report. Address compliance checking will be added in a future phase.

**Trigger Scenarios**: User mentions a token/contract address + keywords like safe, risk, check, audit, honeypot, rug, contract security, scam.

**Local maintenance (optional, repository copy only):**
- If `scripts/update-skill.*` exists in the repository copy, `check` may compare the installed copy with the packaged skill source used by the current install.
- Ask the user before `apply`.
- `apply` updates files within this skill directory only.

---

## MCP Dependencies

### Required MCP Servers
| MCP Server | Status |
|------------|--------|
| Gate-Info | ✅ Required |

### MCP Tools Used

**Query Operations (Read-only)**

- info_coin_get_coin_info
- info_compliance_check_address_risk
- info_compliance_check_token_security
- info_onchain_get_address_info

### Authentication
- API Key Required: No
- Credentials Source: None; this skill uses read-only Gate Info / Gate News MCP access only.

### Installation Check
- Required: Gate-Info
- Install: Use the local Gate MCP installation flow for the current host IDE before continuing.
- Continue only after the required Gate MCP server is available in the current environment.

## Routing Rules

| User Intent | Keywords/Pattern | Action |
|-------------|-----------------|--------|
| Token contract security check | "is this token safe" "any risk with PEPE contract" "check 0x... contract" | Execute this Skill (Token Security mode) |
| Address risk check | "is this address safe" "is this a blacklisted address" | Execute this Skill (Address Risk mode — currently degraded) |
| Single coin analysis | "analyze SOL for me" | Route to `gate-info-coinanalysis` |
| Address tracking | "track this address" "fund flow" | Route to `gate-info-addresstracker` |
| Token on-chain analysis | "on-chain chip distribution" | Route to `gate-info-tokenonchain` |
| Project due diligence | "is this project legit" "team background" | Route to `gate-info-coinanalysis` (fundamentals focus) |

---

## Execution Workflow

### Step 0: Multi-Dimension Intent Check

Before executing this Skill, check if the user's query involves multiple analysis dimensions:

- If the query is about **address safety** (e.g., "is this address safe", "check 0x..."), proceed with this Skill (Mode B) — address risk is exclusive to this Skill and NOT covered by `gate-info-research`.
- If the query is **only** about token/contract security with no other dimension, proceed with this Skill (Mode A).
- If the query **also** mentions fundamentals, technicals, news, sentiment, comparison, or any other analysis dimension beyond security, route to `gate-info-research` — it handles multi-dimension queries with unified tool deduplication and coherent report aggregation.

### Mode A: Token Security Check (Core Mode — Ready)

#### Step 1: Intent Recognition & Parameter Extraction

Extract from user input:
- `token`: Token symbol (e.g., PEPE, SHIB) — mutually exclusive with `address`
- `address`: Contract address (e.g., 0x...) — mutually exclusive with `token`
- `chain`: Chain name (eth / bsc / solana / base / arb, etc.) — **required**

**Parameter Completion Strategy**:
- If user provides only token without chain: ask "Please specify the chain (e.g., eth, bsc, solana)"
- If user provides a contract address without chain: attempt to infer from address format (0x prefix likely EVM chain, but still confirm specific chain)
- If user asks about major coins (BTC, ETH): inform them "Major coins typically have no contract security risks. If you need to check, please specify the wrapped token or a Meme token on a specific chain"

#### Step 2: Call 2 MCP Tools in Parallel

| Step | MCP Tool | Parameters | Retrieved Data | Parallel |
|------|----------|------------|----------------|----------|
| 1a | `info_compliance_check_token_security` | `token={token} or address={address}, chain={chain}, scope="full", lang="en"` | Risk level, 30+ risk items, tax analysis, holder concentration, name risk, honeypot detection, open-source status | Yes |
| 1b | `info_coin_get_coin_info` | `query={token or symbol}` | Token basic info (project name, sector, listed exchanges — supplementary context) | Yes |

> Both Tools are called in parallel with no dependencies.

#### Step 3: LLM Aggregation — Generate Risk Report

Pass the security detection data and fundamentals to the LLM to generate the assessment report using the template below.

### Mode B: Address Risk Check (Degraded Mode)

> `info_compliance_check_address_risk` is not yet available (P3 phase). Currently only `info_onchain_get_address_info` can provide basic address information.

| Step | MCP Tool | Parameters | Retrieved Data | Status |
|------|----------|------------|----------------|--------|
| 1 | `info_onchain_get_address_info` | `address={address}, chain={chain}` | Basic address info, balance, transaction count | ✅ Available |
| 2 | `info_compliance_check_address_risk` | — | Address compliance risk labels | ❌ Not ready |

**Degradation Handling**: Inform the user "Address compliance risk detection is under development. Currently only basic address information is available. For token contract security checks, please provide the token name or contract address."

---

## Report Template (Token Security Mode)

```markdown
## {token} Contract Security Report

### 1. Risk Overview

| Metric | Result |
|--------|--------|
| Chain | {chain} |
| Contract Address | {address} |
| Overall Risk Level | {risk_level_text} ({highest_risk_level}) |
| High-Risk Items | {high_risk_num} |
| Medium-Risk Items | {middle_risk_num} |
| Low-Risk Items | {low_risk_num} |
| Honeypot Detected | {is_honeypot ? "⛔ Yes" : "✅ No"} |
| Open Source | {is_open_source ? "✅ Yes" : "⚠️ No"} |

### 2. High-Risk Item Details

{If high-risk items exist, list each:}

| Risk Item | Description | Value |
|-----------|------------|-------|
| {risk_name_1} | {risk_desc_1} | {risk_value_1} |
| {risk_name_2} | {risk_desc_2} | {risk_value_2} |
| ... | ... | ... |

{If no high-risk items: "✅ No high-risk items detected"}

### 3. Tax Analysis

| Metric | Value | Status |
|--------|-------|--------|
| Buy Tax | {buy_tax}% | {Normal/Elevated/Extreme} |
| Sell Tax | {sell_tax}% | {Normal/Elevated/Extreme} |
| Transfer Tax | {transfer_tax}% | {Normal/Elevated/Extreme} |

{If multiple DEX pools have different tax rates, list the major pool breakdowns}

### 4. Holder Concentration

| Metric | Value | Status |
|--------|-------|--------|
| Holder Count | {holder_count} | {Many/Normal/Low} |
| Top 10 Holder % | {top10_percent}% | {Normal/High/Extremely Concentrated} |
| Top 100 Holder % | {top100_percent}% | — |
| Developer Holdings | {dev_holding_percent}% | {Normal/High} |
| Insider Holdings | {insider_percent}% | {Normal/High} |
| Largest Single Holder | {max_holder_percent}% | {Normal/High} |

### 5. Name Risk

| Metric | Result |
|--------|--------|
| Domain Token | {is_domain_token ? "⚠️ Yes" : "✅ No"} |
| Contains Sensitive Words | {is_sensitive ? "⚠️ Yes" : "✅ No"} |
| Sensitive Words | {sensitive_words} |

### 6. Project Basic Info (Supplementary)

| Metric | Value |
|--------|-------|
| Project Name | {project_name} |
| Sector | {category} |
| Listed on Major Exchanges | {exchange_list} |

### 7. Overall Assessment

{LLM generates a 3-5 sentence comprehensive risk assessment:}
- Overall contract safety level
- Most critical risk items (if any)
- Whether holder concentration is healthy
- Whether tax rates are reasonable
- Whether further manual audit is recommended

### ⚠️ Risk Warnings

{Auto-generated explicit warnings based on detection results:}
- Honeypot detection (if applicable)
- High tax warning (if applicable)
- Excessive holder concentration (if applicable)
- Contract not open-source (if applicable)

> The above analysis is based on automated on-chain data detection and cannot cover all risk scenarios. Please combine with project due diligence and community research for comprehensive judgment.
```

---

## Decision Logic

| Condition | Assessment |
|-----------|------------|
| `is_honeypot == true` | **Highest-level warning**: "⛔ Detected as honeypot contract — extremely likely unable to sell. Do NOT purchase." |
| `is_open_source == false` | Flag "Contract is not open-source — code logic cannot be audited, elevated risk" |
| `buy_tax > 5%` or `sell_tax > 5%` | Flag "Abnormally high tax rate — extreme trading costs" |
| `buy_tax > 10%` or `sell_tax > 10%` | Flag "⛔ Extreme tax rate — suspected malicious contract" |
| `top10_percent > 50%` | Flag "Highly concentrated holdings — insider/whale dump risk" |
| `top10_percent > 80%` | Flag "⛔ Extremely concentrated holdings — dump risk is critical" |
| `dev_holding_percent > 10%` | Flag "Developer holdings are elevated — watch for sell-off risk" |
| `holder_count < 100` | Flag "Extremely few holders — insufficient liquidity and decentralization" |
| `high_risk_num > 0` | List each high-risk item with explanation |
| `high_risk_num == 0 && middle_risk_num <= 2` | Flag "Contract security check passed — no significant risks detected" |
| `is_domain_token == true` | Flag "This is a domain token — unrelated to the project of the same name. Verify carefully." |
| `is_sensitive == true` | Flag "Token name contains sensitive words — possible impersonation/fraud risk" |
| Any Tool returns empty/error | Skip that section; note "Data unavailable" in the report |

---

## Risk Level Mapping

| `highest_risk_level` Value | Risk Level | Label | Description |
|---------------------------|------------|-------|-------------|
| 0 | Safe | ✅ Safe | No risk items detected |
| 1 | Low Risk | Low Risk | Only low-risk items present |
| 2 | Medium Risk | Medium Risk | Medium-risk items present — monitor |
| 3 | High Risk | High Risk | High-risk items present — exercise extreme caution |
| is_honeypot=true | Critical Risk | ⛔ Critical Risk | Honeypot contract — strongly advise staying away |

---

## Error Handling

| Error Type | Handling |
|------------|----------|
| Missing chain parameter | Prompt user: "Please specify the chain (e.g., eth, bsc, solana, base, arb)" |
| Neither token nor address provided | Prompt user: "Please provide a token symbol or contract address" |
| Contract address does not exist / unrecognizable | Prompt user to verify the address and confirm the chain |
| Token is a major coin (BTC/ETH, etc.) | Inform: "Major coins typically have no contract security risks. For contract token checks, specify the wrapped token or Meme token on a specific chain" |
| check_token_security timeout/error | Return error message; suggest trying again later |
| Address risk query (currently unavailable) | Inform: "Address compliance detection is under development." Guide user to `gate-info-addresstracker` for basic address info |
| User inputs a regular address thinking it's a contract | Attempt detection; if empty result, inform "This may not be a contract address. For address information, use the Address Tracker feature" |

---

## Cross-Skill Routing

| User Follow-up Intent | Route To |
|-----------------------|----------|
| "Analyze this coin for me" | `gate-info-coinanalysis` |
| "What about on-chain chip distribution?" | `gate-info-tokenonchain` |
| "Any recent news?" | `gate-news-briefing` |
| "Track this address" | `gate-info-addresstracker` |
| "Compare this with XX" | `gate-info-coincompare` |
| "How is this coin's price action?" | `gate-info-trendanalysis` |

---

## Available Tools & Degradation Notes

| PRD-Defined Tool | Actually Available Tool | Status | Degradation Strategy |
|-----------------|----------------------|--------|---------------------|
| `info_compliance_check_token_security` | `info_compliance_check_token_security` | ✅ Ready | — |
| `info_coin_get_coin_info` | `info_coin_get_coin_info` | ✅ Ready | — |
| `info_onchain_get_address_info` | `info_onchain_get_address_info` | ✅ Ready | Address mode can retrieve basic info |
| `info_compliance_check_address_risk` | — | ❌ Not ready (P3) | Address compliance risk detection unavailable — inform user and guide to address tracker |

---

## Safety Rules

1. **Mandatory honeypot warning**: When `is_honeypot=true` is detected, display the "⛔ Critical Risk" warning in the most prominent position — never downplay
2. **No investment advice**: Risk assessment is based on on-chain data and must include a "not investment advice" disclaimer
3. **No absolute safety guarantees**: Even if all checks pass, state that "automated detection cannot cover all risks"
4. **Data transparency**: Label detection data source and timestamp
5. **Flag missing data**: When any dimension has no data, explicitly inform the user — never fabricate safety conclusions
6. **Address privacy**: Do not proactively expose address holder identities — only display publicly available on-chain data
