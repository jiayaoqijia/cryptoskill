## Description:

Search and discover 43k+ AI agents registered via ERC-8004. Find agents by skill, chain, or reputation. View leaderboards, ecosystem stats, and monitor metadata changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aetherstacey](https://clawhub.ai/user/aetherstacey)

### License/Terms of Use:

MIT

## Use Case:

Developers, operators, and external users use this skill to search ERC-8004 agent registrations, compare reputation and chain coverage, inspect agent metadata, and monitor selected agents for changes before interaction or competitive analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent info lookups may fetch metadata from third-party URLs.

Mitigation: Use the skill only when outbound metadata requests are acceptable, and prefer restricted or opt-in metadata fetching before broad deployment.

Risk: Monitor mode stores baseline state in a shared /tmp cache path.

Mitigation: Avoid running monitor mode as root or on shared systems until the cache is moved to a private per-user directory.

Risk: Discovery queries are sent to the public Agentscan service.

Mitigation: Avoid submitting sensitive search terms or agent identifiers unless disclosure to Agentscan is acceptable.

## Reference(s):

- [Agentscan](https://agentscan.info)
- [Agentscan Agents API](https://agentscan.info/api/agents)
- [Agentscan Networks API](https://agentscan.info/api/networks)
- [ClawHub Skill Page](https://clawhub.ai/aetherstacey/skills/erc8004-discover)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Terminal text and Markdown instructions with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public API queries; monitor mode writes a local baseline cache under /tmp.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
