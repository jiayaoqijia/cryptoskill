---
name: explain-an-error-to-a-beginner
description: Use when a learner hits a stack trace or error message they cannot read. Teaches reading the message literally, classifying the failure, and reproducing it in isolation, rather than handing over the one-line fix.
---

# Explain an Error to a Beginner

Handing over the fix teaches the learner to wait for you. Teaching them to read the message literally, classify it, and shrink a repro makes them independent next time.

## Procedure

1. Read the message literally first: `KeyError: 'user_id'` says a dict lookup used a key that is not present. Do not paraphrase past the text.
2. Split the traceback into three parts: the exception type (`KeyError`), the message (`'user_id'`), and the deepest frame in their own code.
3. Classify the failure: name/shape error, type error, value or range error, or state/timing error. The class narrows the fix.
4. Shrink to a 5-line repro the learner runs themselves: `python3 -c "print({}['user_id'])"`.
5. If the tiny repro does not reproduce, the bug is in the context, not the line — widen from there.
6. Ask what they expected at the failing line versus what was actually there; the gap is the lesson.
7. Show the class of fix, not just this instance: "this shape means the key can be absent — guard or default it."
8. Have the learner explain the fix back before applying it.
9. Point them at how to find the class next time: search the exception name, read the docs for that call.
10. Ask for the exact command that failed, so the repro starts from the real invocation.
11. Point out which frame is theirs versus which frames are library code.
12. Leave them one on-purpose error to cause and read before the session ends.
13. Name the one word in the message that carries the meaning.
14. Show the fixed line and the failing line side by side.
15. Ask them to describe the error aloud in their own words.

## Pitfalls

- Editing the file for them, teaching dependence on a rescuer.
- Quoting the trace but skipping the deepest frame, which is where their code lives.
- Fixing `KeyError` with a blanket `try/except` that hides the real missing field.
- Treating every error as novel when it is a common shape they should learn to recognise.
- Explaining the whole call stack when only one frame is theirs.
- Reading the message as English instead of as a literal statement about values.
- Teaching the deep cause before they can read the surface message.
- Assuming they know what a traceback even is.
- Giving three candidate causes, so they cannot learn which test to run.
- Burying the key word in a paragraph of context.
- Showing only the fix, with nothing to compare against.
- Accepting a silent nod as understanding.

## Verification

    python3 -c "print({}['user_id'])"
    # passes when the learner's written repro raises the same KeyError without the surrounding app

Report to the user: the failure class, the repro command, and the class-level fix rather than the one-off patch.
