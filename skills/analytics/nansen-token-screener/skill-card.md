## Description:

Discover trending tokens — screener, SM holdings, Nansen indicators, and flow intelligence for promising finds. Use when scanning for new tokens or screening what's hot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Crypto researchers and developers use this skill to screen tokens, review smart money holdings and Nansen indicators, and inspect token flows when deciding which assets merit further research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial because two local paths referenced by the skill were not included in the scan.

Mitigation: Check whether the omitted local paths affect your use before installing.

Risk: Research calls can incur x402 payments from the configured wallet, including calls made in loops.

Mitigation: Review wallet authorization, payment policy, and spending limits before running calls; keep flow intelligence to promising candidates.

Risk: Token scores and market indicators can be mistaken for investment recommendations, and some indicator data may be missing or stale.

Mitigation: Use scores as screening signals, inspect individual indicators and their dates, and verify candidates independently before making financial decisions.

## Reference(s):

- [Nansen CLI browser login platform scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)
- [Nansen Token Screener on ClawHub](https://clawhub.ai/nansen-devops/skills/nansen-token-screener)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and structured research results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on selected chain, timeframe, filters, account entitlements, and available indicator data.]

## Skill Version(s):

0.1.5 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
