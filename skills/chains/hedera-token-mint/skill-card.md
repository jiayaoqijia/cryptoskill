## Description:

Create and manage tokens on Hedera (HTS), including fungible token minting, NFT collection creation, token supply setup, and token permission configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harleyscodes](https://clawhub.ai/user/harleyscodes)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to draft Hedera Token Service token-management workflows for creating fungible tokens and NFT collections, minting NFTs, configuring supply and token keys, transferring tokens, and burning tokens.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Transfer and burn examples can execute high-impact token operations against real Hedera accounts if used with production credentials.

Mitigation: Run workflows on testnet first, require explicit user confirmation before execution, and verify token IDs, account IDs, amounts, and signing keys before submitting transactions.

Risk: Unpinned Hedera SDK installation can change behavior as dependencies update.

Mitigation: Pin the @hashgraph/sdk version and review SDK release notes before using the examples with real assets.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with TypeScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples use the Hedera JavaScript SDK and require user-provided account IDs, token IDs, keys, and client configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
