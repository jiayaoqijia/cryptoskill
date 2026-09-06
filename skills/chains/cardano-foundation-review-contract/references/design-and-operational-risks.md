# Design and Operational Risks

Five concerns that surface during a Cardano smart contract review but are **not
vulnerabilities**. No canonical vulnerability catalogue — the Cardano Developer Portal's
database, Plutonomicon, MLabs — treats any of them as an attack class.

Report these as observations, not findings. Give them a severity only if you can
demonstrate a concrete exploit, in which case the finding belongs under whichever
vulnerability class it actually falls into. Presenting an engineering smell as a
security finding is the fastest way to lose a reader's trust in the rest of the report.

Exploit classes live in `vulnerability-checklist.md`, referenced below as
"vulnerability checklist #N".

## 1. Hardcoded Addresses

**Risk**: Informational — engineering concern, not an exploit class
**Applies to**: All script types

**Description**: Script hashes, policy IDs, or key hashes written as literals in the
validator source. This makes the same source unusable across networks and forces a
source edit for any change of counterparty. No canonical vulnerability catalogue lists
it as an attack — report it as a maintainability finding.

Note what parameterization does *not* buy you: parameters are baked into the compiled
code, so applying a different parameter produces a different script hash exactly as
editing a constant would. Neither approach enables upgrade or migration. Only
indirection through a datum or config UTxO gives post-deployment mutability.

**Detection**: Search for literal hex strings and address constants in validator source.

**Mitigation**: Pass addresses and policy IDs as validator parameters applied at
deployment, and where values must change after deployment, read them from a config
UTxO. Two caveats to carry into the review:

