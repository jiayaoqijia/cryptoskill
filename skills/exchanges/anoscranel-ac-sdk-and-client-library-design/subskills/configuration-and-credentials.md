---
name: configuration-and-credentials
domain: software-engineering/configuration-and-credentials
trigger: "Handling configuration and secrets inside a client library."
anti_trigger: "Not for server-side secret management, and not for authentication protocol design."
scope: "Precedence, environment, and never logging a secret."
status: seedling
---

# Configuration and credentials

## Standard

A library that reads configuration from several places must state the precedence, because a caller debugging a wrong endpoint needs to know which source won. The common arrangement is explicit argument over environment over file over default, and it is worth writing down because two libraries in the same process that disagree will produce behaviour nobody can explain.

Credentials need a stricter rule: the library should accept them, never log them, never include them in an error, and never write them to disk. A credential that appears in a stack trace or a debug log has leaked, and the leak is usually in the library's own convenience logging rather than in the caller's code. Redaction should be the library's responsibility because the library controls what it prints.

Primary sources: <https://csrc.nist.gov/> and <https://owasp.org/>.

## Decision rules

- Record the configuration sources and their precedence order.
- Record whether environment variables are read implicitly, which makes behaviour depend on the host.
- Record how a credential is supplied: constructor, environment, or a provider callback.
- Record the redaction applied to logs, errors, and any diagnostic output.
- Record whether the credential is cached and for how long, since a rotated credential must take effect.
- Record the failure mode when a credential is missing, which should be a clear error at construction rather than a puzzling request failure.

## Procedure

1. Record the sources and precedence.
2. Record implicit reads and their effect on portability.
3. Record credential supply and caching.
4. Record redaction points.
5. Record the missing-credential failure mode.
6. Write the configuration model.

## Anti-patterns

- Reading environment variables implicitly, so the same code behaves differently per host.
- A credential included in an error message or a debug log.
- Redaction implemented by the caller, who then forgets one path.
- A cached credential that ignores rotation for the process lifetime.
- A missing credential surfacing as a 401 rather than as a configuration error.

## Done checklist

- [ ] Sources and precedence recorded.
- [ ] Implicit reads recorded.
- [ ] Credential supply recorded.
- [ ] Redaction points recorded.
- [ ] Caching and rotation recorded.
- [ ] Missing-credential behaviour recorded.

The credential's lifetime also needs stating: a library that captures a credential at construction holds it for the process lifetime, which is fine for a static key and wrong for a token that expires, so the record should say whether the library refreshes and how a caller supplies a refresh callback rather than a value.


## Sources

- Security control guidance: <https://csrc.nist.gov/>
- Application security practice: <https://owasp.org/>
- Credential handling context: <https://owasp.org/www-project-top-ten/>
