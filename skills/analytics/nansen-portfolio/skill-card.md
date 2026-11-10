## Description:

How has a wallet's portfolio changed over time? Historical balances, current snapshot, and per-token PnL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and wallet analysts use this skill to review a wallet's historical balances, current holdings, and per-token profit and loss across a selected chain.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research calls can incur x402 payments from the configured wallet, and repeated calls in loops can add charges.

Mitigation: Review payment authorization and spending limits before running calls; bound loops to the intended number of requests.

Risk: The selected API key or browser session provides account API access for research requests.

Mitigation: Use an explicitly selected credential and stop if authentication or session renewal fails; follow the CLI's troubleshooting guidance.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/nansen-devops/skills/nansen-portfolio-tracker)
- [Nansen CLI browser login platform scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)

## Skill Output:

**Output Type(s):** [Analysis, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and structured CLI results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Wallet and chain specific; can include current balances, historical balances, and realized PnL.]

## Skill Version(s):

0.1.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
