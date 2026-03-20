#!/usr/bin/env python3
"""
Polymarket 自动交易机器人 v2
核心优化：
1. Playwright 常驻浏览器获取 PTB（可靠准确）
2. 市场开始后立即获取 PTB（不是等到最后 40 秒）
3. 多层 fallback：Playwright -> HTML 正则 -> Binance 开盘价近似
"""
import sys
import time
import json
import re
import requests
from datetime import datetime, timezone, timedelta

sys.path.insert(0, "/root/.openclaw/workspace/polymarket-arb-bot")

from ai_trader.polymarket_api import get_current_markets
from ai_analyze_v2 import analyze_and_decide


# ====== PTB 获取：多层策略 ======

def get_ptb_from_api(slug):
    """方案0: 已结束的市场从 API 直接拿（秒级）"""
    try:
        resp = requests.get(
            f"https://gamma-api.polymarket.com/events?slug={slug}", timeout=5
        )
        if resp.status_code == 200:
            events = resp.json()
            if events:
                meta = events[0].get("eventMetadata", {})
                ptb = meta.get("priceToBeat")
                if ptb:
                    return float(ptb)
    except:
        pass
    return None


def get_ptb_from_html(slug):
    """方案1: 从 SSR HTML 的 __NEXT_DATA__ 提取（2-3 秒）"""
    url = f"https://polymarket.com/event/{slug}"
    try:
        resp = requests.get(url, timeout=8, headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        })
        if resp.status_code != 200:
            return None
        
        html = resp.text
        
        # 找 __NEXT_DATA__ 中与当前 slug 关联的 PTB
        next_match = re.search(
            r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.DOTALL
        )
        if next_match:
            data = json.loads(next_match.group(1))
            queries = (
                data.get("props", {})
                .get("pageProps", {})
                .get("dehydratedState", {})
                .get("queries", [])
            )
            for q in queries:
                d = q.get("state", {}).get("data", {})
                if isinstance(d, dict) and d.get("slug") == slug:
                    meta = d.get("eventMetadata", {})
                    ptb = meta.get("priceToBeat")
                    if ptb:
                        return float(ptb)

        # Fallback: 页面中 slug 附近找 priceToBeat
        for m in re.finditer(re.escape(slug), html):
            chunk = html[m.start(): m.start() + 2000]
            ptb_m = re.search(r'"priceToBeat":([\d.]+)', chunk)
            if ptb_m:
                val = float(ptb_m.group(1))
                if val > 100:
                    return val

    except Exception as e:
        print(f"  HTML 提取失败: {e}")
    return None


def get_ptb_from_playwright(slug, timeout_ms=12000):
    """方案2: Playwright 浏览器提取（最可靠，8-12 秒）"""
    try:
        from ai_trader.playwright_ptb import get_price_to_beat_playwright
        return get_price_to_beat_playwright(slug, timeout_ms=timeout_ms)
    except Exception as e:
        print(f"  Playwright 提取失败: {e}")
    return None


def get_ptb_from_binance(coin, ts):
    """方案3: Binance 开盘价作为近似值（误差 < $5，0.5 秒）"""
    symbol = f"{coin}USDT"
    try:
        resp = requests.get(
            "https://api.binance.com/api/v3/klines",
            params={"symbol": symbol, "interval": "1m", "startTime": ts * 1000, "limit": 1},
            timeout=3,
        )
        if resp.status_code == 200:
            kline = resp.json()[0]
            open_price = float(kline[1])
            print(f"  ⚠️ 使用 Binance 近似 PTB: ${open_price:,.2f} (可能有 <$5 误差)")
            return open_price
    except:
        pass
    return None


def get_price_to_beat(slug, coin="BTC"):
    """多层获取 PTB"""
    ts = int(slug.split("-")[-1])
    
    # 0. API 直接获取（已结束的市场）
    ptb = get_ptb_from_api(slug)
    if ptb:
        print(f"  ✅ PTB=${ptb:,.2f} (API)")
        return ptb
    
    # 1. HTML SSR
    ptb = get_ptb_from_html(slug)
    if ptb:
        print(f"  ✅ PTB=${ptb:,.2f} (HTML)")
        return ptb
    
    # 2. Playwright
    ptb = get_ptb_from_playwright(slug)
    if ptb:
        return ptb  # playwright_ptb.py 自己会打印
    
    # 3. Binance 近似
    return get_ptb_from_binance(coin, ts)


# ====== 监控主循环 ======

