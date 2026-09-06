## Description: <br>
Read-only Hyperliquid market data assistant with support for natural-language requests and deterministic command parsing through terminal-style `hl ...` and slash-style `/hl ...` commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[k0nkupa](https://clawhub.ai/user/k0nkupa) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to query Hyperliquid market data and read-only account views through natural language or `hl` commands. It formats quotes, movers, funding rankings, order books, candles, positions, balances, orders, and fills for chat without private keys or trading. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can query wallet-linked positions, balances, orders, and fills for supplied Hyperliquid addresses. <br>
Mitigation: Use account features only when comfortable exposing those read-only views in the agent session. <br>
Risk: Saved account aliases are written to `~/.clawdbot/hyperliquid/config.json`. <br>
Mitigation: Avoid saving aliases on shared or managed machines, and review or delete the local config file when needed. <br>
Risk: Changing `HYPERLIQUID_INFO_URL` sends requests to a replacement API endpoint. <br>
Mitigation: Leave `HYPERLIQUID_INFO_URL` unset unless the replacement endpoint is intentionally trusted. <br>


## Reference(s): <br>
- [Hyperliquid API Notes](references/hyperliquid-api.md) <br>
- [Hyperliquid Info Endpoint](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint) <br>
- [Hyperliquid Perpetuals API](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint/perpetuals) <br>
- [Hyperliquid Spot API](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint/spot) <br>
- [ClawHub Skill Page](https://clawhub.ai/k0nkupa/skills/hyperliquid) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown-like plain text with concise bullet lists and terminal command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Hyperliquid API responses formatted for chat; account aliases may be saved locally.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
