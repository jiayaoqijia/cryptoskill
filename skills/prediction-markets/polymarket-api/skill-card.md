## Description:

Query Polymarket prediction markets for market prices, betting odds, event probabilities, and related market data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dannyshmueli](https://clawhub.ai/user/dannyshmueli)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to retrieve and summarize Polymarket prediction market data, including top markets, text searches, specific market slugs, and grouped events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound read-only requests to Polymarket's public API for market data.

Mitigation: Install only if this network access is acceptable, and invoke it only for Polymarket-specific questions or market slugs when tighter control is needed.

## Reference(s):

- [Polymarket Gamma API](https://gamma-api.polymarket.com)
- [ClawHub skill page](https://clawhub.ai/dannyshmueli/skills/polymarket-api)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text market summaries or raw JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public API lookups; no API key required.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
