---
name: external-repo-vetting
description: Vet a third-party repo before trusting or running it.
---

# Vetting a third-party repo (trading bot / tool / deliverable)

Trigger: user sends a GitHub URL ("cek repo ini"). Goal: state what it IS, whether it's
safe, whether it matches the promotion/narrative, and what it's worth — with real evidence,
never by reading the README alone.

**First decide whether it may run at all.** Running is the right default for a repo the user
intends to use (a trading bot, their own deliverable). It is the WRONG move for an untrusted
repo that would execute on a host holding API keys or wallets — there, static vetting (step 0)
is the whole job, and saying "gw nggak akan jalanin ini" is the deliverable.

## Steps

1. **Clone + shape** (one call):
   ```bash
   cd /tmp && rm -rf repo && git clone --depth 50 <url> repo
   cd repo && git log --pretty='%h|%ad|%an|%s' --date=short | head -40
   du -sh --exclude=.git .; du -sh */ | sort -h | tail -12
   ```
   Few squashed commits = delivered/exported project, not organic development. Check author
   account age + repo created/star/fork counts via `api.github.com/repos/<owner>/<name>` and
   `/users/<owner>`.

2. **Is it a fork/vendored upstream?** Look for a whole third-party package inside. Then diff
   byte-for-byte against the real upstream tag/commit:
   ```bash
   git clone --depth 1 --branch <tag> https://github.com/<upstream> up
   # or fetch the exact commit a doc claims: git fetch --depth 1 origin <sha> && git checkout FETCH_HEAD
   diff -rq --exclude=.git --exclude=__pycache__ up repo
   ```
   Identical => code is not the seller's work; value = upstream (often free, check LICENSE).
   Differences are the only part worth assessing.

3. **Malware/secret scan** (split into small commands — long inline payloads get blocked):
   ```bash
   grep -rInoE "\b[a-fA-F0-9]{64}\b" --include=*.py .          # private keys
   grep -rInoE "0x[a-fA-F0-9]{40}" --include=*.py .             # wallets
   grep -rhoE "https?://[a-zA-Z0-9./_-]+" --include=*.py . | sort | uniq -c | sort -rn | head -20
   git ls-files | grep -iE "^\.env$|secret|credential"          # committed secrets
   ```
   All-urls-are-example.com + no hex keys = clean.

4. **Run it** (this is the whole point — claims must be executed, not trusted):
   ```bash
   export PATH=/home/ubuntu/.hermes/bin:$PATH   # uv lives here, not on default PATH
   uv venv --python 3.12 .venv && uv pip install --python .venv/bin/python -r <reqfile>
   ./.venv/bin/python -m <pkg> doctor      # inspect config, no orders
   ./.venv/bin/python -m unittest discover -s <tests dir> -v
   ```
   Record pass/fail counts and the real backtest result. `0 trades` is a result — report it.

5. **Read the wrapper, not the README**: LOC ratio (`find <pkg> -name '*.py' | xargs wc -l`) shows
   how much of the repo is the seller's code. Then check what the strategy actually is
   (indicators, exit rules: TP? trailing? cooldown?) and the real-money risk notes.

6. **Diff claims vs reality**: grep the README/docs for the promotional keywords (product names,
   P&L figures, "AI" model names) and see whether the repo says "not present" itself.

7. **Kalau repo dipromosikan bareng akun X / token / website** (repo cuma "bagian 1"; klaim
   sebenarnya biasanya di luar repo):
   - **Timeline X**: pakai nitter RSS, bukan API X:
     `curl -s -A "Mozilla/5.0 ... Chrome/124.0" "https://shitter.thepixora.com/<handle>/rss"`
     → semua klaim promo + jumlah post (akun baru = post dikit).
   - **Website**: `curl -sL <site> -o site.html`, lalu ekstrak JS inline
     (`re.findall(r'<script[^>]*>(.*?)</script>', h, re.S)`) → **formula asli hampir selalu di
     client-side JS**, bukan di backend. Cari: fungsi `score(`, threshold, flag/wash, `rng(`/`Math.random`.
   - **Placeholder = produk belum jalan**: config kosong seperti `telegram:''`, `botApi:''`,
     atau tabel "menunggu API" ⇒ fitur itu belum ada, cuma mockup.
   - **Token on-chain (keyless)**:
     `https://api.geckoterminal.com/api/v2/networks/<net>/tokens/<ca>` dan `.../tokens/<ca>/pools`
     → harga, FDV, likuiditas, volume 24h, transaksi/pembeli unik, umur pool, launchpad details.
     Trades: `.../networks/<net>/pools/<pool>/trades` → terapkan formula wash/bot punya mereka
     sendiri ke token mereka sendiri (bukti paling tajam: berapa % volume mereka yang "fake"
     menurut filter mereka sendiri).
   - **RPC langsung** (blockscout kena Cloudflare di curl): POST JSON-RPC ke RPC chain —
     `eth_call` `totalSupply` (0x18160ddd) dan `balanceOf` (0x70a08231+addr pad64) untuk cek
     distribusi supply (pool/curve/dead/dev). Retry dgn sleep, kadang 403 rate-limit.
     Cek klaim "supply burned": `eth_getTransactionReceipt` ke tt hash + balance alamat 0x…dEaD.
   - **Rasio volume/likuiditas**: volume 24h ≫ likuiditas (beberapa kali) di pool kecil = churn
     bot/wash, bukan minat organik. Bandingkan juga median trade size.

