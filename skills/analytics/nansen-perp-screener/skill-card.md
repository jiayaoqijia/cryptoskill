## Description:

Screens Hyperliquid perpetual futures for leading contracts, trader rankings, and smart-money activity using Nansen CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Traders and market researchers use the skill to inspect Hyperliquid perpetual-futures volume, open interest, trader leaderboards, and smart-money trades with Nansen CLI filters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research requests and loops may consume credits or trigger authorized x402 wallet payments.

Mitigation: Check account entitlements, wallet authorization, payment policy, and spending limits before running calls, especially loops.

Risk: API keys and saved browser sessions grant access to Nansen account research.

Mitigation: Use an explicitly selected credential, check authentication status, and stop on authentication failure rather than switching to anonymous paid access.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/nansen-devops/skills/nansen-perp-screener)
- [Nansen CLI browser login preview scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with Nansen CLI commands and market summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on live Nansen market data and selected filters.]

## Skill Version(s):

0.1.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
