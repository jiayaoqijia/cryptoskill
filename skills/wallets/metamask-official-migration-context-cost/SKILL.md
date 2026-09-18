---
name: migration-context-cost
description: A file's JS→TS migration cost is driven mostly by context fan-in (upstream types it must read to derive from) and fan-out (downstream files that import it and must be updated), not by its line count. Scope and sequence migration tickets by it.
maturity: experimental
---

# TypeScript Migration Context Cost — Fan-In and Fan-Out

A file's line count is a factor in how hard it is to convert to TypeScript, but usually not the dominant one. The dominant cost is the **context the conversion pulls in** — everything the converter, human or AI, must read or touch to do it correctly.

## The two axes are different kinds of cost

- **Fan-in (upstream source types) — a _reading_ cost.** To type the file's values correctly you must load every upstream module whose types the code should _derive_ from: controller state, function returns, library exports, schemas (see `derive-types`). You read these; you do not change them, and they are usually already TypeScript. A file that derives from many sources is expensive to hold in context even if it is short.
- **Fan-out (downstream consumers) — a _change_ cost.** Re-typing the file ripples to every module that imports it; each may need its own update. These are files you actually edit, so fan-out — together with the file itself — is the **change and review surface**. A widely-imported file has a large change surface even if it is small.

The two are not the same kind of cost: fan-in is what you must _read_ to get the types right; fan-out is what you must _modify_. A 200-line hub imported by 100 files can be a larger migration than a self-contained 2,000-line leaf.

## Why it matters even for AI

Single-pass conversion of a high-fan-in/fan-out file is impractical even for a capable AI: it must hold the target file in context **and** read every upstream source-type file **and** edit every downstream consumer. That context load plus change surface — not the model's ability to read the file itself — is the binding constraint.

## How to use it

- **Scope tickets by context cost more than LOC.** Before sizing a migration ticket, estimate fan-in (how many upstream types it must derive from) and fan-out (`grep -rl` importer count). Size by the read-context plus the change surface, and treat line count as a minor factor.
- **Sequence low-fan-out first.** Convert leaf / low-fan-out files early — few downstream edits per PR. Files whose upstream types are already TypeScript are cheaper on the fan-in side and give later conversions more typed ground to derive from.
- **When the change surface won't fit one PR, reduce it first.** A hub with high fan-out is the case to decompose: split it into coherent units so each unit's fan-out — and thus each PR — is bounded (see `decompose-large-files`). Decomposition is one response to high context cost, not the only place the cost applies.
