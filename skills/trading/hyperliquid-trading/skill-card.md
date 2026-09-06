## Description: <br>
Trade and monitor Hyperliquid perpetual futures, including balance and position checks, market analysis, order placement, cancellation, and execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anajuliabit](https://clawhub.ai/user/anajuliabit) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to monitor Hyperliquid portfolios, analyze crypto market momentum, and prepare or execute perpetual futures trades through agent-run CLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent live Hyperliquid trading authority when HYPERLIQUID_PRIVATE_KEY is available. <br>
Mitigation: Use testnet or a dedicated limited wallet, avoid exposing a main wallet private key, and manually approve every order or cancel-all action before execution. <br>
Risk: Open orders or account state may differ from the agent's last response after a command runs. <br>
Mitigation: Verify open orders, fills, and positions directly after any trade or cancellation. <br>
Risk: The position checker writes portfolio state to a hard-coded local path. <br>
Mitigation: Change or remove the hard-coded trading-state path if local portfolio data should not be written there. <br>
Risk: Automated market signals and strategy examples may be mistaken for financial advice. <br>
Mitigation: Treat signals as informational decision support and verify trade rationale, size, and risk independently before trading. <br>


## Reference(s): <br>
- [Hyperliquid API Reference](references/api.md) <br>
- [Hyperliquid Official Docs](https://hyperliquid.gitbook.io/hyperliquid-docs/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live Hyperliquid and CoinGecko data when commands are run; trading commands require an explicit private key environment variable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and scripts/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
