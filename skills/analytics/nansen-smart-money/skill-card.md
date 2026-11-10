## Description:

Smart money tracking — netflow, trades, holdings, perp trades. Use when finding what smart money wallets are buying/selling or tracking whale activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to query Nansen Smart Money netflows, spot trades, token holdings, and Hyperliquid perpetual trades to inspect wallet activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research calls can incur automatic x402 payments from the configured wallet; repeated calls in loops may multiply charges.

Mitigation: Review wallet authorization and spending limits before research, and bound repeated calls.

## Reference(s):

- [Browser login platform scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)
- [ClawHub skill release](https://clawhub.ai/nansen-devops/skills/nansen-smart-money-tracker)

## Skill Output:

**Output Type(s):** [Analysis, Text, Shell commands]

**Output Format:** [CLI research results as text, tables, or CSV, with shell commands for queries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected chain, labels, filters, and account entitlements.]

## Skill Version(s):

0.1.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
