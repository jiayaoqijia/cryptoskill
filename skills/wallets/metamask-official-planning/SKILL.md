---
name: planning
description: >-
  Use in MetaMask Mobile or MetaMask Extension when scope is ambiguous, the
  change is large, the work is security-sensitive or performance-sensitive,
  a contract or API is being changed, or the engineer asks for mms-planning
  or a plan. Ambiguous means the ask does not name the target, the action,
  and the expected result, or it leaves an open product or contract decision.
  Large means only a new product area, or a cross-system design whose scope
  is not decided. Security, performance, a contract or API change, a long
  diff, or several screens is not large by itself. Contract or API changes
  stop for a brief. Security and performance stop for agreement before the
  edit, even when fully specified. Recommend a spec only when the change is
  also large. Do not use it before every edit. When it applies, read the
  installed mms-* catalog and every matching skill before the edit, brief,
  or yes/no.
maturity: experimental
---

# Planning

## Decision order

When this skill applies, follow this procedure before the first edit of that task. Do not embed a diagram of this procedure.

### Catalog

When `mms-planning` is triggered, run this catalog step before any edit, brief, or approval question. This applies to every execution path, including mechanical changes, reverts, spikes or POCs, routine CI-only work, and fully specified requests. Do not proceed to another step until the catalog check is complete. If a later step is reached before it has run, run it first.

Read the installed `mms-*` catalog. Assess every installed `mms-*` skill by its description. Read the body of every skill whose area the task touches. A partial or uncertain fit is read. Skip a skill only when the task has no surface for it. When an installed `mms-*` skill and a skill outside that catalog both fit, follow the `mms-*` skill. Prefer an installed skill over restating its guidance. The engineer does not have to name a skill.

Name a matching skill that is unavailable in this path's output. On a brief, that is the brief. Do not pretend it was applied. Do not block only because it is missing.

`mms-planning-spec` uses this same catalog rule for the spec it writes.

### 1. Classify

A change proceeds without a brief when any of these is true:

- It is mechanical. A change is mechanical when it cannot change behavior, a contract, or a risk surface. Formatting, comments, behavior-preserving renames, and copy typos that do not change what the product does are mechanical.
- The engineer will not keep the result. That is a throwaway, exploratory, or disposable spike or POC. A spike or POC the engineer will merge does not proceed without a brief. A spike or POC that touches security, privacy, or performance does not proceed without a pause.
- It is routine CI-only: coverage, Jest flags, Sonar, or another workflow edit. Changing how jobs or E2E launch stays on this path. A CI change that is large, a contract or API change, security-sensitive, or performance-sensitive does not use this path. That change stops for a brief and recommends a spec only when it is large.
- The ask points to an existing spec, plan, or ticket whose acceptance criteria cover this change, and the change is not security-sensitive or performance-sensitive. Follow it. Do not recommend another spec, even when the change is large.

Security-sensitive and performance-sensitive work never use step 3. Stop before the first product edit. Do not recommend a spec unless the change is also large. When the ask is fully specified and not large, the pause is a short brief: one line that names the risk, then `Do you agree, or do you want to discuss something in more detail?` Wait. No scope essay. When the ask is not fully specified, use the brief in step 4. An existing spec, plan, or ticket does not skip this pause.

Uncertainty splits by whether a wrong edit is cheap to undo.

Cheap uncertainty is only whether the engineer will keep the result, or whether an existing spec, plan, or ticket covers the change, and only when the change is not security-sensitive or performance-sensitive. Do not stop for a brief. Proceed as in step 3. End the final summary with one line that names that uncertainty and asks the engineer to confirm it. That line does not wait before the edit.

Risk uncertainty is whether the work is security-sensitive, performance-sensitive, a contract or API change, or large, including whether CI work is large or a contract or API change. Stop before the first product edit. Write a short brief, not the brief in step 4. The short brief is one line that names the uncertainty. It has no scope essay, no performance, UX, or test sections, and no spec. Then ask `Do you agree, or do you want to discuss something in more detail?` and wait. On agreement, the edit may start. More detail stays stopped.

Uncertainty about behavior, a contract, or a risk surface means the change is not mechanical.

A revert of a merged pull request or commit does not use steps 2, 3, or 4. Scope is that original change. The message is one line, whether or not it touches security or privacy. That line names the target pull request or commit, names the files, and asks exactly one yes/no question. When it touches security or privacy, that question names the risk. A shorter message is not this step. Do not offer a menu. Do not write a brief and do not recommend a spec. On yes, edit. Security or privacy means auth, secrets, logs or exports of state, permissions, keyring or vault, migrations, or persisted state.

### 2. Jira

Apply this step on every path except a revert.

Follow `mms-jira-brief` for ticket identification and the brief. That skill owns URL, bare-key, and non-Jira-token identification.

When a ticket is identified, read the brief and use it as context. When no ticket is identified, say nothing about Jira and continue. Do not ask for a ticket. Do not suggest creating one.

When a ticket was identified but the brief was not read, say what was missing. A failure file is not a brief that was read. Do not block on that failure.

### 3. Proceed without a brief

A revert does not use this step. Security-sensitive and performance-sensitive work do not use this step. Proceed. Do not show a brief. Do not ask for approval. Do not recommend a spec. Apply the Jira step. Run Checks, then edit.

### 4. Stop for a brief

A revert does not use this step. Stop before the first product edit. Do not block on a missing ticket.

A fully specified ask names the target, the action, and the expected result, and it leaves no open product or contract decision.

