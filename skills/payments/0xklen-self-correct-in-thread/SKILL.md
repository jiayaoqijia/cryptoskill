---
name: self-correct-in-thread
description: Use when you discover your earlier message, report, or decision was wrong. Issue a short standalone correction with the right fact, the command behind it, and the impact.
---

# Self-correct in thread

An uncorrected error keeps working after you notice it: people act on the old claim. Move the correction out fast, give it its own heading, and state what it touched.

## Procedure

1. On discovering the error, stop other work and issue the correction in the same turn if you can.

2. Title it `Correction:` and restate the wrong claim verbatim so it is easy to match.

3. Give the correct fact and the command that proves it: `git show HEAD:config.yml | grep listen`.

4. State the impact: which downstream action or belief the error contaminated.

5. Say whether the fix changes a conclusion, a number, or nothing material.

6. Do not bury the correction inside a fresh report; make it findable on its own.

7. If the wrong claim was already committed or sent, flag it for explicit retraction.

## Pitfalls

- Explaining why you erred without stating the correction buries the point.
- A correction issued after someone acted on the error is too late; move fast.
- Softening ("slight inaccuracy") understates a material error; state the magnitude.
- Over-apologising crowds out the fix; one line of regret, then the correction.
- Correcting silently in a new document, with no reference back, leaves the old one trusted.

## Verification

    grep -n "^Correction:" notes.md   # wrong claim, right fact, command, impact

Post the correction as its own findable note: what was wrong, what is right, what it affects.
