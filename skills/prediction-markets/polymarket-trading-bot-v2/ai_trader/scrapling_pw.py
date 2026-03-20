"""
使用 Scrapling Playwright 引擎提取 Price to Beat
"""
from scrapling.fetchers import PlaywrightFetcher

def get_price_to_beat_scrapling_pw(slug):
    """用 Scrapling Playwright 提取实时 Price to Beat"""
    url = f"https://polymarket.com/event/{slug}"
    
    try:
        fetcher = PlaywrightFetcher(headless=True)
        page = fetcher.get(url, wait_selector='#price-chart-container')
        
        # 提取价格
        element = page.css('#price-chart-container span.text-heading-2xl::text').get()
        
        if element:
            price_text = element.strip()
            if '$' in price_text:
                price_str = price_text.replace('$', '').replace(',', '')
                return float(price_str)
    except Exception as e:
        print(f"Scrapling PW 提取失败: {e}")
    finally:
        try:
            fetcher.close()
        except:
            pass
    
    return None
