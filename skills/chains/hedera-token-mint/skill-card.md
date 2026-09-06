## Description: <br>
Create and manage tokens on Hedera (HTS). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HarleysCodes](https://clawhub.ai/user/HarleysCodes) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill to draft Hedera Token Service code and commands for creating fungible tokens, creating NFT collections, minting NFTs, transferring tokens, burning tokens, and configuring token supply and permissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Create, mint, transfer, and burn examples can submit live Hedera transactions that may incur fees or be irreversible. <br>
Mitigation: Use Hedera testnet first, verify the selected network and all account IDs, token IDs, recipients, and amounts, and require explicit human confirmation before execution. <br>
Risk: Private keys and privileged token keys are required for the demonstrated operations. <br>
Mitigation: Keep keys out of prompts, source files, and logs; load credentials from a secure secret store or environment and limit key permissions to the operation being performed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/HarleysCodes/hedera-token-mint) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with TypeScript and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are implementation snippets and operational guidance; users must supply their own Hedera accounts, token IDs, keys, network, amounts, and recipient details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
