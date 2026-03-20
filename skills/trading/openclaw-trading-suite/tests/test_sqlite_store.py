import sqlite3
import pytest

from openclaw_trading_suite.db import SQLiteStore


def test_sqlite_store_initializes_schema(tmp_path) -> None:
    db_path = tmp_path / "suite.sqlite3"
    store = SQLiteStore(db_path)
    store.init_schema()

    with sqlite3.connect(db_path) as conn:
        names = {
            row[0]
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        }

    assert "strategies" in names
    assert "overnight_reports" in names


def test_sqlite_store_writes_strategy_and_hypothesis(tmp_path) -> None:
    db_path = tmp_path / "suite.sqlite3"
    store = SQLiteStore(db_path)
    store.init_schema()
    store.upsert_strategy(
        strategy_id="s1",
        name="Swing Baseline",
        profile_type="swing",
        version="v1",
        params={"rsi": 14},
        active=True,
        created_at="2026-02-27T00:00:00Z",
    )
    store.insert_hypothesis(
        hypothesis_id="h1",
        strategy_id="s1",
        symbol_or_contract="BTCUSD",
        thesis_text="Momentum continuation",
        entry_plan={"entry": 100},
        exit_plan={"target": 110},
        invalidation={"stop": 95},
        confidence=0.63,
        created_at="2026-02-27T00:00:00Z",
    )

    with sqlite3.connect(db_path) as conn:
        strategy_count = conn.execute("SELECT COUNT(1) FROM strategies").fetchone()[0]
        hyp_count = conn.execute("SELECT COUNT(1) FROM hypotheses").fetchone()[0]

    assert strategy_count == 1
    assert hyp_count == 1


def test_sqlite_store_insert_does_not_replace_existing_rows(tmp_path) -> None:
    db_path = tmp_path / "suite.sqlite3"
    store = SQLiteStore(db_path)
    store.init_schema()
    store.insert_order(
        order_id="o1",
        hypothesis_id="h1",
        venue="mock-execution",
        symbol="BTCUSD",
        side="buy",
        order_type="market",
        qty=1.0,
        limit_price=None,
        status="filled",
        created_at="2026-02-27T00:00:00Z",
    )
    with pytest.raises(sqlite3.IntegrityError):
        store.insert_order(
            order_id="o1",
            hypothesis_id="h1",
            venue="mock-execution",
            symbol="BTCUSD",
            side="sell",
            order_type="market",
            qty=1.0,
            limit_price=None,
            status="filled",
            created_at="2026-02-27T00:01:00Z",
        )
