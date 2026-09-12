## Description:

What is the state of the Hyperliquid perp market? Top contracts by volume/OI, trader leaderboard, and SM perp activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market analysts use this skill to query Nansen's CLI for Hyperliquid perpetual market activity, including contract volume/open interest, trader leaderboard performance, and smart money perp trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a NANSEN_API_KEY and invokes the Nansen CLI.

Mitigation: Run it in an isolated environment with only the required key available.

Risk: The installed nansen-cli package controls the executed market-query behavior.

Mitigation: Install only from a trusted package source and consider pinning or reviewing the nansen-cli version before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nansen-devops/skills/nansen-perp-screener)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and tabular market-query outputs from the Nansen CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the nansen CLI and NANSEN_API_KEY.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
