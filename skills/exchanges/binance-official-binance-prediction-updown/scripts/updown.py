#!/usr/bin/env python3
"""Recurring BTC Up/Down prediction-market daemon for Binance Agentic Wallet.

Defaults to dry-run; places no real orders until explicitly told to.

    round enumeration -> market screening -> probability hook -> price comparison
    -> guards -> quote -> order -> fill confirm -> settlement -> redeem

DISCLAIMER
    This is a scaffold. The bundled strategy is a reference implementation built
    from one measured effect on one proxy data series; it is not a recommendation
    and carries no guarantee of positive expectancy. Every risk control and
    parameter here is a suggestion, not a safeguard: the daemon runs the checks
    you configure and does not judge whether they are sufficient.

    Nothing here is investment advice. Prediction-market positions can expire
    worthless. Automated trading can lose money through market conditions you did
    not anticipate, changes in platform behavior, or defects in this software. It
    is provided as-is, without warranty. You are solely responsible for what you
    run and for any funds you commit.
"""
import json, os, math, subprocess, sys, threading, time, fcntl, argparse
from datetime import datetime, timezone

D = os.path.expanduser(os.environ.get("UPDOWN_HOME", "~/.local/updown"))
os.makedirs(D, exist_ok=True)
CFG_F, ST_F = f"{D}/config.json", f"{D}/state.json"
LOG_F = f"{D}/updown.log"
ROUNDS_J, ORDERS_J, OUTCOMES_J, QUOTES_J = (f"{D}/rounds.jsonl", f"{D}/orders.jsonl",
                                            f"{D}/outcomes.jsonl", f"{D}/quotes.jsonl")
STOP_F, KILL_F = f"{D}/STOP", f"{D}/KILL"
LIVE_ACK_F = f"{D}/I_UNDERSTAND_THE_RISK"
LOCK_F = f"{D}/updown.lock"


CLI_MIN = "1.9.1"          # must match the frontmatter requiredCliVersion

# Measured against the live endpoint: quote rejects anything smaller with
# "Trade amount is below minimum 1 USDT". Clamping a stake below this produces
# an order that is guaranteed to fail, so the daemon refuses instead.
MIN_ORDER_USD = 1.0

# Binance market-data intervals, keyed by the platform's timeframe strings. The
# streak must be measured on the clock the round runs on: hourly candles do not
# describe a five-minute round, and a strategy validated on one is not validated
# for the other.
TF_INTERVAL = {"5 min": "5m", "15 min": "15m", "1 hour": "1h", "daily": "1d"}

# Plumbing only. Nothing here changes how much money can be lost.
DEFAULTS = dict(
    mode="dry-run",                 # dry-run | collect-quotes | live
    poll_sec=60,                    # how often to re-enumerate rounds
    settle_poll_sec=120,            # how often to sweep settlements and redemptions
    kline_refresh_sec=300,
    l1_category="crypto",
    l2_category="up-down",
)

# Capital-touching parameters. No defaults on purpose: a stake size you never
# decided on is exactly as dangerous as a stop you never decided on.
REQUIRED_CFG = ["chain", "symbol", "timeframe", "budget_usd", "stake_usd",
                "max_open_rounds", "max_rounds_per_day", "max_consecutive_losses"]

# Read by the bundled hooks. Replace the hooks and this list changes with them;
# the mechanism layer never interprets these keys.
# fee_bps is NOT here: the platform publishes feeRateBps per topic and that is
# the number that actually bills. Taking it from config would let a stale guess
# silently understate the hurdle.
REQUIRED_POLICY = ["min_streak", "edge_threshold", "max_overround",
                   "max_spread", "min_seconds_to_close", "max_seconds_to_close",
                   "slippage_bps", "expected_slippage_bps", "hit_table"]

SAVE_LK = threading.Lock()
BUDGET_LK = threading.Lock()
S = {}
CFG = {}
LIVE = False


# ══════════════════════════════════════════════════════════════════
#  STRATEGY HOOKS — this block is yours to edit; the mechanism layer
#  never touches it.
#
#  estimate_probability() deliberately cannot see the quote. If it could,
#  you (or a model) would anchor on the market price, and the calibration
#  report would then measure an estimator that looks accurate while holding
#  no edge at all. The mechanism layer compares to the quote afterwards.
# ══════════════════════════════════════════════════════════════════

def estimate_probability(rnd, ctx):
    """Return P(the round closes UP), or None to skip. The mechanism layer then
    compares it against the quote — this function never sees a price.

    Available signals (check before use — several can be None):
      ctx["streak"]      length of the current run of same-direction closed candles
      ctx["streak_dir"]  1 = that run is up, 0 = down
      rnd["feed"]        which oracle settles this round (BINANCE / CHAINLINK)
      rnd["start_price"] the round's reference price, published by the topic
      rnd["close_ms"]    settlement time
      ctx["policy"]      the `policy` section of config.json, verbatim
      ctx["open"]        rounds currently held

    ── The implementation below is a minimal reference that runs, NOT a
       recommended strategy ──
    It reads one mechanical feature (how long the current run is) and looks the
    answer up in a table YOU supply, because the only honest source for those
    numbers is your own measurement of the cadence you trade. Things worth
    knowing while you design yours:

      · Cost, not direction, is the binding constraint. A fee of 200 bps per
        round plus slippage means roughly a 2-3% hurdle EVERY round; a signal
        worth 3pp over a coin flip nets almost nothing. Compute the hurdle
        before you get attached to a hit rate.
      · A hit rate is not an edge. If the market already prices the state your
        signal keys on, a 58% hit rate earns zero. `backtest.py pricedin` is the
        only thing that can rule this out, and it needs live collection first.
      · At-the-money rounds have a fair value of ~0.50 by construction. There is
        no model edge to find there; anything you win comes from the market
        mispricing that 0.50, which is a different and harder claim.
      · Streak length is tempting because it looks like a dose-response, but
        measured across all four cadences the family only rises monotonically on
        one of them. One in four is what noise looks like.
      · An estimator that can see the quote will anchor on it and then score
        beautifully while holding no edge. That is why ctx carries no price —
        resist the urge to fetch one here.
      · Over-rejection looks exactly like "there were no opportunities". Before
        adding a gate, make sure you can see what it rejected in the `decision`
        distribution of rounds.jsonl.
    """
    p = ctx["policy"]
    streak, direction = ctx["streak"], ctx["streak_dir"]
    if streak is None or streak < p["min_streak"]:
        return None
    # policy.hit_table is required and ships with no default: it describes one
    # cadence on one symbol, and a table borrowed from another describes nothing.
    # `backtest.py eval --interval <iv>` prints one ready to paste.
    table = {int(k): float(v) for k, v in (p["hit_table"] or {}).items()}
    if not table:
        return None
    hit = table.get(min(streak, max(table)), table[max(table)])
    # Reversal: a run of ups predicts a down, and vice versa.
    return 1.0 - hit if direction == 1 else hit


