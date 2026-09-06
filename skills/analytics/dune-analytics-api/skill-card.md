## Description: <br>
Dune Analytics API helps agents query, analyze, optimize, and upload blockchain data using the Dune API and DuneSQL references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LZ-Web3](https://clawhub.ai/user/LZ-Web3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to run Dune queries, inspect blockchain table schemas, optimize DuneSQL, analyze wallet and DEX activity, and upload CSV or NDJSON datasets with a DUNE_API_KEY. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Use of DUNE_API_KEY can run queries, consume Dune credits, and access account-scoped Dune resources. <br>
Mitigation: Confirm credit-consuming executions when appropriate, reuse cached results or existing queries when possible, and report execution or credit metadata back to the user. <br>
Risk: Saved-query updates, public query creation, CSV overwrites, table clears, deletes, and uploads can create persistent remote changes. <br>
Mitigation: Require explicit user confirmation before these actions, prefer private Dune resources by default, and prefer append-style uploads for important datasets. <br>
Risk: Uploading local CSV or NDJSON files may expose sensitive data to Dune. <br>
Mitigation: Confirm the file path, intended table, privacy setting, and data sensitivity before upload. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/LZ-Web3/dune-analytics-api) <br>
- [Dune Analytics](https://dune.com) <br>
- [Dune API key settings](https://dune.com/settings/api) <br>
- [Table Discovery](references/table-discovery.md) <br>
- [Query Execution](references/query-execution.md) <br>
- [Common Tables](references/common-tables.md) <br>
- [SQL Optimization](references/sql-optimization.md) <br>
- [Wallet Analysis](references/wallet-analysis.md) <br>
- [Data Upload](references/data-upload.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, JSON, CSV, table-formatted text, SQL, Python snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, dune-client, and DUNE_API_KEY for live Dune API operations.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
