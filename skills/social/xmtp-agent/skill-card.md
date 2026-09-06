## Description: <br>
Building and extending XMTP agents with the Agent SDK for setup and features such as commands, attachments, reactions, groups, transactions, inline actions, and domain resolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[humanagent](https://clawhub.ai/user/humanagent) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to build event-driven XMTP messaging agents, configure agent environments, and add messaging, wallet, group, attachment, command, inline action, and identity-resolution behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Copied attachment examples could save untrusted filenames unsafely. <br>
Mitigation: Sanitize attachment filenames, restrict writes to a dedicated download directory, and prevent path traversal or unintended overwrites. <br>
Risk: Attachment upload examples may publish encrypted objects through public URLs unless that exposure is intentional. <br>
Mitigation: Use private storage or signed URLs where appropriate, document retention and access expectations, and confirm public URL behavior before production use. <br>
Risk: Wallet, payment, group membership, and environment variable flows can expose secrets or perform unintended financial or administrative actions. <br>
Mitigation: Protect .env secrets, use a dedicated low-value agent wallet, and require explicit confirmations, spending limits, and group membership limits. <br>


## Reference(s): <br>
- [ClawHub XMTP skill release](https://clawhub.ai/humanagent/skills/xmtp-agent) <br>
- [Publisher profile](https://clawhub.ai/user/humanagent) <br>
- [Skill overview](artifact/SKILL.md) <br>
- [Building agents](artifact/building-agents/SKILL.md) <br>
- [Handling attachments](artifact/handling-attachments/SKILL.md) <br>
- [Handling transactions](artifact/handling-transactions/SKILL.md) <br>
- [Managing groups](artifact/managing-groups/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with TypeScript and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces implementation guidance and snippets for XMTP agent behavior; it does not directly execute code.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
