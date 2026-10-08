---
name: structure-a-prompt-in-labelled-blocks
description: Use when writing or refactoring a prompt that will run in production. Fix the section order, label every block, and separate instructions from data so the model cannot confuse the two.
---

# Structure a prompt in labelled blocks

A prompt is an interface spec, not a paragraph of wishes. Fixed, labelled blocks in a stable order make the model's job unambiguous and make your prompt diffable when it changes.

## Procedure

1. Use a fixed top-to-bottom order: role, task, constraints, examples, input data, output format. The same order every time, so a channel of the prompt means one thing.

2. Label every block with a delimiter the model cannot produce accidentally — XML-ish tags or a fence, not blank lines.

```
<role>You extract invoice fields.</role>
<task>Return vendor, total, due_date.</task>
<rules>Amounts as integers in minor units. Missing field => null.</rules>
<examples>...</examples>
<input>{{document}}</input>
<output_format>JSON, keys in the order given.</output_format>
```

3. Put the instruction before the data it applies to, and repeat the one-line task at the end for long inputs — models attend more to the start and the end.

4. Separate instructions from untrusted data explicitly: wrap the document in `<input>` and state that nothing inside it is an instruction.

5. Keep constraints as checkable rules — "due_date is ISO-8601 or null", not "be accurate".

6. Pin the output contract in exactly one place; do not scatter format hints across blocks.

7. Version the prompt in a file with the model name in a comment, so a diff shows what changed and when.

## Pitfalls

- Baking the input into the instruction sentence ("Summarise this: <doc>") so the model cannot tell where the task ends and data begins.
- Using the same delimiter for instructions and data, so a document containing `</task>` breaks the structure.
- Blank-line separation of blocks; whitespace is not a boundary and is easily lost in transport.
- A different block order per call site, so the prompt cannot be reasoned about or diffed as a unit.
- Leaving the output format implicit and then parsing whatever came back.

## Verification

    grep -cE '<(role|task|rules|input|output_format)>' prompt.md   # expect the full set, >= 5

Report: "prompt uses 6 labelled blocks in a fixed order; `<input>` is fenced against instructions; stored as prompt.md v3 with the model pinned in the header."
