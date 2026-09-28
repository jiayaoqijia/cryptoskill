## Description:

Shows a wallet's DeFi positions by protocol and chain, including assets, debts, and rewards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Wallet researchers and analysts use this skill to review DeFi positions alongside spot balances across supported chains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Nansen account access may use an API key or browser session, and commands outside the shown read-only queries may have different effects.

Mitigation: Use only the Nansen permissions needed and review any additional command before running it.

Risk: An empty DeFi portfolio result may reflect no tracked positions rather than a complete view of wallet exposure.

Mitigation: Check spot balances and account for the tool's position coverage when interpreting results.

## Reference(s):

- [Nansen DeFi Positions on ClawHub](https://clawhub.ai/nansen-devops/skills/nansen-defi-positions)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Portfolio queries may be empty when no tracked DeFi positions are found.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
