# GraphQL Framework Config Reference

Where each control lives, per framework. Severities in SKILL.md Step 1.

## Apollo Server 2/3 (`apollo-server`, `apollo-server-express`)

```js
new ApolloServer({
  typeDefs, resolvers,
  introspection: process.env.NODE_ENV !== 'production',  // default: disabled in prod
  playground: process.env.NODE_ENV !== 'production',     // same
  debug: false,                                           // stacktrace leakage (default false)
  formatError: (err) => ({ message: err.message }),       // mask everything else
  validationRules: [require('graphql-depth-limit')(10)],  // NOT built-in — absence = finding
});
```
Absence of `introspection: false` is only safe if `NODE_ENV=production` is
actually set in deploy configs — check Dockerfile/CI/compose for `NODE_ENV`.

## Apollo Server 4 (`@apollo/server`)

```js
new ApolloServer({
  schema,
  introspection: false,
  includeStacktraceInErrorResponses: false,  // default false; true = finding
  csrfPrevention: true,                      // default TRUE — explicit false = finding
  validationRules: [depthLimit(10)],
});
```
Field suggestions: use plugin to mask "Did you mean" (e.g. `graphql-no-suggest`)
— Apollo does not mask by default.

## express-graphql

```js
graphqlHTTP({ schema, graphiql: false, introspection: false })  // both default true in older versions
```
Older versions (<0.12) have no `introspection` flag — version-dependent finding.
GET mutations: `graphqlHTTP` accepts queries via GET by default → CSRF risk with cookies.

## graphql-yoga (v3/v4)

```js
createYoga({ schema, graphiql: false, logging: 'warn',
  plugins: [{ onExecute: ... }] /* depth limit via graphql-rate-limit / custom */ })
```
Yoga masks stack traces by default in prod (`maskError`). Depth limit not built in.

## Mercurius (Fastify)

```js
app.register(mercurius, { schema, graphiql: false, ide: false })
```

## Python — graphene / ariadne / strawberry

- GraphiQL: flask-graphql/`graphql-server` `graphiql=True` in prod → finding
- No built-in depth limit in any of the three → absence of `graphql-depth-limit`-equivalent
  (e.g. `graphene-validation` depth rule, custom `ValidationRule`) = High finding
- Strawberry: `extensions` for error masking; debug mode via `debug=True` → finding

## Go — gqlgen

- `gqlgen.yml`: `introspection: true` block (default enabled); complexity:
  `complexity: { field: ... }` / `max_query_complexity` in resolver config —
  absent = DoS finding
- Automatic persisted queries not default → note

## Hasura (config via env)

- `HASURA_GRAPHQL_ADMIN_SECRET` missing/weak → CRITICAL (unauthenticated admin API)
- `HASURA_GRAPHQL_ENABLE_ALLOWLIST` false (default) → arbitrary queries allowed, Medium
- `HASURA_GRAPHQL_DEV_MODE=true` in prod → Medium
- Check docker-compose/k8s env for all three.
