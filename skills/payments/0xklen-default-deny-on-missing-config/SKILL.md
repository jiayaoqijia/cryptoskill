---
name: default-deny-on-missing-config
description: Use when a missing env var, empty policy file or absent feature config could be read as "allow all" — makes absence resolve to deny and refuses to boot on required config.
---

# Default deny on missing config

The dangerous value of a config lookup is not a wrong value — it is *no value*. A missing allow-list read as empty often means "everyone allowed"; a missing secret read as empty string often means "no signing". Make absence a denial, and make required config a startup failure.

## Procedure

1. Enumerate config that changes a security or safety outcome: allow-lists, deny rules, key material, resource caps, kill-switch defaults, auth modes. For each, decide what an *unspecified* value means. It should almost always be the restrictive one.

2. Parse required config at startup and fail closed: refuse to boot if anything mandatory is missing or empty. Fail loud at boot, not silently at first request:
       required = ["DATABASE_URL","SIGNING_KEY","POLICY_PATH"]
       missing = [k for k in required if not os.environ.get(k)]
       if missing: raise SystemExit(f"missing required config: {missing}")

3. Represent policy as an explicit object with no ambiguous zero value. A struct that defaults to `{Allowed: false}` is safe; a bare `[]string` allow-list that defaults to empty and is then checked with `if contain(list, x)` is a fail-open waiting for a typo:
       if len(cfg.AllowList) == 0 { return false }   // empty == deny, not "allow all"

4. Distinguish "config absent" from "config present but empty" only when you mean to. An empty-but-set key may legitimately mean "deny all"; a missing key means "misconfigured". Log the difference.

5. Validate the *shape* too, not just presence: a `POLICY_PATH` that points at a missing file, an unparseable JSON, or a key with the wrong type must also fail at boot. `json.Unmarshal` into a typed struct and reject unknown fields (`DisallowUnknownFields`) so a typo'd key is an error, not a silent default.

6. For hot-reloaded config, keep the last-known-good and never fall back to permissive on a parse error. On reload failure, keep serving the old policy and alert.

7. Snapshot the effective config (redacting secrets) at startup and expose it on an admin endpoint, so during an incident you can see what the process actually loaded rather than what the file was supposed to say.

## Pitfalls

- An empty allow-list treated as "no restriction" — the single most common fail-open, and invisible in code review because the list is empty in prod.
- Defaulting a missing `MAX_ROWS` / `MAX_AMOUNT` to zero and then treating zero as "unlimited" instead of "none".
- Reading config at first use rather than boot, so the service starts healthy and only fails on the one request that needed the missing value.
- A hot-reload that parses a half-written file and applies the partial result, silently dropping half the policy.

## Verification

    # boot with config missing and confirm it refuses to start
    env -u SIGNING_KEY ./app ; echo "exit=$?"            # expect non-zero, clear message
    # boot with an empty allow-list and confirm deny
    SIGNING_KEY=x POLICY='{"allow":[]}' ./app
    curl -s -o /dev/null -w '%{http_code}\n' localhost:8080/protected   # expect 403
    curl -s localhost:8080/admin/config | jq '.policy'                   # shows effective, redacted

Report: the config keys that gate an outcome, the default chosen for each (and why), proof the process refuses to boot without required config, and an empty allow-list denying rather than allowing.
