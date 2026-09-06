## Description: <br>
Query real-time crypto wallet portfolios, transactions, DeFi positions, token prices, NFTs, and gas fees across EVM chains and Solana via Zerion's MCP API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abishekdharshan](https://clawhub.ai/user/abishekdharshan) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and analysts use this skill to configure Zerion's MCP server and ask an agent to retrieve read-only wallet, transaction, DeFi, NFT, token price, and gas-fee information across supported chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet addresses, token and NFT lookups, portfolio questions, and related query patterns may reveal sensitive financial activity when sent to Zerion's remote service. <br>
Mitigation: Use the skill only for wallets you are authorized to analyze, avoid personally identifying or sensitive wallets unless necessary, and review Zerion API usage before sharing query data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/abishekdharshan/skills/zerion-api) <br>
- [Zerion API Documentation](https://developers.zerion.io) <br>
- [Zerion AI and MCP Documentation](https://developers.zerion.io/reference/building-with-ai) <br>
- [Zerion llms.txt](https://developers.zerion.io/llms.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and natural-language query prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Zerion API key and a compatible MCP client; wallet queries are sent to Zerion's remote service.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
