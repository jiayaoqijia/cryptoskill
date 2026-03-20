"""
Live Trading Engine — extends paper trading with real Bybit order execution.
Uses the same strategy logic; replaces simulated fills with actual API calls.
"""
import ccxt
import logging
import json
from datetime import datetime
from pathlib import Path

try:
    import config
except ImportError:
    import config_template as config

from risk_manager import RiskManager

log = logging.getLogger("live")

STATE_FILE = Path("live_state.json")


class LiveTrader:
    def __init__(self):
        self.exchange = ccxt.bybit({
            "apiKey": config.BYBIT_API_KEY,
            "secret": config.BYBIT_API_SECRET,
            "enableRateLimit": True,
            "options": {"defaultType": "swap"},
        })
        self.risk = RiskManager()

    def get_balance(self) -> float:
        """Fetch USDT balance from Bybit unified account."""
        bal = self.exchange.fetch_balance({"type": "swap"})
        return float(bal.get("USDT", {}).get("free", 0))

    def set_leverage(self, symbol: str, leverage: int):
        """Set leverage for a symbol."""
        try:
            self.exchange.set_leverage(leverage, symbol)
        except Exception as e:
            log.warning(f"Set leverage failed (may already be set): {e}")

    def open_long(self, symbol: str, amount: float, sl: float = None, tp: float = None):
        """Open a long position with optional SL/TP."""
        ok, reason = self.risk.can_open_position(amount * self._get_price(symbol) / config.MAX_LEVERAGE)
        if not ok:
            log.warning(f"Risk blocked: {reason}")
            return None

        self.set_leverage(symbol, config.MAX_LEVERAGE)
        params = {}
        if sl:
            params["stopLoss"] = {"triggerPrice": sl, "type": "market"}
        if tp:
            params["takeProfit"] = {"triggerPrice": tp, "type": "market"}

        order = self.exchange.create_order(symbol, "market", "buy", amount, params=params)
        self.risk.position_opened()
        log.info(f"LONG {symbol} amount={amount} order={order['id']}")
        return order

    def open_short(self, symbol: str, amount: float, sl: float = None, tp: float = None):
        """Open a short position with optional SL/TP."""
        ok, reason = self.risk.can_open_position(amount * self._get_price(symbol) / config.MAX_LEVERAGE)
        if not ok:
            log.warning(f"Risk blocked: {reason}")
            return None

        self.set_leverage(symbol, config.MAX_LEVERAGE)
        params = {}
        if sl:
            params["stopLoss"] = {"triggerPrice": sl, "type": "market"}
        if tp:
            params["takeProfit"] = {"triggerPrice": tp, "type": "market"}

        order = self.exchange.create_order(symbol, "market", "sell", amount, params=params)
        self.risk.position_opened()
        log.info(f"SHORT {symbol} amount={amount} order={order['id']}")
        return order

    def close_position(self, symbol: str, side: str):
        """Close an open position."""
        positions = self.exchange.fetch_positions([symbol])
        for pos in positions:
            if float(pos["contracts"]) > 0 and pos["side"] == side:
                close_side = "sell" if side == "long" else "buy"
                order = self.exchange.create_order(
                    symbol, "market", close_side, float(pos["contracts"]),
                    params={"reduceOnly": True}
                )
                self.risk.position_closed()
                log.info(f"CLOSED {symbol} {side} order={order['id']}")
                return order
        return None

    def get_positions(self) -> list:
        """Fetch all open positions."""
        symbols = config.SYMBOLS
        positions = self.exchange.fetch_positions(symbols)
        return [p for p in positions if float(p["contracts"]) > 0]

    def _get_price(self, symbol: str) -> float:
        ticker = self.exchange.fetch_ticker(symbol)
        return ticker["last"]


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    trader = LiveTrader()
    balance = trader.get_balance()
    print(f"Balance: ${balance:.2f} USDT")
    positions = trader.get_positions()
    print(f"Open positions: {len(positions)}")
    for p in positions:
        print(f"  {p['symbol']} {p['side']} {p['contracts']} contracts @ {p['entryPrice']}")
