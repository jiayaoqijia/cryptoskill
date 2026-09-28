## Description:

Search for tokens or entities by name to find token addresses or matching entities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their users search Nansen for tokens and entities by name, including finding a token's full address or narrowing results by chain.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search calls can consume credits or trigger configured wallet payments, particularly when repeated in loops.

Mitigation: Confirm the selected API key or session, wallet authorization, payment policy, and spending limits before searching or running loops.

## Reference(s):

- [Nansen General Search on ClawHub](https://clawhub.ai/nansen-devops/skills/nansen-general-search)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Text and Markdown with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Token and entity name searches support optional chain, result limit, and selected fields.]

## Skill Version(s):

0.1.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
