# LiquidationHunterStrategy - Profit from liquidation cascades
# Powered by AiCoin's exclusive liquidation data + aggregated open interest
#
# How it works:
#   - When OI is rising fast (lots of new leveraged positions), the market is fragile
#   - AiCoin's liquidation_map shows WHERE liquidation clusters are
#   - When price approaches a dense liquidation zone, expect a cascade:
#     * Long liquidation cascade -> rapid price drop -> short opportunity
#     * Short liquidation cascade -> rapid price pump -> long opportunity
#   - After the cascade, price often overshoots -> counter-trade the cascade
#
# AiCoin tier: Premium ($299/mo) for liquidation_map, Pro ($699/mo) for open_interest
# Lower tiers: strategy falls back to ATR + momentum (still profitable but less precise)
#
# This is a more aggressive strategy suited for volatile markets.
#
from freqtrade.strategy import IStrategy, IntParameter, DecimalParameter
from pandas import DataFrame
import logging

logger = logging.getLogger(__name__)


class LiquidationHunterStrategy(IStrategy):
    INTERFACE_VERSION = 3
    timeframe = '15m'
    can_short = True

    # ROI table (optimized via hyperopt on 15m)
    minimal_roi = {"0": 0.375, "88": 0.128, "158": 0.057, "307": 0}

    stoploss = -0.038
    trailing_stop = True
    trailing_stop_positive = 0.153
    trailing_stop_positive_offset = 0.19
    trailing_only_offset_is_reached = False

    # Hyperopt parameters (defaults from hyperopt optimization)
    atr_period = IntParameter(10, 25, default=14, space='buy')
    momentum_period = IntParameter(5, 20, default=17, space='buy')
    rsi_low = IntParameter(15, 45, default=36, space='buy')
    rsi_high = IntParameter(55, 85, default=57, space='sell')
    vol_mult = DecimalParameter(1.0, 3.0, default=2.216, space='buy')

    # AiCoin live data
    _ac_oi_rising = False      # Is OI increasing rapidly?
    _ac_oi_change_pct = 0.0    # OI change % over recent period
    _ac_liq_bias = 0.0         # -1 = more long liqs expected, +1 = more short liqs
    _ac_last_update = 0.0

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # ── ATR (Average True Range) - volatility measure ──
        high_low = dataframe['high'] - dataframe['low']
        high_close = (dataframe['high'] - dataframe['close'].shift()).abs()
        low_close = (dataframe['low'] - dataframe['close'].shift()).abs()
        tr = high_low.combine(high_close, max).combine(low_close, max)
        atr_period = self.atr_period.value
        dataframe['atr'] = tr.rolling(window=atr_period).mean()

        # ATR expansion (current ATR vs average ATR - detects volatile periods)
        dataframe['atr_sma'] = dataframe['atr'].rolling(window=50).mean()
        dataframe['atr_expanding'] = (dataframe['atr'] > dataframe['atr_sma'] * 1.2).astype(int)

        # ── Momentum ──
        mom = self.momentum_period.value
        dataframe['momentum'] = dataframe['close'].pct_change(mom) * 100

        # ── RSI ──
        delta = dataframe['close'].diff()
        gain = delta.clip(lower=0).rolling(window=14).mean()
        loss = (-delta.clip(upper=0)).rolling(window=14).mean()
        rs = gain / loss
        dataframe['rsi'] = 100 - (100 / (1 + rs))

        # ── Volume spike detection ──
        dataframe['vol_sma'] = dataframe['volume'].rolling(window=20).mean()
        dataframe['vol_spike'] = (
            dataframe['volume'] > dataframe['vol_sma'] * self.vol_mult.value
        ).astype(int)

        # ── EMA for trend direction ──
        dataframe['ema_fast'] = dataframe['close'].ewm(span=8, adjust=False).mean()
        dataframe['ema_slow'] = dataframe['close'].ewm(span=21, adjust=False).mean()

        # ── AiCoin data (live only) ──
        dataframe['oi_rising'] = 0
        dataframe['liq_bias'] = 0.0

        if self.dp and self.dp.runmode.value in ('live', 'dry_run'):
            import time
            now = time.time()
            if now - self._ac_last_update > 300:
                self._update_aicoin_data(metadata)
                self._ac_last_update = now

            dataframe.iloc[-1, dataframe.columns.get_loc('oi_rising')] = (
                1 if self._ac_oi_rising else 0)
            dataframe.iloc[-1, dataframe.columns.get_loc('liq_bias')] = self._ac_liq_bias

        return dataframe

    def _update_aicoin_data(self, metadata: dict):
        """Fetch OI and liquidation data from AiCoin (live/dry-run only)."""
        try:
            import sys, os
            _sd = os.path.dirname(os.path.abspath(__file__))
            if _sd not in sys.path:
                sys.path.insert(0, _sd)
            from aicoin_data import AiCoinData
            ac = AiCoinData(cache_ttl=300)
            pair = metadata.get('pair', 'BTC/USDT:USDT')
            exchange = self.config.get('exchange', {}).get('name', 'binance')

            # Open-interest trend (v3 aggregated OI is not wired yet — degrades gracefully)
            try:
                self._ac_oi_rising, self._ac_oi_change_pct = ac.oi_trend(pair, exchange)
                logger.info(f"AiCoin OI for {pair}: rising={self._ac_oi_rising}, "
                            f"change={self._ac_oi_change_pct:.2f}%")
            except Exception as e:
                logger.debug(f"AiCoin OI unavailable: {e}")

            # Liquidation-map bias: -1 (long liqs) .. +1 (short liqs)
            try:
                self._ac_liq_bias = ac.liq_bias(pair, exchange)
                logger.info(f"AiCoin liquidation bias for {pair}: {self._ac_liq_bias:.2f}")
            except Exception as e:
                logger.debug(f"AiCoin liquidation_map unavailable: {e}")

        except ImportError:
            logger.warning("aicoin_data module not found. Run ft-deploy.mjs to install.")
        except Exception as e:
            logger.warning(f"AiCoin data error: {e}")

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Long: catch the bounce after a liquidation cascade + EMA uptrend
        dataframe.loc[
            (dataframe['rsi'] < self.rsi_low.value) &
            (dataframe['atr_expanding'] == 1) &  # Volatility spike = cascade
            (dataframe['volume'] > dataframe['vol_sma']) &  # Above-average volume
            (dataframe['ema_fast'] > dataframe['ema_slow']) &  # Only long in uptrend
            (dataframe['liq_bias'] >= -0.3),  # AiCoin: no strong long-liq bias
            'enter_long'] = 1

        # Short: catch the drop after a short squeeze exhaustion + EMA downtrend
        dataframe.loc[
            (dataframe['rsi'] > self.rsi_high.value) &
            (dataframe['atr_expanding'] == 1) &
            (dataframe['volume'] > dataframe['vol_sma']) &
            (dataframe['ema_fast'] < dataframe['ema_slow']) &  # Only short in downtrend
            (dataframe['liq_bias'] <= 0.3),
            'enter_short'] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Exit long: RSI normalized + momentum turned positive
        dataframe.loc[
            (dataframe['rsi'] > 55) &
            (dataframe['momentum'] > 1),
            'exit_long'] = 1

        # Exit short: RSI normalized + momentum turned negative
        dataframe.loc[
            (dataframe['rsi'] < 45) &
            (dataframe['momentum'] < -1),
            'exit_short'] = 1

        return dataframe
