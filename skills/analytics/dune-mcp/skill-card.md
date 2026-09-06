## Description: <br>
Use Dune MCP through UXC for blockchain table discovery, SQL query creation/execution, execution result retrieval, and visualization with help-first schema inspection, explicit auth binding, and guarded credit-consuming operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and blockchain analysts use this skill to discover Dune tables, create and run Dune SQL queries, retrieve execution results, and generate visualizations through the Dune MCP endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Dune API key for authenticated MCP calls. <br>
Mitigation: Use a dedicated or least-privileged Dune API key and remove the UXC credential binding when access is no longer needed. <br>
Risk: Some operations can consume Dune credits or change saved Dune resources. <br>
Mitigation: Review SQL, query IDs, privacy settings, and likely credit usage before approving create, update, execute, or visualization operations. <br>
Risk: Query privacy can change if a private query is made public or a temporary query is visible. <br>
Mitigation: Inspect privacy fields such as is_private and is_temp before changing or sharing query artifacts. <br>


## Reference(s): <br>
- [Usage Patterns](references/usage-patterns.md) <br>
- [Dune MCP endpoint](https://api.dune.com/mcp/v1) <br>
- [ClawHub skill page](https://clawhub.ai/jolestar/dune-mcp-skill) <br>
- [Publisher profile](https://clawhub.ai/user/jolestar) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, SQL examples, and workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Dune MCP command examples, credential binding steps, query IDs, execution IDs, and result-handling guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
