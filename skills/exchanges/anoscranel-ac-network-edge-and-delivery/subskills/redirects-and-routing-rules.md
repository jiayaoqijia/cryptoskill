---
name: redirects-and-routing-rules
domain: software-engineering/redirects-and-routing-rules
trigger: "Controlling the rules layer that rewrites and redirects at the edge."
anti_trigger: "Not for application route design, and not for CDN cache keys."
scope: "Chains, loops, and the rules layer at the edge."
status: seedling
---

# Redirects and routing rules

## Standard

The edge usually holds a rules layer: rewrite this path, redirect that one, route by header or geography. Each rule is simple; the interactions are not. Two rules that are individually correct can compose into a loop — A redirects to B, B redirects back to A — and a loop at the edge is invisible to the application, because no request ever reaches it. Browsers stop following a loop after a number of hops and show an error the application's logs never mention.

Redirect chains are the quieter cost. Each hop is a round trip the user pays, and a path that redirects three times before serving content spends three network round trips before the first byte of anything useful. Chains accumulate the same way code does — one rule at a time, each defensible — and the only control is measuring the chain length per route and collapsing the middle hops.

Primary source: <https://developer.mozilla.org/en-US/docs/Web/HTTP>.

## Decision rules

- Record every edge rule and its order, because composition is order-sensitive.
- Trace each public route through the rules layer and record the hop count.
- Record redirect status codes deliberately: permanent redirects are cached by browsers and are hard to undo.
- Prefer one 301 over a chain of shorter redirects, and only after the final location is stable.
- Test rule changes with a temporary status before making anything permanent.
- Record the escape hatch: how to remove a rule that browsers have cached.

## Procedure

1. Export the rules layer in evaluation order.
2. Trace representative routes including legacy paths, counting hops.
3. Flag every permanent redirect whose target might change again.
4. Collapse multi-hop chains into single redirects.
5. Test changes with temporary status codes first.
6. Record the rules, the hop counts, and the removal procedure.

## Anti-patterns

- Permanent redirects to locations that later move again.
- Loops that only materialize when two rules ship in the same week.
- A rules layer with no export, reviewed as prose.
- Redirecting through an extra hop to "keep the old rule working".
- Assuming the browser will re-check a 301 it has cached.

## Done checklist

- [ ] Rules exported in order.
- [ ] Route traces with hop counts recorded.
- [ ] Permanent redirects audited for stability.
- [ ] Chains collapsed.
- [ ] Changes tested with temporary codes.
- [ ] Removal procedure recorded.

## Sources

- HTTP redirect status semantics: <https://developer.mozilla.org/en-US/docs/Web/HTTP/Status>
- RFC 9110, HTTP semantics including redirection: <https://www.rfc-editor.org/rfc/rfc9110>
- Caching of permanent redirects: <https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching>
