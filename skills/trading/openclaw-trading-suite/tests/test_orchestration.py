import sqlite3

from openclaw_trading_suite.adapters import AdapterRegistry
from openclaw_trading_suite.adapters.mock import MockExecutionAdapter
from openclaw_trading_suite.autonomy import AutonomyLevel, DecisionInput
from openclaw_trading_suite.db import SQLiteStore
from openclaw_trading_suite.orchestration import ExecutionRequest, evaluate_and_execute


def test_orchestration_executes_and_persists_order(tmp_path) -> None:
    db_path = tmp_path / "suite.sqlite3"
    store = SQLiteStore(db_path)
    store.init_schema()

    registry = AdapterRegistry()
    registry.register(MockExecutionAdapter())

    req = ExecutionRequest(
        autonomy_input=DecisionInput(
            autonomy_level=AutonomyLevel.BALANCED,
            strategy_id="s1",
            hypothesis_id="h1",
            estimated_risk_pct=0.01,
            strategy_risk_limit_pct=0.02,
            portfolio_drawdown_pct=0.01,
            max_portfolio_drawdown_pct=0.10,
        ),
        strategy_id="s1",
        hypothesis_id="h1",
        symbol="BTCUSD",
        side="buy",
        qty=1.0,
    )
    result = evaluate_and_execute(req, registry, store)
    assert result["executed"] is True

    with sqlite3.connect(db_path) as conn:
        orders = conn.execute("SELECT COUNT(1) FROM orders").fetchone()[0]
        fills = conn.execute("SELECT COUNT(1) FROM fills").fetchone()[0]
        risk_decisions = conn.execute("SELECT COUNT(1) FROM risk_decisions").fetchone()[0]
    assert orders == 1
    assert fills == 1
    assert risk_decisions == 1

