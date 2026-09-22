---
name: flow-security
description: Audits multi-step business flows for vulnerabilities that are invisible when endpoints are checked in isolation — order/payment/invoice state-machine violations, cross-step data provenance (stale or client-supplied totals at terminal steps), chained/association IDOR (ownership through entity joins), replay and duplication across steps, step-skipping via direct access, post-payment mutation, amount drift, and privilege transitions between hops. Use when the app has stateful workflows (checkout, signup/verify, submit/approve/publish, request/approve/execute, refunds, provisioning) — the classic case is "order, payment, and invoice each look fine alone, but order → payment → invoice compromises security at invoice generation."
license: MIT
---

# Business Flow Security (cross-endpoint analysis)

## Why this exists

Route-level audits check each endpoint against its own request. Flow-level
vulnerabilities live BETWEEN endpoints: an invariant that must hold across
the sequence (paid before invoiced, server-side price from order time,
ownership through the join chain) is enforced nowhere because every handler
assumes an earlier step established it. Individually clean, jointly broken.

Grounding: OWASP WSTG-BUSL-01..03 (business logic testing), OWASP A04
(Insecure Design), OWASP API Top 10 (API1 BOLA across associations).

## 1 — Reconstruct the flows

Pick the app's money/state-carrying flows (usually 1–5; ask the user or read
routes/models to name them). For each flow, extract:

```bash
# state-carrying entities + their status fields
rg -n "status|state|phase|stage" -g '**/models/**' -g '**/entities/**' -g '*.prisma' -g 'schema*' | rg -v "test" | head -20
# every status WRITE (= a transition) and the endpoints that own them
rg -n "status\s*[:=]|SET\s+status|status:" -g '*.js' -g '*.ts' -g '*.py' -g '*.java' -g '*.rb' -g '*.php' | rg -i "update|set|save|patch" | head -20
# terminal artifacts of flows (what the flow produces)
rg -n -i "invoice|receipt|refund|credit|shipment|provision|payout" -g '*controller*' -g '*handler*' -g '*routes*' -g '*views*' | head -20
```

Write the flow as a sequence with the entity each step reads/writes:

```
POST /orders            writes order(status=cart, total=<derived>)
POST /orders/:id/pay    reads order → calls gateway → writes payment
POST /payments/webhook  writes payment(status=paid)… order(status=paid)?
POST /invoices          reads order + payment → writes invoice(total=?)
```

Include hidden steps: webhooks, background jobs, retry/queue consumers,
admin override endpoints — they are flow steps even when not in the UI.

## 2 — Build the invariant table

For each step, write down what MUST be true before it runs (preconditions)
and what it writes. Two columns per step: `requires` / `effects`. Missing
preconditions are findings — the table makes them visible:

| Step | Requires (must verify in code) | Effects |
|---|---|---|
| create invoice | order.status == paid AND order.user == caller AND payment not already invoiced AND total from order row | invoice row |

## 3 — The 8 flow vulnerability classes

### F1 — Unguarded state transitions (skip / replay / disorder)
```bash
rg -n -i "update.*set.*status|status\s*:\s*['\"]" | rg -v "where.*status|AND status|status\s*==" | head
```
A transition that doesn't check the CURRENT state atomically allows:
invoice a `cart` order (skip payment), invoice twice (replay), refund after
refund. Safe shape: `UPDATE orders SET status='invoiced' WHERE id=? AND
status='paid'` (and check rows-affected), or `findOneAndUpdate({id, status:
'paid'}, …)`. **High/Critical** (money steps = Critical).

### F2 — Cross-step data provenance (stale / client-supplied at terminal steps)
```bash
rg -n "req\.(body|query)\.(total|amount|price|qty|quantity|discount|currency)" | head
```
The invoice/refund/charge step must derive money values from the persisted
source of truth (the order row as written at order time), never from
client re-submission or re-derivation from a mutable relation. If the
client sends the total anywhere past the first step → price tampering
(order says 100, payment says 100, invoice obediently records 1).
**Critical.**

