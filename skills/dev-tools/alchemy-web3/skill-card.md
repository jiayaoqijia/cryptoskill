## Description:

Interact with Alchemy's Web3 APIs for blockchain data, NFTs, tokens, transfers, and webhooks across 80+ chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gizmo-dev](https://clawhub.ai/user/gizmo-dev)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to query Alchemy blockchain APIs for wallet balances, token holdings, NFT metadata, transaction history, gas data, chain references, and monitoring workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Alchemy receives queried blockchain identifiers such as wallet addresses, transaction hashes, contract addresses, and chain selections.

Mitigation: Use the skill only for identifiers you are comfortable sending to Alchemy, and avoid querying sensitive or private wallet activity without authorization.

Risk: The CLI sources a shared ~/.openclaw/.env file before making API requests.

Mitigation: Prefer injecting ALCHEMY_API_KEY through a controlled process environment and review any shared .env file before use.

Risk: Agent workflow examples describe persistent monitoring and potential financial actions.

Mitigation: Require explicit human approval and strict limits before enabling transaction, auto-bid, trade, alerting, or automated action workflows.

Risk: Unrestricted chain selection can route requests to unexpected Alchemy endpoints.

Mitigation: Restrict ALCHEMY_CHAIN and --chain values to known Alchemy chain IDs needed for the deployment.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/gizmo-dev/skills/alchemy-web3)
- [Alchemy documentation](https://www.alchemy.com/docs)
- [Alchemy chains documentation](https://www.alchemy.com/docs/chains)
- [Alchemy SDK](https://github.com/alchemyplatform/alchemy-sdk-js)
- [AI Agent Workflows](references/agent-workflows.md)
- [Supported Chains Reference](references/chains.md)
- [NFT API Reference](references/nft-api.md)
- [Node API Reference](references/node-api.md)
- [Token API Reference](references/token-api.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, curl examples, JSON payloads, and JavaScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ALCHEMY_API_KEY; CLI commands can emit raw JSON with --raw.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter lists 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
