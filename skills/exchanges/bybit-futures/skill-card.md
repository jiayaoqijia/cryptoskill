## Description: <br>
Complete Bybit USDT perpetual futures trading system with risk management, paper trading, backtesting, and live execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sunnyztj](https://clawhub.ai/user/Sunnyztj) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and trading-system operators use this skill to build, configure, paper trade, backtest, and optionally run Bybit USDT perpetual futures bots with configurable risk controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live trading can place real Bybit futures orders and incur financial losses. <br>
Mitigation: Start with paper trading or Bybit testnet, use an isolated low-balance account, and keep position size, leverage, stop loss, daily loss, and open-position limits conservative. <br>
Risk: Trading API credentials can authorize account actions if over-permissioned or exposed. <br>
Mitigation: Use environment variables or a secrets manager, pin dependencies, and create a Bybit API key limited to Contract trading with no withdrawal or asset permissions. <br>
Risk: Optional Telegram notifications and systemd persistence can continue sharing events or running the bot after setup. <br>
Mitigation: Enable Telegram or systemd persistence only when the operator understands what data is shared and how to stop the bot. <br>


## Reference(s): <br>
- [Bybit API Notes & Gotchas](references/bybit_api_notes.md) <br>
- [Adding Custom Strategies](references/custom_strategy.md) <br>
- [Bybit API Management](https://www.bybit.com/app/user/api-management) <br>
- [Bybit Testnet API](https://api-testnet.bybit.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code snippets, shell commands, and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include trading configuration, API setup guidance, backtest commands, paper trading steps, and live execution guidance.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
