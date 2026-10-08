---
name: merge-system-and-user-instruction-layers
description: Use when a product sends per-request overrides alongside fixed system instructions. Define which layer owns what, how they merge, and what a user turn can never override.
---

# Merge system and user instruction layers

System and user turns are not the same authority. Decide once what lives where; otherwise per-request text quietly rewrites the product's rules.

## Procedure

1. Assign ownership: the system layer owns identity, safety rules, the output contract, and tool policy. The user layer owns the specific task, its inputs, and parameters within the contract.

2. Never let the user turn redefine the output format or the safety rules. If a request needs a different format, that is a system-level feature flag, not free text.

3. Merge predictably: build the final prompt as system + a templated user block. The user fills marked slots, not arbitrary positions.

```
<system>...</system>
<user>
 task: {{task}}
 params: {{params}}
</user>
```

4. Treat user-supplied parameters as data, escaped and bounded — an enum checked in code stays an enum, not a string the model re-interprets.

5. When a user turn and the system conflict ("ignore the format and write prose"), the system wins and the model reports the conflict rather than silently obeying.

6. Keep the system block stable across requests so it can be cached and so behaviour does not drift with injected text.

7. Document the split: what a caller can and cannot change per call.

## Pitfalls

- Building the whole prompt from the user's message in production, so nothing is actually fixed.
- Letting user text land before the system rules, where it frames them.
- Interpolating an unbounded user string into an instruction position, enabling injection.
- Per-request system blocks that defeat provider prompt caching and cost far more.
- Assuming the model obeys the hierarchy by default; state it and test it.

## Verification

    python3 -c "import yaml;c=yaml.safe_load(open('config.yaml'));print(c['system_hash'])"   # system hash identical across 10 sampled requests

Report: "system block fixed (hash stable across requests), user input confined to labelled slots; a conflict test ('write prose not JSON') held — the model returned JSON and flagged the conflict."
