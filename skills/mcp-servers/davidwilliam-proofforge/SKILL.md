---
name: proofforge
description: Fix financial code in Lean 4 against a locked ProofForge specification and prove every requirement, checked by the ProofForge judge (six kernels, leanchecker, axiom audit, property tests) with a Passport as the result. Use when a task names a ProofForge task, a locked spec under spec/, candidate/Solution.lean, a requirement such as REQ-..., a Passport, or the proofforge MCP tools.
---

# ProofForge: fix, prove, check

A ProofForge task is a Lean 4 (v4.35, core library, no Mathlib) project with a locked
specification. The only file you change is `candidate/Solution.lean`. The task is done when
`check_candidate` returns `"status": "VERIFIED"`: every requirement proved, the proofs accepted
by six kernels, and the executable built from the same file passing the property tests. No proof,
no merge: a fix that compiles but leaves a requirement `sorry`, REFUTED or UNRESOLVED is not done.

## Tools (MCP server `proofforge`)

| Tool | Use | Cost |
|---|---|---|
| `prior_attempts` | only in a resumed run: what earlier attempts proved (re-checked by Lean against your current file, with a file that installs it all) and how they failed on the goals they left open | once, first |
| `show_task` | issue report, definitions under repair, every locked requirement (id, theorem, exact statement, plain-language text), the rules | instant |
| `goal_at` | the exact proof state at each `sorry` (or error, or a given line) of one declaration | seconds |
| `check_snippet_fast` | a lemma or proof attempt checked after the candidate on a persistent Lean session: errors, and the state at each `sorry` | seconds |
| `try_tactics` | a fixed portfolio of tactics on one theorem proved by `sorry`; returns the proof that closes it | seconds |
| `refute_statement` | a proposed helper statement evaluated on concrete values; FALSE comes with a kernel-checked counterexample | seconds |
| `search_library` | ProofForgeFin theorems, tactics and simp sets; pass `goal` (a statement or a declaration name) to rank by the goal's shape | instant |
| `try_snippet` | a full compile of a snippet after the candidate, without changing the file | a compile |
| `lean_build` | Lean's own output: `lake build Solution`, or `lake env lean <file>` for a scratch file; with the full toolset, also the required theorems the build proves and the best compiling version so far (`.proofforge/best.lean`) | a compile |
| `check_candidate` | the official check (`bin/proofforge check`): VERIFIED / REFUTED / UNRESOLVED per requirement, witnesses, kernel-checked counterexamples, Lean errors, sorry status, Passport | minutes |
| `verify_passport` | reproduce a Passport (`bin/proofforge verify`) | minutes |
| `list_tasks` | the task catalog | instant |

There is no local Lean installation in the shell; Lean runs through these tools. If a tool in
this table is not offered by the server, skip the step that uses it.

None of the tools edits `candidate/Solution.lean`; you write every change yourself. A tool that
finds a proof (`try_tactics`) or proved declarations (`prior_attempts`) gives you their text.

A response, its reasoning included, stops at an output limit of 32,000 tokens. A response cut
there is lost with everything it worked out, and a session can end after a few of them in a row.
Work out the next step only and act on it in the same response, with a tool call or an edit; write
a long proof as `have` steps ending in `sorry` and check them one at a time, rather than working
out the whole proof before the first call.

## Workflow

1. **Start from what is known.** In a resumed run, call `prior_attempts` first. Take the
   declarations it re-checked (paste them, or copy
   `.proofforge/prior-attempts/Solution-with-carried.lean` over the candidate when you want them
   all), and read its failure notes: do not repeat an approach that already failed on a goal.
2. **Read the locked spec.** Call `show_task`, then read `spec/<Lib>/Spec.lean` (the requirement
   predicates), `spec/<Lib>/Challenge.lean` (the definitions under repair and the required
   theorems, each `:= sorry`) and `spec/<Lib>/Lemmas.lean` if present. The theorem statements in
   `Challenge.lean` are what the judge compares, byte for byte after elaboration.
3. **Check, to find the defect.** Run `check_candidate` on the starting file. Each REFUTED
   requirement comes with a witness (an input, the output, the violated requirement) and a
   counterexample: the negation of the locked statement proved about the current code by the
   kernel. That input is the bug. Fix the definition so the witness no longer violates the
   requirement; do not weaken behavior on valid inputs (requirements that demand success still
   have to hold).
4. **Write the fix in the specification's terms.** When the specification states the result of a
   call in closed form (`s' = { s with ... }` built from its own definitions: an index update, a
   start, a credit), write that call of the fixed definition as
   `if <the requirement's preconditions> then some <that closed form> else none`, with the
   specification's definitions wherever the code computes the same quantity and the corrected
   condition where the bug was. The effect requirements are then `simp only [impl] at h` and
   `split at h`, the success requirement is the precondition, and a requirement over sequences of
   calls rewrites each call with the same equation. A line-by-line port of the deployed code
   (`Option` binds, checked subtraction, local `let`s, two-phase updates) needs, before any
   requirement, one equation lemma per call (`impl s c = if ok then some next else none`) proved
   by unfolding and case splits, and every later proof goes through it; keep the port only if
   you prove those equations first, one call at a time.
