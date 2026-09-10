## Description:

Read-only Hyperliquid market data assistant with natural-language, terminal-style, and slash-style requests for quotes, movers, funding rankings, order books, candle snapshots, and account views via the Hyperliquid Info API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[k0nkupa](https://clawhub.ai/user/k0nkupa)

### License/Terms of Use:


## Use Case:

Developers, traders, and analysts use this skill to retrieve read-only Hyperliquid market data and account views from chat or command-style prompts. It supports quotes, movers, funding rankings, order books, candle snapshots, positions, balances, orders, fills, and local account aliases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account-view requests send wallet addresses to Hyperliquid's public Info API.

Mitigation: Use account queries only for addresses you are comfortable sending to the public API, and avoid account views when address privacy is required.

Risk: Saved account aliases store wallet label and address mappings locally, and labels can reveal identity or strategy.

Mitigation: Use non-sensitive labels, restrict access to the local config file, and remove aliases that are no longer needed.

Risk: Natural-language account operations may resolve saved labels or a default account.

Mitigation: Use explicit `hl` or `/hl` commands for account operations and confirm the intended address or alias before querying account data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/k0nkupa/skills/hyperliquid)
- [Hyperliquid API notes](references/hyperliquid-api.md)
- [Hyperliquid Info API reference](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint)
- [Hyperliquid perpetuals API reference](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint/perpetuals)
- [Hyperliquid spot API reference](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint/spot)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text or Markdown chat responses with concise bullets and inline command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only; may call Hyperliquid's public Info API and may store local account aliases.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