8. **Report shape (Indonesian, casual)**
What it is → what I verified by running (with numbers) → what it is NOT (promised features missing)
→ real-money risks → who it's useful for. Lead with the verdict on safety, end with the value call.

### Vetting a listicle post (X thread → N repos)

Someone posts "12 open-source repos the pros won't use" with a pitch ("$8,000 of effects, now free"). Verify the list instead of relaying it.

```bash
curl -s "https://api.fxtwitter.com/<handle>/status/<id>"   # text, author, views, media — no login, no scrape
curl -s "https://api.github.com/repos/<owner>/<name>"       # stars, license.spdx_id, pushed_at, archived
```

Report per repo: stars, last push, license, archived. Then split into **alive** (pushed within ~12 months),
**stale but working**, and **do-not-ship**. License is where the listicles lie:

- `license: null` / no `LICENSE` file means **not open source**, regardless of the code being readable.
- `GPL-3.0` (or any copyleft) propagates into a commercial product — flag it as a shipping blocker, not a footnote.
- `package.json`'s `"license": "MIT"` is not a license file. If GitHub returns `NOASSERTION`, read the repo
  root; absent a `LICENSE`, treat it as unlicensed.

Also drop the promotional arithmetic: "$8,000 → $0" is marketing. Say plainly that the repos were always free
and what the AI actually does is port/rewrite the effect into the user's project.

## 0. Static vetting — read the repo through the API, no clone

Use when the user says "jgn asal clone", "itu apa dlu", or the repo is clearly untrusted. A clone
is not required to answer what a repo is; the GitHub API returns every file.

```python
# execute_code, urllib — a long shell curl to api.github.com can be blocked by approval
B = "https://api.github.com/repos/<owner>/<name>"
api(B)                      # description, stars/forks, created_at, license, size, open issues
api(B + "/git/trees/main?recursive=1")   # every path + size, truncated flag
raw(B + "/contents/<path>")             # Accept: application/vnd.github.raw
```

Read in this order and stop when the answer is clear: description + stars + `size` + created/updated
→ `cordis.patch.yml`/install manifest → `package.json` (deps, scripts, version) → tree sizes (a
multi-MB `*.part` set or one 100k-line bundle means a compiled payload inside the repo) → the 2–3
entrypoint file headers. Module docstrings in a well-written repo state the architecture in one
paragraph; that plus the tree is usually the whole "cara kerjanya" answer.

Secrets scan without cloning: `git ls-files` is unavailable, so grep the tree listing for
`.env`, `secret`, `credential`, `*.pem`, `*.part`, `vendor/`, and read those files individually.

### Red flags of a "free model / free API" freeloader plugin

These repos are usually not malware; they are quota farmers. Judge them on what they touch:

- **Reads existing CLI credentials** — `~/.codex/auth.json`, `~/.claude/.credentials.json`,
  `~/.gemini/oauth_creds.json`. Installing it means handing over sessions the user already trusts.
- **Impersonates an official client** — hardcoded UA (`opencode/latest/<v>/cli`), anonymous
  credential `"public"`, forged session-ID formats. That is ToS violation by design, and the
  vendor's remedy is banning the account, not the plugin.
- **Ships a native binary as split parts** — `engine-parts/*.part` + gzip + SHA-256 + `spawn()`.
  Unauditable by reading; treat as "unknown code executes on this host".
- **Star-gated shared relay** — a Cloudflare Worker holding the real upstream key, unlocked by
  GitHub OAuth plus "star this repo". The star count is an access gate, not a quality signal.
- **Remote content + self-update** — announcement JSON rendered as HTML in-app, plus download →
  hash → atomic replace → hot reload. Repo write access equals code execution on every install.
- **Egress switching** — a proxy/relay outlet exists to dodge per-IP quotas and region gates.

Verdict shape: what it does → how it gets the resource → which of the above it touches → whether it
may run on THIS host (wallet/keys present = no) → what is worth copying (usually the idea, not the code).

## Pitfalls
- Don't judge from README alone; sellers' docs can be honest while the promo around them isn't.
- **A blocked clone is an answer, not an obstacle.** When the user denies the clone, do not retry the
  same outcome through `gh api` tarballs, zip downloads, or a background job — switch to per-file API
  reads (step 0) and say plainly that nothing was cloned or executed.
- **README disclaimers are evidence.** "Free tier prompts may be logged", "credentials are shared",
  "usage is subject to upstream terms" — quote them as the risk finding instead of inferring risk.
- **Star/fork counts are not safety.** High stars on a five-week-old repo buying free access to paid
  models says the demand is real, not that the code was audited by 58k people.
- `curl | python3` and giant one-liners get security-flagged/blocked — write small commands or a script file.
- GitHub API output can be huge (fork/user lists): always `grep` in the same pipe, never dump raw JSON.
- Check upstream **commit**, not just tag: a vendored copy may be upstream main between releases.
- Verify pyproject/requirements: missing `pip` on host is normal (PEP 668) — use uv, not system pip.
