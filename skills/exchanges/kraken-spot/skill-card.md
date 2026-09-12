## Description:

Use a Bash CLI to query Kraken Spot and Futures APIs, inspect account state, run guarded trading and funding actions, and work with Kraken websocket payloads using OpenClaw-managed secrets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gabriel-0110](https://clawhub.ai/user/gabriel-0110)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and external agents use this skill to query Kraken market data, inspect account state, and perform guarded account-changing Kraken Spot and Futures actions through a local Bash CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw private calls and configurable workflows can weaken safeguards around account-changing Kraken actions.

Mitigation: Review raw private and WebSocket workflows before installation, prefer registry-backed read-only aliases where possible, and require explicit confirmation for trading, withdrawals, earn allocation, and transfer actions.

Risk: Kraken API credentials, signatures, or challenge material could be exposed through logs or shared transcripts.

Mitigation: Use least-privilege API keys, prefer read-only keys unless trading is required, inject secrets through environment or OpenClaw secret refs, and keep command output containing challenge signatures out of logs.

Risk: Untrusted configuration can redirect endpoints or alter runtime behavior.

Mitigation: Avoid untrusted OPENCLAW_KRAKEN_CONFIG files and keep Kraken REST and WebSocket endpoint variables pinned to official Kraken hosts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gabriel-0110/skills/kraken-spot)
- [Declared homepage](https://github.com/oscraters/kraken-skill.git)
- [OpenClaw secrets documentation](https://docs.openclaw.ai/gateway/secrets)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI responses are text or JSON from Kraken APIs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash, curl, openssl, base64, and od; jq is optional for compact, pretty, and filtered JSON output.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
