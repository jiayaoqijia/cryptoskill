# Auditing a SaaS / consumer web product ("aman ga?" — read-only)

Companion to `web-tool-audit-recipe.md`. That one reads a **crypto tool's own JS** to find out what
data it really uses. This one is for a **product, app or platform** with no chain attached
(privacy tools, OSINT services, AI SaaS, dashboards) where the user's question is *"is this safe?"*
and the honest answer is never a single word.

What changes vs the DeFi ladder: custody, fees, audits, TVL are irrelevant. The axes that decide the
answer are **who runs it · what it does with the identifiers you must hand over · which marketing
claims are checkable**.

## The 8 rungs

| # | Rung | Command / source | What it yields |
|---|---|---|---|
| 1 | Legal identity | the privacy policy's "Who we are" | legal name, jurisdiction, street address |
| 2 | Domain | registry WHOIS (see below) | creation date, registrar, whether registrant is hidden |
| 3 | Operator footprint | `curl -s https://api.fxtwitter.com/<handle>` | account age (snowflake), followers, real website |
| 4 | Product & pricing | the site's own pages + `/ai-info`-style LLM page | tiers, what it actually does, what it claims |
| 5 | Checkable claims | iTunes Search API, Play developer page | do the advertised apps exist? |
| 6 | The data ask | the policy's "what we collect" | exactly which identifiers the user must submit |
| 7 | Sharing / retention | the policy's share + retention sections | sub-processors, legal requests, how long each class lives |
| 8 | Reputation | ScamAdviser / Scam Detector / Gridinsoft + real user threads | weak signals only — never the verdict |

### 1. Identity — read the address, not the vibe

Real policy text is worth more than the footer: `ANON AI Labs, Inc., a Delaware corporation`,
`95 3rd St, 2nd floor, PMB 17574963, San Francisco, CA 94103`. A **PMB / suite number is a
mailbox**, not a verified HQ — report it as such (risk note, not fraud proof). Presence of a
GDPR-style apparatus (DPA, sub-processor list, a named EU/UK/CH representative such as Prighter, a
`dpo@` address, CCPA rights section) is itself evidence of a real operating entity. This user's
framing: "policy-nya serius kelas perusahaan normal, bukan template scam."

### 2. Domain age + registrar

`rdap.org/domain/<d>` returns nothing for `.ai`. Query the registry on port 43 instead:

```bash
python3 - <<'EOF'
import socket
def whois(server, q, port=43):
    s = socket.create_connection((server, port), timeout=15); s.sendall((q+"\r\n").encode())
    buf = b""
    while True:
        d = s.recv(4096)
        if not d: break
        buf += d
    return buf.decode(errors="ignore")
for line in whois("whois.nic.ai", "serus.ai").splitlines():
    if any(k in line.lower() for k in ("domain","creat","expir","registrar","status","name server","registrant","org")):
        print(line.strip()[:140])
EOF
```

- `Creation Date` = product age. A 10-month-old domain with a company entity behind it is a
  different risk class from a 2-week-old one.
- `Registrant Organization: Domains By Proxy` = identity deliberately concealed → **weight it, and
  say it plainly**; it is a risk factor, not proof of fraud.

### 3. Operator footprint

`api.fxtwitter.com/<handle>` returns followers, tweet count, bio and the numeric id; the snowflake
decodes to the signup date (`((id >> 22) + 1288834974657) / 1000`). Cross-check the bio's website
equals the domain under audit. In the worked case: account Jan 2025, 27.8K followers, 16 tweets,
bio "Agentic privacy" — consistent with an ad-driven startup, plausible.

### 4. Product, pricing, claims

Marketing sites are Astro/Framer-ish and often ship a machine-readable page for LLMs
(`/ai-info`, `/llms.txt`) — the cleanest source for what the product claims to do and its tiers.
Copy the tier table into the report verbatim (Free / $12.99 / $14.99 etc.). Volume of claims ≠
verification: list each claim in a separate "NOT verified" block.

### 5. Checkable claims — apps and logos

- **Advertised app listings are checkable.** `curl -s "https://itunes.apple.com/search?term=<name>&entity=software&limit=200"` and filter results for the brand token; the Play side is
  `play.google.com/store/apps/developer?id=<Dev+Name>` (a `Not Found` title is a real signal).
  In the worked case the site displayed "Download on the App Store / Google Play" badges while
  **no app by that name was findable** in US search — report as *not confirmed* (region limits
  exist), never as "the app is fake".
- **Logo walls are bragging, not customers.** "Used by people at Warner Bros. / PwC / Meta /
  Cloudflare / Google / Amazon" — note the hedge "**people at**". Same for self-reported user
  counts and undisclosed funding rounds ("announces fundraising, amount not stated").
- Apple's API is keyless and country-scoped; absence of a title match is evidence about *that*
  storefront only.

### 6. The data ask — the real answer to "aman ga?"

