## Description: <br>
API reference for CoinMarketCap DEX endpoints including token lookup, pools, transactions, trending, and security analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bryan-cmc](https://clawhub.ai/user/bryan-cmc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to choose CoinMarketCap DEX API endpoints, parameters, and example calls for on-chain token lookup, price retrieval, liquidity analysis, discovery, transactions, and token security checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys may be exposed if users paste credentials directly into generated curl commands or shared logs. <br>
Mitigation: Use an environment variable or secret manager for the CoinMarketCap API key and review commands before running or sharing them. <br>
Risk: Token security, trending, and liquidity data can be misread as trading advice. <br>
Mitigation: Treat API results as informational signals and apply independent due diligence before trading decisions. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/bryan-cmc/cmc-api-onchain-data) <br>
- [Common Use Cases](artifact/references/use-cases.md) <br>
- [DEX Token APIs](artifact/references/tokens.md) <br>
- [DEX Pairs APIs](artifact/references/pairs.md) <br>
- [DEX Platform APIs](artifact/references/platforms.md) <br>
- [DEX Discovery APIs](artifact/references/discovery.md) <br>
- [DEX Security API](artifact/references/security.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, code] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include CoinMarketCap DEX endpoint paths, request parameters, curl examples, response field summaries, and API-key handling guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
