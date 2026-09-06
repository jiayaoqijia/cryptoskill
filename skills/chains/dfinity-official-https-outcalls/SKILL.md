---
name: https-outcalls
description: "Make HTTPS requests from canisters to external web APIs. Covers transform functions for consensus, cycle cost management, response size limits, and idempotency patterns. Use when a canister needs to call an external API, fetch data from the web, or make HTTP requests. Do NOT use for EVM/Ethereum calls — use evm-rpc instead."
license: Apache-2.0
compatibility: "icp-cli >= 0.2.2"
metadata:
  title: HTTPS Outcalls
  category: Integration
---

# HTTPS Outcalls

## What This Is

HTTPS outcalls allow canisters to make HTTP requests to external web services directly from on-chain code. Because the Internet Computer runs on a replicated subnet (multiple nodes execute the same code), all nodes must agree on the response. A transform function strips non-deterministic fields (timestamps, request IDs, ordering) so that every replica sees an identical response and can reach consensus.

## Prerequisites

- For Motoko: `mo:core` 2.0 and `ic >= 2.1.0` in mops.toml
- For Rust: `ic-cdk >= 0.19`, `serde_json` for JSON parsing

## Canister IDs

HTTPS outcalls use the IC management canister:

| Name | Canister ID | Used For |
|------|-------------|----------|
| Management canister | `aaaaa-aa` | The `http_request` management call target |

You do not deploy anything extra. The management canister is built into every subnet.

## Mistakes That Break Your Build

1. **Forgetting the transform function.** Without a transform, the raw HTTP response often differs between replicas (different headers, different ordering in JSON fields, timestamps). Consensus fails and the call is rejected. ALWAYS provide a transform function.

2. **Not attaching cycles to the call.** On a normal Application subnet, HTTPS outcalls are not free — the calling canister must attach cycles to cover the cost, and attaching zero fails the call. Both Motoko and Rust have wrappers that compute and attach the required cycles automatically: in Motoko, use `await Call.httpRequest(args)` from the `ic` mops package (`import Call "mo:ic/Call"`); in Rust, use `ic_cdk::management_canister::http_request` (available since ic-cdk 0.18). Under the hood, both use the `ic0.cost_http_request` system API to calculate the exact cost from `request_size` and `max_response_bytes` — the API is cost-schedule aware, so the same wrapper attaches the correct amount on any subnet type. On a **cloud engine** (`CloudEngine` subnet), that amount is always 0 by design; do not "fix" a working outcall by attaching a hardcoded non-zero fee there — see the `cloud-engine-canisters` skill.

3. **Using HTTP instead of HTTPS.** The IC only supports HTTPS outcalls. Plain HTTP URLs are rejected. The target server must have a valid TLS certificate.

4. **Sizing `max_response_bytes` against the expected body — the limit is not body-only.** The spec defines the size of an HTTP request or response as *the total number of bytes representing the names and values of HTTP headers and the HTTP body*. Response **headers count against `max_response_bytes`**, and a real API commonly sends 1–2 KB of response headers (a unique request id, `Date`, the rate-limit family, CDN headers) before a single byte of body — against a tight cap that is a large share of the budget. Size the cap for **headers + body as they arrive from the server**, then add margin. The failure mode is total: the call fails every time rather than returning a truncated response. The maximum is 2MB = `2_000_000` bytes (decimal, not 2^21), and the same headers-plus-body definition caps the **request** you send at `2_000_000` bytes.

5. **Expecting the transform function to shrink an oversized response under the cap.** The cap is enforced **twice**: once on the raw response as it arrives from the server (headers first, then the body against what remains), and again on the transform's Candid-encoded **output**, which includes serialization overhead. Stripping headers in the transform cannot rescue a raw response that already exceeded the cap, because that first check fails before the transform ever runs. It *can* keep the transform's own output under the cap — worth doing when the transform would otherwise echo the headers back and its encoded output would exceed the limit. Both checks compare against the **same** `max_response_bytes` value, which is why a raw response that only just fits can still fail after the transform: the Candid overhead is added on top. So: size `max_response_bytes` for the raw response, and keep the transform's output small; never set a tight cap on the theory that stripping headers afterwards will make an oversized response fit.

