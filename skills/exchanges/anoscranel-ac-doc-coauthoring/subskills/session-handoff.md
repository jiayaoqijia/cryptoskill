---
name: session-handoff
domain: writing/doc-coauthoring
trigger: "Concluding a co-authoring session or pausing work before document completion; preparing state for resumption"
anti_trigger: "Stopping a session abruptly without saving per-section state; dumping raw chat logs instead of structured handoff summaries"
scope: "Managing session closure and handoff; recording per-section status, resumption pointers, draft version markers, and author sign-off"
status: "seedling"
---

# Session Handoff

## Standard

Ending or pausing a co-authoring session requires a structured handoff artifact that allows any collaborator to resume the work instantly on a single read. Grounded in standard operational handoff practices (SBAR / I-PASS frameworks), this leaf distinguishes between document completion and session closure. The standard mandates recording per-section status (done, drafted, not started), outlining exact next steps, stamping a version marker on the draft, and securing the author's formal sign-off as the closing act. Handoffs must rely on structured summaries rather than exhaustive transcript dumps.

## Decision rules

1. Create a structured handoff summary whenever a co-authoring session is paused or completed.
2. Inventory every section from the skeleton with its precise operational status (done, drafted, in progress, not started).
3. Record immediate resumption pointers, including open questions and the exact next file or section to tackle.
4. Stamp a clear version marker on the draft artifact to prevent confusion between working drafts and final releases.
5. Require explicit author sign-off before closing a session designated as final release.

## Procedure

1. Review the overall document state against the section plan established in Stage 1.
2. Compile a concise handoff capsule detailing completed work, ongoing tasks, and pending decisions.
3. List explicit resumption instructions for any incoming collaborator or future session instance.
4. Verify version numbering and check that all decision logs and draft files are correctly saved to disk.
5. Present the handoff summary to the author, confirm final acknowledgment, and close the session cleanly.

## Anti-patterns

- Stopping work mid-stream without recording section progress or open action items.
- Passing raw, unedited chat transcripts as a resumption guide instead of structured summaries.
- Omitting draft version numbers, leading to conflicting edits across separate sessions.
- Confusing a temporary session pause with final document publication sign-off.

## Done checklist

A handoff that omits the author's sign-off is a session that ended, not a document that finished; record which of the two occurred before closing the session.

- [ ] Per-section status inventory recorded accurately.
- [ ] Resumption pointers and open questions clearly listed.
- [ ] Draft version marker stamped on the deliverable.
- [ ] Author sign-off secured for session closure or release.

## Sources

- SBAR and I-PASS operational handoff frameworks for structured communication (AHRQ TeamSTEPPS tool pages): https://www.ahrq.gov/teamstepps-program/curriculum/communication/tools/sbar.html and https://www.ahrq.gov/teamstepps-program/curriculum/communication/tools/ipass.html ⚠️ ahrq.gov blocks automated fetches (403); pages verified live via search lineage.
- ISO 24495-1 Plain language standards on document versioning and collaborative transparency: https://www.iso.org/standard/78907.html


⚠️ Note: Handoff summaries capture session state at a specific instant; verify ongoing branch alignment before resuming work.