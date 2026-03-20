"""
浏览器备用方案 - 应对 Cloudflare 拦截
使用 OpenClaw 的 browser 工具
"""
import re

def get_price_to_beat_with_browser(slug):
    """使用浏览器获取 Price to Beat"""
    try:
        # 方案1: 使用 OpenClaw browser 工具
        from browser import browser
        
        url = f"https://polymarket.com/event/{slug}"
        result = browser(
            action="snapshot",
            url=url,
            target="host"
        )
        
        # 从 snapshot 提取 priceToBeat
        if result and 'text' in result:
            match = re.search(r'"priceToBeat":([\d.]+)', result['text'])
            if match:
                price = float(match.group(1))
                if price > 10:
                    return price
    except Exception as e:
        print(f"浏览器方案失败: {e}")
    
    return None

# 在 polymarket_api.py 中使用的备用逻辑
def get_price_to_beat_fallback(slug):
    """
    多层备用方案：
    1. 先用 requests（快速）
    2. 失败则用浏览器（可靠）
    """
    import requests
    
    # 方案1: requests
    try:
        url = f"https://polymarket.com/event/{slug}"
        resp = requests.get(url, timeout=5, headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        })
        if resp.status_code == 200:
            match = re.search(r'"priceToBeat":([\d.]+)', resp.text)
            if match:
                price = float(match.group(1))
                if price > 10:
                    return price
    except:
        pass
    
    # 方案2: 浏览器
    print(f"⚠️  requests 失败，切换到浏览器方案...")
    return get_price_to_beat_with_browser(slug)
