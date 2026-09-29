## Description:

Helps agents research tokens through Nansen data on prices, holders, flows, trades, PnL, and perpetual positions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to investigate a specific token's market activity, holders, wallet flows, trades, and profit and loss using Nansen research commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the Nansen CLI package introduces third-party executable code.

Mitigation: Confirm you trust the Nansen CLI package before installation.

Risk: Authenticated research calls, especially in loops, can consume credits or trigger x402 wallet payments.

Mitigation: Check wallet authorization, payment policy, spending limits, and expected call volume before running research.

## Reference(s):

- [Nansen Token Research on ClawHub](https://clawhub.ai/nansen-devops/skills/nansen-token-research)
- [Nansen CLI browser-login platform scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands]

**Output Format:** [Text or Markdown research findings with Nansen CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Research calls require selected authentication and may consume credits or trigger wallet payments.]

## Skill Version(s):

0.1.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
