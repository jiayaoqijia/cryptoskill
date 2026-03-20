"""
Risk Manager — enforces position sizing, daily loss limits, and max positions.
Import config_template as config (or your renamed config.py).
"""
import json
from datetime import datetime, date
from pathlib import Path

try:
    import config
except ImportError:
    import config_template as config

STATE_FILE = Path(__file__).parent / "risk_state.json"


class RiskManager:
    def __init__(self, capital: float = None):
        self.capital = capital or config.TOTAL_CAPITAL
        self.daily_pnl = 0.0
        self.open_positions = 0
        self.today = date.today().isoformat()
        self.trades_today = 0
        self.load_state()

    def load_state(self):
        if STATE_FILE.exists():
            data = json.loads(STATE_FILE.read_text())
            if data.get("date") == date.today().isoformat():
                self.daily_pnl = data.get("daily_pnl", 0.0)
                self.trades_today = data.get("trades_today", 0)
            else:
                self.reset_daily()

    def save_state(self):
        STATE_FILE.write_text(json.dumps({
            "date": date.today().isoformat(),
            "daily_pnl": self.daily_pnl,
            "trades_today": self.trades_today,
            "open_positions": self.open_positions,
            "updated_at": datetime.now().isoformat(),
        }, indent=2))

    def reset_daily(self):
        self.daily_pnl = 0.0
        self.trades_today = 0
        self.today = date.today().isoformat()
        self.save_state()

    def can_open_position(self, size_usdt: float) -> tuple[bool, str]:
        """Check if a new position is allowed."""
        daily_limit = self.capital * config.DAILY_LOSS_LIMIT_PCT
        if self.daily_pnl <= -daily_limit:
            return False, f"Daily loss limit reached: ${abs(self.daily_pnl):.2f}/{daily_limit:.2f}"
        if self.open_positions >= config.MAX_OPEN_POSITIONS:
            return False, f"Max positions reached: {self.open_positions}/{config.MAX_OPEN_POSITIONS}"
        max_size = self.capital * config.MAX_POSITION_PCT
        if size_usdt > max_size:
            return False, f"Position too large: ${size_usdt:.2f} > ${max_size:.2f}"
        return True, "OK"

    def record_trade(self, pnl: float):
        self.daily_pnl += pnl
        self.trades_today += 1
        self.save_state()

    def position_opened(self):
        self.open_positions += 1
        self.save_state()

    def position_closed(self):
        self.open_positions = max(0, self.open_positions - 1)
        self.save_state()

    def get_max_position_size(self) -> float:
        return self.capital * config.MAX_POSITION_PCT

    def status(self) -> str:
        daily_limit = self.capital * config.DAILY_LOSS_LIMIT_PCT
        return (
            f"Risk Status | Date: {self.today}\n"
            f"Daily PnL: ${self.daily_pnl:+.2f} / -${daily_limit:.2f}\n"
            f"Positions: {self.open_positions}/{config.MAX_OPEN_POSITIONS}\n"
            f"Trades today: {self.trades_today}"
        )
