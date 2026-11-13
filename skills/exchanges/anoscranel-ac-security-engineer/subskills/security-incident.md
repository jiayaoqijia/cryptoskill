---
name: security-incident
domain: security-hardening/security-incident
trigger: "A suspected breach or data exposure is live now — who to call, what to isolate, what to preserve, which clocks started."
anti_trigger: "Receiving external researcher reports (subskills/vuln-disclosure.md); standing log design (subskills/security-logging.md)."
scope: "First hour of a breach: contain, preserve, notify clocks"
status: "seedling"
---

# Security Incident — First Hour

## Standard

- NIST **SP 800-61r3** (final 3 Apr 2025) supersedes the 2012 r2, mapping response onto the six CSF 2.0 functions and dropping the four-phase lifecycle (https://csrc.nist.gov/pubs/sp/800/61/r3/final). The detect→contain→eradicate→recover→notify sequence stays defensible; do not cite four phases as NIST.
- Forensic preservation runs **in parallel with containment, never after it** (14-incident cohort, ⚠️ vendor practice data). Containment is isolation, not disconnection, ordered by business criticality.
- CISA's #StopRansomware checklist: out-of-band comms (the actor may be watching), isolate, **snapshot before rebuilding**, logs before rotating, power-down last (it destroys memory evidence) (https://www.cisa.gov/stopransomware/ive-been-hit-ransomware).
- Clocks run from **awareness**, not the conclusion of investigation (GDPR Art. 33: "without undue delay and, where feasible, not later than 72 hours").

## Decision rules

1. Declare early: a false alarm costs an hour; a missed first hour costs the evidence.
2. Record the awareness moment (timestamped, human-attributed); notify on the duty clock, not on certainty — pre-draft the first notification before triage finishes.
3. Preserve before remediating: snapshots and log copies precede rotation or reimaging.
4. Rotate credentials on the affected path, revoking at the issuer first. ⚠️ Rotation and revocation are **human-gated**: propose the exact list of sessions, keys, and tokens; a human executes.
6. One voice outbound: internal comms on a channel assumed compromised, external statements through one named owner. Contradictory press is fatal.

## Procedure

1. **Minute 0–5**: switch to out-of-band comms, declare, name one incident commander, start the awareness log entry.
2. **Minute 5–15**: isolate affected hosts at the network level (snapshot cloud volumes first); isolate administrative systems before everything.
3. **Minute 15–30**: preserve logs (`subskills/security-logging.md`) and export snapshots beyond the attacker's reach; triage affected vs not.
4. **Minute 30–60**: revoke and rotate credentials on the affected path (human-gated); assess exposure against the data map (`subskills/privacy-data.md`).
5. **Clocks**, all from the awareness time: **GDPR Art. 33** — supervisory authority ≤72h; Art. 34 — data subjects, high risk only; **EU CRA Art. 14** (11 Sep 2026) — **24h** early warning, **72h** notification, final report ≤14 days after a fix, for EU-market products when *actively exploited* (watch KEV and ENISA); **India DPDP Rule 7** (13 May 2027 ⚠️) — principals without delay, Board initial without delay, detailed ≤72h; **SEC 8-K Item 1.05** — 4 business days from the **materiality determination** (a timestamped artefact).
6. Eradicate and recover behind production gates; verify before restoring service.
7. Close with a blameless review; every finding becomes an owned, dated ticket.

## Anti-patterns

- Waiting for full scope before notifying — the clock does not pause.
- Reimaging before snapshots exist, or powering the host down first.
- Debating incident status on the compromised platform; paying a ransom is an exec/legal/insurer decision, never a first-hour technical one.

## Done checklist

- [ ] Awareness moment recorded (timestamped, human-attributed); out-of-band comms; commander named.
- [ ] Isolation in criticality order; snapshots before rebuild; logs preserved off-host; scope triaged.
- [ ] Credential revocations proposed to a human and executed; applicable clocks identified (GDPR / CRA / DPDP / SEC).
- [ ] Eradication verified before restoration; findings ticketed.

## Sources

- Primary: NIST SP 800-61r3; CISA #StopRansomware checklist; GDPR Arts. 33/34 (EUR-Lex); EU CRA Art. 14 (Reg. (EU) 2024/2847); SEC Form 8-K Item 1.05 (ecfr.gov).
- <https://www.cisa.gov>
- <https://csrc.nist.gov/pubs/sp/800/61/rev-2/final>
