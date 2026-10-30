---
repo: core
parent: recipe-harness
---

# Core

Headless/state proof only. The canonical wallet fixture supplies signing accounts for Perps writes; no app unlock occurs. Prove behaviour through listed actions or a `command` that drives the controller through its public API as a client does (real messenger, mocked only at the network boundary) and asserts the observable state or event, per Recipe Cook; never a Jest or unit-test probe. Set `timeout_ms` on `command` nodes. Run package tests outside recipes through the package `test:unit:verbose` script, else `test:verbose` (sets `NODE_OPTIONS`; `test` hides test names).
