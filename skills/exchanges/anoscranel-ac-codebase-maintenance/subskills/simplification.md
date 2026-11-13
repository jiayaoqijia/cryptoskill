---
name: simplification
domain: software-engineering/simplification
trigger: "\"Simplify this\", \"this is too complicated\", \"reduce nesting\", \"remove dead code\", \"make this easier to read\", \"clean up this function\"."
anti_trigger: "Applying a named refactoring recipe such as Extract Class (subskills/refactoring.md); deciding which debt to pay (subskills/tech-debt.md); changing behaviour."
scope: "Cutting complexity in working code with behaviour unchanged; complexity measures"
status: "seedling"
---

# Simplification

## Standard

- **Complexity measures**: cyclomatic complexity (McCabe, IEEE TSE 1976) counts decision points; cognitive complexity (SonarSource, G. Ann Campbell, 2017) penalises nesting and broken flow.
- Single metrics link weakly to defects (Shepperd 2008). Use them as trends inside one codebase, not as absolute bars.
- **Deep modules** hide complexity behind simple interfaces (Ousterhout 2018).
- **YAGNI/KISS** (XP canon, Beck).
- Behaviour must stay the same. The test suite is the proof.

## Decision rules

1. Simplify only code covered by tests. No tests → write characterization tests first.
2. Remove before you rewrite: dead code, unused parameters, unreachable branches, stale flags, commented-out code.
3. Replace nesting with guard clauses and early returns.
4. Replace flag arguments with two named functions.
5. Replace hand-rolled loops with standard library calls when the result reads clearer.
6. Collapse speculative abstraction: an interface with one implementation, a factory that builds one type, a config option nobody sets.
7. Inline a helper that is used once and adds no name value.
8. Keep duplication until the third copy. Two similar blocks are often cheaper than a wrong abstraction.
9. Stop when the next change would alter behaviour or public interface.
10. Pick a cognitive-complexity number only as a review trigger, never as a merge gate. ⚠️ Any threshold (e.g. 15) is convention.

## Procedure

1. Measure before:
   ```bash
   radon cc -s -a src/          # Python cyclomatic
   lizard src/                  # many languages
   ```
 Or the cognitive score from your linter (e.g. SonarLint, `eslint-plugin-sonarjs`).
2. Run the full test suite. It must be green.
3. Find dead code: `vulture` (Python), `ts-prune` or `knip` (TS), compiler unused warnings. Delete it in its own commit.
4. Apply rules 3–7, one transformation per commit. Run tests after each.
5. Re-measure. Record before and after in the PR.
6. Read the result as a stranger. If it is not clearer, revert.
7. Check the public interface diff is empty.

## Anti-patterns

- "Simplifying" that adds layers.
- Clever one-liners that are harder to read.
- DRY applied to two coincidentally similar blocks.
- Changing behaviour in a cleanup PR.
- Chasing a metric number instead of reader clarity (Goodhart).
- Cleanup that grows into scope creep.

## Done checklist

- [ ] Tests green before and after every commit.
- [ ] Dead code removed in its own commit.
- [ ] Public interface unchanged.
- [ ] Before/after complexity recorded.
- [ ] A fresh reader finds it clearer.

## Sources

- <https://martinfowler.com/bliki/TechnicalDebtQuadrant.html>
- <https://www.iso.org/standard/78176.html>
- <https://senior-stack.uz/Roadmap/Programming/quality-engineering/engineering-metrics-and-dora/06-metrics-anti-patterns-and-goodhart/senior>
