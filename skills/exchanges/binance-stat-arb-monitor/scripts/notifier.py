#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通知推送模块
"""
import requests
import logging

logger = logging.getLogger(__name__)


def send_telegram(message, config):
    """
    发送到 Telegram
    
    Args:
        message: 消息内容
        config: Telegram 配置 {bot_token, chat_id}
    """
    bot_token = config.get("bot_token")
    chat_id = config.get("chat_id")
    
    if not bot_token or not chat_id:
        logger.warning("Telegram 配置不完整，跳过推送")
        return False
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=data, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        if result.get("ok"):
            logger.info("✅ Telegram 消息发送成功")
            return True
        else:
            logger.error(f"❌ Telegram 发送失败: {result}")
            return False
            
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Telegram 请求失败: {e}")
        return False


def send_feishu(message, config):
    """
    发送到飞书
    
    Args:
        message: 消息内容
        config: 飞书配置 {webhook_url}
    """
    webhook_url = config.get("webhook_url")
    
    if not webhook_url:
        logger.warning("飞书 Webhook 未配置，跳过推送")
        return False
    
    data = {
        "msg_type": "text",
        "content": {
            "text": message
        }
    }
    
    try:
        response = requests.post(webhook_url, json=data, timeout=10)
        response.raise_for_status()
        logger.info("✅ 飞书消息发送成功")
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ 飞书请求失败: {e}")
        return False


def send_notification(platform, message, config):
    """
    统一推送接口
    
    Args:
        platform: 平台 (telegram / feishu)
        message: 消息内容
        config: 平台配置
    """
    if platform == "telegram":
        return send_telegram(message, config)
    elif platform == "feishu":
        return send_feishu(message, config)
    else:
        logger.warning(f"不支持的平台: {platform}")
        return False
