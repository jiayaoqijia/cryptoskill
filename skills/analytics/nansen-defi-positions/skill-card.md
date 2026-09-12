## Description:

What DeFi positions does a wallet hold? Protocol-by-protocol breakdown of assets, debts, and rewards across chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users use this skill to inspect a wallet's DeFi positions across protocols and chains, including assets, debts, rewards, and related spot balances.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires installing and running the nansen-cli package.

Mitigation: Confirm the package source is trusted before installation and pin the CLI version for reproducible deployments.

Risk: The skill requires a NANSEN_API_KEY.

Mitigation: Use an API key with the least access needed and manage it as a secret.

Risk: A wallet may have no tracked DeFi positions or incomplete DeFi coverage.

Mitigation: Treat empty DeFi responses as no tracked positions for that query and combine DeFi results with spot balance checks as the skill instructs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nansen-devops/skills/nansen-defi-positions)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with Nansen CLI shell commands and tabular result descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NANSEN_API_KEY and the nansen CLI; DeFi position queries may return empty results for wallets with no tracked positions.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
