## Description:

Manage smart alerts — list, create, update, toggle, delete. Use when setting up or managing token flow alerts, smart money alerts, or notification rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use Nansen smart alerts to monitor smart-money token flows and token transfers, configure notification rules, and manage existing alerts through the Nansen CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Webhook URLs and signing secrets can be exposed in shared output or agent transcripts.

Mitigation: Keep them out of shared output and transcripts; pass webhook signing secrets through stdin or the documented environment variable.

## Reference(s):

- [Nansen CLI browser login platform scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)
- [ClawHub skill release](https://clawhub.ai/nansen-devops/skills/nansen-smart-alerts)
- [Publisher profile](https://clawhub.ai/user/nansen-devops)

## Skill Output:

**Output Type(s):** [Shell commands, Text, Configuration instructions]

**Output Format:** [Nansen CLI commands and text or table results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Manages smart alerts through the selected Nansen account credentials; channel credentials are redacted in output by default.]

## Skill Version(s):

0.1.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
