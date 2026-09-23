#!/usr/bin/env python3
"""fere.py — portable multi-wallet CLI for the FereAI API (api.fereai.xyz).

One Ed25519 keypair == one Fere agent == one wallet pair (1 EVM + 1 Solana address).
This CLI keeps a *keyring* of them, so a single machine can drive one wallet or ten
thousand (one per end user) with the same commands.

    fere.py new alice                  # register a wallet, save it to the keyring
    fere.py ls                         # every wallet you own
    fere.py holdings alice             # balances across every chain + venue
    fere.py quote alice --chain base --in USDC --out 0x<token> --usd 10
    fere.py buy   alice --chain base --in USDC --out 0x<token> --usd 10 \
                        --tp 1.0:0.5 --sl 0.3:1.0 --i-understand-this-moves-real-money

Credentials, in priority order:
  1. --agent <name>            a keyring entry ($FERE_HOME/agents.json, 0600)
  2. $FERE_AGENT_SEED_B64 (+ $FERE_AGENT_ID)   single-agent servers / CI
  3. $FERE_TOKEN               a pre-minted agt_* bearer (read-only-ish; cannot re-mint)

Secrets are NEVER printed. `key <name>` needs an explicit --reveal, and even then
prints to stderr with a warning. Tokens are shown as prefix+length.

Deps: httpx, and either `cryptography` (preferred) or `pynacl`. Proxies are honoured
via httpx trust_env (HTTPS_PROXY / SSL_CERT_FILE).
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import stat
import sys
import time
import uuid
from decimal import Decimal
from pathlib import Path

import httpx

BASE = os.environ.get("FERE_BASE_URL", "https://api.fereai.xyz").rstrip("/")
HOME = Path(os.environ.get("FERE_HOME", Path.home() / ".fere"))
KEYRING = HOME / "agents.json"
KEY_PREFIX = os.environ.get("FERE_KEY_PREFIX", "fere_")

# ── chain table — the ONE place a chain id, sentinel or stable lives ──────────
# EVM native sentinel: 0x + exactly 40 hex 'e'. A 41-char or one-short variant is
# accepted by dryrun and fails live. assert_sentinel() is called at import.
EVM_NATIVE = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
SOL_NATIVE = "So11111111111111111111111111111111111111112"

# Every quote asset below is checked against a primary source, because a wrong stable
# address is a wrong trade: the four USDCs against Circle's own contract-address page,
# Base + Solana USDC also seen in live holdings rows, RH USDG from our own live trades.
# BNB deliberately has NO symbol shortcut — we have not verified a stable there, and an
# unverified constant in this table would route money to it. Pass the address instead.
CHAINS = {
    "ethereum": {"id": 1,       "native": EVM_NATIVE, "dec": 18,
                 "stable": {"USDC": ("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", 6)}},
    "base":     {"id": 8453,    "native": EVM_NATIVE, "dec": 18,
                 "stable": {"USDC": ("0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", 6)}},
    "arbitrum": {"id": 42161,   "native": EVM_NATIVE, "dec": 18,
                 "stable": {"USDC": ("0xaf88d065e77c8cC2239327C5EDb3A432268e5831", 6)}},
    "polygon":  {"id": 137,     "native": EVM_NATIVE, "dec": 18,
                 "stable": {"USDC": ("0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359", 6)}},
    "bnb":      {"id": 56,      "native": EVM_NATIVE, "dec": 18, "stable": {}},
    "robinhood":{"id": 4663,    "native": EVM_NATIVE, "dec": 18,
                 "stable": {"USDG": ("0x5fc5360D0400a0Fd4f2af552ADD042D716F1d168", 6)}},
    "solana":   {"id": 7565164, "native": SOL_NATIVE, "dec": 9,
                 "stable": {"USDC": ("EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v", 6)}},
}
ALIAS = {"eth": "ethereum", "sol": "solana", "rh": "robinhood", "robinhood-chain": "robinhood",
         "bsc": "bnb", "arb": "arbitrum", "matic": "polygon"}
MIN_NOTIONAL_USD = Decimal("5")


def assert_sentinel() -> None:
    """Fail at import, not at a live order, if the sentinel was ever shortened."""
    s = EVM_NATIVE
    assert s.startswith("0x") and len(s) == 42, f"EVM sentinel must be 42 chars, got {len(s)}"
    assert all(c in "eE" for c in s[2:]), "EVM sentinel body must be 40x e/E"
    assert s == "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE", "EVM sentinel byte mismatch"
    assert len(SOL_NATIVE) == 43 and SOL_NATIVE.startswith("So111"), "Solana sentinel mismatch"


assert_sentinel()


def chain(name_or_id) -> dict:
    k = str(name_or_id).lower()
    k = ALIAS.get(k, k)
    if k in CHAINS:
        return {"name": k, **CHAINS[k]}
    for name, c in CHAINS.items():
        if str(c["id"]) == k:
            return {"name": name, **c}
    sys.exit(f"unknown chain {name_or_id!r}; known: {', '.join(CHAINS)} (+ ids)")


def resolve_token(c: dict, token: str) -> tuple[str, int, bool]:
    """'USDC' | 'native' | a raw address -> (wire address, decimals, is_dollar_stable).
    Never lowercases: Solana mints are base58 and case-sensitive."""
    t = token.strip()
    if t.lower() == "native":
        return c["native"], c["dec"], False
    up = t.upper()
    if up in c["stable"]:
        return (*c["stable"][up], True)
    return t, -1, False  # unknown decimals; the caller must pass smallest units


# ── crypto: prefer `cryptography`, fall back to pynacl ────────────────────────
try:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

    def _sk_from_seed(seed: bytes):
        return Ed25519PrivateKey.from_private_bytes(seed)

    def _pub(sk) -> bytes:
        from cryptography.hazmat.primitives import serialization
        return sk.public_key().public_bytes(
            encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)

    def _sign(sk, msg: bytes) -> bytes:
        return sk.sign(msg)
except ImportError:  # pragma: no cover
    try:
        from nacl.signing import SigningKey
    except ImportError:
        sys.exit("need `cryptography` (preferred) or `pynacl`: pip install cryptography httpx")

    def _sk_from_seed(seed: bytes):
        return SigningKey(seed)

    def _pub(sk) -> bytes:
        return bytes(sk.verify_key)

    def _sign(sk, msg: bytes) -> bytes:
        return sk.sign(msg).signature


# ── base58check, for the portable one-string key ─────────────────────────────
_B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def b58encode(b: bytes) -> str:
    n = int.from_bytes(b, "big")
    out = ""
    while n:
        n, r = divmod(n, 58)
        out = _B58[r] + out
    return "1" * (len(b) - len(b.lstrip(b"\x00"))) + out


def b58decode(s: str) -> bytes:
    n = 0
    for ch in s:
        if ch not in _B58:
            raise ValueError(f"bad base58 char {ch!r}")
        n = n * 58 + _B58.index(ch)
    body = n.to_bytes((n.bit_length() + 7) // 8, "big")
    return b"\x00" * (len(s) - len(s.lstrip("1"))) + body


def b58check_encode(payload: bytes) -> str:
    chk = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    return b58encode(payload + chk)


def b58check_decode(s: str) -> bytes:
    raw = b58decode(s)
    payload, chk = raw[:-4], raw[-4:]
    if hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4] != chk:
        raise ValueError("checksum mismatch — key string is corrupt")
    return payload


def encode_key(seed: bytes, agent_id: str | None) -> str:
    """version 0x01 = seed+agent_id, 0x00 = seed only (recoverable by re-register)."""
    if agent_id:
        return KEY_PREFIX + b58check_encode(b"\x01" + seed + agent_id.encode())
    return KEY_PREFIX + b58check_encode(b"\x00" + seed)


def decode_key(s: str) -> tuple[bytes, str | None]:
    s = s.strip()
    if s.startswith(KEY_PREFIX):
        s = s[len(KEY_PREFIX):]
    elif "_" in s:                      # tolerate a foreign prefix (trench_, myapp_)
        s = s.split("_", 1)[1]
    payload = b58check_decode(s)
    ver, seed, rest = payload[0], payload[1:33], payload[33:]
    if ver not in (0, 1) or len(seed) != 32:
        raise ValueError("unsupported key version")
    return seed, (rest.decode() if ver == 1 and rest else None)


# ── keyring ──────────────────────────────────────────────────────────────────
def _read_keyring() -> dict:
    if not KEYRING.exists():
        return {"agents": {}, "default": None}
    return json.loads(KEYRING.read_text())


def _write_keyring(data: dict) -> None:
    HOME.mkdir(parents=True, exist_ok=True)
    os.chmod(HOME, stat.S_IRWXU)
    tmp = KEYRING.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=1))
    os.chmod(tmp, stat.S_IRUSR | stat.S_IWUSR)
    tmp.replace(KEYRING)
    os.chmod(KEYRING, stat.S_IRUSR | stat.S_IWUSR)


class Agent:
    def __init__(self, name, seed_b64, agent_id=None, wallets=None, token=None):
        self.name = name
        self.seed = base64.b64decode(seed_b64)
        self.sk = _sk_from_seed(self.seed)
        self.agent_id = agent_id
        self.wallets = wallets or {}
        self._token = token
        self._token_exp = float("inf") if token else 0.0

    @property
    def seed_b64(self) -> str:
        return base64.b64encode(self.seed).decode()

    @property
    def pub_b64(self) -> str:
        return base64.b64encode(_pub(self.sk)).decode()

    def sign_b64(self, msg: str) -> str:
        return base64.b64encode(_sign(self.sk, msg.encode())).decode()

    def save(self) -> None:
        kr = _read_keyring()
        kr.setdefault("agents", {})[self.name] = {
            "seed_b64": self.seed_b64, "public_key_b64": self.pub_b64,
            "agent_id": self.agent_id, "base_url": BASE, "wallets": self.wallets,
            "created_at": kr.get("agents", {}).get(self.name, {}).get("created_at", int(time.time())),
        }
        kr["default"] = kr.get("default") or self.name
        _write_keyring(kr)

    @classmethod
    def load(cls, name: str | None):
        kr = _read_keyring()
        if name is None:
            name = kr.get("default")
        if name and name in kr.get("agents", {}):
            a = kr["agents"][name]
            return cls(name, a["seed_b64"], a.get("agent_id"), a.get("wallets"))
        if os.environ.get("FERE_AGENT_SEED_B64"):
            return cls(name or "env", os.environ["FERE_AGENT_SEED_B64"],
                       os.environ.get("FERE_AGENT_ID"))
        if os.environ.get("FERE_TOKEN"):
            return cls(name or "token", base64.b64encode(b"\x00" * 32).decode(),
                       None, None, os.environ["FERE_TOKEN"])
        sys.exit(f"no wallet {name or '(default)'} — run `fere.py new <name>` "
                 f"or set FERE_AGENT_SEED_B64 / FERE_TOKEN")


# ── HTTP ─────────────────────────────────────────────────────────────────────
class Api:
    # The server blocks up to 90 s on ?wait=true, so a client timeout under that
    # guarantees a read timeout on every write. 130 s leaves headroom.
    def __init__(self, agent: Agent | None = None, timeout=130.0):
        self.agent = agent
        self.c = httpx.Client(timeout=timeout, trust_env=True)

    def raw(self, method: str, path: str, **kw) -> httpx.Response:
        """Retry rules exist because retrying a write is how you spend twice.

        A ConnectError means the request never reached Fere, so re-sending is safe.
        A ReadTimeout means it DID reach Fere and the answer was lost — re-sending is
        a second order. On 2026-09-12 an earlier version of this method re-sent a swap
        twice on read timeouts and Fere filled all three: **there is no server-side
        dedupe on `idempotency_key`.** So: retry GET (reads are free to repeat), never
        retry anything else. A write that times out is UNKNOWN — read holdings.
        """
        url = path if path.startswith("http") else f"{BASE}/{path.lstrip('/')}"
        idempotent = method.upper() in ("GET", "HEAD", "OPTIONS")
        for attempt in range(3):
            try:
                return self.c.request(method, url, **kw)
            except httpx.ConnectError as e:
                # the agent proxy mints leaf certs with notBefore=now; first call can lose the race
                if "not yet valid" in str(e) and attempt < 2:
                    time.sleep(1.5 * (attempt + 1))
                    continue
                raise
            except httpx.ReadTimeout:
                if idempotent and attempt < 2:
                    time.sleep(2 * (attempt + 1))
                    continue
                raise RuntimeError(
                    f"{method} {path} timed out after the request was already sent. "
                    f"This is UNKNOWN, not failed — the action may have executed. "
                    f"Read holdings (and /v1/notifications) before doing anything else; "
                    f"do NOT re-send, an idempotency_key does not dedupe server-side."
                ) from None
        raise RuntimeError("unreachable")  # pragma: no cover

    def bearer(self) -> str:
        a = self.agent
        if a._token and time.time() < a._token_exp - 300:
            return a._token
        if not a.agent_id:
            sys.exit("no agent_id for this wallet — `fere.py recover <name>` or re-register")
        ts = str(int(time.time()))
        r = self.raw("POST", "/v1/auth/token",
                     json={"agent_id": a.agent_id, "timestamp": ts, "signature": a.sign_b64(ts)})
        if r.status_code != 200:
            j = body(r)
            if j.get("code") == "stale_timestamp" or "stale" in str(j):
                sys.exit("Fere rejected the timestamp — this machine's clock is off; sync NTP")
            sys.exit(f"token mint failed {r.status_code}: {json.dumps(redact(j))[:300]}")
        j = r.json()
        a._token, a._token_exp = j["token"], time.time() + j.get("expires_in", 3600)
        return a._token

    def get(self, path, **kw):
        return body(self.raw("GET", path, headers=self._h(), **kw))

    def post(self, path, payload=None, **kw):
        return body(self.raw("POST", path, headers=self._h(), json=payload, **kw))

    def delete(self, path, payload=None, **kw):
        return body(self.raw("DELETE", path, headers=self._h(), json=payload, **kw))

    def _h(self) -> dict:
        return {"Authorization": f"Bearer {self.bearer()}", "Content-Type": "application/json"}

    def close(self):
        self.c.close()


def body(r: httpx.Response):
    try:
        j = r.json()
    except Exception:
        j = {"_text": r.text[:500]}
    if isinstance(j, dict):
        j.setdefault("_status", r.status_code)
    return j


SECRET_KEYS = {"token", "secret_key", "seed_b64", "seed", "signature", "authorization",
               "private_key", "secret", "public_key"}


def redact(o):
    if isinstance(o, dict):
        return {k: (f"<redacted len={len(v)}>" if k.lower() in SECRET_KEYS and isinstance(v, str)
                    else redact(v)) for k, v in o.items()}
    if isinstance(o, list):
        return [redact(x) for x in o]
    if isinstance(o, str) and o.startswith("agt_"):
        return f"<redacted agt_… len={len(o)}>"
    return o


def out(obj, as_json: bool):
    print(json.dumps(redact(obj), indent=1, default=str) if as_json else obj)


# ── holdings: the only source of truth for a fill ────────────────────────────
def hkey(row: dict) -> tuple:
    """(chain_id, address) — EVM lowercased, Solana/venue symbols kept case-exact."""
    addr = str(row.get("base_address") or "native")
    cid = int(row.get("chain_id") or 0)
    if addr.startswith("0x"):
        addr = addr.lower()
    return (cid, addr)


def hunits(row: dict) -> Decimal:
    """tokens_bought is a decimal string that may be in sci notation ('2.065E-15').
    amount_in_wei_or_lamports is None on Hyperliquid/venue rows — never int() it blind."""
    for f in ("tokens_bought",):
        v = row.get(f)
        if v not in (None, ""):
            try:
                return Decimal(str(v))
            except Exception:
                pass
    return Decimal(0)


# A plain GET /v1/holdings can be served from Fere's saved answer: an EMPTY
# wallet's answer is kept for up to 45 min and never re-checked, so a deposit
# that lands just after one empty read stays invisible (Fere RCA, 2026-09-23 —
# $100 USDC on Base missing for ~40 min while perp/fund, which reads the chain,
# worked first try). `event=wallet-refresh` drops the saved answer and re-reads
# the wallet, same as the app's Refresh button. Every read this CLI makes is
# either a person asking or a fill being confirmed, so every read refreshes.
# An unknown `event` value is silently ignored (200, cached) — spell it exactly.
HOLDINGS_REFRESH = {"event": "wallet-refresh"}


def holdings_map(api: Api, refresh: bool = True) -> dict:
    """3 tries with backoff — a single upstream 502 blanks the whole response, and a
    stale baseline turns a late fill into a double buy. `refresh` (default on)
    bypasses Fere's saved answer — see HOLDINGS_REFRESH."""
    last = None
    for i, wait in enumerate((0, 2, 4)):
        if wait:
            time.sleep(wait)
        j = api.get("/v1/holdings", params=HOLDINGS_REFRESH if refresh else None)
        rows = j.get("holdings") if isinstance(j, dict) else None
        if isinstance(rows, list):
            return {hkey(r): r for r in rows}
        last = j
    sys.exit(f"holdings unreadable after 3 tries: {json.dumps(redact(last))[:300]}")


