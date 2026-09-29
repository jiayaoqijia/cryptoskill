## Description:

How has a wallet's portfolio changed over time? Historical balances, current snapshot, and per-token PnL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Wallet analysts and developers use Nansen CLI to compare historical token balances with a current wallet snapshot and review per-token trading performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research calls and loops can consume Nansen credits or trigger authorized x402 wallet payments.

Mitigation: Review account entitlements, wallet authorization, payment policy, and spending limits before running calls; limit the number of calls.

Risk: An untrusted CLI package or unverified authentication may expose credentials or lead to unintended access.

Mitigation: Trust the Nansen CLI package before installing it, select an authorized API key or browser session, and check authentication status before research.

## Reference(s):

- [Nansen Portfolio Tracker on ClawHub](https://clawhub.ai/nansen-devops/skills/nansen-portfolio-tracker)
- [Nansen CLI browser login preview scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with bash commands and portfolio analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Historical balances, current holdings, and per-token PnL depend on the selected wallet, chain, and time window.]

## Skill Version(s):

0.1.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
