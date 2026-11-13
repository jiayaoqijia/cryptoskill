---
name: tool-surface-record
domain: prompt-engineering/tool-surface-record
trigger: "Recording the tool surface and its misfire history."
anti_trigger: "Not for runtime plumbing, and not for an audit trail of requests."
scope: "The written record: tool inventory, misfire log, and change history."
status: seedling
---

# Tool surface record

## Standard

The tool surface drifts: tools are added for features, renamed for clarity, split because a description could not carry two behaviours, and each change moves the selection odds for every other tool on the menu. The tool-surface record makes that drift visible: an inventory of the current menu with each entry's purpose and boundaries, a misfire log of what the model actually did, and a dated history of every change with its measured effect.

The misfire log is the active ingredient. When an agent picks the wrong tool, retries a permission error, or calls nothing where a tool existed, that event and its request text go in the log; the fix — usually a description or boundary edit — goes in beside it, and the next period shows whether the misfire class disappeared. A surface without this loop is tuned by feel: every change is a guess, and the guesses compound until nobody remembers why the menu confuses the model the way it does.

Primary sources: <https://modelcontextprotocol.io/docs/concepts/architecture> and <https://osf.io/prereg/>.

## Decision rules

- The inventory lists every tool with name, purpose, stated boundaries, and its neighbours.
- Every misfire is logged with the request text, the tool selected, and the tool that was right.
- Fixes are logged beside their misfires, with the period's recurrence rate.
- Each change to any tool is an entry: what changed, why, and the selection-accuracy effect.
- Rejected tool candidates recorded with reasons when the reason might reappear.
- Record is append-only; reviews read the log before proposing new tools.

## Procedure

1. Build the inventory from the live menu, with boundaries stated per entry.
2. Log each real misfire with its request text at the time it occurs.
3. Diagnose from the log: wrong selection, parameter invention, no-call, or indeterminate.
4. Apply the fix and record it beside the misfire.
5. Compare the next period's rate for that misfire class.
6. Before proposing any new tool: read the log for the last rejection of it.

## Anti-patterns

- A surface that mutates with no changelog.
- Logging misfires in a spreadsheet nobody opens when designing new tools.
- Fixes without recurrence measurement — "the prompt was rewritten" is not evidence.
- A changelog that records what changed but not why or with what effect.
- The same tool rejected three times with three different descriptions.

## Done checklist

- [ ] Inventory written with boundaries.
- [ ] All misfires logged in real time.
- [ ] Each misfire classified by cause.
- [ ] Fixes recorded with recurrence rate.
- [ ] Rejected candidates searchable before re-proposal.
- [ ] Changes reviewed against the measurable effect.

## Sources

- Tool layer architecture: <https://modelcontextprotocol.io/docs/concepts/architecture>
- Stated-change discipline: <https://osf.io/prereg/>
- Tool-use guidance: <https://docs.anthropic.com/en/docs/agents-and-tools/tool-use>
