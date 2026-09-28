## Description:

Manage Nansen smart alerts for token flows, smart money activity, transfers, and contract interactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Nansen users and developers use this skill to list, create, update, enable, disable, and delete account smart alerts and configure their notification channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Updating, toggling, or deleting the wrong alert changes account notification rules.

Mitigation: Review the target alert and double-check its ID before changing it.

Risk: Webhooks send alert payloads to the configured endpoint.

Mitigation: Use trusted HTTPS endpoints and a webhook secret when available.

## Reference(s):

- [Nansen Smart Alerts on ClawHub](https://clawhub.ai/nansen-devops/skills/nansen-smart-alerts)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration guidance]

**Output Format:** [Markdown with bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands manage alerts through the Nansen CLI and may configure Telegram, Slack, Discord, or webhook notifications.]

## Skill Version(s):

0.1.2 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
