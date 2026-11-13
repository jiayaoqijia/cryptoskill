---
name: ui-microcopy
domain: writing/ui-microcopy
trigger: "\"write this error message\", \"button label\", \"empty state\", \"form hint\"."
anti_trigger: "Full doc pages and READMEs (subskills/technical-docs.md); procedures and runbooks (subskills/procedures-sops.md)."
scope: "Buttons, errors, empty states, form hints, microcopy tests and word limits"
status: "seedling"
---

# UI microcopy

## Standard

- **Errors say what happened and how to fix it.** GOV.UK Design System: "Describe what has happened and tell them how to fix it… plain English, use positive language and get to the point" (https://design-system.service.gov.uk/components/error-message/). Microsoft's Win32 guidelines name the same three parts: what happened and why, the end result for the user, and how to prevent it (https://learn.microsoft.com/en-us/windows/win32/debug/error-message-guidelines).
- **The banned list is explicit.** GOV.UK: no jargon; no "forbidden", "illegal", "you forgot", "prohibited"; no "please" — it "implies a choice"; no "sorry"; no "valid"/"invalid"; no humour like "oops" (same sources).
- **Be specific.** Separate messages for empty, too long, too short, disallowed characters and wrong format. "An error occurred" and "This field is required" both fail.
- **Placement and hooks.** The message goes after the question and hint; the component adds a hidden "Error:" prefix for screen readers. Normative hooks: WCAG 2.2 SC 3.3.1 Error Identification and SC 3.3.3 Error Suggestion (https://www.w3.org/TR/WCAG22/).
- **Buttons are verb-first.** GOV.UK: sentence case, text describes the action and starts with a verb, one primary button per page (https://design-system.service.gov.uk/components/button/).

## Decision rules

1. Every error names the failure and the fix. If the fix cannot be named, the message is not ready.
2. ⚠️ No primary source publishes a numeric word cap. House convention (uncited): buttons of one to three words; errors of one sentence for what happened plus one for the fix; empty states of one line plus one action.
3. Empty states state the situation, then the filling action. "Nothing here yet" alone fails.
4. Hints sit in the label or helper text — never only in the placeholder, which vanishes on typing.
5. Buttons use the verb the user would say: "Create account", not "Submit". Destructive confirmations name the object and the consequence.

## Procedure

1. List every state: default, empty, loading, each failure mode, success, denied.
2. Write the error first: what happened, then the fix.
3. Write the button as action verb plus object, sentence case.
4. Write the empty state: situation in one line, filling action in one line.
5. Write hints above the field; never rely on a placeholder as the label.
6. Run the five tests, then fix failures in the text, not by adding words.
7. Check screen-reader order: label, hint, error with prefix.

## The five tests

- **Action:** can a tired user pick the right control from the label alone?
- **Five-second:** read once, then say what happened and what to do.
- **Read-aloud:** the text sounds like a person talking.
- **Screen-reader:** the error announces with its prefix after the label.
- **Banned-word scan:** search for please, sorry, oops, invalid, forbidden.

## Anti-patterns

- "An error occurred" with no fix.
- "Please" and "sorry" as politeness — both imply optionality.
- Humour in an error state; the user is mid-failure.
- A placeholder doing the label's job; one message covering five failures.

## Done checklist

- [ ] Every failure mode has its own message.
- [ ] Each error states what happened and the fix, in order.
- [ ] Buttons verb-first, sentence case, one primary per view.
- [ ] Empty states carry situation plus action.
- [ ] Hints outside placeholders; all five tests logged.
- [ ] Screen-reader order verified.

## Sources

- https://design-system.service.gov.uk/components/error-message/ · https://design-system.service.gov.uk/components/button/
- https://learn.microsoft.com/en-us/windows/win32/debug/error-message-guidelines · https://www.w3.org/TR/WCAG22/
