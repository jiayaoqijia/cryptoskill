## Description: <br>
Complete Bittensor SDK reference for Subtensor, AsyncSubtensor, Metagraph, Axon, Dendrite, Synapse, chain data models, extrinsics, extras, and utilities used in Bittensor wallet, staking, subnet, registration, liquidity, proxy, coldkey swap, and weight-setting workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[taoleeh](https://clawhub.ai/user/taoleeh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill as Bittensor SDK reference material for building, reviewing, and operating agents or applications that query Bittensor networks, manage wallets, stake, register neurons, set weights, and perform chain operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill covers wallet-signing and administrator blockchain actions, including staking, registration, proxy changes, coldkey swaps, sudo/root operations, and other financial-authority workflows. <br>
Mitigation: Treat transaction-building suggestions as high risk and verify the network, wallet, destination addresses, amounts, coldkey or proxy changes, and sudo/root calls before signing. <br>
Risk: Documentation examples may lead an agent toward live chain operations without strong scoping or safety warnings. <br>
Mitigation: Prefer read-only queries, testnet execution, dry-run checks, or explicit human approval before any live transaction or wallet mutation. <br>
Risk: The skill may involve sensitive wallet material or credentials. <br>
Mitigation: Do not expose coldkeys, hotkeys, seed phrases, private keys, wallet files, or signing credentials to the agent; sign only through trusted local wallet flows. <br>


## Reference(s): <br>
- [Bittensor SDK skill page](https://clawhub.ai/taoleeh/bittensor-sdk) <br>
- [Publisher profile](https://clawhub.ai/user/taoleeh) <br>
- [Bittensor Docs](https://docs.bittensor.com/) <br>
- [Bittensor SDK Reference](https://bittensor-sdk.readthedocs.io/) <br>
- [Learn Bittensor](https://docs.learnbittensor.org/) <br>
- [Bittensor GitHub](https://github.com/opentensor) <br>
- [Publisher website](https://bittensor.quest) <br>
- [Full autoapi reference](references/autoapi/index.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline Python and shell code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only reference output; any transaction-building guidance requires user review before signing.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
