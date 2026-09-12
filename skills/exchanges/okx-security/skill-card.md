## Description:

Okx Security helps agents run OKX Onchain OS checks for token risk, DApp phishing, transaction and signature safety, and token approval review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ok-james-01](https://clawhub.ai/user/ok-james-01)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent prepare and run OKX Onchain OS security checks before interacting with tokens, DApps, transactions, signatures, or token approvals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install or update a local OKX onchainos CLI from a changing remote release.

Mitigation: Install only if the OKX release process is trusted, and verify installer and binary checksums before running commands.

Risk: Some scan-failure paths may allow a user to proceed without completed security results.

Mitigation: Report failed scans clearly, ask whether to retry or proceed, and warn that the operation has not been verified.

Risk: Approval revocation, transaction, signing, broadcast, and swap workflows can affect wallet assets.

Mitigation: Require explicit user review before any wallet signing, broadcast, approval, revoke, or swap action.

## Reference(s):

- [OKX Web3](https://web3.okx.com)
- [OKX Developer Portal](https://web3.okx.com/onchain-os/dev-portal)
- [Risk Token Detection](references/risk-token-detection.md)
- [Risk Domain Detection](references/risk-domain-detection.md)
- [Risk Transaction Detection](references/risk-transaction-detection.md)
- [Risk Approval Monitoring](references/risk-approval-monitoring.md)

## Skill Output:

**Output Type(s):** [Analysis, Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with inline shell commands and security findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May query wallet and portfolio data, guide approval revocation or transaction workflows, and requires explicit review before wallet signing, broadcast, approval, or swap actions.]

## Skill Version(s):

3.1.3 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
