## Description:

Dune Analytics API helps agents query, analyze, optimize, and upload blockchain data through Dune using reference guidance and helper scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lz-web3](https://clawhub.ai/user/lz-web3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to discover Dune tables, run or inspect saved queries, write DuneSQL for EVM and Solana analytics, track Dune credits, and upload CSV or NDJSON data for analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run credit-consuming Dune operations.

Mitigation: Confirm query execution, performance tier, and expected scan scope before running live Dune calls, and report credits consumed when available.

Risk: The skill can update saved query SQL, upload data, clear tables, delete tables, or create public queries.

Mitigation: Require explicit user review before account-changing actions, prefer private queries and tables, and avoid public creation unless the user accepts that fallback.

Risk: The skill requires access to a Dune API key.

Mitigation: Use a scoped DUNE_API_KEY in an isolated environment and avoid exposing the key in prompts, logs, generated SQL, or shared artifacts.

Risk: Unpinned dependencies can change behavior over time.

Mitigation: Pin dune-client in production environments and review dependency changes before upgrading.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lz-web3/skills/dune-analytics-api)
- [Dune Analytics](https://dune.com)
- [Dune API Key Settings](https://dune.com/settings/api)
- [Table Discovery](references/table-discovery.md)
- [Query Execution Patterns](references/query-execution.md)
- [Dune Common Tables Reference](references/common-tables.md)
- [SQL Optimization Patterns for Dune](references/sql-optimization.md)
- [Wallet Analysis Patterns](references/wallet-analysis.md)
- [Data Upload (CSV/NDJSON)](references/data-upload.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, SQL, JSON, CSV, shell commands, and tabular text depending on the requested Dune task.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3, dune-client, and DUNE_API_KEY for live Dune operations.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
