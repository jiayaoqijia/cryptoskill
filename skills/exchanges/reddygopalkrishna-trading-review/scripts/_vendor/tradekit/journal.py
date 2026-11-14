"""SQLite trade journal shared by planner, gate, router and analytics skills.

Lifecycle: planned -> open -> closed   (or planned -> cancelled)
"""

from __future__ import annotations

import csv
import datetime as dt
import io
import json
import sqlite3
from pathlib import Path
from typing import Dict, Iterable, List, Optional

from . import config

SCHEMA = """
CREATE TABLE IF NOT EXISTS trades (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol        TEXT NOT NULL,
    side          TEXT NOT NULL CHECK (side IN ('long','short')),
    status        TEXT NOT NULL CHECK (status IN ('planned','open','closed','cancelled')),
    setup         TEXT,
    thesis        TEXT,
    account       TEXT DEFAULT 'paper',
    plan_entry    REAL, plan_stop REAL, plan_target REAL,
    qty           REAL,
    entry_price   REAL, entry_time TEXT,
    stop          REAL,
    exit_price    REAL, exit_time TEXT, exit_reason TEXT,
    fees          REAL DEFAULT 0,
    pnl           REAL, r_multiple REAL, hold_days REAL,
    mae           REAL, mfe REAL,
    grade         TEXT,
    tags          TEXT DEFAULT '[]',
    notes         TEXT DEFAULT '',
    broker_order_id TEXT,
    created_at    TEXT NOT NULL, updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_trades_status ON trades(status);
CREATE INDEX IF NOT EXISTS ix_trades_symbol ON trades(symbol);
"""

FIELDS = ("symbol", "side", "status", "setup", "thesis", "account", "plan_entry", "plan_stop", "plan_target",
          "qty", "entry_price", "entry_time", "stop", "exit_price", "exit_time", "exit_reason", "fees", "pnl",
          "r_multiple", "hold_days", "mae", "mfe", "grade", "tags", "notes", "broker_order_id")


def _now() -> str:
    return dt.datetime.now().isoformat(timespec="seconds")


