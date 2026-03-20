from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any


def _json(value: Any) -> str:
    return json.dumps(value, sort_keys=True)


@dataclass
class SQLiteStore:
    db_path: Path

    def __post_init__(self) -> None:
        self.db_path = Path(self.db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA synchronous = NORMAL;")
        return conn

    def init_schema(self) -> None:
        with self.connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS strategies (
                    strategy_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    profile_type TEXT NOT NULL,
                    version TEXT NOT NULL,
                    params_json TEXT NOT NULL,
                    active INTEGER NOT NULL,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS hypotheses (
                    hypothesis_id TEXT PRIMARY KEY,
                    strategy_id TEXT NOT NULL,
                    symbol_or_contract TEXT NOT NULL,
                    thesis_text TEXT NOT NULL,
                    entry_plan_json TEXT NOT NULL,
                    exit_plan_json TEXT NOT NULL,
                    invalidation_json TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS signals (
                    signal_id TEXT PRIMARY KEY,
                    hypothesis_id TEXT NOT NULL,
                    signal_time TEXT NOT NULL,
                    features_json TEXT NOT NULL,
                    signal_side TEXT NOT NULL,
                    signal_strength REAL NOT NULL,
                    regime_tag TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS risk_decisions (
                    risk_decision_id TEXT PRIMARY KEY,
                    hypothesis_id TEXT NOT NULL,
                    risk_profile_json TEXT NOT NULL,
                    position_size REAL NOT NULL,
                    approval_mode TEXT NOT NULL,
                    approved INTEGER NOT NULL,
                    decision_reason TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS orders (
                    order_id TEXT PRIMARY KEY,
                    hypothesis_id TEXT NOT NULL,
                    venue TEXT NOT NULL,
                    symbol TEXT NOT NULL,
                    side TEXT NOT NULL,
                    order_type TEXT NOT NULL,
                    qty REAL NOT NULL,
                    limit_price REAL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS fills (
                    fill_id TEXT PRIMARY KEY,
                    order_id TEXT NOT NULL,
                    fill_time TEXT NOT NULL,
                    fill_price REAL NOT NULL,
                    fill_qty REAL NOT NULL,
                    fee REAL NOT NULL
                );

                CREATE TABLE IF NOT EXISTS positions (
                    position_id TEXT PRIMARY KEY,
                    strategy_id TEXT NOT NULL,
                    symbol TEXT NOT NULL,
                    open_time TEXT NOT NULL,
                    close_time TEXT,
                    realized_pnl REAL NOT NULL,
                    max_adverse_excursion REAL NOT NULL,
                    max_favorable_excursion REAL NOT NULL,
                    close_reason TEXT
                );

                CREATE TABLE IF NOT EXISTS daily_metrics (
                    metric_date TEXT NOT NULL,
                    strategy_id TEXT NOT NULL,
                    trades INTEGER NOT NULL,
                    win_rate REAL NOT NULL,
                    expectancy REAL NOT NULL,
                    sharpe REAL NOT NULL,
                    max_drawdown REAL NOT NULL,
                    net_pnl REAL NOT NULL,
                    PRIMARY KEY (metric_date, strategy_id)
                );

                CREATE TABLE IF NOT EXISTS model_runs (
                    run_id TEXT PRIMARY KEY,
                    strategy_id TEXT NOT NULL,
                    model_type TEXT NOT NULL,
                    feature_set_version TEXT NOT NULL,
                    train_window TEXT NOT NULL,
                    validation_metrics_json TEXT NOT NULL,
                    promoted INTEGER NOT NULL,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS lessons_learned (
                    lesson_id TEXT PRIMARY KEY,
                    strategy_id TEXT NOT NULL,
                    source TEXT NOT NULL,
                    lesson_text TEXT NOT NULL,
                    action_item TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS overnight_reports (
                    report_id TEXT PRIMARY KEY,
                    report_date TEXT NOT NULL,
                    autonomy_level TEXT NOT NULL,
                    summary_md TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS mandates (
                    mandate_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    base_currency TEXT NOT NULL,
                    risk_mode TEXT NOT NULL,
                    target_json TEXT NOT NULL,
                    constraints_json TEXT NOT NULL,
                    intent_align_ref TEXT,
                    created_at TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS mandate_progress (
                    progress_id TEXT PRIMARY KEY,
                    mandate_id TEXT NOT NULL,
                    metric_date TEXT NOT NULL,
                    progress_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                """
            )

    def _insert(self, table: str, payload: dict[str, Any], on_conflict: str = "error") -> None:
        cols = ", ".join(payload.keys())
        placeholders = ", ".join("?" for _ in payload)
        conflict_clause = ""
        if on_conflict == "ignore":
            conflict_clause = "OR IGNORE "
        elif on_conflict == "replace":
            conflict_clause = "OR REPLACE "
        with self.connect() as conn:
            conn.execute(
                f"INSERT {conflict_clause}INTO {table} ({cols}) VALUES ({placeholders})",
                tuple(payload.values()),
            )

    def _upsert(
        self,
        table: str,
        payload: dict[str, Any],
        conflict_cols: tuple[str, ...],
    ) -> None:
        cols = ", ".join(payload.keys())
        placeholders = ", ".join("?" for _ in payload)
        conflict_cols_sql = ", ".join(conflict_cols)
        update_cols = [col for col in payload if col not in conflict_cols]
        update_sql = ", ".join(f"{col}=excluded.{col}" for col in update_cols)
        with self.connect() as conn:
            conn.execute(
                (
                    f"INSERT INTO {table} ({cols}) VALUES ({placeholders}) "
                    f"ON CONFLICT({conflict_cols_sql}) DO UPDATE SET {update_sql}"
                ),
                tuple(payload.values()),
            )

    def upsert_strategy(
        self,
        strategy_id: str,
        name: str,
        profile_type: str,
        version: str,
        params: dict[str, Any],
        active: bool,
        created_at: str,
    ) -> None:
        self._upsert(
            "strategies",
            {
                "strategy_id": strategy_id,
                "name": name,
                "profile_type": profile_type,
                "version": version,
                "params_json": _json(params),
                "active": int(active),
                "created_at": created_at,
            },
            conflict_cols=("strategy_id",),
        )

    def insert_hypothesis(
        self,
        hypothesis_id: str,
        strategy_id: str,
        symbol_or_contract: str,
        thesis_text: str,
        entry_plan: dict[str, Any],
        exit_plan: dict[str, Any],
        invalidation: dict[str, Any],
        confidence: float,
        created_at: str,
    ) -> None:
        self._insert(
            "hypotheses",
            {
                "hypothesis_id": hypothesis_id,
                "strategy_id": strategy_id,
                "symbol_or_contract": symbol_or_contract,
                "thesis_text": thesis_text,
                "entry_plan_json": _json(entry_plan),
                "exit_plan_json": _json(exit_plan),
                "invalidation_json": _json(invalidation),
                "confidence": confidence,
                "created_at": created_at,
            },
        )

    def insert_signal(
        self,
        signal_id: str,
        hypothesis_id: str,
        signal_time: str,
        features: dict[str, Any],
        signal_side: str,
        signal_strength: float,
        regime_tag: str,
    ) -> None:
        self._insert(
            "signals",
            {
                "signal_id": signal_id,
                "hypothesis_id": hypothesis_id,
                "signal_time": signal_time,
                "features_json": _json(features),
                "signal_side": signal_side,
                "signal_strength": signal_strength,
                "regime_tag": regime_tag,
            },
        )

    def insert_risk_decision(
        self,
        risk_decision_id: str,
        hypothesis_id: str,
        risk_profile: dict[str, Any],
        position_size: float,
        approval_mode: str,
        approved: bool,
        decision_reason: str,
        created_at: str,
    ) -> None:
        self._insert(
            "risk_decisions",
            {
                "risk_decision_id": risk_decision_id,
                "hypothesis_id": hypothesis_id,
                "risk_profile_json": _json(risk_profile),
                "position_size": position_size,
                "approval_mode": approval_mode,
                "approved": int(approved),
                "decision_reason": decision_reason,
                "created_at": created_at,
            },
        )

    def insert_order(
        self,
        order_id: str,
        hypothesis_id: str,
        venue: str,
        symbol: str,
        side: str,
        order_type: str,
        qty: float,
        limit_price: float | None,
        status: str,
        created_at: str,
    ) -> None:
        self._insert(
            "orders",
            {
                "order_id": order_id,
                "hypothesis_id": hypothesis_id,
                "venue": venue,
                "symbol": symbol,
                "side": side,
                "order_type": order_type,
                "qty": qty,
                "limit_price": limit_price,
                "status": status,
                "created_at": created_at,
            },
        )

    def insert_fill(
        self,
        fill_id: str,
        order_id: str,
        fill_time: str,
        fill_price: float,
        fill_qty: float,
        fee: float,
    ) -> None:
        self._insert(
            "fills",
            {
                "fill_id": fill_id,
                "order_id": order_id,
                "fill_time": fill_time,
                "fill_price": fill_price,
                "fill_qty": fill_qty,
                "fee": fee,
            },
        )

    def insert_daily_metric(
        self,
        metric_date: str,
        strategy_id: str,
        trades: int,
        win_rate: float,
        expectancy: float,
        sharpe: float,
        max_drawdown: float,
        net_pnl: float,
    ) -> None:
        self._insert(
            "daily_metrics",
            {
                "metric_date": metric_date,
                "strategy_id": strategy_id,
                "trades": trades,
                "win_rate": win_rate,
                "expectancy": expectancy,
                "sharpe": sharpe,
                "max_drawdown": max_drawdown,
                "net_pnl": net_pnl,
            },
            on_conflict="error",
        )

    def insert_model_run(
        self,
        run_id: str,
        strategy_id: str,
        model_type: str,
        feature_set_version: str,
        train_window: str,
        validation_metrics: dict[str, Any],
        promoted: bool,
        created_at: str,
    ) -> None:
        self._insert(
            "model_runs",
            {
                "run_id": run_id,
                "strategy_id": strategy_id,
                "model_type": model_type,
                "feature_set_version": feature_set_version,
                "train_window": train_window,
                "validation_metrics_json": _json(validation_metrics),
                "promoted": int(promoted),
                "created_at": created_at,
            },
        )

    def insert_lesson(
        self,
        lesson_id: str,
        strategy_id: str,
        source: str,
        lesson_text: str,
        action_item: str,
        status: str,
        created_at: str,
    ) -> None:
        self._insert(
            "lessons_learned",
            {
                "lesson_id": lesson_id,
                "strategy_id": strategy_id,
                "source": source,
                "lesson_text": lesson_text,
                "action_item": action_item,
                "status": status,
                "created_at": created_at,
            },
        )

    def insert_overnight_report(
        self,
        report_id: str,
        report_date: str,
        autonomy_level: str,
        summary_md: str,
        created_at: str,
    ) -> None:
        self._insert(
            "overnight_reports",
            {
                "report_id": report_id,
                "report_date": report_date,
                "autonomy_level": autonomy_level,
                "summary_md": summary_md,
                "created_at": created_at,
            },
        )

    def upsert_daily_metric(
        self,
        metric_date: str,
        strategy_id: str,
        trades: int,
        win_rate: float,
        expectancy: float,
        sharpe: float,
        max_drawdown: float,
        net_pnl: float,
    ) -> None:
        self._upsert(
            "daily_metrics",
            {
                "metric_date": metric_date,
                "strategy_id": strategy_id,
                "trades": trades,
                "win_rate": win_rate,
                "expectancy": expectancy,
                "sharpe": sharpe,
                "max_drawdown": max_drawdown,
                "net_pnl": net_pnl,
            },
            conflict_cols=("metric_date", "strategy_id"),
        )

    def upsert_mandate(
        self,
        mandate_id: str,
        name: str,
        base_currency: str,
        risk_mode: str,
        target: dict[str, Any],
        constraints: dict[str, Any],
        intent_align_ref: str | None,
        created_at: str,
    ) -> None:
        self._upsert(
            "mandates",
            {
                "mandate_id": mandate_id,
                "name": name,
                "base_currency": base_currency,
                "risk_mode": risk_mode,
                "target_json": _json(target),
                "constraints_json": _json(constraints),
                "intent_align_ref": intent_align_ref,
                "created_at": created_at,
            },
            conflict_cols=("mandate_id",),
        )

    def insert_mandate_progress(
        self,
        progress_id: str,
        mandate_id: str,
        metric_date: str,
        progress: dict[str, Any],
        created_at: str,
    ) -> None:
        self._insert(
            "mandate_progress",
            {
                "progress_id": progress_id,
                "mandate_id": mandate_id,
                "metric_date": metric_date,
                "progress_json": _json(progress),
                "created_at": created_at,
            },
        )
