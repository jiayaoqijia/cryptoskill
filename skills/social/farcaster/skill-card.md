## Description:

Post, read, search, and engage on Farcaster via the Neynar API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openclaw-consensus-bot](https://clawhub.ai/user/openclaw-consensus-bot)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to read Farcaster data and perform account actions such as posting casts, replying, reacting, deleting casts, searching casts, and looking up users or channels through Neynar.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Neynar API key and signer UUID that can act on a Farcaster account.

Mitigation: Store credentials in protected environment variables or a secret store; avoid passing secrets on the command line.

Risk: The documented eval credential-loading pattern can execute shell text derived from a JSON file.

Mitigation: Avoid that pattern and load credentials through a trusted secret manager or manually exported environment variables.

Risk: Posting, reacting, following, and deleting casts can create public or destructive account changes.

Mitigation: Require explicit confirmation before write actions and treat cast deletion as irreversible unless recovery is available outside this skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openclaw-consensus-bot/skills/farcaster-skill)
- [Neynar v2 API endpoint reference](references/neynar_endpoints.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, python3, NEYNAR_API_KEY, and NEYNAR_SIGNER_UUID for write operations.]

## Skill Version(s):

1.0.1 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