def size_position(rnd, ctx, edge):
    """Return the USD stake. The mechanism layer then clamps it to
    min(value, stake_usd, remaining budget).

    Bundled reference: flat stake. Edge-proportional sizing is tempting, but the
    edge estimate here is itself uncertain, and scaling by an uncertain number
    mostly scales the error.
    """
    return ctx["cfg"]["stake_usd"]


# ══════════════════════════════════════════════════════════════════
#  Mechanism layer below. Guards are enforced here and hooks cannot
#  bypass them; their values come from your config.
# ══════════════════════════════════════════════════════════════════

def now_ms():
    return int(time.time() * 1000)


def log(msg):
    line = f"{datetime.now(timezone.utc):%Y-%m-%d %H:%M:%S} {msg}"
    print(line, flush=True)
    try:
        with open(LOG_F, "a") as f:
            f.write(line + "\n")
    except OSError:
        pass


def jsonl(path, obj):
    try:
        with open(path, "a") as f:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")
    except OSError as e:
        log(f"WARN cannot append {path}: {e}")


def fnum(x, default=None):
    try:
        if x is None or x == "":
            return default
        return float(x)
    except (TypeError, ValueError):
        return default


def baw(*args, timeout=60):
    """Call the CLI and return parsed JSON, or None. Never raises."""
    cmd = ["baw"] + [str(a) for a in args] + ["--json"]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        log(f"WARN timeout: {' '.join(cmd[:4])}")
        return None
    try:
        return json.loads(r.stdout)
    except Exception:
        if r.stdout.strip() or r.stderr.strip():
            log(f"WARN unparsable: {' '.join(cmd[:4])} -> {(r.stdout or r.stderr)[:160].strip()}")
        return None


def ok(resp):
    return bool(resp) and resp.get("success") is True


def api_err(resp):
    if not resp:
        return "no response"
    e = resp.get("error") or {}
    return f"{e.get('name') or e.get('code')}: {e.get('message')}"


def session_alive(resp):
    """A dead session must never look like a quiet market. Any auth failure is
    surfaced loudly and recorded as the reason a round was skipped."""
    if resp and resp.get("success") is False:
        name = (resp.get("error") or {}).get("name", "")
        if name in ("NOT_LOGGED_IN", "SESSION_EXPIRED"):
            return False
    return True


# ───────────────────────────── state ────────────────────────────

def load_state():
    global S
    try:
        S = json.load(open(ST_F))
    except Exception:
        S = {}
    S.setdefault("deployed", 0.0)        # capital at risk right now (open stakes)
    S.setdefault("realized_pnl", 0.0)    # cumulative settled P&L, signed
    S.setdefault("open", {})           # roundKey -> position record
    S.setdefault("done", {})           # roundKey -> settled record
    S.setdefault("day", "")
    S.setdefault("rounds_today", 0)
    S.setdefault("consecutive_losses", 0)
    S.setdefault("halt_reason", None)


def save():
    with SAVE_LK:
        tmp = f"{ST_F}.{os.getpid()}.tmp"
        try:
            with open(tmp, "w") as f:
                json.dump(S, f, indent=1)
            os.replace(tmp, ST_F)
        except OSError as e:
            log(f"WARN state save failed: {e}")


def worst_case_room():
    """How much more may be put at risk before the worst case breaches budget.

    `budget_usd` is documented as an amount whose total loss is acceptable, so
    that is what it is enforced as: every open stake is assumed to lose, and the
    losses already realised are counted. The invariant is

        realised losses + capital currently at risk  <=  budget_usd

    which holds even if every open round settles to zero. An earlier version
    treated `deployed` as cumulative turnover and never decremented it at
    settlement, which stopped the daemon after budget/stake rounds regardless of
    whether it had lost anything — a halt unrelated to risk, and in direct
    conflict with the sample sizes this strategy family needs.
    """
    with BUDGET_LK:
        lost = max(0.0, -(fnum(S.get("realized_pnl"), 0.0) or 0.0))
        at_risk = fnum(S.get("deployed"), 0.0) or 0.0
        return fnum(CFG["budget_usd"], 0.0) - lost - at_risk


def add_deployed(usd):
    # Read-modify-write under the same lock the budget gate reads it under, so
    # one lock covers both sides of the invariant rather than two that disagree.
    with BUDGET_LK:
        S["deployed"] = (fnum(S.get("deployed"), 0.0) or 0.0) + usd


def roll_day():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if S.get("day") != today:
        S["day"] = today
        S["rounds_today"] = 0


# ────────────────────────── config / gates ──────────────────────

TEMPLATE = {
    "chain": "",
    "symbol": "",          # BTCUSDT | ETHUSDT | BNBUSDT
    "timeframe": "",       # "5 min" | "15 min" | "1 hour" | "daily"
    "budget_usd": None,
    "stake_usd": None,
    "max_open_rounds": None,
    "max_rounds_per_day": None,
    "max_consecutive_losses": None,
    "mode": "dry-run",
    # slippage_bps = order tolerance; expected_slippage_bps = measured typical
    # loss used in the edge calculation. They are not the same number.
    "policy": {k: None for k in REQUIRED_POLICY},
}


def load_config():
    global CFG, LIVE
    if not os.path.exists(CFG_F):
        with open(CFG_F, "w") as f:
            json.dump(TEMPLATE, f, indent=2)
        sys.exit(f"wrote an empty config template to {CFG_F}\n"
                 f"fill every field and start again. Nothing here has a default, "
                 f"because a value you never decided on is not a safe value.")
    CFG = json.load(open(CFG_F))
    for k, v in DEFAULTS.items():
        CFG.setdefault(k, v)
    pol = CFG.get("policy") or {}

    missing = [k for k in REQUIRED_CFG if CFG.get(k) in (None, "", [])]
    missing += [f"policy.{k}" for k in REQUIRED_POLICY if pol.get(k) in (None, "")]
    if missing:
        sys.exit("refusing to start — these are unset and have no default:\n  "
                 + "\n  ".join(missing))
    if fnum(CFG.get("stake_usd"), 0.0) < MIN_ORDER_USD:
        sys.exit(f"stake_usd is {CFG.get('stake_usd')} but the platform minimum is "
                 f"{MIN_ORDER_USD} USDT — every order would be rejected.")
    if fnum(CFG.get("budget_usd"), 0.0) < fnum(CFG.get("stake_usd"), 0.0):
        sys.exit(f"budget_usd ({CFG.get('budget_usd')}) is smaller than stake_usd "
                 f"({CFG.get('stake_usd')}) — not a single round could be opened.")
    CFG["policy"] = pol
    LIVE = CFG.get("mode") == "live"
    return CFG


