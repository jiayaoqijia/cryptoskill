## Description:

Gate Exchange market analysis tool for liquidity, slippage, funding arbitrage, basis, momentum, liquidation monitoring, manipulation risk, and related spot or futures market reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to request read-only Gate market analysis across liquidity, momentum, liquidation, arbitrage, basis, manipulation risk, slippage, K-line, and portfolio-allocation scenarios. It produces structured data-based reports and explicitly separates analysis from investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on mutable remote runtime rules from GitHub master.

Mitigation: Review the referenced rules before installation and prefer a release that bundles or pins the runtime rules.

Risk: The skill can produce trading, portfolio, and market-direction guidance that users may misread as personalized financial advice.

Mitigation: Treat outputs as market information only, keep the read-only boundary, and retain the not-investment-advice disclaimer.

Risk: Weak credential guidance could lead users to paste keys into chat or over-permission an MCP configuration.

Mitigation: Configure credentials only through secure MCP server settings, avoid pasting secrets into chat, and use least-privilege read-only credentials when credentials are required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gate-exchange/skills/gate-exchange-market-analysis)
- [Gate](https://www.gate.com)
- [Gate MCP Setup](https://github.com/gateio/gate-mcp)
- [MCP Execution Specification](artifact/references/mcp.md)
- [Scenario and Call Specifications](artifact/references/scenarios.md)
- [Gate Runtime Rules Referenced by Artifact](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown structured market-analysis reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only analysis; requires Gate MCP market-data tools and explicit pair or contract inputs for scenario-specific reports.]

## Skill Version(s):

1.0.2 (source: server release metadata; source frontmatter reports 2026.3.23-1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
