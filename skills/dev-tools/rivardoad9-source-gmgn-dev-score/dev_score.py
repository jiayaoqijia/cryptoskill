#!/usr/bin/env python3
"""Dev-score data collection and calculation.

Usage:  python3 dev_score.py <chain> <dev_address> [max_pages] [mode]

  chain        sol | bsc | eth | base | tron | ...
  dev_address  the wallet that launched the coins
  max_pages    buy/sell pages to walk, 20 rows each (default 25)
  mode         default | brief   (brief skips the cross-wallet exit check)

Prints ONE JSON object to stdout and nothing else; progress notes go to stderr.

The JSON is measured facts plus the score terms derived from them. It carries no
wording, no language and no layout: what the reader sees is written by the caller
from these numbers. Every string that came from the API and could be chosen by an
attacker (token symbols, destination addresses) is sanitised before it enters the
object, so the caller may quote it directly.

Scoring model: references/scoring.md.  API fields: references/fields.md.
"""
import json, math, os, re as _re, subprocess, sys, time

argv      = sys.argv[1:]
if len(argv) < 2:
    sys.exit(__doc__)
CHAIN     = argv[0]
DEV       = argv[1]
MAX_PAGES = int(argv[2]) if len(argv) > 2 and argv[2] else 25
MODE      = argv[3] if len(argv) > 3 and argv[3] else 'default'
TOP_K     = 20                      # coins the dump analysis must have COMPLETE data for
MIN_GAP_S = 0.35                    # min seconds between CLI calls - paces under the limiter

# gmgn-cli ALREADY retries a 429 by waiting until the server's x-ratelimit-reset header,
# plus a 1s buffer - the authoritative instant, which is exactly what must not be guessed.
# It just refuses to wait longer than GMGN_RATE_LIMIT_AUTO_RETRY_MAX_WAIT_MS (default 5000),
# so a ~45s ban leaks out as an error instead. Raise the cap and the CLI absorbs the ban
# itself, on the header rather than on a regex, and never lands on the reset boundary.
ENV = dict(os.environ, GMGN_RATE_LIMIT_AUTO_RETRY_MAX_WAIT_MS='90000')

_last_call, _gap = 0.0, MIN_GAP_S

def note(msg):
    """Progress and rate-limit notes. stderr, so stdout stays parseable JSON."""
    print(msg, file=sys.stderr, flush=True)

def emit(obj):
    json.dump(obj, sys.stdout, ensure_ascii=False, default=float)
    sys.stdout.write('\n')
    raise SystemExit

def dw(t):
    """Display width. A CJK char occupies two terminal columns, so safe()'s length
    budget has to be measured in columns, not characters."""
    import unicodedata
    return sum(2 if unicodedata.east_asian_width(c) in 'WF' else 1 for c in str(t))

# ── house helpers ─────────────────────────────────────────
def run_cli(args, timeout=40, tries=3):
    """Two distinct rate-limit failures, two distinct waits.

    Soft: exit 0 with empty stdout — a short backoff clears it.
    Hard: HTTP 429 RATE_LIMIT_BANNED — the message carries the reset time. Retrying
    at or before that instant EXTENDS the ban by 5s (up to 5 minutes), so wait for the
    stated window plus a margin, never poll the boundary. One dev at a time still
    trips this: a 500-launch dev needs 12 activity pages at weight 3 each.
    """
    import re as _re
    global _last_call, _gap
    for k in range(tries):
        # Pace, don't recover. The limiter is rate=20 capacity=20; a weight-3 route
        # sustains ~6.7 req/s, but violations ACCUMULATE into a ban across runs, so
        # stay well under. 0.35s between calls costs ~6s on a 16-page walk and is the
        # difference between finishing and being banned for 45s at a time.
        wait_gap = _gap - (time.time() - _last_call)
        if wait_gap > 0: time.sleep(wait_gap)
        _last_call = time.time()
        r = subprocess.run(['gmgn-cli'] + args + ['--raw'], capture_output=True, text=True,
                           timeout=timeout, env=ENV)
        if r.returncode == 0 and r.stdout.strip():
            return json.loads(r.stdout)
        err = (r.stderr or '') + (r.stdout or '')
        _gap = min(8.0, _gap * 2)       # any limit signal: halve the pace for the REST of the run,
                                        # so one hiccup does not become a ban. Self-tunes to whatever
                                        # quota the key actually has, without hardcoding the window.
        if '429' in err or 'RATE_LIMIT' in err:
            m = _re.search(r'~(\d+)s remaining', err)
            wait = (int(m.group(1)) if m else 45) + 20      # margin: never retry on the boundary
            if k < tries - 1:
                note(f'[rate limited, waiting {wait}s before retry]')
                time.sleep(wait); continue
            raise RuntimeError(err.strip())
        if k < tries - 1:
            time.sleep(3 * (k + 1)); continue
        raise RuntimeError(err.strip() or 'empty response (rate limited?)')

def unwrap(resp):
    return resp.get('data', resp) if isinstance(resp, dict) and 'data' in resp else resp

def _f(v, default=0.0):
    try: return float(v)
    except (TypeError, ValueError): return default

def _clamp(x, lo=0.0, hi=1.0):
    return lo if x < lo else hi if x > hi else x

def _b(v):
    if isinstance(v, bool): return v
    if isinstance(v, (int, float)): return v != 0
    if isinstance(v, str): return v.strip().lower() in ('1', 'true', 'yes')
    return False


REPORT_CHROME = set('⛔⚠🔴🟠🟡🟢→←↑↓·▲▼●■□')
_ANSI_RESIDUE = _re.compile(r'\[[0-9;?]+[a-zA-Z]|\[[HJKmf]')   # what a CSI leaves behind once ESC is gone
                                                        # (params required, or a bare final byte,
                                                        #  so a symbol like '[TEST]' is left alone)
_PLAIN_TICKER = _re.compile(r'^[A-Za-z0-9 _$.+\-]+$')      # everything else gets quoted as a name

def safe(t, n=24):
    """Token symbols and names are attacker-controlled — anyone can deploy a coin called
    '\\n  ⛔ VERDICT: dumps' or one carrying ANSI escapes, and this report is read by both a human
    terminal and a model that summarizes it. Strip every non-printable character (control,
    bidi, zero-width), strip the report's own structural glyphs, and cap the length, so a
    symbol can neither forge a report line, nor forge a verdict marker, nor drive the terminal.

    Three things stripping alone did not cover, all seen in the hostile test:
    - Dropping the ESC byte leaves the REST of the escape as literal text, so an ANSI-coloured
      symbol printed '[31m' in the middle of the coin column. Remove the residue too.
    - `n` was a CHARACTER count while the layout is measured in DISPLAY columns, so a 24-CJK-char
      symbol is 48 columns wide and shoves the rest of the row past the right edge. Budget by dw().
    - A symbol can still hold ordinary WORDS, and this report's own vocabulary is the dangerous
      set: a coin literally named 'VERDICT dumps 100/100' printed that phrase next to its market cap and
      read as this script's verdict. Anything that is not a plain ticker is therefore wrapped in
      「」, which makes injected prose read as a name someone chose rather than as our commentary.
      Normal tickers (STONK, WIF, cbBTC) match _PLAIN_TICKER and are printed unchanged."""
    t = ''.join(c for c in str(t or '') if c.isprintable() and c not in REPORT_CHROME)
    t = _ANSI_RESIDUE.sub('', t)
    t = ' '.join(t.split())        # a run of spaces is how injected text buys itself a visual gap
    plain  = (not t) or bool(_PLAIN_TICKER.match(t))
    budget = n if plain else n - 4                      # 「」 is two WIDE chars = 4 of the budget
    if dw(t) > budget:
        keep, w = '', 0
        for c in t:
            cw = dw(c)
            if w + cw > budget - 1: break
            keep += c; w += cw
        t = keep + '…'
    t = t.strip() or '?'
    return t if plain else '「' + t + '」'

