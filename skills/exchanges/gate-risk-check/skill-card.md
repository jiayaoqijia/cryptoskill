## Description: <br>
Token and address risk assessment for security-focused token, contract, and address queries using Gate-Info MCP data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to generate concise token contract security reports or limited address-risk responses for crypto safety questions. It is intended for security-only queries and routes broader coin research to other Gate skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Gate-Info MCP service or shared runtime-rule files may be misconfigured or untrusted in the local environment. <br>
Mitigation: Install only when the configured Gate-Info MCP service and shared Gate runtime-rule files are trusted. <br>
Risk: Address-risk mode does not provide a full compliance or safety verdict. <br>
Mitigation: Treat address-risk responses as limited basic address information and use manual verification or other checks for compliance decisions. <br>
Risk: Automated token reports can miss risks and should not be read as a guarantee that an asset is safe. <br>
Mitigation: Present risk levels with evidence, preserve critical warnings, and avoid investment-advice or absolute-safety language. <br>


## Reference(s): <br>
- [MCP Execution Specification](references/mcp.md) <br>
- [Scenario Examples](references/scenarios.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/gate-exchange/gate-info-risk-check) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, guidance] <br>
**Output Format:** [Structured Markdown risk assessment report or degradation message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only output based on Gate-Info MCP responses; address-risk mode may provide only basic address information.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
