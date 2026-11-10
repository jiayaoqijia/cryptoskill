## Description:

Search for tokens or entities by name. Use when you have a token name and need the full address, or want to find an entity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts can search for a token or entity by name to find matching details such as a token address, name, symbol, or chain.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A supported HTTP 402 response can trigger a payment from the configured wallet, and repeated searches can each incur a charge.

Mitigation: Review the wallet authorization, payment policy, and spending limits before searching; keep repeated calls within the intended scope.

## Reference(s):

- [Browser login platform scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)

## Skill Output:

**Output Type(s):** [Text, Shell commands]

**Output Format:** [CLI search results with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Result count and fields depend on the query options.]

## Skill Version(s):

0.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
