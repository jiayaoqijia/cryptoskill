## Description:

Detects x402 crypto paywalls for AI agents, checks payment policy, signs USDC payments on Base through the Coinbase facilitator, and retries the original request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tara-quinn-ai](https://clawhub.ai/user/tara-quinn-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to let agents access x402-enabled paid APIs or premium content while enforcing spending limits, network and asset restrictions, domain controls, optional human approval, and payment logging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires wallet signing authority and can initiate real USDC payments.

Mitigation: Use a dedicated low-balance wallet, start on Base Sepolia testnet, and require human approval before enabling mainnet spending.

Risk: Payments may be sent to unintended services if domain or recipient controls are too broad.

Mitigation: Configure non-empty domain and recipient allowlists before production use.

Risk: Server security evidence reports unresolved package-identity concerns.

Mitigation: Confirm the npm packages are published by the expected owner and match this source before installing.

Risk: Server security evidence warns against relying on the current policy engine until malformed and negative amount handling is fixed.

Mitigation: Keep conservative spend limits, inspect payment requirements before approval, and avoid unattended production use until the policy handling issue is resolved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tara-quinn-ai/skills/x402-paywall-kit)
- [Tara Quinn homepage](https://taraquinn.ai)
- [x402 protocol](https://x402.org)
- [README](README.md)
- [Agent package README](packages/agent/README.md)
- [Express package README](packages/express/README.md)
- [Shared package README](packages/shared/README.md)
- [Demo README](demo/README.md)
- [Product requirements](docs/PRD.md)
- [Agent setup example](references/agent-setup.example.ts)
- [Policy example](references/policy.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript examples, shell commands, and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes guidance for wallet environment variables, policy controls, network selection, and payment logging.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
