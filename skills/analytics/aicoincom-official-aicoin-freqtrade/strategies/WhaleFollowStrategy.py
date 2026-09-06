# WhaleFollowStrategy - Follow whale/institutional order flow
# Powered by AiCoin's exclusive big_orders data (200+ exchanges aggregated)
#
# How it works:
#   - Standard indicators (RSI + EMA) provide base signals (works in backtest)
#   - In live/dry-run mode, AiCoin whale data adds an edge:
#     * big_orders: detect large institutional buy/sell pressure
#     * ls_ratio: cross-exchange long/short ratio as contrarian signal
#   - When whales are buying AND retail is short -> strong long signal
#   - When whales are selling AND retail is long -> strong short signal
#
# AiCoin tier required: Normal ($99/mo) for big_orders, Basic ($29/mo) for ls_ratio
# Backtest: works with standard indicators only (conservative estimate)
# Live: AiCoin data adds alpha on top of base signals
#
from freqtrade.strategy import IStrategy, IntParameter, DecimalParameter
from pandas import DataFrame
import logging

logger = logging.getLogger(__name__)


class WhaleFollowStrategy(IStrategy):
    INTERFACE_VERSION = 3
    timeframe = '15m'
    can_short = True

    # ROI: take profit at these thresholds (optimized via hyperopt)
    minimal_roi = {"0": 0.316, "107": 0.106, "178": 0.047, "217": 0}

    stoploss = -0.236
    use_exit_signal = False  # ROI + trailing stop exits outperform signal-based exits

    trailing_stop = True
    trailing_stop_positive = 0.042
    trailing_stop_positive_offset = 0.061

    # Hyperopt-optimizable parameters (defaults from hyperopt optimization)
    rsi_buy = IntParameter(20, 40, default=34, space='buy')
    rsi_sell = IntParameter(60, 80, default=65, space='sell')
    ema_fast_len = IntParameter(5, 15, default=9, space='buy')
    ema_slow_len = IntParameter(15, 30, default=23, space='buy')
    whale_weight = DecimalParameter(0.0, 1.0, default=0.324, space='buy')

    # AiCoin data (updated periodically in live mode)
    _ac_whale_signal = 0.0   # -1 (selling) to +1 (buying)
    _ac_ls_ratio = 0.5       # 0-1, >0.5 = more longs
    _ac_last_update = 0.0

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # ── Standard indicators (always available) ──
        # RSI
        delta = dataframe['close'].diff()
        gain = delta.clip(lower=0).rolling(window=14).mean()
        loss = (-delta.clip(upper=0)).rolling(window=14).mean()
        rs = gain / loss
        dataframe['rsi'] = 100 - (100 / (1 + rs))

        # EMA
        dataframe['ema_fast'] = dataframe['close'].ewm(
            span=self.ema_fast_len.value, adjust=False).mean()
        dataframe['ema_slow'] = dataframe['close'].ewm(
            span=self.ema_slow_len.value, adjust=False).mean()

        # Volume SMA (for volume confirmation)
        dataframe['vol_sma'] = dataframe['volume'].rolling(window=20).mean()

        # ── AiCoin whale data (live/dry-run only) ──
        dataframe['whale_signal'] = 0.0
        dataframe['ls_ratio'] = 0.5

        if self.dp and self.dp.runmode.value in ('live', 'dry_run'):
            import time
            now = time.time()
            # Update AiCoin data every 5 minutes
            if now - self._ac_last_update > 300:
                self._update_aicoin_data(metadata)
                self._ac_last_update = now

            # Apply to last row (current candle)
            dataframe.iloc[-1, dataframe.columns.get_loc('whale_signal')] = self._ac_whale_signal
            dataframe.iloc[-1, dataframe.columns.get_loc('ls_ratio')] = self._ac_ls_ratio

        return dataframe

    def _update_aicoin_data(self, metadata: dict):
        """Fetch latest AiCoin whale data (live/dry-run only)."""
        try:
            import sys, os
            _sd = os.path.dirname(os.path.abspath(__file__))
            if _sd not in sys.path:
                sys.path.insert(0, _sd)
            from aicoin_data import AiCoinData
            ac = AiCoinData(cache_ttl=300)
            pair = metadata.get('pair', 'BTC/USDT:USDT')
            exchange = self.config.get('exchange', {}).get('name', 'binance')

            # Whale order-book pressure: -1 (selling) .. +1 (buying)
            try:
                self._ac_whale_signal = ac.whale_signal(pair, exchange)
                logger.info(f"AiCoin whale signal for {pair}: {self._ac_whale_signal:.2f}")
            except Exception as e:
                logger.debug(f"AiCoin whale data unavailable: {e}")

            # Long/short ratio normalized to 0..1 ( >0.5 = more longs )
            try:
                self._ac_ls_ratio = ac.ls_ratio_norm()
                logger.info(f"AiCoin L/S ratio: {self._ac_ls_ratio:.2f}")
            except Exception as e:
                logger.debug(f"AiCoin ls_ratio unavailable: {e}")

        except ImportError:
            logger.warning("aicoin_data module not found. Run ft-deploy.mjs to install.")
        except Exception as e:
            logger.warning(f"AiCoin data error: {e}")

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        w = self.whale_weight.value

        # Long entry: uptrend + RSI low + whale buying + retail short
        dataframe.loc[
            (dataframe['rsi'] < self.rsi_buy.value) &
            (dataframe['ema_fast'] > dataframe['ema_slow']) &
            (dataframe['volume'] > dataframe['vol_sma'] * 0.5) &
            # AiCoin boost: whale buying (signal > 0) or no data (signal == 0)
            (dataframe['whale_signal'] >= -0.3 * w) &
            # AiCoin boost: contrarian - retail is short (ls_ratio < 0.5)
            (dataframe['ls_ratio'] <= 0.5 + 0.2 * (1 - w)),
            'enter_long'] = 1

        # Short entry: downtrend + RSI high + whale selling + retail long
        dataframe.loc[
            (dataframe['rsi'] > self.rsi_sell.value) &
            (dataframe['ema_fast'] < dataframe['ema_slow']) &
            (dataframe['volume'] > dataframe['vol_sma'] * 0.5) &
            (dataframe['whale_signal'] <= 0.3 * w) &
            (dataframe['ls_ratio'] >= 0.5 - 0.2 * (1 - w)),
            'enter_short'] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (dataframe['rsi'] > 75),
            'exit_long'] = 1

        dataframe.loc[
            (dataframe['rsi'] < 25),
            'exit_short'] = 1

        return dataframe
