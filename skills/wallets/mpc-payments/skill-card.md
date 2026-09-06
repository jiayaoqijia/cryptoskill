## Description: <br>
Accept crypto payments on Solana via MoonPay Commerce by creating Pay Links, generating checkout URLs, checking transactions, and listing supported currencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mavagio](https://clawhub.ai/user/mavagio) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, merchants, and agents assisting merchant operators use this skill to configure MoonPay Commerce credentials, create Solana Pay Links, generate checkout URLs, and review payment transactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles MoonPay Commerce API credentials for a merchant account. <br>
Mitigation: Run setup only in a trusted terminal, avoid sharing terminal logs or screenshots, use the least-privilege API key available, and clear the saved config when finished. <br>
Risk: The skill can create, disable, or enable live Pay Links. <br>
Mitigation: Verify payment amounts, currencies, wallet selection, and Pay Link IDs before allowing create, disable, or enable commands to run. <br>
Risk: Saved credentials are stored on disk for later shell-script use. <br>
Mitigation: Keep the config file restricted to the current user with mode 600 and remove it when the agent no longer needs payment-account access. <br>


## Reference(s): <br>
- [MoonPay Commerce API Reference](artifact/references/api-reference.md) <br>
- [MoonPay Commerce OpenAPI Spec](https://api.hel.io/v1/docs-json) <br>
- [MoonPay Commerce Swagger UI](https://api.hel.io/v1/docs) <br>
- [MoonPay Commerce Docs](https://docs.hel.io) <br>
- [MoonPay Commerce Dashboard](https://app.hel.io) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May instruct an agent to run setup and helper shell scripts that call MoonPay Commerce APIs.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata and CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
