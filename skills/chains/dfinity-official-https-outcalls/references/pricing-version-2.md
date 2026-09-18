# Pricing Version 2 (Pay-As-You-Go)

Version 2 is selected per call by the `pricing_version` field of `http_request`. Version 1 is still
the replica default and is deprecated. `flexible_http_request` has no such field and is always
priced with version 2.

**Rust only for now.** `ic-cdk-management-canister` 0.2.0's `HttpRequest` builder always selects
version 2. The Motoko `ic` package (4.x) prices with version 1 and has no version 2 path, which
needs a `moc` carrying the new cost primitive.

## What it charges

Version 1 charges for the bytes you *reserve*: `max_response_bytes`, whether you use them or not,
fixed when the call is made and never refunded. Version 2 charges for what the call *consumes*.

**Never hard-code a price.** Read the amount at runtime with `ic0.cost_http_request_v2`, or let
`HttpRequest::send()` do it. The per-unit coefficients are replica constants and can change; what
is stable, and what you need in order to reason about the levers, is *which resources are priced*.

What each version charges for:

| Resource | Version 1 | Version 2 |
|---|---|---|
| Request size (URL, headers, body, transform name and context) | charged | charged, in the base fee |
| Response bytes | charged against `max_response_bytes`, whether used or not | charged for the bytes that actually arrive |
| Round-trip time | **free** | charged per millisecond |
| Transform instructions | **free** | charged per instruction |
| Putting the response in a block | folded into the reserved-byte charge | charged per delivered byte, on the size after the transform |
| A per-call base fee | charged | charged |

The response, time and instruction terms are charged once for **each node that performs the
outcall**: all `n` of them for a fully replicated call, one for non-replicated, `total_requests` for
flexible. So subnet size multiplies them.

Two asymmetries decide whether migrating helps: version 1 overcharges for reserved size, and
version 2 charges for time and instructions that version 1 gave away free.

**`max_response_bytes` sets no price under version 2.** It still caps the response, and it still
sizes the reservation (see below).

One asymmetry between the quote and the charge is worth knowing, because it decides whether a
transform pays for itself. The **charge** for putting the response in a block is linear in the bytes
actually delivered, with no lower bound. The **quote** floors that term at about 1 KB, because
"whatever was asked for, a reject of this size may be delivered in its place". So stripping bytes
always lowers the bill in proportion to what you strip, while shrinking an already-small response
does not lower the reservation any further.

## Reserving: the four expectations

`ic0.cost_http_request_v2` quotes what to attach, from the resources you say you expect. In Rust
those are the four `with_expected_*` setters. Anything left unset falls back to the maximum that
parameter could reach:

| Setter | Default when unset |
|---|---|
| `with_expected_roundtrip_time_ms` | `60_000` (the longest the system waits) |
| `with_expected_raw_response_bytes` | `max_response_bytes`, or `2_000_000` if unset |
| `with_expected_transformed_response_bytes` | the above plus `1_024` bytes of Candid overhead |
| `with_expected_transform_instructions` | `5_000_000_000` if a transform is set, otherwise **0** |

Those defaults are expensive. The figures below were read from `ic0.cost_http_request_v2` on a
13-node subnet for a 200-byte request with `max_response_bytes = 4_000` and a transform set. Treat
them as indicative magnitudes rather than constants, and read your own with `get_cost()`:

| Configuration | Attached (cycles) |
|---|---|
| All four unset | 5_344_015_469 |
| Round trip 300 ms and instructions 1M declared | 112_185_476 |
| All four declared (sizes at 2_000) | 69_433_156 |
| For comparison, version 1 with the cap at 4_000 | 91_780_000 |
| For comparison, version 1 with the cap unset | 20_850_180_000 |

Which narrowing matters most depends on `max_response_bytes`, and it flips:

