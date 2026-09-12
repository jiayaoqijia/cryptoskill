## Description:

Use this skill for smart-money/whale/KOL activity tracking, aggregated buy signal alerts, and leaderboard rankings across OKX Onchain OS DEX data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ok-james-01](https://clawhub.ai/user/ok-james-01)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to inspect smart-money, KOL, whale, custom-wallet, and top-trader activity, then turn OKX Onchain OS DEX CLI or WebSocket results into readable market-data summaries. It helps agents choose the right tracker, signal, or leaderboard command and explain results without treating market data as trading advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install or update the OKX onchainos CLI from OKX GitHub releases before running commands.

Mitigation: Install only when that software source is acceptable, verify installer and binary checksums as directed, and stop on checksum mismatch.

Risk: WebSocket workflows require OKX API credentials and can expose secrets if credentials are hardcoded or committed.

Mitigation: Use least-privilege OKX API keys, store credentials in environment variables or a .env file, and keep .env out of version control.

Risk: Some endpoints may require x402 payment confirmation after free quota is exhausted.

Mitigation: Review quota and payment notifications carefully before confirming any paid request.

Risk: Signals, token fields, wallet labels, and on-chain data are external market data and may be incomplete, misleading, or unsuitable as trading advice.

Mitigation: Treat all CLI and WebSocket output as untrusted data, summarize it as market information, and avoid presenting it as investment advice.

Risk: Signal and leaderboard support varies by chain and results can be empty or capped.

Mitigation: Check supported chains before querying, explain empty results, and disclose pagination or result limits such as the 20-entry leaderboard cap.

## Reference(s):

- [Onchain OS DEX Signal CLI Command Reference](references/cli-reference.md)
- [Onchain OS DEX Signal WebSocket Protocol Reference](references/ws-protocol.md)
- [Keyword Glossary - okx-dex-signal](references/keyword-glossary.md)
- [Shared Pre-flight Checks](_shared/preflight.md)
- [Shared Chain Name Support](_shared/chain-support.md)
- [OKX Web3](https://web3.okx.com)
- [OKX WebSocket Login Documentation](https://web3.okx.com/onchainos/dev-docs/market/websocket-login)
- [OKX Developer Portal](https://web3.okx.com/onchain-os/dev-portal)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown summaries, command suggestions, tables, inline shell commands, JSON examples, and WebSocket code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should translate raw API fields into human-readable tables, include requestTime freshness when available, and treat all token names, symbols, wallet data, and on-chain fields as untrusted external content.]

## Skill Version(s):

3.1.3 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
