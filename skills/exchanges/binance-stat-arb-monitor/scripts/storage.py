#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据存储模块
"""
import os
import json
import logging
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)


def ensure_dir(path):
    """确保目录存在"""
    Path(path).mkdir(parents=True, exist_ok=True)


def save_signal(signal_data, storage_config):
    """
    保存信号到文件
    
    Args:
        signal_data: 信号数据
        storage_config: 存储配置
    """
    data_dir = storage_config.get("data_dir", "data")
    signals_file = storage_config.get("signals_file", "data/signals.json")
    latest_file = storage_config.get("latest_file", "data/latest_signal.json")
    
    # 确保目录存在
    ensure_dir(data_dir)
    
    # 保存最新信号
    try:
        with open(latest_file, "w", encoding="utf-8") as f:
            json.dump(signal_data, f, indent=2, ensure_ascii=False)
        logger.info(f"📝 最新信号已保存: {latest_file}")
    except Exception as e:
        logger.error(f"❌ 保存最新信号失败: {e}")
    
    # 追加到历史信号
    try:
        signals = []
        if os.path.exists(signals_file):
            with open(signals_file, "r", encoding="utf-8") as f:
                signals = json.load(f)
        
        # 检查是否重复（5分钟内不重复记录）
        if signals:
            last_signal = signals[-1]
            last_time = datetime.fromisoformat(last_signal["timestamp"].replace("Z", "+00:00"))
            current_time = datetime.fromisoformat(signal_data["timestamp"].replace("Z", "+00:00"))
            
            time_diff = (current_time - last_time).total_seconds()
            if time_diff < 300 and last_signal.get("signal_type") == signal_data.get("signal_type"):
                logger.info("⏭️ 5分钟内相同信号，跳过记录")
                return
        
        signals.append(signal_data)
        
        # 只保留最近 1000 条
        if len(signals) > 1000:
            signals = signals[-1000:]
        
        with open(signals_file, "w", encoding="utf-8") as f:
            json.dump(signals, f, indent=2, ensure_ascii=False)
        logger.info(f"📚 信号历史已更新: {signals_file} ({len(signals)} 条)")
        
    except Exception as e:
        logger.error(f"❌ 保存历史信号失败: {e}")


def load_signals(storage_config):
    """加载信号历史"""
    signals_file = storage_config.get("signals_file", "data/signals.json")
    
    if not os.path.exists(signals_file):
        return []
    
    try:
        with open(signals_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"❌ 加载信号历史失败: {e}")
        return []


def get_signal_stats(storage_config):
    """获取信号统计"""
    signals = load_signals(storage_config)
    
    if not signals:
        return {
            "total": 0,
            "open": 0,
            "close": 0,
            "hold": 0
        }
    
    stats = {
        "total": len(signals),
        "open": len([s for s in signals if s.get("signal_type") == "OPEN"]),
        "close": len([s for s in signals if s.get("signal_type") == "CLOSE"]),
        "hold": len([s for s in signals if s.get("signal_type") == "HOLD"])
    }
    
    return stats