- **With a tight cap**, the transform-instruction default dominates: nearly all of that 5.34 billion
  is the query-limit reserve, held for a transform that may only strip headers. Declaring
  `with_expected_transform_instructions` is then by far the highest-value change. A request with no
  transform at all reserves nothing for one.
- **With a large or unset cap**, the byte terms dominate instead, because the delivery reserve is
  charged per byte of the transformed response and that defaults to the cap. With the cap unset the
  same call reserves about 34 billion, of which the blockspace reserve is the large majority, and
  declaring the round trip and the instructions only brings it to about 28.8 billion: a 1.2x
  improvement, not a 48x one.

So for a large cap, the first lever is `max_response_bytes` itself, which is a real ceiling the call
is bound by: setting it to something the response will actually fit brings both byte terms down with
it, since they default to it. Reach for `raw_response_bytes` only if you are willing to bet on the
server. The exception is `transformed_response_bytes`, which is yours to declare whenever the
transform bounds its own output, and which matters most precisely when the cap has to stay large
(see the practical rule below).

For a call that completes comfortably within either reservation, the charge is the same: rows two
and three above settle at the same amount, and only the cycles *held during the call* differ. So
narrowing is usually about how many outcalls the canister can have in flight.

But the attachment is not inert, and this is where version 1 intuition misleads. Everything beyond
the base fee becomes the per-node allowance, and the allowance **sets the node's operating limits**:

```rust
max_response_size: self.max_response_size.min(max_downloaded_bytes(remaining)),
max_response_time: MAX_RESPONSE_TIME.min(max_response_time(remaining)),
// and: MAX_INSTRUCTIONS_PER_QUERY_MESSAGE.min(max_transform_instructions(self.remaining()))
```

