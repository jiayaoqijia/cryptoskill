## Description:

Analyzes token holder quality through smart-money holdings, labeled wallet flows, and recent buyer and seller activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Token researchers and analysts use this skill to assess holder quality, compare labeled wallet flows, and review recent buyers and sellers for a token contract.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research calls may consume credits or trigger authorized wallet payments, especially in loops.

Mitigation: Confirm account credentials and wallet spending limits before running research commands or loops.

Risk: Anonymous access or failed authentication may interrupt the intended research workflow.

Mitigation: Check authentication status first and stop on invalid or failed authentication rather than retrying anonymously.

## Reference(s):

- [Nansen Holder Analysis on ClawHub](https://clawhub.ai/nansen-devops/skills/nansen-holder-analysis)

## Skill Output:

**Output Type(s):** [Analysis, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a token contract address and chain; the holders endpoint excludes native and wrapped tokens.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