- On-chain code cannot verify that a given script hash corresponds to a *properly
  instantiated* parameterized script. An attacker-instantiated variant has an equally
  valid-looking hash, so anything that accepts a script hash from untrusted input must
  pin it (see #3).
- A config datum is worthless unless authenticated. Read it from a reference input
  carrying a one-shot NFT (vulnerability checklist #14), or you have traded a hardcoded constant for
  attacker-chosen configuration.

**Sources**: [Plutonomicon — Parameterization](https://plutonomicon.github.io/plutonomicon/vulnerabilities),
[Aiken — Validators and parameters](https://aiken-lang.org/language-tour/validators),
[Vacuumlabs vulnerability checklist #3 — Trust No UTxO](https://medium.com/@vacuumlabs_auditing/cardano-vulnerabilities-3-trust-no-utxo-b252650ac2b9)

## 2. Collateral and Failure-Mode Assumptions

**Risk**: Informational — operational concern
**Applies to**: All script types

**Description**: Collateral is forfeited **only** when a transaction is accepted into a
block with its scripts failing phase-2 validation. If chain state changed so that an
input no longer exists, the transaction fails **phase 1** and is rejected outright:
no fee, no collateral. The official documentation is explicit — "if the on-chain
conditions have changed since the transaction was constructed, that transaction will be
rejected entirely, and no fees will be charged", and "an honest user is never at risk of
losing their collateral".

Because Plutus evaluation is deterministic over a fixed transaction, a user whose
tooling evaluates scripts locally before signing can predict phase-2 success and
therefore cannot lose collateral. An attacker front-running a UTxO does **not** cause
collateral loss.

Collateral griefing is a widespread misconception, and a report claiming it will not
survive review. Treat this as an operational checklist item.

**Detection**: Check that off-chain flows evaluate scripts locally before signing (all
mainstream SDKs do by default — flag anything that skips or stubs evaluation). Check
that transactions set a collateral return output and `totalCollateral`.

**Mitigation**: Rely on local script evaluation before submission. Set a collateral
return output so that at most the required percentage of the fee is ever at risk rather
than the whole collateral UTxO. The genuine griefing vectors in this neighbourhood are
UTxO contention causing phase-1 failures and wasted user effort (vulnerability checklist #12), and
always-failing scripts leaving funds permanently unspendable (vulnerability checklist #27) — report those under
their own entries.

**Sources**: [Cardano docs — Collateral mechanism](https://docs.cardano.org/about-cardano/learn/collateral-mechanism),
[IOG — No-surprises transaction validation, part 2](https://www.iog.io/blog/posts/2021/09/07/no-surprises-transaction-validation-part-2/),
[Plutonomicon — EUTXO Concurrency DoS](https://plutonomicon.github.io/plutonomicon/vulnerabilities)

## 3. Script Hash Mismatch

**Risk**: Medium — deployment concern with security consequences
**Applies to**: Multi-validator setups

**Description**: When scripts reference each other by hash, changing one changes its
hash and breaks every reference to it. The outcomes worth reporting are concrete:
funds permanently locked because a validator demands a counterpart hash no deployed
script has, or a deployment wired to the *wrong* script — which, if an attacker can
influence which hash is injected, is a genuine exploit.

There is a structural constraint here: two scripts **cannot** both be parameterized by
each other's hash, since a script's hash depends on its parameters. Cross-references
must form a directed acyclic graph.

**Detection**: Search for script hashes used as parameters or in cross-script checks.
Verify the build injects hashes in dependency order, and that the graph is acyclic.

**Mitigation**: Inject cross-references as parameters at deployment and automate hash
computation in the build. Where the dependency is genuinely mutual, use one of the
documented escapes: a multi-purpose validator (one script, one hash, several purposes),
withdraw-zero forwarding so only one direction is compiled in (vulnerability checklist #13), or passing hashes
through an authenticated config datum read as a reference input (vulnerability checklist #14). Add a
deployment-time check that compares on-chain deployed hashes against locally recomputed
ones *before* any funds move.

**Sources**: [Anastasia Labs — Stake validator pattern](https://github.com/Anastasia-Labs/design-patterns/blob/main/stake-validator/STAKE-VALIDATOR.md),
[CIP-112 — Observe script type](https://cips.cardano.org/cip/CIP-0112),
[Plutonomicon — Parameterization](https://plutonomicon.github.io/plutonomicon/vulnerabilities)

## 4. Plutus Version Confusion

**Risk**: Low — compatibility concern
**Applies to**: Plutus/Plinth and Plutarch projects, legacy compiled artifacts

**Description**: Mixing ledger language versions without understanding what each can
see. V1 scripts do not receive reference inputs in their script context, so they cannot
validate against them, and V1 scripts still fail when their spent inputs carry inline
datums. Cost models differ per version.

A transaction containing reference inputs does **not** fail merely for carrying a V1
script: CIP-0110 relaxed that rule at the Chang hard fork (September 2024), and the V1
script runs with a context that simply excludes them. Protocol version 11 revised the
V1/V2 reference-input predicates further and unified built-ins across versions. Older
material describing the stricter rule is stale.

**Detection**: This does not apply to current Aiken projects: Aiken never targeted V1,
and since v1.1.10 `aiken.toml` rejects `v1` and `v2` entirely — current Aiken emits V3.
For Haskell/Plutarch code, check the ledger language in the build config and in the
deployed script envelope (`PlutusScriptV1` / `V2` / `V3`).

**Mitigation**: Use Plutus V3 for new development. When integrating with existing V1
contracts — older DEXes, legacy deployments — know that your transaction *may* now
include reference inputs, but the V1 script will not see them, and inline datums on its
spent inputs remain fatal. Test against the actual deployed version.

**Sources**: [Plutus — Ledger language version](https://plutus.cardano.intersectmbo.org/docs/working-with-scripts/ledger-language-version),
[CIP-0110](https://cips.cardano.org/cip/CIP-0110),
[Aiken CHANGELOG](https://github.com/aiken-lang/aiken/blob/main/CHANGELOG.md)

## 5. Redeemer Size Bloat

**Risk**: Informational — efficiency concern, not an exploit class
**Applies to**: All script types

**Description**: Large redeemers increase fees and consume transaction size. No
canonical vulnerability catalogue lists this as an attack class, and for good reason:
the redeemer is chosen by whoever submits the transaction, so the cost is
self-inflicted rather than something a third party imposes on your users.

The one security-adjacent case is a validator *design* that forces every spender to
supply large redeemer data — full merkle proofs, copies of datums — which can push a
spend path against the hard limits and brick it. That belongs under the general
unbounded-data weakness (vulnerability checklist #3, vulnerability checklist #22) rather than here.

**Detection**: Check redeemer type definitions for large or unbounded structures and
estimate serialized size for typical operations.

**Mitigation**: Keep redeemers small; prefer enum-style redeemers. Pass indices rather
than copies of data the validator can find itself (vulnerability checklist #17). Move bulk data to reference
inputs.

**Sources**: [Anastasia Labs — Enum redeemers and UTxO indexers](https://github.com/Anastasia-Labs/design-patterns),
[CIP-31 — Reference inputs](https://cips.cardano.org/cip/CIP-31)

---

## Quick reference

| # | Concern | Nature | Applies to |
|---|---|---|---|
| 1 | Hardcoded Addresses | engineering concern, not an exploit class | All |
| 2 | Collateral and Failure-Mode Assumptions | operational concern | All |
| 3 | Script Hash Mismatch | deployment concern with security consequences | Multi-validator |
| 4 | Plutus Version Confusion | compatibility concern | Plutus/Plutarch |
| 5 | Redeemer Size Bloat | efficiency concern, not an exploit class | All |
