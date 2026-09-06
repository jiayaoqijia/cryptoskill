## Description: <br>
Analyze Uniswap pool data including liquidity distribution, fee tiers, tick ranges, TVL, and on-chain pool state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and DeFi operators use this skill to inspect Uniswap v3/v4 pool structure, query read-only pool state, and reason about liquidity distribution, fee tiers, tick ranges, and TVL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: On-chain analysis may require an Ethereum RPC endpoint or API key. <br>
Mitigation: Use a dedicated read-only endpoint or API key that is appropriate for these queries, and avoid exposing credentials unnecessarily. <br>
Risk: Pool analysis can be misleading if the chain, pool address, or RPC data is incorrect. <br>
Mitigation: Confirm the chainId, pool address, and important results against trusted sources before using the analysis for operational decisions. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with TypeScript and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference read-only on-chain RPC queries and chain configuration.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
