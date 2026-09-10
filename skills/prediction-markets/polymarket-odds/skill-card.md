## Description:

Polymarket Odds helps agents query Polymarket prediction-market odds, events, prices, tags, and order books from a command-line interface.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deanpress](https://clawhub.ai/user/deanpress)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to look up current prediction-market probabilities for sports, politics, crypto, elections, geopolitics, and related topics. It supports market search, event browsing, current price lookup, and order-book inspection without requiring an API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market search terms and token IDs are sent to Polymarket public APIs.

Mitigation: Use the skill only with queries and token IDs that are acceptable to share with Polymarket.

Risk: Returned odds may be mistaken for financial advice.

Mitigation: Treat odds as informational market data and verify decisions through appropriate financial or domain review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deanpress/skills/polymarket-odds)
- [Polymarket Gamma API](https://gamma-api.polymarket.com)
- [Polymarket CLOB API](https://clob.polymarket.com)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text and Markdown summaries with CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only market lookup results from public Polymarket endpoints; no account access or trade execution.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
