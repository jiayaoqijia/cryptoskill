---
name: ac-release-publish
description: "Publish or update a small public release of an agent-written artifact — skill files, spec documents, prompts — by treating every user-facing file as a claim set: inventory each factual sentence, verify it against the bytes, audit independently, repair from evidence, audit the delta, and gate the irreversible push. Use when asking 'publish this release', 'cut a release', 'verify the README before push', 'the release claims are wrong', 'sync the public files', or when a shipped release carries claims nobody checked. Not for: feature code, CI pipelines, or app deployment."
license: MIT
metadata:
  domain: skill-authoring
---

# Release Publishing

## Overview

A release page is not documentation. It is a set of assertions about an artifact: how many files it holds, what it does not contain, which version it is, where its links go. Treat every user-facing file — README, proof file, changelog — as a claim set. Each claim gets a proof command and an observed result before anything is pushed. The proof runs against the exact bytes that will ship.

The order matters because each step depends on the last. Claims are frozen to a tree hash, the gates run on that tree, a second hand audits it, repairs are logged against the findings, a third read audits the delta, one reviewer issues a single ship-or-halt verdict, and only then does the push happen. The published tree is verified again from a fresh clone, because the working copy is not what the world received.

The failure this pipeline exists to stop is cheap and common: a README written from memory shipped seven false claims in one release. Every one of them would have died to a single command.

## When to use

- Cutting a first public release of a small repository of documents, prompts, or skill files.
- Publishing an update that changes what the README or changelog asserts.
- A release has already shipped and someone found a claim that is not true.
- Local installed copies have drifted from the public files and need a resync.
- An audit returned findings on a release and the repairs need a second look.

## When NOT to use

Feature code is outside: this pipeline checks documents about an artifact, not the artifact's behaviour. CI pipelines and release automation are outside: the steps here are run by hand on a small repository, and wiring them into a pipeline is a different job. Application deployment is outside. Large monorepos, multi-package release trains, and binary distribution with signing keys are outside the tested range.

## Subskill index

| Leaf | domain segment | scope (one line) |
|---|---|---|
| `subskills/claim-files.md` | `skill-authoring/claim-files` | Inventory every factual sentence in the user-facing files and prove each one against the shipped bytes |
| `subskills/gates-run.md` | `skill-authoring/gates-run` | Run the local gate suite on the exact bytes that will ship, with no build artifacts left behind |
| `subskills/independent-audit.md` | `skill-authoring/independent-audit` | Brief a read-only second hand to sample the claims and return file, line, severity, and replacement text |
| `subskills/repair-and-delta.md` | `skill-authoring/repair-and-delta` | Repair from evidence, log every removal, and audit the delta for what the repair broke |
| `subskills/gate-review.md` | `skill-authoring/gate-review` | Issue the one verdict that licenses the push, or halt with an exact list of items |
| `subskills/push-publish.md` | `skill-authoring/push-publish` | Fetch, commit, tag the final commit, push without force, and publish notes drawn from the changelog |
| `subskills/release-verify.md` | `skill-authoring/release-verify` | Verify the published tree from a fresh clone, sync installed copies through the install gate, and close the record |

## Status and honest limits

Status: seedling. The procedure is written for a small public repository: one maintainer, tens of files, one release at a time. It has not been exercised on a monorepo, a multi-maintainer release train, or signed binary distribution.

Independence is a process property, not a guarantee. If the same agent writes the files and runs the audit, the audit is a careful re-read, not a second pair of eyes.

The gates catch patterns, not meaning. A fluent false sentence that matches no pattern passes every scan in this pack.

⚠️ House conventions here: the claim-set framing, the seven-step order, the single-verdict gate, and the install-gate rule. No public standard prescribes them for a repository this size; the cited standards supply the individual ideas, not the pipeline.

The delta audit lowers the rate of repair-introduced defects. It does not reach zero, and no step in this pack measures the residual rate.
