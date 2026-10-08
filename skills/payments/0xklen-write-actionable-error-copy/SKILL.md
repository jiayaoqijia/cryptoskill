---
name: write-actionable-error-copy
description: Use when writing or reviewing any message a user sees on failure. Turns blame-and-jargon errors into copy that names the cause, the impact, and the one next step.
---

# Write actionable error copy

An error message is the product speaking at its worst moment. This skill makes every failure message say what happened, what it means for the user, and exactly what to do next.

## Procedure

1. Collect the user-facing strings: `grep -rIn 'error\|failed\|invalid' src/locales/en.json` (or wherever copy lives) into `errors.md`.
2. For each string enforce three parts in order: what happened, what it means for the user's data or task, and the single next action.
3. Replace internal identifiers with human terms: `ECONNREFUSED` becomes "The service is temporarily unavailable", never the raw code.
4. Never blame the user or the machine ("you entered an invalid input", "an error occurred"); state the condition neutrally.
5. Give exactly one primary action per message — Retry, Sign in again, Contact support — with a link or button. Two competing actions stall the user.
6. Preserve any code the user must quote to support, shown in a copyable field rather than buried in sentence text.
7. Check every message at 60-character width (a mobile toast) and confirm the action is visible without scrolling.
8. Lint the whole set for tone; flag a message that reads differently from its neighbours.
9. Write the copy with the variable values filled in, so the sentence reads naturally with the longest real value.
10. Rate each message by severity and reserve the strongest visual weight for the ones the user must act on.

11. Keep a glossary of product terms used in messages so copy is consistent across writers and locales.

## Pitfalls

- Logging the raw exception to the user; it leaks stack traces and internal hostnames.
- "Please try again later" with no later and no alternative, which reads as a shrug.
- Copy that appears only after the fact, with no way to retry the failed action in place.
- Over-localising numbers and dates into a sentence so translators break it; keep them as parameters.
- Distinguishing cases the user cannot act on differently; if the fix is the same, the message is redundant.
- A single generic message reused for unrelated failures, so debugging from a screenshot is impossible.
- Error copy that only appears in a console log the user never opens.

- Using the same word for two different failures, so support cannot tell which one occurred.

## Verification

    grep -c 'Retry\|Try again\|Sign in\|Contact' errors.md; grep -in 'invalid input\|an error occurred' errors.md || echo clean

Report the messages with no next action and any that leak an internal code or stack trace.
