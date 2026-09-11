## Description:

Operate Binance Spot market, account, and order APIs through UXC with a curated OpenAPI schema, Binance query signing, and separate mainnet/testnet link flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to discover, configure, and execute Binance Spot REST operations for market data, account reads, order queries, test orders, and carefully reviewed order placement or cancellation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent access to Binance Spot account data and trading actions can expose financial data or execute trades.

Mitigation: Prefer testnet first, use read-only or narrowly permissioned API keys where possible, and require explicit review before any mainnet write.

Risk: A changeable remote OpenAPI schema can affect signed financial operations.

Mitigation: Use the bundled schema or replace the remote schema reference with a pinned, hash-verified copy.

Risk: Mixing Binance API keys and signing material from different key records can cause invalid signatures.

Mitigation: Keep each API key paired with the matching Ed25519 private key or HMAC secret for the same mainnet or testnet key record.

## Reference(s):

- [Usage patterns](references/usage-patterns.md)
- [Curated OpenAPI schema](references/binance-spot.openapi.json)
- [Official Binance Spot API docs](https://github.com/binance/binance-spot-api-docs)
- [Binance Spot skill source material](https://github.com/binance/binance-skills-hub/tree/main/skills/binance/spot)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, API Calls, Guidance]

**Output Format:** [Markdown with inline bash commands, JSON-oriented response guidance, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prefers testnet-first signed examples, JSON output envelopes, and explicit review before mainnet writes.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
