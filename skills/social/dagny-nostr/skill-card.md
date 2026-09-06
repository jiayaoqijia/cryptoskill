## Description: <br>
Dagny Nostr (nak) guides an agent in using the nak CLI to publish notes, reply in threads, check replies or mentions, monitor Nostr relays, and sign publishing actions with NOSTR_SECRET_KEY. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardbickerton](https://clawhub.ai/user/edwardbickerton) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and agents use this skill to create Nostr posts, reply with correct thread tags, inspect replies or mentions, and manage relay interactions through nak CLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The nak install path uses a remote script that can change over time. <br>
Mitigation: Review the install script before execution or use a pinned/package-manager install when available. <br>
Risk: NOSTR_SECRET_KEY exposure can compromise the signing identity used for publishing. <br>
Mitigation: Use a dedicated automation key and keep NOSTR_SECRET_KEY out of chats, logs, shell history, screenshots, and repositories. <br>
Risk: Published Nostr events may be public and durable across relays. <br>
Mitigation: Review content, relay targets, and tags before publishing, and assume posted events can remain publicly accessible. <br>


## Reference(s): <br>
- [nak GitHub repository](https://github.com/fiatjaf/nak) <br>
- [nak install script](https://raw.githubusercontent.com/fiatjaf/nak/master/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Nostr relay URLs, event IDs, public keys, and environment-variable references; secret key values should not be exposed.] <br>

## Skill Version(s): <br>
0.1.4 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
