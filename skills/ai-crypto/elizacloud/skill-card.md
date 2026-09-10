## Description:

Manage elizaOS Cloud - deploy AI agents, chat completions, image/video generation, voice cloning, knowledge base, containers, and marketplace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[odilitime](https://clawhub.ai/user/odilitime)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to manage elizaOS Cloud agents, invoke generation endpoints, work with knowledge and A2A APIs, and perform cloud account operations from chat guidance or shell/API examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses ELIZACLOUD_API_KEY for cloud changes and API calls.

Mitigation: Use a narrowly scoped API key, keep it out of version control, and rotate separate development and production keys.

Risk: Agent deletion, billing changes, top-ups, API-key creation, and public or discoverable registration can have account or cost impact.

Mitigation: Require explicit user approval before executing destructive, billing, credential, or public registration actions.

Risk: Chat, image, knowledge, and A2A payloads may send sensitive content to elizaOS Cloud endpoints.

Mitigation: Avoid sending secrets or regulated data unless the user has confirmed the data handling requirements for the account and use case.

Risk: ELIZACLOUD_BASE_URL can redirect requests to a different endpoint.

Mitigation: Set ELIZACLOUD_BASE_URL only to a trusted HTTPS elizaOS endpoint.

Risk: The optional global CLI install shown in the artifact is not pinned.

Mitigation: Prefer a pinned version or local project install before running CLI commands.

## Reference(s):

- [elizaOS Cloud API Reference](references/api-reference.md)
- [elizaOS Cloud Docs](https://www.elizacloud.ai/docs)
- [elizaOS Cloud OpenAPI Spec](https://elizacloud.ai/api/openapi.json)
- [elizaOS Cloud Dashboard](https://elizacloud.ai/dashboard)
- [ClawHub Skill Page](https://clawhub.ai/odilitime/skills/elizacloud)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request examples and shell commands that require ELIZACLOUD_API_KEY.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
