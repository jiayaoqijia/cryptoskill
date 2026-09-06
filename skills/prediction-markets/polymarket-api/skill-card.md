## Description: <br>
Query Polymarket prediction markets for market prices, event probabilities, betting odds, and related public market data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dannyshmueli](https://clawhub.ai/user/dannyshmueli) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and analysts use this skill to retrieve public Polymarket market and event data, including top markets, search results, individual market slugs, prices, volumes, and probabilities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends lookup requests, including search terms or slugs, to Polymarket's public API. <br>
Mitigation: Avoid entering private or sensitive information in market searches, and allow network access only to the disclosed Polymarket API endpoint where strict governance is required. <br>


## Reference(s): <br>
- [Polymarket Gamma API](https://gamma-api.polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text market summaries or raw JSON from the Polymarket public API] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include market questions, Yes/No prices as percentages, 24h volume, total volume, liquidity, status, end date, and truncated descriptions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
