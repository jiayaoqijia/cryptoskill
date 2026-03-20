"""
使用 OpenClaw 浏览器提取 Price to Beat
"""
import subprocess
import json

def get_price_to_beat_openclaw(slug):
    """用 OpenClaw 浏览器提取 Price to Beat"""
    url = f"https://polymarket.com/event/{slug}"
    
    try:
        # 使用 openclaw CLI
        result = subprocess.run([
            'openclaw', 'browser', 'eval',
            '--url', url,
            '--wait', '3000',
            '--expr', "document.querySelector('#price-chart-container span.text-heading-2xl')?.textContent?.trim()"
        ], capture_output=True, text=True, timeout=15)
        
        if result.returncode == 0:
            output = result.stdout.strip()
            # 解析价格
            if output and '$' in output:
                price_str = output.replace('$', '').replace(',', '')
                return float(price_str)
    except:
        pass
    
    return None
