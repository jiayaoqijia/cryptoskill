## Description: <br>
Use when you need to query Etherscan API V2 for onchain activity, contract metadata, ABI/source retrieval, proxy implementation discovery, and transaction/log analysis across EVM chains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidtaikocha](https://clawhub.ai/user/davidtaikocha) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to query Etherscan-compatible APIs for onchain activity, contract metadata, ABI/source retrieval, transaction status, logs, and proxy implementation handling across supported EVM chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may use an Etherscan API key while preparing read-only blockchain queries. <br>
Mitigation: Keep the key out of shared chats, logs, generated URLs, and committed files; rotate the key if it is exposed. <br>
Risk: Generated query URLs can reveal investigated addresses, transaction hashes, block ranges, or other blockchain analysis targets. <br>
Mitigation: Review and redact generated URLs before sharing them outside the intended workspace. <br>
Risk: Wrong chain IDs, failed status envelopes, or unbounded pagination can produce misleading or incomplete analysis. <br>
Mitigation: Confirm the target chainid, treat status "0" as non-success, respect rate limits, and use explicit block windows with resumable pagination. <br>


## Reference(s): <br>
- [Endpoint Cheatsheet](references/endpoint-cheatsheet.md) <br>
- [Explorer URL Patterns](references/explorer-url-patterns.md) <br>
- [Network Map](references/network-map.md) <br>
- [Rate Limits](references/rate-limits.md) <br>
- [Etherscan API V2 Introduction](https://docs.etherscan.io/introduction) <br>
- [Etherscan Supported Chains](https://docs.etherscan.io/supported-chains) <br>
- [Etherscan Rate Limits](https://docs.etherscan.io/resources/rate-limits) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with API query examples, parsed result summaries, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Expected responses include the exact URL or query used without exposing the API key, chain and explorer context, endpoint module/action, parsed status/result summary, and proxy follow-up decisions when applicable.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
