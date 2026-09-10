## Description:

Build and sign XRP Ledger transactions. Use for: (1) Creating payment transactions, (2) Building NFT mint/burn transactions, (3) Signing with Xaman wallet, (4) Submitting to XRPL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harleyscodes](https://clawhub.ai/user/harleyscodes)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to draft XRPL payment and NFT transaction examples, integrate Xaman-signed submission flows, and review key XRPL transaction fields before implementation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real XRPL transaction submission can affect live wallets if users apply examples without enough safety checks.

Mitigation: Prefer testnet or devnet during development and confirm destination, amount, network, fees, and full transaction contents before submitting any signed transaction.

Risk: A likely incorrect transaction example could mislead implementation.

Mitigation: Independently verify every transaction type and field against XRPL documentation before adapting the example.

Risk: The skill depends on the `xrpl` package for transaction construction and submission examples.

Mitigation: Pin and audit the `xrpl` dependency before using the skill in wallet-connected workflows.

## Reference(s):


## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance, API Calls]

**Output Format:** [Markdown with bash and TypeScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes XRPL transaction examples and public RPC endpoint guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
