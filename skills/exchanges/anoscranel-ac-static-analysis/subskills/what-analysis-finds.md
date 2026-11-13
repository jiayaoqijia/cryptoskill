---
name: what-analysis-finds
domain: software-engineering/what-analysis-finds
trigger: "Understanding what a mechanical reader can and cannot detect."
anti_trigger: "Not for runtime behaviour, and not for security-specific analysis."
scope: "The shape of mechanically detectable problems."
status: seedling
---

# What analysis finds

## Standard

Static analysis detects patterns with a local, syntactic definition: an unused import, an unreachable branch, a name that shadows a builtin, a condition that repeats a previous one. It is strong exactly where the defect is visible in the code's own shape — where reading the text is enough — and weak where the defect lives in behaviour across time: a race, a protocol violation, a resource leak under a specific interleaving. No rule sees a network call fail.

The honest division of labour follows. Analysis catches the class of defect that is tiresome for a human to keep checking: the mechanical invariants, repeated hundreds of times, where attention fails first. Review and testing catch the class that needs judgement or execution. A team that expects analysis to find real bugs is disappointed; a team that lets it carry the mechanical invariants finds its review time goes where judgement pays.

Primary source: <https://martinfowler.com/>.

## Decision rules

- Classify candidate rules by what they find: mechanical invariant, structural smell, or probable bug.
- Expect high confidence from mechanical invariants and low from probable-bug heuristics.
- Record what the tool cannot see: types across untyped boundaries, runtime interleavings, external state.
- Treat each new rule's first weeks as calibration — its false positive rate decides its value.
- Prefer rules whose findings need no context to judge, and distrust rules whose findings always need discussion.
- Record the parser's blind spots for the language in use: macros, generated code, dynamic constructs.

## Procedure

1. Inventory the tool's rule set and classify each rule by finding type.
2. Estimate false-positive rate per rule from a sample of its findings.
3. Record the blind spots for the codebase's language features.
4. Sort rules by confidence and prepare the severity assignment from that order.
5. Drop or warn rules whose findings need context every time.
6. Record the classification and the tool's limits.

## Anti-patterns

- Enabling every rule in the box.
- Expecting analysis to replace review for behavioural defects.
- Treating a heuristic probable-bug rule as an invariant.
- Ignoring the tool's blind spots and trusting its silence there.
- Keeping a rule because it came enabled, when nobody acts on its findings.

## Done checklist

- [ ] Rules classified by finding type.
- [ ] False-positive rates sampled.
- [ ] Blind spots recorded.
- [ ] Severity assignment drafted from confidence.
- [ ] Context-dependent rules demoted or dropped.
- [ ] Classification recorded.

## Sources

- Static analysis practice: <https://martinfowler.com/articles/code-review.html>
- Linting and code quality: <https://martinfowler.com/bliki/CodeSmell.html>
- Compiler warning research: <https://dl.acm.org/>
