## Description:

Guides in-depth token research across prices, holders, flows, trades, PnL, and perpetual markets using Nansen commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and developers use this skill to investigate a specific token's market activity, holders, flows, trades, and PnL through the Nansen CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research calls, especially loops or large queries, can consume credits or trigger configured wallet payments.

Mitigation: Review the payment policy and spending limits before running calls or loops.

Risk: Research requires an authorized API key or browser session, and the installed CLI handles account access.

Mitigation: Check authentication before research and review the nansen-cli package source before installation.

## Reference(s):

- [Nansen Token Research on ClawHub](https://clawhub.ai/nansen-devops/skills/nansen-token-research)
- [nansen-cli package](https://www.npmjs.com/package/nansen-cli)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown]

**Output Format:** [Markdown with Nansen CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI results can be displayed as tables or exported as CSV.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
