# JSON Responses: Parsing and Normalizing

Two things that come up on almost every outcall to a JSON API, kept out of `SKILL.md` because
neither is specific to outcalls.

## Parsing a typed body

`fetch_price` is the GET example from `SKILL.md`.

```rust
use serde::Deserialize;

#[derive(Deserialize)]
struct PriceResponse {
    #[serde(rename = "internet-computer")]
    internet_computer: PriceData,
}

#[derive(Deserialize)]
struct PriceData {
    usd: f64,
}

#[ic_cdk::update]
async fn get_icp_price_usd() -> String {
    let body = fetch_price().await;

    match serde_json::from_str::<PriceResponse>(&body) {
        Ok(parsed) => format!("ICP price: ${:.2}", parsed.internet_computer.usd),
        Err(e) => format!("Failed to parse price response: {}", e),
    }
}
```

Needs `serde = { version = "1", features = ["derive"] }` and `serde_json = "1"`.

## Normalizing field order in a transform

If replicated consensus fails because the server serializes JSON fields in a different order per
response, parse and re-serialize in the transform. `serde_json::Value` orders object keys
deterministically, so this makes the bodies byte-identical across nodes.

```rust
use ic_cdk_management_canister::{HttpRequestResult, TransformArgs};

#[ic_cdk::query(hidden = true)]
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

Two cautions. This costs instructions proportional to the body size, so declare
`with_expected_transform_instructions` accordingly under pricing version 2 (see
`references/pricing-version-2.md`). And it does not help with values that differ per node, such as
timestamps or an echoed caller IP: for those, extract only the fields you need.
