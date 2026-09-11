## Description:

Discover, browse, filter, inspect, and optionally pay for x402-compatible API endpoints and MCP tools from the x402 Bazaar using USDC micropayments on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coinvest518](https://clawhub.ai/user/coinvest518)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to discover x402-compatible HTTP APIs and MCP tools, compare price, type, and payment requirements, and optionally make USDC paid calls on Base through a configured wallet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid calls require agent wallet signing authority.

Mitigation: Use a dedicated low-balance wallet, test on testnet first, and avoid exposing valuable private keys to the agent.

Risk: Endpoint price or payment requirements may be unsafe or unexpected.

Mitigation: Verify each endpoint and price before payment and keep conservative per-call spending limits configured.

Risk: Wallet secrets in .env or desktop configuration files can be exposed through local file access or accidental sharing.

Mitigation: Keep wallet secrets out of repositories and shared configuration, and add them only after dependency installation has been completed in an isolated environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/coinvest518/skills/openclaw-x402-skill)
- [x402 MCP integration guide](artifact/x402-MCP.md)
- [x402 protocol documentation](https://docs.cdp.coinbase.com/x402)
- [x402 Bazaar documentation](https://docs.cdp.coinbase.com/x402/bazaar)
- [Base network documentation](https://docs.base.org)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, configuration snippets, service listings, and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include endpoint URLs, quoted prices, network identifiers, transaction hashes, and paid API response data.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
