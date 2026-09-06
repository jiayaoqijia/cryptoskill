// Strategy code generator (从 ft-deploy.mjs 抽出来, 单一职责).
//
// 用 indicators[] + aicoin_data[] + 可选的 entry_logic / exit_logic 拼出
// 一份 freqtrade IStrategy 子类 .py 文件文本. 选 indicator 就生成对应的
// pandas 计算块, 选 aicoin_data 就生成 _update_aicoin_data + 在 entry 加
// 对应的过滤条件.
//
// 为什么不用 freqtrade-templates: 这里的目标是给 agent / 用户低门槛快速
// 生成可跑的策略, 不希望 agent 还要 mkdir / cp template / search-replace.
// 内置生成器一次产出完整文件.

export const AVAILABLE_INDICATORS = [
  'rsi', 'bb', 'bollinger', 'ema', 'sma', 'macd',
  'stochastic', 'kdj', 'atr', 'adx', 'cci',
  'williams_r', 'willr', 'vwap', 'ichimoku',
  'volume_sma', 'volume', 'obv',
];

export const AVAILABLE_AICOIN_DATA = [
  'funding_rate (付费套餐)',
  'ls_ratio (付费套餐)',
  'big_orders (付费套餐)',
  'open_interest (v3 聚合 OI 历史暂未接通，会自动降级)',
  'liquidation_map (付费套餐)',
];

export const PAID_DATA = {
  funding_rate: '付费套餐',
  ls_ratio: '付费套餐',
  big_orders: '付费套餐',
  open_interest: '付费套餐（注意 v3 聚合 OI 历史暂未接通）',
  liquidation_map: '付费套餐',
};

