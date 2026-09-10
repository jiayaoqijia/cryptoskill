## Description:

Make paid API requests using the x402 HTTP payment protocol for x402-protected services, including private web search through an x402 search gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kodos-vibe](https://clawhub.ai/user/kodos-vibe)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to make x402-paid HTTP requests and retrieve web search results from x402-protected gateways while signing payments with a dedicated Base Sepolia wallet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically authorize wallet payments for x402 requests.

Mitigation: Use a dedicated low-balance test wallet, inspect payment terms and endpoints manually, and avoid granting access to valuable funds.

Risk: Private keys may be supplied through environment variables or command-line arguments.

Mitigation: Prefer a key file, do not reuse a valuable wallet, and avoid exposing private keys in shell history or process listings.

Risk: Install-time npm dependencies are fetched before the request scripts are used.

Mitigation: Review the setup script and dependency list before installation, especially in managed or production environments.

## Reference(s):

- [Known x402 services](references/services.md)
- [ClawHub skill page](https://clawhub.ai/kodos-vibe/skills/x402-private-search)
- [Web Search x402 gateway](https://nicholas-hopefully-plumbing-troubleshooting.trycloudflare.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands; CLI responses are emitted as JSON or text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May authorize x402 payments using a configured wallet and prints API responses to stdout.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
