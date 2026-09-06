## Description: <br>
ERC-8004 Trustless Agents - Register and manage AI agent identities on TRON and BSC blockchains with on-chain reputation tracking <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SpyderJR](https://clawhub.ai/user/SpyderJR) <br>

### License/Terms of Use: <br>
CC0-1.0 <br>


## Use Case: <br>
Developers and engineers use this skill to register, query, update, and submit feedback for AI agent identities on TRON and BSC networks using ERC-8004/TRC-8004 registries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use wallet private keys to sign irreversible TRON or BSC transactions. <br>
Mitigation: Use a dedicated low-balance wallet, start on testnets, and require explicit approval before any register, feedback, or set-uri command on mainnet. <br>
Risk: Persistent plaintext private key storage can expose wallet funds if the host is compromised. <br>
Mitigation: Avoid storing private keys in shell startup files or plaintext wallet files; prefer scoped environment variables or a managed secret store. <br>
Risk: Wrong or spoofed contract addresses could route transactions to unintended contracts. <br>
Mitigation: Verify contract addresses independently before mainnet use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SpyderJR/8004-skill) <br>
- [EIP-8004 specification](https://eips.ethereum.org/EIPS/eip-8004) <br>
- [8004.org](https://8004.org) <br>
- [TRON Developers documentation](https://developers.tron.network/) <br>
- [TronWeb JavaScript SDK](https://github.com/tronprotocol/tronweb) <br>
- [TronScan](https://tronscan.org/) <br>
- [TronGrid API service](https://www.trongrid.io/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce commands that read wallet private keys and submit TRON or BSC transactions.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
