## Description:

Token deep dive — info, OHLCV, holders, flows, flow intelligence, who bought/sold, DEX trades, PnL, perp trades, perp positions, perp PnL leaderboard. Use when researching a specific token in depth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to research a specific crypto token by examining its market data, holders, wallet flows, DEX trades, profit and loss, and perpetual futures activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research calls can trigger x402 payments from the configured wallet, and calls in loops can each incur a payment.

Mitigation: Check wallet authorization, payment policy, and spending limits before running calls or loops; use anonymous x402 only with explicit user intent and payment setup.

Risk: API keys and browser sessions provide account access, and authentication renewal can fail.

Mitigation: Use an explicitly selected key or saved session, check `nansen auth status` before research, protect credentials, and stop if authentication or renewal fails.

## Reference(s):

- [Nansen CLI browser login platform scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)
- [ClawHub skill release](https://clawhub.ai/nansen-devops/skills/nansen-token-research)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Shell commands]

**Output Format:** [Markdown research summaries and shell command examples; CLI results may be presented as tables or CSV.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Research is scoped to the selected token and chain; perpetual futures queries use a symbol.]

## Skill Version(s):

0.1.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
