"""
Paper Trading v2 — WebSocket Real-Time Engine
Connects to Bybit public WebSocket for real-time tickers + 1h kline signals.
Strategies: EMA crossover + RSI mean reversion (configurable).
"""
import asyncio
import json
import logging
import time
import requests
import websockets
from datetime import datetime
from pathlib import Path
from collections import deque
import ccxt

try:
    import config
except ImportError:
    import config_template as config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("paper_trading.log"), logging.StreamHandler()],
)
log = logging.getLogger("paper_ws")

STATE_FILE = Path("paper_state.json")
BYBIT_WS = "wss://stream.bybit.com/v5/public/linear"

# Map: WebSocket symbol → ccxt symbol
WS_TO_CCXT = {s.replace("/", "").replace(":USDT", ""): s for s in config.SYMBOLS}
# e.g. {"ETHUSDT": "ETH/USDT:USDT", "SOLUSDT": "SOL/USDT:USDT"}


def send_tg(msg: str):
    if not config.TG_BOT_TOKEN:
        return
    try:
        requests.post(
            f"https://api.telegram.org/bot{config.TG_BOT_TOKEN}/sendMessage",
            json={"chat_id": config.TG_CHAT_ID, "text": msg, "parse_mode": "HTML"},
            timeout=10,
        )
    except Exception as e:
        log.error(f"TG send failed: {e}")