export function buildStrategyCode(name, tf, desc, ds, indicators, entryLogic, exitLogic, direction = 'long') {
  const L = [];  // lines
  const has = (k) => ds.has(k);
  const any = ds.size > 0;

  const defaultIndicators = ['rsi', 'bb', 'ema', 'volume_sma'];
  const allIndicators = new Set(indicators && indicators.length ? indicators.map((i) => i.toLowerCase()) : defaultIndicators);
  const hasInd = (k) => allIndicators.has(k);

  L.push(`# ${name} - ${desc}`);
  if (any) L.push(`# AiCoin data: ${[...ds].join(', ')} (live/dry_run only)`);
  L.push(`# Indicators: ${[...allIndicators].join(', ')}`);
  L.push(`# Backtest: uses technical indicators only`);
  L.push(`#`);
  L.push(`from freqtrade.strategy import IStrategy, IntParameter, DecimalParameter`);
  L.push(`from pandas import DataFrame`);
  L.push(`import logging`);
  L.push(``);
  L.push(`logger = logging.getLogger(__name__)`);
  L.push(``);
  L.push(``);
  L.push(`class ${name}(IStrategy):`);
  L.push(`    INTERFACE_VERSION = 3`);
  L.push(`    timeframe = '${tf}'`);
  const canShort = direction === 'both' || direction === 'short';
  L.push(`    can_short = ${canShort ? 'True' : 'False'}`);
  L.push(``);
  L.push(`    minimal_roi = {"0": 0.05, "60": 0.03, "120": 0.01}`);
  L.push(`    stoploss = -0.05`);
  L.push(`    trailing_stop = True`);
  L.push(`    trailing_stop_positive = 0.02`);
  L.push(`    trailing_stop_positive_offset = 0.03`);
  L.push(``);
  L.push(`    # Hyperopt parameters`);
  if (hasInd('rsi')) {
    L.push(`    rsi_buy = IntParameter(20, 40, default=30, space='buy')`);
    L.push(`    rsi_sell = IntParameter(60, 80, default=70, space='sell')`);
  }
  if (hasInd('stochastic') || hasInd('kdj')) {
    L.push(`    stoch_buy = IntParameter(10, 30, default=20, space='buy')`);
    L.push(`    stoch_sell = IntParameter(70, 90, default=80, space='sell')`);
  }
  if (hasInd('cci')) {
    L.push(`    cci_buy = IntParameter(-200, -50, default=-100, space='buy')`);
    L.push(`    cci_sell = IntParameter(50, 200, default=100, space='sell')`);
  }
  if (hasInd('williams_r') || hasInd('willr')) {
    L.push(`    willr_buy = IntParameter(-90, -70, default=-80, space='buy')`);
    L.push(`    willr_sell = IntParameter(-30, -10, default=-20, space='sell')`);
  }
  if (has('funding_rate'))
    L.push(`    funding_threshold = DecimalParameter(0.005, 0.1, default=0.01, space='buy')`);
  L.push(``);

  if (any) {
    L.push(`    # AiCoin cached data (updated every 5 min in live mode)`);
    if (has('funding_rate'))     L.push(`    _ac_funding_rate = 0.0`);
    if (has('ls_ratio'))         L.push(`    _ac_ls_ratio = 0.5`);
    if (has('big_orders'))       L.push(`    _ac_whale_signal = 0.0`);
    if (has('open_interest'))    L.push(`    _ac_oi_rising = False`);
    if (has('liquidation_map'))  L.push(`    _ac_liq_bias = 0.0`);
    L.push(`    _ac_last_update = 0.0`);
    L.push(``);
  }

  L.push(`    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:`);

  if (hasInd('rsi')) {
    L.push(`        # RSI`);
    L.push(`        delta = dataframe['close'].diff()`);
    L.push(`        gain = delta.clip(lower=0).rolling(window=14).mean()`);
    L.push(`        loss = (-delta.clip(upper=0)).rolling(window=14).mean()`);
    L.push(`        rs = gain / loss`);
    L.push(`        dataframe['rsi'] = 100 - (100 / (1 + rs))`);
    L.push(``);
  }
  if (hasInd('bb') || hasInd('bollinger')) {
    L.push(`        # Bollinger Bands`);
    L.push(`        dataframe['bb_mid'] = dataframe['close'].rolling(window=20).mean()`);
    L.push(`        bb_std = dataframe['close'].rolling(window=20).std()`);
    L.push(`        dataframe['bb_upper'] = dataframe['bb_mid'] + 2 * bb_std`);
    L.push(`        dataframe['bb_lower'] = dataframe['bb_mid'] - 2 * bb_std`);
    L.push(``);
  }
  if (hasInd('ema')) {
    L.push(`        # EMA`);
    L.push(`        dataframe['ema_fast'] = dataframe['close'].ewm(span=8, adjust=False).mean()`);
    L.push(`        dataframe['ema_slow'] = dataframe['close'].ewm(span=21, adjust=False).mean()`);
    L.push(``);
  }
  if (hasInd('sma')) {
    L.push(`        # SMA`);
    L.push(`        dataframe['sma_short'] = dataframe['close'].rolling(window=10).mean()`);
    L.push(`        dataframe['sma_long'] = dataframe['close'].rolling(window=50).mean()`);
    L.push(``);
  }
  if (hasInd('macd')) {
    L.push(`        # MACD`);
    L.push(`        ema12 = dataframe['close'].ewm(span=12, adjust=False).mean()`);
    L.push(`        ema26 = dataframe['close'].ewm(span=26, adjust=False).mean()`);
    L.push(`        dataframe['macd'] = ema12 - ema26`);
    L.push(`        dataframe['macd_signal'] = dataframe['macd'].ewm(span=9, adjust=False).mean()`);
    L.push(`        dataframe['macd_hist'] = dataframe['macd'] - dataframe['macd_signal']`);
    L.push(``);
  }
  if (hasInd('stochastic') || hasInd('kdj')) {
    L.push(`        # Stochastic (KDJ)`);
    L.push(`        low14 = dataframe['low'].rolling(window=14).min()`);
    L.push(`        high14 = dataframe['high'].rolling(window=14).max()`);
    L.push(`        dataframe['stoch_k'] = 100 * (dataframe['close'] - low14) / (high14 - low14)`);
    L.push(`        dataframe['stoch_d'] = dataframe['stoch_k'].rolling(window=3).mean()`);
    L.push(`        dataframe['stoch_j'] = 3 * dataframe['stoch_k'] - 2 * dataframe['stoch_d']`);
    L.push(``);
  }
  if (hasInd('atr')) {
    L.push(`        # ATR (Average True Range)`);
    L.push(`        high_low = dataframe['high'] - dataframe['low']`);
    L.push(`        high_close = (dataframe['high'] - dataframe['close'].shift()).abs()`);
    L.push(`        low_close = (dataframe['low'] - dataframe['close'].shift()).abs()`);
    L.push(`        tr = high_low.combine(high_close, max).combine(low_close, max)`);
    L.push(`        dataframe['atr'] = tr.rolling(window=14).mean()`);
    L.push(``);
  }
  if (hasInd('adx')) {
    L.push(`        # ADX (Average Directional Index)`);
    L.push(`        plus_dm = dataframe['high'].diff().clip(lower=0)`);
    L.push(`        minus_dm = (-dataframe['low'].diff()).clip(lower=0)`);
    L.push(`        _tr = (dataframe['high'] - dataframe['low']).combine((dataframe['high'] - dataframe['close'].shift()).abs(), max).combine((dataframe['low'] - dataframe['close'].shift()).abs(), max)`);
    L.push(`        atr14 = _tr.rolling(window=14).mean()`);
    L.push(`        plus_di = 100 * plus_dm.rolling(window=14).mean() / atr14`);
    L.push(`        minus_di = 100 * minus_dm.rolling(window=14).mean() / atr14`);
    L.push(`        dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di)`);
    L.push(`        dataframe['adx'] = dx.rolling(window=14).mean()`);
    L.push(`        dataframe['plus_di'] = plus_di`);
    L.push(`        dataframe['minus_di'] = minus_di`);
    L.push(``);
  }
  if (hasInd('cci')) {
    L.push(`        # CCI (Commodity Channel Index)`);
    L.push(`        tp = (dataframe['high'] + dataframe['low'] + dataframe['close']) / 3`);
    L.push(`        tp_sma = tp.rolling(window=20).mean()`);
    L.push(`        tp_mad = tp.rolling(window=20).apply(lambda x: (x - x.mean()).abs().mean(), raw=True)`);
    L.push(`        dataframe['cci'] = (tp - tp_sma) / (0.015 * tp_mad)`);
    L.push(``);
  }
  if (hasInd('williams_r') || hasInd('willr')) {
    L.push(`        # Williams %R`);
    L.push(`        high14_w = dataframe['high'].rolling(window=14).max()`);
    L.push(`        low14_w = dataframe['low'].rolling(window=14).min()`);
    L.push(`        dataframe['willr'] = -100 * (high14_w - dataframe['close']) / (high14_w - low14_w)`);
    L.push(``);
  }
  if (hasInd('vwap')) {
    L.push(`        # VWAP (approximation using cumulative)`);
    L.push(`        tp_v = (dataframe['high'] + dataframe['low'] + dataframe['close']) / 3`);
    L.push(`        cum_tpv = (tp_v * dataframe['volume']).rolling(window=20).sum()`);
    L.push(`        cum_vol = dataframe['volume'].rolling(window=20).sum()`);
    L.push(`        dataframe['vwap'] = cum_tpv / cum_vol`);
    L.push(``);
  }
  if (hasInd('ichimoku')) {
    L.push(`        # Ichimoku Cloud`);
    L.push(`        nine_high = dataframe['high'].rolling(window=9).max()`);
    L.push(`        nine_low = dataframe['low'].rolling(window=9).min()`);
    L.push(`        dataframe['tenkan'] = (nine_high + nine_low) / 2`);
    L.push(`        twentysix_high = dataframe['high'].rolling(window=26).max()`);
    L.push(`        twentysix_low = dataframe['low'].rolling(window=26).min()`);
    L.push(`        dataframe['kijun'] = (twentysix_high + twentysix_low) / 2`);
    L.push(`        dataframe['senkou_a'] = ((dataframe['tenkan'] + dataframe['kijun']) / 2).shift(26)`);
    L.push(`        fiftytwo_high = dataframe['high'].rolling(window=52).max()`);
    L.push(`        fiftytwo_low = dataframe['low'].rolling(window=52).min()`);
    L.push(`        dataframe['senkou_b'] = ((fiftytwo_high + fiftytwo_low) / 2).shift(26)`);
    L.push(``);
  }
  if (hasInd('volume_sma') || hasInd('volume')) {
    L.push(`        # Volume SMA`);
    L.push(`        dataframe['vol_sma'] = dataframe['volume'].rolling(window=20).mean()`);
  }
  if (hasInd('obv')) {
    L.push(`        # OBV (On Balance Volume)`);
    L.push(`        import numpy as np`);
    L.push(`        obv_sign = np.where(dataframe['close'] > dataframe['close'].shift(), 1, np.where(dataframe['close'] < dataframe['close'].shift(), -1, 0))`);
    L.push(`        dataframe['obv'] = (obv_sign * dataframe['volume']).cumsum()`);
    L.push(`        dataframe['obv_sma'] = dataframe['obv'].rolling(window=20).mean()`);
    L.push(``);
  }

  if (any) {
    L.push(``);
    L.push(`        # AiCoin data columns (default values for backtest)`);
    if (has('funding_rate')) {
      L.push(`        dataframe['funding_rate'] = 0.0`);
      L.push(`        dataframe['funding_extreme'] = 0`);
    }
    if (has('ls_ratio'))         L.push(`        dataframe['ls_ratio'] = 0.5`);
    if (has('big_orders'))       L.push(`        dataframe['whale_signal'] = 0.0`);
    if (has('open_interest'))    L.push(`        dataframe['oi_rising'] = 0`);
    if (has('liquidation_map'))  L.push(`        dataframe['liq_bias'] = 0.0`);
    L.push(``);
    L.push(`        if self.dp and self.dp.runmode.value in ('live', 'dry_run'):`);
    L.push(`            import time`);
    L.push(`            now = time.time()`);
    L.push(`            if now - self._ac_last_update > 300:`);
    L.push(`                self._update_aicoin_data(metadata)`);
    L.push(`                self._ac_last_update = now`);
    L.push(``);
    if (has('funding_rate')) {
      L.push(`            dataframe.iloc[-1, dataframe.columns.get_loc('funding_rate')] = self._ac_funding_rate`);
      L.push(`            t = self.funding_threshold.value`);
      L.push(`            if self._ac_funding_rate > t:`);
      L.push(`                dataframe.iloc[-1, dataframe.columns.get_loc('funding_extreme')] = 1`);
      L.push(`            elif self._ac_funding_rate < -t:`);
      L.push(`                dataframe.iloc[-1, dataframe.columns.get_loc('funding_extreme')] = -1`);
    }
    if (has('ls_ratio'))
      L.push(`            dataframe.iloc[-1, dataframe.columns.get_loc('ls_ratio')] = self._ac_ls_ratio`);
    if (has('big_orders'))
      L.push(`            dataframe.iloc[-1, dataframe.columns.get_loc('whale_signal')] = self._ac_whale_signal`);
    if (has('open_interest'))
      L.push(`            dataframe.iloc[-1, dataframe.columns.get_loc('oi_rising')] = 1 if self._ac_oi_rising else 0`);
    if (has('liquidation_map'))
      L.push(`            dataframe.iloc[-1, dataframe.columns.get_loc('liq_bias')] = self._ac_liq_bias`);
  }

  L.push(``);
  L.push(`        return dataframe`);
  L.push(``);

  if (any) {
    L.push(`    def _update_aicoin_data(self, metadata: dict):`);
    L.push(`        try:`);
    L.push(`            import sys, os`);
    L.push(`            _sd = os.path.dirname(os.path.abspath(__file__))`);
    L.push(`            if _sd not in sys.path:`);
    L.push(`                sys.path.insert(0, _sd)`);
    L.push(`            from aicoin_data import AiCoinData`);
    L.push(`            ac = AiCoinData(cache_ttl=300)`);
    L.push(`            pair = metadata.get('pair', 'BTC/USDT:USDT')`);
    L.push(`            exchange = self.config.get('exchange', {}).get('name', 'binance')`);
    L.push(``);

    if (has('funding_rate')) {
      L.push(`            try:`);
      L.push(`                self._ac_funding_rate = ac.funding_rate_pct(pair, exchange)`);
      L.push(`                logger.info(f"AiCoin funding rate for {pair}: {self._ac_funding_rate:.4f}%")`);
      L.push(`            except Exception as e:`);
      L.push(`                logger.debug(f"AiCoin funding_rate unavailable: {e}")`);
      L.push(``);
    }
    if (has('ls_ratio')) {
      L.push(`            try:`);
      L.push(`                self._ac_ls_ratio = ac.ls_ratio_norm()`);
      L.push(`                logger.info(f"AiCoin L/S ratio: {self._ac_ls_ratio:.2f}")`);
      L.push(`            except Exception as e:`);
      L.push(`                logger.debug(f"AiCoin ls_ratio unavailable: {e}")`);
      L.push(``);
    }
    if (has('big_orders')) {
      L.push(`            try:`);
      L.push(`                self._ac_whale_signal = ac.whale_signal(pair, exchange)`);
      L.push(`                logger.info(f"AiCoin whale signal for {pair}: {self._ac_whale_signal:.2f}")`);
      L.push(`            except Exception as e:`);
      L.push(`                logger.debug(f"AiCoin big_orders unavailable: {e}")`);
      L.push(``);
    }
    if (has('open_interest')) {
      L.push(`            try:`);
      L.push(`                self._ac_oi_rising, _chg = ac.oi_trend(pair, exchange)`);
      L.push(`                logger.info(f"AiCoin OI rising={self._ac_oi_rising} change={_chg:.2f}%")`);
      L.push(`            except Exception as e:`);
      L.push(`                logger.debug(f"AiCoin OI unavailable: {e}")`);
      L.push(``);
    }
    if (has('liquidation_map')) {
      L.push(`            try:`);
      L.push(`                self._ac_liq_bias = ac.liq_bias(pair, exchange)`);
      L.push(`                logger.info(f"AiCoin liq bias for {pair}: {self._ac_liq_bias:.2f}")`);
      L.push(`            except Exception as e:`);
      L.push(`                logger.debug(f"AiCoin liquidation_map unavailable: {e}")`);
      L.push(``);
    }

    L.push(`        except ImportError:`);
    L.push(`            logger.warning("aicoin_data module not found. Run ft-deploy.mjs to install.")`);
    L.push(`        except Exception as e:`);
    L.push(`            logger.warning(f"AiCoin data error: {e}")`);
    L.push(``);
  }

  // populate_entry_trend
  const longC = [];
  const shortC = [];

  if (entryLogic && entryLogic.long) {
    longC.push(`(${entryLogic.long})`);
    shortC.push(`(${entryLogic.short || entryLogic.long})`);
  } else {
    if (hasInd('rsi')) {
      longC.push("(dataframe['rsi'] < self.rsi_buy.value)");
      shortC.push("(dataframe['rsi'] > self.rsi_sell.value)");
    }
    if (hasInd('ema')) {
      longC.push("(dataframe['ema_fast'] > dataframe['ema_slow'])");
      shortC.push("(dataframe['ema_fast'] < dataframe['ema_slow'])");
    }
    if (hasInd('sma')) {
      longC.push("(dataframe['sma_short'] > dataframe['sma_long'])");
      shortC.push("(dataframe['sma_short'] < dataframe['sma_long'])");
    }
    if (hasInd('macd')) {
      longC.push("(dataframe['macd'] > dataframe['macd_signal'])");
      shortC.push("(dataframe['macd'] < dataframe['macd_signal'])");
    }
    if (hasInd('stochastic') || hasInd('kdj')) {
      longC.push("(dataframe['stoch_k'] < self.stoch_buy.value)");
      shortC.push("(dataframe['stoch_k'] > self.stoch_sell.value)");
    }
    if (hasInd('bb') || hasInd('bollinger')) {
      longC.push("(dataframe['close'] < dataframe['bb_lower'])");
      shortC.push("(dataframe['close'] > dataframe['bb_upper'])");
    }
    if (hasInd('cci')) {
      longC.push("(dataframe['cci'] < self.cci_buy.value)");
      shortC.push("(dataframe['cci'] > self.cci_sell.value)");
    }
    if (hasInd('williams_r') || hasInd('willr')) {
      longC.push("(dataframe['willr'] < self.willr_buy.value)");
      shortC.push("(dataframe['willr'] > self.willr_sell.value)");
    }
    if (hasInd('adx')) {
      longC.push("(dataframe['adx'] > 20) & (dataframe['plus_di'] > dataframe['minus_di'])");
      shortC.push("(dataframe['adx'] > 20) & (dataframe['minus_di'] > dataframe['plus_di'])");
    }
    if (hasInd('ichimoku')) {
      longC.push("(dataframe['close'] > dataframe['senkou_a']) & (dataframe['close'] > dataframe['senkou_b'])");
      shortC.push("(dataframe['close'] < dataframe['senkou_a']) & (dataframe['close'] < dataframe['senkou_b'])");
    }
    if (hasInd('vwap')) {
      longC.push("(dataframe['close'] < dataframe['vwap'])");
      shortC.push("(dataframe['close'] > dataframe['vwap'])");
    }
    if (hasInd('obv')) {
      longC.push("(dataframe['obv'] > dataframe['obv_sma'])");
      shortC.push("(dataframe['obv'] < dataframe['obv_sma'])");
    }
    if (hasInd('volume_sma') || hasInd('volume')) {
      longC.push("(dataframe['volume'] > dataframe['vol_sma'] * 0.5)");
      shortC.push("(dataframe['volume'] > dataframe['vol_sma'] * 0.5)");
    }
    if (longC.length === 0) {
      longC.push("(dataframe['volume'] > 0)");
      shortC.push("(dataframe['volume'] > 0)");
    }
  }

  if (has('funding_rate'))     { longC.push("(dataframe['funding_extreme'] <= 0)");  shortC.push("(dataframe['funding_extreme'] >= 0)"); }
  if (has('ls_ratio'))         { longC.push("(dataframe['ls_ratio'] <= 0.55)");      shortC.push("(dataframe['ls_ratio'] >= 0.45)"); }
  if (has('big_orders'))       { longC.push("(dataframe['whale_signal'] >= -0.3)");  shortC.push("(dataframe['whale_signal'] <= 0.3)"); }
  if (has('liquidation_map'))  { longC.push("(dataframe['liq_bias'] >= -0.3)");      shortC.push("(dataframe['liq_bias'] <= 0.3)"); }

  const doLong = direction === 'long' || direction === 'both';
  const doShort = direction === 'short' || direction === 'both';

  L.push(`    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:`);
  if (doLong) {
    L.push(`        dataframe.loc[`);
    longC.forEach((c, i) => L.push(`            ${c}${i < longC.length - 1 ? ' &' : ','}`));
    L.push(`            'enter_long'] = 1`);
    L.push(``);
  }
  if (doShort) {
    L.push(`        dataframe.loc[`);
    shortC.forEach((c, i) => L.push(`            ${c}${i < shortC.length - 1 ? ' &' : ','}`));
    L.push(`            'enter_short'] = 1`);
    L.push(``);
  }
  L.push(`        return dataframe`);
  L.push(``);

  L.push(`    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:`);
  if (exitLogic && exitLogic.long) {
    if (doLong) {
      L.push(`        dataframe.loc[`);
      L.push(`            (${exitLogic.long}),`);
      L.push(`            'exit_long'] = 1`);
    }
    if (doShort) {
      L.push(`        dataframe.loc[`);
      L.push(`            (${exitLogic.short || exitLogic.long}),`);
      L.push(`            'exit_short'] = 1`);
    }
  } else {
    if (hasInd('rsi')) {
      if (doLong) {
        L.push(`        dataframe.loc[`);
        L.push(`            (dataframe['rsi'] > 70),`);
        L.push(`            'exit_long'] = 1`);
      }
      if (doShort) {
        L.push(`        dataframe.loc[`);
        L.push(`            (dataframe['rsi'] < 30),`);
        L.push(`            'exit_short'] = 1`);
      }
    } else if (hasInd('stochastic') || hasInd('kdj')) {
      if (doLong) {
        L.push(`        dataframe.loc[`);
        L.push(`            (dataframe['stoch_k'] > 80),`);
        L.push(`            'exit_long'] = 1`);
      }
      if (doShort) {
        L.push(`        dataframe.loc[`);
        L.push(`            (dataframe['stoch_k'] < 20),`);
        L.push(`            'exit_short'] = 1`);
      }
    } else if (hasInd('cci')) {
      if (doLong) {
        L.push(`        dataframe.loc[`);
        L.push(`            (dataframe['cci'] > 150),`);
        L.push(`            'exit_long'] = 1`);
      }
      if (doShort) {
        L.push(`        dataframe.loc[`);
        L.push(`            (dataframe['cci'] < -150),`);
        L.push(`            'exit_short'] = 1`);
      }
    } else if (hasInd('macd')) {
      if (doLong) {
        L.push(`        dataframe.loc[`);
        L.push(`            (dataframe['macd'] < dataframe['macd_signal']),`);
        L.push(`            'exit_long'] = 1`);
      }
      if (doShort) {
        L.push(`        dataframe.loc[`);
        L.push(`            (dataframe['macd'] > dataframe['macd_signal']),`);
        L.push(`            'exit_short'] = 1`);
      }
    } else {
      L.push(`        dataframe.loc[`);
      L.push(`            (dataframe['volume'] > 0),  # exits handled by ROI/stoploss`);
      L.push(`            'exit_long'] = 0  # placeholder`);
      if (doShort) {
        L.push(`        dataframe.loc[`);
        L.push(`            (dataframe['volume'] > 0),`);
        L.push(`            'exit_short'] = 0`);
      }
    }
  }
  L.push(`        return dataframe`);
  L.push(``);

  return L.join('\n');
}