Decide whether a spec trigger applies. The only spec trigger is a large change, as defined in When to use. That trigger wins over a fully specified ask. A new design or a contract or API change that is not large gets a brief, not a spec. Security-sensitive work, performance-sensitive work, keyring, vault, auth, migrations, and persisted state are not large by themselves. Do not recommend a spec for them unless the change is also large. Say why in one line. Do not name `mms-planning-spec` in chat.

A new public method is a contract or API change. A contract or API change stops for a brief and does not use the yes/no path, including when the objection is that this repo should not hold the edit (wrong owner, a core package, or an existing API elsewhere). Put that objection in the brief. Do not answer with the objection alone. Recommend a spec only when that change is also large.

A fully specified ask that is security-sensitive or performance-sensitive does not use this yes/no. It uses the pause in step 1. A new public method or other contract or API change does not use that yes/no. When no spec trigger applies and the ask is fully specified, and it is not security-sensitive or performance-sensitive, this does not stop for a brief. Apply the Jira step. Do not mention a missing ticket. Do not write a brief. State scope in one line. Run Checks, then end with one yes/no and wait. Do not offer a menu. Do not use either question below. On yes, the edit may start.

When a spec trigger applies, the ask is not fully specified, or the change is a contract or API change, the change stops for a brief. Apply the Jira step.

Then brief scope and non-goals. Include performance, security, UX, and tests only when that area can change the work. Omit empty areas.

Run Checks, then ask the question below that matches whether a spec was recommended.

When a spec was recommended, do not end on the recommendation alone. Write the brief in the chat output, then end that same output with this question and wait. Do not use a structured choice prompt or a bottom sheet.

`Do you want me to continue with a planning spec, continue from this brief, or discuss something in more detail?`

Continuing with a planning spec reads and follows `mms-planning-spec` and does not edit product code in that turn. Continuing from the brief is agreement and the edit may start. More detail returns to the brief and asks this question again.

When a spec was not recommended, write the brief in the chat output, then end that same output with this question and wait. Do not use a structured choice prompt or a bottom sheet. No product edit happens before the answer:

`Do you agree, or do you want to discuss something in more detail?`

More detail returns to the brief. Agreement is the point where the edit may start.

## Checks

Run these before an edit that proceeds without a brief, before the revert yes/no, before the fully specified yes/no, and before the spec question or the agreement question. Every item that applies is required. A miss goes back to that step. Do not continue with it open.

- [ ] Classification matches step 1: the change proceeds without a brief, is cheap uncertainty, is a revert, takes the fully specified fast path, stops for a short brief, or stops for a brief.
- [ ] Before the revert yes/no: the message is one line, whether or not there is a security or privacy risk. That line names the target pull request or commit, names the files, and asks exactly one yes/no. A security or privacy revert names the risk in that question. A message that omits the target, the files, or the question is not done. There is no brief, spec, or menu.
- [ ] The Jira step is done except on a revert. A ticket that was identified was read. No ticket means no Jira mention and no request to create one.
- [ ] A spec is recommended only as step 4 states: for a large change, and never over an existing spec, plan, or ticket whose acceptance criteria cover the change. Security, a contract or API change, keyring, vault, auth, migrations, or persisted state does not get a spec unless that change is also large. A risk-uncertainty stop is a one-line short brief and does not recommend a spec.
- [ ] Before the fully specified yes/no: a fully specified ask with no spec trigger and no security, privacy, or performance surface states scope in one line and ends with one yes/no. There is no brief and no spec. A fully specified ask that is security-sensitive or performance-sensitive does not use this path. It stops for the one-line pause in step 1 and waits. A new public method or other contract or API change does not use this path.
- [ ] On every path, including mechanical, revert, unkept spike or POC, routine CI-only, and fully specified yes/no, the installed `mms-*` catalog was read and each matching skill was read or named missing. A path that edits, asks yes/no, or writes a brief without that read is not done.
- [ ] Cheap uncertainty proceeds only when the change is not security-sensitive or performance-sensitive. The final summary ends with one line that names the uncertainty and asks the engineer to confirm it. There is no brief and no wait before the edit.
- [ ] Security-sensitive or performance-sensitive work stops before the edit, even when fully specified, covered by a ticket, or not large. The fully specified pause is one line that names the risk, then the agreement question. No spec unless the change is also large.
- [ ] When the change stops for a brief, the brief states scope and non-goals. Performance, security, UX, and tests are present only when that area can change the work. A short brief is one line and does not use those sections.

## When to use

- Scope is ambiguous. The ask does not name the target, the action, and the expected result, or it leaves an open product or contract decision.
- The change is large. Large means only a new product area, or a cross-system design whose scope is not decided. A long diff, several screens, security, a contract or API change, keyring, vault, auth, migrations, or persisted state is not large by itself.
- The change introduces or modifies a public contract or API, including adding a public method. Stop for a brief, even when the change is fully specified. Recommend a spec only when the change is also large.
- The work is security-sensitive. That means auth, secrets, logs or exports of state, permissions, keyring or vault, migrations, or persisted state. Stop for agreement before the edit. This is not large by itself.
- The work is performance-sensitive. That means a screen's render or data path, list, animation, polling, prefetch, realtime data, startup, account or network switch, a new or changed selector, context provider, bundle, memory, battery, latency, or profiling. Stop for agreement before the edit. This is not large by itself. A copy typo, comment, behavior-preserving rename, or reading an existing selector to show a value already in the store, is not performance-sensitive.
- The engineer asks for `mms-planning`, a plan, or a planning spec.

Do not use this skill before every edit.

## Workflow

Follow Decision order, in that sequence. Run Checks at the points it names. Do not measure skill adoption. Do not write to Jira. `.specs/` and `.briefs/` are local and not team-shared storage. Do not stage them.
