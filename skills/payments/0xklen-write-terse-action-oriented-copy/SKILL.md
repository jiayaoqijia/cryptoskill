---
name: write-terse-action-oriented-copy
description: Use when UI text is verbose or vague. Cuts labels, buttons and errors to the shortest string that keeps the action unambiguous, and sets a length budget per surface.
---

# Write terse, action-oriented copy

Interface text is read in a glance and competes with the layout for space. "Click here to proceed with saving your changes" is 8 words where "Save" is 1 and carries the same meaning.

## Procedure

1. Set a length budget per surface and enforce it: button labels ≤ 3 words, menu items ≤ 4 words, field labels ≤ 3 words, error one-liners ≤ 12 words, tooltips ≤ 15.
2. Start button and menu labels with a verb that names the outcome: `Save`, `Delete account`, `Export CSV`, `Invite teammate`. Not `OK`, `Submit`, `Proceed`.
3. Make the label match the result. A dialog titled "Delete project?" whose button says "Continue" forces the reader to re-derive what happens; use "Delete project" on the button.
4. Cut politeness and hedging from controls: drop "Please", "just", "simply", "in order to", "click here". Keep them where warmth is the point (success confirmations).
5. Prefer specific nouns over pronouns. "This action cannot be undone" beats "Are you sure?" — say what is destroyed and whether it is reversible.
6. Front-load the meaningful word; users scan the first two words of a label. `Export CSV` not `CSV export options`.
7. Sentinel values must be words, not punctuation: an em-dash or `--` for "no value" reads as a rendering bug. Use "None" or leave the cell blank with a tooltip.
8. Write empty and error copy as a sentence a support agent could paste: what happened, what the user can do. "We couldn't reach the server. Check your connection and try again."
9. Localise-proof the strings: keep them in a resource file, never concatenated from fragments, so translators see a full sentence.
10. Use the same verb for the same action everywhere — if saving is "Save" on one screen, it is not "Update" or "Apply" on another. A single action with three names makes users re-learn it.
11. Write the button label as the answer to the dialog's question: a title "Delete 3 files?" is answered by a button "Delete 3 files", not "Yes".

## Worked example

    Before: "Are you sure you want to permanently remove this workspace? This action cannot be undone."
    After:  title "Delete workspace?"
            body  "This deletes 'Acme' and its 12 projects. This cannot be undone."
            buttons: "Cancel" | "Delete workspace"

The terse version names the object, the count and the consequence in 11 words and makes the destructive button say exactly what it does.

## Pitfalls

- Destructive and safe actions styled and phrased identically, so the only cue is colour.
- Sentence-case and Title Case mixed across the same screen, which reads as sloppy even when every word is fine.
- Two-word labels that are technically correct but ambiguous (`Apply`, `Manage`) forcing a tooltip to explain the button.
- Truncating into vagueness to hit a budget: "Configure" clipped to "Conf…" is worse than a shorter synonym. Rewrite, do not clip.
- Vague success toasts ("Changes saved") with no object, so a user who had two tabs open cannot tell which change landed.

## Verification

    # Flag control labels over the word budget:
    grep -rnoE '(label|title|aria-label)="([^"]+)"' src/ \
      | awk -F'"' '{n=split($2,a," "); if(n>3) print n" words: "$2}'

No control label over 3 words (menu items 4, tooltips 15). Report any over-budget string with its replacement and the surface it renders on.