def live_confirmed():
    """Live mode requires acknowledging the amount at risk, by writing the
    current budget into a file. Requiring the number rather than mere existence
    means the acknowledgement cannot be inherited by copying someone else's
    runtime directory, and that raising budget_usd invalidates it."""
    want = fnum(CFG.get("budget_usd"))
    if not os.path.exists(LIVE_ACK_F):
        return False, f"missing {LIVE_ACK_F}"
    try:
        got = fnum(open(LIVE_ACK_F).read().strip().replace("$", "").replace(",", ""))
    except OSError as e:
        return False, str(e)
    if got is None:
        return False, "acknowledgement file holds no number"
    if abs(got - want) > 1e-9:
        return False, f"acknowledged {got} but budget_usd is {want}"
    return True, "ok"


def cli_version_ok():
    """cli-check returns success:true even when an update is needed; the verdict
    lives in data.needUpdateCli, not in the envelope."""
    r = baw("cli-check", "--required-version", CLI_MIN)
    if not r:
        return False, "cli-check produced no output"
    need = (r.get("data") or {}).get("needUpdateCli")
    if need is True:
        return False, f"CLI below required {CLI_MIN}"
    return True, "ok"


def acquire_lock():
    """flock, held for the process lifetime. A single kernel-arbitrated call with
    no create-then-write window, and the kernel releases it when the holder dies,
    which removes the whole notion of a stale lock needing cleanup."""
    fd = os.open(LOCK_F, os.O_RDWR | os.O_CREAT, 0o644)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        try:
            holder = open(LOCK_F).read().strip()
        except OSError:
            holder = "?"
        sys.exit(f"another instance holds {LOCK_F} (pid {holder})")
    os.ftruncate(fd, 0)
    os.write(fd, str(os.getpid()).encode())
    return fd      # keep referenced for the process lifetime


# ─────────────────────── price series / streak ──────────────────

_kl = {"ts": 0, "rows": [], "sym": None}   # sym = (symbol, interval)


def kline_interval():
    """Candle interval for the streak. Follows the round cadence unless the
    config overrides it — someone whose signal genuinely lives on another clock
    should be able to say so, explicitly."""
    return CFG.get("kline_interval") or TF_INTERVAL.get(CFG.get("timeframe"), "1h")


def klines(limit=200):
    """Recent candles for the configured symbol at the round's own cadence.

    Read from the public Binance market-data endpoint — no key, no session. That
    is the feed the BINANCE-fed timeframes settle against; the CHAINLINK ones
    resolve elsewhere, which pre-flight warns about.
    """
    sym = CFG.get("symbol") or "BTCUSDT"
    iv = kline_interval()
    if (time.time() - _kl["ts"] < CFG.get("kline_refresh_sec", 300)
            and _kl["rows"] and _kl["sym"] == (sym, iv)):
        return _kl["rows"]
    url = (f"https://api.binance.com/api/v3/klines?symbol={sym}"
           f"&interval={iv}&limit={int(limit)}")
    try:
        import urllib.request
        with urllib.request.urlopen(url, timeout=20) as r:
            raw = json.load(r)
        rows = [[float(c[1]), float(c[2]), float(c[3]), float(c[4]),
                 float(c[5]), int(c[0]), 0] for c in raw]
    except Exception as e:
        log(f"WARN kline fetch failed ({sym} {iv}): {e}")
        return _kl["rows"]
    rows.sort(key=lambda c: c[5])
    _kl.update(ts=time.time(), rows=rows, sym=(sym, iv))
    try:
        json.dump(rows, open(f"{D}/klines_{iv}.json", "w"))
    except OSError:
        pass
    return rows


def streak_state():
    """(length, direction) of the current run of same-direction closed hours.
    Only *closed* candles count; the in-progress hour is excluded, because its
    direction can still flip and a strategy that reads it is reading noise."""
    rows = klines()
    if len(rows) < 6:
        return None, None
    closed = rows[:-1]
    up = [1 if c[3] > c[0] else 0 for c in closed]
    d = up[-1]
    n = 0
    for v in reversed(up):
        if v != d:
            break
        n += 1
    return n, d


# ──────────────────────── round enumeration ─────────────────────

def list_rounds():
    """Enumerate Up/Down topics for the configured symbol and timeframe.

    Shape confirmed against the live endpoint: data.marketTopics[] -> markets[]
    -> outcomes[]. Each topic covers one symbol at one cadence (5 min / 15 min /
    1 hour / daily) and carries its own fee, slippage default and price feed.
    """
    r = baw("prediction", "market", "list",
            "--l1Category", CFG["l1_category"], "--l2Category", CFG["l2_category"],
            "--limit", 50)
    if not session_alive(r):
        return None, "session"
    if not ok(r):
        return None, api_err(r)
    topics = (r.get("data") or {}).get("marketTopics") or []
    want_s, want_t = CFG["symbol"], CFG["timeframe"]
    return [t for t in topics if isinstance(t, dict)
            and t.get("symbol") == want_s and t.get("timeframe") == want_t], None


def pick(d, *names, default=None):
    for n in names:
        if isinstance(d, dict) and d.get(n) not in (None, ""):
            return d[n]
    return default


def parse_round(topic):
    """Normalise one topic into the round the pipeline works with.

    Returns None when the topic is not a tradable two-outcome Up/Down round.
    """
    markets = topic.get("markets") or []
    if not markets:
        return None
    m = markets[0]
    if str(m.get("tradingStatus", "")).upper() != "OPEN":
        return None
    outs = m.get("outcomes") or []
    if len(outs) != 2:
        return None
    up = down = None
    for o in outs:
        nm = str(o.get("name", "")).strip().lower()
        if nm == "up":
            up = o
        elif nm == "down":
            down = o
    if not (up and down):
        return None
    vd = topic.get("variantData") or {}
    return {
        "key": str(m.get("marketId")),
        "topicId": topic.get("marketTopicId"),
        "marketId": m.get("marketId"),
        "title": m.get("question") or topic.get("title") or "",
        "close_ms": int(topic["endDate"]) if topic.get("endDate") else None,
        "start_ms": int(topic["startDate"]) if topic.get("startDate") else None,
        "fee_bps": fnum(topic.get("feeRateBps"), 0.0) or 0.0,
        "default_slippage_bps": topic.get("slippageBps"),
        "feed": vd.get("priceFeedProvider"),
        "feed_symbol": vd.get("priceFeedSymbol"),
        "start_price": fnum(vd.get("startPrice")),
        "liquidity": fnum(topic.get("liquidity"), 0.0),
        "up": {"name": "Up", "tokenId": up.get("tokenId"), "price": fnum(up.get("price"))},
        "down": {"name": "Down", "tokenId": down.get("tokenId"), "price": fnum(down.get("price"))},
    }


