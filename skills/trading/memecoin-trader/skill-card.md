## Description:

Automates headless memecoin trading on Solana by guiding an agent to configure and run the fdv.lol CLI with Agent Gary Full AI Control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[build23w](https://clawhub.ai/user/build23w)

### License/Terms of Use:


## Use Case:

External users and agent operators use this skill to create a local trading profile, supply required Solana RPC, wallet, Jupiter, and LLM credentials, and run a fully agent-controlled memecoin trading CLI. The skill is intended for users who understand autonomous crypto-trading risk and can enforce small balances and local secret handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill supports autonomous crypto trading and can authorize AI-directed trading decisions.

Mitigation: Use only a burner wallet with a strict small balance and configure hard trading limits before running.

Risk: The skill asks the agent to run remote CLI code while using wallet and API secrets.

Mitigation: Independently review and pin the exact CLI version before execution, prefer a sandboxed run, and keep profile files private with owner-only permissions.

Risk: Profile files contain sensitive wallet and API credentials.

Mitigation: Keep credentials local, avoid logging secrets, redact outputs, and do not upload or publish populated profiles.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/build23w/skills/agentic-powered-memecoin-trader)
- [fdv.lol repository](https://github.com/build23w/fdv.lol)
- [fdv.lol upstream profile example](https://github.com/build23w/fdv.lol/blob/main/tools/profiles/fdv.profiles.example.json)
- [Local OpenClaw example profile](artifact/openclaw.example.json)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON profile configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a locally generated profile containing user-provided RPC, wallet, Jupiter, and LLM credentials.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
