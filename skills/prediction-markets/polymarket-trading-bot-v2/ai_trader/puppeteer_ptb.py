"""
通过 Puppeteer 提取 Price to Beat
"""
import subprocess

def get_price_to_beat_puppeteer(slug):
    """用 Puppeteer 从页面提取 Price to Beat"""
    try:
        script_path = '/root/.openclaw/workspace/polymarket-arb-bot/get_ptb_puppeteer.js'
        result = subprocess.run(
            ['node', script_path, slug],
            capture_output=True,
            text=True,
            timeout=30  # 增加到 30 秒
        )
        
        if result.returncode == 0:
            output = result.stdout.strip()
            if output and output != 'null' and output != '':
                try:
                    return float(output)
                except:
                    pass
        
        # 打印错误信息用于调试
        if result.stderr:
            print(f"Puppeteer stderr: {result.stderr[:200]}")
            
    except subprocess.TimeoutExpired:
        print(f"Puppeteer 超时: {slug}")
    except Exception as e:
        print(f"Puppeteer 异常: {e}")
    
    return None
