## Description:

Token deep dive — info, OHLCV, holders, flows, flow intelligence, who bought/sold, DEX trades, PnL, perp trades, perp positions, perp PnL leaderboard. Use when researching a specific token in depth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Crypto analysts, researchers, and developers use this skill to investigate a token's market data, holders, flows, trades, PnL, and perpetual-market activity through Nansen CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A supported x402 payment challenge can spend funds from the configured wallet, and each research call, including calls in a loop, can incur a payment.

Mitigation: Check wallet authorization, payment policy, and spending limits before running research; keep repeated calls within the intended scope.

Risk: Flow intelligence may return all-zero flows for illiquid tokens, and smart-money holder filtering is unsupported for some tokens.

Mitigation: Check the token's liquidity and endpoint support, and treat zero-flow or unavailable-filter results as coverage limits rather than conclusive market signals.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/nansen-devops/skills/nansen-token-research)
- [Nansen CLI browser login platform scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands]

**Output Format:** [CLI research results and analysis in text or Markdown; CSV is available when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results vary by endpoint and selected token, chain, symbol, timeframe, and lookback options.]

## Skill Version(s):

0.1.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
