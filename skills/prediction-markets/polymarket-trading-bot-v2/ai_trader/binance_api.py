"""
币安 API 数据采集模块
"""
import requests
import time
from datetime import datetime

BINANCE_API = "https://api.binance.com"

def get_klines(symbol, interval, limit=10):
    """获取 K线数据"""
    url = f"{BINANCE_API}/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    try:
        resp = requests.get(url, params=params, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            # 返回格式: [open_time, open, high, low, close, volume, ...]
            return [{
                'time': int(k[0]),
                'open': float(k[1]),
                'high': float(k[2]),
                'low': float(k[3]),
                'close': float(k[4]),
                'volume': float(k[5])
            } for k in data]
    except Exception as e:
        print(f"获取K线失败: {e}")
    return []

def get_current_price(symbol):
    """获取实时价格"""
    url = f"{BINANCE_API}/api/v3/ticker/price"
    try:
        resp = requests.get(url, params={"symbol": symbol}, timeout=5)
        if resp.status_code == 200:
            return float(resp.json()['price'])
    except:
        pass
    return None

def get_24h_stats(symbol):
    """获取24小时统计"""
    url = f"{BINANCE_API}/api/v3/ticker/24hr"
    try:
        resp = requests.get(url, params={"symbol": symbol}, timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            return {
                'volume': float(data['volume']),
                'quote_volume': float(data['quoteVolume']),
                'price_change_pct': float(data['priceChangePercent'])
            }
    except:
        pass
    return None
