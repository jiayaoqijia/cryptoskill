## Description:

Helps agents assess Hyperliquid perpetual markets using contract volume and open interest, trader leaderboards, and smart-money trades.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and developers use this skill to request Hyperliquid perpetual-market snapshots, compare contracts by volume or open interest, and inspect trader and smart-money activity through the Nansen CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research calls, especially in loops, may consume credits or trigger automatic x402 wallet payments.

Mitigation: Confirm intended usage and wallet authorization and spending limits before running calls; avoid unbounded loops.

Risk: Research requires a selected, working API key or browser session.

Mitigation: Check authentication status before research and stop on failed or uncertain authentication rather than retrying anonymously.

## Reference(s):

- [Nansen Perp Screener on ClawHub](https://clawhub.ai/nansen-devops/skills/nansen-perp-screener)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with Nansen CLI command examples and market-research summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on authenticated Nansen research calls and the selected market filters.]

## Skill Version(s):

0.1.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
