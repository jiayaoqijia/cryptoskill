## Description:

API reference for CoinMarketCap DEX endpoints including token lookup, pools, transactions, trending, and security analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bryan-cmc](https://clawhub.ai/user/bryan-cmc)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to choose CoinMarketCap DEX endpoints and parameters for on-chain token lookup, prices, liquidity pools, trending discovery, transactions, and security checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed if copied into shared logs or committed files.

Mitigation: Use environment variables or a secrets manager and redact X-CMC_PRO_API_KEY values from examples, logs, and commits.

Risk: Wallet-address and transaction results can reveal activity linked to people or organizations.

Mitigation: Treat address and transaction outputs as sensitive and share only the minimum necessary context.

Risk: On-chain security signals can be misunderstood as a guarantee of token safety.

Mitigation: Review risk score, warnings, liquidity lock, ownership, holder concentration, and trading flags together before acting.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bryan-cmc/skills/cmc-api-onchain-data)
- [CoinMarketCap Pro API Base URL](https://pro-api.coinmarketcap.com)
- [CoinMarketCap Pro API Login](https://pro.coinmarketcap.com/login)
- [DEX Token APIs](artifact/references/tokens.md)
- [DEX Pairs APIs](artifact/references/pairs.md)
- [DEX Platform APIs](artifact/references/platforms.md)
- [DEX Discovery APIs](artifact/references/discovery.md)
- [DEX Security API](artifact/references/security.md)
- [Common Use Cases](artifact/references/use-cases.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API endpoint references, JSON request examples, and curl command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a CoinMarketCap API key for live API calls; avoid exposing keys in shared logs or committed files.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