class MarketTracker:
    def __init__(self):
        self.tracked = {}  # slug -> market info
        self.ptb_cache = {}  # slug -> PTB value
        self.analyzed = set()  # 已分析的 slug
    
    def update_markets(self):
        """更新市场列表"""
        markets = get_current_markets()
        now = datetime.now(timezone.utc)
        
        for market in markets:
            slug = market["slug"]
            
            if slug not in self.tracked:
                self.tracked[slug] = market
                end_dt = datetime.fromisoformat(
                    market["end_time"].replace("Z", "+00:00")
                )
                remaining = (end_dt - now).total_seconds()
                print(f"\n🆕 新市场: {market['coin']} | {slug}")
                print(f"   结束: {end_dt.strftime('%H:%M:%S')} UTC | 剩余: {remaining:.0f}s")
                
                # 市场一出现就尝试获取 PTB
                if slug not in self.ptb_cache:
                    print(f"   📡 提前获取 PTB...")
                    ptb = get_price_to_beat(slug, market["coin"])
                    if ptb:
                        self.ptb_cache[slug] = ptb
            else:
                # 更新赔率
                self.tracked[slug]["up_odds"] = market["up_odds"]
                self.tracked[slug]["down_odds"] = market["down_odds"]
        
        return markets
    
    def check_trigger(self):
        """检查是否有市场需要分析"""
        now = datetime.now(timezone.utc)
        
        for slug, market in list(self.tracked.items()):
            if slug in self.analyzed:
                continue
            
            end_dt = datetime.fromisoformat(
                market["end_time"].replace("Z", "+00:00")
            )
            remaining = (end_dt - now).total_seconds()
            
            # 结束前 40 秒触发分析
            if 20 < remaining <= 42:
                self.analyzed.add(slug)
                self.process_market(slug, market, remaining)
        
        # 清理旧数据
        for slug in list(self.tracked.keys()):
            end_dt = datetime.fromisoformat(
                self.tracked[slug]["end_time"].replace("Z", "+00:00")
            )
            if (now - end_dt).total_seconds() > 60:
                del self.tracked[slug]
                self.ptb_cache.pop(slug, None)
    
    def process_market(self, slug, market, remaining):
        """处理单个市场"""
        coin = market["coin"]
        up_odds = market["up_odds"]
        down_odds = market["down_odds"]
        
        # 计算市场时间范围（ET 时区）
        end_dt = datetime.fromisoformat(market["end_time"].replace("Z", "+00:00"))
        start_dt = end_dt - timedelta(minutes=5)
        et_offset = timedelta(hours=-5)  # ET = UTC-5
        start_et = start_dt + et_offset
        end_et = end_dt + et_offset
        time_range = f"{start_et.strftime('%b %-d, %-I:%M')}-{end_et.strftime('%-I:%M%p')} ET"
        
        print(f"\n{'='*60}")
        print(f"🔔 触发分析: {coin} | {time_range}")
        
        # 获取 PTB（优先用缓存）
        ptb = self.ptb_cache.get(slug)
        if not ptb:
            print("  📡 PTB 未缓存，实时获取...")
            ptb = get_price_to_beat(slug, coin)
        
        if not ptb:
            print("  ❌ 无法获取 PTB，跳过")
            print(f"{'='*60}\n")
            return
        
        print(f"  💰 PTB: ${ptb:,.2f}")
        print(f"  📊 赔率: UP={up_odds:.3f} DOWN={down_odds:.3f}")
        
        # AI 分析
        should_bet, direction, confidence, details = analyze_and_decide(
            coin, ptb, up_odds, down_odds, slug
        )
        
        print(f"  🤖 AI: {direction} | 置信度: {confidence*100:.0f}%")
        print(f"  📈 位置: {details.get('position_dir','?')}({details.get('position_score',0)}) "
              f"动量: {details.get('momentum_dir','?')}({details.get('momentum_score',0)}) "
              f"ATR: {details.get('diff_in_atr',0):.2f}x")
        print(f"  💵 EV: {details.get('expected_value',0):+.3f} | "
              f"目标赔率: {details.get('target_odds',0):.3f}")
        
        if should_bet:
            print(f"  ✅ 满足下注条件！{details.get('bet_reason','')}")
            # execute_bet(slug, direction, 10)  # 取消注释启用下注
            print(f"  ⚠️ 下注功能关闭（取消注释启用）")
        else:
            print(f"  ❌ 不满足: {details.get('bet_reason','')}")
        
        print(f"{'='*60}\n")


def main():
    print("🤖 Polymarket 交易机器人 v2 启动")
    print("   PTB 策略: API -> HTML -> Playwright -> Binance 近似")
    print()
    
    # 预热 Playwright
    try:
        from ai_trader.playwright_ptb import warmup, shutdown
        warmup()
    except Exception as e:
        print(f"⚠️ Playwright 预热失败: {e}")
    
    tracker = MarketTracker()
    
    try:
        while True:
            try:
                tracker.update_markets()
                tracker.check_trigger()
            except KeyboardInterrupt:
                raise
            except Exception as e:
                print(f"❌ 循环错误: {e}")
            
            time.sleep(2)
    
    except KeyboardInterrupt:
        print("\n⛔ 机器人停止")
    finally:
        try:
            shutdown()
        except:
            pass


if __name__ == "__main__":
    main()
