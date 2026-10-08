---
name: teach-a-tool-by-its-failure-modes
description: Use when introducing a tool like git, docker, or a package manager. Teaches it through its three most common errors and the mental model each reveals, rather than listing flags, so the learner can diagnose instead of memorise.
---

# Teach a Tool by Its Failure Modes

A flag cheat-sheet is forgotten by lunch. A tool's three most common errors, each tied to the mental model it exposes, gives the learner diagnosis instead of recall.

## Procedure

1. Pick the three errors a beginner actually hits, in order. For git: detached HEAD, merge conflict, and pushed-then-amended history.
2. For each, reproduce it on purpose in a scratch clone: `git clone /tmp/tools-demo && cd tools-demo && git checkout HEAD~1`.
3. Decode the message literally, then name the model it assumes: "detached HEAD means commits here are not on a branch".
4. Give the safe recovery command and say who it affects: `git switch -` returns to the branch, and nothing is lost if you had not committed.
5. Mark which errors are one-way (rewriting shared history) versus reversible, because fear is what stalls learners.
6. Close each with a "you will know this is happening when..." tell, so they recognise it next time.
7. Leave the scratch repo path `/tmp/tools-demo` so they can break it freely.
8. Have them break it deliberately and recover before you move to the next mode.
9. Write the three tells on one card they can keep; recall of the tell is the point, not the flag list.
10. Ask the learner to cause each error themselves before you explain it.
11. Keep the scratch repo disposable and note the one command that recreates it.
12. Map each error to the docs page that explains it, so the learner can go deeper.
13. Sequence the three errors from most to least common.
14. End by showing where the docs explain each error.
15. Quiz the tell, not the flag, at the end.

## Pitfalls

- A command list with no failure context, remembered for a day.
- Teaching the recovery without the model, so the next variant still stumps them.
- Hiding the dangerous cases, so the learner treats all commands as equally safe.
- Using a shared repo for the deliberate breakage.
- Explaining all flags of one subcommand instead of the errors of the tool as a whole.
- Demoing on a clean repo where the error never actually appears.
- Choosing exotic errors when the common ones are the real time sinks.
- Teaching on a repo that holds uncommitted work they could lose.
- Assuming the learner's mental model of branches matches yours.
- Ordering by severity instead of frequency.
- Leaving the learner with nowhere to read further.
- Testing flag recall when the goal is diagnosis.

## Verification

    cd /tmp/tools-demo && git checkout HEAD~1 && git status | head -3
    # passes when the learner names the state, the model, and the recovery without looking

Report to the user: the three errors, the model each exposes, and the reversible/one-way label.
