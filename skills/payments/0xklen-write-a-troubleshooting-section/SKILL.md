---
name: write-a-troubleshooting-section
description: Use when docs must help a user diagnose and fix a problem without paging support. Organises symptoms as searchable entries with the cause, the check, and the fix.
---

# Write a Troubleshooting Section

Troubleshooting docs are searched by an error message, not read top to bottom. Each entry must be findable by the exact symptom and end in a fix.

## Procedure

1. Organise by symptom, in the user's words: "Connection refused on port 5432", not "Database connectivity subsystem".
2. Quote the literal error string in the heading, including the code: `EADDRINUSE: address already in use`.
3. For each entry, use three labelled parts: Symptom, Cause, Fix. Keep them in that order.
4. Give the diagnostic command before the fix so the user confirms the diagnosis: `lsof -i :5432`.
5. State the fix as commands, and name the file to edit if configuration is involved.
6. Add a one-line "why this happens" so the user can generalise to the next error.
7. Link to the relevant config or runbook instead of repeating it.
8. Order entries by observed frequency, most common first; bury the rare case.
9. Include a "when this does not work" fallback: the next diagnostic step or the support channel.
10. Mirror real support tickets: every recurring ticket becomes an entry with its literal error text.
11. Add a version or environment note when the fix is specific to a release or OS.
12. Test by searching for the error string; the entry must rank high with the exact match.

## Pitfalls

- Headings that name the cause not the symptom, so the search for the error text misses them.
- A fix with no diagnostic step, so the user applies it blind and breaks something else.
- Copy-pasting a Stack Overflow answer with the wrong version's behaviour.
- Entries that describe the problem but never state the resolution.
- Splitting one problem across two entries, so neither is complete.
- Fixing by disabling a safety check, which trades one outage for a later worse one.
- An entry whose fix requires root or a permission the reader may not hold, with no note.

## Verification

    grep -n 'EADDRINUSE' docs/troubleshooting.md

The exact literal error is present in a heading or the first line of its entry. Take the top five support tickets and confirm each literal error string appears with a diagnostic and a fix.
