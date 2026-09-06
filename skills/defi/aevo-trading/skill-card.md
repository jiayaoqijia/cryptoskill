## Description: <br>
AI trading assistant skill for AEVO, a decentralized derivatives exchange, connecting MCP-compatible clients to market data, portfolio management, order execution, risk analysis, and options strategies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yichulau](https://clawhub.ai/user/yichulau) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect MCP-compatible clients to AEVO for crypto derivatives market analysis, portfolio risk review, and user-confirmed order, cancellation, leverage, and strategy workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can connect an agent to AEVO trading credentials and real order execution. <br>
Mitigation: Use testnet or read-only credentials first, verify the MCP server or hosted endpoint, and review every order, cancellation, leverage change, and strategy execution before confirming. <br>
Risk: Private API, signing, or wallet credentials may be exposed if mishandled during setup or responses. <br>
Mitigation: Avoid wallet private keys unless necessary, clear credentials after use, and redact any private keys or secrets from user-visible output. <br>
Risk: Leveraged derivatives and options workflows can create liquidation, slippage, concentration, or partial-execution risk. <br>
Mitigation: Run pre-trade risk checks, inspect margin and liquidity, use stop-losses for leveraged positions, and report partial strategy failures with manual cleanup steps. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yichulau/aevo-trading-skill) <br>
- [AEVO Exchange](https://aevo.xyz) <br>
- [AEVO API Docs](https://docs.aevo.xyz) <br>
- [MCP Server Package](https://pypi.org/project/mcp-aevo-server/) <br>
- [Risk Rules](references/risk-rules.md) <br>
- [Tool Reference](references/tools.md) <br>
- [Workflows](references/workflows.md) <br>
- [Options Reference](references/options.md) <br>
- [Instrument Naming](references/instruments.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and plain text with inline tool names, command snippets, JSON configuration, and quantitative trading analysis.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include trade plans, risk summaries, order details, credential setup guidance, and confirmation prompts before trading actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
