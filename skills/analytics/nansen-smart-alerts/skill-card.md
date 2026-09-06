## Description: <br>
Manage smart alerts - list, create, update, toggle, delete. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nansen-devops](https://clawhub.ai/user/nansen-devops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up and manage Nansen smart alerts for token flows, smart money activity, contract interactions, and notification rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can delete or modify Nansen smart alerts when used with a NANSEN_API_KEY. <br>
Mitigation: Confirm alert IDs before deletion or update, and prefer disabling alerts when the intended change is uncertain. <br>
Risk: Webhook alert payloads may reveal monitored tokens, addresses, or operational strategy. <br>
Mitigation: Send webhooks only to trusted HTTPS endpoints and use webhook secrets when configuring webhook delivery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nansen-devops/nansen-smart-alerts) <br>
- [Publisher profile](https://clawhub.ai/user/nansen-devops) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the nansen CLI and NANSEN_API_KEY to manage alert configuration and state.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
