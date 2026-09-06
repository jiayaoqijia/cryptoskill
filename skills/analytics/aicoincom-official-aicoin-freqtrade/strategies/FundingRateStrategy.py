# FundingRateStrategy - Exploit extreme funding rates for mean reversion
# Powered by AiCoin's cross-exchange weighted funding rate data
#
# How it works:
#   - Extreme positive funding -> market over-leveraged long -> expect pullback -> short
#   - Extreme negative funding -> market over-leveraged short -> expect bounce -> long
#   - Uses Bollinger Bands for timing entries at price extremes
#   - AiCoin advantage: volume-weighted funding rates across ALL exchanges,
#     not just a single exchange's rate (more accurate market sentiment)
#
# AiCoin tier required: Basic ($29/mo) for funding_rate
# Backtest: works with Bollinger Bands + RSI only
# Live: funding rate data adds significant edge
#
from freqtrade.strategy import IStrategy, IntParameter, DecimalParameter
from pandas import DataFrame
import logging

logger = logging.getLogger(__name__)


class FundingRateStrategy(IStrategy):
    INTERFACE_VERSION = 3
    timeframe = '1h'
    can_short = True

    # ROI table (optimized via hyperopt)
    minimal_roi = {"0": 0.374, "167": 0.11, "554": 0.085, "1841": 0}

    stoploss = -0.213
    trailing_stop = True
    trailing_stop_positive = 0.142
    trailing_stop_positive_offset = 0.23
    trailing_only_offset_is_reached = False

    # Hyperopt parameters (defaults from hyperopt optimization)
    bb_period = IntParameter(15, 30, default=23, space='buy')
    bb_std = DecimalParameter(1.5, 3.0, default=2.215, space='buy')
    rsi_oversold = IntParameter(20, 40, default=20, space='buy')
    rsi_overbought = IntParameter(60, 80, default=68, space='sell')
    funding_threshold = DecimalParameter(0.01, 0.10, default=0.013, space='buy')

    # AiCoin live data
    _ac_funding_rate = 0.0    # Current funding rate (%)
    _ac_funding_trend = 0.0   # Funding rate momentum
    _ac_last_update = 0.0

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # ── Bollinger Bands ──
        period = self.bb_period.value
        dataframe['bb_mid'] = dataframe['close'].rolling(window=period).mean()
        rolling_std = dataframe['close'].rolling(window=period).std()
        dataframe['bb_upper'] = dataframe['bb_mid'] + self.bb_std.value * rolling_std
        dataframe['bb_lower'] = dataframe['bb_mid'] - self.bb_std.value * rolling_std

        # Bollinger Band width (volatility measure)
        dataframe['bb_width'] = (dataframe['bb_upper'] - dataframe['bb_lower']) / dataframe['bb_mid']

        # ── RSI ──
        delta = dataframe['close'].diff()
        gain = delta.clip(lower=0).rolling(window=14).mean()
        loss = (-delta.clip(upper=0)).rolling(window=14).mean()
        rs = gain / loss
        dataframe['rsi'] = 100 - (100 / (1 + rs))

        # ── Volume ──
        dataframe['vol_sma'] = dataframe['volume'].rolling(window=20).mean()

        # ── AiCoin funding rate (live only) ──
        dataframe['funding_rate'] = 0.0
        dataframe['funding_extreme'] = 0  # -1=very negative, 0=neutral, +1=very positive

        if self.dp and self.dp.runmode.value in ('live', 'dry_run'):
            import time
            now = time.time()
            if now - self._ac_last_update > 300:
                self._update_funding(metadata)
                self._ac_last_update = now

            dataframe.iloc[-1, dataframe.columns.get_loc('funding_rate')] = self._ac_funding_rate
            threshold = self.funding_threshold.value
            if self._ac_funding_rate > threshold:
                dataframe.iloc[-1, dataframe.columns.get_loc('funding_extreme')] = 1
            elif self._ac_funding_rate < -threshold:
                dataframe.iloc[-1, dataframe.columns.get_loc('funding_extreme')] = -1

        return dataframe

    def _update_funding(self, metadata: dict):
        """Fetch the latest funding rate from AiCoin (live/dry-run only)."""
        try:
            import sys, os
            _sd = os.path.dirname(os.path.abspath(__file__))
            if _sd not in sys.path:
                sys.path.insert(0, _sd)
            from aicoin_data import AiCoinData
            ac = AiCoinData(cache_ttl=300)
            pair = metadata.get('pair', 'BTC/USDT:USDT')
            exchange = self.config.get('exchange', {}).get('name', 'binance')

            try:
                self._ac_funding_rate = ac.funding_rate_pct(pair, exchange)
                logger.info(f"AiCoin funding rate for {pair}: {self._ac_funding_rate:.4f}%")
            except Exception as e:
                logger.debug(f"AiCoin funding_rate unavailable: {e}")

        except ImportError:
            logger.warning("aicoin_data module not found. Run ft-deploy.mjs to install.")
        except Exception as e:
            logger.warning(f"AiCoin data error: {e}")

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Long: price at BB lower + RSI oversold + volume confirmation
        dataframe.loc[
            (dataframe['close'] < dataframe['bb_lower']) &
            (dataframe['rsi'] < self.rsi_oversold.value) &
            (dataframe['volume'] > dataframe['vol_sma'] * 0.5) &
            # Funding boost: negative funding = shorts paying, expect squeeze
            (dataframe['funding_extreme'] <= 0),
            'enter_long'] = 1

        # Short: price at BB upper + RSI overbought + volume confirmation
        dataframe.loc[
            (dataframe['close'] > dataframe['bb_upper']) &
            (dataframe['rsi'] > self.rsi_overbought.value) &
            (dataframe['volume'] > dataframe['vol_sma'] * 0.5) &
            # Funding boost: positive funding = longs paying, expect dump
            (dataframe['funding_extreme'] >= 0),
            'enter_short'] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Exit long when price reaches BB mid (conservative take-profit)
        dataframe.loc[
            (dataframe['close'] > dataframe['bb_mid']) &
            (dataframe['rsi'] > 55),
            'exit_long'] = 1

        # Exit short when price reaches BB mid
        dataframe.loc[
            (dataframe['close'] < dataframe['bb_mid']) &
            (dataframe['rsi'] < 45),
            'exit_short'] = 1

        return dataframe
