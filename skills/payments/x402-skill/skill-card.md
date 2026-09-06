## Description: <br>
Discover, browse, filter, and pay for x402-compatible API endpoints and MCP tools from the x402 Bazaar. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coinvest518](https://clawhub.ai/user/coinvest518) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to discover x402-compatible services, inspect payment requirements, and optionally make paid API calls using USDC. It is suited for browsing available pay-per-call APIs and for controlled agent workflows that need discovery, filtering, and payment execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent-triggered USDC payments may spend real funds on third-party API calls. <br>
Mitigation: Use a dedicated low-balance wallet, prefer testnet first, and set strict per-call spend limits before enabling paid calls. <br>
Risk: Wallet private keys are required for paid calls and could expose funds if mishandled. <br>
Mitigation: Do not use a primary wallet key; keep EVM_PRIVATE_KEY local, out of version control, and scoped to a limited-balance wallet. <br>
Risk: Automatic MCP payment flows can send requests and payment proofs without manual review. <br>
Mitigation: Enable automatic payments only with endpoint allowlisting, confirmation controls, and logs covering amount, recipient, network, and transmitted request data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/coinvest518/openclaw-x402-skill) <br>
- [x402 MCP integration guide](x402-MCP.md) <br>
- [Coinbase CDP x402 Bazaar documentation](https://docs.cdp.coinbase.com/x402/bazaar) <br>
- [Coinbase CDP x402 documentation](https://docs.cdp.coinbase.com/x402) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown and terminal text with inline shell commands, configuration snippets, service listings, and API response payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include payment amounts, recipient and network details, transaction hashes, endpoint URLs, and returned third-party API data.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
