---
name: email
domain: writing/email
trigger: "\"write this email\", \"reply to this thread\", \"follow up\", \"one-ask email\", \"cover note\"."
anti_trigger: "A standalone decision document (subskills/memo-report.md); newsletter and sequence copy (out of scope for this tree)."
scope: "One-ask emails: subject, first line, ask, reply-ready; follow-ups"
status: "seedling"
---

# Business email

## Standard

- **Fix five slots before drafting:** document type, audience, goal (inform, persuade, request approval), length limit, tone. Skipping the slots is how a message becomes a conversation nobody can action (<https://datafield.dev/working-with-ai-tools-effectively/part-04/chapter-27/>).
- **Every claim in a generated draft traces to a span in the raw message.** Verification re-reads the source text, never a summary. A generated summary is not evidence of what the sender said (<https://mail.google.com/>).
- **Sending is a human act, permanently.** Recall does not exist. SMTP has no recall command, provider undo is a pre-send buffer capped at 30 seconds, and exchange recall is intra-organisation, read-dependent. "Draft is the terminal state": no automation promotes a message out of draft.
- **Subject lines carry data.** From 2.3M+ posts: keep 20–100 characters (<https://aitoolverify.com/best-ai-tools-email-marketing-2026> ⚠️ newsletter-platform data, not an email standard). Under 50 is ideal for mobile; no ALL CAPS or excess punctuation. Preview text extends the subject instead of repeating it.
- **Anti-spam is per jurisdiction.** CAN-SPAM requires opt-out and has no B2B exception. CASL express consent never expires, with the burden on the sender. UK PECR makes the instigator liable.
- **Accessibility is part of the message.** Every reply keeps a usable plain-text part and alt text on images.

## Decision rules

1. One ask per email. Two asks means two emails.
2. Subject line: the ask plus the object, no pretext. If the reader sees only the subject, they know what is wanted.
3. First line carries the ask. Warmth comes after, never as throat-clearing.
4. Reply-ready: the reader answers in one line without opening another document. Put the question as a question.
5. ⚠️ No primary source sets a business-email subject length. House convention: 20–100 characters.
6. Length: the email fits one phone screen. If it cannot, it is a memo.
7. Follow-ups: one nudge that adds new information, then stop.

## Procedure

1. Name the one ask. If you cannot write it in one sentence, split the email.
2. Verify every date, number and promise against the source message's raw text.
3. Write the subject: the ask and the object.
4. Write the first line: the ask, plainly.
5. Write the body in the order: context (one sentence), the ask, the deadline, what happens next.
6. Add the reply-ready question as the closing line.
7. Attach the plain-text part; alt-text every image.
8. Hand it to the human as a draft with the verification record. **The human sends.**

## Anti-patterns

- The "quick question" opener that never reaches the question.
- Two asks in one message.
- Dates or figures carried from a summary instead of the source.
- A follow-up chain with no new information.

## Done checklist

- [ ] One ask, written as one sentence.
- [ ] Every claim verified to the raw source span.
- [ ] Subject states the ask and object.
- [ ] First line is the ask; closing line is reply-ready.
- [ ] Fits one screen; plain-text part and alt text present.
- [ ] Consent state checked for any bulk or commercial send.
- [ ] **Human-gated:** sent by a named person.

## Sources

- <https://mail.google.com/>
- <https://datafield.dev/working-with-ai-tools-effectively/part-04/chapter-27/>
- https://www.rfc-editor.org/rfc/rfc5321.html
