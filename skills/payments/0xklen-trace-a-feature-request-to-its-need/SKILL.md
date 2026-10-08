---
name: trace-a-feature-request-to-its-need
description: Use when a specific feature is requested and the motive behind it is unstated. Asks why down the causal chain to the root job, then checks the feature is the cheapest way to do it.
---

# Trace a feature request to its need

The requested feature is a guess at how to meet a need. This skill walks the causal chain to the underlying job so the team can pick a cheaper or better way to satisfy it.

## Procedure

1. Write the request verbatim in `need.md` under `request:`.
2. Ask "what does that let you do?" and write the answer under `1:`. Repeat to three or four levels, stopping when the answer is a general purpose ("so I can decide", "so I can ship"), which marks the root job.
3. At each level note whether it is a statement about a mechanism (a feature) or a job (a need). Features sit at the top; jobs at the bottom.
4. Read the chain back and check each link actually follows; a jump like "add export so I can impress the board" hides a broken step.
5. Test the root job: would the same need exist if the product were rebuilt from scratch? If yes, it is stable and worth designing for.
6. List the ways to meet the root job, including the requested feature, a config change, a manual process, or an integration.
7. Pick the cheapest way that satisfies the job and note why the original feature was not chosen, if it was not.
8. Record the chain in the ticket so the next person does not repeat the questioning.
9. Check the chain against a persona who would not have this need, to test whether the root job is universal or personal.
10. Attach a quote from a real user at the root level, so the job is grounded in data and not in logic alone.

11. Test the root job by removing the product entirely: the job should still describe a real piece of human work.

## Pitfalls

- Stopping at the first "why" because the answer sounds sufficient.
- Rating the root job as a project goal ("increase revenue") rather than a user job.
- Using the chain to argue against the request rather than to meet it better.
- Accepting an answer that merely rephrases the feature ("so I can export").
- Forgetting the chain once the feature ships, so the next related request starts over.
- Drilling in a loop where each answer is a synonym for the last, which signals you have hit the root.
- Ending the chain at a technical mechanism because the user described the feature in technical terms.

- Recording the chain but not the decision it produced, so the analysis has no effect.

## Verification

    grep -cE '^(request|[0-9]):' need.md; grep -c '^job:' need.md

Report the root job, the chosen way to meet it, and whether it differs from the original request.