def book(market_id, token_id):
    """Best ask / best bid and the size resting there.

    order-book takes --marketId, NOT --marketTopicId. They are different ids and
    passing the topic id fails outright, which is the friendly case; the unfriendly
    one would have been a silent empty book.
    """
    r = baw("prediction", "market", "order-book",
            "--marketId", market_id, "--tokenId", token_id)
    if not session_alive(r):
        return None, "session"
    if not ok(r):
        return None, api_err(r)
    d = r.get("data") or {}

    def lvl(side):
        if not side or not isinstance(side[0], dict):
            return None, 0.0
        return fnum(side[0].get("price")), fnum(side[0].get("size"), 0.0)

    ask, ask_sz = lvl(d.get("asks"))
    bid, bid_sz = lvl(d.get("bids"))
    return {"ask": ask, "ask_size": ask_sz, "bid": bid, "bid_size": bid_sz}, None


# ─────────────────────────── screening ──────────────────────────

def read_book(rnd):
    """Fetch both sides of the book. No judgement — just what is quoted."""
    bu, err = book(rnd["marketId"], rnd["up"]["tokenId"])
    if err:
        return None, f"order-book up: {err}"
    bd, err = book(rnd["marketId"], rnd["down"]["tokenId"])
    if err:
        return None, f"order-book down: {err}"
    if not bu or not bd or bu["ask"] is None or bd["ask"] is None:
        return None, "incomplete book"
    secs = ((rnd["close_ms"] - now_ms()) / 1000.0) if rnd["close_ms"] else None
    # Prices come back at two decimals, so these differences are exact in intent
    # but not in binary: 0.57 - 0.55 evaluates to 0.020000000000000018, and a
    # threshold of 0.02 would reject a book that is exactly at the limit.
    return {"up_ask": bu["ask"], "up_bid": bu["bid"], "up_ask_size": bu["ask_size"],
            "dn_ask": bd["ask"], "dn_bid": bd["bid"], "dn_ask_size": bd["ask_size"],
            "overround": round(bu["ask"] + bd["ask"] - 1.0, 6),
            "secs_to_close": round(secs, 1) if secs is not None else None}, None


def gate(rnd, q):
    """Apply the tradability gates to an already-read book.

    Separate from read_book on purpose: collection records every book it can
    see, including the ones this configuration would refuse. Recording only the
    books that pass your own filters biases the priced-in sample towards tight
    markets and throws away most of the data.
    """
    p = CFG["policy"]
    if not rnd["close_ms"]:
        return "no close time on the topic"
    secs = q.get("secs_to_close")
    if secs is None:
        return "no close time on the topic"
    if secs < p["min_seconds_to_close"]:
        return f"too close to settlement ({secs:.0f}s)"
    if secs > p["max_seconds_to_close"]:
        return f"outside the entry window ({secs:.0f}s)"
    if q["overround"] > p["max_overround"]:
        return f"overround {q['overround']:.4f} > {p['max_overround']}"
    for nm, a, b in (("up", q["up_ask"], q["up_bid"]), ("down", q["dn_ask"], q["dn_bid"])):
        if b is None:
            continue
        spread = round(a - b, 6)
        if spread > p["max_spread"]:
            return f"{nm} spread {spread:.4f} > {p['max_spread']}"
    return None


def cost_fraction(rnd):
    """Expected cost per round, as a fraction of the payout.

    Two different numbers get confused here, and confusing them is expensive in
    both directions:

      slippage_bps           a TOLERANCE sent with the order — the worst fill
                             you will accept. It is not money you expect to pay.
      expected_slippage_bps  what you actually lose to the book on a typical
                             fill, measured from your own executions.

    Subtracting the tolerance would charge every round for a worst case that
    rarely happens, which silently suppresses trades that were worth taking.
    Only the fee (published per topic) and your measured slippage belong here.

    Calibrate expected_slippage_bps from the ALL-IN lines the daemon logs after
    each fill: effective price paid versus the ask that was quoted.
    """
    return (rnd["fee_bps"] + fnum(CFG["policy"]["expected_slippage_bps"], 0.0)) / 10000.0


def valid_prob(x):
    """A hook is user code and can be wrong. An out-of-range probability is not
    a strong opinion — it is a bug, and left unchecked it produces the largest
    possible 'edge' and therefore the most confident order the scaffold can
    place. Reject rather than clamp: silently rescaling someone's broken output
    hides the defect and keeps trading on it."""
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None, f"hook returned a non-numeric probability: {x!r}"
    if v != v or v in (float("inf"), float("-inf")):
        return None, "hook returned a non-finite probability"
    if not (0.0 <= v <= 1.0):
        return None, f"hook returned {v} — a probability must be within [0, 1]"
    return v, None


def decide(prob_up, q, rnd):
    """Three branches; 'no trade' is the common one by design.

    The breakeven hit rate is the quoted price plus costs: buying Up at 0.55 with
    a 2% fee needs a better-than-57% long-run hit rate. Enforced here rather than
    left to the strategy, because at this cadence costs dominate the result.
    """
    for side in ("up_ask", "dn_ask"):
        v = q.get(side)
        # A tradable outcome price lives strictly inside (0, 1). Zero or missing
        # is bad data, and bad data reads as a free lunch to the edge formula.
        if v is None or not (0.0 < float(v) < 1.0):
            return None, float("-inf"), None
    c = cost_fraction(rnd)
    thr = CFG["policy"]["edge_threshold"]
    up_edge = prob_up - q["up_ask"] - c
    dn_edge = (1.0 - prob_up) - q["dn_ask"] - c
    if up_edge >= dn_edge and up_edge > thr:
        return "up", up_edge, q["up_ask"]
    if dn_edge > up_edge and dn_edge > thr:
        return "down", dn_edge, q["dn_ask"]
    return None, max(up_edge, dn_edge), None


# ─────────────────────────── execution ──────────────────────────

