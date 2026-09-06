## Description: <br>
Set up an lnd remote signer container that holds private keys separately from the agent. Exports a credentials bundle (accounts JSON, TLS cert, admin macaroon) for watch-only litd nodes. Container-first with Docker, native fallback. Use when firewalling private key material from AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Roasbeef](https://clawhub.ai/user/Roasbeef) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to set up a separated Lightning lnd remote signer for watch-only agent nodes, keeping private key material on a dedicated signer machine while exporting the credentials needed for watch-only operation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The exported bundle contains an admin macaroon and signer connection material that could authorize sensitive signer access if mishandled. <br>
Mitigation: Replace the admin macaroon with a scoped signer-only macaroon for production and avoid transferring the base64 bundle through chats or logs. <br>
Risk: The signer exposes RPC and REST services on ports 10012 and 10013 for watch-only node access. <br>
Mitigation: Firewall ports 10012 and 10013 so only the intended watch-only node can reach them, and use testnet before handling mainnet funds. <br>
Risk: The signer stores seed and wallet password files on the signer machine. <br>
Mitigation: Run the signer on dedicated or hardened hardware and secure or remove stored seed and wallet password files after setup. <br>
Risk: External helper scripts and source-build paths can pull or run third-party software. <br>
Mitigation: Inspect external helper scripts and dependencies before execution, especially before using real funds. <br>


## Reference(s): <br>
- [Remote Signer Architecture](references/architecture.md) <br>
- [Lightning Network lnd repository](https://github.com/lightningnetwork/lnd.git) <br>
- [ClawHub skill page](https://clawhub.ai/Roasbeef/lightning-security-module) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and configuration file references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup, start, stop, export, and hardening guidance for a remote Lightning signer workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