### F3 — Chained (association) IDOR
```bash
rg -n "(invoice|receipt|shipment|refund).*find(By)?\(\s*\{?\s*(orderId|order_id|paymentId|payment_id)" | head
```
Each endpoint checks ITS object's ownership but not the JOIN path:
`/invoices?order_id=` fetches the order without `order.userId == caller` —
user A invoices/reads user B's order even though `/orders/:id` itself is
properly guarded. Rule: any handler accepting an id of entity X that
belongs to the flow must verify ownership through the FULL association
chain (invoice → order → user), not just existence of X. **High/Critical.**

### F4 — Replay & duplication at terminal steps
Webhook fires twice, retry double-submits, user double-clicks: does the
terminal step dedup on the flow's BUSINESS key (unique index on
`payment_id` in invoices, idempotency key checked at the step that
consumes it — not only where it's created)? Absence → double invoice /
double refund. **High** (Critical for refunds/credits).
```bash
rg -n -i "idempot|unique.*payment|uniqueIndex|ON CONFLICT|duplicate key" | head
```

### F5 — Step-skipping via direct access
Call the last step first: `POST /invoices` with an order id that has no
payment at all. Terminal endpoints must verify the PRIOR ARTIFACT exists
(payment row), not just the order. Census the flow's steps and hit each
with "what if I call this directly?" reasoning. **High/Critical.**

### F6 — Post-boundary mutation
```bash
rg -n "(put|patch|update).*(order|payment|cart)" -i | head
```
If the order is mutable after `status=paid` (PUT without a status guard),
the attacker changes quantity/items AFTER payment and the invoice (or the
fulfillment) reads the tampered row. Entities must be frozen at the trust
boundary (payment) — mutations either rejected or versioned. **High.**

### F7 — Amount drift across steps
Total computed at order time (10.005, floats), charged rounded (10.01),
invoiced truncated (10.00) → refund/credit arbitrage. Check: same
representation everywhere (integers of minor units / Decimal), same
currency field at every step, taxes computed once at the boundary.
**Medium** (High with refund flows).

### F8 — Privilege transitions between hops
Step 1 requires user auth, step 2 (webhook/callback) none, step 3 (invoice
fetch) session-OR-token — the weakest hop defines the flow's security.
Check each step's auth against the census table; internal callbacks must
carry signed/verified flow context (payment id they act on), not trust
"only our gateway calls this". Pairs with trusted-header rules in
`../auth-review/SKILL.md`. **Critical** when a hop is spoofable.

## 4 — Audit mode: flow-first

For transactional apps, do this pass BEFORE route-level grepping: walking
the flow as an attacker tells you which endpoints deserve deep reading and
raises route-level severities (a weak input check on `/orders` is Critical
if it feeds the invoice total). Re-run the chain rules of
`../security-audit/SKILL.md` Phase 2.5 with flow findings —
F2+F6 chains into money theft; F5+F3 chains into cross-user invoicing.

## 5 — Reporting

Each finding cites the FLOW, not just a line: the endpoint sequence, the
invariant violated, the concrete abuse story ("create order → pay 1 →
PATCH order total to 1000 → invoice reads tampered row"), and the fix at
the RIGHT step (guard the transition / derive the value / verify the join /
freeze the entity). Tag `flow-` with the class (F1–F8).

## False-positive discipline

- Legit async/stateful designs (admin-override transitions, support tools
  that legally skip steps) — check for an authorization guard on the
  override path before flagging F1/F5.
- Event-sourced / append-only models: "mutation" is a new event, not an
  UPDATE — F6 applies if events aren't validated against prior state.
- Idempotency at the QUEUE layer (exactly-once consumers) can satisfy F4 —
  verify the consumer ack, don't demand a unique index too.
