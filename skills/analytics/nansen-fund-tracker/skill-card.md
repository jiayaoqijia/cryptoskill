## Description:

Helps track crypto fund holdings and net accumulation across Ethereum and Solana using Nansen research commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and developers use this skill to compare crypto fund holdings with recent inflows and outflows across Ethereum and Solana.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research calls may consume credits or trigger authorized wallet payments, especially in loops.

Mitigation: Confirm the selected authentication method, wallet payment policy, and spending limits before running commands or loops.

Risk: An anonymous or failed authentication state can lead to unintended access or payment behavior.

Mitigation: Check authentication status before research; stop on anonymous selection, uncertain renewal, or authentication failure rather than retrying anonymously.

## Reference(s):

- [Nansen Fund Tracker on ClawHub](https://clawhub.ai/nansen-devops/skills/nansen-fund-tracker)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fund holdings and netflow comparisons depend on the selected chain and current Nansen data.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
