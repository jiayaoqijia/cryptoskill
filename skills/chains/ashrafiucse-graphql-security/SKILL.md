---
name: graphql-security
description: Audits GraphQL APIs for security misconfiguration and abuse — introspection/GraphiQL/playground exposed in production, missing query depth and complexity limits, resolver-level authorization gaps and IDOR, error/stacktrace/field-suggestion leakage, query-batching abuse, CSRF with cookie auth, and unbounded custom scalars. Covers Apollo, graphql-yoga, express-graphql, graphql-js, graphene/strawberry/ariadne, gqlgen, Hasura. Use when the project has a GraphQL server, .graphql schema files, or GraphQL dependencies.
license: MIT
---

# GraphQL Security

## Step 0 — Detect the stack

```bash
rg --files -g '*.graphql' -g '*.graphqls' | head
rg -n "apollo-server|@apollo/server|graphql-yoga|express-graphql|mercurius|graphene|strawberry-graphql|ariadne|gqlgen|hasura" -g 'package.json' -g 'requirements*.txt' -g 'pyproject.toml' -g '*.go' -g 'docker-compose*.yml' | head
```

Record: server library + version, whether schema is code-first or SDL, where
resolvers live, how auth reaches context (header token vs session cookie).

## Step 1 — Server configuration checks

Per-framework config locations: `references/frameworks.md`. Checks and default
severities (adjust with context):

| Check | Finding if present/absent | Severity |
|---|---|---|
| Introspection enabled in prod config | full attack-surface disclosure | Medium (High if admin/internal types visible) |
| GraphiQL / Playground / Apollo Sandbox reachable in prod | interactive query console for attackers | Medium |
| No query depth **or** complexity limit | nested-query DoS (`{a{b{c{...}}}}` bombs) | High |
| `formatError` returns `originalError`/stacktrace; Apollo `includeStacktraceInErrorResponses`/`debug` on | internal error leakage | Medium |
| Field suggestions not masked in prod ("Did you mean..." hints) | schema oracle for attackers | Low/Medium |
| Query batching enabled unbounded (`shouldBatch`, array bodies) | auth-brute-force in one request | Medium |
| Cookie-session auth + no CSRF protection (Apollo v4 `csrfPrevention: false`/absent) | cross-site mutation execution | High |
| Mutations accepted over GET (express-graphql) | CSRF + logging of creds in URLs | High |
| No persisted operations / allowlist for public clients | arbitrary query crafting | Low (note) |

## Step 2 — Resolver authorization (the #1 GraphQL bug source)

```bash
rg -n "Query:|Mutation:|Subscription:|resolve\(|fieldResolver|@auth|@hasRole|context\.user|ctx\.user" --type js --type ts --type py --type go | head -40
```

For every resolver returning or mutating objects:
- **Field-level authz missing**: `User.passwordHash`, `User.email`, admin/internal types returned to unauthenticated callers → HIGH (CRITICAL for credentials/PII)
- **IDOR**: `user(id)` resolved without ownership/scope check → same class as REST IDOR, HIGH
- **Subscription auth**: `subscribe` handlers skipping auth → Medium/High
- **Trust of client args**: `role`, `isAdmin`, `price`, `userId` taken from args without server-side derivation → HIGH

## Step 3 — Schema & input review

```bash
rg -n -i "admin|secret|token|impersonate|delete|export|password" -g '*.graphql' -g '*.graphqls' | head -30
```

- Sensitive-named types/mutations without a guard (directive or resolver check) → flag per Step 2
- Custom scalars without `validation` (unbounded `Int`/`String` into loops/DB `LIMIT`) → Medium
- Login/reset/signup mutations without rate limiting (GraphQL bypasses REST limiters!) → High
- Default pagination `first`/`last` unbounded (`allUsers` returns everything) → Medium

## Reporting

Evidence = config lines + resolver code + schema lines. Fixes are one-liners in
most frameworks — give the exact snippet from `references/frameworks.md`
(`introspection: false`, `validationRules: [depthLimit(10)]`, `csrfPrevention: true`,
masked `formatError`). Note positives (allowlists, persisted queries, field-level directives).
