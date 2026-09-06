## Description: <br>
Interact with Polymarket US prediction markets to browse or search markets, check prices and odds, view portfolio positions and balances, place or cancel trades, check order status, look up events or sports markets, and get market settlement info using the polymarket-us Python package. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tyhouch](https://clawhub.ai/user/tyhouch) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to browse Polymarket US prediction markets, inspect prices and portfolio data, and prepare authenticated trading actions through the polymarket-us Python SDK. It is intended for workflows where orders are previewed and explicitly confirmed before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated use can view portfolio data and place, cancel, modify, or close trades that may affect real money. <br>
Mitigation: Require explicit user confirmation after checking market, side, price, quantity, and time-in-force before any trading action. <br>
Risk: Private keys or API credentials could be exposed through chat, logs, or overly broad access. <br>
Mitigation: Keep the private key out of chat and logs, store credentials in environment variables, and use the least-privileged key available. <br>
Risk: The skill depends on the external polymarket-us package for SDK behavior. <br>
Mitigation: Install and use the package only when the operator trusts the package and its dependency chain. <br>
Risk: YES-side price semantics and market slug conventions can lead to incorrect order intent or price selection. <br>
Mitigation: Preview orders and present the market, YES/NO side, converted price, quantity, and intent clearly before execution. <br>


## Reference(s): <br>
- [Polymarket US API Reference](references/api_reference.md) <br>
- [Polymarket Developer Portal](https://polymarket.us/developer) <br>
- [Polymarket Public Data API](https://gateway.polymarket.us) <br>
- [Polymarket Trading API](https://api.polymarket.us) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include SDK usage examples, environment variable setup, market summaries, portfolio summaries, order previews, and user-confirmed trading guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
