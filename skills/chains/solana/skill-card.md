## Description: <br>
Solana Dev Skill guides agents through Solana dApp, wallet, transaction, program, codegen, testing, and security work using framework-kit, @solana/kit, Anchor, Pinocchio, Codama, LiteSVM, Mollusk, and Surfpool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[h4rkl](https://clawhub.ai/user/h4rkl) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to plan and implement Solana application, wallet, transaction, on-chain program, client generation, testing, payment, and security tasks. It helps agents choose modern Solana tooling and produce implementation guidance, code, commands, and review notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pinocchio zero-copy pointer-cast examples may be unsafe if copied without validating Rust preconditions. <br>
Mitigation: Prefer field-by-field parsing, or explicitly verify unsafe Rust preconditions before using zero-copy pointer casts. <br>
Risk: Wallet, signing, payment, or mainnet-facing code can affect user funds or transaction authority. <br>
Mitigation: Review recipients, amounts, signers, fees, CPIs, token program variants, and confirmation behavior before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/h4rkl/skills/solana-dev-skill) <br>
- [Solana documentation](https://solana.com/docs) <br>
- [Solana Kit docs](https://solana.com/docs/clients/kit) <br>
- [framework-kit repository](https://github.com/solana-foundation/framework-kit) <br>
- [Anchor documentation](https://www.anchor-lang.com/) <br>
- [Pinocchio repository](https://github.com/anza-xyz/pinocchio) <br>
- [Codama repository](https://github.com/codama-idl/codama) <br>
- [Solana security best practices](https://solana.com/docs/programs/security) <br>
- [LiteSVM repository](https://github.com/LiteSVM/litesvm) <br>
- [Mollusk repository](https://github.com/buffalojoec/mollusk) <br>
- [Surfpool documentation](https://docs.surfpool.dev/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown responses with code snippets, shell commands, checklists, and file-level guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include risk notes for signing, fees, CPIs, token transfers, payments, and mainnet-facing changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