class PaperTrader:
    def __init__(self):
        self.exchange = ccxt.bybit({"enableRateLimit": True, "options": {"defaultType": "swap"}})
        self.capital = config.TOTAL_CAPITAL
        self.positions = {}   # strategy_name → position dict
        self.trades = []
        self.prices = {}      # ws_symbol → float
        self.klines = {}      # ws_symbol → deque of candles
        self.load_state()

    def load_state(self):
        if STATE_FILE.exists():
            data = json.loads(STATE_FILE.read_text())
            self.capital = data.get("capital", config.TOTAL_CAPITAL)
            self.positions = data.get("positions", {})
            self.trades = data.get("trades", [])
            log.info(f"Loaded state: capital=${self.capital:.2f}, {len(self.positions)} positions, {len(self.trades)} trades")

    def save_state(self):
        STATE_FILE.write_text(json.dumps({
            "capital": self.capital,
            "positions": self.positions,
            "trades": self.trades,
            "prices": dict(self.prices),
            "updated_at": datetime.now().isoformat(),
        }, indent=2, default=str))

    def init_klines(self):
        """Pull historical 1h candles via REST on startup."""
        for ws_sym, ccxt_sym in WS_TO_CCXT.items():
            try:
                candles = self.exchange.fetch_ohlcv(ccxt_sym, "1h", limit=50)
                self.klines[ws_sym] = deque(maxlen=50)
                for c in candles:
                    self.klines[ws_sym].append({"t": c[0], "o": c[1], "h": c[2], "l": c[3], "c": c[4], "v": c[5]})
                log.info(f"Init {ws_sym}: {len(self.klines[ws_sym])} candles")
            except Exception as e:
                log.error(f"Failed to fetch {ws_sym} klines: {e}")
                self.klines[ws_sym] = deque(maxlen=50)

    # ── Position Management ──

    def open_position(self, strategy: str, symbol: str, side: str, price: float):
        margin = self.capital * config.MAX_POSITION_PCT
        leverage = config.MAX_LEVERAGE
        amount = (margin * leverage) / price
        fee = margin * leverage * 0.0006  # Bybit taker fee

        if side == "long":
            sl = price * (1 - config.STOP_LOSS_PCT)
            tp = price * (1 + config.TAKE_PROFIT_PCT)
        else:
            sl = price * (1 + config.STOP_LOSS_PCT)
            tp = price * (1 - config.TAKE_PROFIT_PCT)

        self.capital -= fee
        self.positions[strategy] = {
            "symbol": symbol, "side": side,
            "entry_price": price, "amount": amount,
            "margin": margin, "sl": sl, "tp": tp,
            "entry_time": datetime.now().isoformat(), "entry_fee": fee,
        }
        self.save_state()

        coin = symbol.replace("USDT", "")
        msg = f"📝 <b>[Paper] {strategy} OPEN</b>\n{coin} {side.upper()} @ ${price:,.2f}\nMargin: ${margin:.2f} | {leverage}x\nSL: ${sl:,.2f} | TP: ${tp:,.2f}"
        log.info(msg)
        send_tg(msg)

    def close_position(self, strategy: str, price: float, reason: str):
        if strategy not in self.positions:
            return
        pos = self.positions[strategy]
        fee = pos["margin"] * config.MAX_LEVERAGE * 0.0006
        if pos["side"] == "long":
            pnl = (price - pos["entry_price"]) / pos["entry_price"] * pos["margin"] * config.MAX_LEVERAGE
        else:
            pnl = (pos["entry_price"] - price) / pos["entry_price"] * pos["margin"] * config.MAX_LEVERAGE
        net_pnl = pnl - fee
        self.capital += net_pnl

        self.trades.append({
            "strategy": strategy, "symbol": pos["symbol"], "side": pos["side"],
            "entry_price": pos["entry_price"], "exit_price": price,
            "margin": pos["margin"], "pnl": round(net_pnl, 2),
            "pnl_pct": round(net_pnl / pos["margin"] * 100, 1),
            "reason": reason, "entry_time": pos["entry_time"],
            "exit_time": datetime.now().isoformat(),
        })
        del self.positions[strategy]
        self.save_state()

        coin = pos["symbol"].replace("USDT", "")
        emoji = "💚" if net_pnl > 0 else "🔴"
        msg = f"{emoji} <b>[Paper] {strategy} CLOSE</b>\n{coin} {pos['side'].upper()} | {reason}\n${pos['entry_price']:,.2f} → ${price:,.2f}\nPnL: ${net_pnl:+.2f} ({net_pnl/pos['margin']*100:+.1f}%)\nBalance: ${self.capital:.2f}"
        log.info(msg)
        send_tg(msg)

    def check_sl_tp(self, strategy: str, price: float):
        if strategy not in self.positions:
            return
        pos = self.positions[strategy]
        if pos["side"] == "long":
            if price <= pos["sl"]:
                self.close_position(strategy, pos["sl"], "Stop Loss")
            elif price >= pos["tp"]:
                self.close_position(strategy, pos["tp"], "Take Profit")
        else:
            if price >= pos["sl"]:
                self.close_position(strategy, pos["sl"], "Stop Loss")
            elif price <= pos["tp"]:
                self.close_position(strategy, pos["tp"], "Take Profit")

    # ── Indicators ──

    @staticmethod
    def calc_ema(closes: list, span: int) -> list:
        ema = [closes[0]]
        k = 2 / (span + 1)
        for c in closes[1:]:
            ema.append(c * k + ema[-1] * (1 - k))
        return ema

    @staticmethod
    def calc_rsi(closes: list, period: int = 14) -> list:
        deltas = [closes[i] - closes[i - 1] for i in range(1, len(closes))]
        rsi = [50.0] * period
        gains = [max(d, 0) for d in deltas[:period]]
        losses = [max(-d, 0) for d in deltas[:period]]
        avg_gain = sum(gains) / period
        avg_loss = sum(losses) / period
        for i in range(period, len(deltas)):
            d = deltas[i]
            avg_gain = (avg_gain * (period - 1) + max(d, 0)) / period
            avg_loss = (avg_loss * (period - 1) + max(-d, 0)) / period
            rs = avg_gain / avg_loss if avg_loss else float("inf")
            rsi.append(100 - (100 / (1 + rs)))
        return rsi

    # ── Strategy Signals (on candle close) ──

    def check_ema_crossover(self, strategy: str, symbol: str, fast: int = 12, slow: int = 26):
        """EMA crossover strategy. Call on candle close."""
        if symbol not in self.klines or len(self.klines[symbol]) < slow + 1:
            return
        closes = [k["c"] for k in self.klines[symbol]]
        price = closes[-1]

        if symbol in self.prices:
            self.check_sl_tp(strategy, self.prices[symbol])

        ema_fast = self.calc_ema(closes, fast)
        ema_slow = self.calc_ema(closes, slow)
        golden = ema_fast[-2] <= ema_slow[-2] and ema_fast[-1] > ema_slow[-1]
        death = ema_fast[-2] >= ema_slow[-2] and ema_fast[-1] < ema_slow[-1]

        if strategy in self.positions:
            pos = self.positions[strategy]
            if pos["side"] == "long" and death:
                self.close_position(strategy, price, "EMA Death Cross")
            elif pos["side"] == "short" and golden:
                self.close_position(strategy, price, "EMA Golden Cross")
        else:
            if golden:
                self.open_position(strategy, symbol, "long", price)
            elif death:
                self.open_position(strategy, symbol, "short", price)

    def check_rsi(self, strategy: str, symbol: str, period: int = 14, oversold: int = 30, overbought: int = 70):
        """RSI mean reversion strategy. Call on candle close."""
        if symbol not in self.klines or len(self.klines[symbol]) < period + 5:
            return
        closes = [k["c"] for k in self.klines[symbol]]
        price = closes[-1]

        if symbol in self.prices:
            self.check_sl_tp(strategy, self.prices[symbol])

        rsi = self.calc_rsi(closes, period)
        curr, prev = rsi[-1], rsi[-2]

        if strategy in self.positions:
            pos = self.positions[strategy]
            if pos["side"] == "long" and curr > overbought:
                self.close_position(strategy, price, "RSI Overbought")
            elif pos["side"] == "short" and curr < oversold:
                self.close_position(strategy, price, "RSI Oversold")
        else:
            if prev < oversold and curr >= oversold:
                self.open_position(strategy, symbol, "long", price)
            elif prev > overbought and curr <= overbought:
                self.open_position(strategy, symbol, "short", price)

    # ── Kline Update ──

    def update_kline(self, symbol: str, kline_data: dict):
        if symbol not in self.klines:
            self.klines[symbol] = deque(maxlen=50)
        t = kline_data["start"]
        candle = {
            "t": t, "o": float(kline_data["open"]), "h": float(kline_data["high"]),
            "l": float(kline_data["low"]), "c": float(kline_data["close"]), "v": float(kline_data["volume"]),
        }
        if self.klines[symbol] and self.klines[symbol][-1]["t"] == t:
            self.klines[symbol][-1] = candle
        else:
            self.klines[symbol].append(candle)

        if kline_data.get("confirm", False):
            log.info(f"Candle close: {symbol} @ {candle['c']}")
            # ── STRATEGY DISPATCH ── customize here
            if symbol == "ETHUSDT":
                self.check_ema_crossover("ETH_EMA", symbol)
            elif symbol == "SOLUSDT":
                self.check_rsi("SOL_RSI", symbol)

    def summary(self) -> str:
        wins = [t for t in self.trades if t["pnl"] > 0]
        total_pnl = sum(t["pnl"] for t in self.trades)
        wr = len(wins) / len(self.trades) * 100 if self.trades else 0
        lines = [
            f"Balance: ${self.capital:.2f} | PnL: ${total_pnl:+.2f}",
            f"Trades: {len(self.trades)} | Win rate: {wr:.0f}%",
            f"Open: {len(self.positions)}",
        ]
        return "\n".join(lines)


