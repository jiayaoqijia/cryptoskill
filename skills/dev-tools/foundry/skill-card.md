## Description: <br>
Self-writing meta-extension that forges new capabilities by researching documentation and writing extensions, tools, hooks, and skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lekt9](https://clawhub.ai/user/lekt9) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use Foundry with OpenClaw to research documentation, generate extensions, tools, hooks, and skills, and manage self-improvement workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and activates external code that can change agent behavior. <br>
Mitigation: Review the npm package and source before installation, pin a version where possible, and use a separate test OpenClaw profile. <br>
Risk: Generated code or self-modification can introduce unsafe or unwanted changes. <br>
Mitigation: Require manual diff review before generated code or self-changes are enabled. <br>
Risk: Auto-learning and marketplace publishing may expose or persist activity patterns beyond the intended scope. <br>
Mitigation: Disable auto-learning and marketplace publishing until the configuration and data boundaries have been reviewed. <br>


## Reference(s): <br>
- [ClawHub Foundry skill page](https://clawhub.ai/lekt9/skills/foundry) <br>
- [Foundry homepage](https://getfoundry.app) <br>
- [OpenClaw Foundry repository](https://github.com/lekt9/openclaw-foundry) <br>
- [Foundry Marketplace](https://api.claw.getfoundry.app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code, shell command, and JSON configuration blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-facing implementation guidance and generated OpenClaw artifacts.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
