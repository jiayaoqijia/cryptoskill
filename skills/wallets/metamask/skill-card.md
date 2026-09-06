## Description: <br>
MetaMask Wallet - Give your agent spending power through CreditClaw payment, wallet, checkout, and spending-management workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codejika](https://clawhub.ai/user/codejika) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to let an agent register with CreditClaw, check spending permissions, request owner-approved purchases, manage balances, make x402 or card-based payments, and create checkout pages or invoices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable real spending, payment signing, checkout, invoicing, and storefront workflows. <br>
Mitigation: Use a limited and revocable CreditClaw API key, keep approval mode strict, and confirm merchant, domain, amount, recipient address, and purchase purpose before each transaction. <br>
Risk: A leaked CREDITCLAW_API_KEY could let another actor act as the agent in CreditClaw commerce workflows. <br>
Mitigation: Store the key only in a secrets manager or protected environment variable, never send it outside creditclaw.com API requests, and rotate or revoke it if exposure is suspected. <br>
Risk: The encrypted-card rail may expose decrypted card details during a checkout flow. <br>
Mitigation: Use the encrypted-card rail only in an isolated execution environment, keep decrypted card data in memory only, never log or persist it, and discard it immediately after checkout. <br>
Risk: The listing name references MetaMask, while the artifact behavior centers on CreditClaw spending, card, x402, checkout, invoice, and storefront capabilities. <br>
Mitigation: Review the CreditClaw scope with the owner before installation and do not rely on the MetaMask branding alone to assess permissions or expected behavior. <br>
Risk: The Stripe x402 wallet rail is described as private beta and may not be available for all accounts. <br>
Mitigation: Check rail status before use and fall back to supported payment rails only when the owner has explicitly enabled them. <br>
Risk: Invoice, customer, buyer, shipping, webhook, and transaction data can contain sensitive third-party information. <br>
Mitigation: Minimize disclosure, avoid unnecessary retention, verify webhook signatures, and treat commerce records as sensitive operational data. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/codejika/metamask) <br>
- [CreditClaw main skill documentation](https://creditclaw.com/skill.md) <br>
- [Encrypted card checkout guide](https://creditclaw.com/encrypted-card.md) <br>
- [Stripe x402 wallet guide](https://creditclaw.com/stripe-x402-wallet.md) <br>
- [Wallet management guide](https://creditclaw.com/management.md) <br>
- [Checkout, invoices, and shop guide](https://creditclaw.com/checkout.md) <br>
- [Heartbeat polling guide](https://creditclaw.com/heartbeat.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with inline bash commands, JSON request and response examples, and API endpoint references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a CREDITCLAW_API_KEY environment variable for authenticated CreditClaw API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence; artifact skill.md frontmatter reports 2.0.0 and skill.json reports 2.5.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
