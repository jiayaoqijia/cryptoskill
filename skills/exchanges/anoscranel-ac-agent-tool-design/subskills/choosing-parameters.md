---
name: choosing-parameters
domain: prompt-engineering/choosing-parameters
trigger: "Designing parameter sets the model can fill correctly."
anti_trigger: "Not for JSON Schema syntax, and not for transport."
scope: "Parameter sets the model can fill correctly from what it knows."
status: seedling
---

# Choosing parameters

## Standard

Every parameter is a question the model must answer before the tool runs, and the model answers from what it holds in context. A parameter it can infer — dates it has seen, IDs returned by earlier tools, names present in the request — is fillable. A parameter requiring knowledge it cannot have — internal codes, enumeration values it has never seen, whether a record is "type 3" — produces a confident invention, which is worse than an honest failure because the tool runs on it.

The fix set is short. Enumerations must be stated in the schema itself, because the model cannot guess a closed vocabulary; defaults must exist where a reasonable default exists, so the model is not forced to invent; required means truly required, since each additional one raises the chance of a fabricated value; and the parameter's name in the schema should be the word the request would use, not the internal field's column name. Parameter design is the model-facing half of the interface, and it is judged by the fill rate it achieves on real requests.

Primary sources: <https://platform.openai.com/docs/guides/function-calling> and <https://docs.anthropic.com/en/docs/agents-and-tools/tool-use>.

## Decision rules

- Stated enumerations live in the schema as the allowed values, never in prose elsewhere.
- Every optional parameter gets a default the tool can act on.
- Required list is the minimum for correct execution; optional is not decoration, it is deferred.
- Parameter names match the request vocabulary, not the database column.
- Never require what the model cannot know without being told; provide it elsewhere or redesign.
- Test fill rate: sample real requests, count parameters the model filled correctly first try.

## Procedure

1. List the facts the tool genuinely needs to act.
2. For each, ask: can the model know this from context, from the schema alone, or cannot at all?
3. Make schema-only knowledge explicit in the parameter definition as an enumeration or pattern.
4. Remove or default anything the model cannot know.
5. Rename parameters to the request's word where they diverge.
6. Measure first-try fill rate on real requests; iterate on the failures.

## Anti-patterns

- Free-text parameters where the real domain is a fixed vocabulary.
- Required flags used as documentation of importance rather than necessity.
- Internal enum codes exposed with no mapping visible to the model.
- Boolean pairs where a single enumerated choice is clearer.
- A ten-parameter tool where three carry nearly every call.

## Done checklist

- [ ] Facts classified by how the model can know them.
- [ ] Enumerations stated in the schema.
- [ ] Defaults present on optional parameters.
- [ ] Names matched to request vocabulary.
- [ ] First-try fill rate measured.
- [ ] Failures iterated until fill rate is acceptable.

## Sources

- Parameter schemas and strict mode: <https://platform.openai.com/docs/guides/function-calling>
- Tool definitions and parameters: <https://docs.anthropic.com/en/docs/agents-and-tools/tool-use>
- Architecture layering: <https://modelcontextprotocol.io/docs/concepts/architecture>
