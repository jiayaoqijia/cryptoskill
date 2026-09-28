## Description:

Helps track a wallet's portfolio over time using historical balances, current holdings, and per-token profit and loss.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Wallet holders and analysts use this skill to compare historical and current token balances and review per-token trading performance through Nansen.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research calls may consume API credits or trigger x402 payments, particularly in loops.

Mitigation: Confirm account entitlements and existing wallet authorization, payment policy, and spending limits before running calls.

Risk: Research requires access to a Nansen API key or browser session.

Mitigation: Check authentication status, use an explicitly selected credential, and stop on authentication failure rather than retrying anonymously.

## Reference(s):

- [Nansen Portfolio Tracker on ClawHub](https://clawhub.ai/nansen-devops/skills/nansen-portfolio-tracker)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with shell commands and portfolio analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected wallet, chain, time window, and account access.]

## Skill Version(s):

0.1.1 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
