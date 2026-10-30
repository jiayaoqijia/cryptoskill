# Review PR worked example

This example is illustrative. Rediscover every action, field, selector, and recipe ref in the active checkout.

## PR claims and frozen review contract

PR body:

> When the user changes order type to Limit, the limit-price field is visible and Market remains available.

Changed UI code adds `data-testid="order-type-toggle"` and `data-testid="limit-price-input"`.

Freeze this contract:

| # | Acceptance criterion | Source | Proof mode | Planned proof | Preconditions |
|---|---|---|---|---|---|
| 1 | When the user changes order type to Limit, the limit-price field is visible and Market remains available. | authored: PR body | visual | Select Limit; exact wait/assert for limit-price input; screenshot | Review account already has no matching BTC position or order on the selected testnet |

```text
Adapter: extension
Proof profile: extension-cdp-live
Recipe decision: generate-ui
Target environment: fullscreen
Known limitations: none

Continue from this frozen basis.
```

## Recipe skeleton after contract freeze

Assume current discovery confirms `metamask.perps.start_state`, `metamask.perps.teardown_state`, `ui.press`, `ui.wait_for`, and `ui.screenshot` with the fields below. The selector values came from this PR's diff.

```json
{
  "$schema": "https://farmslot.io/schemas/recipe-v1.schema.json",
  "description": "Prove the Limit order form acceptance criterion.",
  "paramsSchema": {
    "type": "object",
    "additionalProperties": false
  },
  "workflow": {
    "entry": "setup-clean-market",
    "teardown": "teardown-clean-market",
    "nodes": {
      "setup-clean-market": {
        "action": "metamask.perps.start_state",
        "network": "testnet",
        "market": "BTC",
        "page": "market_details",
        "positions": {
          "state": "none"
        },
        "orders": {
          "state": "none"
        },
        "intent": "Open BTC Perps and assert that the required testnet state already holds.",
        "next": "ac1-select-limit"
      },
      "ac1-select-limit": {
        "action": "ui.press",
        "test_id": "order-type-toggle",
        "intent": "Select the Limit order form.",
        "next": "ac1-assert-limit-price"
      },
      "ac1-assert-limit-price": {
        "action": "ui.wait_for",
        "test_id": "limit-price-input",
        "expected": "visible",
        "intent": "Confirm the Limit price field is visibly available.",
        "next": "ac1-assert-market-option"
      },
      "ac1-assert-market-option": {
        "action": "ui.wait_for",
        "test_id": "market-order-option",
        "expected": "visible",
        "intent": "Confirm the Market order option remains visibly available.",
        "next": "ac1-screenshot-limit-form"
      },
      "ac1-screenshot-limit-form": {
        "action": "ui.screenshot",
        "path": "evidence-ac1-limit-form.png",
        "label": "AC1 — Limit price field visible",
        "intent": "Preserve the visible Limit form as reviewer evidence.",
        "next": "done"
      },
      "done": {
        "action": "end",
        "status": "pass"
      },
      "teardown-clean-market": {
        "action": "metamask.perps.teardown_state",
        "market": "BTC",
        "positions": {
          "state": "none"
        },
        "orders": {
          "state": "none"
        },
        "intent": "Assert that the final BTC Perps state still holds after proof.",
        "next": "teardown-done"
      },
      "teardown-done": {
        "action": "end",
        "status": "pass"
      }
    }
  }
}
```

Extension `start_state` and `teardown_state` only navigate, observe, and assert;
they do not create, close, or cancel financial state. Establish mutable financial
preconditions through an explicitly authorized funded leaf or outside the proof,
then state that dependency in the frozen contract. The selector values must come
from the current PR and action discovery. The revert test is: reverting the PR
must make at least one AC assertion fail.

## Example final report

```markdown
## QA review

**PR:** https://github.com/MetaMask/metamask-extension/pull/12345
**Validated head:** 0123456789abcdef0123456789abcdef01234567
**Platform/proof profile:** extension / extension-cdp-live
**Overall verdict:** PASS
**Reviewer recommendation:** READY FOR HUMAN REVIEW
**Run evidence:** temp/tasks/recipe-cook/<review-task>/artifacts/recipe-run

| # | Acceptance criterion | Source | Proof mode | Recipe nodes | Evidence | Verdict | Rationale |
|---|---|---|---|---|---|---|---|
| 1 | When the user changes order type to Limit, the limit-price field is visible and Market remains available. | authored: PR body | visual | `ac1-select-limit`, `ac1-assert-limit-price`, `ac1-assert-market-option`, `ac1-screenshot-limit-form` | `evidence-ac1-limit-form.png`; `trace.json` | PASS | Both exact visibility assertions executed successfully, and the screenshot shows both controls in the Limit form. |

**Trace:** 8/8 nodes passed; 0 failed.
**Untestable:** none
**Notes:** The recipe established and restored a clean BTC testnet market state. No PR-specific runtime warnings were recorded.

### Validated findings

- None.
```
