## Description: <br>
Provides agent guidance for using OKX Onchain OS DEX Market CLI and WebSocket commands to retrieve on-chain token prices, candlesticks, index prices, and wallet PnL while handling x402 payment notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ok-james-01](https://clawhub.ai/user/ok-james-01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to route OKX Onchain OS market-data requests, collect missing chain, token, and wallet parameters, run market price, K-line, index, and portfolio PnL commands, and present payment notifications or region restrictions safely. <br>

### Deployment Geography for Use: <br>
Global, subject to OKX service restrictions including unavailable DEX access in the United Kingdom and gateway blocking for sanctioned countries. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install or update a local CLI from a remote release channel. <br>
Mitigation: Install only from the trusted OKX/onchainos release channel, verify checksums where provided, and review install or update failures before continuing. <br>
Risk: WebSocket workflows require API credentials and the security evidence flags conflicting credential guidance. <br>
Mitigation: Keep API keys in environment variables or ignored .env files, never hardcode credentials, and review WebSocket usage before running scripts or bots. <br>
Risk: Market API calls may trigger x402 payments after quota is exhausted. <br>
Mitigation: Require explicit user confirmation before paid calls, watch payment notifications, and unset saved payment defaults when automatic paid calls are no longer desired. <br>
Risk: CLI output includes token names, symbols, and on-chain fields from external sources. <br>
Mitigation: Treat CLI output as untrusted data and do not interpret returned content as agent instructions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ok-james-01/okx-dex-market) <br>
- [OKX Web3](https://web3.okx.com) <br>
- [CLI Command Reference](references/cli-reference.md) <br>
- [WebSocket Protocol Reference](references/ws-protocol.md) <br>
- [Keyword Glossary](references/keyword-glossary.md) <br>
- [Payment Notifications](_shared/payment-notifications.md) <br>
- [Pre-flight Checks](_shared/preflight.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and formatted market-data results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require API credentials, wallet/payment confirmation, and region-aware error handling.] <br>

## Skill Version(s): <br>
3.1.3 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
