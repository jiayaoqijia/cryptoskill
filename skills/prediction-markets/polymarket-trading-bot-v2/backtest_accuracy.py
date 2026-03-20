#!/usr/bin/env python3
"""回测脚本 - 验证 AI 预测的实际准确率"""
import json
import requests
from datetime import datetime, timezone
from collections import defaultdict

def get_market_result(slug):
    """获取市场最终结果"""
    url = f"https://gamma-api.polymarket.com/events?slug={slug}"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            return None
        
        data = resp.json()
        if not data:
            return None
        
        markets = data[0].get('markets', [])
        if not markets:
            return None
        
        market = markets[0]
        if not market.get('closed'):
            return None
        
        outcomes = json.loads(market['outcomes'])
        prices = json.loads(market['outcomePrices'])
        
        for outcome, price in zip(outcomes, prices):
            if float(price) >= 0.99:
                return outcome.upper()
        
        return None
    except:
        return None

def analyze_decisions():
    """分析决策准确率"""
    with open('logs/decisions_v2.jsonl', 'r') as f:
        decisions = [json.loads(line) for line in f]
    
    print(f"📊 总决策数: {len(decisions)}")
    print(f"⏰ 时间范围: {decisions[0]['timestamp']} 至 {decisions[-1]['timestamp']}\n")
    
    # 按置信度分组
    confidence_groups = {
        '100%': [],
        '90-99%': [],
        '80-89%': [],
        '70-79%': [],
        '60-69%': [],
        '<60%': []
    }
    
    results = []
    checked = 0
    
    for dec in decisions:
        conf = dec['confidence']
        pred_dir = dec['direction']
        slug = dec['slug']
        
        # 跳过测试数据
        if 'test' in slug:
            continue
        
        # 获取实际结果
        actual = get_market_result(slug)
        if actual is None:
            continue
        
        checked += 1
        correct = (actual == pred_dir)
        
        result = {
            'slug': slug,
            'coin': dec['coin'],
            'predicted': pred_dir,
            'actual': actual,
            'correct': correct,
            'confidence': conf,
            'ev': dec['ev'],
            'timestamp': dec['timestamp']
        }
        results.append(result)
        
        # 分组
        if conf == 1.0:
            confidence_groups['100%'].append(result)
        elif conf >= 0.9:
            confidence_groups['90-99%'].append(result)
        elif conf >= 0.8:
            confidence_groups['80-89%'].append(result)
        elif conf >= 0.7:
            confidence_groups['70-79%'].append(result)
        elif conf >= 0.6:
            confidence_groups['60-69%'].append(result)
        else:
            confidence_groups['<60%'].append(result)
    
    print(f"✅ 已验证市场: {checked}/{len([d for d in decisions if 'test' not in d['slug']])}\n")
    
    # 总体准确率
    if results:
        total_correct = sum(1 for r in results if r['correct'])
        total_acc = total_correct / len(results) * 100
        print(f"🎯 总体准确率: {total_correct}/{len(results)} = {total_acc:.1f}%\n")
    
    # 按置信度分析
    print("📈 按置信度分组:")
    for group_name, group_results in confidence_groups.items():
        if not group_results:
            continue
        
        correct = sum(1 for r in group_results if r['correct'])
        total = len(group_results)
        acc = correct / total * 100 if total > 0 else 0
        
        print(f"  {group_name:8s}: {correct:3d}/{total:3d} = {acc:5.1f}%")
    
    # 按币种分析
    print("\n💰 按币种分组:")
    coin_stats = defaultdict(lambda: {'correct': 0, 'total': 0})
    for r in results:
        coin_stats[r['coin']]['total'] += 1
        if r['correct']:
            coin_stats[r['coin']]['correct'] += 1
    
    for coin, stats in sorted(coin_stats.items()):
        acc = stats['correct'] / stats['total'] * 100
        print(f"  {coin}: {stats['correct']}/{stats['total']} = {acc:.1f}%")
    
    # 按方向分析
    print("\n🎲 按预测方向:")
    dir_stats = defaultdict(lambda: {'correct': 0, 'total': 0})
    for r in results:
        dir_stats[r['predicted']]['total'] += 1
        if r['correct']:
            dir_stats[r['predicted']]['correct'] += 1
    
    for direction, stats in sorted(dir_stats.items()):
        acc = stats['correct'] / stats['total'] * 100
        print(f"  {direction:4s}: {stats['correct']}/{stats['total']} = {acc:.1f}%")
    
    # 高置信度 + 高EV 的表现
    print("\n⭐ 高质量信号 (置信度≥80% & EV>0.5):")
    high_quality = [r for r in results if r['confidence'] >= 0.8 and r['ev'] > 0.5]
    if high_quality:
        hq_correct = sum(1 for r in high_quality if r['correct'])
        hq_acc = hq_correct / len(high_quality) * 100
        print(f"  准确率: {hq_correct}/{len(high_quality)} = {hq_acc:.1f}%")
    else:
        print("  无数据")
    
    # 保存详细结果
    with open('logs/backtest_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 详细结果已保存到: logs/backtest_results.json")

if __name__ == '__main__':
    analyze_decisions()
