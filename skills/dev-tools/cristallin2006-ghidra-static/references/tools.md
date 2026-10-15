# 本 skill 工具入口

按当前问题选择工具，用 --help 查参数；工具是否可用以发现/功能探针为准。

| 脚本 | 用途线索 |
|---|---|
| `scripts/cone_invert.py` | cone_invert.py - 通用锥形反向传播求解器（铁律 6 阶梯 ①'：peel 无递推段/段非目标时的下一档）。 |
| `scripts/peel_inverse.py` | peel_inverse.py - 掩码依赖图 + 滞后-k 可剥离递推判定（铁律 6 工具形态：先剥离，再考虑 z3/SMT）。 |
