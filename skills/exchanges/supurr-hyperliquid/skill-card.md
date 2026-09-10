## Description:

Backtest, deploy, and monitor trading bots on Hyperliquid with Grid, DCA, and Spot-Perp Arbitrage strategies across Native Perps, Spot markets, and HIP-3 sub-DEXes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yashagarwal1994](https://clawhub.ai/user/yashagarwal1994)

### License/Terms of Use:

MIT

## Use Case:

External developers and trading operators use this skill to have an agent generate Supurr CLI commands, strategy configuration, backtest steps, deployment commands, and monitoring guidance for Hyperliquid trading bots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote installers and release-hosted CLI binaries run under the installing user account.

Mitigation: Install only from a trusted Supurr release path, and prefer pinned, checksum- or signature-verified downloads.

Risk: API-wallet private keys may be provided to the CLI in plaintext.

Mitigation: Use a restricted API wallet and subaccount, avoid placing real keys in shell history, and rotate any key previously supplied on the command line.

Risk: The skill can guide live bot deployment, which can place trades and create financial loss.

Mitigation: Review generated configs before deployment, backtest first, start with limited funds, and isolate bot activity with restricted accounts where possible.

## Reference(s):

- [Supurr CLI Command Reference](SKILL.md)
- [Grid Bot Tutorial](tutorials/grid.md)
- [DCA Bot Tutorial](tutorials/dca.md)
- [Arb Bot Tutorial](tutorials/arb.md)
- [Hyperliquid Info API](https://api.hyperliquid.xyz/info)
- [Supurr CLI Installer](https://cli.supurr.app/install)
- [Supurr Skill Installer](https://cli.supurr.app/skill-install)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command sequences for credential setup, config generation, backtesting, deployment, monitoring, updates, and troubleshooting.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
