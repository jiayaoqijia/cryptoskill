## Description:

Interact with Polymarket US prediction markets to browse and search markets, check prices and odds, view portfolio positions and balances, place or cancel trades, check order status, look up events or sports markets, and get settlement information using the polymarket-us Python package.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tyhouch](https://clawhub.ai/user/tyhouch)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to retrieve Polymarket US market data, format market and portfolio information, and prepare authenticated trading workflows through the Python SDK. Trading use requires API credentials and explicit user confirmation before any state-changing action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enable live financial trading actions when authenticated Polymarket credentials are available.

Mitigation: Require explicit user review and confirmation before placing, modifying, canceling, canceling all, or closing any position.

Risk: The SDK install command does not pin a reviewed polymarket-us package version.

Mitigation: Install a pinned, reviewed SDK version in an isolated environment before enabling trading workflows.

Risk: Polymarket API credentials may authorize portfolio and trading operations.

Mitigation: Use limited-scope credentials where possible and keep POLYMARKET_KEY_ID and POLYMARKET_SECRET_KEY out of generated outputs.

## Reference(s):

- [Polymarket US API Reference](references/api_reference.md)
- [Polymarket Developer API Keys](https://polymarket.us/developer)
- [Polymarket Public Data API](https://gateway.polymarket.us)
- [Polymarket Trading API](https://api.polymarket.us)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include market summaries, order previews, portfolio summaries, and SDK usage examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
