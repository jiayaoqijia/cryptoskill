## Description:

Scans DeFi protocols for yield opportunities, compares APY against risk and sustainability signals, tracks TVL changes, and flags new farming opportunities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jamierossouw](https://clawhub.ai/user/jamierossouw)

### License/Terms of Use:


## Use Case:

External users and developers can use this skill to compare DeFi yield opportunities across protocols such as Aave, Compound, Curve, Uniswap v3, and Yearn. It is intended for informational yield research and should not replace independent financial, tax, liquidity, or smart-contract risk review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Yield rankings can become stale or incomplete because APY, TVL, liquidity, fees, and protocol incentives change frequently.

Mitigation: Independently verify current APY, liquidity, smart-contract risk, fees, and tax implications before acting on any opportunity.

Risk: Entry instructions may be misread as authorization to connect wallets or move funds.

Mitigation: Treat the skill output as informational research only and do not connect wallets or transfer funds unless you explicitly decide to do so outside the skill.

## Reference(s):

- [DeFiLlama API](https://api.llama.fi)
- [Curve API](https://curve.fi/api)
- [Yearn API](https://yearn.fi/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown table with concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ranks DeFi opportunities by APY, risk, sustainability, gas efficiency, TVL, and recommendation signal.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