def place(rnd, side, usd):
    """quote -> confirm -> place. A quote expires; a stale one is refetched once
    rather than failing the round."""
    token = rnd[side]["tokenId"]
    for attempt in (1, 2):
        q = baw("prediction", "trade", "quote",
                "--binanceChainId", CFG["chain"], "--tokenId", token,
                "--marketTopicId", rnd["topicId"], "--side", "BUY",
                "--amount", f"{usd:.2f}", "--orderType", "MARKET",
                "--slippageBps", int(CFG["policy"]["slippage_bps"]))
        if not session_alive(q):
            return None, "session"
        if not ok(q):
            return None, f"quote: {api_err(q)}"
        qd = q.get("data") or {}
        quote_id = pick(qd, "quoteId", "id")
        slip = pick(qd, "slippageBps", default=int(CFG["policy"]["slippage_bps"]))
        r = baw("prediction", "trade", "place-order",
                "--quoteId", quote_id, "--slippageBps", slip, "--orderType", "MARKET")
        if ok(r):
            return {"quote": qd, "order": r.get("data") or {}}, None
        msg = api_err(r)
        if attempt == 1 and ("expire" in msg.lower() or "stale" in msg.lower()):
            log(f"  quote expired, refetching")
            continue
        return None, f"place-order: {msg}"
    return None, "quote kept expiring"


def confirm_fill(order_id, tries=12, gap=3):
    """A successful placement means *submitted*, not filled.

    Observed live: `place-order` returns success and the order then settles to
    status FAILED ("Failed to execute the market order") with zero filled. Treat
    the placement response as a receipt, never as a fill.

    The history payload keys the list as `orders`.
    """
    terminal_ok = ("FILLED", "SUCCESS", "COMPLETED", "DONE")
    terminal_bad = ("FAILED", "CANCELED", "CANCELLED", "EXPIRED", "REJECTED")
    for _ in range(tries):
        r = baw("prediction", "order", "history", "--limit", 50)
        if ok(r):
            rows = (r.get("data") or {}).get("orders") or []
            for o in rows:
                if not isinstance(o, dict):
                    continue
                if str(o.get("orderId")) != str(order_id):
                    continue
                st = str(o.get("status", "")).upper()
                if st in terminal_ok or st in terminal_bad:
                    return o, st
        time.sleep(gap)
    return None, "UNCONFIRMED"


def book_pnl(pnl):
    """Fold a settled round's realised P&L into the running total."""
    with BUDGET_LK:
        S["realized_pnl"] = (fnum(S.get("realized_pnl"), 0.0) or 0.0) + (fnum(pnl, 0.0) or 0.0)


def release(key, usd, why):
    """Undo a reservation when the order did not become a position.

    Without this a failed order consumes budget forever and leaves a phantom
    open round that blocks max_open_rounds — the daemon's books diverge from the
    account, and every later guard reads the wrong number.
    """
    with BUDGET_LK:
        S["deployed"] = max(0.0, (fnum(S.get("deployed"), 0.0) or 0.0) - usd)
    if S["rounds_today"] > 0:
        S["rounds_today"] -= 1
    S["open"].pop(key, None)
    save()
    log(f"RELEASED {key} ${usd:.2f} back to budget — {why}")


# ───────────────────── settlement and redemption ────────────────

def redeem_sweep():
    """Winnings do not become money on their own. Unclaimed payouts are idle
    capital, and the next round's stake may be sitting inside them.

    redeem takes --tokenIds (plural, comma-separated) and settles them in one
    batch, so sweep everything claimable in a single call rather than looping —
    fewer on-chain interactions and one batchId to follow up on.
    """
    r = baw("prediction", "position", "list", "--tab", "PENDING_CLAIM", "--limit", 50)
    if not session_alive(r):
        log("ALERT session expired during redeem sweep — winnings stay unclaimed")
        return
    if not ok(r):
        return
    data = r.get("data") or {}
    rows = data.get("positions") or data.get("list") or []
    ids = [str(p.get("tokenId")) for p in rows
           if isinstance(p, dict) and p.get("tokenId") and p.get("canClaim")]
    if not ids:
        return
    rr = baw("prediction", "trade", "redeem",
             "--tokenIds", ",".join(ids), "--binanceChainId", CFG["chain"])
    if not ok(rr):
        log(f"WARN redeem failed for {len(ids)} position(s): {api_err(rr)}")
        return
    d = rr.get("data") or {}
    # Submitted is not settled here either: each result carries its own status
    # and may sit PENDING for a while. The next sweep re-reads PENDING_CLAIM, so
    # anything that silently failed comes back around rather than being lost.
    results = d.get("results") or []
    pending = sum(1 for x in results if str(x.get("status", "")).upper() == "PENDING")
    log(f"REDEEM submitted {len(ids)} position(s) batch={d.get('batchId')} "
        f"pending={pending}")
    jsonl(ORDERS_J, {"ts": now_ms(), "action": "redeem", "tokenIds": ids,
                     "batchId": d.get("batchId"), "results": results})


def reconcile_open(cutoff_sec=180):
    """Open rounds whose order never became a position must not linger.

    An UNCONFIRMED placement can still land, so give it a window; after that,
    re-read the order and either keep it or hand the budget back.
    """
    if not S["open"]:
        return
    r = baw("prediction", "order", "history", "--limit", 50)
    if not ok(r):
        return
    by_id = {str(o.get("orderId")): o for o in ((r.get("data") or {}).get("orders") or [])
             if isinstance(o, dict)}
    for key in list(S["open"].keys()):
        pos = S["open"][key]
        if pos.get("fill_status") not in (None, "UNCONFIRMED"):
            continue
        if (now_ms() - pos.get("opened_ms", 0)) / 1000.0 < cutoff_sec:
            continue
        o = by_id.get(str(pos.get("orderId")))
        st = str((o or {}).get("status", "")).upper()
        if st in ("FAILED", "CANCELED", "CANCELLED", "EXPIRED", "REJECTED"):
            release(key, fnum(pos.get("stake_usd"), 0.0) or 0.0, f"reconcile: {st}")
        elif st in ("FILLED", "SUCCESS", "COMPLETED", "DONE"):
            pos["fill_status"] = st
            pos["filled_shares"] = fnum((o or {}).get("filledShareQty"), 0.0)
            save()
        elif not o:
            release(key, fnum(pos.get("stake_usd"), 0.0) or 0.0,
                    "reconcile: order not present in history")


