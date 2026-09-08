# 既有两处 SQL 改动复核

> 快照说明：本文复核的是补原 SQL 注释之前的 6 行语法改动，下面行号对应那个阶段。此后按用户要求新增 26 行注释，未改变可执行内容；当前行号和哈希见[注释保留日志](<D:/work/company/太钢二炼钢/analysis/dameng-migration/sql-comment-preservation-log.json>)。

日期：2026-09-06。范围：只读复核此前两处应用 SQL 改动，作为方案可行性评估的证据；本轮未修改或回退业务代码，未执行数据库语句。

## 结论

两处转换的核心方向有官方语法依据，当前证据不足以判定它们引入了确定的运行缺陷。可以继续逐条进行源码适配，但**这两个片段还不能作为整条服务适配完成的证明，也不能直接推广为全仓库机械替换规则**。

本工作属于应用 SQL 源码适配。构建运行包、数据库全量样本或由开发人员承担数据库迁移，都不是继续源码审查的全局前置条件。具体 SQL 的输入类型、格式、语义不明时，应只挂起对应条目。运行验证由可用的 DM8 环境完成，可以先交付常量组成的独立 SELECT 验证脚本，无须迁移业务表才能验证本次两个表达式。

## 复核对象及完整性

| 对象 | 实际改动 | 当前检查结果 |
|---|---|---|
| [tmsme59_inq.cpp](D:/work/company/太钢二炼钢/Server/TMSM/p_tmsm_7160/tmsme59_inq.cpp:86) | 1 行：日历日差改为 DATEDIFF，单行来源改为 DUAL | 当前 SHA256 与日志一致；按日志还原前版本与 Git HEAD 字节一致 |
| [wmfm01_inq.cpp](D:/work/company/太钢二炼钢/Server/WMSM/p_wmsm_8170/wmfm01_inq.cpp:280) | 5 行：日期加减取消 DAY 后缀，SYSIBM.SYSDUMMY1 改为 DUAL | 当前 SHA256 与日志一致；按日志还原前版本与 Git HEAD 字节一致 |

两文件的 GB18030 解码再编码结果与原字节一致，行数及 CRLF 数保持。验证依据为 [sql-conversion-log.json](D:/work/company/太钢二炼钢/analysis/dameng-migration/sql-conversion-log.json)，本轮额外比对了 Git HEAD，未只依赖日志的自述。编码、差异与哈希检查仅证明改动边界，没有证明数据库执行成功。

## CHANGE-01：日历日差

原表达式是 `DAYS(DATE(TIMESTAMP(end))) - DAYS(DATE(TIMESTAMP(start)))`；现表达式是 `DATEDIFF(DAY, CAST(start AS TIMESTAMP), CAST(end AS TIMESTAMP))`。

