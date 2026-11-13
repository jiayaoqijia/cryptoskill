---
name: failure-and-recovery
domain: collaboration/failure-and-recovery
trigger: "Handling a failed, truncated, or stalled subagent; recovering from execution errors; resuming from partial files"
anti_trigger: "Respawning a failed agent from scratch with the original prompt; ignoring partial work left on disk"
scope: "Failure classes: transient vs latent/context faults; resumption from partial files with continuation brief; escalation paths"
status: seedling
---

# Failure and Recovery

## Standard

- **House subagent recovery standard**: a failed or truncated subagent is never restarted from scratch; recovery matches failure mode: transient timeout triggers direct re-dispatch with the same session ID, whereas context exhaustion triggers reading the partial file from disk and issuing a downshifted continuation brief. ⚠️ House threshold.
- **ArXiv 2608.24358, "The Handoff Tax"**: downshifting to continuation prompts requires passing more trajectory (completed work and remaining gaps) rather than fewer tokens, ensuring continuity without state loss. <https://arxiv.org/abs/2608.24358>
- **Fault classification theory**: distinguishing transient network/tool faults from latent prompt ambiguities prevents looping futile retries on broken briefs.

## Decision rules

1. Never discard partial work on disk when a subagent fails; inspect the checkpoint file first.
2. For transient network timeouts or tool errors, re-dispatch the same task tool call with the same session ID to continue where it stopped.
3. For latent prompt faults or instruction confusion, retrying cannot help; re-brief the agent with corrected constraints before resuming.
4. When respawning after a session crash, read the partial output file from disk and provide a continuation brief detailing what is done and what remains.
5. If the same error signature recurs across two consecutive retries, escalate immediately to a stronger model or human intervention.
6. Never restart a multi-step research or coding task from scratch when intermediate checkpoint files exist on disk.

## Procedure

1. Detect subagent failure via timeout, truncation, or validation rejection.
2. Inspect the workspace or output directory for incremental checkpoint files written before the failure.
3. Classify the failure: transient (retry same session), latent brief error (re-brief), or context crash (resume from file).
4. If resuming from file, construct a continuation brief containing the completed sections, remaining scope, and verbatim constraints.
5. Dispatch the continuation prompt to the recovery agent.
6. Verify that the recovery agent successfully appends to the existing file rather than overwriting it.

## Anti-patterns

- **Scraping the slate.** Deleting partial files and restarting from zero after a timeout. Fix: resume from disk checkpoint.
- **Blind retry loop.** Running the exact same failing prompt five times in a row. Fix: classify fault and fix the brief or model.
- **Ignoring recovery context.** Giving a replacement agent zero information about what the dead agent already completed. Fix: pass trajectory.
- **Silent failure acceptance.** Pretending a crashed agent succeeded because it stopped throwing errors. Fix: verify file completeness.

## Done checklist

- [ ] Failure mode classified (transient vs latent vs crash).
- [ ] Partial checkpoint files inspected on disk.
- [ ] Recovery path chosen (same-session retry vs file-based resumption brief).
- [ ] Continuation brief includes completed work and remaining scope.
- [ ] Replacement agent verified to append correctly.

## Sources

- ArXiv 2608.24358, "The Handoff Tax": <https://arxiv.org/abs/2608.24358>
- Internal operational playbooks for subagent recovery and checkpoint resumption.
