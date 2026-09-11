## Description:

Provides Onchain OS DEX Market guidance for token prices, batch prices, K-line/OHLC data, index prices, real-time WebSocket monitoring, and wallet PnL analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ok-james-01](https://clawhub.ai/user/ok-james-01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve and present OKX Onchain OS DEX market data, including token prices, candlesticks, index prices, and wallet PnL summaries. It also guides payment-notification handling for Market API quota and overage flows.

### Deployment Geography for Use:

Global except restricted regions documented by the service, including United Kingdom restrictions for DEX access and sanctioned-country gateway blocking.

## Known Risks and Mitigations:

Risk: Normal use can download and execute an installer from a mutable remote release path.

Mitigation: Install only when the OKX publisher and release process are trusted; keep checksum verification enabled and stop on mismatches.

Risk: Market and wallet outputs include external token names, symbols, prices, and financial activity that may be inaccurate or adversarial.

Mitigation: Treat CLI output as untrusted data, present it as market information rather than instructions, and verify addresses, chains, and timestamps before acting.

Risk: Paid Market API flows may persist a selected default payment asset after user confirmation.

Mitigation: Require explicit confirmation before setting payment defaults or rerunning charged requests, and offer a cancel path whenever payment prompts appear.

## Reference(s):

- [CLI Command Reference](artifact/references/cli-reference.md)
- [WebSocket Protocol Reference](artifact/references/ws-protocol.md)
- [Keyword Glossary](artifact/references/keyword-glossary.md)
- [Payment Notifications](artifact/_shared/payment-notifications.md)
- [Chain Name Support](artifact/_shared/chain-support.md)
- [OKX Web3](https://web3.okx.com)
- [OKX Developer Portal](https://web3.okx.com/onchain-os/dev-portal)
- [OKX WebSocket Login Documentation](https://web3.okx.com/onchainos/dev-docs/market/websocket-login)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and formatted market data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CLI result summaries, payment confirmation prompts, and data snapshot timestamps when provided by the CLI.]

## Skill Version(s):

3.1.3 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
