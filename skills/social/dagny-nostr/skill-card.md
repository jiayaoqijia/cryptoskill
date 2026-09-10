## Description:

Manage Nostr posting and engagement via the nak CLI, including publishing signed notes, replying with correct threading tags, tagging users, checking replies or mentions, and monitoring relays.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardbickerton](https://clawhub.ai/user/edwardbickerton)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to guide an agent through Nostr posting workflows with nak, including publishing signed notes, replying with root/reply tags, tagging users, and checking replies or mentions on a relay.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to install nak through an unverified remote shell script.

Mitigation: Review the installer before execution and prefer a pinned release or verified package when available.

Risk: NOSTR_SECRET_KEY or nsec exposure can allow account takeover.

Mitigation: Keep signing secrets out of prompts, command history, and logs; use environment variables or restricted local files for storage.

Risk: Nostr posts, tags, relay choices, and event IDs may be public and difficult to remove.

Mitigation: Review content, recipients, tags, and relays before publishing; avoid posting secrets or private information.

## Reference(s):

- [nak CLI repository](https://github.com/fiatjaf/nak)
- [nak install script](https://raw.githubusercontent.com/fiatjaf/nak/master/install.sh)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include nak CLI commands, relay URLs, event identifiers, public keys, and environment variable references for signing.]

## Skill Version(s):

0.1.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
