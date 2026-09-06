# Limits the agent cannot raise

Derived from [`/for-agents/concepts/policy-controls`](https://docs.waap.human.tech/for-agents/concepts/policy-controls)
and [`/for-agents/concepts/approvals-and-notifications`](https://docs.waap.human.tech/for-agents/concepts/approvals-and-notifications).

## Where the check happens

The policy gate sits **in front of the key**, server-side, and runs before a
signature exists. On a signing request:

1. **The exact bytes are verified.** The transaction that was reviewed is the
   transaction that gets signed. A client that renders one thing and submits
   another does not get a signature.
2. **The policy engine returns one verdict.** Spend limits, risk thresholds and
   approval rules apply regardless of what the caller asked for.
3. **The approval is single-use.** It is bound to one user, one transaction
   digest and one operation, then burned before signing.
4. **The signer re-verifies independently** before producing a signature.

The agent participates in none of these steps. That is the property that makes
the limit a control rather than a note.

## Setting a limit

```bash
waap-cli policy set --daily-spend-limit 100   # whole USD, 0–10,000
waap-cli policy get
```

The policy is three fields. Authentication method, risk threshold, and a daily
USD limit. And it is universal: one rule, authored once, with no chain
dimension. Do not design around per-contract or velocity limits; they are not
shipped.

## The limit is a threshold, not a stop

**Crossing the daily limit does not halt the account. It summons the human.** The
policy engine's outcomes include waiting for authorization alongside outright
rejection, and the 2FA path exists precisely so a request above the line can be
approved rather than dropped.

This matters more than it sounds, because it decides how the agent's code is
shaped:

```
verdict → accepted        → signature proceeds
        → needs authz     → a human is asked; the request resumes on approval
        → rejected        → the request is refused
```

An agent that collapses the middle branch into the third stops working the first
time it does its job correctly. Handle it as a wait, not an error, and never
retry it in a loop. The human has already been asked, and retrying just
generates noise.

Some things the daily limit does not gate at all: self-sends, swaps of any size,
and typed data that settles off-chain. State those carve-outs rather than
implying the limit covers everything.

## Why an in-agent check is not a boundary

A limit enforced inside the agent's own loop is evaluated **after** the agent has
decided, by code the agent can read and, in most runtimes, edit. Two failures
follow:

- **Prompt injection reaches the check.** An attacker who can influence the
  agent's context can influence anything the agent computes, including whether it
  believes it is under a limit.
- **A capable agent can rewrite its own config.** If the limit lives in a file the
  agent can open, the limit is a suggestion.

The published agent-loss incidents share this shape. The control existed in the
same trust domain as the thing being controlled.

Write the limit where the agent cannot reach it, and let the request be decided
server-side.

## What the gate actually checks

Four engine behaviours, distinct from the three fields you author:

- **Simulation**: the most conservative result across providers wins.
- **Recipient address reputation** and a requesting-domain check against known
  malicious lists; the higher risk wins.
- **Address binding**: your real addresses are re-derived server-side, so a
  compromised client cannot name an unrelated address to dodge the limit.
- **Escalation** above your risk threshold, resumed by one approval.

Simulation is an input and can fail. Do not present these as fields a developer
configures.

## Human approval

For anything above the line, the gate requires a second factor from the person
rather than the agent: a human-readable description of what is about to happen,
and an approval sent out of band. The agent proposes; the human approves; the
protocol enforces.

## Reviewing an agent that touches money

Check these in order. The first three are disqualifying.

- [ ] No private key or seed phrase in the environment, the prompt, the tool
      definitions, or anything a tool can read back.
- [ ] No spend limit whose only enforcement is agent-side code.
- [ ] No delegated grant without a recipient allowlist, a ceiling and an expiry.
- [ ] No Privilege passed in argv. `--privilege-stdin` only.
- [ ] Escalation is handled as a distinct branch from rejection, and neither is
      retried blindly.
- [ ] Dry run is the default, and enabling spend required a deliberate number.
- [ ] The account is funded for the chain it settles on, so failures are real
      failures rather than empty balances.
- [ ] Each agent has its own `WAAP_CLI_SESSION_DIR`.
- [ ] Nothing arriving from outside the agent (a token, an NFT, a tool result,
      a webhook body) can widen what the agent may do. Authority comes from the
      gate, never from inbound data.

That last one is the lesson of the incidents where an inbound asset carried
permissions with it. Nothing that arrives in a wallet should be able to grant
anything.
