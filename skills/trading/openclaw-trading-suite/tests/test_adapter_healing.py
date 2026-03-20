from dataclasses import dataclass
from typing import Any

from openclaw_trading_suite.adapters import (
    AdapterCallError,
    AdapterRegistry,
    AdapterType,
    ExecutionAdapter,
    call_with_healing,
)


@dataclass(frozen=True)
class FailingExecutionAdapter(ExecutionAdapter):
    name: str = "failing-execution"

    def place_order(self, order: dict[str, Any]) -> dict[str, Any]:
        raise RuntimeError("boom")


def test_healing_falls_back_to_second_adapter() -> None:
    registry = AdapterRegistry()
    registry.register(FailingExecutionAdapter())

    @dataclass(frozen=True)
    class GoodExecutionAdapter(ExecutionAdapter):
        name: str = "good-execution"

        def place_order(self, order: dict[str, Any]) -> dict[str, Any]:
            return {"status": "filled", "qty": order.get("qty"), "avg_fill_price": 101.0}

    registry.register(GoodExecutionAdapter())

    out = call_with_healing(
        registry=registry,
        adapter_type=AdapterType.EXECUTION,
        preferred_name="failing-execution",
        fallback_names=["good-execution"],
        retries_per_adapter=1,
        call_fn=lambda adapter: adapter.place_order({"symbol": "BTCUSD", "qty": 1}),
    )
    assert out.adapter_name == "good-execution"
    assert out.payload["status"] == "filled"
    assert any(not attempt.success for attempt in out.attempts)


def test_healing_raises_if_all_adapters_fail() -> None:
    registry = AdapterRegistry()
    registry.register(FailingExecutionAdapter())
    try:
        call_with_healing(
            registry=registry,
            adapter_type=AdapterType.EXECUTION,
            preferred_name="failing-execution",
            retries_per_adapter=1,
            call_fn=lambda adapter: adapter.place_order({"symbol": "BTCUSD", "qty": 1}),
        )
        assert False, "expected AdapterCallError"
    except AdapterCallError as exc:
        assert "all_adapter_attempts_failed" in str(exc)
        assert exc.attempts
