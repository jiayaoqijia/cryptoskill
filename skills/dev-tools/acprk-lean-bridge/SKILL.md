---
name: lean-bridge
description: Connect paper propositions to Lean4/Mathlib theorems with a proposition-to-Lean-name table, a zero-sorry policy and an axiom audit. Use when formalising the algebraic core of a paper, when a reviewer questions a proof, or before claiming "machine-checked" anywhere. Covers Mathlib cache pitfalls and the lean-lsp MCP tools.
---
# lean-bridge: paper proposition ↔ Lean theorem

## Scope: what to formalise

Formalise the **finite algebraic core**: identities, support and character arguments,
counting bounds, injectivity and admissibility conditions, cost-ratio identities and
limits. Do **not** try to formalise lattice hardness, concrete noise distributions or
performance.

If a quantity is only *modelled*, say so in the table and in the paper. An example is a
noise bound taken as a definition rather than derived from ciphertext semantics. The
paper may then claim only "operation/level counts are machine-checked relative to the
model". It may **not** claim "noise growth is machine-checked".

## Procedure

1. Start from `lib/lean-template/`. Copy it and keep `lean-toolchain` and the Mathlib
   `rev` in sync.
2. **Run a numeric check first** (`skills/sage-check`). Never start formalising a
   statement that has not survived toy parameters.
3. For each proposition, write the Lean *statement* first, with the proof as a
   placeholder on a WIP branch. Get the statement reviewed against the paper text.
   Most mismatches are in the statement, not the proof. Common ones: the Lean version
   is weaker, uses ℕ where the paper needs ℤ, or adds a hypothesis the paper omits.
4. Prove it. Useful tactics: `decide` for tiny concrete finite facts; `ring`,
   `field_simp`, `linear_combination` for identities; `omega` for linear
   ℕ/ℤ arithmetic; `norm_num`, `simp` for evaluation. Avoid `native_decide`.
5. Fill in the **table**, which is kept in the Lean project README and mirrored in
   THEORY.md:

   | paper statement | Lean name (fully qualified) | file | modelling notes |
   |---|---|---|---|
   | Lemma 3.2 (support stability) | `Proj.Support.stable` | `Support.lean` | coefficient level |

6. **Gate** (all must pass before the table is cited in the paper):
   - `lake build` is green on a clean checkout at the recorded commit;
   - `scripts_check_no_sorry.sh` reports no `sorry`/`admit`/`axiom`/`native_decide`;
   - an axiom audit of every headline theorem (`#print axioms T` or `lean_verify`)
     shows only `propext`, `Classical.choice`, `Quot.sound`;
   - the table rows match the paper numbering on the final PDF.
7. Record the Lean commit and the "green build" log in EVIDENCE.md, for example
   "N results, zero sorry" as the printed fact and the `lake build` log as its source.

## Lessons

- Lean often **finds redundant or insufficient hypotheses**. Run
  `lean_minimal_hypotheses` on key theorems. Sometimes a hypothesis the paper states
  is not needed, which gives a stronger theorem. Sometimes the Lean proof needs one
  the paper forgot, which is a correctness fix. Report both to `theorist` and
  `falsifier`.
- Formalising the *coefficient-level* statement is usually much easier than the
  *polynomial-ring* statement. Prove a bridge lemma (for example, the coefficient of
  `P.comp (C a * X)`) once and reuse it.
- Keep each file under a few hundred lines, with one namespace per paper section.
- A cost-ratio "→ 2 as d → ∞" claim can be formalised with `Filter.Tendsto`. Pair it
  with an explicit finite bound, because reviewers care about concrete sizes.

## Mathlib cache pitfalls

See `lib/lean-template/README.md`. In short: match the toolchain and the Mathlib rev;
run `lake exe cache get` after every `lake update`; never `import Mathlib` in project
files; allow minutes for the first cold import; look up renamed lemmas with search
tools, not from memory.

## lean-lsp MCP tools (if configured)

| need | tool | tip |
|---|---|---|
| quick compile of a snippet | `lean_run_code` | self-contained with imports; the server needs `lake` on PATH |
| goal at a line | `lean_goal` | omit the column to see the state before and after the line |
| errors | `lean_diagnostic_messages` | "no goals to be solved" means delete tactics |
| lemma by name fragment | `lean_local_search` | use before guessing a name |
| lemma by meaning | `lean_leansearch` / `lean_leanfinder` | rate-limited |
| lemma by type | `lean_loogle` | rate-limited, a few calls per 30 s |
| try tactics | `lean_multi_attempt` | `["simp", "ring", "omega", "decide", "norm_num"]` |
| which hypotheses are needed | `lean_minimal_hypotheses` | |
| axiom audit | `lean_verify` | fully qualified name |
| after adding imports | `lean_build` | slow; `fetch_cache=true` only for missing oleans |
