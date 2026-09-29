## Description:

Tracks crypto fund and venture capital holdings across Ethereum and Solana and compares their net accumulation signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Crypto researchers and investors use this skill to compare fund token holdings and net flows across Ethereum and Solana.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research calls, including repeated calls, may consume credits or trigger authorized wallet payments.

Mitigation: Review credits, wallet authorization, and spending limits before running research commands or loops.

Risk: A missing or failed account session may prevent research calls.

Mitigation: Select an API key or saved browser session, check authentication status, and stop if authentication fails rather than switching to anonymous paid access.

## Reference(s):

- [Nansen Fund Tracker on ClawHub](https://clawhub.ai/nansen-devops/skills/nansen-fund-tracker)
- [Nansen CLI browser login preview scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with bash commands and fund holdings and net-flow analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Nansen CLI research results for Ethereum and Solana; results depend on current account access and available data.]

## Skill Version(s):

0.1.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