def settle_sweep():
    """Close out rounds we hold once the market resolves, and write the outcome
    row that makes calibration possible."""
    if not S["open"]:
        return
    r = baw("prediction", "position", "settled-history", "--limit", 50)
    if not ok(r):
        return
    data = r.get("data") or {}
    rows = data.get("positions") or data.get("list") or data.get("records") or []
    by_token = {}
    for row in rows:
        if isinstance(row, dict):
            by_token[str(pick(row, "tokenId", "outcomeTokenId"))] = row

    for key in list(S["open"].keys()):
        pos = S["open"][key]
        row = by_token.get(str(pos.get("tokenId")))
        if not row:
            continue
        result = str(pick(row, "result", "status", "outcome", default="")).lower()
        won = bool(row.get("isWinner")) or "win" in result
        # `pnl` comes back null on settled rounds; the realised figure lives in
        # realizedPnl. Reading the wrong one books every win as zero and quietly
        # destroys the calibration ledger, which is the whole point of this file.
        pnl = fnum(row.get("realizedPnl"))
        claim = fnum(row.get("claimAmount"))
        cost = fnum(row.get("totalCost"))
        if pnl is None and claim is not None and cost is not None:
            pnl = claim - cost
        pnl = pnl if pnl is not None else 0.0
        pos.update(settled_ms=now_ms(), result=result, won=won, pnl=pnl)
        # Symmetric with add_deployed(): the stake is no longer at risk once the
        # round has resolved. Without this, `deployed` only ever grows and the
        # budget gate becomes a turnover cap instead of a risk cap.
        with BUDGET_LK:
            S["deployed"] = max(0.0, (fnum(S.get("deployed"), 0.0) or 0.0)
                                - (fnum(pos.get("stake_usd"), 0.0) or 0.0))
        book_pnl(pnl)
        S["done"][key] = pos
        del S["open"][key]
        S["consecutive_losses"] = 0 if won else S.get("consecutive_losses", 0) + 1
        jsonl(OUTCOMES_J, {
            "ts": now_ms(), "key": key, "title": pos.get("title"),
            "side": pos.get("side"), "prob": pos.get("prob"), "ask": pos.get("ask"),
            "edge": pos.get("edge"), "overround": pos.get("overround"),
            "streak": pos.get("streak"), "streak_dir": pos.get("streak_dir"),
            "stake_usd": pos.get("stake_usd"), "result": result, "won": won, "pnl": pnl,
            "shares": fnum(row.get("shares")), "total_cost": cost,
            "claim_amount": claim, "fill_price": pos.get("fill_price"),
        })
        log(f"SETTLED {key} {pos.get('side')} -> {result} pnl={pnl}")
        if S["consecutive_losses"] >= CFG["max_consecutive_losses"]:
            S["halt_reason"] = (f"{S['consecutive_losses']} consecutive losses "
                                f">= max_consecutive_losses")
            log(f"HALT {S['halt_reason']}")
    save()


# ──────────────────────────── one round ─────────────────────────

def record(rnd, decision, reason, extra=None):
    heartbeat(decision)
    row = {"ts": now_ms(), "key": rnd["key"], "title": rnd["title"],
           "close_ms": rnd["close_ms"], "feed": rnd.get("feed"),
           "feed_symbol": rnd.get("feed_symbol"), "fee_bps": rnd.get("fee_bps"),
           "decision": decision, "reason": reason}
    row.update(extra or {})
    jsonl(ROUNDS_J, row)


