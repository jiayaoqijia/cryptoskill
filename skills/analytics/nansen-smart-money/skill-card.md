## Description:

Helps agents research smart-money token flows, trades, holdings, and perpetual trades with the Nansen CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and developers use this skill to inspect smart-money wallet activity, including netflows, spot trades, portfolio holdings, and Hyperliquid perpetual trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repeated research calls may consume paid API credits or trigger wallet payments.

Mitigation: Confirm the selected credentials and payment limits before research; avoid broad loops without explicit cost approval.

Risk: An expired or invalid login could lead to unintended anonymous paid access if authentication is bypassed.

Mitigation: Check authentication status and stop on failures; do not switch to anonymous access to retry.

## Reference(s):

- [Nansen Smart Money Tracker on ClawHub](https://clawhub.ai/nansen-devops/skills/nansen-smart-money-tracker)
- [Nansen CLI browser login preview scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides filters for chain, trader label, result limit, sorting, and CSV or table output.]

## Skill Version(s):

0.1.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
