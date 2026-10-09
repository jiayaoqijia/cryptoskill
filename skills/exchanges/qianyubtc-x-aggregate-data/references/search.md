# X 搜索语法速查

`x.py search "<查询>"` 的查询就是 X 网页搜索框里的写法，可以组合。默认按时间倒序（最新），`--top` 按热门。

| 写法 | 意思 |
| --- | --- |
| `比特币 ETF` | 同时包含两个词 |
| `"精确短语"` | 整句匹配 |
| `比特币 OR BTC` | 任一（OR 要大写） |
| `比特币 -空投` | 排除某个词 |
| `from:elonmusk` | 某人发的 |
| `to:elonmusk` | 回复某人的 |
| `@elonmusk` | 提到某人的 |
| `(from:a OR from:b)` | 几个人发的（一次最多二十来个，查询串太长会报错） |
| `since_time:1790812800` / `until_time:1791417600` | 时间范围（Unix 秒，准；这两个是 2026-10-01 和 2026-10-08 的 UTC 零点）。**用 `x.py search` 的 `--since 2026-10-01` / `--until 2026-10-08` / `--since 24h` 就行，脚本会换算** |
| `since:2026-10-01` / `until:2026-10-08` | 按日期，不太准（实测 `until:` 不生效），别用 |
| `min_faves:100` / `min_retweets:50` / `min_replies:20` | 至少多少赞 / 转发 / 回复 |
| `lang:zh` / `lang:en` / `lang:ja` | 语言 |
| `filter:links` / `filter:media` / `filter:images` / `filter:videos` | 带链接 / 带图或视频 |
| `-filter:replies` / `filter:replies` | 不要回复 / 只要回复 |
| `-filter:retweets` | 不要转推 |
| `filter:verified` / `filter:blue_verified` | 认证账号 |
| `conversation_id:<推文id>` | 某条推下面的整个对话（回复区） |
| `url:github.com` | 链接里带某个域名 |
| `#话题` / `$BTC` | 话题标签 / 代币符号 |

## 例子

- 某人这周说过的和 AI 有关的：`x.py search "from:sama AI" --since 7d`
- 中文区今天关于某币点赞最多的讨论：`x.py search '$SOL lang:zh' --since 24h --min-likes 50 --limit 100 --sort likes`
- `--top` 是 X 的"热门"排序（综合互动和新鲜度），不是按点赞；要"点赞最多"用上面的写法
- 某条推下回复者在说什么：`x.py tweet <链接> --replies 100`（比搜 `conversation_id:` 更方便）
- 谁在转发某个 GitHub 项目：`url:github.com/owner/repo`

## 注意

- 被 X 搜索降权 / 封禁的账号搜不到，看某个人发了什么用 `x.py tweets <账号>` 更准。
- `min_faves` 这类门槛是在 X 那边过滤的，刚发的推还没攒够赞时搜不到。
- 一页约 20 条，`--limit` 大了会自动翻页（每页之间停一下）。
