## Description:

Accept crypto payments on Solana via MoonPay Commerce (formerly Helio) by creating Pay Links, generating checkout URLs, checking transactions, and listing supported currencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mavagio](https://clawhub.ai/user/mavagio)

### License/Terms of Use:


## Use Case:

Developers, engineers, and merchants use this skill to configure MoonPay Commerce credentials and operate Solana crypto-payment flows for products, services, invoices, or payment status checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create and modify real payment links with MoonPay Commerce merchant credentials.

Mitigation: Confirm amounts, currencies, pay-link IDs, wallet selection, and intended payment action before running generated commands or helper scripts.

Risk: API credentials are stored locally and may be exposed on shared, managed, recorded, or multi-user machines.

Mitigation: Store the config with owner-only permissions, avoid setup during screen sharing or recording, and rotate the API secret if it may have appeared in terminal output or process logs.

## Reference(s):

- [MoonPay Commerce API Reference](references/api-reference.md)
- [MoonPay Commerce OpenAPI Specification](https://api.hel.io/v1/docs-json)
- [MoonPay Commerce Documentation](https://docs.hel.io)
- [MoonPay Commerce Dashboard](https://app.hel.io)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call MoonPay Commerce APIs through curl and jq when the user runs the provided helper scripts.]

## Skill Version(s):

0.3.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
