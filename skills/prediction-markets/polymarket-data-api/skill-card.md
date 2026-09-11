## Description:

Query public Polymarket prediction market data without authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bombfuock](https://clawhub.ai/user/bombfuock)

### License/Terms of Use:


## Use Case:

Developers and analysts use this skill to retrieve public Polymarket market data, including top markets, keyword-filtered markets, market details, and event listings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to Polymarket's public API when its commands are run.

Mitigation: Use the skill only in environments where outbound access to https://gamma-api.polymarket.com is allowed, and apply network allowlisting if required.

Risk: Market data returned from a public API may be incomplete, unavailable, delayed, or unsuitable as sole decision support.

Mitigation: Review API responses before acting on them and corroborate important market information with appropriate sources.

## Reference(s):

- [Polymarket Gamma API](https://gamma-api.polymarket.com)
- [ClawHub skill page](https://clawhub.ai/bombfuock/skills/polymarket-data-api)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text summaries or JSON returned from command-line API queries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outbound requests are made to Polymarket's public API when commands are run.]

## Skill Version(s):

1.0.0 (source: artifact metadata and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
