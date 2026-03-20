"""
Polymarket 数据采集模块 - 使用浏览器方案
"""
import json
import requests
from datetime import datetime, timezone

"""
Polymarket 数据采集模块
"""
import json
import re
import requests
from datetime import datetime, timezone

def get_price_to_beat_browser(slug):
    """从 HTML 提取 Price to Beat"""
    url = f"https://polymarket.com/event/{slug}"
    try:
        resp = requests.get(url, timeout=10, headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        })
        if resp.status_code == 200:
            match = re.search(r'"priceToBeat":([\d.]+)', resp.text)
            if match:
                price = float(match.group(1))
                if 100 < price < 1000000:
                    return price
    except:
        pass
    return None

def get_current_markets():
    """获取当前进行中的 5分钟市场"""
    now_ts = int(datetime.now(timezone.utc).timestamp())
    base_5m = (now_ts // 300) * 300
    
    markets = []
    for prefix in ['btc-updown-5m', 'eth-updown-5m']:
        slug = f"{prefix}-{base_5m}"
        coin = 'BTC' if 'btc' in prefix else 'ETH'
        
        try:
            resp = requests.get(
                f"https://gamma-api.polymarket.com/events?slug={slug}",
                timeout=3
            )
            if resp.status_code == 200:
                events = resp.json()
                if events and not events[0].get('closed'):
                    event = events[0]
                    market = event['markets'][0]
                    
                    # 获取 Price to Beat
                    ptb = get_price_to_beat_browser(slug)
                    
                    prices = json.loads(market['outcomePrices'])
                    
                    markets.append({
                        'slug': slug,
                        'coin': coin,
                        'end_time': event['endDate'],
                        'price_to_beat': ptb,
                        'up_odds': float(prices[0]),
                        'down_odds': float(prices[1])
                    })
        except:
            pass
    
    return markets
