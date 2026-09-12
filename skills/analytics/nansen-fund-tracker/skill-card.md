## Description:

What are crypto funds and VCs holding right now? Cross-chain fund portfolios and net accumulation signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query Nansen smart-money holdings and netflow data for crypto fund and VC portfolio research across Ethereum and Solana.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Nansen CLI can access NANSEN_API_KEY when the skill runs.

Mitigation: Use a scoped Nansen API key where possible and expose only the minimum environment needed for research queries.

Risk: The release depends on an unpinned nansen-cli package.

Mitigation: Prefer a pinned and reviewed nansen-cli version before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nansen-devops/skills/nansen-fund-tracker)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Configuration]

**Output Format:** [Markdown with bash command examples and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NANSEN_API_KEY and the nansen CLI.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
