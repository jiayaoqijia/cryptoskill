## Description:

REST API for optimized token swapping, executable transaction generation, swap quoting, token pricing, token metadata, and liquidity-provider discovery using the SushiSwap Aggregator.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xmasayoshi](https://clawhub.ai/user/0xmasayoshi)

### License/Terms of Use:


## Use Case:

Developers and external integrators use this skill to build agent workflows that query SushiSwap pricing, quotes, token data, liquidity-provider data, and swap transaction payloads through the SushiSwap REST API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can generate executable crypto swap transaction payloads.

Mitigation: Require explicit review of chain ID, token addresses, sender, recipient, amount, slippage, price impact, fee receiver, tx.to, tx.value, and calldata before wallet approval, signing, or broadcast.

Risk: Agents may construct requests against an unintended or spoofed API endpoint.

Mitigation: Configure clients to use only https://api.sushi.com for live SushiSwap API calls.

Risk: Swap-related requests may omit or misuse the required referrer value.

Mitigation: Require the integrator-supplied referrer parameter for quote and swap endpoints and do not auto-generate, spoof, or omit it.

## Reference(s):

- [OpenAPI usage guide](references/OPENAPI.md)
- [Sushi API OpenAPI schema](references/openapi.yaml)
- [Sushi API](https://api.sushi.com)
- [SwaggerHub API Auto Mocking endpoint](https://virtserver.swaggerhub.com/sushi-labs/sushi/7.0.0)

## Skill Output:

**Output Type(s):** [guidance, API calls, code, configuration]

**Output Format:** [Markdown with HTTP request details, JSON-compatible parameters, and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the bundled OpenAPI schema as the source of truth for endpoint paths, required parameters, defaults, and response shapes.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
