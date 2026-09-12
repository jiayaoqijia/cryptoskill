## Description:

Tracks Nansen smart-money netflow, DEX trades, holdings, and perpetual trades to help agents investigate what labeled wallets are buying or selling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts, developers, and agent operators use this skill to prepare Nansen CLI smart-money research commands for wallet netflow, spot DEX trades, holdings, and Hyperliquid perpetual trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a third-party Nansen CLI that receives a NANSEN_API_KEY.

Mitigation: Verify the nansen-cli package source, prefer a pinned reviewed version, and use a narrowly scoped API key that can be rotated.

Risk: Generated smart-money research commands can produce incomplete, stale, or misinterpreted market information.

Mitigation: Review commands and Nansen results before using them for trading, research, or operational decisions.

## Reference(s):

- [Nansen Smart Money Tracker ClawHub release](https://clawhub.ai/nansen-devops/skills/nansen-smart-money-tracker)
- [Nansen publisher profile](https://clawhub.ai/user/nansen-devops)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Nansen CLI subcommands, chain and label filters, field selection, table or CSV output options, and NANSEN_API_KEY setup guidance.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
