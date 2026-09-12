## Description:

Token deep dive - info, OHLCV, holders, flows, flow intelligence, who bought/sold, DEX trades, PnL, perp trades, perp positions, perp PnL leaderboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to research a specific token through Nansen CLI commands covering market data, holders, wallet flows, DEX trades, PnL, and perpetuals activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the external nansen-cli package and local nansen binary.

Mitigation: Install only from a trusted package source, and pin or review the package before use in sensitive environments.

Risk: The skill requires a Nansen API key for token research commands.

Mitigation: Use a revocable, least-privilege API key and avoid exposing command output that may contain sensitive research context.

Risk: Some token queries may be unsupported or return sparse data, such as smart-money holder filters or all-zero flow intelligence for illiquid tokens.

Mitigation: Treat unsupported filters and sparse flow data as coverage limitations, and corroborate conclusions before acting on results.

## Reference(s):

- [Nansen Token Research on ClawHub](https://clawhub.ai/nansen-devops/skills/nansen-token-research)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CLI flags for table or CSV output where supported by nansen-cli.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