6. **Ignoring the header limits.** Independent of `max_response_bytes`, the spec caps HTTP requests and responses at **64 headers**, **8 KiB** per header name or value, and **48 KiB** for all header names and values combined. The URL must not exceed **8192** bytes. On the request side these are enforced when the replica decodes your arguments, so an over-limit request never leaves the subnet and fails with `InvalidManagementPayload` — e.g. `Deserialize error: The number of elements exceeds maximum allowed 64` — rather than with any HTTP-looking error. If you send no `user-agent` header the IC adds `user-agent: ic/1.0`, and that added header does not count toward these limits.

7. **Omitting `max_response_bytes`.** If you do not set `max_response_bytes`, the system assumes the maximum (2MB) and charges cycles accordingly — roughly 20.85 billion cycles on a 13-node subnet. Always set this to a reasonable upper bound for your expected response (see pitfall 4 for what counts toward it).

8. **Non-idempotent POST requests without caution.** Because multiple replicas make the same request, a POST endpoint that is not idempotent (e.g., "create order") will be called N times (once per replica, typically 13 on a 13-node subnet). Use idempotency keys or design endpoints to handle duplicate requests.

9. **Not handling outcall failures.** External servers can be down, slow, or return errors. Always handle the error case. There are **two distinct timeouts**, and neither traps — both come back as rejects (in Motoko the `await` raises a catchable `Error`; in Rust the wrapper returns `Err`):
   - The remote server does not respond within **30 seconds**: `SysFatal`, message `Timeout expired`.
   - The subnet does not produce a response within **60 seconds**: `SysTransient`, message `Canister http request timed out`. This one is the retryable one.

10. **Calling localhost or private IPs.** HTTPS outcalls can only reach public internet endpoints. Localhost, 10.x.x.x, 192.168.x.x, and other private ranges are blocked.

11. **Forgetting the `Host` header.** Some API endpoints require the `Host` header to be explicitly set. The IC does not automatically set this from the URL.

## Implementation

### Motoko

The management canister types are imported via `import IC "ic:aaaaa-aa"` (compiler-provided). The `ic` mops package (`import Call "mo:ic/Call"`) provides `Call.httpRequest` which auto-computes and attaches the required cycles.

```motoko
import Blob "mo:core/Blob";
import Nat "mo:core/Nat";
import Text "mo:core/Text";
import IC "ic:aaaaa-aa";
import Call "mo:ic/Call";

persistent actor {

  // Transform function: strips headers so all replicas see the same response for consensus.
  // MUST be a `shared query` function.
  public query func transform({
    context : Blob;
    response : IC.http_request_result;
  }) : async IC.http_request_result {
    {
      response with headers = []; // Strip headers -- they often contain non-deterministic values
    };
  };

  // GET request: fetch a JSON API
  public func getIcpPriceUsd() : async Text {
    let url = "https://api.coingecko.com/api/v3/simple/price?ids=internet-computer&vs_currencies=usd";

    let request : IC.http_request_args = {
      url = url;
      // Always set — omitting defaults to 2MB and charges accordingly.
      // Budget for response headers + body: the cap covers both, and the
      // transform cannot bring an oversized response back under it.
      max_response_bytes = ?(10_000 : Nat64);
      headers = [
        { name = "User-Agent"; value = "ic-canister" },
      ];
      body = null;
      method = #get;
      transform = ?{
        function = transform;
        context = Blob.fromArray([]);
      };
      is_replicated = null;
    };

    // Call.httpRequest computes and attaches the required cycles automatically
    let response = await Call.httpRequest(request);

    switch (Text.decodeUtf8(response.body)) {
      case (?text) { text };
      case (null) { "Response is not valid UTF-8" };
    };
  };

  // POST transform: also discards the body because httpbin.org includes the
  // sender's IP in the "origin" field, which differs across replicas.
  public query func transformPost({
    context : Blob;
    response : IC.http_request_result;
  }) : async IC.http_request_result {
    {
      response with
      headers = [];
      body = Blob.fromArray([]);
    };
  };

  // POST request: send JSON data
  public func postData(jsonPayload : Text) : async Text {
    let url = "https://httpbin.org/post";

    let request : IC.http_request_args = {
      url = url;
      max_response_bytes = ?(50_000 : Nat64);
      headers = [
        { name = "Content-Type"; value = "application/json" },
        { name = "User-Agent"; value = "ic-canister" },
        // Idempotency key: prevents duplicate processing if multiple replicas hit the endpoint
        { name = "Idempotency-Key"; value = "unique-request-id-12345" },
      ];
      body = ?Text.encodeUtf8(jsonPayload);
      method = #post;
      transform = ?{
        function = transformPost;
        context = Blob.fromArray([]);
      };
      is_replicated = null;
    };

    // Call.httpRequest computes and attaches the required cycles automatically
    let response = await Call.httpRequest(request);

    if (response.status == 200) {
      "POST successful (status 200)";
    } else {
      "POST failed with status " # Nat.toText(response.status);
    };
  };
};
```

