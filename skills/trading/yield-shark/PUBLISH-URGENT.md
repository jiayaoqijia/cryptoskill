# 🦈 YieldShark 收益鲨鱼 - 紧急发布指南

## ⚠️ 当前情况

**YieldShark 已 100% 完成，所有功能测试通过！**

但由于服务器环境限制，**无法自动完成 ClawHub 登录**，需要你在本地电脑手动操作。

---

## 🚀 快速发布步骤 (3 分钟搞定)

### 方案 A: 最简单 - 浏览器登录发布

1. **打开你的电脑浏览器**
   ```
   https://clawhub.ai/login
   ```

2. **登录账号**
   - 邮箱：`gztanht@gmail.com`
   - 完成邮箱验证码

3. **获取 CLI Token**
   - 登录后点击右上角头像 → Settings → CLI Tokens
   - 点击 "Generate New Token"
   - 复制生成的 token (格式类似：`ch_xxxxx`)

4. **回到终端，运行发布命令**
   ```bash
   cd ~/.openclaw/workspace/skills/yield-shark
   npx clawhub login --token ch_xxxxx  # 替换为你的 token
   npx clawhub publish . --no-input
   ```

5. **完成！** 
   - 看到 "✓ Published successfully" 就成功了
   - 技能主页：https://clawhub.com/skills/yield-shark

---

### 方案 B: 如果你已经有 Token

直接运行：
```bash
export CLAWHUB_TOKEN=<你的token>
cd ~/.openclaw/workspace/skills/yield-shark
npx clawhub publish . --no-input
```

---

## ✅ 发布前验证

运行以下命令，确保一切正常：

```bash
cd ~/.openclaw/workspace/skills/yield-shark

# 测试 USDT
node scripts/monitor.mjs USDT --limit 3

# 测试 USDC
node scripts/monitor.mjs USDC --limit 3

# 检查 skill 状态
openclaw skills info yield-shark
```

**预期输出：**
```
📦 yield-shark ✓ Ready
🦈 YieldShark - 嗅到钱的味道！
```

---

## 📊 技能信息 (发布后会显示)

| 项目 | 内容 |
|------|------|
| **名称** | 🦈 YieldShark 收益鲨鱼 |
| **Slug** | yield-shark |
| **作者** | @gztanht |
| **版本** | 1.0.0 |
| **数据** | DeFiLlama 实时 API |
| **定价** | 免费 3 次/天 + 0.01 USDT/次 |
| **钱包** | USDT: 0x33f943...5ad9, USDC: 0xcb5173...0e44 |

---

## 💡 发布后做什么？

1. **分享技能**: 把 https://clawhub.com/skills/yield-shark 分享给朋友
2. **测试收费**: 用新账号测试免费额度和付费流程
3. **收集反馈**: 根据用户反馈优化功能
4. **持续更新**: 添加更多平台和功能

---

## 🎯 待优化功能 (v1.1)

- [ ] 多代币对比 (--tokens USDT,USDC)
- [ ] 历史趋势图
- [ ] Telegram 推送
- [ ] 平台官网直达链接
- [ ] 更多链支持

---

**现在只需要你登录获取 Token，其他都搞定了！** 🦈🚀
