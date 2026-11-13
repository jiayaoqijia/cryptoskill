---
name: ac-agent-memory-and-recall
description: "Memory that outlives the session: what an agent writes down at the end of its work, how notes are shaped so recall works, promoting working knowledge to permanent memory, superseding facts instead of appending contradictions, staleness and dated facts, and the written memory record. It teaches the discipline of persistent agent memory; it never predicts what a model will remember in-context and never recommends a storage product. Use when asking \"agent memory\", \"persistent memory\", \"memory file\", \"what should the agent remember\", \"note anatomy\", \"promote to memory\", \"supersede stale facts\", \"knowledge cleanup\", \"recall between sessions\", \"memory record\", \"note-taking system for agents\". Not for in-window context budgeting and compaction (ac-prompt-engineer), not for vector index mechanics and chunking (ac-retrieval-and-vector-systems), not for mid-task session handoff checkpoints (ac-handoff)."
license: MIT
metadata:
  domain: prompt-engineering
status: seedling
---

# Agent memory and recall

## Overview

A session ends and the conversation context dies with it. What survives is what was written down — and the difference between an agent that repeats its mistakes every session and one that compounds its knowledge is the discipline of the write-down. Persistent memory is not a product you install; it is a practice: what to record, in what shape, promoted how, superseded when, with what review triggers.

This skill covers that practice. Its neighbours hold the complementary mechanics: ac-prompt-engineer's tokens-capacity leaf budgets the window within one session; ac-retrieval-and-vector-systems builds the search layer that memory sits on; ac-handoff resumes one interrupted task. This skill owns the durable layer — what persists after the session is gone — and the recall discipline that makes the persisted layer usable.

Primary sources: <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents> and <https://en.wikipedia.org/wiki/Knowledge_management>.

## When to use

- When an agent's knowledge must survive session boundaries.
- When designing what gets written down at the end of work.
- When memory has grown and needs cleanup or supersession.
- When retrieved memories are trusted more or less than they should be.

## When NOT to use

- For in-window context budgeting and compaction (use ac-prompt-engineer).
- For index, chunking, and embedding mechanics (use ac-retrieval-and-vector-systems).
- For the mid-task checkpoint that resumes interrupted work (use ac-handoff).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/what-persists.md` | `prompt-engineering/what-persists` | The session-end write-down: what outlives the session and what dies with it. |
| `subskills/note-anatomy.md` | `prompt-engineering/note-anatomy` | One fact per note, dated, titled for retrieval, tagged for coverage. |
| `subskills/promote-and-supersede.md` | `prompt-engineering/promote-and-supersede` | Working note to permanent memory, dedupe, and contradiction handling. |
| `subskills/recall-discipline.md` | `prompt-engineering/recall-discipline` | Reading memory before acting, matching query to note, and trust calibration. |
| `subskills/staleness-and-review.md` | `prompt-engineering/staleness-and-review` | Lifecycle states for facts, review cadences, and pruning. |
| `subskills/knowledge-manage.md` | `prompt-engineering/knowledge-manage` | Memory cleanup, archive versus delete, and governance of the whole corpus. |
| `subskills/migration-and-portability.md` | `prompt-engineering/migration-and-portability` | Moving memory when infrastructure dies; format and export discipline. |
| `subskills/memory-record.md` | `prompt-engineering/memory-record` | The inventory of what is remembered, reviewed on a cadence. |

## Status and honest limits

Memory is a liability when stale: an agent that recalls a deprecated fact with confidence is worse than one that recalls nothing. Every technique here assumes the write-down is cheap and the recall is searchable; where retrieval infrastructure is absent, the discipline still applies to plain files. Nothing here predicts what a model will hold in its context window — that is in-window mechanics — and no storage product is recommended.
