## Description: <br>
Use a Bash CLI to query Kraken Spot and Futures APIs, inspect account state, run guarded trading and funding actions, and work with Kraken websocket payloads using OpenClaw-managed secrets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Gabriel-0110](https://clawhub.ai/user/Gabriel-0110) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent inspect Kraken market data and account state, then prepare or execute guarded Spot, Futures, funding, earn, subaccount, and websocket workflows through a local CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send signed Kraken API requests, including arbitrary private and futures raw calls outside the confirmed alias workflow. <br>
Mitigation: Use least-privilege API keys, prefer read-only keys unless trading is required, and require explicit operator approval before raw private, futures raw, withdrawal, transfer, or arbitrary websocket use. <br>
Risk: Trading, funding, earn, subaccount, and withdrawal workflows can change account state or move assets. <br>
Mitigation: Require confirmation for state-changing operations and avoid withdrawal permissions unless they are essential for the deployment. <br>
Risk: Credential exposure or endpoint tampering could lead to unauthorized exchange activity. <br>
Mitigation: Provide secrets through managed environment references, keep OPENCLAW_KRAKEN_CONFIG and base URL settings under operator control, and rely on the skill's redaction and base URL validation behavior. <br>


## Reference(s): <br>
- [ClawHub Kraken CLI release page](https://clawhub.ai/Gabriel-0110/kraken-spot) <br>
- [Kraken skill homepage](https://github.com/oscraters/kraken-skill.git) <br>
- [OpenClaw secrets documentation](https://docs.openclaw.ai/gateway/secrets) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [API responses are emitted by the CLI; stderr is intended for sanitized operational messages.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
