## Description:

Query cryptocurrency prices, market rankings, 24-hour changes, and coin search results through the CoinGecko API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ouyangabel](https://clawhub.ai/user/ouyangabel)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to look up cryptocurrency prices, market-cap rankings, 24-hour price changes, and CoinGecko coin IDs from an agent workflow. The price data is for reference and should not be treated as financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts CoinGecko over the network whenever an agent performs price lookups or coin searches.

Mitigation: Allow network access only to api.coingecko.com where policy controls support domain restrictions.

Risk: Cryptocurrency prices returned by the external API may be delayed, unavailable, rate limited, or unsuitable for financial decisions.

Mitigation: Treat returned market data as reference information and verify important decisions against authoritative sources.

Risk: Some command-line output is partly Chinese, which may reduce readability for operators who expect English-only logs.

Mitigation: Review sample output before deployment and document expected messages for support staff.

## Reference(s):

- [CoinGecko API Documentation](https://www.coingecko.com/api/documentation)
- [CoinGecko API v3 Endpoint](https://api.coingecko.com/api/v3)
- [ClawHub Skill Page](https://clawhub.ai/ouyangabel/skills/coingecko-price)
- [ClawHub Publisher Profile](https://clawhub.ai/user/ouyangabel)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text and Markdown-friendly command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command output may include current prices, 24-hour percentage changes, market-cap rankings, coin IDs, and API rate-limit errors.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
