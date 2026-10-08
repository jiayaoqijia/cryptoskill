---
name: mentor-by-socratic-questioning
description: Use when a learner asks a question they could answer themselves. Guides with a ladder of questions that narrows to the answer, and refuses to hand it over until the learner has made a genuine attempt.
---

# Mentor by Socratic Questioning

Answering every question builds a lookup relationship; the learner defers instead of thinking. A question ladder that narrows the search gets them to the answer under their own power.

## Procedure

1. Ask the learner to state what they already know and what specifically they are stuck on.
2. Start broad and narrow one rung per exchange:
   - "What does the error message literally say?"
   - "What was different just before it broke?"
   - "Where would that value come from?"
   - "What would you expect if it were there?"
3. Cap at four rungs; if the learner is still stuck, give a pointer to the file or doc, not the answer.
4. Reward the process aloud: "you found it by ruling out the cache — that is the method."
5. Never answer a question a one-line command would answer; ask them to run `git log -1 -- path` instead.
6. After resolution, ask them to write the reasoning in one sentence for the next person.
7. If the learner is blocked by a missing fact, supply that fact; questioning a pure knowledge gap is unfair.
8. Note in `mentor-log.md` which rung usually unlocks people, so your ladder improves over time.
9. Watch for the learner guessing to please you; ask them to say why, not just what.
10. Let silence sit for a few seconds after a rung; the learner usually fills it.
11. Have the learner restate the question in their own words before the ladder starts.
12. Keep a shared doc of resolved questions so the same ladder is not climbed twice.
13. Ask one question at a time and wait for the answer before the next.
14. Write the learner's answers down so they see their reasoning tracked.
15. End by naming the method they used, not just the answer they found.

## Pitfalls

- A rung that is really a hint dressed as a question ("have you tried the debugger?").
- Six rungs of questions that frustrate instead of guide.
- Withholding a fact the learner simply does not have yet.
- Asking leading questions that telegraph the answer, so nothing is actually discovered.
- Relenting and answering mid-ladder because silence is uncomfortable.
- Turning the ladder into an interrogation instead of a shared search.
- Asking rhetorical questions rather than ones with a real answer.
- Rushing to the next rung before the learner has had time to think.
- Using the ladder on a learner who is panicking; lead with reassurance first.
- Stacking questions so the learner answers none fully.
- Forgetting the earlier answers, so the ladder feels random.
- Praising only the answer, not the method that produced it.

## Verification

    grep -cE '^Q[0-9]:' mentor-log.md
    # passes when the log shows <= 4 rungs to resolution and at least one 'ruled out' observation

Report to the user: the rungs asked and the sentence the learner wrote to explain the resolution.
