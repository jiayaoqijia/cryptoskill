## Description:

Trade on Hyperliquid perp markets across native and HIP-3 venues with quote generation, order routing, split execution, funding and orderbook comparisons, position management, and optional automatic collateral swaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mehranhydary](https://clawhub.ai/user/mehranhydary)

### License/Terms of Use:

MIT

## Use Case:

External developers and trading workflow operators use this skill to inspect Hyperliquid perp market liquidity, compare funding and orderbooks, generate routing quotes, and execute single-market or split-market trades when a wallet is configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an external SDK that is not pinned in the artifact and that may handle private keys and transaction signing.

Mitigation: Review and pin the exact SDK version before installation, start with read-only quote and market-data methods, and use a limited-purpose wallet for any trading tests.

Risk: Trading methods can trigger financial and on-chain actions, including fee approval and collateral-swap behavior.

Mitigation: Prefer quote-then-execute flows, avoid one-step trade methods unless the automatic behavior is acceptable, and disable the builder fee with builder: null when it is not desired.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mehranhydary/skills/hyperliquid-prime)
- [Source Repository](https://github.com/mehranhydary/hl-prime)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with TypeScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe read-only quote workflows, CLI usage, SDK configuration, and wallet-gated trading execution steps.]

## Skill Version(s):

0.1.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
