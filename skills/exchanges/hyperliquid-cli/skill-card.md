## Description: <br>
Trade crypto, stocks (AAPL, NVDA, TSLA), indexes, and commodities (GOLD, SILVER) 24/7 on Hyperliquid via HIP-3, with real-time position and P&L tracking, orderbook monitoring, multi-account management, and websocket client support for low-latency trading. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrisling-dev](https://clawhub.ai/user/chrisling-dev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, trading operators, and agents use this skill to install and operate the Hyperliquid CLI for market data, account monitoring, account setup, and order workflows across crypto and HIP3 markets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent live authority to trade with real funds through the Hyperliquid CLI. <br>
Mitigation: Use testnet first and prefer a dedicated low-balance or restricted API wallet before allowing mainnet trading. <br>
Risk: Private keys and account data may be exposed if stored in shell profiles, shared environments, logs, or exported position data. <br>
Mitigation: Avoid raw private keys in shared shell environments, keep wallet material scoped to local account storage where possible, and review any logging or export destinations before use. <br>
Risk: Leveraged trading and HIP3 market identifiers can create unintended financial exposure when commands are issued with the wrong coin value, size, or margin setting. <br>
Mitigation: Check market identifiers with `hl markets ls`, verify leverage and margin with `hl asset leverage`, and require human review before order placement. <br>
Risk: Installing a global npm CLI adds supply-chain risk for a tool that can control trading accounts. <br>
Mitigation: Verify the npm package source and installed version before connecting any wallet with trading authority. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chrisling-dev/skills/hyperliquid-cli) <br>
- [Hyperliquid CLI repository](https://github.com/chrisling-dev/hyperliquid-cli) <br>
- [Hyperliquid API wallet setup](https://app.hyperliquid.xyz/API) <br>
- [Hyperliquid CLI Reference](artifact/reference.md) <br>
- [Hyperliquid CLI Examples](artifact/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that query balances, configure accounts, start a local server, or place live orders when connected to a funded API wallet.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