NOW = time.time()

# ── 1. Launch history ─────────────────────────────────────
# ── A peak market cap has to be believable, and one live figure was not ───────────────────────
# Measured on robinhood: a coin reporting token_ath_mc = $21,428,991,480 while holding 28 holders,
# $9.5K of pool liquidity, a $38K market cap and 3.7 cents of lifetime creator fees. No market ever
# produced that number. It nonetheless maxed B1 at 60/60, became his flagship, and took over
# His best work from the coin he actually built ($326M peak, 34K holders, $4.5M pool) -- so the whole
# POWER axis and the entire top-3 section were reporting a data artifact as his achievement.
# The global `ath_mc > 5e10` reject gate cannot catch it: $21B sails under a $50B bar, and rejecting
# the whole dev would be wrong anyway -- one bad row must not cost him a score. So the check is PER
# COIN, against that coin's own footprint, and it is deliberately loose: a genuine 100x rug (peak
# $10M, now $10K, 800 holders) must pass untouched, and only a figure orders of magnitude past
# anything the coin could ever have supported may fail.
ATH_MIN_HOLDERS = 500       # a real crowd was there -> the peak is credible on its own
ATH_MAX_RATIO   = 1e4       # a peak may exceed today's footprint 10,000x before we disbelieve it
def ath_ok(t):
    a = _f(t.get('token_ath_mc'))
    if a < 1e6: return True                                   # small numbers need no defence
    if _f(t.get('holders')) >= ATH_MIN_HOLDERS: return True
    # A peak is only disbelieved against EVIDENCE. With no footprint at all -- holders, pool and
    # market cap all absent -- there is nothing to contradict it, so trust it. Failing closed here
    # would be silent and catastrophic: on any chain that omits these fields every peak over $1M
    # reads as fake, POWER collapses to ~0 for a legitimate dev, and the report shows a wall of
    # warnings instead of a score. The bogus row this guard exists for is caught either way,
    # because it HAS a footprint ($9.5K pool, 28 holders) and that footprint is what convicts it.
    foot = max(_f(t.get('pool_liquidity')), _f(t.get('market_cap')))
    if foot <= 0 and t.get('holders') is None: return True
    return a <= ATH_MAX_RATIO * max(foot, 1.0)

def t_ath(t):
    """The peak this skill is willing to score. An unbelievable figure reads as 0 rather than being
    dropped: the coin stays in the book and in the per-coin detail, because what is untrusted is the
    NUMBER, not the launch."""
    return _f(t.get('token_ath_mc')) if ath_ok(t) else 0.0

def read_book(ct):
    """Everything derived straight from `created-tokens`, in one place so the N==0 re-read path below
    cannot drift from the first read -- it used to recompute four of these inline.

    On N: `inner_count + open_count` is normally the true launch total, because tokens[] is capped at
    ~101 rows. But it can also come back SMALLER than that array -- measured live on a robinhood dev
    whose counters said 63 + 17 = 80 while tokens[] held 95 real rows. Trusting the counters there
    understated his launches by 15 and, worse, left `alive` counted over 95 rows against a
    denominator of 80: two different populations inside one rate. Each source is a floor on the truth
    (a counter cannot invent launches; an array row cannot be a coin he did not create), so max() is
    the only reading that can never sit below the real number. The counters keep the graduation rate to themselves,
    where numerator and denominator come from the same place."""
    toks   = ct.get('tokens') or []
    inner  = int(_f(ct.get('inner_count')))
    opened = int(_f(ct.get('open_count')))
    N_ctr  = inner + opened
    N      = max(N_ctr, len(toks))
    ath_mc = _f((ct.get('creator_ath_info') or {}).get('ath_mc'))
    junk   = [t for t in toks if not ath_ok(t)]
    best   = max([t_ath(t) for t in toks] or [0.0])
    # creator_ath_info names whatever the server called his best coin, so it inherits the same bad
    # figure. When a junk row exists and the headline peak is above every believable one, it IS that row.
    if junk and ath_mc > best: ath_mc = best
    return toks, inner, opened, N_ctr, N, ath_mc, junk

ct = unwrap(run_cli(['portfolio', 'created-tokens', '--chain', CHAIN, '--wallet', DEV]))
toks, inner, opened, N_ctr, N, ath_mc, ath_junk = read_book(ct)

# ── 2a. N == 0 is TWO different facts, and asserting the wrong one is the worst output ──
# `N < 1` used to print "this address has never launched a token -- not a dev" -- a verdict. But the API can answer 200 OK with a
# structurally complete, entirely EMPTY body while its index is degraded: observed live on a wallet
# that had returned 28 launches and 134 trade rows an hour earlier, and then read inner_count 0 /
# open_count 0 / tokens [] / buy 0 / sell 0. Downstream of a blank read this skill confidently told
# the user a real dev was not a dev, which is strictly worse than saying nothing.
#
# The two cases cannot be separated from `created-tokens` alone -- both give zeros -- so separate them
# by CORROBORATION. A wallet the index really knows about carries other traces: trades, a token count,
# a last-activity timestamp. So:
#   * launches 0 BUT the wallet shows trading history  -> indexed, and genuinely not a dev. Assert it.
#   * launches 0 AND every field on every endpoint is 0 -> we cannot tell an empty wallet from an empty
#     index. Report that, do not rule.
# One re-fetch first: a transient blank clears on retry, while a genuinely empty wallet stays empty, so
# the retry can only ever help. It costs one call on the rare N==0 path and nothing on the normal path.
alive_hint, refetched = None, False
if N < 1:
    try:
        time.sleep(2.0)
        ct2 = unwrap(run_cli(['portfolio', 'created-tokens', '--chain', CHAIN, '--wallet', DEV]))
        n2  = int(_f(ct2.get('inner_count'))) + int(_f(ct2.get('open_count')))
        if n2 > 0:                       # the first read was a blip; carry on with the good one
            ct = ct2
            toks, inner, opened, N_ctr, N, ath_mc, ath_junk = read_book(ct2)
            refetched = True
    except Exception:
        pass
if N < 1:
    # Second endpoint: does the index know this address AT ALL?
    try:
        st = unwrap(run_cli(['portfolio', 'stats', '--chain', CHAIN, '--wallet', DEV])) or {}
        ps = st.get('pnl_stat') or {}
        alive_hint = any(_f(st.get(k)) != 0 for k in ('buy', 'sell', 'last_timestamp',
                                                     'realized_profit', 'total_cost')) \
                     or _f(ps.get('token_num')) != 0
    except Exception:
        alive_hint = None            # could not check -- absence of a check is not evidence either

# ── The non-person gate is about BEHAVIOUR, not about a launch count ───────────────────────────────
# `N > 20000` alone was a cliff straight through the live distribution: a 17,752-launch wallet was
# scored, and a 20,102-launch wallet was refused outright -- even though it had 369 graduations and a
# coin that peaked at $91.86M. Refusing there is the same error the scoring side was already
# corrected for: a demonstrated achievement was thrown away by a threshold.
# What the gate is actually trying to exclude is an address that is not a person making launches --
# a launchpad or factory contract, where "will HE dump on you" has no referent. That shows up as
# volume with NOTHING ever coming out of it: nothing graduated and nothing ever reached a real market
# cap. Volume plus real graduations plus a real peak is a bot-scale dev, which is a person, and a
# trader asking "can I buy his next launch" deserves an answer about him.
# Both figures are available before the expensive trade walk, so the gate stays cheap and early.
FACTORY_N   = 20000        # above this the count on its own stops being informative
FACTORY_ATH = 1e6          # ... so require evidence that something he launched actually traded
reject, unknown = None, None
if N > FACTORY_N and (opened < 1 or ath_mc < FACTORY_ATH):
                              reject = 'not_a_person'      # launchpad or factory contract, not a launcher