### Rust

```toml
# Cargo.toml
[package]
name = "https_outcalls_backend"
version = "0.1.0"
edition = "2021"

[lib]
crate-type = ["cdylib"]

[dependencies]
ic-cdk = "0.19"
candid = "0.10"
serde = { version = "1", features = ["derive"] }
serde_json = "1"
```

```rust
use ic_cdk::api::canister_self;
use ic_cdk::management_canister::{
    http_request, HttpHeader, HttpMethod, HttpRequestArgs, HttpRequestResult,
    TransformArgs, TransformContext, TransformFunc,
};
use ic_cdk::{query, update};
use serde::Deserialize;

/// Transform function: strips non-deterministic headers so all replicas agree.
/// MUST be a #[query] function.
#[query(hidden = true)]
fn transform(args: TransformArgs) -> HttpRequestResult {
    HttpRequestResult {
        status: args.response.status,
        body: args.response.body,
        headers: vec![], // Strip all headers for consensus
        // If you need specific headers, filter them here:
        // headers: args.response.headers.into_iter()
        //     .filter(|h| h.name.to_lowercase() == "content-type")
        //     .collect(),
    }
}

/// GET request: Fetch JSON from an external API
#[update]
async fn fetch_price() -> String {
    let url = "https://api.coingecko.com/api/v3/simple/price?ids=internet-computer&vs_currencies=usd";

    let request = HttpRequestArgs {
        url: url.to_string(),
        // Budget for response headers + body: the cap covers both, and the
        // transform cannot bring an oversized response back under it.
        max_response_bytes: Some(10_000),
        method: HttpMethod::GET,
        headers: vec![
            HttpHeader {
                name: "User-Agent".to_string(),
                value: "ic-canister".to_string(),
            },
        ],
        body: None,
        transform: Some(TransformContext {
            function: TransformFunc::new(canister_self(), "transform".to_string()),
            context: vec![],
        }),
        is_replicated: None,
    };

    // http_request calls automatically attaches the required cycles
    match http_request(&request).await {
        Ok(response) => {
            let body = String::from_utf8(response.body)
                .unwrap_or_else(|_| "Invalid UTF-8 in response".to_string());

            if response.status != candid::Nat::from(200u64) {
                return format!("HTTP error: status {}", response.status);
            }

            body
        }
        Err(err) => {
            format!("HTTP outcall failed: {:?}", err)
        }
    }
}

/// Typed response parsing example
#[derive(Deserialize)]
struct PriceResponse {
    #[serde(rename = "internet-computer")]
    internet_computer: PriceData,
}

#[derive(Deserialize)]
struct PriceData {
    usd: f64,
}

#[update]
async fn get_icp_price_usd() -> String {
    let body = fetch_price().await;

    match serde_json::from_str::<PriceResponse>(&body) {
        Ok(parsed) => format!("ICP price: ${:.2}", parsed.internet_computer.usd),
        Err(e) => format!("Failed to parse price response: {}", e),
    }
}

/// POST transform: strips headers AND body because httpbin.org includes the
/// sender's IP in the "origin" field, which differs across replicas.
#[query(hidden = true)]
fn transform_post(args: TransformArgs) -> HttpRequestResult {
    HttpRequestResult {
        status: args.response.status,
        body: vec![],
        headers: vec![],
    }
}

/// POST request: Send JSON data to an external API
#[update]
async fn post_data(json_payload: String) -> String {
    let url = "https://httpbin.org/post";

    let request = HttpRequestArgs {
        url: url.to_string(),
        max_response_bytes: Some(50_000),
        method: HttpMethod::POST,
        headers: vec![
            HttpHeader {
                name: "Content-Type".to_string(),
                value: "application/json".to_string(),
            },
            HttpHeader {
                name: "User-Agent".to_string(),
                value: "ic-canister".to_string(),
            },
            // Idempotency key: prevents duplicate processing across replicas
            HttpHeader {
                name: "Idempotency-Key".to_string(),
                value: "unique-request-id-12345".to_string(),
            },
        ],
        body: Some(json_payload.into_bytes()),
        transform: Some(TransformContext {
            function: TransformFunc::new(canister_self(), "transform_post".to_string()),
            context: vec![],
        }),
        is_replicated: None,
    };

    // http_request automatically attaches the required cycles
    match http_request(&request).await {
        Ok(response) => {
            if response.status == candid::Nat::from(200u64) {
                "POST successful (status 200)".to_string()
            } else {
                format!("POST failed with status {}", response.status)
            }
        }
        Err(err) => {
            format!("HTTP outcall failed: {:?}", err)
        }
    }
}
```

