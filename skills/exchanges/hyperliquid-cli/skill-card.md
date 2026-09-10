## Description:

Trade crypto, stocks (AAPL, NVDA, TSLA), indexes, and commodities (GOLD, SILVER) 24/7 on Hyperliquid via HIP-3. Real-time position & P&L tracking, orderbook monitoring, multi-account management, and websocket client for sub-5ms low-latency high-frequency trading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrisling-dev](https://clawhub.ai/user/chrisling-dev)

### License/Terms of Use:


## Use Case:

External developers and traders use this skill to install and operate the Hyperliquid CLI for market data, account monitoring, order placement, leverage checks, and automated trading workflows. It supports both API-wallet trading and read-only monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide live-funds trading and private-key setup.

Mitigation: Use a dedicated low-balance API wallet, prefer read-only mode for monitoring, and review all trade commands before execution.

Risk: The install command uses an unpinned global npm package.

Mitigation: Verify the npm package name and version before installing or upgrading the CLI.

Risk: Account JSON may expose sensitive trading or portfolio data if sent to external services.

Mitigation: Send account data only to trusted endpoints and minimize webhook payloads.

Risk: Private keys can leak through shell history or long-lived environment variables.

Mitigation: Avoid storing private keys in shell history or persistent environment files; use local account management where appropriate.

Risk: The skill includes optional referral guidance unrelated to core setup.

Mitigation: Treat referral links as optional and separate from installation or wallet configuration.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chrisling-dev/skills/hyperliquid-cli)
- [Hyperliquid CLI GitHub Repository](https://github.com/chrisling-dev/hyperliquid-cli)
- [Hyperliquid API Wallet Setup](https://app.hyperliquid.xyz/API)
- [Hyperliquid App](https://app.hyperliquid.xyz)
- [Command Reference](artifact/reference.md)
- [Workflow Examples](artifact/examples.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commands that execute live trades or monitor account data; users should review commands before execution.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
