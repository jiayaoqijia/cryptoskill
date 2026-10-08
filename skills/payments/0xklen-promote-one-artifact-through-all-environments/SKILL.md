---
name: promote-one-artifact-through-all-environments
description: Use when builds differ per environment and "it worked in staging" fails in prod. Builds once and promotes the identical artifact through each stage with only inputs changing.
---

# Promote one artifact through all environments

If each environment builds its own image you are not testing a release, you are testing rebuilds and hoping they match. Build once, promote the same bytes.

## Procedure

1. Build the artifact once in CI and tag it immutably with the commit SHA:
       docker build -t registry.acme.com/app:git-$(git rev-parse --short HEAD) .
2. Deploy that exact tag to every environment; never rebuild per stage:
       image = "registry.acme.com/app:git-${var.git_sha}"
3. Pass the SHA through the pipeline as the single release identifier; the deploy job resolves nothing by `latest`.
4. Vary only inputs that are environment-specific and non-code: instance size, replica count, secrets, feature flags.
5. Record which SHA is live per environment so you can prove staging and prod ran the same bytes:
       kubectl -n prod get deploy app -o jsonpath='{.spec.template.spec.containers[0].image}'
6. Sign the artifact and verify the signature at deploy so a promoted image is provably the built one.
7. Keep environment config in code (`<env>.tfvars` or values files) and diff them; only declared keys may differ.
8. Roll back by promoting the previous SHA, not by rebuilding an older branch.

## Pitfalls

- `latest` tags, so "the same image" is a different image after the next push.
- Rebuilding in staging for a config tweak, so prod gets a different binary than what was tested.
- Promoting the image but hand-editing the env config, so prod config differs from what staging ran.
- Mutable tags overwritten by a later build, so a promo silently redeploys different bytes.
- Reusing one shared tag across parallel builds, so which SHA is live becomes unknowable.

- A registry that allows tag overwrites, so a promoted `git-abc123` is silently replaced by a rebuild.
- Building a different architecture in CI than prod runs (amd64 build, arm64 nodes), so the promoted bytes will not start.

## Verification

    kubectl -n staging get deploy app -o jsonpath='{...image}'
    kubectl -n prod    get deploy app -o jsonpath='{...image}'   # identical tags

Report: the artifact tag, the live tag per environment (should all match), and the signature verification result.
