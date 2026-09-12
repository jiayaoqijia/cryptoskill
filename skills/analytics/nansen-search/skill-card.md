## Description:

Search for tokens or entities by name. Use when you have a token name and need the full address, or want to find an entity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search Nansen for token or entity records by name, optionally filtering by type, chain, result limit, or output fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned npm CLI package and uses a Nansen API key at runtime.

Mitigation: Pin and verify the nansen-cli package before installation, and use a least-privilege or revocable Nansen API key.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nansen-devops/skills/nansen-general-search)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and concise search-result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the nansen CLI and NANSEN_API_KEY at runtime.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
