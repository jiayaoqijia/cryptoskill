## Description: <br>
Gate Exchange Assets helps agents query read-only Gate account balances and asset holdings across total, account-specific, and currency-specific scopes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve read-only Gate asset overviews, account balances, coin holdings, and account-book details through a configured Gate MCP session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive Gate exchange API credentials and wallet-related account access. <br>
Mitigation: Use a dedicated Gate API key with only the documented read permissions and no withdrawal permission. <br>
Risk: Broad balance-query routing could answer unintended account-balance requests. <br>
Mitigation: Phrase requests with explicit Gate context and account scope before allowing the skill to query balances. <br>
Risk: Partial MCP failures or missing modules can produce incomplete asset views. <br>
Mitigation: Return degraded output that marks missing modules explicitly and do not infer unavailable balances. <br>


## Reference(s): <br>
- [Gate Assets MCP Specification](references/mcp.md) <br>
- [Gate Exchange Assets Runtime Rules](references/gate-runtime-rules.md) <br>
- [Gate Skills Homepage](https://github.com/gate/gate-skills) <br>
- [Gate API Key Management](https://www.gate.com/myaccount/profile/api-key/manage) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown balance summaries with account distribution, valuation notes, and degraded-data markers when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only account data is reported from configured Gate access; unavailable modules are marked rather than inferred.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
