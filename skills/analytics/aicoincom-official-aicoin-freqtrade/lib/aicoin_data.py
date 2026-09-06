"""AiCoin Data SDK for Freqtrade Strategies (AiCoin Open API v3)
================================================================
Import this in your Freqtrade strategy to pull AiCoin's aggregated market data
from 200+ exchanges:

    from aicoin_data import AiCoinData

    ac = AiCoinData()                              # auto-loads API key from .env
    signal  = ac.whale_signal('BTC/USDT:USDT', 'binance')   # -1..+1
    ls      = ac.ls_ratio_norm()                            # 0..1
    funding = ac.funding_rate_pct('BTC/USDT:USDT', 'binance')  # percent
    bias    = ac.liq_bias('BTC/USDT:USDT', 'binance')          # -1..+1

The high-level helpers above return plain numbers ready to drop into a strategy.
For raw responses use ac.get('<endpoint>', {...}) — see catalog at
https://open.aicoin.com/api/v3/_catalog.

Built-in 5-min cache avoids hammering the API in live mode. In backtest mode
AiCoin real-time data is not available — strategies should fall back to standard
indicators (the helpers raise, strategies catch and use defaults).

Some endpoints need a paid AiCoin subscription — see https://www.aicoin.com/opendata.
"""
import hmac
import hashlib
import base64
import json
import os
import time
import random
import logging
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from urllib.parse import urlencode

logger = logging.getLogger(__name__)

# Freqtrade/CCXT exchange name -> AiCoin market slug (v3 normalizes okx internally).
EXCHANGE_MAP = {
    'binance': 'binance', 'okx': 'okx', 'bybit': 'bybit', 'bitget': 'bitget',
    'gate': 'gate', 'gateio': 'gate', 'htx': 'huobipro', 'huobi': 'huobipro',
    'kucoin': 'kucoin',
}

# Common base ticker -> AiCoin coin_key slug. Anything else is resolved live
# via /coins/search and cached.
COIN_KEY_MAP = {
    'btc': 'bitcoin', 'eth': 'ethereum', 'sol': 'solana', 'xrp': 'ripple',
    'doge': 'dogecoin', 'bnb': 'binancecoin', 'ada': 'cardano', 'ltc': 'litecoin',
    'link': 'chainlink', 'dot': 'polkadot', 'trx': 'tron', 'avax': 'avalanche',
    'sui': 'sui', 'apt': 'aptos', 'ton': 'toncoin', 'near': 'near',
    'op': 'optimism', 'arb': 'arbitrum', 'uni': 'uniswap', 'aave': 'aave',
    'pepe': 'pepe', 'hype': 'hyperliquid', 'wld': 'worldcoin',
}


class AiCoinError(Exception):
    """Raised when the AiCoin API returns an error or is unreachable."""


def ccxt_to_v3(pair: str, exchange: str = 'binance') -> dict:
    """CCXT pair + exchange -> partial v3 identity {market, contract_type, base}.

    'BTC/USDT:USDT' -> {'market': 'binance', 'contract_type': 'perpetual', 'base': 'btc'}
    'BTC/USDT'      -> {'market': 'binance', 'contract_type': 'spot',      'base': 'btc'}

    The coin_key still needs resolving — use AiCoinData._pair() which does both.
    """
    return {
        'market': EXCHANGE_MAP.get(exchange.lower(), exchange.lower()),
        'contract_type': 'perpetual' if ':' in pair else 'spot',
        'base': pair.split('/')[0].lower(),
    }


