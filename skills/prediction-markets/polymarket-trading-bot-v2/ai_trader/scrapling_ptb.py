"""
使用 Scrapling 提取 Price to Beat
"""
from scrapling import Fetcher

def get_price_to_beat_scrapling(slug):
    """用 Scrapling 提取实时 Price to Beat"""
    url = f"https://polymarket.com/event/{slug}"
    
    try:
        fetcher = Fetcher()
        page = fetcher.get(url)
        
        # 提取 #price-chart-container 里的 text-heading-2xl 元素
        element = page.css('#price-chart-container span.text-heading-2xl::text').get()
        
        if element:
            # 解析价格
            price_text = element.strip()
            if '$' in price_text:
                price_str = price_text.replace('$', '').replace(',', '')
                return float(price_str)
    except Exception as e:
        print(f"Scrapling 提取失败: {e}")
    
    return None
