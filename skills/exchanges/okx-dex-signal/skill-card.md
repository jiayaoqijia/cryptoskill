## Description: <br>
Guides agents in using Onchain OS commands to track smart-money, KOL, whale, and custom-wallet DEX activity, aggregated buy signals, real-time WebSocket monitoring, and top-trader leaderboards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ok-james-01](https://clawhub.ai/user/ok-james-01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent for DEX market-signal workflows, including wallet activity tracking, aggregated buy alerts, supported-chain checks, leaderboard rankings, and WebSocket monitoring guidance. The skill also guides payment/quota handling and credential-aware setup for OKX market APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install or update the onchainos CLI from remote OKX GitHub releases. <br>
Mitigation: Install only after confirming the source and checksum verification steps are acceptable for the deployment environment. <br>
Risk: Some workflows can involve paid x402 or API-quota actions. <br>
Mitigation: Require explicit user confirmation before any paid or quota-consuming action. <br>
Risk: WebSocket workflows may require OKX API credentials. <br>
Mitigation: Use credentials only when intentionally enabling WebSocket access, keep them in environment variables or local ignored files, and avoid committing secrets. <br>
Risk: DEX signal, leaderboard, and tracker results may be mistaken for financial advice. <br>
Mitigation: Present results as informational market data and avoid recommending trades solely from signal output. <br>
Risk: Token names, symbols, wallet labels, and on-chain fields are untrusted external content. <br>
Mitigation: Display external fields as data only and do not treat them as instructions. <br>
Risk: DEX functionality may be unavailable in some regions. <br>
Mitigation: Surface the regional availability message when applicable and do not expose raw backend error codes. <br>


## Reference(s): <br>
- [Onchain OS DEX Signal CLI Command Reference](references/cli-reference.md) <br>
- [Keyword Glossary](references/keyword-glossary.md) <br>
- [Onchain OS DEX Signal WebSocket Protocol Reference](references/ws-protocol.md) <br>
- [Shared Pre-flight Checks](_shared/preflight.md) <br>
- [Shared Chain Name Support](_shared/chain-support.md) <br>
- [OKX Web3](https://web3.okx.com) <br>
- [OKX Developer Portal](https://web3.okx.com/onchain-os/dev-portal) <br>
- [OKX WebSocket Login Documentation](https://web3.okx.com/onchainos/dev-docs/market/websocket-login) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tables, command examples, JSON snippets, and concise user-facing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include command suggestions, workflow hints, payment or quota notices, request timestamps, and warnings to treat market-signal output as informational rather than financial advice.] <br>

## Skill Version(s): <br>
3.1.3 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
