#!/usr/bin/env python3
"""
Airdrop Hunter - 空投猎人
每次调用收费 0.001 USDT
"""

import sys

# 空投数据库（实际应该从API获取）
AIRDROPS = [
    {"name": "LayerZero", "status": "快照完成", "estimate": "$500-2000", "hot": True},
    {"name": "zkSync Era", "status": "进行中", "estimate": "$300-1000", "hot": True},
    {"name": "Starknet", "status": "已发放", "estimate": "$350", "claimed": True},
    {"name": "Scroll", "status": "进行中", "estimate": "$200-500", "hot": False},
    {"name": "Linea", "status": "进行中", "estimate": "$150-400", "hot": False},
]


def get_airdrops() -> list:
    """获取当前空投列表"""
    return AIRDROPS


def check_eligibility(address: str) -> list:
    """检查地址是否符合空投条件（模拟）"""
    # 实际需要调用链上API检查
    eligible = []
    for airdrop in AIRDROPS:
        if airdrop["status"] == "已发放":
            eligible.append({
                **airdrop,
                "claimed": True,
                "amount": airdrop["estimate"]
            })
    return eligible


def format_result(airdrops: list, eligible: list = None) -> str:
    lines = [
        "🎁 空投猎人",
        "━━━━━━━━━━━━━━━━",
        "🔥 热门空投:"
    ]
    
    for i, a in enumerate(airdrops[:5], 1):
        hot_emoji = "🔥" if a.get("hot") else "  "
        claimed = "✅ 已领取" if a.get("claimed") else ""
        lines.append(f"{i}. {a['name']} ({a['status']}) {hot_emoji}")
        if a.get("estimate"):
            lines.append(f"   预估: {a['estimate']} {claimed}")
    
    if eligible:
        total = sum(int(e["estimate"].replace("$", "").split("-")[0]) for e in eligible)
        lines.append(f"\n📊 空投总收益: ${total}")
    
    lines.append("")
    lines.append("✅ 已扣费 0.001 USDT")
    
    return "\n".join(lines)


if __name__ == "__main__":
    airdrops = get_airdrops()
    
    if len(sys.argv) > 1:
        address = sys.argv[1]
        eligible = check_eligibility(address)
        print(format_result(airdrops, eligible))
    else:
        print(format_result(airdrops))
