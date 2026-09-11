## Description:

Provides agent guidance for paper and live perpetual futures trading on Hyperliquid, including leverage selection, OBV divergence, and auto-stop-loss workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jamierossouw](https://clawhub.ai/user/jamierossouw)

### License/Terms of Use:


## Use Case:

External developers and trading operators use this skill to guide an agent through Hyperliquid perpetual futures automation, including paper/live trading, leverage management, signal-based entries, and stop-loss handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live leveraged crypto futures automation can cause financial loss if an agent places orders or changes leverage without clear consent.

Mitigation: Use paper mode where possible; require explicit confirmation for live orders, leverage changes, and stop-loss changes; apply account and position-size limits.

Risk: The security review notes that paper/live separation and confirmation requirements are not clearly defined.

Mitigation: Document and enforce separate paper and live workflows before deployment, with live trading disabled unless the user explicitly enables it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jamierossouw/skills/hyperliquid-perps)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May steer an agent toward paper or live leveraged trading workflows; require human confirmation before live orders or leverage changes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
