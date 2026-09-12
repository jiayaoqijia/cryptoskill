## Description:

Operate Kraken public market APIs through UXC with a curated OpenAPI schema, market-first discovery, and explicit private-auth boundary notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect and run Kraken public market-data reads for server time, asset pair metadata, ticker data, OHLC candles, and order book snapshots. It is intended for public, read-only market-data workflows, not private account or trading operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is described as public and read-only, but it bundles a private account and trading API schema.

Mitigation: Keep usage limited to the curated public schema and remove or split the private schema into a separately reviewed trading skill with confirmation gates.

Risk: Setup links to a mutable remote schema, which can change after review.

Mitigation: Pin UXC to a reviewed public-only schema or verify the schema content before linking it in automation.

Risk: Providing Kraken API keys could enable private account or trading behavior outside the documented public-read scope.

Mitigation: Do not provide Kraken API keys when using this skill, and verify the linked schema exposes only public endpoints.

## Reference(s):

- [Usage Patterns](references/usage-patterns.md)
- [Kraken Public API OpenAPI Schema](references/kraken-public.openapi.json)
- [Official Kraken API Intro](https://docs.kraken.com/api/docs/guides/global-intro)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API output expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public Kraken market-data operations should stay on the JSON output envelope and avoid private credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
