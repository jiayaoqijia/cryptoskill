# gate-info-riskcheck

## Overview

An AI Agent skill that performs **token contract security and address risk assessment**. **Mode A (Token Security)**: parallel `info_compliance_check_token_security` + `info_coin_get_coin_info` → structured risk report (risk overview, high-risk items, tax, holder concentration, name risk, project info, overall assessment). **Mode B (Address Risk)**: degraded — only `info_onchain_get_address_info` available; `info_compliance_check_address_risk` not yet ready. Chain parameter is required for token check. Read-only.

### Core Capabilities

| Capability | Description | Example |
|------------|-------------|---------|
| **Token security** | Honeypot, tax, holder concentration, name risk, 30+ risk items | "Is this token safe" / "Check PEPE contract risk" |
| **Contract check** | Risk level, high/medium/low risk counts, open source | "Check 0x... contract on eth" |
| **Address risk** | Currently degraded; basic address info only until check_address_risk is ready | "Is this address safe" |
| **7-section report** | Risk Overview, High-Risk Details, Tax, Holder Concentration, Name Risk, Project Info, Overall Assessment + Risk Warnings | Per SKILL.md Report Template |

### Routing

| User intent | Action |
|-------------|--------|
| Token/contract security | Execute this skill (Token Security mode) |
| Address risk | Execute this skill (Address Risk mode — degraded) |
| Single coin analysis | Route to `gate-info-coinanalysis` |
| Address tracking / fund flow | Route to `gate-info-addresstracker` |
| On-chain chip distribution | Route to `gate-info-tokenonchain` |

### Architecture

- **Input**: Token symbol or contract address + **chain** (required). Or address for Address Risk mode.
- **Tools**: Token mode — `info_compliance_check_token_security`, `info_coin_get_coin_info` (parallel). Address mode — `info_onchain_get_address_info` only; `info_compliance_check_address_risk` not available.
- **Output**: Contract Security Report (7 sections) or address degradation message. **Decision Logic** (honeypot, tax, concentration, name risk), **Risk Level Mapping**, **Error Handling**, **Safety** (mandatory honeypot warning, no safety guarantee) — see SKILL.md.