elif ath_mc > 5e10:           reject = 'peak_implausible'  # >50B USD peak: the data source is wrong
elif N < 1 and alive_hint:    reject = 'never_launched'    # indexed, has traded, has launched nothing
elif N < 1:                   unknown = True               # cannot tell an empty wallet from an empty index

# Both exits return the same shape as a full score minus the scores, so the caller
# never has to special-case the presence of keys. `scored` is the only branch it reads.
if unknown:
    # No verdict here, on purpose: `traces` False means the index knows this wallet and it
    # is genuinely empty, None means the corroborating read itself failed. A degraded index
    # answers 200 OK with a structurally complete empty body, so asserting "not a dev" off
    # these zeros is the one output strictly worse than saying nothing.
    emit({'scored': False, 'reason': 'index_empty', 'chain': CHAIN, 'dev': DEV,
          'traces': alive_hint, 'launches': N, 'refetched': refetched})
if reject:
    emit({'scored': False, 'reason': reject, 'chain': CHAIN, 'dev': DEV,
          'launches': N, 'graduated': opened, 'on_curve': inner,
          'peak_mc_usd': ath_mc, 'refetched': refetched})

# ── 3. Every trade he made, in his own coins ──────────────
launch_ts = {t.get('token_address'): _f(t.get('create_timestamp')) for t in toks}

def walk(types, max_pages, token=None, stop_before=None, wallet=None):
    """The server caps page size at 20 rows regardless of --limit, so filter by type
    server-side instead of paging through transfers and fee claims to find the buys.

    Rows come back newest-first (verified), so `stop_before` is a lossless early exit:
    once a page is entirely older than his earliest launch, no later row can belong to
    any coin he created. For a dev who traded for years before launching, that is the
    difference between 40 pages and 6.

    Returns (rows, pages_used, truncated). truncated=True means a live cursor remained.
    """
    rows, cursor, pages = [], None, 0
    while pages < max_pages:
        a = ['portfolio', 'activity', '--chain', CHAIN, '--wallet', wallet or DEV, '--limit', '20']
        for t in types: a += ['--type', t]
        if token:  a += ['--token', token]
        if cursor: a += ['--cursor', cursor]
        page = unwrap(run_cli(a))
        got = page.get('activities') or []
        rows += got
        cursor = page.get('next'); pages += 1
        if not cursor or not got: return rows, pages, False
        if stop_before and got and max(_f(x.get('timestamp')) for x in got) < stop_before:
            return rows, pages, False          # walked past every launch — nothing left to find
    return rows, pages, bool(cursor)

earliest_launch = min([v for v in launch_ts.values() if v > 0] or [0])
acts, pages, trunc = walk(['buy', 'sell'], MAX_PAGES, stop_before=earliest_launch)
rem,  rpages, _r   = walk(['remove'], 3)   # not `_` — that is the i18n helper
pages += rpages

# A truncated walk stops at the OLD end. Any coin launched at/after the oldest row we
# saw is therefore already complete — its whole life is inside the window. Only coins
# launched BEFORE that point can be missing trades, so resolve exactly those, biggest
# first, with a per-token walk. Cost is bounded by TOP_K and does not grow with his
# trade history — which is what made the unbounded walk fail in the first place.
unresolved = []
if trunc and acts:
    oldest_seen = min(_f(x.get('timestamp')) for x in acts)
    maybe = [t for t in toks if _f(t.get('create_timestamp')) < oldest_seen]
    maybe.sort(key=lambda t: t_ath(t), reverse=True)
    for t in maybe[:TOP_K]:
        r_, p_, _t = walk(['buy', 'sell'], 5, token=t.get('token_address'))   # not `_` — that is the i18n helper
        acts += r_; pages += p_
    unresolved = maybe[TOP_K:]
truncated = bool(unresolved)      # only still-unknown coins count as truncation now

seen_ids, dedup = set(), []
for a in acts:
    k = (((a.get('token') or {}).get('address')), a.get('event_type'),
         a.get('timestamp'), a.get('cost_usd') or a.get('quote_amount'), a.get('tx_hash'))
    if k in seen_ids: continue
    seen_ids.add(k); dedup.append(a)
acts = dedup

# ── Cross-wallet exits — the one blind spot that silently invalidates every rate below ──
# pull multiple, 1st-sell delay and "he never sold a share" all assume the dev sells from the wallet he
# launched from. Move the supply to a second wallet first and all three read perfectly clean
# while the dump happens in the open. Two cheap checks, in the only order that is honest:
# find where supply went, THEN check whether it was actually sold. Moving supply is not a dump.
SIB_MIN_SHARE = 0.01     # ignore dust — a pre-dump move is a chunk of supply, not a tip
SIB_MAX_CHECK = 3        # verification is bounded: biggest moves by USD only
# brief mode exists to screen many devs cheaply; this check costs up to 8+1+3 calls, and an
# unverified move cannot be told apart from a lock or exchange address. Running half of it
# in batch would manufacture false alarms, so brief skips it and says so.
SIB_ON = (MODE != 'brief')
BURN = {'0x0000000000000000000000000000000000000000',
        '0x000000000000000000000000000000000000dead',
        '11111111111111111111111111111111'}

# Same lossless exit as the buy/sell walk: transfers older than his earliest launch cannot
# be a pre-dump move. Without it a wallet with a long transfer history hides the move past
# the page cap — and a missed move makes him look cleaner, the dangerous direction.
tout, tpages, tout_trunc = walk(['transferOut'], 8, stop_before=earliest_launch) if SIB_ON else ([], 0, False)
pages += tpages                # NOTE: the FILTER value is transferOut (camelCase),
                               # but the returned event_type is transfer_out (snake_case)
moves = []
for a in tout:
    tk = a.get('token') or {}
    ad = tk.get('address')
    if ad not in launch_ts: continue             # only coins HE created can be pre-dump moves
    # Sanitised at the source, like every symbol: `to_address` is API-supplied and gets printed
    # (truncated to 8 chars) inside ⛔/⚠ lines. Eight characters is enough room for a newline plus a
    # forged fragment, so the same rule that guards token symbols has to guard this too.
    # TRUNCATE FIRST, SANITISE SECOND, and keep the two results apart. safe() closes a non-plain
    # value with 」, so slicing its OUTPUT cuts that bracket off and the quoted run never visibly
    # ends -- 「VERDICT dumps 100… followed by the report's own words, which is exactly the confusion the
    # quoting exists to prevent. `to` stays full because it is compared against fund_from_address
    # (a real address is plain, so safe() returns it unchanged and the match still works); `to_disp`
    # is the short form for printing, and safe() owns its final shape including both brackets.
    to = safe((a.get('to_address') or '').lower(), 64)
    to_disp = safe((a.get('to_address') or '').lower()[:8], 12)
    if to == '?' or to in BURN or to == DEV.lower(): continue
    sup   = _f(tk.get('total_supply'))
    share = (_f(a.get('token_amount')) / sup) if sup > 0 else 0.0
    if share < SIB_MIN_SHARE: continue
    after = _f(a.get('timestamp')) - launch_ts[ad]
    moves.append({'tok': ad, 'sym': safe(tk.get('symbol') or ad[:6], 16), 'to': to, 'share': share,
                  'to_disp': to_disp,
                  'usd': _f(a.get('cost_usd')), 'after': after, 'pre': after < 0})
