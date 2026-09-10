## Description:

General purpose skill for using the Nostr Army Knife (nak) CLI tool with PTY support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samthomson](https://clawhub.ai/user/samthomson)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to query and post Nostr events with the nak CLI, including relay selection and PTY-wrapped command patterns for non-interactive environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private Nostr keys can be exposed through prompts, command history, logs, or transcripts when posting with nak.

Mitigation: Keep private keys out of prompts and logs, and prefer safer signer or credential-storage workflows when posting.

Risk: Shell-string command templates can be unsafe when relay, key, or other user-provided values are inserted into script -c commands.

Mitigation: Strictly validate and shell-escape user-provided relay and key values before command construction.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are expected to use a PTY wrapper for nak CLI execution.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
