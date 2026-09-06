## Description: <br>
On-chain reputation for AI agents. Give feedback, check scores, view leaderboards, and build trust via the ERC-8004 Reputation Registry. Supports Base, Ethereum, Polygon, Monad, BNB. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aetherstacey](https://clawhub.ai/user/aetherstacey) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to look up ERC-8004 reputation, give or revoke feedback, inspect feedback clients, and view reputation leaderboards across supported chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Write commands use wallet credentials and can send real blockchain transactions. <br>
Mitigation: Use a dedicated low-balance wallet, verify the chain, agent ID, target contract, tags, and gas estimate, and avoid putting main wallet credentials in shared shells, logs, CI, or long-lived agent environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aetherstacey/erc8004-reputation) <br>
- [ERC-8004 specification](https://eips.ethereum.org/EIPS/eip-8004) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and CLI text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read commands query public chain RPCs; write commands can submit blockchain transactions when wallet credentials are configured.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
