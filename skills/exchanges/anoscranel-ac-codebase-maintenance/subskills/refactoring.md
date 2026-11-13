---
name: refactoring
domain: software-engineering/refactoring
trigger: "\"Refactor this\", \"extract this into a class\", \"move this method\", \"split this module safely\", \"add tests before refactoring legacy code\", \"strangler fig\"."
anti_trigger: "Free-form cleanup with no named recipe (subskills/simplification.md); choosing which debt to pay first (subskills/tech-debt.md); new behaviour."
scope: "Named refactorings in safe steps, under characterization tests"
status: "seedling"
---

# Refactoring

## Standard

- **Definition** (Fowler, *Refactoring*, 2nd ed., 2018): a change to internal structure that makes code easier to understand and cheaper to modify without changing observable behaviour. Small steps, each tested.
- **Catalogue**: https://refactoring.com/catalog/ (Extract Function, Inline Function, Move Function, Rename Variable, Extract Class, Replace Conditional with Polymorphism, Introduce Parameter Object, Split Phase…).
- **Characterization tests** (Feathers, *Working Effectively with Legacy Code*, 2004): record current behaviour before changing structure.
- **Strangler fig** (Fowler 2004): build the new beside the old and move traffic over gradually.
- Refactoring does not always improve quality attributes; effects vary (arXiv:1908.05399, 142 studies). Treat it as a targeted act.

## Decision rules

1. Either change behaviour or change structure. Never both in one commit.
2. No tests on the target → write characterization tests first, in a separate, earlier commit. Leave production code unchanged while doing so.
3. Use the IDE or language server's automated refactoring when available. It is safer than hand edits.
4. Opportunistic refactoring (while extending) is fine for small smells. Cross-cutting redesign gets its own planned PR.
5. A refactor branch that turns a test red it did not touch is a behaviour change. Stop and revert.
6. Tests change only by addition during a refactor. A modified assertion needs a reason in the commit.
7. Big rewrites use strangler fig, never big-bang.
8. A refactor that changes an architecturally significant decision needs an ADR.

## Procedure

1. Name the smell and the target recipe, e.g. "Long Function → Extract Function ×3".
2. Check coverage of the target: `pytest --cov=pkg.mod`, `vitest --coverage`, `go test -cover`.
3. If coverage is thin, write characterization tests:
   ```python
   def test_price_characterization():
       # Records current behaviour, including odd cases. Do not "fix" here.
       assert price(qty=0, tier="gold") == 0
       assert price(qty=3, tier="unknown") == 30.0
   ```
 For wide output, use golden-master (approval) files. Commit.
4. Apply one catalogue step. Run tests. Commit with `refactor:` prefix.
5. Repeat step 4 until the recipe is done.
6. For a strangler: put a routing seam (proxy, interface or flag) in front of the old code; build the new path; move one case at a time; delete the old path when no case uses it.
7. Run the full suite and the diff check: tests only added; public interface unchanged unless planned.
8. Open the PR labelled refactor-only.

## Anti-patterns

- "Refactor" PR that also fixes bugs.
- Refactoring code with no tests.
- Rewriting assertions to match new output.
- Big-bang rewrite with no rollback.
- Agent-applied refactor accepted without checking behaviour preservation.

## Done checklist

- [ ] Characterization tests committed first where coverage was thin.
- [ ] Each commit applies one named step and is green.
- [ ] No unexplained test changes.
- [ ] Behaviour unchanged; diff labelled refactor-only.
- [ ] ADR written if a significant decision changed.

## Sources

- <https://blog.paulserban.eu/booknote/refactoring-in-practice-a-deep-dive-into-fowler-becks-timeless-engineering-classic>
- <https://martinfowler.com/bliki/TechnicalDebtQuadrant.html>
- https://refactoring.com/catalog/ · https://arxiv.org/abs/1908.05399
