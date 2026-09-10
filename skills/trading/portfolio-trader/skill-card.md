## Description:

Connects to a user's investment accounts through the SnapTrade SDK to support brokerage connections, portfolio reporting, account workflows, and order operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brendanwood](https://clawhub.ai/user/brendanwood)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to connect brokerage accounts through SnapTrade, retrieve portfolio totals, inspect accounts and brokerages, and perform order-related workflows when live trading is intentionally enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes live brokerage trading capability that could create unintended financial transactions.

Mitigation: Install only when trading access is intended; remove or disable order scripts unless needed, and require explicit user confirmation plus checked-order previews before any trade.

Risk: The skill handles brokerage credentials, account data, and financial reports that are sensitive.

Mitigation: Protect the SnapTrade configuration file, restrict access to generated reports, and avoid forwarding financial summaries through messaging channels unless the privacy exposure is accepted.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/brendanwood/skills/portfolio-trader)
- [SnapTrade API Reference](https://docs.snaptrade.com/reference)
- [SnapTrade Getting Started](https://docs.snaptrade.com/docs/getting-started)
- [Connection Portal Integration](https://docs.snaptrade.com/docs/implement-connection-portal)
- [SnapTrade Webhooks](https://docs.snaptrade.com/docs/webhooks)
- [API Reference Summary](references/api-reference.md)
- [Connection Portal Summary](references/connection-portal.md)
- [Getting Started Summary](references/getting-started.md)
- [Webhooks Summary](references/webhooks.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local command workflows and JSON-style portfolio or order status outputs; requires SnapTrade credentials configured outside the skill files.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