// 极简策略, 给 host 模式 deploy 没指定 strategy 时兜底.
export const SAMPLE_STRATEGY = `# Sample RSI + EMA strategy for Freqtrade
# Uses pure pandas — no TA-Lib C library required
from freqtrade.strategy import IStrategy
from pandas import DataFrame


class SampleStrategy(IStrategy):
    INTERFACE_VERSION = 3
    timeframe = '5m'
    can_short = True

    minimal_roi = {"0": 0.05, "30": 0.03, "60": 0.02, "120": 0.01}

    stoploss = -0.03
    trailing_stop = True
    trailing_stop_positive = 0.01
    trailing_stop_positive_offset = 0.02

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # RSI (pure pandas, no talib)
        delta = dataframe['close'].diff()
        gain = delta.clip(lower=0).rolling(window=14).mean()
        loss = (-delta.clip(upper=0)).rolling(window=14).mean()
        rs = gain / loss
        dataframe['rsi'] = 100 - (100 / (1 + rs))

        # EMA (pure pandas)
        dataframe['ema_fast'] = dataframe['close'].ewm(span=8, adjust=False).mean()
        dataframe['ema_slow'] = dataframe['close'].ewm(span=21, adjust=False).mean()
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (dataframe['rsi'] < 35) &
            (dataframe['ema_fast'] > dataframe['ema_slow']) &
            (dataframe['volume'] > 0),
            'enter_long'] = 1
        dataframe.loc[
            (dataframe['rsi'] > 65) &
            (dataframe['ema_fast'] < dataframe['ema_slow']) &
            (dataframe['volume'] > 0),
            'enter_short'] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (dataframe['rsi'] > 70),
            'exit_long'] = 1
        dataframe.loc[
            (dataframe['rsi'] < 30),
            'exit_short'] = 1
        return dataframe
`;
