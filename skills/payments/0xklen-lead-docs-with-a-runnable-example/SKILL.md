---
name: lead-docs-with-a-runnable-example
description: Use when explaining a tool, library, or feature to someone who will learn by doing. Puts a complete working example before the reference prose, with the output it produces.
---

# Lead Docs with a Runnable Example

Readers learn a tool by running it, not by reading its options. A complete example that works on the first paste teaches more than three paragraphs of prose.

## Procedure

1. Open the section with the smallest complete example, including nothing omitted that would break it (imports, setup lines).
2. Make the example self-contained: no "assume a configured client". Show the two lines that configure it.
3. Show the expected output directly beneath, in its own fenced block, so the reader can compare.
4. Order the example along the reader's task: build, run, observe. Not along the module's internal structure.
5. Add a "what just happened" paragraph of two or three sentences after the output.
6. Move to the options table only after the reader has a working mental model.
7. Provide a second example that shows the one variation most readers need next (error handling, a different input).
8. Keep the example under 20 lines; longer examples go to `examples/` with a link and a filename.
9. Use real-ish values, not foo/bar; `users_table` beats `x`.
10. Give each example a name you can link to, so a bug report can cite the exact snippet.
11. Note the version the example targets, so a reader on an older release knows it may not apply.
12. Run the example verbatim from a clean checkout before publishing.

## Pitfalls

- A "simplified" example that omits the line everyone forgets, so it fails when copied.
- Prose that describes each concept before the reader has seen it work, front-loading theory.
- Example output that no longer matches, so the reader thinks they broke it.
- A fragment hinting at an example without the surrounding variables, forcing guesswork.
- Examples that only show the success path, hiding the error a first-timer will hit.
- A sample whose printed output includes a timestamp, so every reader sees a "wrong" copy.
- Burying the runnable example below the architecture overview.

## Verification

    python -c "$(sed -n '/```python/,/```/p' docs/quickstart.md | sed '1d;$d')"
    # extract and run the first example block; it must exit 0 and print the documented output

Confirm every fenced block in the doc runs as-is, and report any block that needed an edit to pass.
