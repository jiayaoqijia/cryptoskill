"""
使用 OpenClaw browser 工具提取 Price to Beat
"""

def get_price_to_beat_openclaw_direct(slug):
    """用 OpenClaw browser 工具提取"""
    try:
        from browser import browser
        
        url = f"https://polymarket.com/event/{slug}"
        
        # 打开页面
        result = browser(action="open", url=url)
        if not result or 'targetId' not in result:
            return None
        
        target_id = result['targetId']
        
        # 等待加载
        browser(action="act", request={"kind": "wait", "timeMs": 3000}, targetId=target_id)
        
        # 提取价格
        result = browser(
            action="act",
            request={
                "kind": "evaluate",
                "fn": "() => { const el = document.querySelector('#price-chart-container span.text-heading-2xl'); return el ? el.textContent.trim() : null; }"
            },
            targetId=target_id
        )
        
        if result and 'result' in result:
            price_text = result['result']
            if price_text and '$' in price_text:
                price_str = price_text.replace('$', '').replace(',', '')
                return float(price_str)
    except Exception as e:
        print(f"OpenClaw 浏览器提取失败: {e}")
    
    return None
