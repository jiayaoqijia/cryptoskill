## Description: <br>
Agent APIs x402 Skill helps agents call x402-protected paid endpoints for QR code generation and image hosting, with additional image, video, and vision APIs documented as planned. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parsonssss](https://clawhub.ai/user/parsonssss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent builders use this skill to configure an agent to pay for and call x402 API endpoints. The documented live uses are generating QR code images and uploading images to receive a public URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent authority to sign x402 payments with an EVM private key. <br>
Mitigation: Use a dedicated low-balance wallet, store the private key only in a secure secret store, and require explicit approval before each paid request. <br>
Risk: Paid requests could be sent to an unexpected endpoint or with unexpected payment details. <br>
Mitigation: Verify the API base URL, endpoint path, and x402 payment requirements before signing and retrying a request. <br>
Risk: Image uploads may return publicly reachable URLs. <br>
Mitigation: Do not upload sensitive images unless public accessibility is intended and acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/parsonssss/x402-agent-api-skill) <br>
- [Publisher profile](https://clawhub.ai/user/parsonssss) <br>
- [x402 API base URL](https://www.x402api.app/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with TypeScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents through x402 payment signing, endpoint retries, QR image responses, and public image upload URLs.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
