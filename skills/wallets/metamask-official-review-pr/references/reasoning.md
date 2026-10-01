# Evidence-guided reasoning

Use this fixed flow before specialist routing. It helps the reviewer choose high-value checks and explain the limits of the evidence.

## 1. Build the claim map

Extract explicit claims from the pull request title and body, linked issue, changed code, and tests. Add implicit safety claims introduced by the diff, such as:

- existing behavior remains stable;
- failure stays bounded and recoverable;
- persisted state remains compatible;
- authorization and sensitive data boundaries remain intact;
- rendering and interaction cost remain acceptable;
- tests exercise the behavior they claim to cover.

Tie every claim to a changed path or cited pull request statement.

## 2. Draft the reviewer TL;DR

Synthesize the available pull request description, frozen code changes, comments within changed code, existing review comments, and linked issue context. Write two to four concise bullets in original agent wording:

- the intended outcome;
- the implementation approach visible in the diff;
- reviewer-relevant constraints, dependencies, or scope boundaries.

Rephrase rather than copy the pull request description. Present this as assistance to the reviewer, not as the author's statement or an approval. Mark material source gaps as unread.

## 3. Rank claims

Rank claims by:

1. user or system impact;
2. change size and reach;
3. uncertainty in the implementation;
4. reversibility after release;
5. strength of the available evidence.

Examine the highest-ranked claims first. Report the claims selected and the important claims left open.

## 4. Choose a concrete risk

For each selected claim, state one observable condition that would challenge it. Prefer a specific input, transition, failure, race, stale state, boundary value, or cross-platform difference.

The condition must be checkable from an available evidence source. Questions about unavailable evidence remain open questions.

## 5. Match evidence to the claim

| Evidence | Supports |
| --- | --- |
| Frozen diff and head files | Control flow, state transitions, API use, error paths, data boundaries |
| Tests at the frozen head | The scenarios and assertions the tests actually exercise |
| Check rollup | Which named automation completed and its conclusion |
| Visual evidence | Visible layout, copy, ordering, clipping, and interaction state shown |
| Runtime evidence | The exercised behavior, environment, and observations captured |
| Existing review comments | Earlier reviewer observations and deduplication |

State the evidence boundary. For example, a screenshot supports a visible layout claim; code or runtime evidence supports persistence and error-handling claims.

## 6. Route skills

Open [routing.md](routing.md). Apply repository preference skills for matching rules and domain capability skills for matching behavior. Record why each skill was selected or skipped.

## 7. Record guidance

For every substantive observation, record:

- a stable `<SEVERITY>-<n>` finding id from the report-wide sequence;
- claim;
- risk checked;
- evidence type and citation;
- evidence boundary;
- severity based on impact if confirmed;
- reviewer guidance;
- exact file, line, and requested change for a GitHub comment.

A claim supported by the evidence can be listed under **Claims examined** with its evidence boundary. This records coverage while leaving the approval decision with the human reviewer.
