## Description: <br>
Build and sign XRP Ledger transactions, including payments, NFT mint or burn transactions, Xaman-signed submission, and direct XRPL submission. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HarleysCodes](https://clawhub.ai/user/HarleysCodes) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers building XRP Ledger integrations use this skill to draft transaction objects, prepare Xaman-signed submissions, and reference common XRPL transaction fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Signed XRP Ledger transactions can affect real funds or account state. <br>
Mitigation: Verify destination, amount, destination tag, transaction type, NFT fields, issuer, flags, fees, and network before signing or submitting. <br>
Risk: Experimenting against a mainnet endpoint can submit irreversible ledger actions. <br>
Mitigation: Use XRPL testnet or devnet examples while experimenting, then switch networks only after reviewing the finalized transaction. <br>
Risk: Unpinned dependencies can change transaction-building behavior in downstream projects. <br>
Mitigation: Pin the xrpl npm dependency in production projects and review dependency updates before release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/HarleysCodes/xrpl-tx-builder) <br>
- [Publisher profile](https://clawhub.ai/user/HarleysCodes) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with TypeScript examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
