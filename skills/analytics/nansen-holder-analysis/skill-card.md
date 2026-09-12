## Description:

Is this token held by quality wallets or retail noise? SM holder ratio, flow breakdown by label, and recent buyer quality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and crypto analysts use this skill to inspect token holder quality with Nansen CLI data, including smart-money holders, wallet-label flow breakdowns, and recent buyer or seller quality signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an npm-distributed nansen-cli package and requires a Nansen API key.

Mitigation: Install only a trusted or reviewed CLI version, prefer pinning where possible, and scope and rotate the NANSEN_API_KEY according to normal credential practices.

Risk: Holder analysis excludes native and wrapped tokens when using the holders endpoint.

Mitigation: Use a specific token contract address and avoid applying holder endpoint output to unsupported native or wrapped token cases.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nansen-devops/skills/nansen-holder-analysis)
- [Nansen DevOps publisher profile](https://clawhub.ai/user/nansen-devops)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks and concise analysis guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NANSEN_API_KEY and the nansen CLI; holder analysis must use a specific token contract address.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
