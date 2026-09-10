## Description:

Assist with XRP transactions, destination tags, reserves, and XRPL features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users and developers use this skill for concise operational guidance on XRP transfers, destination tags, account reserves, trust lines, transaction outcomes, and common scams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe key-handling or delegated-signing guidance could lead users to expose signing authority or lose funds.

Mitigation: Treat XRP family seeds, secret keys, mnemonics, and delegated signing keys as highly sensitive, and verify security advice against current XRPL documentation before acting.

Risk: Incorrect transaction-finality or retry guidance could cause duplicate, failed, or misdirected payments.

Mitigation: Verify destination tags, reserve requirements, and transaction hashes in a validated ledger before retrying, replacing, or escalating a payment.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution or persistence; guidance should be reviewed before use with real XRP transfers.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
