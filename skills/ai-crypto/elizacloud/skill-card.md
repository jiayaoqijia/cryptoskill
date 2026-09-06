## Description: <br>
Manage elizaOS Cloud - deploy AI agents, chat completions, image/video generation, voice cloning, knowledge base, containers, and marketplace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[odilitime](https://clawhub.ai/user/odilitime) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to manage elizaOS Cloud accounts, deploy and interact with hosted agents, generate media, manage knowledge bases and containers, and work with billing or API-key workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform broad elizaOS Cloud account-management actions, including destructive, deployment, billing, payment, and API-key workflows. <br>
Mitigation: Use a least-privilege API key and manually approve deletes, deployments, API-key creation, knowledge uploads, public registrations, credit purchases, auto top-up, crypto payments, and other cost-incurring actions. <br>
Risk: Requests may be sent to an unintended service if the configurable base URL is changed. <br>
Mitigation: Keep ELIZACLOUD_BASE_URL pointed at the official trusted endpoint unless a reviewed alternative endpoint is intentionally required. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/odilitime/elizacloud) <br>
- [elizaOS Cloud API reference](references/api-reference.md) <br>
- [elizaOS Cloud documentation](https://www.elizacloud.ai/docs) <br>
- [elizaOS Cloud OpenAPI specification](https://elizacloud.ai/api/openapi.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ELIZACLOUD_API_KEY; ELIZACLOUD_BASE_URL can override the default API endpoint.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