**静态判断：核心语义合理。** IBM 的 DAYS 按日期给出整数表示；DM 的三参数 DATEDIFF 按指定单位计跨越的日期时间边界。对于能在两端成功解析、无时区的现代业务日期，两者都计算结束日期减开始日期的日历天数，参数方向也一致。跨午夜但不到 24 小时应得 1，而不是 0。[IBM DAYS](https://www.ibm.com/docs/en/db2/11.5.x?topic=functions-days)、[DM 函数：DATEDIFF](https://eco.dameng.com/document/dm/zh-cn/pm/function.html)

**条件风险：字符串解析契约尚未闭合。** 服务从输入表合并 `REC_CREATE_TIME`、`CHANGE_TIME`，随后调用 `ToString()`，没有在改动行规定时间格式。DM 的 CAST 使用日期时间格式规则；不能仅从字段名推断实际传入的一定是 `YYYY-MM-DD HH24:MI:SS`，也不能假定一定是 14 位紧凑字符串。若实际输入与会话格式不合，需按确认的格式使用显式转换或已有 BM2 的日期类型绑定。这是对应条目的待确认项，不是当前已复现的故障。[源码输入位置](D:/work/company/太钢二炼钢/Server/TMSM/p_tmsm_7160/tmsme59_inq.cpp:63)、[DM 函数：日期格式和 CAST](https://eco.dameng.com/document/dm/zh-cn/pm/function.html)

**返回值：没有证据要求修改读取代码。** 原值和新值都是整数性质的天数；现有代码用 `GetDecimal(1)` 放入 `CDecimal`。用户已确认 BM2 处理类型转换，单凭 SQL 函数返回整数不能判定这里需要更改。该局部变量后续用于日志，参与使用时间计算的相关表达式已被注释；实际分钟计算仍来自后面的查询。[读取位置](D:/work/company/太钢二炼钢/Server/TMSM/p_tmsm_7160/tmsme59_inq.cpp:97)

**确认的未完成项：同一函数仍执行多处 DB2 风格时间差表达式。** 第 113、141、195、218、256 行有两参数 `TIMESTAMPDIFF(4/8, CHAR(...))`，第 287 行还使用 `SYSIBM.SYSDUMMY1`。因此转换第 86 行并不使整个行车作业率查询完成适配。[后续小时查询](D:/work/company/太钢二炼钢/Server/TMSM/p_tmsm_7160/tmsme59_inq.cpp:113)、[分钟查询](D:/work/company/太钢二炼钢/Server/TMSM/p_tmsm_7160/tmsme59_inq.cpp:141)

后续转换这些两参数 TIMESTAMPDIFF 时，必须重新判断计算含义：DM 的 `DATEDIFF(MINUTE/HOUR,...)` 计边界，不能直接当作经过的完整分钟或小时。例如从 12:00:59 到 12:01:00 只经过一秒，按分钟边界计数是 1。IBM 的时间戳时长表达式又存在月、年换算估计规则；源码同时出现不同数据库方言，不能把某个 DB2 分支的推测行为自动当成现网 Oracle 的已验证业务契约。[IBM TIMESTAMPDIFF](https://www.ibm.com/docs/en/db2-for-zos/13.0.0?topic=functions-timestampdiff)、[DM 函数](https://eco.dameng.com/document/dm/zh-cn/pm/function.html)

## CHANGE-02：最近三天的日期序列

**静态判断：日期边界保持。** 原 CTE 从查询日期减三天开始，每次加一天，旧日期小于查询日期减一天时继续；现表达式保留了这些边界。DM 官方说明日期可直接加减天数。因此，按合法日期输入推导，CTE 仍产生查询日期之前的三天；例如 `20240301` 应产生 `20240227`、`20240228`、`20240229`。这是数学推导的期望值，未在 DM8 执行。[DM 日期运算](https://eco.dameng.com/document/dm/zh-cn/sql-dev/practice-date)

**递归结构：未发现足以判错的结构问题。** DM 官方支持递归 WITH，`RECURSIVE` 通常可省略；当前 CTE 使用 UNION ALL，递归成员只引用 A 一次，也没有递归成员禁止的 DISTINCT、GROUP BY、集函数或把 A 放在外连接右侧的情况。整数序号与日期递增的对应类型具备兼容基础。完整表达式的名称解析、实际版本行为仍应由独立 SQL 检查确认；不能仅因没有 `WITH RECURSIVE` 就判为不兼容。[DM 数据查询语句 §4.4.2.3](https://eco.dameng.com/document/dm/zh-cn/pm/check-phrases)

原有 `@DATE_TIME` 参数、`TO_DATE(...,'YYYYMMDD')` 格式、TO_CHAR 输出及 LEFT JOIN 条件保持，格式约束比 CHANGE-01 清晰；BM2 参数绑定适配作为用户确认的基础沿用。

**确认的未完成项：同一报表分支仍有后续旧语法。** 查询日期序列后，`TFOSMT03A` 分支继续执行“合计行”查询，第 327、329、333 行仍含 `TO_DATE(...) - 1 DAY`。即使 CTE 通过，也不能宣称该报表分支完整通过。其他表分支同样存在 `DAYS`、`- 1 DAYS` 等候选表达式，需要分别审查。[同一分支的后续合计查询](D:/work/company/太钢二炼钢/Server/WMSM/p_wmsm_8170/wmfm01_inq.cpp:327)、[相邻稳定周期分支](D:/work/company/太钢二炼钢/Server/WMSM/p_wmsm_8170/wmfm01_inq.cpp:247)

## 两处共同的数据库分支影响

两处 switch 都让 DB2、DB2_ORACLE、MSSQL、ORACLE 及 default 共用同一赋值。修改没有新增或单独选择达梦分支，**事实上的改动范围包含所有这些标签的执行路径**。[TMSM 分支](D:/work/company/太钢二炼钢/Server/TMSM/p_tmsm_7160/tmsme59_inq.cpp:79)、[WMSM 分支](D:/work/company/太钢二炼钢/Server/WMSM/p_wmsm_8170/wmfm01_inq.cpp:272)

当前用户目标是把应用切到 DM8，并未要求继续交付其他数据库版本。因此，这个事实本身不是已确认缺陷；但后续方案应明确按 DM8 交付，不能同时声称旧多库行为保持。若某个模块还要发布旧库版本，应对该模块单独确定分支策略，不要凭想象添加未经确认的 BM2 枚举值。

## 对执行方式的建议

1. 将转换单位从“关键词或一行”提升为“一条完整 SQL 及同一调用路径的关联语句”，同时保留逐项小差异。
2. 每个条目写清：输入类型和格式、原有结果含义、DM 写法、是否影响其他数据库分支、还缺什么证据。
3. 把状态区分为“源码已转换”“静态已复核”“DM SQL 已执行验证”。此前日志已注明仅两个表达式转换、没有完整服务完成，不应提升其完成等级。
4. 对有确定规则的相同模式可以批量定位和辅助改写；日期时长、空值、锁语义、隐式转换和动态 SQL 应逐个语境审查。
5. 两个片段的最小验证可用常量 SELECT：同日、跨午夜、负方向、月末和闰日；三天 CTE 检查恰好三条连续日期。涉及业务表的 JOIN、汇总和 CRUD 再随对应测试条件验证。这不要求当前负责人承担表或数据迁移。

最终建议：**适合继续有依据的应用 SQL 适配；不适合把这两处局部转换直接扩大为全仓库无差别替换。** 本轮的确定发现是已有改动边界清晰、两条调用链尚未完整处理；日期格式和多库保留属于条件风险，数据库未运行属于验证状态，三者应分开记录。