class Journal:
    def __init__(self, db_path: Optional[Path] = None):
        self.path = Path(db_path) if db_path else config.path("journal.db")
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA)

    def __del__(self):
        try:
            self.conn.close()
        except Exception:  # noqa: BLE001
            pass

    # ------------------------------------------------------------ helpers
    @staticmethod
    def _row(r: sqlite3.Row) -> Dict:
        d = dict(r)
        try:
            d["tags"] = json.loads(d.get("tags") or "[]")
        except json.JSONDecodeError:
            d["tags"] = []
        return d

    def get(self, trade_id: int) -> Dict:
        r = self.conn.execute("SELECT * FROM trades WHERE id=?", (trade_id,)).fetchone()
        if not r:
            raise KeyError(f"trade {trade_id} not found")
        return self._row(r)

    def _insert(self, data: Dict) -> Dict:
        data = {k: v for k, v in data.items() if k in FIELDS}
        if isinstance(data.get("tags"), (list, tuple)):
            data["tags"] = json.dumps(list(data["tags"]))
        now = _now()
        data["created_at"] = data["updated_at"] = now
        cols = ",".join(data)
        q = ",".join("?" for _ in data)
        cur = self.conn.execute(f"INSERT INTO trades ({cols}) VALUES ({q})", list(data.values()))
        self.conn.commit()
        return self.get(cur.lastrowid)

    def update(self, trade_id: int, **changes) -> Dict:
        changes = {k: v for k, v in changes.items() if k in FIELDS}
        if "tags" in changes and isinstance(changes["tags"], (list, tuple)):
            changes["tags"] = json.dumps(list(changes["tags"]))
        if not changes:
            return self.get(trade_id)
        changes["updated_at"] = _now()
        sets = ",".join(f"{k}=?" for k in changes)
        self.conn.execute(f"UPDATE trades SET {sets} WHERE id=?", [*changes.values(), trade_id])
        self.conn.commit()
        return self.get(trade_id)

    # ------------------------------------------------------------ lifecycle
    def plan(self, symbol: str, side: str, entry: float, stop: float, target: Optional[float] = None,
             qty: Optional[float] = None, setup: str = "", thesis: str = "", tags: Iterable[str] = (),
             account: str = "paper") -> Dict:
        side = _side(side)
        return self._insert({"symbol": symbol, "side": side, "status": "planned", "plan_entry": entry,
                             "plan_stop": stop, "plan_target": target, "qty": qty, "stop": stop, "setup": setup,
                             "thesis": thesis, "tags": list(tags), "account": account})

    def open(self, trade_id: Optional[int] = None, *, symbol: Optional[str] = None, side: Optional[str] = None,
             entry_price: float, qty: float, stop: Optional[float] = None, entry_time: Optional[str] = None,
             fees: float = 0.0, setup: str = "", account: str = "paper", broker_order_id: Optional[str] = None,
             tags: Iterable[str] = ()) -> Dict:
        t_entry = entry_time or _now()
        if trade_id:
            t = self.get(trade_id)
            if t["status"] not in ("planned", "open"):
                raise ValueError(f"trade {trade_id} is {t['status']}")
            return self.update(trade_id, status="open", entry_price=entry_price, qty=qty,
                               stop=stop if stop is not None else t["stop"], entry_time=t_entry,
                               fees=(t["fees"] or 0) + fees, broker_order_id=broker_order_id or t["broker_order_id"],
                               account=account or t["account"], setup=t["setup"] or setup)
        if not symbol or not side:
            raise ValueError("symbol and side required to open a trade without a plan")
        return self._insert({"symbol": symbol, "side": _side(side), "status": "open", "entry_price": entry_price,
                             "qty": qty, "stop": stop, "plan_stop": stop, "entry_time": t_entry, "fees": fees,
                             "setup": setup, "account": account, "broker_order_id": broker_order_id,
                             "tags": list(tags)})

    def close(self, trade_id: int, exit_price: float, exit_time: Optional[str] = None, fees: float = 0.0,
              reason: str = "", mae: Optional[float] = None, mfe: Optional[float] = None) -> Dict:
        t = self.get(trade_id)
        if t["status"] != "open":
            raise ValueError(f"trade {trade_id} is {t['status']}, not open")
        qty = float(t["qty"] or 0)
        direction = 1 if t["side"] == "long" else -1
        total_fees = (t["fees"] or 0) + fees
        pnl = (exit_price - t["entry_price"]) * qty * direction - total_fees
        stop = t["plan_stop"] if t["plan_stop"] is not None else t["stop"]
        r = None
        if stop is not None and t["entry_price"] != stop and qty:
            r = pnl / (abs(t["entry_price"] - stop) * qty)
        x_time = exit_time or _now()
        hold = None
        try:
            hold = (dt.datetime.fromisoformat(x_time) - dt.datetime.fromisoformat(t["entry_time"])).total_seconds() / 86400
        except (TypeError, ValueError):
            pass
        return self.update(trade_id, status="closed", exit_price=exit_price, exit_time=x_time,
                           exit_reason=reason, fees=total_fees, pnl=round(pnl, 4),
                           r_multiple=round(r, 4) if r is not None else None,
                           hold_days=round(hold, 3) if hold is not None else None, mae=mae, mfe=mfe)

    def cancel(self, trade_id: int, reason: str = "") -> Dict:
        t = self.get(trade_id)
        if t["status"] != "planned":
            raise ValueError("only planned trades can be cancelled")
        return self.update(trade_id, status="cancelled", exit_reason=reason)

    def note(self, trade_id: int, text: str, grade: Optional[str] = None, tags: Iterable[str] = ()) -> Dict:
        t = self.get(trade_id)
        notes = (t["notes"] + "\n" if t["notes"] else "") + f"[{_now()}] {text}"
        new_tags = sorted(set(t["tags"]) | set(tags))
        return self.update(trade_id, notes=notes, grade=grade or t["grade"], tags=new_tags)

    # ------------------------------------------------------------ queries
    def list(self, status: Optional[str] = None, symbol: Optional[str] = None, since: Optional[str] = None,
             setup: Optional[str] = None, account: Optional[str] = None, limit: int = 1000) -> List[Dict]:
        q = "SELECT * FROM trades WHERE 1=1"
        args: List = []
        if status:
            q += " AND status=?"
            args.append(status)
        if symbol:
            q += " AND symbol=?"
            args.append(symbol)
        if setup:
            q += " AND setup=?"
            args.append(setup)
        if account:
            q += " AND account=?"
            args.append(account)
        if since:
            q += " AND COALESCE(exit_time, entry_time, created_at) >= ?"
            args.append(since)
        q += " ORDER BY COALESCE(exit_time, entry_time, created_at) ASC, id ASC LIMIT ?"
        args.append(limit)
        return [self._row(r) for r in self.conn.execute(q, args).fetchall()]

    def closed_today(self, day: Optional[str] = None) -> List[Dict]:
        day = day or dt.date.today().isoformat()
        return [t for t in self.list(status="closed") if (t["exit_time"] or "").startswith(day)]

    def consecutive_losses(self) -> int:
        n = 0
        for t in reversed(self.list(status="closed")):
            if (t["pnl"] or 0) < 0:
                n += 1
            else:
                break
        return n

    # ------------------------------------------------------------ import / export
    def export_csv(self) -> str:
        rows = self.list()
        buf = io.StringIO()
        cols = ["id", *FIELDS, "created_at", "updated_at"]
        w = csv.DictWriter(buf, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            r = dict(r)
            r["tags"] = ",".join(r["tags"])
            w.writerow(r)
        return buf.getvalue()

    def import_csv(self, text: str, account: str = "imported") -> int:
        """Import closed trades: symbol, side, qty, entry_price, exit_price, entry_time, exit_time[, stop, fees, setup]."""
        n = 0
        for raw in csv.DictReader(io.StringIO(text)):
            r = {k.strip().lower(): (v.strip() if isinstance(v, str) else v) for k, v in raw.items() if k}
            try:
                t = self.open(symbol=r["symbol"], side=r.get("side", "long"), entry_price=float(r["entry_price"]),
                              qty=float(r["qty"]), stop=float(r["stop"]) if r.get("stop") else None,
                              entry_time=r.get("entry_time") or None, fees=float(r.get("fees") or 0) / 2,
                              setup=r.get("setup", ""), account=account)
                if r.get("exit_price"):
                    self.close(t["id"], float(r["exit_price"]), exit_time=r.get("exit_time") or None,
                               fees=float(r.get("fees") or 0) / 2, reason=r.get("exit_reason", ""))
                n += 1
            except (KeyError, ValueError) as e:
                raise ValueError(f"bad row {raw}: {e}") from None
        return n


def _side(side: str) -> str:
    s = str(side).lower()
    if s in ("long", "buy", "b", "l"):
        return "long"
    if s in ("short", "sell", "s"):
        return "short"
    raise ValueError("side must be long or short")
