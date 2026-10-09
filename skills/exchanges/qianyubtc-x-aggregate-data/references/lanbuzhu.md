# 蓝不住的 X 中文区统计

`stats / rank / champions / daily / feed / hot / topics / rumors / rumor` 这几个命令读的是 [蓝不住 lanbuzhu.org](https://lanbuzhu.org) 的开放接口（`https://lanbuzhu.org/api/open/v1`，只读，免费，不用注册）。蓝不住长期跟踪数千个 X 中文区账号，每天定格一次数据。

## 口径

- **一天** = 北京时间 8 点到次日 8 点（UTC 的一天）。`today` 是还没结束的今天，`yday` 是已经定格的昨天。
- **发帖** = 原创 + 引用（不含转推、回复）。
- **评论** = 回复别人的条数（按发帖计数推算）。
- **涨粉** = 当天最后一次记录的粉丝数 − 前一天最后一次。新收录的号第一天没有。
- **推文曝光** = 当天新增的浏览（以前发的推当天涨的也算）。
- **帖均曝光**（avgv）= 最近 7 个完整的天，每条原创 / 引用的平均浏览。
- 数据不完整显示 `null`，不是 0。`partial: true` 表示这段时间里有的天没数据，或那天没从头抓全（新收录的号常见），数字可能偏小。
- 返回里的日期：`stats` 的 `as_of` 写了 today / yday 各是哪天；`rank` 的 `days`、`champions` 的 `day` 是统计的那天（或范围）。北京时间凌晨 0–8 点问"昨天"，`yday` 其实是前天那个统计日，回答时要说清。
- 粉丝数：`champions` 里已经定格（`frozen: true`）的天，`followers` 是那天的；其他地方是现在的。
- `7d` / `30d` = 最近 6 / 29 个完整的天 + 还没结束的今天。
- 还没统计完：`champions` 返回 `pending`（涨粉 / 评论还没出数，那几项给空），`rank` 按涨粉 / 评论排今天时返回 `pending`（排名只来自少数已经有数的账号）。
- 账号上的 `suspected_limited: true` = 蓝不住判断这个号最近疑似被限流（帖均曝光远低于粉丝数该有的水平），仅供参考。

## 返回里的常用字段

- `account`：`handle` `name` `followers` `track`（赛道：ai / crypto / finance / media）`tier`（粉丝段）`x_url` `lanbuzhu_url`。
- `stats <账号>`：
  - `table`：`today / yday / 7d / 30d` 各一组 `views posts replies gain avgv maxv`。
  - `series`：近 30 天每天的 `views posts replies gain rank`（rank = 当天曝光在全部收录账号里的名次）。
  - `top`：近 30 天曝光最高的 5 条推。
  - `champs`：夺冠记录（`dim` = posts / replies / gain / views，`streak` 连冠天数，`record` 破纪录）。
  - `health`：曝光效率（帖均曝光 ÷ 粉丝，%）和同粉丝段中位数比，`views_wow` / `gain_wow` 是周环比 %。
  - `events`：最近的大V动态。
  - `stats`：粉丝、7 天涨粉、7 天帖均曝光、累计夺冠次数；`peers`：同赛道近 7 天曝光最高的几个号。
- `feed` 的 `type`：
  - `delete`：删帖，`data.text` 是删前原文，`data.views` 删前曝光；
  - `name / bio`：改名、改简介，`data.from → data.to`；`avatar`：换头像，`data.to` 是新头像；
  - `locked / gone / back`：锁推、失联（不存在或被封）、恢复；
  - `following`：关注数一下子变了很多；`fans`：一天涨粉 / 掉粉特别多；
  - `interact`：收录账号之间转推（rt）/ 引用（quote）/ 提到（mention）；
  - `viral`：24 小时内破 10 万曝光的推。
- `rumors` / `rumor`：`score` 风险分 0–100，`verdict` 是结论（疑似谣言 / 存疑 / 数据不足 / 暂未发现问题），`status` 是状态（在谣言库 / 已撤下 / 作者申诉中），`noted` = 有社区笔记，`report_url` 是蓝不住上的报告页。**仅供参考，不代表事实认定**；被站长撤下的不再提供报告。

## 限制

- 每个 IP（IPv6 按 /64）每分钟 60 次、每天 3000 次、最多查 300 个不同账号（`stats`、`feed --handle`），UTC 零点重置；超了返回 429，等一会儿再试。服务器忙时可能返回 503，30 秒后再试。
- 只给单个账号或前 N 名（排行最多 50），不提供整份名单；`feed --handle` 只给这个号最近 30 条。
- 没收录的账号会返回 404 和推荐收录的链接；收录后先观察 2 天才进榜。
- 用蓝不住的数据请注明来源"蓝不住 lanbuzhu.org"。
