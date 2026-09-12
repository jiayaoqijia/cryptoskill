## Description:

Operate Bybit V5 public market APIs through UXC with a curated OpenAPI schema, market-first discovery, and explicit private-auth boundary notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect and run Bybit V5 public market-data reads through UXC, including server time, instruments metadata, tickers, order books, and klines. It is intended for public-data workflows and excludes private account and trading operations in this release.

### Deployment Geography for Use:

Global, subject to Bybit regional and IP access restrictions.

## Known Risks and Mitigations:

Risk: The skill creates or uses a UXC CLI alias and sends outbound requests to Bybit and the referenced schema URL.

Mitigation: Review the alias target and schema URL before installation, and allow those network destinations only in approved environments.

Risk: Private account access and trading actions are outside the inspected v1 scope and would require signing support not included in this release.

Mitigation: Keep use to public market-data endpoints unless a future reviewed version adds and validates a Bybit signer flow.

Risk: Bybit API access may be affected by regional or IP restrictions.

Mitigation: Confirm the execution environment is permitted for Bybit API access before relying on results or debugging request parameters.

## Reference(s):

- [Usage Patterns](references/usage-patterns.md)
- [Curated Bybit V5 OpenAPI Schema](references/bybit-v5.openapi.json)
- [Official Bybit V5 Docs](https://bybit-exchange.github.io/docs/v5/guide)
- [ClawHub Skill Page](https://clawhub.ai/jolestar/skills/bybit-openapi-skill)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public market-data endpoints only; no API keys or trading authority in the inspected release.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
