# 默认链范围与资产核验

用户偏好，确认于2026-10-28：注意力/alpha未指定链时，优先Robinhood Chain和Base；Sui、BSC、Solana为同级次覆盖。根据研究问题和可得证据分配采集预算，不强制五链每次全搜。明确指定标的/其他链时按用户请求，不让优先级变成排除规则。不自动创建扫描或监控。

## 先确认研究对象

| 链 | 身份与链上重点 | 免费采集起点 |
|---|---|---|
| Robinhood Chain | 链上合约/主网、真实池、桥入桥出、可兑现深度、部署者和LP控制；与App上架、HOOD股票、股票代币分开，不能推定Robinhood背书 | 官方connecting文档、公共RPC、Blockscout、DEX实际覆盖；没有聚合器覆盖则记缺口 |
| Base | EVM合约/池身份、跨链净流量、稳定币和真实深度、关联钱包、LP及权限变化 | 官方RPC、浏览器、DEX与DefiLlama已覆盖数据 |
| Sui | Move coin type、升级/铸币能力、对象与持有人、池深度与真实交易；pool/object ID不是coin type | 当前官方GraphQL/gRPC、浏览器、DEX；不要默认旧JSON-RPC可用 |
| BSC | EVM身份、税费/黑名单/可升级权限、部署者关联、LP控制与大额转移 | 官方网络文档、公共RPC、浏览器、DEX |
| Solana | mint及Token/Token-2022程序、mint/freeze/扩展权限、持有人与关联钱包、LP和迁移、交易失败 | Solana只读RPC、浏览器、DEX |

Robinhood官方connecting页在本次查阅列出mainnet 4663、testnet 46630，原生gas ETH；mainnet RPC为https://rpc.mainnet.chain.robinhood.com，浏览器https://robinhoodchain.blockscout.com。每次研究重新核对官方文档，再用eth_chainId与区块数据验证实际连接。测试网交易不作主网市场证据。Base/BSC也先核实官方网络参数及实际chainId，不信搜索摘要或名称。

Sui coin type使用0xpackage::module::COIN；脚本规范package为64位小写十六进制，保留Move标识符大小写；0x2::sui::SUI与native_id=sui合并。普通64位object ID拒绝作为币种，泛型coin type需模型先核验并使用明确native_id与证据，不猜测。现有Ethereum等账本身份不迁移。

## 窗口与变化

新近注意力标的以近1h/6h/24h及可得历史观察；成熟标的加7d/30d。窗口是采集选项，解释由模型决定。至少两个可比时间点才描述变化，记录区块/checkpoint、时间、池/对象/钱包范围；缺历史、标签或交易解析不能改写为无卖压。各链按能力核验权限，不把EVM renounce或LP锁仓规则硬套Move/Solana。

## 当前实现边界

脚本rpc只读allowlist包含eth_chainId；sui-checkpoint固定执行只读GraphQL checkpoint查询，提供链上时点入口，不代表已实现Sui全量持有人/事件索引。深入数据通过原生只读工具/浏览器捕获后导入native evidence；有分页/归档限制明确披露。GraphQL返回errors即失败，保留原始响应。

来源（查阅2026-10-28，动态内容每次复核）：
- https://docs.robinhood.com/chain/connecting/
- https://www.docs.sui.io/develop/accessing-data/graphql/graphql-migration-cookbook
- https://www.docs.sui.io/develop/accessing-data/graphql/query-with-graphql
