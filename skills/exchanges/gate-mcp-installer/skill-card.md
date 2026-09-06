## Description: <br>
Gate MCP one-click installer for OpenClaw and mcporter that helps install or configure Gate MCP servers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical users use this skill to install Gate MCP servers for OpenClaw through mcporter and to receive post-install authentication guidance for Gate CEX, DEX, info, and news services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer handles financial-service credentials and authenticated remote services. <br>
Mitigation: Use least-privilege Gate API keys, avoid withdrawal permissions unless explicitly required, and rotate or remove credentials after use. <br>
Risk: mcporter may store OAuth tokens, request headers, API keys, or API secrets locally. <br>
Mitigation: Review the local mcporter configuration after installation and keep credentials out of assistant output, logs, and shared files. <br>
Risk: The skill configures remote Gate MCP endpoints and a fixed DEX API key. <br>
Mitigation: Verify the Gate remote endpoints and the hardcoded DEX key are acceptable for the user's trust model before installing. <br>


## Reference(s): <br>
- [MCP execution specification](references/mcp.md) <br>
- [Gate MCP GitHub documentation](https://github.com/gate/gate-mcp) <br>
- [Gate Skills GitHub documentation](https://github.com/gate/gate-skills) <br>
- [Gate API documentation](https://www.gate.com/docs/developers/apiv4/en/) <br>
- [mcporter GitHub documentation](https://github.com/mcporter-dev/mcporter) <br>
- [ClawHub skill page](https://clawhub.ai/gate-exchange/gate-mcp-openclaw-installer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include installation status, verification notes, authentication follow-up steps, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
