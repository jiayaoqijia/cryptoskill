## Description:

What are crypto funds and VCs holding right now? Cross-chain fund portfolios and net accumulation signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Crypto researchers and portfolio analysts use this skill to review fund and VC holdings and compare net accumulation across supported chains, including Ethereum and Solana.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A supported HTTP 402 response can trigger a payment from the configured wallet for each research call, including calls repeated in loops.

Mitigation: Confirm wallet authorization, payment policy, and spending limits, and review the number of calls before running research. Do not switch to anonymous access to retry after an authentication failure.

## Reference(s):

- [Browser login platform scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)
- [Nansen Fund Tracker on ClawHub](https://clawhub.ai/nansen-devops/skills/nansen-fund-tracker)

## Skill Output:

**Output Type(s):** [Analysis, Shell commands, Text]

**Output Format:** [Markdown with shell command examples and portfolio metrics returned by the CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Holdings and netflow results depend on available Nansen account access, entitlements, and data.]

## Skill Version(s):

0.1.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