5. **Decompose.** Put each required theorem in the file with its locked statement and `sorry`,
   and the helper lemmas you plan to use above it, each `:= by sorry`. Compile with `lean_build`.
   Before you spend effort on a helper, run `refute_statement` on it (by `name`, or pass a
   `statement` before writing it), above all for inequalities with subtraction, division, rounding
   or scaling and for claims about every input. A FALSE result gives the values that break it:
   add the missing hypothesis or fix the bound, and sample it again.
6. **Bank the short requirements first.** Once the fixed definition compiles, run `try_tactics`
   on every required theorem, and prove the ones that follow directly from the definitions, from
   the locked lemmas or from another requirement (a bound given by the routine's last step, an
   equality with the deployed algorithm, a consequence of a requirement already proved) before
   starting a long proof. A long proof can outlast the budget; the requirements already proved
   are kept.
7. **Prove, cheapest first.** For each open theorem, helpers first:
   - `try_tactics` on it. If a tactic closes it, put the returned proof in the file.
   - Otherwise `goal_at` to see the exact hypotheses and goal at each `sorry`; then
     `search_library` with `goal` set to the theorem's name for lemmas whose conclusion fits.
     `import ProofForgeFin` (or one module) is allowed and its declarations are checked by the
     same kernels. The library's `lib_defs` tactic rewrites definitions that match ProofForgeFin
     definitions (and sums restated by recursion) into the library's, so its lemmas apply.
   - Write the proof in steps with `have h : P := by sorry` and iterate with
     `check_snippet_fast` (seconds) until it has no error; then `try_snippet` (a full compile)
     and put it in the file. Break a step that resists into a new helper and go back to step 5.
   - When a library module fits the argument (its doc ends with "Using the module", as
     `ProofForgeFin.Accumulator.Market` does for reward indices over runs of operations), follow
     that recipe step by step: it names the lemma for each step and the bridges from the
     specification's definitions to the library's, most of them by `rfl`.
8. **Keep the file compiling.** Move a proof into `candidate/Solution.lean` only once it compiles
   as a snippet, and run `lean_build` after every edit of the file. Where `lean_build` keeps the
   best compiling version as `.proofforge/best.lean`, restore it
   (`cp .proofforge/best.lean candidate/Solution.lean`) when an edit breaks the file and the error
   is not a quick fix. `#print axioms` in a scratch file that imports `Solution` shows which
   theorems still depend on `sorryAx`. Fix a failed build from its first error; later errors
   often follow from it. From the third failed build in a row `lean_build` names the declarations
   with errors: put `sorry` in place of their proofs so that the file compiles, and work each out
   with `check_snippet_fast`.
9. **Check and iterate.** `check_candidate`. A new witness or counterexample means the behavior
   is still wrong: go back to step 3 with it. `lean_errors` and `theorem_status` show what is
   not proved; `proof_check.reasons` names scan violations or a Comparator rejection (a statement
   that differs from the lock, a forbidden axiom, a kernel that rejects a declaration).
10. **Done.** Stop only at `"status": "VERIFIED"`. Report the Passport path and `passport_sha256`;
   `verify_passport` reproduces it.

## Rules the judge enforces

- Files under `spec/`, `app/`, `lakefile.toml`, `lake-manifest.json` and `lean-toolchain` are
  locked; the judge uses the repository's copies and rejects a workspace whose copies differ.
- Imports: the task's `Spec` and `Lemmas`, `Init.*`, `Std.*`, `ProofForgeFin.*`.
- Forbidden in the candidate: `sorry`, `axiom`, `opaque`, `implemented_by`, `extern`, `unsafe`,
  `@[export]`, `@[csimp]`, `macro`, `elab`, `syntax`, `initialize`, `#eval`, `run_cmd`,
  `native_decide`, `set_option`, simprocs and any other elaboration-time code.
- Permitted axioms: `propext`, `Quot.sound`, `Classical.choice`.
- At a literal scale such as `10 ^ 18` or `10 ^ 36`, prove arithmetic over a variable scale and
  instantiate it: two of the six kernels unfold literal powers in equations Lean's kernel accepts.

## Lean 4.35 notes

- `omega` handles linear arithmetic over `Nat` and `Int` with literals; it does not see through
  definitions: `simp only [f]` or `unfold f` first.
- Nonlinear facts (`a * b / c` bounds): `Nat.div_le_div_right`, `Nat.mul_le_mul`,
  `Nat.div_mul_le_self`, `Nat.lt_div_mul_add`, or the library's `ceilDiv` and fixed-point lemmas.
- `split`, `cases h : e`, `by_cases`, `match` on the shape of the definition keep goals small;
  `simp_all` on a large state is slow and brittle.
- `decide` is fine on small closed propositions; `native_decide` is rejected.
- Mathlib tactics do not exist here: `by_contra` (use `apply Classical.byContradiction` then
  `intro h`, or `by_cases`), `set` (`generalize hx : e = x`), `ring` and `ring_nf` (`grind`, or
  `Nat.mul_comm`, `Nat.mul_assoc`, `Nat.mul_add` rewrites and `ac_rfl`), `linarith` (`omega`),
  `interval_cases` (a case split, then `omega`), `norm_num` (`decide`, `simp`, `omega`),
  `push_neg` (`Nat.not_lt`, `Nat.not_le`, `Classical.not_not`), `positivity` (`Nat.mul_pos`,
  `Nat.pow_pos`). A file that uses one does not compile.