async def run(trader: PaperTrader):
    ws_symbols = list(WS_TO_CCXT.keys())
    subscribe = {
        "op": "subscribe",
        "args": [f"tickers.{s}" for s in ws_symbols] + [f"kline.60.{s}" for s in ws_symbols],
    }
    last_save = time.time()
    last_report = time.time()

    while True:
        try:
            async with websockets.connect(BYBIT_WS, ping_interval=20) as ws:
                await ws.send(json.dumps(subscribe))
                log.info(f"Connected. Subscribed: {ws_symbols}")
                async for raw in ws:
                    data = json.loads(raw)
                    if "op" in data:
                        continue
                    topic = data.get("topic", "")
                    msg = data.get("data", {})

                    if topic.startswith("tickers."):
                        sym = topic.split(".")[1]
                        if isinstance(msg, dict) and "lastPrice" in msg:
                            price = float(msg["lastPrice"])
                            trader.prices[sym] = price
                            for strat, pos in list(trader.positions.items()):
                                if pos["symbol"] == sym:
                                    trader.check_sl_tp(strat, price)

                    elif topic.startswith("kline."):
                        parts = topic.split(".")
                        sym = parts[2] if len(parts) > 2 else ""
                        klines = msg if isinstance(msg, list) else [msg]
                        for kl in klines:
                            trader.update_kline(sym, kl)

                    now = time.time()
                    if now - last_save > 300:
                        last_save = now
                        trader.save_state()
                    if now - last_report > 21600:
                        last_report = now
                        send_tg(trader.summary())

        except (websockets.ConnectionClosed, ConnectionError) as e:
            log.warning(f"Disconnected: {e}, reconnecting in 5s...")
            await asyncio.sleep(5)
        except Exception as e:
            log.error(f"Error: {e}, reconnecting in 10s...")
            await asyncio.sleep(10)


def main():
    trader = PaperTrader()
    trader.init_klines()
    send_tg(f"Paper Trading Started\n{trader.summary()}")
    asyncio.run(run(trader))


if __name__ == "__main__":
    main()
