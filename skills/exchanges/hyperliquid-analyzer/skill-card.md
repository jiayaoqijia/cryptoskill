## Description: <br>
Analyze Hyperliquid market data and provide trading insights, including real-time price monitoring, trend analysis, and risk assessment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[B0on](https://clawhub.ai/user/B0on) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and traders use this skill to query Hyperliquid market data, review short-term market conditions, and draft trading insight summaries. It can also help with portfolio-aware analysis when the user provides optional wallet or API credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill queries Hyperliquid over the network for market data. <br>
Mitigation: Use it only in environments where outbound requests to Hyperliquid are acceptable and expected. <br>
Risk: Portfolio or authenticated features may use a wallet address or API key. <br>
Mitigation: Provide only the minimum necessary wallet address or a limited, read-only API key; do not provide private keys or highly privileged credentials. <br>
Risk: Trading guidance can be affected by volatile or stale market data. <br>
Mitigation: Review market context and risk tolerance before acting on generated analysis. <br>


## Reference(s): <br>
- [Hyperliquid API info endpoint](https://api.hyperliquid.xyz/info) <br>
- [Hyperliquid Analyzer on ClawHub](https://clawhub.ai/B0on/hyperliquid-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash commands and market analysis text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include market prices, trend labels, volatility and risk summaries, portfolio observations, and trading guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