def handle(rnd):
    key = rnd["key"]
    if key in S["open"] or key in S["done"]:
        return
    p = CFG["policy"]

    streak, sdir = streak_state()
    q, err = read_book(rnd)
    if err:
        record(rnd, "SKIP_SCREEN", err, {"streak": streak, "streak_dir": sdir})
        return

    ctx = {"cfg": CFG, "policy": p, "streak": streak, "streak_dir": sdir,
           "now_ms": now_ms(), "open": S["open"]}
    prob = estimate_probability(rnd, ctx)

    # Any run that is not spending money records the quote alongside the state.
    # Collecting is free here, and making it exclusive to one mode would force a
    # second pass over the same rounds just to answer "is it already priced in".
    if not LIVE:
        jsonl(QUOTES_J, {"ts": now_ms(), "key": key, "title": rnd["title"],
                         "symbol": CFG["symbol"], "timeframe": CFG["timeframe"],
                         "feed": rnd.get("feed"), "feed_symbol": rnd.get("feed_symbol"),
                         "start_ms": rnd.get("start_ms"), "close_ms": rnd["close_ms"],
                         "start_price": rnd.get("start_price"),
                         "fee_bps": rnd.get("fee_bps"),
                         "streak": streak, "streak_dir": sdir, "prob_hook": prob, **q})

    # collect-quotes additionally stops here: no guards, no sizing, no orders.
    if CFG["mode"] == "collect-quotes":
        record(rnd, "COLLECT", "quote recorded, no order", {"prob": prob, **q})
        return

    why = gate(rnd, q)
    if why:
        record(rnd, "SKIP_SCREEN", why, {"prob": prob, "streak": streak,
                                         "streak_dir": sdir, **q})
        return

    if prob is None:
        record(rnd, "SKIP_HOOK", "hook returned None",
               {"streak": streak, "streak_dir": sdir, **q})
        return
    prob, bad = valid_prob(prob)
    if bad:
        # Loud on purpose: this is a defect in the strategy, and a skipped round
        # is a far better outcome than an order sized by a broken number.
        log(f"ALERT {bad} — round skipped. Fix estimate_probability().")
        record(rnd, "BAD_HOOK", bad, {"streak": streak, "streak_dir": sdir, **q})
        return

    side, edge, ask = decide(prob, q, rnd)
    breakeven = (ask + cost_fraction(rnd)) if ask else None
    if side is None:
        record(rnd, "NO_EDGE", f"best edge {edge:.4f} <= threshold {p['edge_threshold']}",
               {"prob": prob, "streak": streak, "streak_dir": sdir, **q})
        return

    # Guards, all enforced here.
    roll_day()
    if S.get("halt_reason"):
        record(rnd, "HALTED", S["halt_reason"], {"prob": prob, **q}); return
    if os.path.exists(STOP_F):
        record(rnd, "STOPPED", "STOP file present", {"prob": prob, **q}); return
    if len(S["open"]) >= CFG["max_open_rounds"]:
        record(rnd, "GUARD", "max_open_rounds", {"prob": prob, **q}); return
    if S["rounds_today"] >= CFG["max_rounds_per_day"]:
        record(rnd, "GUARD", "max_rounds_per_day", {"prob": prob, **q}); return

    stake = min(fnum(size_position(rnd, ctx, edge), 0.0) or 0.0, fnum(CFG["stake_usd"]))
    stake = min(stake, worst_case_room())

    # ── M1: depth. The screen was done against the top of the book, so an order
    # larger than what rests there walks into worse prices and the figure the
    # decision was made on stops being the figure that fills. Cap the stake at
    # the USDT available at the best ask rather than trusting slippage tolerance
    # to absorb it.
    ask_size = fnum(q.get("up_ask_size" if side == "up" else "dn_ask_size"), 0.0) or 0.0
    top_usdt = (ask or 0.0) * ask_size
    if top_usdt > 0 and stake > top_usdt:
        record(rnd, "GUARD", f"stake ${stake:.2f} exceeds ${top_usdt:.2f} resting at the "
                             f"best ask — would walk the book",
               {"prob": prob, "top_of_book_usdt": round(top_usdt, 2), **q})
        return
    if stake < MIN_ORDER_USD:
        # Covers both an exhausted budget and a stake_usd set below the floor:
        # either way the order would be rejected, so do not spend a round on it.
        room = worst_case_room()
        why = (f"worst-case room ${room:.2f} left against budget_usd "
               f"(realised loss + capital at risk)" if room < MIN_ORDER_USD
               else f"stake ${stake:.2f} below the platform minimum ${MIN_ORDER_USD:.2f}")
        record(rnd, "GUARD", why, {"prob": prob, **q})
        return

    common = {"prob": prob, "ask": ask, "edge": edge, "breakeven": breakeven,
              "stake_usd": round(stake, 2), "streak": streak, "streak_dir": sdir, **q}

    if not LIVE:
        record(rnd, "DRY_RUN", f"would buy {side}", common)
        log(f"DRY_RUN {rnd['title'][:46]} {side} p={prob:.3f} ask={ask:.3f} "
            f"edge={edge:+.3f} breakeven={breakeven:.3f} ${stake:.2f}")
        return

    res, err = place(rnd, side, stake)
    if err:
        record(rnd, "ORDER_FAILED", err, common)
        log(f"ORDER FAILED {rnd['title'][:46]}: {err}")
        return

    order_id = pick(res["order"], "orderId", "id")
    add_deployed(stake)
    S["rounds_today"] += 1
    pos = {"key": key, "title": rnd["title"], "side": side,
           "tokenId": rnd[side]["tokenId"], "orderId": order_id,
           "opened_ms": now_ms(), "close_ms": rnd["close_ms"], **common}
    S["open"][key] = pos
    save()
    jsonl(ORDERS_J, {"ts": now_ms(), "action": "buy", **pos})
    # The decision log must contain the rounds that were actually traded, not
    # only the ones that were skipped — otherwise outcomes.jsonl has nothing to
    # join against and the calibration question becomes unanswerable.
    record(rnd, "ORDER", f"bought {side}", {**common, "orderId": order_id})
    log(f"ORDER {rnd['title'][:46]} {side} ${stake:.2f} ask={ask:.3f} "
        f"edge={edge:+.3f} order={order_id}")

    row, st = confirm_fill(order_id)
    pos["fill_status"] = st
    if row:
        pos["filled_usdt"] = fnum(row.get("filledUsdtAmount"), 0.0)
        pos["filled_shares"] = fnum(row.get("filledShareQty"), 0.0)
        pos["fill_price"] = fnum(row.get("price"))
        pos["fee_paid"] = fnum(row.get("marketProviderFee"))
        pos["error"] = row.get("errorMessage")
    save()

    if st in ("FAILED", "CANCELED", "CANCELLED", "EXPIRED", "REJECTED"):
        jsonl(ORDERS_J, {"ts": now_ms(), "action": "order_failed", "key": key,
                         "orderId": order_id, "status": st,
                         "error": (row or {}).get("errorMessage")})
        release(key, stake, f"order {st}: {(row or {}).get('errorMessage')}")
        return
    if st == "UNCONFIRMED":
        # Left in place deliberately: it may still land. reconcile_open() checks
        # it on the next sweep rather than guessing now.
        log(f"  fill status UNCONFIRMED — will reconcile on the next sweep")
        return
    # The buy row was written at submit time, so it carries no fill data. Append
    # the confirmation as its own row rather than mutating history — the audit
    # trail should show what was known when.
    jsonl(ORDERS_J, {"ts": now_ms(), "action": "order_filled", "key": key,
                     "orderId": order_id, "status": st,
                     "filled_usdt": pos.get("filled_usdt"),
                     "filled_shares": pos.get("filled_shares"),
                     "fill_price": pos.get("fill_price"),
                     "fee_paid": pos.get("fee_paid")})
    # Report the number that actually matters for the cost model: what you paid
    # per share versus the ask you screened on. This is the input for
    # expected_slippage_bps — measure it, do not guess it.
    shares = fnum(pos.get("filled_shares"), 0.0) or 0.0
    spent = fnum(pos.get("filled_usdt"), 0.0) or 0.0
    if shares > 0 and spent > 0 and ask:
        eff = spent / shares
        allin = (eff / ask - 1.0) * 10000.0
        pos["allin_bps_vs_ask"] = round(allin, 1)
        save()
        log(f"  FILLED {shares} shares @ {pos.get('fill_price')} | "
            f"ALL-IN {eff:.4f} vs ask {ask:.4f} = {allin:+.0f} bps "
            f"(fee {rnd['fee_bps']:.0f} bps + slippage)")
    else:
        log(f"  FILLED {pos.get('filled_shares')} shares @ {pos.get('fill_price')} "
            f"fee={pos.get('fee_paid')}")


# ──────────────────────────── main loop ─────────────────────────

