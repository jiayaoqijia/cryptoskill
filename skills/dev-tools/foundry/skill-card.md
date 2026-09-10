## Description:

Self-writing meta-extension that forges new capabilities — researches docs, writes extensions, tools, hooks, and skills

This skill is ready for commercial/non-commercial use.

## Publisher:

[lekt9](https://clawhub.ai/user/lekt9)

### License/Terms of Use:


## Use Case:

Developers and engineers use Foundry with OpenClaw to research documentation, generate extensions, tools, hooks, and skill packages, and capture learning from implementation outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Foundry can create and modify OpenClaw capabilities, including self-extension behavior.

Mitigation: Review generated code before enabling it and require explicit confirmation before self-extension.

Risk: Automatic learning from agent activity and external sources can persist new patterns or capabilities.

Mitigation: Disable autoLearn by default unless the operator has reviewed the behavior and approved the learning sources.

Risk: Unpinned or auto-enabled installation and marketplace actions can introduce unreviewed capabilities.

Mitigation: Pin and verify the plugin version, and require explicit confirmation before marketplace publishing or community ability installation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lekt9/skills/foundry)
- [Foundry Homepage](https://getfoundry.app)
- [OpenClaw Repository Metadata](https://github.com/lekt9/openclaw-foundry)
- [Foundry Marketplace](https://api.claw.getfoundry.app)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell-command, code, and JSON configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify OpenClaw extensions, skills, hooks, tools, and configuration when invoked through Foundry workflows.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