For a privacy/OSINT product the user must submit exactly the identifiers they want to protect:
name, email, login tokens, billing, **search queries and monitoring targets (emails, phone
numbers)**, and — if they connect a messaging channel — the channel identifier *and message
contents*. Say this out loud: **what is at risk is your data, not your money.** Then give a usage
rule set (burner email, no real phone/wallet, free tier first, test export/delete before paying,
don't look up third parties — the legal exposure is on the user).

### 7. Sharing + retention — quote the hedge, don't paraphrase it

Pull the policy body (see the reader-proxy note in `blocked-page-recovery`) and quote verbatim:

- `"We do not sell your personal information in the traditional sense."` — the qualifier is the
  finding. Say what sharing *does* happen: sub-processors (hosting/analytics/payment/support),
  removal requests forwarded to third parties, **legal/process disclosure**, business transfers.
- Retention usually splits by class: account + customer content = life of account; exposure-alert
  metadata **60 days**; security/operational logs **~90 days**; billing records **up to 7 years**
  (tax). Print the split, not a single "they keep your data".
- AI clause: data sent to third-party AI providers for **inference only**, not retained for
  training (as claimed) — attribute it as a claim.

### 8. Reputation signals — weak, contradictory, still worth one line

ScamAdviser / Scam Detector / Gridinsoft are automated and disagree with each other (in the worked
case: "slightly low trust / owner hiding identity" vs "probably legit"). Cite them as weak signals
with their score, then lead with real user threads (Reddit etc.): one 5-month paying user who was
happy and compared it favourably to Incogni, one tester who used a fake identity and found real
breach hits but called the legal protection absent. **Neither side alone is the verdict.**

## Verdict shape (what the user actually wants)

Not a score — a sentence plus rules:

> Bukan scam generik (entitas, policy, harga, docs rapi). Risiko utamanya bukan duit ilan, tapi
> data: buat pakai lu wajib nyerahin identifier yang mau dilindungi. Aman dipakai **dengan
> syarat**: email burner · jangan nomor HP/wallet asli · Free dulu · tes export+delete sebelum
> bayar · jangan dipakai ngintip orang lain.

Then close with the **priority action** (e.g. read the `/legal/subprocessors` list to see where the
data flows) and offer it with "gas" — never "mau gw buatkan?".

## Not-verified handling (mandatory)

Split the report into **verified ✅** and **not verifiable ⚠️** blocks. "Not found" ≠ "false":
"App-nya nggak gw temuin di pencarian App Store/Play (bisa region-limited) — status: **belum
terkonfirmasi**, bukan terbukti bohong." Same wording discipline as the DeFi ladder's rung 8.

## Worked case — serus.ai (5 Oct 2026)

User dropped `https://www.serus.ai/` with "serus ai, itu aman ga? coba cek in".

- Operator **ANON AI Labs, Inc.** (Delaware C-corp), SF address with **PMB 17574963**; origins in
  Sweden; founders Filip Landgren PhD (CEO) + Anthon Wansland; X `@serus_ai` (Jan 2025, 27,787
  followers, 16 tweets); funding announced 9 Sep 2026, **amount not disclosed**; 300K registered
  users claimed 24 Aug 2026 (self-reported).
- Domain registered **2025-12-09**, GoDaddy, **Domains By Proxy** registrant, Cloudflare NS.
- Product: footprint discovery (data brokers/people-search/public records), agentic OSINT (email,
  phone, username, name, domain, **wallet**), dark-web + breach lookups, automated removal +
  Autopilot, Developer API + MCP. Tiers: Free $0 (5 removals/day) · Intelligence $12.99/mo ·
  Protection $14.99/mo ($8.25 annual).
- **Not verified:** logo wall ("people at" Meta/Google/PwC/…), 300K users, funding amount, and the
  advertised App Store / Play apps (none findable from here).
- Policy: `"do not sell … in the traditional sense"`; retention 60-day alert metadata / ~90-day
  logs / up to 7-year billing; AI inference-only clause; export+delete from settings; Prighter rep
  for EU/UK/CH; `dpo@serus.ai`.
- Reputation: ScamAdviser low-medium ("owner hiding identity"), Scam Detector medium-low, Gridinsoft
  67/100 on the app subdomain; Reddit both a happy 5-month subscriber and a skeptical tester.
- **Brand-jacking bonus:** many `$SERUS` tokens exist across Solana/Base. The Solana pump.fun mint
  `8LQMfD6ASyqw4w9YpC8M5Ge8eo3By9TBKi5e6waspump` carried the real X handle + website in its GMGN
  link fields while being **dead** (3 holders, 24h volume 0, SOL side of the pool $0.17, LP burned,
  mint/freeze renounced, created 25 Sep 2026, never migrated). Verdict: **not the project's token —
  avoid**, and say it before the user confuses the two.

Vault note: `~/obsidian-vault/Ide Project - Serus AI.md`.
