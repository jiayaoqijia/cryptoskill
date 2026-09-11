## Description:

Helps agents call paid x402 API endpoints for QR code generation and image hosting, with documented planned image, vision, and video APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parsonssss](https://clawhub.ai/user/parsonssss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to integrate paid x402 API calls for QR code image generation and image upload hosting while following the required payment flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid x402 requests can give an agent payment-signing authority without enough user control or payment validation.

Mitigation: Use a dedicated low-balance wallet, pin the API URL to the intended service, and require manual confirmation for each paid request.

Risk: Image upload behavior can make private or regulated images externally hosted.

Mitigation: Avoid uploading private or regulated images unless external hosting is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/parsonssss/skills/x402-agent-api-skill)
- [x402 API service](https://www.x402api.app/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript code examples, shell commands, and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide paid API calls that return PNG QR code image data or public image URLs.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
