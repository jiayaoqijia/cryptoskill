## Description:

On-chain reputation for AI agents. Give feedback, check scores, view leaderboards, and build trust via the ERC-8004 Reputation Registry. Supports Base, Ethereum, Polygon, Monad, BNB.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aetherstacey](https://clawhub.ai/user/aetherstacey)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to inspect ERC-8004 reputation data, monitor feedback across supported chains, submit feedback, revoke prior feedback, and view reputation leaderboards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Write commands can sign and broadcast blockchain transactions using configured wallet secrets, spending gas and creating changes that may be hard to undo.

Mitigation: Review each transaction before execution, use a dedicated low-value wallet, and avoid exposing a primary mnemonic or private key to the runtime.

Risk: Leaderboard results come from third-party Agentscan data and may be stale, incomplete, or unavailable.

Mitigation: Treat leaderboard output as advisory and verify important reputation decisions against on-chain registry reads.

Risk: Unpinned dependencies and public RPC endpoints can change behavior or availability over time.

Mitigation: Install in an isolated virtual environment, prefer pinned and hashed dependencies, and review network endpoints before deployment.

## Reference(s):

- [ERC-8004 Specification](https://eips.ethereum.org/EIPS/eip-8004)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Agentscan](https://agentscan.info)
- [ClawHub Release Page](https://clawhub.ai/aetherstacey/skills/erc8004-reputation)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and CLI output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read operations query blockchain RPC endpoints; write operations can sign and broadcast blockchain transactions when wallet credentials are configured.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
