## Description:

Manage smart alerts for token flows, smart money activity, transfer events, contract calls, and notification rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and internal Nansen users use this skill to list, create, update, toggle, and delete smart alerts for token flows, smart money activity, transfer events, contract calls, and notification routing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and relies on an unpinned nansen-cli package that uses an internal Nansen API key.

Mitigation: Install only from a trusted package source, pin or review the dependency before deployment, and use a narrowly scoped API key.

Risk: Alert delete operations can permanently remove configured smart alerts.

Mitigation: Inspect target alerts before deletion and prefer disabling alerts when permanent removal is not required.

Risk: Webhook notifications can forward alert payloads to external endpoints.

Mitigation: Send webhooks only to endpoints the user controls and trusts, and protect webhook secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nansen-devops/skills/nansen-smart-alerts)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and option tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the nansen CLI and NANSEN_API_KEY environment variable.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
