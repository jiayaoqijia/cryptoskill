## Description:

Performs read-only token contract security checks and limited address risk assessment with structured risk reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check token or contract security signals such as honeypot status, tax risk, holder concentration, name risk, and open-source status. Address safety requests are handled in degraded mode with basic on-chain address information only.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated token and contract risk signals may be mistaken for investment advice or a guarantee of safety.

Mitigation: Present findings as automated risk signals, include no-investment-advice and no-absolute-safety language, and recommend manual due diligence.

Risk: Address-risk mode is limited and may not provide complete blacklist, compliance, or risk screening.

Mitigation: Clearly disclose degraded address compliance detection and limit output to available basic on-chain address information.

Risk: Missing chain, unsupported tokens, or unavailable tool data can produce incomplete reports.

Mitigation: Require the chain before token checks, ask for clarification when inputs are incomplete, and mark unavailable report sections instead of fabricating conclusions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gate-exchange/skills/gate-info-risk-check)
- [Gate Info RiskCheck MCP Specification](references/mcp.md)
- [Scenarios and Prompt Examples](references/scenarios.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown structured risk report or concise degradation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only Gate Info MCP lookups; token mode requires a chain; address compliance checks are currently limited.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
