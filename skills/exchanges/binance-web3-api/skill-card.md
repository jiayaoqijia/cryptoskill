## Description:

Operates Binance Web3 public market and research APIs through UXC with a curated OpenAPI schema for token search, metadata, market snapshots, address holdings, rankings, token audit, and smart money signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to discover and execute public Binance Web3 read operations for token research, wallet-position lookup, rankings, audits, and market signals without account trading access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup can load a mutable remote OpenAPI schema that may change after review.

Mitigation: Prefer the bundled schema file or a commit-pinned schema URL, and review schema changes before linking the command.

Risk: Public Binance Web3 requests may associate queried wallet addresses with request logs.

Mitigation: Avoid querying wallet addresses that should not be associated with Binance request logs; use public or test addresses where possible.

Risk: The skill covers public research endpoints and not Binance account trading APIs.

Mitigation: Keep use within token research, market snapshots, rankings, audit, signals, and address holdings; do not treat it as an account trading or posting interface.

## Reference(s):

- [Usage patterns](references/usage-patterns.md)
- [Curated OpenAPI schema](references/binance-web3.openapi.json)
- [Binance Web3 API host](https://web3.binance.com)
- [Binance skills hub source material](https://github.com/binance/binance-skills-hub/tree/main/skills/binance-web3)
- [ClawHub skill page](https://clawhub.ai/jolestar/skills/binance-web3-openapi-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown guidance with inline shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to keep UXC command output in JSON envelopes and to use operation-scoped headers where required.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
