from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

from openclaw_trading_suite.adapters import (
    AdapterCallError,
    AdapterRegistry,
    AdapterType,
    call_with_healing,
)
from openclaw_trading_suite.autonomy import Decision, DecisionInput, evaluate_decision
from openclaw_trading_suite.db import SQLiteStore


def _utc_now() -> str:
    return datetime.now(UTC).isoformat()


@dataclass(frozen=True)
class ExecutionRequest:
    autonomy_input: DecisionInput
    strategy_id: str
    hypothesis_id: str
    symbol: str
    side: str
    qty: float
    order_type: str = "market"
    limit_price: float | None = None
    venue_adapter_name: str = "mock-execution"
    venue_fallback_names: list[str] | None = None
    risk_profile: dict | None = None


def evaluate_and_execute(
    req: ExecutionRequest,
    adapters: AdapterRegistry,
    store: SQLiteStore,
) -> dict:
    decision_out = evaluate_decision(req.autonomy_input)
    risk_decision_id = str(uuid4())
    store.insert_risk_decision(
        risk_decision_id=risk_decision_id,
        hypothesis_id=req.hypothesis_id,
        risk_profile=req.risk_profile or {},
        position_size=req.qty,
        approval_mode=req.autonomy_input.autonomy_level.value,
        approved=decision_out.decision == Decision.APPROVE,
        decision_reason=decision_out.reason,
        created_at=_utc_now(),
    )

    if decision_out.decision != Decision.APPROVE:
        return {
            "executed": False,
            "decision": decision_out.decision.value,
            "reason": decision_out.reason,
        }

    order_id = str(uuid4())
    order_payload = {
        "symbol": req.symbol,
        "side": req.side,
        "qty": req.qty,
        "type": req.order_type,
        "limit_price": req.limit_price,
    }

    try:
        outcome = call_with_healing(
            registry=adapters,
            adapter_type=AdapterType.EXECUTION,
            preferred_name=req.venue_adapter_name,
            fallback_names=req.venue_fallback_names,
            retries_per_adapter=2,
            call_fn=lambda adapter: adapter.place_order(order_payload),
        )
        execution = outcome.payload
        used_venue = outcome.adapter_name
    except AdapterCallError as exc:
        store.insert_order(
            order_id=order_id,
            hypothesis_id=req.hypothesis_id,
            venue=req.venue_adapter_name,
            symbol=req.symbol,
            side=req.side,
            order_type=req.order_type,
            qty=req.qty,
            limit_price=req.limit_price,
            status="adapter_error",
            created_at=_utc_now(),
        )
        return {
            "executed": False,
            "decision": decision_out.decision.value,
            "reason": "execution_adapter_failure",
            "error": str(exc),
            "order_id": order_id,
            "attempts": [
                {
                    "adapter_name": attempt.adapter_name,
                    "success": attempt.success,
                    "error": attempt.error,
                }
                for attempt in exc.attempts
            ],
        }
    except Exception as exc:
        store.insert_order(
            order_id=order_id,
            hypothesis_id=req.hypothesis_id,
            venue=req.venue_adapter_name,
            symbol=req.symbol,
            side=req.side,
            order_type=req.order_type,
            qty=req.qty,
            limit_price=req.limit_price,
            status="internal_error",
            created_at=_utc_now(),
        )
        return {
            "executed": False,
            "decision": decision_out.decision.value,
            "reason": "unexpected_execution_error",
            "error": f"{type(exc).__name__}: {exc}",
            "order_id": order_id,
        }

    store.insert_order(
        order_id=order_id,
        hypothesis_id=req.hypothesis_id,
        venue=used_venue,
        symbol=req.symbol,
        side=req.side,
        order_type=req.order_type,
        qty=req.qty,
        limit_price=req.limit_price,
        status=execution.get("status", "unknown"),
        created_at=_utc_now(),
    )

    fill_id = str(uuid4())
    store.insert_fill(
        fill_id=fill_id,
        order_id=order_id,
        fill_time=_utc_now(),
        fill_price=float(execution.get("avg_fill_price", req.limit_price or 0.0)),
        fill_qty=float(execution.get("qty", req.qty)),
        fee=float(execution.get("fee", 0.0)),
    )
    return {
        "executed": True,
        "decision": decision_out.decision.value,
        "order_id": order_id,
        "fill_id": fill_id,
    }
