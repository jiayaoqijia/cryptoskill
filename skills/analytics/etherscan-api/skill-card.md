## Description:

Use when you need to query Etherscan API V2 for onchain activity, contract metadata, ABI/source retrieval, proxy implementation discovery, and transaction/log analysis across EVM chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidtaikocha](https://clawhub.ai/user/davidtaikocha)

### License/Terms of Use:


## Use Case:

Developers and blockchain analysts use this skill to query Etherscan-compatible API V2 endpoints for EVM transaction activity, logs, contract ABI/source metadata, proxy implementation details, and transaction status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Etherscan API keys can be exposed if generated URLs or logs include the apikey parameter.

Mitigation: Provide the API key through ETHERSCAN_API_KEY or a secret store, and redact apikey values before sharing generated URLs, logs, or results.

Risk: Queries against the wrong chainid can produce misleading onchain context.

Mitigation: Confirm the target chainid and explorer against the network map before querying, and include the chainid and explorer in outputs.

Risk: Large activity or log scans can exceed Etherscan plan limits or miss results without pagination.

Mitigation: Use throttling, retries, explicit block ranges, pagination, and resumable checkpoints for long-running scans.

## Reference(s):

- [Network Map (Etherscan V2)](references/network-map.md)
- [Endpoint Cheatsheet](references/endpoint-cheatsheet.md)
- [Rate Limits (Etherscan V2)](references/rate-limits.md)
- [Explorer URL Patterns](references/explorer-url-patterns.md)
- [Etherscan API V2 Introduction](https://docs.etherscan.io/introduction)
- [Etherscan Supported Chains](https://docs.etherscan.io/supported-chains)
- [Etherscan Rate Limits](https://docs.etherscan.io/resources/rate-limits)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration guidance]

**Output Format:** [Markdown with inline URLs, query parameters, parsed result summaries, and bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include the queried chain, endpoint module/action, redacted request URL, parsed status/result summary, and proxy follow-up decisions when relevant.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
