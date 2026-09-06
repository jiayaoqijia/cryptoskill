## Description: <br>
Monitors Binance ETH/BTC perpetual futures price ratios, calculates z-scores, records signal JSON, and can send mean-reversion trade alerts to Telegram or Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lemonea](https://clawhub.ai/user/lemonea) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and quantitative-trading operators use this skill to monitor ETH/BTC statistical-arbitrage conditions, generate local signal records, and optionally send alert messages for manual review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated trading signals may be mistaken for automated financial advice. <br>
Mitigation: Treat signals as informational, manually review them, and validate strategy behavior before using them for live trading. <br>
Risk: Telegram or Feishu notification credentials can be exposed if configuration files are shared. <br>
Mitigation: Keep notification tokens private, use environment-specific configuration, and avoid committing real secrets. <br>
Risk: Market data access, regional API restrictions, fees, or extreme market moves can make signal estimates unreliable. <br>
Mitigation: Use testnet or dry-run validation, monitor API failures, and account for fees, slippage, and funding costs before acting. <br>


## Reference(s): <br>
- [Binance Stat Arb Monitor release page](https://clawhub.ai/lemonea/binance-stat-arb-monitor) <br>
- [Binance Futures API reference](references/binance_api.md) <br>
- [Statistical arbitrage strategy theory](references/stat_arb_theory.md) <br>
- [Binance Futures API documentation](https://binance-docs.github.io/apidocs/futures/cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance, shell commands, configuration JSON, local signal JSON, and notification text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes latest and historical signal files under data/ and may send Telegram or Feishu alerts when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
