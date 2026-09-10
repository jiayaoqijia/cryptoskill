## Description:

Helps agents build, configure, backtest, paper trade, and optionally run Bybit USDT perpetual futures trading workflows with risk controls and strategy templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunnyztj](https://clawhub.ai/user/sunnyztj)

### License/Terms of Use:


## Use Case:

Developers and trading-system builders use this skill to assemble Bybit futures bots, configure API credentials and risk parameters, run historical backtests, test strategies in paper mode, and prepare live execution workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The live trading workflow can place real leveraged futures orders.

Mitigation: Audit and modify the code before live use, validate behavior with paper trading or testnet first, and connect only API keys restricted to contract trading with withdrawals disabled.

Risk: The deployment guidance recommends a persistent root-level systemd service.

Mitigation: Avoid the root deployment pattern or convert it to a locked-down user service with limited filesystem, network, and secret access.

Risk: Telegram notifications can send trading details to a configured chat.

Mitigation: Disable Telegram unless the destination chat is trusted and the user accepts sharing position and performance details there.

Risk: Risk controls are documented but security evidence says safety controls need review before real funds are connected.

Mitigation: Confirm stop-loss, take-profit, position sizing, daily loss limits, and max-position behavior under realistic failure cases before using live capital.

## Reference(s):

- [Bybit API Notes](artifact/references/bybit_api_notes.md)
- [Custom Strategy Guide](artifact/references/custom_strategy.md)
- [Bybit API Management](https://www.bybit.com/app/user/api-management)
- [Bybit Testnet API](https://api-testnet.bybit.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code, configuration examples, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may guide API setup, backtesting, paper trading, and live trading; live behavior depends on user credentials, configuration, and Bybit API responses.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