def wait_task(api: Api, task_id: str, timeout=240) -> dict:
    """Statuses come back UPPERCASE from /v1/tasks and lowercase from /v1/swap. Compare
    case-insensitively; `message` is a constant and means nothing.

    Two things make the timeout matter. Some tasks are slow — an HL setup took >90 s to
    reach its real verdict — so a short cap turns a real error into a fake "TIMEOUT".
    And an id that was NEVER ISSUED answers 200 PENDING forever, so a loop with no
    deadline never exits. TIMEOUT here means *unknown*, never failed: keep the id and
    re-poll it, and never retry the underlying action on the strength of it."""
    deadline = time.time() + timeout
    j = {}
    while time.time() < deadline:
        j = api.get(f"/v1/tasks/{task_id}")
        st = str(j.get("status", "")).upper()
        if st in ("SUCCESS", "FAILURE", "REVOKED"):
            return j
        time.sleep(2)
    return {**j, "status": "TIMEOUT"}


# ── tx lock: one on-chain action in flight per wallet, ≥3 s gap ──────────────
class TxLock:
    def __init__(self, name: str, wait=180, gap=3.0):
        self.p = HOME / "locks" / f"{name}.lock"
        self.wait, self.gap = wait, gap

    def __enter__(self):
        self.p.parent.mkdir(parents=True, exist_ok=True)
        deadline = time.time() + self.wait
        while True:
            try:
                fd = os.open(self.p, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
                os.write(fd, str(os.getpid()).encode())
                os.close(fd)
                return self
            except FileExistsError:
                age = time.time() - self.p.stat().st_mtime if self.p.exists() else 1e9
                if age > 300:                       # stale lock from a killed run
                    self.p.unlink(missing_ok=True)
                    continue
                if time.time() > deadline:
                    sys.exit("another trade is in flight for this wallet (queued too long)")
                print("[queued] another trade in flight for this wallet…", file=sys.stderr)
                time.sleep(2)

    def __exit__(self, *exc):
        time.sleep(self.gap)                        # Fere's dev: parallel sends -> nonce errors
        self.p.unlink(missing_ok=True)


# ── commands ─────────────────────────────────────────────────────────────────
def cmd_new(a):
    kr = _read_keyring()
    names = [a.name] if not a.count else [f"{a.name}-{i+1}" for i in range(a.count)]
    made = []
    for name in names:
        if name in kr.get("agents", {}) and not a.force:
            print(f"[skip] {name} already exists (use --force to re-register a NEW wallet)")
            continue
        seed = os.urandom(32)
        ag = Agent(name, base64.b64encode(seed).decode())
        api = Api(ag)
        r = api.raw("POST", "/v1/auth/register",
                    json={"agent_name": name, "public_key": ag.pub_b64})
        j = body(r)
        if r.status_code == 409 or j.get("code") == "duplicate_key":
            sys.exit(f"public key already registered: {j.get('message')}")
        if r.status_code != 200:
            sys.exit(f"register failed {r.status_code}: {json.dumps(redact(j))[:300]}")
        v = body(api.raw("POST", "/v1/auth/verify", json={
            "registration_id": j["registration_id"], "challenge": j["challenge"],
            "signature": ag.sign_b64(j["challenge"])}))
        ag.agent_id = v.get("agent_id")
        if not ag.agent_id:
            sys.exit(f"verify failed: {json.dumps(redact(v))[:300]}")
        # wallets provision in <1 s in practice; docs say poll up to 60 s
        for _ in range(30):
            w = api.get("/v1/wallets")
            if not w.get("provisioning") and w.get("wallets"):
                ag.wallets = {x["chain_type"]: x["address"] for x in w["wallets"]}
                break
            time.sleep(2)
        ag.save()
        api.close()
        made.append({"name": name, "agent_id": ag.agent_id, **ag.wallets})
        print(f"[new] {name}  evm={ag.wallets.get('evm')}  solana={ag.wallets.get('solana')}")
    if a.json:
        out({"created": made, "keyring": str(KEYRING)}, True)
    elif made:
        print(f"\nkeyring: {KEYRING} (0600). Back it up — the key IS the login.\n"
              f"Fund the addresses above; there is no programmatic withdrawal to an "
              f"external address, so treat deposits as committed capital.")


def cmd_ls(a):
    kr = _read_keyring()
    rows = []
    for name, x in sorted(kr.get("agents", {}).items()):
        rows.append({"name": name, "agent_id": x.get("agent_id"),
                     "evm": (x.get("wallets") or {}).get("evm"),
                     "solana": (x.get("wallets") or {}).get("solana"),
                     "default": name == kr.get("default")})
    if a.json:
        return out({"agents": rows, "keyring": str(KEYRING)}, True)
    if not rows:
        return print(f"no wallets yet — `fere.py new <name>` (keyring {KEYRING})")
    w = max(len(r["name"]) for r in rows)
    for r in rows:
        print(f"{'*' if r['default'] else ' '} {r['name']:<{w}}  {r['evm'] or '—'}  "
              f"{r['solana'] or '—'}")


def cmd_rm(a):
    kr = _read_keyring()
    if a.name not in kr.get("agents", {}):
        sys.exit(f"no such wallet {a.name}")
    if not a.yes:
        sys.exit(f"refusing to delete {a.name} without --yes. THE KEY IS THE ONLY LOGIN: "
                 f"run `fere.py key {a.name} --reveal` and save the string first, or the "
                 f"funds in that wallet are gone.")
    kr["agents"].pop(a.name)
    if kr.get("default") == a.name:
        kr["default"] = next(iter(kr["agents"]), None)
    _write_keyring(kr)
    print(f"[rm] {a.name} removed from the keyring (the Fere agent still exists)")


def cmd_key(a):
    ag = Agent.load(a.name)
    s = encode_key(ag.seed, ag.agent_id)
    if not a.reveal:
        return print(f"{ag.name}: portable key is {len(s)} chars. Re-run with --reveal to print "
                     f"it (secret — it is the whole login, treat it like a seed phrase).")
    print("!! SECRET — anyone with this string controls the wallet. Do not paste it into a "
          "chat, a commit, or a log.", file=sys.stderr)
    print(s)


def cmd_import(a):
    key = a.key or os.environ.get("FERE_IMPORT_KEY") or sys.stdin.read()
    try:
        seed, agent_id = decode_key(key)
    except ValueError as e:
        sys.exit(f"that key is not usable: {e}. Nothing was imported — check for a "
                 f"truncated paste or a changed character; the checksum exists so a "
                 f"typo fails here instead of silently opening an empty wallet.")
    ag = Agent(a.name, base64.b64encode(seed).decode(), agent_id)
    api = Api(ag)
    if not agent_id:
        ag.agent_id = _recover_agent_id(api, ag)
    w = api.get("/v1/wallets")
    ag.wallets = {x["chain_type"]: x["address"] for x in w.get("wallets", [])}
    ag.save()
    api.close()
    print(f"[import] {a.name}  evm={ag.wallets.get('evm')}  solana={ag.wallets.get('solana')}")


def _recover_agent_id(api: Api, ag: Agent) -> str:
    """Re-register the SAME public key: Fere answers 409 duplicate_key naming the agent.
    Parsing that message is a fallback — store the agent_id alongside the seed instead."""
    r = api.raw("POST", "/v1/auth/register",
                json={"agent_name": f"recover-{uuid.uuid4().hex[:8]}", "public_key": ag.pub_b64})
    j = body(r)
    if r.status_code == 200 and j.get("registration_id"):
        sys.exit("that key was never registered — this is a fresh seed, not a recovery")
    # 409 body is nested: {"detail":{"error":{"code":"duplicate_key","message":
    # "Public key already registered as agent_<16>"}}} — scan the whole envelope
    m = re.search(r"agent_[A-Za-z0-9_-]{8,}", json.dumps(j))
    if m:
        return m.group(0)
    sys.exit(f"could not recover agent_id: {json.dumps(redact(j))[:300]}")


def cmd_recover(a):
    ag = Agent.load(a.name)
    api = Api(ag)
    ag.agent_id = _recover_agent_id(api, ag)
    w = api.get("/v1/wallets")
    ag.wallets = {x["chain_type"]: x["address"] for x in w.get("wallets", [])}
    ag.save()
    api.close()
    print(f"[recover] {ag.name} -> {ag.agent_id}  evm={ag.wallets.get('evm')}")


def cmd_wallets(a):
    api = Api(Agent.load(a.name))
    out(api.get("/v1/wallets"), True)


def cmd_credits(a):
    api = Api(Agent.load(a.name))
    out(api.get("/v1/credits"), True)


def cmd_chains(a):
    r = httpx.get(f"{BASE}/v1/chains", trust_env=True, timeout=20)
    out(r.json(), True)


def cmd_holdings(a):
    api = Api(Agent.load(a.name))
    rows = list(holdings_map(api).values())
    if a.chain:
        cid = chain(a.chain)["id"]
        rows = [r for r in rows if int(r.get("chain_id") or 0) == cid]
    if a.raw:
        return out({"holdings": rows}, True)
    rows.sort(key=lambda r: -(r.get("value_usd") or 0))
    total = sum(r.get("value_usd") or 0 for r in rows)
    shown = [r for r in rows if (r.get("value_usd") or 0) >= a.min_usd]
    if a.json:
        return out({"total_usd": total, "rows": [{
            "chain": r.get("chain"), "token_name": r.get("token_name"),
            "address": r.get("base_address"), "units": str(hunits(r)),
            "value_usd": r.get("value_usd"), "verified": r.get("verified"),
            "protocol": r.get("protocol"),
            "exits": [o.get("bucketSortKey") for o in (r.get("outstanding_orders") or [])],
        } for r in shown]}, True)
    print(f"{'CHAIN':<11} {'TOKEN':<22} {'UNITS':>22} {'USD':>10}  EXITS")
    for r in shown:
        exits = ",".join(o.get("bucketSortKey", "?") for o in (r.get("outstanding_orders") or []))
        flag = "" if r.get("verified") else " (unverified)"
        print(f"{str(r.get('chain')):<11} {str(r.get('token_name'))[:22]:<22} "
              f"{str(hunits(r))[:22]:>22} {r.get('value_usd') or 0:>10.2f}  {exits}{flag}")
    hid = len(rows) - len(shown)
    print(f"{'':<11} {'TOTAL':<22} {'':>22} {total:>10.2f}"
          + (f"   ({hid} rows under ${a.min_usd} hidden)" if hid else ""))


def cmd_security(a):
    api = Api(Agent.load(a.name))
    c = chain(a.chain)
    j = api.post("/v1/security/check",
                 {"tokens": [{"chain_id": c["id"], "token_address": a.token}]})
    res = (j.get("results") or [{}])[0]
    status = res.get("status")
    # RH and other uncovered chains return allowed:true with status unsupported_chain —
    # gate on status, never on `allowed` alone.
    verdict = "PASS" if status == "passed" else f"NOT-CHECKED ({status})" if status in (
        "unsupported_chain", "api_unavailable", "skipped") else f"BLOCK ({status})"
    if a.json:
        return out(j, True)
    print(f"{verdict}  provider={res.get('provider')}  reason={res.get('reason')}")


def _amount_units(a, dec_in: int, stable_in: bool) -> str:
    """--usd is only meaningful when the input token is a dollar stable. For ETH, SOL or
    any other token, "$10" is not 10 units — demand explicit smallest units instead.

    The $5 min-notional floor is enforced on the --usd path only: with an explicit
    --amount we have no price and cannot tell $4 from $400, so that path is the
    caller's responsibility."""
    if a.amount:
        return str(a.amount)
    if a.usd is None:
        sys.exit("pass --usd (only with a stable --in) or --amount (smallest units)")
    if not stable_in:
        sys.exit(f"--usd needs a dollar stable as --in (got {a.token_in!r}). For a native "
                 f"coin or any other token pass --amount in smallest units — otherwise "
                 f"'--usd 10' would mean 10 TOKENS, not $10.")
    if Decimal(str(a.usd)) < MIN_NOTIONAL_USD:
        sys.exit(f"min notional is ${MIN_NOTIONAL_USD} — below it routes fail and dust is unsellable")
    return str(int(Decimal(str(a.usd)) * (10 ** dec_in)))


def _hooks(spec: str | None) -> dict | None:
    if not spec:
        return None
    try:
        pct, sell = spec.split(":")
        return {"price_percentage": float(pct), "sell_percentage": float(sell)}
    except ValueError:
        sys.exit("hook format is PCT:SELLFRAC, e.g. --tp 1.0:0.5 (+100%, sell half)")


def _swap_body(a) -> dict:
    cin = chain(a.chain)
    cout = chain(a.chain_out or a.chain)
    tin, dec_in, stable_in = resolve_token(cin, a.token_in)
    tout, _, _ = resolve_token(cout, a.token_out)
    b = {"chain_id_in": cin["id"], "chain_id_out": cout["id"], "token_in": tin,
         "token_out": tout, "amount": _amount_units(a, dec_in, stable_in),
         "slippage_bps": a.slippage}
    if _hooks(a.tp):
        b["take_profit"] = _hooks(a.tp)
    if _hooks(a.sl):
        b["stop_loss"] = _hooks(a.sl)
    if a.cancel_conditional:
        b["cancel_conditional_orders"] = True
    return b


def cmd_quote(a):
    api = Api(Agent.load(a.name))
    b = {**_swap_body(a), "dryrun": True}
    j = api.post("/v1/swap?wait=true&timeout=90", b)
    tid = j.get("task_id")
    t = wait_task(api, tid) if tid else {}
    out({"request": b, "response": j, "task": t}, True)
    print("\nNOTE: a dryrun validates balance + shape, NOT the route. It passes for addresses "
          "that fail live (the zero address is the classic one). It is not proof of a fill.",
          file=sys.stderr)


def cmd_trade(a):
    """buy / sell / swap — all one path, all confirmed by holdings diff."""
    if not a.i_understand_this_moves_real_money:
        sys.exit("this moves REAL money. Re-run with --i-understand-this-moves-real-money "
                 "(or use `quote` for a dryrun).")
    ag = Agent.load(a.name)
    api = Api(ag)
    b = _swap_body(a)
    idem = a.idempotency_key or str(uuid.uuid4())
    b["idempotency_key"] = idem
    kin = (chain(a.chain)["id"], b["token_in"].lower() if b["token_in"].startswith("0x") else b["token_in"])
    kout = (chain(a.chain_out or a.chain)["id"],
            b["token_out"].lower() if b["token_out"].startswith("0x") else b["token_out"])

    with TxLock(ag.name):
        before = holdings_map(api)
        j = api.post("/v1/swap?wait=true&timeout=90", b)
        tid = j.get("task_id")
        task = wait_task(api, tid) if tid else {}
        status = str(task.get("status") or j.get("status") or "?").upper()
        err = str((task.get("result") or {}).get("error") or "")
        definitive_fail = "balance validation failed" in err.lower() or j.get("_status", 200) >= 400

        # a "failure" can still fill late: re-read holdings 3x over ~15 s before believing it
        filled, d_in, d_out = False, Decimal(0), Decimal(0)
        for i in range(3):
            if i:
                time.sleep(5)
            after = holdings_map(api)
            d_in = hunits(before.get(kin, {})) - hunits(after.get(kin, {}))
            d_out = hunits(after.get(kout, {})) - hunits(before.get(kout, {}))
            if d_out > 0 or d_in > 0:
                filled = True
                break
            if definitive_fail:
                break

    tx = (task.get("result") or {}).get("tx_hash")
    verdict = ("FILLED" if filled else
               "FAILED" if definitive_fail else
               "UNCONFIRMED — do NOT retry; re-check holdings before placing anything else")
    out({"verdict": verdict, "task_status": status, "tx_hash": tx, "idempotency_key": idem,
         "delta_in": str(d_in), "delta_out": str(d_out), "error": err or None,
         "note": "holdings delta is the fill; task status and `message` are hints only"}, True)
    sys.exit(0 if filled else 1)


def cmd_hooks(a):
    api = Api(Agent.load(a.name))
    c = chain(a.chain)
    b = {"chain_id": c["id"], "token_address": a.token}
    if _hooks(a.tp):
        b["take_profit"] = _hooks(a.tp)
    if _hooks(a.sl):
        b["stop_loss"] = _hooks(a.sl)
    j = api.post("/v1/hooks", b)
    out(j, True)
    print("\nNOTE: hooks re-base on Fere's price AT REGISTRATION, not your entry, and they "
          "have been observed to vanish. Reconcile holdings[].outstanding_orders every poll.",
          file=sys.stderr)


def cmd_orders(a):
    api = Api(Agent.load(a.name))
    if a.cancel:
        return out(api.delete(f"/v1/limit-orders/{a.cancel}"), True)
    if a.create:
        c_in, c_out = chain(a.chain), chain(a.chain_out or a.chain)
        tin, dec_in, stable_in = resolve_token(c_in, a.token_in)
        tout, _, _ = resolve_token(c_out, a.token_out)
        b = {"chain_id_in": c_in["id"], "chain_id_out": c_out["id"], "token_in": tin,
             "token_out": tout, "amount": _amount_units(a, dec_in, stable_in),
             "price_usd_trigger": a.price, "condition": a.condition,
             "trigger_token_address": a.trigger_token or tout,
             "trigger_token_chain": str(c_out["id"]), "slippage_bps": a.slippage}
        return out(api.post("/v1/limit-orders?wait=true&timeout=90", b), True)
    q = f"?status={a.status}" if a.status else ""
    out(api.get(f"/v1/limit-orders{q}"), True)


def cmd_outstanding(a):
    api = Api(Agent.load(a.name))
    if a.delete:
        return out(api.delete("/wallet/outstanding-orders",
                              {"outstanding_order_ids": a.delete}), True)
    out(api.get("/wallet/outstanding-orders"), True)


def _money_gate(a, what: str):
    if not a.i_understand_this_moves_real_money:
        sys.exit(f"{what} moves REAL money. Re-run with --i-understand-this-moves-real-money.")


def _run_task(api: Api, j: dict, label: str, as_json=True):
    """Every venue write is an async task. Poll it, then say plainly what happened —
    and remind the caller that the venue's own state, not this status, is the truth."""
    tid = j.get("task_id")
    task = wait_task(api, tid) if tid else {}
    status = str(task.get("status") or j.get("status") or "?").upper()
    out({"op": label, "queued": j, "task": task, "status": status,
         "note": "confirm against the venue's own state (orders/positions/holdings), "
                 "not this status"}, as_json)
    return status


def cmd_perp(a):
    """Hyperliquid perps — the account is per agent, so every wallet has its own."""
    api = Api(Agent.load(a.name))
    op = a.op
    if op == "status":
        # min_fund_usd is the gate: HL perps need ~$50 to activate, not $5
        return out(api.get("/v1/perp/setup"), True)
    if op == "orders":
        return out(api.get("/v1/perp/orders"), True)
    if op == "markets":
        j = api.get("/v1/perp/markets")     # the API ignores any search arg; filter here
        rows = j.get("tokens") or j.get("markets") or []
        if a.search:
            rows = [r for r in rows if a.search.upper() in str(r.get("symbol", "")).upper()]
        return out({"count": len(rows), "markets": [
            {"symbol": r.get("symbol"), "address": r.get("address"),
             "price_usd": r.get("priceUSD"), "sz_decimals": r.get("decimals"),
             "max_leverage": r.get("name"), "detail": r.get("description")}
            for r in rows[:a.limit]]}, True)
    if op == "setup":
        return _run_task(api, api.post("/v1/perp/setup", {}), "perp.setup")
    with TxLock(Agent.load(a.name).name):
        if op == "fund":
            _money_gate(a, "funding the perp account")
            c = chain(a.chain)
            tok, dec, stable = resolve_token(c, a.token or "native")
            body_ = {"amount": a.amount or _amount_units(a, dec, stable),
                     "source_chain_id": c["id"]}
            if (a.token or "").lower() != "native":
                body_["source_token"] = tok
            if a.usd:
                body_["display_amount_usd"] = a.usd
            return _run_task(api, api.post("/v1/perp/fund", body_), "perp.fund")
        if op == "open":
            _money_gate(a, "opening a perp")
            body_ = {"asset": a.asset, "is_buy": a.side == "buy", "size": a.size,
                     "leverage": a.leverage, "is_cross": not a.isolated,
                     "order_type": a.type, "slippage_pct": a.slippage_pct,
                     "reduce_only": a.reduce_only}
            for k, v in (("limit_price", a.limit_price), ("tp_price", a.tp_price),
                         ("sl_price", a.sl_price)):
                if v is not None:
                    body_[k] = v
            return _run_task(api, api.post("/v1/perp/open", body_), "perp.open")
        if op == "close":
            _money_gate(a, "closing a perp")
            body_ = {"asset": a.asset, "slippage_pct": a.slippage_pct}
            if a.size is not None:
                body_["size"] = a.size
            return _run_task(api, api.post("/v1/perp/close", body_), "perp.close")
        if op == "cancel":
            return _run_task(api, api.post("/v1/perp/orders/cancel",
                                           {"asset": a.asset, "order_id": a.order_id}),
                             "perp.cancel")
        if op == "withdraw":
            _money_gate(a, "withdrawing perp collateral")
            body_ = {"amount_usd": a.usd, "destination_chain_id": chain(a.chain)["id"]}
            if a.token and a.token.lower() != "native":
                body_["destination_token"] = resolve_token(chain(a.chain), a.token)[0]
            return _run_task(api, api.post("/v1/perp/withdraw", body_), "perp.withdraw")
    sys.exit(f"unknown perp op {op}")


def cmd_hl(a):
    """Hyperliquid SPOT — USDC-quoted, same per-agent account as the perps."""
    api = Api(Agent.load(a.name))
    if a.op == "orders":
        return out(api.get("/v1/spot_hl/orders"), True)
    if a.op == "markets":
        j = api.get("/v1/spot_hl/markets")
        rows = j.get("markets") or j.get("tokens") or []
        if a.search:
            rows = [r for r in rows if a.search.upper() in str(r.get("symbol", "")).upper()]
        return out({"count": len(rows), "markets": [
            {"symbol": r.get("symbol"), "address": r.get("address"),
             "price_usd": r.get("priceUSD"), "sz_decimals": r.get("decimals")}
            for r in rows[:a.limit]]}, True)
    with TxLock(Agent.load(a.name).name):
        if a.op in ("buy", "sell"):
            _money_gate(a, f"an HL spot {a.op}")
            body_ = {"asset": a.asset, "order_type": a.type, "slippage_pct": a.slippage_pct}
            if a.size is not None:
                body_["size"] = a.size
            elif a.op == "buy":
                sys.exit("--size is required to buy (it is the base-token amount, not USD)")
            for k, v in (("limit_price", a.limit_price), ("tp_price", a.tp_price),
                         ("sl_price", a.sl_price)):
                if v is not None and (a.op == "buy" or k == "limit_price"):
                    body_[k] = v
            return _run_task(api, api.post(f"/v1/spot_hl/{a.op}", body_), f"hl.{a.op}")
        if a.op == "tpsl":
            body_ = {"asset": a.asset}
            for k, v in (("tp_price", a.tp_price), ("sl_price", a.sl_price), ("size", a.size)):
                if v is not None:
                    body_[k] = v
            if "tp_price" not in body_ and "sl_price" not in body_:
                sys.exit("pass at least one of --tp-price / --sl-price")
            return _run_task(api, api.post("/v1/spot_hl/tp-sl", body_), "hl.tpsl")
        if a.op == "cancel":
            return _run_task(api, api.post("/v1/spot_hl/orders/cancel",
                                           {"asset": a.asset, "order_id": a.order_id}), "hl.cancel")
    sys.exit(f"unknown hl op {a.op}")


# Polymarket lives on the webapp-tagged routes, NOT under /v1 — but they accept an
# agent bearer and the state is per agent (verified 2026-09-09). openapi carries no
# request bodies for the write ops, so those take an explicit --body JSON: the MCP tool
# schema is the best available spec and the gateway may rename fields.
POLY_READ = {"status": "/polymarket/setup/status", "orders": "/polymarket/orders/open",
             "activity": "/polymarket/activity", "meta": "/polymarket/meta"}
POLY_WRITE = {"setup": "/polymarket/setup", "migrate": "/polymarket/setup/v2",
              "fund": "/polymarket/fund-safe", "order": "/polymarket/order",
              "cancel": "/polymarket/order/cancel", "redeem": "/polymarket/redeem",
              "withdraw": "/polymarket/withdraw",
              "ack": "/polymarket/disclaimer/acknowledge"}


def cmd_poly(a):
    api = Api(Agent.load(a.name))
    if a.op in POLY_READ:
        return out(api.get(POLY_READ[a.op]), True)
    if a.op in POLY_WRITE:
        if a.op in ("fund", "order", "withdraw", "redeem"):
            _money_gate(a, f"polymarket {a.op}")
        try:
            payload = json.loads(a.body) if a.body else {}
        except json.JSONDecodeError as e:
            sys.exit(f"--body must be JSON: {e}")
        j = api.post(POLY_WRITE[a.op], payload)
        if j.get("task_id"):
            return _run_task(api, j, f"poly.{a.op}")
        return out(j, True)
    sys.exit(f"unknown poly op {a.op}")


def cmd_task(a):
    api = Api(Agent.load(a.name))
    out(wait_task(api, a.task_id) if a.poll else api.get(f"/v1/tasks/{a.task_id}"), True)


def cmd_notifications(a):
    ag = Agent.load(a.name)
    api = Api(ag)
    if not a.stream:
        return out(api.get("/v1/notifications"), True)
    # EventSource cannot set headers — SSE has to be a plain streaming GET
    deadline = time.time() + a.stream
    with api.c.stream("GET", f"{BASE}/v1/notifications/stream",
                      headers={"Authorization": f"Bearer {api.bearer()}",
                               "Accept": "text/event-stream"}, timeout=None) as r:
        for line in r.iter_lines():
            if line and not line.startswith(":"):
                print(line, flush=True)
            if time.time() > deadline:
                break


def main():
    p = argparse.ArgumentParser(prog="fere.py", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--json", action="store_true", help="machine-readable output")
    # --json accepted on either side of the subcommand; SUPPRESS keeps the sub-parser
    # from clobbering a top-level --json with its own default
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--json", action="store_true", default=argparse.SUPPRESS,
                        help="machine-readable output")
    sub = p.add_subparsers(dest="cmd", required=True, parser_class=lambda **kw:
                           argparse.ArgumentParser(parents=[common], **kw))

    def agent_arg(sp, optional=True):
        sp.add_argument("name", nargs="?" if optional else None,
                        help="keyring wallet name (default: the keyring default)")

    s = sub.add_parser("new", help="register one or many new wallets")
    s.add_argument("name")
    s.add_argument("--count", type=int, help="make N wallets named <name>-1..N (multi-tenant)")
    s.add_argument("--force", action="store_true", help="overwrite a keyring entry (NEW wallet)")
    s.set_defaults(fn=cmd_new)

    s = sub.add_parser("ls", help="list wallets in the keyring"); s.set_defaults(fn=cmd_ls)
    s = sub.add_parser("rm", help="forget a wallet (needs --yes)")
    s.add_argument("name"); s.add_argument("--yes", action="store_true"); s.set_defaults(fn=cmd_rm)

    s = sub.add_parser("key", help="show the portable one-string key (secret)")
    agent_arg(s); s.add_argument("--reveal", action="store_true"); s.set_defaults(fn=cmd_key)

    s = sub.add_parser("import", help="restore a wallet from a portable key string")
    s.add_argument("name"); s.add_argument("--key", help="omit to read stdin / $FERE_IMPORT_KEY")
    s.set_defaults(fn=cmd_import)

    s = sub.add_parser("recover", help="re-derive agent_id by re-registering the same pubkey")
    agent_arg(s); s.set_defaults(fn=cmd_recover)

    for name, fn, helptxt in (("wallets", cmd_wallets, "addresses"),
                              ("credits", cmd_credits, "credit balance"),
                              ("chains", cmd_chains, "GET /v1/chains (no auth)")):
        s = sub.add_parser(name, help=helptxt)
        agent_arg(s)
        s.set_defaults(fn=fn)

    s = sub.add_parser("holdings", help="balances across every chain and venue")
    agent_arg(s)
    s.add_argument("--chain"); s.add_argument("--raw", action="store_true")
    s.add_argument("--min-usd", type=float, default=0.01)
    s.set_defaults(fn=cmd_holdings)

    s = sub.add_parser("security", help="honeypot / rug check before you buy")
    agent_arg(s); s.add_argument("--chain", required=True); s.add_argument("--token", required=True)
    s.set_defaults(fn=cmd_security)

    def trade_args(sp):
        agent_arg(sp)
        sp.add_argument("--chain", required=True, help="source chain (name or id)")
        sp.add_argument("--chain-out", help="destination chain (omit = same-chain)")
        sp.add_argument("--in", dest="token_in", required=True, help="USDC | native | 0x… | mint")
        sp.add_argument("--out", dest="token_out", required=True)
        sp.add_argument("--usd", type=float, help="notional when --in is a known stable")
        sp.add_argument("--amount", help="exact amount in smallest units (wei/lamports)")
        sp.add_argument("--slippage", type=int, default=300, help="bps (default 300; 500 thin)")
        sp.add_argument("--tp", help="take profit PCT:SELLFRAC, e.g. 1.0:0.5")
        sp.add_argument("--sl", help="stop loss PCT:SELLFRAC, e.g. 0.3:1.0")
        sp.add_argument("--cancel-conditional", action="store_true")
        sp.add_argument("--idempotency-key")

    s = sub.add_parser("quote", help="dryrun a swap (no money moves)")
    trade_args(s); s.set_defaults(fn=cmd_quote)

    for name, helptxt in (("swap", "LIVE swap, confirmed by holdings diff"),
                          ("buy", "alias of swap"), ("sell", "alias of swap")):
        s = sub.add_parser(name, help=helptxt)
        trade_args(s)
        s.add_argument("--i-understand-this-moves-real-money", action="store_true")
        s.set_defaults(fn=cmd_trade)

    s = sub.add_parser("hooks", help="register percentage TP/SL on a token you already hold")
    agent_arg(s); s.add_argument("--chain", required=True); s.add_argument("--token", required=True)
    s.add_argument("--tp"); s.add_argument("--sl"); s.set_defaults(fn=cmd_hooks)

    s = sub.add_parser("orders", help="absolute-USD limit orders (full CRUD)")
    agent_arg(s)
    s.add_argument("--create", action="store_true"); s.add_argument("--cancel", metavar="ID")
    s.add_argument("--status"); s.add_argument("--chain"); s.add_argument("--chain-out")
    s.add_argument("--in", dest="token_in"); s.add_argument("--out", dest="token_out")
    s.add_argument("--usd", type=float); s.add_argument("--amount")
    s.add_argument("--price", type=float, help="USD trigger")
    s.add_argument("--condition", choices=("gte", "lte"), default="gte")
    s.add_argument("--trigger-token"); s.add_argument("--slippage", type=int, default=300)
    s.set_defaults(fn=cmd_orders)

    s = sub.add_parser("outstanding", help="list/cancel hooks (the only hook CRUD there is)")
    agent_arg(s); s.add_argument("--delete", nargs="+", metavar="ID"); s.set_defaults(fn=cmd_outstanding)

    money = "--i-understand-this-moves-real-money"

    s = sub.add_parser("perp", help="Hyperliquid perps — per-agent account")
    s.add_argument("op", choices=("status", "setup", "markets", "orders", "fund", "open",
                                  "close", "cancel", "withdraw"))
    agent_arg(s)
    s.add_argument("--asset", help="perp symbol, e.g. BTC"); s.add_argument("--size", type=float)
    s.add_argument("--side", choices=("buy", "sell"), default="buy", help="buy = long")
    s.add_argument("--leverage", type=int, default=1)
    s.add_argument("--isolated", action="store_true", help="default is cross margin")
    s.add_argument("--type", choices=("market", "limit"), default="market")
    s.add_argument("--limit-price", type=float)
    s.add_argument("--tp-price", type=float, help="ABSOLUTE price (not a percentage)")
    s.add_argument("--sl-price", type=float, help="ABSOLUTE price (not a percentage)")
    s.add_argument("--slippage-pct", type=float, default=0.5)
    s.add_argument("--reduce-only", action="store_true")
    s.add_argument("--order-id", type=int, help="venue oid from `perp orders`")
    s.add_argument("--chain", default="base", help="fund source / withdraw destination")
    s.add_argument("--token", help="source/destination token (default native)")
    s.add_argument("--usd", type=float); s.add_argument("--amount")
    s.add_argument("--search"); s.add_argument("--limit", type=int, default=20)
    s.add_argument(money, action="store_true")
    s.set_defaults(fn=cmd_perp)

    s = sub.add_parser("hl", help="Hyperliquid spot — same per-agent account")
    s.add_argument("op", choices=("markets", "orders", "buy", "sell", "tpsl", "cancel"))
    agent_arg(s)
    s.add_argument("--asset"); s.add_argument("--size", type=float, help="BASE token amount")
    s.add_argument("--type", choices=("market", "limit"), default="market")
    s.add_argument("--limit-price", type=float)
    s.add_argument("--tp-price", type=float); s.add_argument("--sl-price", type=float)
    s.add_argument("--slippage-pct", type=float, default=0.5)
    s.add_argument("--order-id", type=int)
    s.add_argument("--search"); s.add_argument("--limit", type=int, default=20)
    s.add_argument(money, action="store_true")
    s.set_defaults(fn=cmd_hl)

    s = sub.add_parser("poly", help="Polymarket — per-agent safe, webapp-tagged routes")
    s.add_argument("op", choices=("status", "orders", "activity", "meta", "setup", "migrate",
                                  "fund", "order", "cancel", "redeem", "withdraw", "ack"))
    agent_arg(s)
    s.add_argument("--body", help="JSON request body (write ops carry no openapi schema; "
                                  "mirror the fere_polymarket_* MCP tool fields)")
    s.add_argument(money, action="store_true")
    s.set_defaults(fn=cmd_poly)

    s = sub.add_parser("task", help="poll an async task to terminal")
    agent_arg(s); s.add_argument("task_id"); s.add_argument("--poll", action="store_true")
    s.set_defaults(fn=cmd_task)

    s = sub.add_parser("notifications", help="recent events, or hold the SSE stream open")
    agent_arg(s); s.add_argument("--stream", type=int, metavar="SECS"); s.set_defaults(fn=cmd_notifications)

    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
