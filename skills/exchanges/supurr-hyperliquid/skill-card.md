## Description: <br>
Backtest, deploy, and monitor trading bots on Hyperliquid. Supports Grid, DCA, and Spot-Perp Arbitrage strategies across Native Perps, Spot markets (USDC/USDH), and HIP-3 sub-DEXes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yashagarwal1994](https://clawhub.ai/user/yashagarwal1994) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, trading operators, and external users use this skill to guide an agent through Supurr CLI workflows for Hyperliquid strategy setup, backtesting, deployment, monitoring, and bot shutdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill covers live trading workflows and commands that can deploy or stop bots using wallet credentials. <br>
Mitigation: Require explicit human approval before live deploy, stop, or update actions; prefer testnet, subaccounts, or limited API wallets for initial use. <br>
Risk: The installers fetch shell scripts and binaries from Supurr-controlled endpoints. <br>
Mitigation: Install only if Supurr and its release infrastructure are trusted; inspect installer scripts before running them and avoid piping remote scripts directly to a shell. <br>
Risk: Credential setup stores wallet address and private key material under the user's Supurr configuration directory. <br>
Mitigation: Do not paste private keys into shared shells, protect local credential files, and check permissions on ~/.supurr/credentials.json. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yashagarwal1994/supurr-hyperliquid) <br>
- [Supurr CLI command reference](SKILL.md) <br>
- [Grid bot tutorial](tutorials/grid.md) <br>
- [DCA bot tutorial](tutorials/dca.md) <br>
- [Arb bot tutorial](tutorials/arb.md) <br>
- [Hyperliquid Info API](https://api.hyperliquid.xyz/info) <br>
- [Supurr CLI installer](https://cli.supurr.app/install) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational guidance for a trading CLI; live deployment, stop, update, and credential-handling steps should remain subject to explicit human approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
