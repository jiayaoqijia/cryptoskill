## Description:

How has a wallet's portfolio changed over time? Historical balances, current snapshot, and per-token PnL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to inspect how a blockchain wallet portfolio changed over time, compare historical balances with the current snapshot, and review per-token realized PnL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Nansen API key in the runtime environment.

Mitigation: Keep NANSEN_API_KEY out of logs and shared shells, and run the skill in an isolated or least-privileged environment when stronger containment is needed.

Risk: The skill depends on the npm-distributed Nansen CLI.

Mitigation: Install and run it only when you trust the Nansen CLI package and its supply chain.

## Reference(s):

- [Nansen Portfolio Tracker Skill Page](https://clawhub.ai/nansen-devops/skills/nansen-portfolio-tracker)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the Nansen CLI and requires NANSEN_API_KEY in the runtime environment.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
