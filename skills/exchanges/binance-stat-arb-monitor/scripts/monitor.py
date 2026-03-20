#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Binance 统计套利监控脚本
计算 ETH/BTC 永续合约比率的 z-score，生成交易信号并推送
"""
import os
import sys
import json
import logging
import datetime
from pathlib import Path

# 添加脚本目录到路径
sys.path.insert(0, str(Path(__file__).parent))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_config():
    """加载配置"""
    config_path = Path(__file__).parent.parent / "config.json"
    if not config_path.exists():
        config_path = Path(__file__).parent.parent / "config.example.json"
        logger.warning(f"config.json 不存在，使用模板: {config_path}")
    
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    """主函数"""
    logger.info("=" * 60)
    logger.info("🚀 Binance 统计套利监控启动")
    logger.info("=" * 60)
    
    # 加载配置
    try:
        config = load_config()
    except Exception as e:
        logger.error(f"❌ 配置加载失败: {e}")
        return
    
    # 导入模块（使用直接导入）
    import fetcher
    import calculator
    import formatter
    import storage
    import notifier
    
    get_market_data = fetcher.get_market_data
    determine_signal = calculator.determine_signal
    format_signal_message = formatter.format_signal_message
    format_signal_json = formatter.format_signal_json
    send_notification = notifier.send_notification
    save_signal = storage.save_signal
    
    strategy = config["strategy"]
    logger.info(f"监控交易对: {strategy['symbol1']} / {strategy['symbol2']}")
    logger.info(f"回看周期: {strategy['lookback_period']} {strategy['interval']}")
    logger.info(f"开仓阈值: ±{strategy['entry_threshold']}")
    logger.info("-" * 40)
    
    # 1. 获取市场数据
    try:
        data = get_market_data(
            config["binance"],
            strategy["symbol1"],
            strategy["symbol2"],
            strategy["lookback_period"],
            strategy["interval"]
        )
    except Exception as e:
        logger.error(f"❌ 获取市场数据失败: {e}")
        return
    
    if data is None:
        logger.error("❌ 无法获取市场数据")
        return
    
    eth_price = data["prices"]["eth"]
    btc_price = data["prices"]["btc"]
    ratios = data["ratios"]
    
    logger.info(f"ETH 价格: ${eth_price:,.2f}")
    logger.info(f"BTC 价格: ${btc_price:,.2f}")
    logger.info(f"当前比率: {data['current_ratio']:.6f}")
    logger.info(f"历史均值: {data['mean']:.6f}")
    logger.info(f"z-score: {data['zscore']:.2f}")
    
    # 2. 判断信号
    signal_type, direction, reason = determine_signal(
        data["zscore"],
        strategy["entry_threshold"],
        strategy["exit_threshold"],
        strategy["stop_loss"]
    )
    
    logger.info(f"信号判断: {signal_type} - {reason}")
    
    # 3. 计算信号强度
    strength = min(5, max(1, int(abs(data["zscore"]) / 0.8)))
    
    # 4. 格式化信号
    signal_data = format_signal_json(
        signal_type=signal_type,
        direction=direction,
        zscore=data["zscore"],
        ratio=data["current_ratio"],
        mean=data["mean"],
        std=data["std"],
        eth_price=eth_price,
        btc_price=btc_price,
        strength=strength,
        reason=reason,
        threshold=strategy,
        position_size=strategy["position_size_usd"]
    )
    
    # 5. 保存信号
    save_signal(signal_data, config["storage"])
    
    # 6. 发送通知
    if signal_type != "HOLD" and config["notification"].get("enabled"):
        message = format_signal_message(signal_data)
        
        if config["notification"].get("telegram", {}).get("enabled"):
            send_notification(
                "telegram",
                message,
                config["notification"]["telegram"]
            )
        
        if config["notification"].get("feishu", {}).get("enabled"):
            send_notification(
                "feishu",
                message,
                config["notification"]["feishu"]
            )
    
    logger.info("✅ 监控完成")
    logger.info("=" * 60)
    
    return signal_data


if __name__ == "__main__":
    main()
