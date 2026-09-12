## Description:

Operate Bitget public exchange market APIs through UXC with a curated OpenAPI schema, market-first discovery, and explicit private-auth boundary notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to discover and execute read-only Bitget public spot market-data operations, including symbols, tickers, candles, and order book snapshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote schema retrieval can introduce supply-chain drift if the schema URL changes after review.

Mitigation: Prefer the bundled schema or a pinned reviewed schema URL when reproducible behavior is required.

Risk: Extending the skill to private account or trading endpoints would add signing, credential, and transaction risks outside this release scope.

Mitigation: Keep this release limited to public read-only market data unless a separate Bitget signer flow and review are completed.

## Reference(s):

- [Usage patterns](references/usage-patterns.md)
- [Curated OpenAPI schema](references/bitget-v2.openapi.json)
- [Official Bitget API intro](https://www.bitget.com/api-doc/common/intro)
- [Skill page](https://clawhub.ai/jolestar/skills/bitget-openapi-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON-oriented API response guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance emphasizes JSON output envelopes, narrow spot market reads, and public read-only endpoints.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
