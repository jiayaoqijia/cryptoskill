## Description: <br>
Connect to a user's investment accounts via SnapTrade SDK to generate portfolio reports, manage brokerage connections, and place or monitor brokerage orders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brendanwood](https://clawhub.ai/user/brendanwood) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to connect SnapTrade-supported brokerage accounts, retrieve account and portfolio totals, generate connection or reconnect links, and place or monitor buy/sell orders when explicitly requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store brokerage API credentials and user secrets. <br>
Mitigation: Protect the snaptrade.json secret file, keep permissions restrictive, and avoid sharing generated reports or configuration contents. <br>
Risk: The skill can place real buy and sell orders through connected brokerage accounts. <br>
Mitigation: Require explicit approval of the exact account, symbol, side, quantity, order type, price, and time-in-force before running order scripts. <br>
Risk: Scheduled or forwarded portfolio reports can expose sensitive financial data. <br>
Mitigation: Enable cron or messaging delivery only after verifying the destination, message contents, and disable procedure. <br>


## Reference(s): <br>
- [SnapTrade API Reference](https://docs.snaptrade.com/reference) <br>
- [SnapTrade Getting Started](https://docs.snaptrade.com/docs/getting-started) <br>
- [Connection Portal Integration](https://docs.snaptrade.com/docs/implement-connection-portal) <br>
- [SnapTrade Webhooks](https://docs.snaptrade.com/docs/webhooks) <br>
- [api-reference.md](references/api-reference.md) <br>
- [getting-started.md](references/getting-started.md) <br>
- [connection-portal.md](references/connection-portal.md) <br>
- [webhooks.md](references/webhooks.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce SnapTrade portal links, account summaries, portfolio total JSON, per-broker total JSON, and order status updates.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
