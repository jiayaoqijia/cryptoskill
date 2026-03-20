"""
使用 Playwright 常驻浏览器获取 Price to Beat
核心优化：浏览器只启动一次，后续请求直接导航，速度 3-5 秒
"""
import time
import re
import atexit
from datetime import datetime, timezone

# 全局浏览器实例
_browser = None
_context = None
_page = None
_playwright = None


def _ensure_browser():
    """确保浏览器已启动（懒加载，只启动一次）"""
    global _browser, _context, _page, _playwright
    
    if _page is not None:
        try:
            _page.evaluate("1+1")  # 检查页面是否还活着
            return _page
        except:
            _cleanup()
    
    from playwright.sync_api import sync_playwright
    _playwright = sync_playwright().start()
    _browser = _playwright.chromium.launch(
        headless=True,
        args=[
            "--no-sandbox",
            "--disable-gpu",
            "--disable-dev-shm-usage",
            "--disable-images",  # 不加载图片，加速
        ]
    )
    _context = _browser.new_context(
        user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        viewport={"width": 1280, "height": 720}
    )
    _page = _context.new_page()
    
    # 拦截不必要的资源，加速加载（保留 CSS 和 JS）
    def _block_resources(route):
        rt = route.request.resource_type
        url = route.request.url
        if rt in ("image", "media", "font"):
            route.abort()
        elif any(x in url for x in [
            "analytics", "segment", "hotjar", "sentry", "gtag",
            "google-analytics", "facebook", "twitter.com/i/",
            "intercom", "amplitude", "mixpanel", "datadog",
        ]):
            route.abort()
        else:
            route.continue_()
    
    _page.route("**/*", _block_resources)
    
    # 注册退出清理
    atexit.register(_cleanup)
    
    return _page


def _cleanup():
    """清理浏览器资源（安全退出，忽略 EPIPE 等错误）"""
    global _browser, _context, _page, _playwright
    import signal
    # 忽略 SIGPIPE
    old_handler = signal.signal(signal.SIGPIPE, signal.SIG_IGN) if hasattr(signal, 'SIGPIPE') else None
    try:
        if _browser:
            try:
                _browser.close()
            except:
                pass
        if _playwright:
            try:
                _playwright.stop()
            except:
                pass
    except:
        pass
    finally:
        if old_handler is not None:
            try:
                signal.signal(signal.SIGPIPE, old_handler)
            except:
                pass
    _browser = _context = _page = _playwright = None


def get_price_to_beat_playwright(slug, timeout_ms=12000):
    """
    用 Playwright 获取 Price to Beat
    
    首次调用约 12-15 秒（启动浏览器）
    后续调用约 3-6 秒（复用浏览器）
    
    Returns: float 或 None
    """
    url = f"https://polymarket.com/event/{slug}"
    
    try:
        page = _ensure_browser()
        
        t0 = time.time()
        page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
        
        # 等待 price-chart-container 出现（attached 即可，不要求 visible）
        page.wait_for_selector("#price-chart-container", state="attached", timeout=min(timeout_ms, 8000))
        
        # 等 JS 渲染 PTB 值
        time.sleep(1)
        
        # 提取 "Price to beat" 旁边的价格
        ptb_text = page.evaluate(r"""() => {
            const container = document.getElementById('price-chart-container');
            if (!container) return null;
            
            // 方案1: 找 "Price to beat" 标签旁边的价格
            const spans = container.querySelectorAll('span');
            for (let i = 0; i < spans.length; i++) {
                if (spans[i].textContent.trim().toLowerCase().includes('price to beat')) {
                    // 下一个 span 就是价格
                    for (let j = i + 1; j < Math.min(i + 5, spans.length); j++) {
                        const text = spans[j].textContent.trim();
                        if (text.startsWith('$') && /\d{2,}/.test(text)) {
                            return text;
                        }
                    }
                }
            }
            
            // 方案2: 找 class 包含 tracking-wide font-[620] 的 span
            const ptbEl = container.querySelector('span[class*="tracking-wide"][class*="font-"]');
            if (ptbEl) {
                const text = ptbEl.textContent.trim();
                if (text.startsWith('$')) return text;
            }
            
            return null;
        }""")
        
        elapsed = time.time() - t0
        
        if ptb_text:
            # 解析 "$70,184.48" -> 70184.48
            price_str = ptb_text.replace("$", "").replace(",", "").strip()
            price = float(price_str)
            print(f"✅ PTB={price:.2f} (Playwright, {elapsed:.1f}s)")
            return price
        else:
            print(f"⚠️ PTB 未找到 (Playwright, {elapsed:.1f}s)")
            return None
            
    except Exception as e:
        print(f"❌ Playwright 错误: {e}")
        # 出错时清理浏览器，下次重新启动
        _cleanup()
        return None


def warmup():
    """预热浏览器（在 monitor 启动时调用）"""
    print("🔥 预热 Playwright 浏览器...")
    t0 = time.time()
    try:
        _ensure_browser()
        print(f"✅ 浏览器就绪 ({time.time()-t0:.1f}s)")
    except Exception as e:
        print(f"❌ 预热失败: {e}")


def shutdown():
    """关闭浏览器"""
    _cleanup()
    print("🔒 浏览器已关闭")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        slug = sys.argv[1]
    else:
        now_ts = int(datetime.now(timezone.utc).timestamp())
        base_5m = (now_ts // 300) * 300
        slug = f"btc-updown-5m-{base_5m}"
    
    print(f"测试 slug: {slug}")
    
    # 第一次调用（含启动）
    t0 = time.time()
    ptb1 = get_price_to_beat_playwright(slug)
    print(f"第一次: PTB={ptb1}, 耗时={time.time()-t0:.1f}s")
    
    # 第二次调用（复用浏览器）
    t0 = time.time()
    ptb2 = get_price_to_beat_playwright(slug)
    print(f"第二次: PTB={ptb2}, 耗时={time.time()-t0:.1f}s")
    
    shutdown()
