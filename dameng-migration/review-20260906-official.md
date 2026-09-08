# 应用 SQL 适配 DM8：官方资料复核

研究日期：2026-09-06。范围是应用源码及应用配置中的 SQL 适配。BM2 的连接、命令、模型、绑定、分页、类型转换和事务已支持达梦，以用户确认为前提。本轮未连接数据库，未修改业务源码。

## 结论

**方案可行，可以直接开始分批转换，不需要先取得完整构建包、全库 DDL 或全库样本。** 这是工程判断：源码可以揭示 SQL 文本、拼接过程、参数、数据库分支和结果使用方式；DM 官方语法资料足以支持许多表达式的保留或改写决定。

交付承诺应表述为“已取得应用 SQL 的静态审查和源码适配完成，剩余单项依赖已列明”。只有实际在目标版本执行过的语句，才能追加“DM8 执行验证通过”；没有执行记录时，不能承诺业务结果和性能已全部验证。这两个完成标准应分开记录，不用后一阶段的环境条件阻止前一阶段工作。

官方 DTS 评估文档也区分语法兼容性分析与目标库解析，并明确提示内置解析器版本可能与目标 DM 版本不同。这进一步说明：自动扫描或离线解析可以辅助审查，但不能直接当作目标版本的执行结果。本方案不要求引入 DTS 或开展数据迁移。[DTS 评估](https://eco.dameng.com/document/dm/zh-cn/pm/dts_assessment.html)

“改为达梦语法”不要求每条 SQL 都发生文字变化。普通增删改查以及目标支持的 Oracle 风格表达式可以保留；达梦的查询、写入语法均由官方手册明确给出。[数据查询语句](https://eco.dameng.com/document/dm/zh-cn/pm/check-phrases)、[数据的插入、删除和修改](https://eco.dameng.com/document/dm/zh-cn/pm/insertion-deletion-modification.html)

## 官方依据及其适配含义

| 核查项 | 官方资料说明 | 对本项目的处理建议 |
|---|---|---|
| 兼容模式 | 当前官方文档列出模式 2 为部分兼容 Oracle，模式 8 为部分兼容 DB2；修改模式可能影响数据存储和操作结果。[配置实例](https://eco.dameng.com/document/dm/zh-cn/start/dm-instance-linux.html) | 不能看到 DB2 写法就要求设置模式 8，也不能自行决定模式 2。记录实际 DM8 小版本及既定模式；未知时，先做不依赖它们的转换。 |
| NVL、DECODE | 两者均受支持；NVL 参数类型不同时会发生转换，转换可能失败。[函数手册 §8.4、§8.6](https://eco.dameng.com/document/dm/zh-cn/pm/function.html) | 不做全局函数替换。混合类型表达式单独检查参数及返回类型。 |
| TO_DATE | 函数受支持，但返回类型受 COMPATIBLE_MODE、ORA_DATE_FMT 影响，日期格式也有明确规则。[函数手册 §8.3](https://eco.dameng.com/document/dm/zh-cn/pm/function.html) | 显式格式优先核对；涉及隐式转换、字段读取类型时，只索取相关参数或字段类型。 |
| ROWNUM | 可限制行数；赋值发生在排序之前，直接用大于 1 的下界不能实现普通分页。[数据查询语句 §4.15](https://eco.dameng.com/document/dm/zh-cn/pm/check-phrases) | 保留正确的嵌套查询次序。BM2 自身分页已适配，仍需检查应用手写分页。 |
| 序列 NEXTVAL/CURRVAL | DM 支持序列伪列和 `FROM DUAL`；CURRVAL 依赖会话先使用 NEXTVAL，返回类型有 BIGINT 与扩展序列 DEC(30) 的区别。[数据定义语句：序列](https://eco.dameng.com/document/dm/zh-cn/pm/definition-statement.html) | 现有正常取序列语法可保留，关注会话及取值代码。不把序列创建、当前值搬迁变成本轮任务。 |
| 日期差 | DATEDIFF 计日期边界；DM 原生 TIMESTAMPDIFF 使用单位、起点、终点三个参数，返回间隔整数。[函数手册 §8.3](https://eco.dameng.com/document/dm/zh-cn/pm/function.html) | 日历日差、完整时长、近似月年差应分别制定规则，不能只替换函数名称。 |
| 日期加减 | DM 支持日期与整数相加减，以天为单位。[日期运算 §2.1](https://eco.dameng.com/document/dm/zh-cn/sql-dev/practice-date.html) | 原表达式含义明确时，可以把日步长转换成有文档依据的整数天运算。仍需核对完整查询结构。 |
| 空串与 NULL | DM 默认规则与 Oracle 有区别，兼容模式会影响空串处理；模式改变也不等同于已有数据自动获得相同语义。[Oracle 移植说明](https://eco.dameng.com/document/dm/zh-cn/start/oracle_dm)、[Oracle 迁移 FAQ](https://eco.dameng.com/document/dm/zh-cn/faq/faq-oracle-dm8-migrate.html) | `IS NULL`、`= ''`、TRIM、拼接及增删改条件需要单项判断。不能为“兼容”直接扩大 UPDATE/DELETE 命中集合。 |
| 元数据目录 | DM 有 Oracle 兼容视图，也有 SYSOBJECTS、SYSCOLUMNS 等自身目录；底层列类型、精度、长度字段有各自定义。[数据库检查](https://eco.dameng.com/document/dm/zh-cn/faq/faq-db-check)、[系统目录附录](https://eco.dameng.com/document/dm/zh-cn/pm/dm8-admin-manual-appendix1.html) | 不把 USER_TAB_COLUMNS 一律判错，也不把 SYSIBM/SYSCAT 按表名批量替换。逐条核对模式、列名、类型名称和长度单位的返回契约。 |

## TIMESTAMPDIFF 必须避免的误判

IBM 对 DB2 两参数 TIMESTAMPDIFF 的定义是基于时间戳差值字符串估算指定间隔，部分单位采用每月 30 天、每年 365 天。单位 256 表示年、64 表示月、32 表示周。不能把这些数字直接传给 DM 原生函数，或把跨月结果默认视为相同。[IBM TIMESTAMPDIFF 定义](https://www.ibm.com/docs/en/db2-for-zos/13.0.0?topic=functions-timestampdiff)

DM 的[其他数据库迁移 FAQ](https://eco.dameng.com/document/dm/zh-cn/faq/faq-other-dm8-migrate.html)包含一个需要警惕的示例：源表达式的 256 对应年，目标示例却使用 month；其中 DB2 单位表也与 IBM 原定义不一致。**该页只能辅助定位问题，不能直接作为批量转换模板。** 源语义以 IBM 对实际 DB2 版本的定义为准，目标语法以 DM SQL 函数手册为准。这里只确认写法的来源特征，未据此认定项目现网使用 DB2。

对项目内两参数写法，应恢复开始时间、结束时间、计量单位、取整方式，再判断业务原意。可明确保持的直接改；确有跨月算法歧义的，只暂停那条表达式，并写清所需答案。不能把“目标函数名相同”当作等价证明，也不能借适配顺便改变业务时长阈值。

## 静态适配如何形成可验收结果

以下是基于上述官方证据和本项目范围作出的实施建议：

1. 以“可恢复的 SQL 模板及其分支”为审查单位。文件命中数不等于 SQL 条数，更不等于待改写条数；评论、类型声明、同名副本与运行 SQL 应保持来源标识。
2. 每条记录原 SQL、目标 SQL或保留决定、参数、返回列、来源文件、适用条件及依据。只修改确定的方言差异，保持读写条件、绑定顺序和事务边界。
3. 对动态 SQL 同时追踪生产端、拼接片段与执行端。执行入口能接受字符串，不足以证明尚未取得的配置文本兼容。这里只需请求那组实际 SQL/片段及参数定义，不需要整张配置表的数据迁移。
4. BM2 已适配不等于所有业务 DatabaseKind 分支自动选对。只需确认达梦连接对应的枚举及实际取值，不能要求整个构建包才能继续其他转换。
5. 验证记录分别列出：静态审查、实际 DM SQL 执行、应用调用验证。尚未运行就明确留空。若后续有 DM 测试实例，函数和无业务表的查询可先独立验证；完整业务执行属于进一步证据。
6. 某条 SQL 的类型、空串语义、目标模式或外部配置未知时，登记为“该项待确认”，并继续处理其余条目。所有待确认项应随交付列明，不能归入“已转换完成”。

## 对既有方案的明确修正

- 构建包、全库 DDL、全量样本、数据库搬迁、停机切换和全系统联调，不作为开始应用 SQL 转换的统一前置条件。
- 现有[SQL 转换判断](<D:/work/company/太钢二炼钢/analysis/dameng-migration/SQL转换判断.md>)记录的两处改写具有相关语法依据，但“表达式有依据”不等于两个完整服务已适配或已在 DM8 通过；本研究未执行它们。
- 兼容函数的保留、明确差异的改写、单项依赖的登记，均属于有价值的交付；不以修改行数衡量完成度。
- 对系统最终运行成功的保证，需要相应执行证据。当前可以推进并交付源码适配，不把静态审查结论扩张成数据库迁移或上线验收结论。

资料限制：本次使用达梦在线官方文档和 IBM 源函数定义。在线文档随版本更新；目标 DM8 小版本和实际参数尚未在本研究中读取。所有配置相关判断因此保留条件，未作数据库设置建议或操作。
