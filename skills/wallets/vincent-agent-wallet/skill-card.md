## Description: <br>
Vincent helps agents create and use policy-controlled wallets for EVM transfers, swaps, smart-contract transactions, raw signing, and Polymarket activity without exposing private keys to the agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[piperwallet](https://clawhub.ai/user/piperwallet) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to provision agent wallets, store API access, check balances, transfer or swap tokens, execute EVM transactions, and operate Polymarket wallets under owner-defined policies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can receive broad ongoing authority to move funds, sign messages, and place prediction-market bets. <br>
Mitigation: Use a dedicated low-balance wallet, claim it immediately, and set spending limits, allowlists, and require-approval policies before funding it. <br>
Risk: API keys and re-link tokens can restore wallet access and should be treated as financial credentials. <br>
Mitigation: Store credentials securely, share re-link tokens only when needed, and rotate or re-link access if exposure is suspected. <br>
Risk: Raw signing and arbitrary contract calls can have effects that are hard for an agent to evaluate safely. <br>
Mitigation: Use raw signing or arbitrary contract calls only after personally verifying the target, chain, amount, calldata, and expected effect. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/piperwallet/skills/vincent-agent-wallet) <br>
- [Vincent wallet application](https://heyvincent.ai) <br>
- [Vincent wallet API](https://heyvincent.ai/api/secrets) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown with curl examples, JSON request bodies, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce wallet API usage steps, credential storage guidance, and policy setup recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