So a larger attachment buys the call permission to consume more, and it is billed for what it
consumes. Bytes are safe, because the cap is also bounded by your own `max_response_bytes` ("never
above what the caller asked for, even when it could afford more"). Time and instructions are not:
a bigger allowance raises the deadline toward the 60-second ceiling and the transform limit toward
the full query limit, so a slow endpoint or an expensive transform that a tight allowance would
have cut off instead runs to completion and charges for it.

**So the attachment is not inert: beyond the base fee it is the per-node allowance, and the allowance
is a ceiling on what the call may consume.** The charge follows what the call actually consumes, so
the size of the attachment changes the bill only when that ceiling binds. The two cases are
symmetric:

- **Ceiling does not bind** (the usual case). The call completes comfortably under either budget, so
  it consumes the same either way and is charged the same. Narrowing the expectations here changes
  only the cycles held, not the bill, which is why narrowing is normally about how many outcalls you
  can have in flight.
- **Ceiling binds.** A slow endpoint or a long transform that a tight budget would have cut short
  runs further under a larger one, and the call is charged for the extra. Over-attaching here raises
  the bill, not merely the hold.

Version 1 is no licence to over-attach either. Its charge is fixed when the call is made, so a
margin is never billed, but **a margin is still not free**: it is held for the whole call, so it
still caps how many outcalls the canister can have in flight. Neither version makes "attach a round
number to be safe" a good habit; they just punish it differently.

## The four values fund ONE pooled budget

This is the part that is easy to get wrong. The expectations are not four independent limits. They
are not even sent to the replica: they only decide how many cycles `send()` attaches. The replica
splits the attachment, minus the base fee, into a per-node allowance:

```text
per_replica_allowance = min(payment - base_fee, max_usage_fee) / node_count
```

and then derives each node's operating limits from **whatever is left of that whole allowance**,
by asking what it still buys at each resource's per-unit price:

- response size cap: `min(max_response_bytes, what the remaining allowance buys in bytes)`
- response deadline: `min(60 s, what it buys in milliseconds)`
- transform instruction limit: `min(the query limit, what it buys in instructions)`

(The published formulas divide `transform_instructions` by 13. That 13 is a reference subnet size
the fees are calibrated against, not the node count: a node is charged the same for a transform on
every subnet. Do not read it as `n`.)

Consequences an agent must know:

- Declaring a small `roundtrip_time_ms` does **not** impose that as the deadline. With the figures
  above, declaring 300 ms still leaves the nodes a deadline of tens of seconds, because the
  deadline comes from the pooled allowance, not from the declared value.
- Narrowing any one expectation tightens **all** the limits, because they share the pool.
- `remaining` at transform time is the allowance minus what the bytes actually downloaded and the
  milliseconds actually elapsed have already cost.
  Elapsed time differs per node, so the instruction limit differs per node. A transform sitting near
  its limit finishes on fast nodes and is cut off on slow ones, which is a divergence rather than a
  clean error.

Practical rule, by who controls the value:

- **`roundtrip_time_ms` and `transform_instructions`: declare them.** The round trip is soft (the
  deadline comes from the pooled allowance, not your figure) and the instruction count is a property
  of code you wrote.
- **`raw_response_bytes`: leave it at its default of `max_response_bytes`.** The server decides this
  one, and declaring fewer bytes than it sends is the narrowing that fails late (see below). To bring
  this term down, lower `max_response_bytes` itself.
- **`transformed_response_bytes`: declare it when your transform bounds its own output.** This is
  the exception to "leave the byte expectations alone", and often the largest single saving.

That last one deserves its own explanation, because it is the case where lowering
`max_response_bytes` cannot help. Delivery is by far the most expensive byte: on a 13-node subnet
one costs about 9,490 cycles charged against about 650 for a raw byte downloaded, roughly 15 times
more, and about 21 times more on the reservation for a fully replicated call (see the note below on
why the two differ). And `transformed_response_bytes` defaults to `max_response_bytes` plus 1,024,
so a transform that *shrinks* the response a lot leaves the delivery reserve sized for the raw
response.

Consider a 500 KB response that the transform reduces to a 2 KB extract. `max_response_bytes` has to
stay around 500 KB, because the raw response must fit under it, so it is not available as a lever.
For a fully replicated call the default transformed expectation of roughly 501 KB **reserves** about
6.87 billion cycles for delivery, where declaring 2,000 reserves about 27.4 million. (Those settle
at about 4.75 billion and 19.0 million respectively; the reservation is higher for the reason in the
next paragraph.) Nothing else you can change comes close.

The reservation and the charge differ by more than the 1 KB floor here. For a **fully replicated**
call the quote divides the delivery fee by the agreement threshold and multiplies by the node count,
`n / canister_http_threshold(n)`, which is 13/9 on a 13-node subnet, so each contributing node
reserves enough to cover the whole delivery on its own. A non-replicated call is not scaled that
way, so for it the reservation and the charge coincide.

This is safe in a way that `raw_response_bytes` is not: your transform decides its own output size,
so a fixed-shape extract has a bound you actually know. Two cautions. Size it from what your
transform emits, not from the raw response, and remember it is the Candid-encoded output that
counts. If your transform *expands* the payload, declaring from the raw size under-funds delivery;
the default cannot do that, since a transformed response is itself capped at `max_response_bytes`.

## Under-funding is accepted, not rejected

The up-front check is against the **base fee only**. Attach less than the call needs and it is
accepted, runs with tighter per-node limits, and fails partway, possibly *after* the remote server
was already contacted. The failure is intermittent: it depends on how slow the endpoint was and how
much work the transform did on that call.

Exact rejects, for `http_request`:

```text
"Insufficient cycles"                                           [CanisterReject]
    A node exhausted its own allowance. This is ordinary response content: it
    competes for agreement like a body, so it reaches the canister only if a
    quorum of nodes produce the same reject. One node's exhaustion delivers
    nothing on its own.

"No consensus could be reached. Replicas had different responses.
 Details: request_id: <id>, hashes: <...>"                      [SysTransient]
    The likely outcome of a marginal budget, because the per-node instruction
    limit depends on per-node elapsed time. Same message as a bad transform, so
    check the budget before rewriting the transform.

"Canister http request timed out"                               [SysTransient]
    Possible, but NOT an automatic consequence of under-funding. It needs two
    things at once: a node that never reports at all, and a collective
    allowance too small to fund delivery without that node's share of it. The
    delivery check is `initial_spent > allowance * num_replicas`, where
    `num_replicas` counts only "the replicas contributing to a response", so a
    silent node shrinks the pool. The payload is then invalid rather than
    rejected, nothing can be finalised, and the request sits until the
    60-second timeout. A well-funded call tolerates the same silent node
    without noticing, which is exactly the slack that under-funding removes.
    Diagnostically the worst case: the message mentions nothing about cycles,
    and "a timed-out request has no signed shares, hence no spend report", so
    there is no usage to inspect. Normally this reject is the retryable one; an
    under-funded call will time out again, so check the attachment first.

    What does NOT cause this: nodes giving up at different moments. That
    produces differing shares, which resolve promptly as an agreed reject or a
    divergence. With every node reporting, one of those two always fires, so
    you get an error rather than a hang.

"Out of cycles: ..."                                            [CanisterReject]
    Pooled shortfall, and the prompt counterpart of the timeout above. Every
    contributor reported and agreed, but what they left unspent still does not
    cover putting the response in a block. Synthesized by the payload builder;
    no node reports it.

"Http body exceeds size limit of <N> bytes."                        [SysFatal]
    Under version 2, <N> may be budget-derived rather than your
    max_response_bytes, so the body that failed can be well under the cap you
    set. Raise the reservation, not the cap.
```

For `flexible_http_request`, both conditions come back as a **reply**, not a reject: a node that
exhausts its share counts toward `too_many_rejects`, and an exhausted collective allowance is the
dedicated `out_of_cycles` global error.

## Refunds settle asynchronously

Each node returns what it did not spend. A node that never reported has its allowance returned when
the request times out, one minute after the response was delivered. A canister that reads its own
balance immediately after an outcall will see it still settling.

## Version and funding must agree

Version 2 is supported on mainnet: the flag that gates it was enabled on 2026-09-02 and is present
in the replica versions running across every subnet. Setting `pricing_version = 2` takes effect.

What does go wrong is a mismatch between the field and the attachment. The replica validates the
version only loosely: it filters an unrecognised value to the default, with no error.

```rust
args.pricing_version
    .filter(|v| allowed_versions.contains(v))
    .unwrap_or(DEFAULT_HTTP_OUTCALLS_PRICING_VERSION)  // = 1
```

So a bogus value surfaces as a funding problem rather than a validation one:

- Version 2 funded with a version 1 amount is **accepted**, because the up-front check is only the
  base fee. It then runs on a smaller per-node allowance than intended and can fail partway.
- Version 1 funded with a version 2 amount is **rejected up front**, because version 1 wants the
  whole `max_response_bytes` charge immediately:
  `"http_request request sent with <X> cycles, but <Y> cycles are required."` [CanisterReject]

Let one wrapper own both. `HttpRequest::send()` pairs version 2 with `cost_http_request_v2`;
Motoko's `Call.httpRequest` pairs version 1 with `cost_http_request`.

## Migrating

Version 2 is not uniformly cheaper. Version 1 overcharges for reserved size but gives away elapsed
time and transform instructions, so:

- A call that left `max_response_bytes` unset, or set it generously, gets dramatically cheaper.
- A call with a tightly tuned cap, a slow endpoint or a heavy transform can cost **more**, because
  it was previously getting the time and the instructions for free.

Check those two cases before migrating. Under version 1 the only lever was a tighter
`max_response_bytes`. Under version 2 the round trip and the transform are governed by their
expectations, while size is still governed by `max_response_bytes`: it no longer sets the price, but
it still sizes the reservation.