### Cycle Cost Estimation

The `ic0.cost_http_request` system API computes the exact cycle cost at runtime, so canisters do not need to hard-code the formula. Both `Call.httpRequest` from the `ic` mops package (Motoko) and `ic_cdk::management_canister::http_request` (Rust) call it internally and attach the required cycles automatically. For manual use: in Motoko, `Prim.costHttpRequest(requestSize, maxResponseBytes)` (via `import Prim "mo:⛔"`); in Rust, `ic_cdk::api::cost_http_request(request_size, max_res_bytes)`.

`request_size` is the sum of byte lengths of the URL, all header names and values, the body, the transform function name, and the transform context.

For reference, the underlying formula on a 13-node subnet (n = 13) is:

```text
Base cost:                      49_140_000 cycles  (= (3_000_000 + 60_000*13) * 13)
+ per request byte:              5_200 cycles      (= 400 * 13)
+ per max_response_bytes byte:  10_400 cycles      (= 800 * 13)

IMPORTANT: The charge is against max_response_bytes, NOT actual response size.
Omitting max_response_bytes assumes the 2MB maximum (2_000_000 bytes) and costs
49_140_000 + 10_400 * 2_000_000 = 20_849_140_000 cycles (~20.85B), plus the
per-request-byte term.
```

Unused cycles are refunded when the call returns, so over-budgeting is **safe but not free**. Attached cycles leave the canister's spendable balance for the *duration* of the call, so a hand-attached margin directly caps how many outcalls the canister can have in flight before it runs out of balance. For a canister making one outcall per user action, that margin is a concurrency limit. This is why both wrappers attach the exact computed amount rather than a round number — as the `ic` mops package puts it: *"Only minimal amount of cycles are added to the call. This helps the canister to make more calls in parallel without running out of cycles."*

Do not hand-attach a buffer "to be safe". Call the wrapper, or compute the exact cost with `Prim.costHttpRequest` / `ic_cdk::api::cost_http_request` and attach that. The way to lower the cost of an outcall is a tighter `max_response_bytes`, never a larger attachment.

This formula applies on a normal **Application subnet**. It does not apply on a **cloud engine** (`CloudEngine` subnet): there, `ic0.cost_http_request` returns 0 regardless of `request_size` or `max_response_bytes`, because engines run under a free cost schedule. Load the `cloud-engine-canisters` skill for the engine's call rules before writing or debugging outcall code that will run there.

## Deploy & Test

### Local Deployment

```bash
# Start the local replica
icp network start -d

# Deploy your canister
icp deploy backend
```

