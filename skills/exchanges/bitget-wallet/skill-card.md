## Description:

Interact with Bitget Wallet API for crypto market data, token info, swap quotes, and security audits on supported chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[karryzhang](https://clawhub.ai/user/karryzhang)

### License/Terms of Use:

MIT

## Use Case:

External developers and crypto users use this skill to let an agent query Bitget Wallet market and token security data, compare liquidity and rankings, and guide human-confirmed swap or order workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Signed orders and swap submissions can move funds.

Mitigation: Require explicit user confirmation before signing or submitting, and review order amounts, fees, approvals, destination addresses, and EIP-7702 delegation details before execution.

Risk: Raw private-key signing increases loss exposure if the runtime is not trusted.

Mitigation: Prefer external wallet confirmation or a tightly scoped secrets workflow; do not provide a private key unless the environment, dependencies, and requested transaction are fully reviewed.

Risk: Mutable update behavior can replace local skill files with newer code.

Mitigation: Pin a reviewed release where possible and inspect diffs, network endpoints, dependencies, and credential handling before accepting updates.

## Reference(s):

- [Bitget Wallet API Documentation](https://web3.bitget.com/en/docs)
- [Artifact README](artifact/README.md)
- [Artifact Changelog](artifact/CHANGELOG.md)
- [Artifact Compatibility Guide](artifact/COMPATIBILITY.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON, Configuration]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live market data, token security audit results, swap quotes, unsigned transaction or order data, and signed transaction arrays when the signing helper is used.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter version: 2026.3.5-1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