moves.sort(key=lambda m: m['usd'], reverse=True)

funder = ''
if moves:
    # Supply out to the same address that funded him = one operator, two wallets.
    try:
        funder = (((unwrap(run_cli(['portfolio', 'stats', '--chain', CHAIN, '--wallet', DEV]))
                    or {}).get('common') or {}).get('fund_from_address') or '').lower()
        pages += 1
    except Exception:
        funder = ''

sib_sold, sib_pending = [], []
for m in moves[:SIB_MAX_CHECK]:
    m['same_as_funder'] = bool(funder and m['to'] == funder)
    try:
        rows, rp, _v = walk(['buy', 'sell'], 2, token=m['tok'], wallet=m['to'])
        pages += rp
    except Exception:
        m['unchecked'] = True; sib_pending.append(m); continue
    sells = [x for x in rows if x.get('event_type') == 'sell']
    m['sold'] = sum(_f(x.get('cost_usd')) for x in sells)
    m['fs']   = min([_f(x.get('timestamp')) - launch_ts[m['tok']] for x in sells], default=None)
    (sib_sold if m['sold'] > 0 else sib_pending).append(m)

# A `remove` row is the heaviest single finding in this skill, so it has to actually be one.
# Measured on a live launchpad (`pons`): four `remove` rows with token_amount=0, quote_amount=0
# and no cost_usd, on a coin whose pool still holds 3.85M USD of liquidity 48 days later. Those are LP-position
# / fee-management calls, not a drain. Three guards, all required:
#   1. the row must move the TOKEN out of the pool, and
#   2. it must move a MEANINGFUL amount of it, and
#   3. a pool that is still alive was not drained — you cannot have pulled the liquidity out of
#      a pool that is still worth millions.
# Only a sized removal on a coin that is now dead forces systematic. A sized removal on a live coin
# is disclosed as partial and left out of the gate, because it is not what the gate is for.
#
# ── Guard 2 exists because `sz > 0` was never a threshold ─────────────────────────────────────
# Measured live on sol: one row with token_amount=0, quote_amount=0.0259 of the PAIRED token and an
# empty cost_usd forced systematic on its own -- CONDUCT 55 -> 45, TOTAL 56 -> 46, and the report told the
# reader "do not buy -- there is no safe entry" about a dev with no sell anywhere in his history. Zero tokens left
# that pool; nothing was drained. The old `max(token_amount, cost_usd, quote_amount) > 0` also maxed
# three INCOMPATIBLE units together -- token units, USD, and units of whatever token happened to be
# on the other side of the pool -- so no meaningful threshold could even be expressed in it.
# `cost_usd` came back as an empty string on every single `remove` row measured on sol, so a USD floor
# cannot carry this check on its own; it is accepted as confirmation when the API supplies one at all.
# The denominator that IS always present on the row is `token.total_supply`, and it is in the same unit
# as `token_amount`, so share-of-supply is the one sizing that works everywhere.
LP_MIN_SHARE = 0.005     # 0.5% of supply pulled back out of the pool. Below this it is fee/LP noise:
                         # the dust rows measured were 0.00059% and 0.00000% of supply.
LP_MIN_USD   = 500.0     # or a confirmed USD size, on the chains that populate cost_usd at all
per, lp_hits, lp_zero = {}, [], 0
for a in acts + rem:
    ad = ((a.get('token') or {}).get('address'))
    et = a.get('event_type')
    if ad not in launch_ts: continue
    if et == 'remove':
        # A drain has to move the token. A row that moves 0 of it is a fee or LP-position call,
        # whatever the quote leg says -- and the quote leg is denominated in the OTHER token, so it
        # can never be compared against a token amount or a USD figure.
        sup_r = _f(((a.get('token') or {}).get('total_supply')))
        amt_r = _f(a.get('token_amount'))
        shr_r = (amt_r / sup_r) if sup_r > 0 else 0.0
        if amt_r > 0 and (shr_r >= LP_MIN_SHARE or _f(a.get('cost_usd')) >= LP_MIN_USD):
            lp_hits.append(ad)
        else:
            lp_zero += 1
    p = per.setdefault(ad, {'buy': 0.0, 'sell': 0.0, 'fs': None, 'fb': None})
    amt = _f(a.get('cost_usd') or a.get('quote_amount'))
    ts  = _f(a.get('timestamp'))
    if et == 'buy':
        p['buy'] += amt
        d = ts - launch_ts[ad]
        if p['fb'] is None or d < p['fb']: p['fb'] = d
    elif et == 'sell':
        p['sell'] += amt
        d = ts - launch_ts[ad]
        if p['fs'] is None or d < p['fs']: p['fs'] = d

# A sibling wallet's sells are his sells. Fold them in so pull multiple and 1st-sell delay measure the
# dev, not the wallet — otherwise concealment is rewarded with a cleaner score than selling
# openly. Supply merely parked elsewhere is NOT folded in: it has not been sold yet.
for m in sib_sold:
    p = per.setdefault(m['tok'], {'buy': 0.0, 'sell': 0.0, 'fs': None, 'fb': None})
    p['sell'] += m['sold']
    if m.get('fs') is not None and (p['fs'] is None or m['fs'] < p['fs']): p['fs'] = m['fs']

CUT_MULT, CUT_SEC = 1.5, 30      # dump = pulled out >=1.5x AND first sell within 30s
# The boolean above still defines the WORD dump and still feeds the three-tier gate, whose bands were
# calibrated on it. It must not also be what CONDUCT deducts on: crossing a line says nothing about
# degree, so `2.70x @40s` read clean while `1.73x @28s` read dump — 56% more money taken, forgiven for
# waiting 12 extra seconds. Severity below is continuous in BOTH axes, so the deduction orders those
# two the right way round while the gate keeps the input it was calibrated on.
SEV_MULT_FULL = 4.0             # pulling >=4x what he put in is a full 1.0 on the amount axis
SEV_SEC_ZERO  = 120.0           # a first sell at/after 120s is not racing the open: 0 on the timing axis
def f_mult(m):  return _clamp((m - 1.0) / (SEV_MULT_FULL - 1.0))
def f_delay(x): return _clamp((SEV_SEC_ZERO - x) / SEV_SEC_ZERO) if x is not None else 0.0
traded, cut, mults, delays, snipes, no_buy = [], [], [], [], 0, []
sev_by = {}                     # token -> severity 0..1; a coin he never sold contributes exactly 0
for ad, p in per.items():
    if p['buy'] <= 0 and p['sell'] <= 0: continue
    traded.append(ad)
    # Two different quantities that used to share one variable, and the report printed the wrong one.
    # pull multiple is what he took out over what he put in -- UNDEFINED when he never bought, and the 99.0
    # standing in for it there is a sentinel, not a measurement. It leaked straight into the median, so
    # a dev whose sells were all creator-fee revenue read "Cash out vs put in -- 99.00×" -- measured live on
    # 20 of one dev's 29 coins, where the truth was that he claimed creator fees and sold those.
    # The sentinel keeps its job in the SEVERITY and dump inputs, where supply sold with no matching buy
    # has to count as maximally suspicious on the amount axis (the timing axis is what then holds it in
    # check -- and it did: every one of those 20 coins sold days to weeks after open, severity 0).
    # It just may never appear in anything reported as a measurement.
    mult     = (p['sell'] / p['buy']) if p['buy'] > 0 else None
    mult_sev = mult if mult is not None else (99.0 if p['sell'] > 0 else 0.0)
    if mult is not None:  mults.append(mult)
    elif p['sell'] > 0:   no_buy.append(ad)
    if p['fb'] is not None and p['fb'] <= 60: snipes += 1
    if p['fs'] is not None: delays.append(p['fs'])
    sev_by[ad] = f_mult(mult_sev) * f_delay(p['fs'])
    if mult_sev >= CUT_MULT and p['fs'] is not None and p['fs'] <= CUT_SEC: cut.append(ad)

