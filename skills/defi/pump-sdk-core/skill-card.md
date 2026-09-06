## Description: <br>
Build and extend the core Pump SDK, an offline-first TypeScript SDK that constructs Solana TransactionInstructions for token creation, buying, selling, migration, and creator fee collection across Pump, PumpAMM, PumpFees, and Mayhem programs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[speraxos](https://clawhub.ai/user/speraxos) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to build, extend, and maintain TypeScript SDK code that creates Solana transaction instructions and decodes Pump protocol account state. It supports instruction-builder patterns for token creation, buying, selling, migration, creator fee collection, and safe account validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated or edited Solana instruction code could be incorrect before transaction signing or broadcasting. <br>
Mitigation: Review generated instructions and transaction-building code before signing or broadcasting. <br>
Risk: RPC URLs may include provider credentials. <br>
Mitigation: Treat SOLANA_RPC_URL and any embedded provider tokens as sensitive; avoid logging or committing them. <br>


## Reference(s): <br>
- [Pump SDK repository homepage](https://github.com/nirholas/pump-fun-sdk) <br>
- [ClawHub skill page](https://clawhub.ai/speraxos/pump-sdk-core) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with TypeScript code and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference SOLANA_RPC_URL for online SDK workflows; review generated Solana instruction code before signing or broadcasting transactions.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
