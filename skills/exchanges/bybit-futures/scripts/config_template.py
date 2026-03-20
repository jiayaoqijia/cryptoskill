"""
Trading System Configuration
Copy this to config.py and fill in your values.
"""
import os

# === Bybit API ===
# Get from: https://www.bybit.com/app/user/api-management
# Permissions needed: Read-Write (Contract), NO Assets/Withdrawal
BYBIT_API_KEY = os.getenv("BYBIT_API_KEY", "YOUR_API_KEY")
BYBIT_API_SECRET = os.getenv("BYBIT_API_SECRET", "YOUR_API_SECRET")

# === Telegram Notifications (optional) ===
# Create bot via @BotFather, get chat_id via @userinfobot
TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN", "")
TG_CHAT_ID = os.getenv("TG_CHAT_ID", "")

# === Risk Parameters ===
TOTAL_CAPITAL = 1000.0          # Total capital in USDT
MAX_POSITION_PCT = 0.20         # Max 20% of capital per trade
MAX_LEVERAGE = 5                # Max leverage multiplier
STOP_LOSS_PCT = 0.03            # 3% stop loss
TAKE_PROFIT_PCT = 0.06          # 6% take profit (2:1 reward/risk)
DAILY_LOSS_LIMIT_PCT = 0.10     # Stop trading after 10% daily loss
MAX_OPEN_POSITIONS = 3          # Max simultaneous positions

# === Trading Pairs ===
# Format: ccxt unified symbol for USDT perpetuals
SYMBOLS = [
    "ETH/USDT:USDT",
    "SOL/USDT:USDT",
]

# === Funding Rate Arbitrage (optional) ===
FUNDING_RATE_THRESHOLD = 0.0005   # Consider arb when rate > 0.05%
FUNDING_RATE_HIGH = 0.001         # Strong signal when rate > 0.1%

# === Intervals ===
PRICE_CHECK_INTERVAL = 10        # seconds (REST mode only)
FUNDING_CHECK_INTERVAL = 300     # seconds