def med(xs): 
    xs = sorted(xs)
    return xs[len(xs)//2] if xs else None

n_tr      = len(traded)
n_mult    = len(mults)          # coins where pull multiple is defined at all (he both bought and sold)
cut_rate  = (len(cut) / n_tr) if n_tr else None
med_mult  = med(mults)          # over n_mult, never over n_tr -- see the sentinel note above
med_delay = med(delays)
# med() returns xs[len//2], so at n=2 it hands back the LARGER of the two. On a dev with first
# sells of 276s and 2.7 days that printed a 2.7d median and the advice "he typically starts selling
# 2.7 days after open", while his flagship had actually started at 4.6 minutes -- the error direction
# that makes a dev look SAFER than he is. Timing advice must quote the fastest he has ever moved, not
# the middle.
min_delay = min(delays) if delays else None
snipe_rate= (snipes / n_tr) if n_tr else None
mean_sev  = (sum(sev_by.values()) / n_tr) if n_tr else None   # drives the CONDUCT deduction
med_sev   = med(list(sev_by.values()))

# ── 4. Structure of his book ──────────────────────────────
def is_alive(t): return _b(t.get('is_open')) and _f(t.get('pool_liquidity')) >= 4000
alive = sum(1 for t in toks if is_alive(t))
# `alive` can only be counted over `tokens[]`, and the server truncates that array at ~101 rows
# in ATH-DESCENDING order. Dividing it by the true total N put a ceiling on survival rate that no dev
# past 101 launches could reach (365 launches -> max 27.4%, 287 -> 34.8%), so the number was
# re-punishing launch COUNT, which factory_pen already prices, and the bias grew with N. Worse,
# the rows that survive truncation are his NEWEST coins, so the miss is systematic, not noisy.
# Numerator and denominator must describe the same population: the launches actually sampled.
#
# ── What the truncation actually keeps, measured ───────────────────────────────────────────────
# This skill used to state that `tokens[]` is truncated ATH-DESCENDING, and concluded from that
# that "the coins that decide the verdict are guaranteed to be in the sample". Measured live on two
# sol wallets, that is false: the array is ordered by `create_timestamp` DESCENDING, so the 101 rows
# are his NEWEST launches plus (apparently) his ATH coin appended. On a 17,752-launch wallet the
# sample spanned about SIX HOURS. His real #2 -- a coin that peaked at $8.26M with 4,130 holders and
# a $200K pool, which he was still holding -- was absent, while two coins that peaked at $8.2K and
# $6.6K were present, because they happened to be launched inside the window.
# Nothing in the documented API enumerates the launches outside that window, so the fix is not to
# recover them: it is to stop ASSERTING things the sample cannot support. Every claim about his
# career-wide success count is gated on `book_trunc` below.
surv_den = min(len(toks), N)                          # sampled population, not the true total
surv  = alive / surv_den if surv_den else 0.0
surv_trunc = surv_den < N                             # sample truncated -> say so in the wording
book_trunc = surv_trunc                               # same fact, named for the POWER-side claims
# The window the sample actually covers, so the report can name it instead of implying the book is whole.
# The OLDEST row alone is misleading: the API appends his ATH coin to the recent window, so on the
# measured wallet the oldest row was 41 days back while the other 100 rows spanned six hours -- and a
# disclosure saying "created after <41 days ago>" reads as six weeks of coverage. So name the window
# the BULK of the rows fall in, and only mention the older straggler as what it is.
_bcts = sorted(_f(t.get('create_timestamp')) for t in toks if _f(t.get('create_timestamp')) > 0)
def _dstamp(ts): return time.strftime('%Y-%m-%d %H:%M', time.localtime(ts))
book_from  = _dstamp(_bcts[0]) if _bcts else '?'
_bulk_i    = max(1, int(len(_bcts) * 0.05)) if len(_bcts) > 20 else 0
book_bulk  = _dstamp(_bcts[_bulk_i]) if _bcts else '?'
# True when the bulk window is materially tighter than the full span -- i.e. the oldest rows are
# stragglers and quoting them would overstate coverage.
book_narrow = bool(_bcts) and (_bcts[_bulk_i] - _bcts[0]) > 3 * 86400
book_span_h = ((_bcts[-1] - _bcts[_bulk_i]) / 3600.0) if _bcts else 0.0
# survival rate is now scoped; graduation rate is not. `open_count` and `inner_count` are both server-side counters
# over the FULL history, so opened / N_ctr is a true ratio and needs no scoping -- and it must divide
# by the COUNTERS, not by N, because N may have been raised above them by a longer tokens[] and we do
# not know whether the rows the counters missed were graduated or still on the curve.
grad  = opened / N_ctr if N_ctr else 0.0
cto   = (sum(1 for t in toks if _b(t.get('cto_flag'))) / len(toks)) if toks else 0.0
stuck = (sum(1 for t in toks if _b(t.get('liquidity_less_4k'))) / len(toks)) if toks else 0.0
big   = [t for t in toks if t_ath(t) >= 1e6]
k1m   = len(big)
dd_big= None
if big:
    dds = [1.0 - (_f(t.get('market_cap')) / t_ath(t)) for t in big if t_ath(t) > 0]
    dd_big = med(dds)

by_addr    = {t.get('token_address'): t for t in toks}
lp_drained = [ad for ad in set(lp_hits) if not is_alive(by_addr.get(ad) or {})]
lp_partial = [ad for ad in set(lp_hits) if is_alive(by_addr.get(ad) or {})]
lp_removed = bool(lp_drained)          # only a sized pull on a now-dead coin forces the gate

top = sorted(toks, key=lambda t: t_ath(t), reverse=True)[:3]
top1 = top[0] if top else None
top1_cut  = bool(top1 and top1.get('token_address') in cut)

# ── Coordinated launch buying — the only cross-wallet signal that needs no link back to him ──
# `bundler_rate` is the share of supply bought in the SAME BLOCK as the create tx. That makes it
# the one measurement that survives the blind spot below: a second wallet with no transfer edge
# and no shared funder still shows up here the instant it buys his open alongside creation.
# It does NOT say WHOSE wallets those are — a paid bundler service and a third-party sniper bot
# land in the same number as the dev's own alts. So it is DISCLOSED, never scored. Turning an
# unattributable number into a deduction would penalise a dev for other people's bots, and the
# whole point of the dump gate is that every deduction names a thing HE did.
BUND_HOT = 0.20
brs      = [_f(t.get('bundler_rate')) for t in toks if t.get('bundler_rate') not in (None, '')]
br_med   = med(brs) if brs else None
br_hot   = sorted([t for t in toks if _f(t.get('bundler_rate')) >= BUND_HOT],
                  key=lambda t: _f(t.get('bundler_rate')), reverse=True)

# His flagship, resolved now rather than at print time: `open_timestamp` (market open)
# is the real age and the thin-record shrink below depends on it. `create_timestamp`
# is contract creation and can be a week earlier — using it would overstate the record.
top1_status, top1_age_src = 'unreadable', 'create'   # status codes are listed in references/fields.md
top1_bal    = 0.0                 # creator balance, when the API returned one
top1_closed = False               # API says the flagship position is closed -> audit how it left
top1_hold   = None                # True/False only when the API SAID something. `not top1_closed`
                                  # was being read as "he is holding", so a flagship whose
                                  # creator_token_status came back '' with creator_token_balance 0
                                  # reported as "still in his hands, untouched" -- an affirmative claim about a bag
                                  # the data does not show. None means say neither.
top1_ts = _f(top1.get('create_timestamp')) if top1 else 0.0
if top1:
    try:
        ti  = unwrap(run_cli(['token', 'info', '--chain', CHAIN, '--address', top1.get('token_address')]))
        d_  = ti.get('dev') or {}
        st  = (d_.get('creator_token_status') or '')
        bal = _f(d_.get('creator_token_balance'))
        top1_bal = bal
        if st or bal: top1_hold = (st == 'creator_hold') or bal > 0
        ots = _f(ti.get('open_timestamp'))
        if ots > 0: top1_ts, top1_age_src = ots, 'open'
        if   st == 'creator_hold': top1_status = 'holding'
        elif 'sell' in st:         top1_status = 'sold_own_bag'
        elif st == 'creator_close':
            # Confirmed on robinhood/PONS: status `creator_close` with balance 0 while the
            # activity feed holds no `sell` and no `transferOut` at all. The position is
            # provably gone and the exit route is provably not in the data. Say exactly that —
            # calling it a sale would invent a row, and calling it unavailable would hide a
            # status the API did return.
            top1_closed = True
            top1_status = 'closed_no_sell_row'
        elif top1.get('token_address') not in per:
            top1_status = 'untraded_but_supply_moved' if sib_sold else 'untraded'
    except Exception:
        pass
top1_days = max(0.0, (NOW - top1_ts) / 86400) if top1 else 0.0

# How long he has been launching AT ALL. This -- not his flagship's age -- is what the CONDUCT shrink
# below needs: the shrink asks "has he been around long enough for a dump record to exist", which is a
# property of his career, not of one coin. Keying it on the flagship inverted the answer on the case
# that matters most: a dev six months and forty clean launches deep whose NEWEST coin happens to be
# his biggest read as a three-day rookie and lost ~36 CONDUCT points. Flagship age stays where it belongs
# -- a disclosure, plus the POWER-side discount on a peak that has not held (a coin's durability is an
# outcome, and outcomes score POWER; that is the same rule that got `struct` deleted from CONDUCT).
# CAVEAT: earliest_launch comes from tokens[], which the API caps at ~101 rows ordered by
# create_timestamp DESCENDING, so on a truncated book it is the start of the sampled WINDOW, not of
# his career. This was previously written off as a mild strictness bias on the theory that the cut
# discarded his smallest coins; with create-desc ordering the cut discards his OLDEST coins, and the
# understatement is not mild. Measured live: a 17,752-launch wallet's 101 rows spanned about six
# hours, which reads as a rookie and would cost ~36 CONDUCT points. career_days is therefore treated as
# a FLOOR whenever the book is truncated (see career_floor), and factory_pen carries the factory case
# on launch volume, where it belongs.
career_days = max(0.0, (NOW - earliest_launch) / 86400) if earliest_launch > 0 else 0.0
# `earliest_launch` is the oldest row in `tokens[]`, and the array is create-DESCENDING, so on a
# truncated book it is the start of the WINDOW, not the start of his career -- older launches exist by
# definition (that is what truncation means) and are simply not readable. The old note assumed this
# was a mild strictness bias; with create-desc truncation it is not mild: a 17k-launch wallet's window
# spanned six hours, which would read as a rookie and cost ~36 CONDUCT points. So the career figure is a
# FLOOR when the book is truncated, and the time half of the shrink below may not fire on a floor --
# "we cannot see how far back he goes" is not "he only started today".
career_floor = book_trunc          # career_days is a lower bound, not a measurement

# ── Flagship exit audit — the one case where a MISSING row is itself a finding ──
# When the API says the flagship position is closed, the supply provably left the wallet. Every dump
# number in this skill is computed from rows in this wallet, so if nothing accounts for that exit, the
# clean pull multiple and the late 1st-sell delay on his single most important coin are measuring an empty wallet.
# That is not the same as our sampling being thin: the API asserts the position is gone, and the
# wallet's own feed fails to say how — an affirmative inconsistency, which is why it deducts rather
# than merely capping (the unproven tier, where nothing happened at all, only caps).
# It must not fire on an exit that IS accounted for. Supply can leave innocently and visibly: burned,
# added to an LP, or transferred out. `burn` is not an accepted --type filter value, so this pulls the
# flagship's UNFILTERED feed (bounded: one token, 3 pages) and asks whether any row at all explains
# the exit. A failed lookup never accuses -- an accusation has to be positively established.
ACCOUNTED = ('sell', 'transfer_out', 'burn', 'add', 'remove')
opaque_exit, exit_kinds = False, []
if top1 and top1_closed:
    try:
        rows_, p_, _t3 = walk([], 3, token=top1.get('token_address'))
        pages += p_
        exit_kinds  = sorted({(r.get('event_type') or '?') for r in rows_})
        opaque_exit = not any(r.get('event_type') in ACCOUNTED for r in rows_)
    except Exception:
        opaque_exit = False
if opaque_exit:
    top1_status = 'closed_exit_unrecorded'
elif top1_closed and exit_kinds:
    # The audit CLEARING him used to change nothing. The status was written in the creator_close
    # branch ABOVE, before the audit ran, and only the accusing branch ever rewrote it -- so a dev
    # whose exit is fully documented still read "how it left cannot be traced" on the same screen as
    # a row saying "sold, and the path is traceable". Measured live: the flagship had five real
    # `sell` rows in its own feed. Two lines that contradict each other are worse than either one
    # alone, because the reader cannot tell which to act on. Name the rows the audit actually found.
    top1_status = 'closed_exit_documented'
exit_accounted = [k for k in ACCOUNTED if k in exit_kinds]

# ── 5. CONDUCT ───────────────────────────────────────────────
# CONDUCT answers one question — will he sell into your bid at open — so every term in it has to be
# something HE did. survival rate / graduation rate / drawdown used to multiply this score through `struct`, which made the
# market's outcome its largest lever (survival rate alone swung 50 points) while his two direct dump signals,
# pull multiple and 1st-sell delay, moved it by zero. They score POWER (B4) now, where an outcome belongs, and
# survival rate is no longer counted twice (it was in `struct` AND in B3).
# Every term is rounded to ONE decimal at computation, not at print time, so `100 - a - b - c = d`
# is true of the numbers on screen and not merely of the floats behind them. Rounding only at print
# made the row visibly fail to add (100-0-0-32-3-15 printed as 49, from true terms 31.6 / 3.1 / 49.4).
# The cost is <=0.05 of a point per term, which no verdict band can notice.
R = lambda x: round(x, 1)
abandon_pen = R(_clamp((cto - 0.30) / 0.70) * 10.0)       # walked-away rate above 30%
dump_pen    = R((55.0 * mean_sev) if mean_sev is not None else 0.0)  # mean severity over coins he traded
raw         = R(max(0.0, 100.0 - dump_pen - abandon_pen))

# The shrink asks how much dump evidence exists, so the sample it counts is the coins with TRADE
# data, not launches. While `struct` sat in CONDUCT a 365-launch factory with zero trade rows was held
# down by its dead book; with CONDUCT built only from his own actions, N/5 would hand that same factory
# w = 1 and a near-100 baseline for having no record at all — the exact lift this shrink exists to
# forbid. n_tr/5 keeps it: no trade rows -> w = 0 -> CONDUCT sits at the 60 floor before factory_pen.
# The second half is CAREER length, not flagship age -- see career_days above for why the flagship
# was the wrong gauge here. Both halves now ask the same question (is there enough record to judge
# him) from the two independent directions that record has: breadth and time.
# The time half is skipped on a truncated book: it would be shrinking on a window length, not on a
# career length. Breadth (n_tr) still shrinks normally, and factory_pen still prices launch volume.
w = min(1.0, n_tr / 5.0) * (1.0 if career_floor else min(1.0, career_days / 30.0))
cred = R(60.0 + (raw - 60.0) * w) if raw > 60.0 else raw
shrunk = R(raw - cred)
cred_pre = cred          # post-shrink, pre-penalty -- the report quotes it to show what the shrink did

# Bonding-curve pileup. Spraying coins that never leave the curve is something he DOES, so it is
# CONDUCT, not POWER. The scale is log, not linear: it has to bite at the dozens, because the median dev
# launches 6 coins and `inner` in the hundreds is a spray-and-pray signature. The old linear
# (inner-50)/950 only reached half strength at 500 stuck coins and charged a 224-coin factory 8
# points -- survivable while `struct` also multiplied it down, and far too gentle once CONDUCT stopped
# pricing his dead book at all.
FAC_LO, FAC_HI = 20.0, 500.0                              # 0 at 20 stuck coins, full 45 at 500
factory_pen = 45.0 * _clamp(
    (math.log10(max(FAC_LO, inner)) - math.log10(FAC_LO)) / (math.log10(FAC_HI) - math.log10(FAC_LO)))
# Sized as a real deduction, not a rounding: it says the cleanest-looking evidence on his most
# important coin cannot be relied on. It sits AFTER the shrink for the same reason factory_pen does --
# this is an established fact about him, not an inference from a thin sample, so it must not be
# multiplied down by w.
OPAQUE_PEN = 15.0
opaque_pen = OPAQUE_PEN if opaque_exit else 0.0
factory_pen = R(factory_pen)
cred = R(max(0.0, cred - factory_pen - opaque_pen))

# ── 6. POWER ───────────────────────────────────────────────
B1 = R(_clamp((math.log10(max(1.0, min(ath_mc, 5e10))) - 5.0) / 4.0) * 60.0)  # peak
B2 = R(0.0 if k1m < 1 else min(25.0, 11.0 + 5.0 * math.log2(k1m)))           # repeatable (was 30)
B3 = 10.0 if (top1 and is_alive(top1)) else 0.0                            # best still alive (was 15)
# B4 receives the three book-quality terms that used to multiply CONDUCT. drawdown enters HERE and only here,
# at 2 points of weight, and never touches B1: "it fell later" does not erase "he did build it once".
# An unknown drawdown (no 1M+ coin) counts as 0.5 rather than 1.0 — absence of a big coin is not a clean
# drawdown record, and free points there would reward having nothing to measure.
# B4 is scaled by how many launches were actually sampled, and it is the ONE term that must be:
# survival rate and graduation rate are both 100% on a book of one coin, so an unscaled B4 handed every single-launch
# dev ~24 free points and pushed POWER to the 100 ceiling, where nothing discriminates any more. The
# scale runs from 0, not from a midpoint — an unmeasured book earns nothing rather than being assumed
# average — and B4 is additive, so this can only withhold a bonus, never manufacture a penalty. B1
# (peak market cap, the demonstrated achievement) is untouched by it.
dd_term = (1.0 - _clamp(dd_big)) if dd_big is not None else 0.5
w_book  = min(1.0, surv_den / 5.0)                                         # sampled-book confidence
# B4's ceiling is 10, not 25: B2 and B3 gave up 10 points to make room, so B1+B2+B3+B4 = 105 -- the
# same pre-cap ceiling POWER had before the move. At 25 the components summed to 120 and min(100,...)
# started binding on ordinary devs: a dev whose best coin peaked at ~10M USD scored POWER 93 because his
# book happened to be alive, and peak -- the demonstrated achievement -- fell from 60/105 to 60/120 of
# the axis. Book quality is also partly double-counted: B3 already pays for the flagship being alive.
B4 = R(10.0 * (0.50 * _clamp(surv) + 0.30 * _clamp(grad) + 0.20 * dd_term) * w_book)
power = R(min(100.0, B1 + B2 + B3 + B4))
# Lift only, never a drag: POWER below 50 must not subtract from CONDUCT — a weak record
# is already priced into CONDUCT, and letting it subtract twice would double-count it.
bonus = R(max(0.0, min(1.0, k1m / 3.0) * (power - 50.0) / 50.0 * 15.0))

total = R(_clamp(cred + bonus, 0.0, 100.0))

# ── 7. dump-rate gate — three tiers, asymmetric in the thin-sample case ──
# frequent deducts 20 from CONDUCT instead of flooring it at 65, because a ceiling erases exactly the
# information the severity model was built to produce: CONDUCT arrived above 65 for every frequent dev, so
# min(cred, 65) swallowed the whole pull deduction and printed the same 65 for a mild dumper and a
# brutal one. TOTAL is still capped at 74 so no frequent dev can reach 🟢 -- the tier keeps its verdict,
# it just stops flattening ranking inside itself. systematic keeps the hard cap: at that frequency the
# tier IS the answer and there is nothing left to rank.
# The deduction applies to frequent only -- a MEASURED dump rate. unproven keeps the old ceiling:
# that tier is absence of evidence, and charging it the same 20 points as a proven dumper turns "we
# could not check" into "he is guilty". A ceiling is the right instrument there -- it withholds a good
# score without inventing a bad one, and the thin-record shrink is already pulling him down as well.
PEN_OFTEN                = 20.0           # frequent (measured): CONDUCT −20
CAP_UNPROVEN             = 65.0           # unproven: ceiling, not a deduction
CAP_OFTEN_TOT            = 74.0           # both: TOTAL capped at 🟡

CAP_SYS,   CAP_SYS_TOT   = 45.0, 49.0     # systematic: capped below 🟠
tier, tier_why = 'none', ''
if lp_removed:
    tier, tier_why = 'sys', 'lp'
elif n_tr < 5:
    # too few traded coins to trust a rate: fall back to count, and to whether the
    # flagship itself was cut. Never call this tier clean — it is unproven, not proven.
    tier = 'sys' if (len(cut) >= 2 or top1_cut) else 'often_unproven'
else:
    if cut_rate > 0.75 or top1_cut: tier = 'sys'
    elif len(cut) == 0:             tier = 'none'   # measured clean, not merely unproven
    elif cut_rate <= 0.30:          tier = 'rare'
    else:                           tier = 'often'
if   tier == 'often':          cred = max(0.0, cred - PEN_OFTEN)
elif tier == 'often_unproven': cred = min(cred, CAP_UNPROVEN)
elif tier == 'sys':            cred = min(cred, CAP_SYS)
# TOTAL is recomputed from the POST-gate CONDUCT, then capped. It used to be computed once before the gate
# and only ceilinged afterwards, so a gated dev printed a sum that did not add up: CONDUCT 65 + bonus 2.8
# = 69, because the 69 still came from the uncapped 66. Cap the input, not just the answer.
total = R(_clamp(cred + bonus, 0.0, 100.0))
if   tier in ('often', 'often_unproven'): total = min(total, CAP_OFTEN_TOT)
elif tier == 'sys':                       total = min(total, CAP_SYS_TOT)
# The dump gate can never fire on a coin whose exit is invisible -- a flagship dump needs a sell row to exist.
# So the same ceiling the unproven tier uses applies here: he may be clean, but it cannot be shown.
if opaque_exit: total = min(total, CAP_OFTEN_TOT)

# ── 8. Verdict band ───────────────────────────────────────
# Four bands, named not worded. The caller says them in the reader's language; what must not
# drift is WHERE the cuts are, because every number above was calibrated against these.
band = ('buyable' if total >= 75 else 'mixed' if total >= 50 else
        'avoid'   if total >= 30 else 'stay_away')

# ── 9. Emit ───────────────────────────────────────────────
# One JSON object of measured facts and the terms derived from them. Deliberately not a
# report: no wording, no ordering, no language, no thresholds re-stated as sentences. Keys
# carry their unit (`_usd`, `_s`, `_days`, `_rate`) so a number cannot be read in the wrong
# one, and a value the data could not establish is `null` -- never 0, which would read as a
# measurement. Every symbol and address below has already been through safe().

def coin(t):
    a = t_ath(t); m = _f(t.get('market_cap')); ts = _f(t.get('create_timestamp'))
    return {
        'symbol':        safe(t.get('symbol'), 16),
        'token':         safe(t.get('token_address'), 64),
        'peak_mc_usd':   a,
        'mc_usd':        m,
        'drawdown':      (1.0 - m / a) if a > 0 else None,
        'holders':       _f(t.get('holders')),
        'pool_usd':      _f(t.get('pool_liquidity')),
        'tradeable':     is_alive(t),
        'age_days':      max(0.0, (NOW - ts) / 86400) if ts > 0 else None,
        'created_ts':    ts,
        'bundler_rate':  _f(t.get('bundler_rate')) if t.get('bundler_rate') not in (None, '') else None,
    }

def move(m):
    return {
        'symbol':             m['sym'],
        'token':              safe(m['tok'], 64),
        'to':                 m['to_disp'],
        'share_of_supply':    m['share'],
        'usd':                m['usd'],
        'seconds_after_open': m['after'],
        'before_open':        m['pre'],
        'same_as_funder':     m.get('same_as_funder', False),
        'sold_usd':           m.get('sold'),
        'first_sell_s':       m.get('fs'),
        'unchecked':          m.get('unchecked', False),
    }

emit({
    'scored': True, 'chain': CHAIN, 'dev': DEV, 'as_of': NOW, 'mode': MODE,

    'score': {'total': total, 'conduct': cred, 'power': power, 'bonus': bonus, 'band': band},

    # What each axis is made of, so the caller can name the one term that decided the answer
    # without recomputing anything. The shrink is reported as from/to because that is what it
    # did -- it pulls an unproven score toward 60 ("we cannot tell"), it is not a fine.
    'conduct_terms': {
        'raw': raw, 'dump_pen': dump_pen, 'abandon_pen': abandon_pen,
        'shrink_from': raw, 'shrink_to': cred_pre, 'shrunk': shrunk, 'shrink_weight': w,
        'factory_pen': factory_pen, 'opaque_pen': opaque_pen,
        'mean_severity': mean_sev, 'median_severity': med_sev,
    },
    'power_terms': {
        'peak': B1, 'repeatable': B2, 'flagship_alive': B3, 'book_quality': B4,
        'book_weight': w_book, 'drawdown_term': dd_term,
    },

    # The gate. `key` is the tier, `forced_by` names what fired it when it was not the dump
    # rate itself ('lp' = a drained pool), and the caps say which ceiling actually bound.
    'dump_gate': {
        'tier': tier, 'forced_by': tier_why or None,
        'dumps': len(cut), 'coins_with_trades': n_tr, 'dump_rate': cut_rate,
        'flagship_dumped': top1_cut,
        'definition': {'multiple_at_least': CUT_MULT, 'first_sell_within_s': CUT_SEC,
                       'severity_full_multiple': SEV_MULT_FULL, 'severity_zero_s': SEV_SEC_ZERO},
        'caps': {'conduct_pen_frequent': PEN_OFTEN, 'conduct_cap_unproven': CAP_UNPROVEN,
                 'total_cap_frequent': CAP_OFTEN_TOT, 'conduct_cap_systematic': CAP_SYS,
                 'total_cap_systematic': CAP_SYS_TOT},
        'total_capped': total < R(_clamp(cred + bonus, 0.0, 100.0)) or bool(opaque_exit),
    },

    'launches': {
        'total': N, 'counter_total': N_ctr, 'on_curve': inner, 'graduated': opened,
        'graduation_rate': grad, 'sampled': len(toks), 'tradeable': alive,
        'survival_rate': surv, 'survival_den': surv_den,
        'stuck_rate': stuck, 'walkaway_rate': cto,
        'over_1m': k1m, 'median_drawdown_over_1m': dd_big,
        'career_days': career_days, 'career_days_is_floor': career_floor,
    },

    'his_trades': {
        'coins_with_trades': n_tr, 'coins_with_pull_multiple': n_mult,
        'median_pull_multiple': med_mult,
        'median_first_sell_s': med_delay, 'fastest_first_sell_s': min_delay,
        'self_snipe_rate': snipe_rate,
        'dumped_coins': len(cut), 'sell_without_buy_coins': len(no_buy),
        'severity_by_token': {safe(k, 64): v for k, v in sev_by.items()},
    },

    'liquidity': {
        'drained': [safe((by_addr.get(a) or {}).get('symbol') or a[:6], 16) for a in lp_drained],
        'partial': [safe((by_addr.get(a) or {}).get('symbol') or a[:6], 16) for a in lp_partial],
        'ignored_rows': lp_zero, 'forces_gate': lp_removed,
        'min_share_of_supply': LP_MIN_SHARE, 'min_usd': LP_MIN_USD,
    },

    # `holds` is tri-state on purpose: True/False only when the API SAID something, null when
    # it returned nothing. `not closed` was being read as "he is holding", which is an
    # affirmative claim about a bag the data does not show.
    'flagship': (dict(coin(top1), status=top1_status, holds=top1_hold, balance=top1_bal,
                      position_closed=top1_closed, dumped=top1_cut,
                      age_days=top1_days, age_from=top1_age_src,
                      exit_rows=exit_kinds, exit_accounted_by=exit_accounted,
                      exit_unrecorded=opaque_exit) if top1 else None),
    'top': [coin(t) for t in top],

    'cross_wallet': {
        'enabled': SIB_ON, 'moves': [move(m) for m in moves[:SIB_MAX_CHECK]],
        'sold': [move(m) for m in sib_sold], 'pending': [move(m) for m in sib_pending],
        'total_moves': len(moves), 'verified': min(len(moves), SIB_MAX_CHECK),
        'min_share_of_supply': SIB_MIN_SHARE,
    },

    'bundler': {'median': br_med, 'threshold': BUND_HOT,
                'hot': [{'symbol': safe(t.get('symbol'), 16),
                         'rate': _f(t.get('bundler_rate'))} for t in br_hot]},

    # Everything that limits how far the numbers above may be pushed. A caller that omits
    # this section is over-claiming: the book is a window, not a career, whenever
    # `book_truncated` is true, and `unresolved_coins` can only ever hide dumps, never add any.
    'coverage': {
        'refetched': refetched,
        'pages_walked': pages, 'max_pages': MAX_PAGES, 'top_k_resolved': TOP_K,
        'trade_history_truncated': truncated, 'unresolved_coins': len(unresolved),
        'book_truncated': book_trunc,
        'book_oldest_ts': _bcts[0] if _bcts else None,
        'book_bulk_from_ts': _bcts[_bulk_i] if _bcts else None,
        'book_has_old_straggler': book_narrow, 'book_bulk_span_h': book_span_h,
        'implausible_peaks': [coin(t) for t in ath_junk],
    },
})
