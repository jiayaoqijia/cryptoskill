## Description: <br>
Interact with Alchemy's Web3 APIs for blockchain data, NFTs, tokens, transfers, and webhooks across 80+ chains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gizmo-dev](https://clawhub.ai/user/gizmo-dev) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and AI agents use this skill to query wallet balances, token and NFT data, transaction history, blocks, gas prices, ENS names, and webhook-oriented Alchemy workflows across supported chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an Alchemy API key and can expose wallet-monitoring data in command output. <br>
Mitigation: Protect ALCHEMY_API_KEY, avoid logging secrets, and treat wallet balances, transfers, and monitoring results as sensitive. <br>
Risk: Agent workflows could be extended toward trading, bidding, wallet signing, or transaction broadcasting. <br>
Mitigation: Require explicit human confirmation, simulation, and spending limits before connecting this skill to transaction-producing actions. <br>
Risk: Unrecognized chain names or unsupported endpoints can produce misleading or failed blockchain queries. <br>
Mitigation: Use known Alchemy chain identifiers and validate responses before acting on returned data. <br>


## Reference(s): <br>
- [Alchemy Web3 ClawHub Page](https://clawhub.ai/gizmo-dev/alchemy-web3) <br>
- [Alchemy Docs](https://www.alchemy.com/docs) <br>
- [Alchemy Supported Chains](https://www.alchemy.com/docs/chains) <br>
- [Alchemy Dashboard](https://dashboard.alchemy.com) <br>
- [Alchemy SDK](https://github.com/alchemyplatform/alchemy-sdk-js) <br>
- [AI Agent Workflows](references/agent-workflows.md) <br>
- [NFT API Reference](references/nft-api.md) <br>
- [Token API Reference](references/token-api.md) <br>
- [Node API Reference](references/node-api.md) <br>
- [Supported Chains Reference](references/chains.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell, curl, JavaScript, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ALCHEMY_API_KEY; commands can return human-readable text or raw JSON.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter lists 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