Note: HTTPS outcalls work on the local replica. icp-cli proxies the requests through the local HTTP gateway.

### Mainnet Deployment

```bash
# Ensure your canister has enough cycles (check balance first)
icp canister status backend -e ic

# Deploy
icp deploy -e ic backend
```

## Verify It Works

```bash
# 1. Test the GET outcall (fetch price)
icp canister call backend getIcpPriceUsd '()'   # Motoko example above
icp canister call backend fetch_price '()'      # Rust example above
# Expected: Something like '("{\"internet-computer\":{\"usd\":12.34}}")'
# (actual price will vary)

# 2. Test the POST outcall
icp canister call backend postData '("{\"test\": \"hello\"}")'    # Motoko
icp canister call backend post_data '("{\"test\": \"hello\"}")'   # Rust
# Expected: JSON response from httpbin.org echoing back your data

# 3. If using Rust with the typed parser:
icp canister call backend get_icp_price_usd '()'
# Expected: '("ICP price: $12.34")'

# 4. Check canister cycle balance (outcalls consume cycles)
icp canister status backend
# Verify the balance decreased slightly after outcalls

# 5. Test error handling: call with an unreachable URL
# Add a test function that calls a non-existent domain and verify
# it returns an error message rather than trapping
```

### Debugging Outcall Failures

If an outcall fails:

```bash
# Check the replica log for detailed error messages
# Local: icp output shows errors inline
# Mainnet: check the canister logs

# Exact reject messages from the replica (match on these, not on paraphrases):
#
# "Timeout expired"                                                     [SysFatal]
#     The remote server did not respond within 30s.
#
# "Canister http request timed out"                                  [SysTransient]
#     The subnet did not produce a response within 60s. Retryable.
#
# "Deadline Exceeded"                                                [SysTransient]
#     The adapter did not answer the replica within its 60s deadline. Rarer
#     than the two above: the adapter's own 30s timeout usually fires first.
#
# "No consensus could be reached. Replicas had different responses.
#  Details: request_id: <id>, hashes: <...>"                         [SysTransient]
#     Transform is missing or not stripping enough non-determinism.
#
# There are THREE distinct size-limit messages, all [SysFatal], because response
# headers are counted against max_response_bytes BEFORE the body is read:
#
# "Header size exceeds specified response size limit <N>"
#     The response headers ALONE exceeded max_response_bytes.
#
# "Http body exceeds size limit of <N> bytes."
#     The body exceeded the allowance REMAINING after header bytes were
#     subtracted. Note the message prints the full cap <N>, not the remainder,
#     so the body that failed can be well under <N>. Do not read this message
#     as "my body is too big" -- it means headers + body are too big.
#
# "Transformed http response exceeds limit: <N>"
#     The Candid-encoded output of your transform exceeded max_response_bytes.
#
#     Raising max_response_bytes fixes all three. Stripping headers in the
#     transform fixes ONLY this last one: the first two are checked before
#     the transform runs.
#
# "http_request request sent with <X> cycles, but <Y> cycles are required."
#                                                              [CanisterReject]
#     Attached less than the computed cost. Use the wrapper rather than a
#     hand-picked number.
```

### Transform Debugging

If you get "no consensus could be reached" errors, your transform function is not making responses identical. Common culprits:

1. **Response headers differ** -- strip ALL headers in the transform
2. **JSON field ordering differs** -- parse and re-serialize the JSON in the transform
3. **Timestamps in response body** -- extract only the fields you need

Advanced transform that normalizes JSON:

```rust
#[query]
fn transform_normalize(args: TransformArgs) -> HttpRequestResult {
    // Parse and re-serialize to normalize field ordering
    let body = if let Ok(json) = serde_json::from_slice::<serde_json::Value>(&args.response.body) {
        serde_json::to_vec(&json).unwrap_or(args.response.body)
    } else {
        args.response.body
    };

    HttpRequestResult {
        status: args.response.status,
        body,
        headers: vec![],
    }
}
```

## Additional References

- Load `cloud-engine-canisters` for canisters running on a cloud engine, including why outcall cost drops to 0 there and why outcalls must never be routed through the engine's console proxy.
