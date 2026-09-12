## Description:

Financial capability for AI entities -- pay Lightning invoices, check balance, create invoices via Nostr Wallet Connect (NIP-47).

This skill is ready for commercial/non-commercial use.

## Publisher:

[vveerrgg](https://clawhub.ai/user/vveerrgg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to give agents scoped Lightning wallet capabilities through Nostr Wallet Connect, including checking balances, paying invoices, creating invoices, and reviewing transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move real Lightning funds through an NWC wallet connection.

Mitigation: Use only scoped, revocable NWC connections with low balances, wallet-side spending limits, and only the NIP-47 methods needed.

Risk: An agent could pay an invoice without sufficient human review.

Mitigation: Require explicit user approval for the exact invoice, amount, recipient or context, and purpose before any payment.

Risk: The NWC connection string authorizes wallet actions if exposed.

Mitigation: Store NWC_CONNECTION_STRING only as a secret, never in source code or logs.

Risk: The install path may pull dependencies without production pinning.

Mitigation: Review and pin dependencies before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vveerrgg/skills/nostrwalletconnect)
- [ClawHub publisher profile](https://clawhub.ai/user/vveerrgg)
- [OpenClaw homepage metadata](https://github.com/HumanjavaEnterprises/nwc.app.OC-python.src)
- [PyPI package](https://pypi.org/project/nostrwalletconnect/)
- [NostrKey prerequisite skill](https://clawhub.ai/vveerrgg/nostrkey)
- [NSE integration reference](https://clawhub.ai/vveerrgg/nse)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an NWC connection string and async Python usage.]

## Skill Version(s):

0.1.4 (source: frontmatter, artifact metadata, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
