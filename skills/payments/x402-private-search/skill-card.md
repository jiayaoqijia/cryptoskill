## Description: <br>
Enables agents to make x402-paid HTTP requests, including paid web search through an x402 gateway, using USDC payments on Base Sepolia. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kodos-vibe](https://clawhub.ai/user/kodos-vibe) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external agents use this skill to access x402-protected APIs and run paid web searches after configuring a funded Base Sepolia wallet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can sign x402 payments from the configured wallet. <br>
Mitigation: Use a dedicated low-balance test wallet and review the service URL and price before each paid request. <br>
Risk: Private keys may be exposed through command-line arguments or long-lived environment variables. <br>
Mitigation: Prefer a local key file with restrictive permissions and avoid reusing valuable wallets or mainnet private keys. <br>
Risk: The documented web search endpoint uses a transient Cloudflare gateway that may change or be unsuitable for sensitive queries. <br>
Mitigation: Verify the gateway with its health or routes endpoint before use and avoid sending sensitive searches through it. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kodos-vibe/x402-private-search) <br>
- [Known x402 Services](references/services.md) <br>
- [Known x402 web search service](https://nicholas-hopefully-plumbing-troubleshooting.trycloudflare.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, API calls] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May sign x402 payment requests and print response bodies to stdout.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
