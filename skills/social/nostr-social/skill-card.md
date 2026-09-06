## Description: <br>
Gives an OpenClaw agent its own Nostr identity and Cashu ecash wallet for posting, messaging, following, zaps, profile management, and wallet interactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shawnyeager](https://clawhub.ai/user/shawnyeager) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to give an OpenClaw agent a self-sovereign Nostr social presence, local identity keys, and a Cashu/Lightning wallet. It supports setup, social posting, DMs, follows, reactions, zaps, wallet balance checks, invoices, and payment commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles identity keys and wallet seed material for a Nostr identity and Cashu wallet. <br>
Mitigation: Install only when the operator accepts local key and seed storage; back up the wallet seed securely and protect the local key and wallet files. <br>
Risk: The skill can publish posts, DMs, deletions, follows, and payment-related zap actions through third-party Nostr, Cashu, Lightning, and avatar services. <br>
Mitigation: Require explicit confirmation before posts, DMs, deletions, wallet sends, zaps, or relay/profile changes, and review the destination, amount, and message content before execution. <br>
Risk: The security assessment flags insufficiently clear confirmations and scoping around monitoring and public or payment-related actions. <br>
Mitigation: Constrain automated monitoring and autoresponse behavior to expected accounts and rate limits, and keep user review in the loop for public, private, and payment-affecting actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shawnyeager/skills/nostr-social) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local Nostr identity and Cashu wallet files during agent-directed setup.] <br>

## Skill Version(s): <br>
1.1.8 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
