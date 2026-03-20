"""
简化的 Price to Beat 提取 - 直接从 HTML
"""
import requests
import re

def get_price_to_beat_simple(slug):
    """从 HTML 提取 Price to Beat（简化版）"""
    url = f"https://polymarket.com/event/{slug}"
    
    try:
        resp = requests.get(url, timeout=10, headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        })
        
        if resp.status_code == 200:
            # 从 JSON 字段提取
            match = re.search(r'"priceToBeat":([\d.]+)', resp.text)
            if match:
                price = float(match.group(1))
                if 100 < price < 1000000:
                    return price
    except:
        pass
    
    return None