class AiCoinData:
    """AiCoin Open API v3 client for use inside Freqtrade strategies.

    - HMAC-SHA1 signed requests, 4 X-Aic-* headers (v3 auth).
    - Auto-loads the API key from .env files.
    - Built-in TTL cache (default 5 min) to avoid hammering the API.
    """

    _cache: dict = {}  # shared across instances

    def __init__(self, cache_ttl: int = 300):
        self.cache_ttl = cache_ttl
        self._load_env()
        self._setup_proxy()
        defaults = self._load_defaults()
        self.base = os.environ.get('AICOIN_BASE_URL', 'https://open.aicoin.com')
        self.key = os.environ.get('AICOIN_ACCESS_KEY_ID', defaults.get('accessKeyId', ''))
        self.secret = os.environ.get('AICOIN_ACCESS_SECRET', defaults.get('accessSecret', ''))

    # ── Setup helpers ──

    @staticmethod
    def _load_env():
        for f in (Path('/workspace/.env'),                        # 容器(Hermes/CC entrypoint 注入)
                  Path.home() / '.coinos' / '.env',               # 规范位置(coinos 文件夹), 与 JS loader 对齐
                  Path.cwd() / '.env',
                  Path.home() / '.openclaw' / 'workspace' / '.env',
                  Path.home() / '.openclaw' / '.env'):
            if not f.exists():
                continue
            try:
                for line in f.read_text().splitlines():
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    eq = line.find('=')
                    if eq < 1:
                        continue
                    k, v = line[:eq].strip(), line[eq + 1:].strip()
                    if len(v) >= 2 and v[0] in ('"', "'") and v[-1] == v[0]:
                        v = v[1:-1]
                    os.environ.setdefault(k, v)
            except Exception:
                pass

    @staticmethod
    def _setup_proxy():
        proxy = (os.environ.get('PROXY_URL') or os.environ.get('HTTPS_PROXY')
                 or os.environ.get('https_proxy') or os.environ.get('HTTP_PROXY')
                 or os.environ.get('http_proxy'))
        if proxy and not proxy.startswith('socks'):
            os.environ.setdefault('HTTPS_PROXY', proxy)
            os.environ.setdefault('HTTP_PROXY', proxy)

    @staticmethod
    def _load_defaults() -> dict:
        p = Path(__file__).parent / 'defaults.json'
        try:
            return json.loads(p.read_text()) if p.exists() else {}
        except Exception:
            return {}

    # ── Auth + HTTP ──

    def _auth_headers(self) -> dict:
        nonce = '%016x' % random.getrandbits(64)
        ts = str(int(time.time()))
        s = f'AccessKeyId={self.key}&SignatureNonce={nonce}&Timestamp={ts}'
        h = hmac.new(self.secret.encode(), s.encode(), hashlib.sha1).hexdigest()
        return {
            'X-Aic-AccessKey-Id': self.key,
            'X-Aic-Signature-Nonce': nonce,
            'X-Aic-Timestamp': ts,
            'X-Aic-Signature': base64.b64encode(h.encode()).decode(),
            'User-Agent': 'AiCoin-Freqtrade/2.0',
        }

    def _call(self, method: str, path: str, params: dict = None):
        """Sign and send a v3 request. Returns the envelope's `data`, or raises."""
        full = '/api/v3/' + path.strip('/').replace('api/v3/', '', 1)
        headers = self._auth_headers()
        if method == 'GET':
            clean = {k: (','.join(map(str, v)) if isinstance(v, (list, tuple)) else v)
                     for k, v in (params or {}).items() if v not in (None, '')}
            qs = urlencode(clean)
            req = Request(self.base + full + (('?' + qs) if qs else ''), headers=headers)
        else:
            headers['Content-Type'] = 'application/json'
            req = Request(self.base + full, data=json.dumps(params or {}).encode(),
                          headers=headers, method='POST')
        try:
            with urlopen(req, timeout=30) as resp:
                body = json.loads(resp.read())
        except HTTPError as e:
            try:
                body = json.loads(e.read())
            except Exception:
                body = {}
            err = body.get('error') if isinstance(body.get('error'), dict) else {}
            raise AiCoinError(f"HTTP {e.code}: {err.get('message') or body.get('error') or e.reason}")
        except Exception as e:
            raise AiCoinError(str(e))
        if body.get('ok') is False:
            err = body.get('error') or {}
            raise AiCoinError(err.get('message') or err.get('code') or 'request failed')
        return body.get('data')

    def get(self, path: str, params: dict = None, cache_key: str = None):
        """GET any v3 endpoint. `path` is the bit after /api/v3/ (e.g. 'market/klines')."""
        if cache_key and self.cache_ttl > 0 and cache_key in self._cache:
            ts, data = self._cache[cache_key]
            if time.time() - ts < self.cache_ttl:
                return data
        data = self._call('GET', path, params)
        if cache_key and self.cache_ttl > 0:
            self._cache[cache_key] = (time.time(), data)
        return data

    def post(self, path: str, body: dict = None):
        """POST any v3 endpoint."""
        return self._call('POST', path, body)

    # ── Pair identity ──

    def _resolve_coin_key(self, ticker: str) -> str:
        t = ticker.lower()
        if t in COIN_KEY_MAP:
            return COIN_KEY_MAP[t]
        ck = self._cache.get(f'ck:{t}')
        if ck:
            return ck[1]
        try:
            data = self.get('coins/search', {'query': ticker, 'limit': 5})
            items = (data or {}).get('list') or (data or {}).get('items') or []
            for it in items:
                cand = it.get('coin_key') or it.get('coinKey') or it.get('key')
                if cand:
                    self._cache[f'ck:{t}'] = (time.time(), cand)
                    return cand
        except Exception:
            pass
        return t  # last resort

    def _pair(self, pair: str, exchange: str = 'binance') -> dict:
        """CCXT pair + exchange -> v3 query dict {coin_key, market, contract_type}."""
        v = ccxt_to_v3(pair, exchange)
        return {'coin_key': self._resolve_coin_key(v['base']),
                'market': v['market'], 'contract_type': v['contract_type']}

    # ── Raw data (return the v3 `data` payload) ──

    def coin_ticker(self, coin_keys: str):
        """Real-time prices. coin_keys: 'bitcoin' or 'bitcoin,ethereum'."""
        return self.get('coins/tickers', {'coin_key': coin_keys}, f'ticker:{coin_keys}')

    def klines(self, pair: str, exchange: str = 'binance', interval: str = '1h', limit: int = 100):
        """K-line data for a CCXT pair."""
        q = {**self._pair(pair, exchange), 'interval': interval, 'limit': limit}
        return self.get('market/klines', q, f'kline:{pair}:{interval}:{limit}')

    def funding_rate(self, pair: str, exchange: str = 'binance', limit: int = 20):
        """Funding-rate history (newest first). data.funding_rates[].close is the rate."""
        q = {**self._pair(pair, exchange), 'contract_type': 'perpetual', 'limit': limit}
        return self.get('derivatives/funding-rates', q, f'funding:{pair}:{limit}')

    def long_short_ratio(self):
        """Cross-exchange aggregated long/short ratio summary."""
        return self.get('derivatives/long-short-ratio/summary', cache_key='ls_ratio')

    def big_orders(self, pair: str, exchange: str = 'binance'):
        """Whale resting orders (order-book big bids/asks)."""
        q = self._pair(pair, exchange)
        return self.get('market/big-orders', q, f'big_orders:{pair}')

    def liquidation_map(self, pair: str, exchange: str = 'binance', window: str = '24h'):
        """Liquidation heatmap bucketed by leverage."""
        q = {**self._pair(pair, exchange), 'window': window}
        return self.get('derivatives/liquidations/map', q, f'liqmap:{pair}:{window}')

    def hl_whale_positions(self, coin: str = None):
        """Hyperliquid whale open positions. coin is the HL symbol, e.g. 'BTC'."""
        return self.get('hyperliquid/whales/open-positions',
                        {'coin': coin} if coin else {}, f'hl_whale:{coin}')

    def hl_taker_delta(self, coin: str, interval: str = '1h'):
        """Hyperliquid accumulated taker buy/sell delta."""
        return self.get('hyperliquid/accumulated-taker-delta',
                        {'coin': coin, 'interval': interval}, f'hl_taker:{coin}:{interval}')

    # ── High-level signals (plain numbers, ready for a strategy) ──

    def whale_signal(self, pair: str, exchange: str = 'binance') -> float:
        """Whale order-book pressure as -1 (selling/asks) .. +1 (buying/bids)."""
        data = self.big_orders(pair, exchange)
        items = (data or {}).get('items') or []
        buy = sum(float(o.get('high_turnover', 0) or 0) for o in items if o.get('depth_type') == 'bid')
        sell = sum(float(o.get('high_turnover', 0) or 0) for o in items if o.get('depth_type') == 'ask')
        total = buy + sell
        return (buy - sell) / total if total > 0 else 0.0

    def ls_ratio_norm(self) -> float:
        """Long/short ratio normalized to 0..1 ( >0.5 = more longs )."""
        data = self.long_short_ratio()
        detail = (((data or {}).get('summary') or {}).get('detail')) or {}
        ratio = float(detail.get('last', 1.0) or 1.0)
        return max(0.0, min(1.0, ratio / (1.0 + ratio)))

    def funding_rate_pct(self, pair: str, exchange: str = 'binance') -> float:
        """Latest funding rate as a percentage (e.g. 0.01 = 0.01%)."""
        data = self.funding_rate(pair, exchange, limit=5)
        rows = (data or {}).get('funding_rates') or []
        if not rows:
            raise AiCoinError('no funding-rate data')
        # v3 时序是升序(oldest-first,与 K 线一致),rows[0] 是窗口内**最旧**的一条。
        # 别假设顺序 —— 按时间字段取最大那条作为"最新";取不到时间字段才退回 rows[-1](升序末尾)。
        def _ts(r):
            for k in ('close_time', 'time', 'timestamp', 'ts', 'create_time', 'fundingTime'):
                v = r.get(k)
                if v is not None:
                    try:
                        return float(v)
                    except (TypeError, ValueError):
                        pass
            return None
        latest = max(rows, key=lambda r: (_ts(r) if _ts(r) is not None else float('-inf'))) \
            if any(_ts(r) is not None for r in rows) else rows[-1]
        return float(latest.get('close', 0) or 0) * 100

    def oi_trend(self, pair: str, exchange: str = 'binance'):
        """(is_rising, change_pct) for aggregated open interest.

        NOTE: v3's aggregated OI history is not wired yet (returns 501). This
        raises until the data source is connected — strategies should fall back.
        """
        q = {**self._pair(pair, exchange), 'interval': '15m', 'limit': 10}
        data = self.get('derivatives/open-interest/stablecoin-margin', q)
        rows = data if isinstance(data, list) else (data or {}).get('list') or []
        if len(rows) < 2:
            raise AiCoinError('no open-interest data')
        first = float(rows[0].get('open_interest', rows[0].get('value', 0)) or 0)
        last = float(rows[-1].get('open_interest', rows[-1].get('value', 0)) or 0)
        change = (last - first) / first * 100 if first > 0 else 0.0
        return (change > 3.0, change)

    def liq_bias(self, pair: str, exchange: str = 'binance') -> float:
        """Liquidation-map directional bias: -1 (long liqs dominate) .. +1 (short liqs dominate)."""
        data = self.liquidation_map(pair, exchange)
        data_map = (((data or {}).get('map') or {}).get('data_map')) or {}
        long_total = short_total = 0.0
        for bucket in data_map.values():
            long_total += sum(float(r[2]) for r in bucket.get('long', []) if len(r) >= 3)
            short_total += sum(float(r[2]) for r in bucket.get('short', []) if len(r) >= 3)
        total = long_total + short_total
        return (short_total - long_total) / total if total > 0 else 0.0

    # ── Cache ──

    def clear_cache(self):
        self._cache.clear()

    def set_cache_ttl(self, seconds: int):
        self.cache_ttl = seconds
