## Description:

Analyze Uniswap pool data including liquidity distribution, fee tiers, tick ranges, and TVL for on-chain pool state questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

Developers, analysts, and DeFi operators use this skill to inspect Uniswap v3/v4 pool structure, liquidity distribution, fee tiers, tick ranges, TVL, and on-chain state for LP or trading analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable installer commands or unpinned revisions can install a different skill or dependency version than the reviewed release.

Mitigation: Pin the ClawHub or npm installer version and review the exact skill revision before use, especially in wallet, trading, or production analytics environments.

Risk: Pool analysis can inform LP or trading decisions and may be misleading if RPC data, pool addresses, token decimals, or chain configuration are wrong.

Mitigation: Verify pool addresses, chain IDs, RPC endpoints, token decimals, and computed metrics against trusted sources before acting on analysis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wpank/skills/uniswap-pool-analysis)
- [Skill specification](artifact/SKILL.md)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [analysis, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with TypeScript examples and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include on-chain query guidance, pool metric interpretation, price and tick conversion logic, and multi-chain RPC configuration guidance.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
