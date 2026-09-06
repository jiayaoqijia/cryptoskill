## Description: <br>
AI-powered trading insights suite: prediction markets (Polymarket/Kalshi) and social sentiment signals powered by UnifAI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zbruceli](https://clawhub.ai/user/zbruceli) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and trading analysts use this skill to query prediction markets, compare Polymarket and Kalshi market data, and analyze social sentiment signals for research and trading insight workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an AI broad external tool access for trading-related workflows, which can produce incorrect or overly actionable trading guidance. <br>
Mitigation: Use it for analysis unless live trading controls are explicitly reviewed, add user confirmation and limits before any trading authority, and treat outputs as decision support rather than financial advice. <br>
Risk: API keys, wallets, or accounts with live trading authority could expose financial activity if connected directly. <br>
Mitigation: Use sandbox or read-only API keys where possible and avoid connecting wallets or accounts with live trading authority without additional safeguards. <br>
Risk: The included FastAPI server may expose trading analysis capabilities and configured credentials if published as-is. <br>
Mitigation: Do not expose the server publicly without authentication, network controls, secret handling review, and dependency pinning. <br>


## Reference(s): <br>
- [UnifAI SDK](https://github.com/unifai-network/unifai-sdk-py) <br>
- [LiteLLM Documentation](https://docs.litellm.ai/) <br>
- [Kalshi API Documentation](https://docs.kalshi.com) <br>
- [Polymarket Documentation](https://docs.polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with shell command examples and market analysis summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include market prices, probabilities, volume, sentiment scores, news summaries, and setup guidance that depend on external APIs and configured API keys.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