def preflight():
    v_ok, v_msg = cli_version_ok()
    if not v_ok:
        sys.exit(f"refusing to start — {v_msg}. Below the floor the CLI behaves "
                 f"differently and this scaffold assumes the current semantics.")
    if LIVE:
        okc, why = live_confirmed()
        if not okc:
            sys.exit(f"live mode refused — {why}\n"
                     f"write the current budget into {LIVE_ACK_F} to acknowledge "
                     f"what is at risk:\n  echo {CFG['budget_usd']} > {LIVE_ACK_F}")

    # Probe the prediction endpoint itself, not `wallet status`. The wallet can
    # answer while the prediction session is dead, and a daemon that starts in
    # that state skips every round while looking exactly like a quiet market.
    probe = baw("prediction", "position", "list", "--limit", 1)
    if not session_alive(probe):
        sys.exit("prediction session is not authenticated. Sign in first — a daemon "
                 "started without one skips every round, and that is indistinguishable "
                 "from a market with no opportunities.")
    # Validate symbol/timeframe against what is actually listed. These are exact
    # strings with a space in them ("5 min"), and a typo does not raise — it
    # simply matches no topic, so the daemon would run forever looking busy
    # while enumerating nothing. That is the worst failure mode available here,
    # so it is checked against the live catalogue rather than a hardcoded list.
    cat = baw("prediction", "market", "list",
              "--l1Category", CFG["l1_category"], "--l2Category", CFG["l2_category"],
              "--limit", 50)
    if ok(cat):
        topics = (cat.get("data") or {}).get("marketTopics") or []
        combos = sorted({(t.get("symbol"), t.get("timeframe")) for t in topics
                         if isinstance(t, dict)})
        if (CFG["symbol"], CFG["timeframe"]) not in combos:
            lines = "\n  ".join(f"{sym!r:12} {tf!r}" for sym, tf in combos)
            sys.exit(f"no listed topic matches symbol={CFG['symbol']!r} "
                     f"timeframe={CFG['timeframe']!r}.\nCurrently listed:\n  {lines}")
        feeds = {(t.get("variantData") or {}).get("priceFeedProvider")
                 for t in topics
                 if t.get("symbol") == CFG["symbol"] and t.get("timeframe") == CFG["timeframe"]}
        feedstr = ', '.join(sorted(f for f in feeds if f)) or 'unknown'
        log(f"settlement feed for {CFG['symbol']} {CFG['timeframe']}: {feedstr}")

        # The bundled hook reads hourly Binance spot candles. State that plainly
        # whenever the configured round settles on something else or at another
        # granularity — a strategy validated on one series and run against
        # another is not validated at all, and nothing downstream would notice.
        iv = kline_interval()
        log(f"streak candles: {CFG['symbol']} {iv} "
            f"({'from config' if CFG.get('kline_interval') else 'derived from timeframe'})")
        if CFG["timeframe"] != "1 hour":
            log(f"NOTE  the bundled hook reads hourly Binance spot candles, but "
                f"{CFG['timeframe']!r} rounds settle on {feedstr}"
                + (" at a different granularity" if "BINANCE" in feeds else
                   " — a different feed entirely")
                + ". Its measured hit rates do not transfer to this cadence; "
                  "re-validate against the feed this round settles on, or treat "
                  "the run as a plumbing test only.")

    log(f"mode={CFG['mode']} chain={CFG['chain']} symbol={CFG['symbol']} "
        f"timeframe={CFG['timeframe']!r} budget=${CFG['budget_usd']} "
        f"stake=${CFG['stake_usd']} policy={json.dumps(CFG['policy'], sort_keys=True)}")


def settle_thread():
    while True:
        try:
            reconcile_open()
            settle_sweep()
            redeem_sweep()
        except Exception as e:
            log(f"WARN settle thread: {e}")
        time.sleep(CFG.get("settle_poll_sec", 120))


# Seeded at import so the first summary lands after a real interval. Starting at
# zero makes the very first call fire immediately, with an empty tally, and
# report "nothing matched" before anything has had a chance to match — a false
# alarm that sends the reader off to debug a config that is fine.
_hb = {"ts": time.time(), "counts": {}, "seen": 0}


def heartbeat(decision=None, every=600):
    """Summarise decisions on a timer.

    'No trades' is the expected state for most configurations, but silence is
    indistinguishable from a daemon that has quietly stopped working. A periodic
    tally makes an idle run verifiable rather than merely quiet.
    """
    if decision:
        _hb["counts"][decision] = _hb["counts"].get(decision, 0) + 1
    if time.time() - _hb["ts"] < every:
        return
    _hb["ts"] = time.time()
    if _hb["counts"]:
        tally = " ".join(f"{k}={v}" for k, v in sorted(_hb["counts"].items()))
        log(f"HEARTBEAT {tally} | open={len(S['open'])} "
            f"at_risk=${fnum(S.get('deployed'), 0):.2f} "
            f"realized=${fnum(S.get('realized_pnl'), 0):+.2f} "
            f"room=${worst_case_room():.2f} rounds_today={S.get('rounds_today')}")
    elif _hb["seen"]:
        # Rounds were enumerated but every one was already known (open or done),
        # so no new decision was recorded. Working as intended, not idle.
        log(f"HEARTBEAT {_hb['seen']} round(s) seen, all already handled | "
            f"open={len(S['open'])}")
    else:
        log(f"HEARTBEAT no round matched symbol={CFG.get('symbol')} "
            f"timeframe={CFG.get('timeframe')!r} in the last {every}s — "
            f"check those two if it persists")
    _hb["counts"] = {}
    _hb["seen"] = 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--collect-quotes", action="store_true",
                    help="record state -> quotes -> result and never trade")
    a = ap.parse_args()

    load_state()
    load_config()
    if a.collect_quotes:
        CFG["mode"] = "collect-quotes"
        globals()["LIVE"] = False
    lock = acquire_lock()                      # noqa: F841 — held for process life
    preflight()

    if CFG["mode"] != "collect-quotes":
        threading.Thread(target=settle_thread, daemon=True).start()

    # Everything inside the loop is wrapped. handle() already guards a single
    # round, but the loop scaffolding — enumeration, parsing, state save — was
    # not, and an exception there kills the process silently. A long-running
    # trader that dies quietly is worse than one that is loudly wrong.
    fails = 0
    while True:
        try:
            if os.path.exists(KILL_F):
                log("KILL file present — exiting. On-chain positions are untouched.")
                return
            rounds, err = list_rounds()
            if err == "session":
                log("ALERT session expired — not a quiet market. Re-authenticate; "
                    "rounds are being skipped and recorded as such.")
            elif err:
                log(f"WARN market list: {err}")
            else:
                heartbeat()
                for m in rounds or []:
                    r = parse_round(m)
                    if not r:
                        continue
                    _hb["seen"] += 1
                    try:
                        handle(r)
                    except Exception as e:
                        log(f"WARN round {r.get('key')}: {e}")
                save()
            fails = 0
        except KeyboardInterrupt:
            log("interrupted — exiting. On-chain positions are untouched.")
            return
        except Exception as e:
            # Back off rather than spin: a persistent fault should not hammer
            # the API, and the escalating interval shows up in the log.
            fails += 1
            delay = min(300, 15 * fails)
            log(f"ERROR main loop ({fails} in a row): {type(e).__name__}: {e} — "
                f"retrying in {delay}s")
            time.sleep(delay)
            continue
        # Coerced: a non-numeric poll_sec in config would otherwise raise here,
        # outside the guard above, and take the process down.
        time.sleep(max(5.0, fnum(CFG.get("poll_sec"), 60.0) or 60.0))

if __name__ == "__main__":
    main()
