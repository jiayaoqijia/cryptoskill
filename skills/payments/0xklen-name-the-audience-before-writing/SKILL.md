---
name: name-the-audience-before-writing
description: Use when starting any document, update, or reply. Decide who reads it and what they must do, then include only what that reader needs.
---

# Name the audience before writing

A document written for everyone serves no one. Fix the reader and their goal first, and every inclusion test becomes easy.

## Procedure

1. Name the primary reader and their goal in one line before drafting: `on-call engineer, must restart the service`.

2. State what they must do after reading; make that action the spine of the document.

3. Include only background that reader lacks; cut what they already know.

4. Choose the register and terms for that reader — no unexplained internal shorthand.

5. Move secondary audiences to an appendix rather than diluting the main text.

6. Check each section against the reader's goal; delete sections that serve no one.

7. If two audiences need opposite things, write two documents, not one compromise.

## Pitfalls

- Writing for yourself, then "simplifying", leaves your own assumptions in.
- Serving an executive and an engineer in one doc satisfies neither.
- Assuming shared context the reader lacks stalls them at line one.
- Jargon excludes a newcomer; plain language patronises an expert; know which reader you have.
- A doc that says everything about the system helps no one take the next step.

## Verification

    head -3 doc.md   # names the reader and the action they must take

State the reader and their action at the top; write only what serves that reader.
