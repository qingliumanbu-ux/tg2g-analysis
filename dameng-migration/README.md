# 后台 SQL 达梦适配清单

更新：2026-09-06（第二轮自查后）。**当前状态：全部 21 个 Server 模块的基础转换已完成**——台账 [sql-ledger.csv](<D:/work/company/太钢二炼钢/analysis/dameng-migration/sql-ledger.csv>) 共 17,595 条（可保留 17,201 / 已转换 345 / 待人工口径 34 / 动态文本 15），终态见 **[全模块基础转换总结报告](<D:/work/company/太钢二炼钢/analysis/dameng-migration/全模块基础转换总结报告.md>)**。下一阶段为精修：HR-001—006 口径答复→34 条挂起语句改写→15 条动态文本→E2/E3/E4 验证→Client 端登记。用户最新明确：负责应用/后台代码中的 SQL 转换，使查询、新增、修改、删除等操作使用 DM8 支持的语法；不承担数据库数据/对象迁移、环境部署和全项目联调。BM2 底层适配以用户确认作为前提。构建包、全库 DDL、样本和双库环境不再作为开始 SQL 转换的前置条件。

## 1. 当前文档入口

准备交给新的 Agent 持续实施时，先发送 **[Agent 交接与持续执行说明](<D:/work/company/太钢二炼钢/analysis/dameng-migration/AGENT交接与持续执行说明.md>)**。该文档包含当前未提交改动、首批接续点、循环执行协议、台账格式和可直接复制的启动指令。

二级模块完成时按[模块完成与 SQL 等价性验收规范](<D:/work/company/太钢二炼钢/analysis/dameng-migration/模块完成与SQL等价性验收规范.md>)停下来汇报。报告必须区分源码适配、DM8 可执行和结果等价，使用[模块完成报告模板](<D:/work/company/太钢二炼钢/analysis/dameng-migration/templates/模块完成报告模板.md>)，由用户审核后再进入下一模块。

后续通过 **[taigang-dm8-sql Skill](<D:/work/company/太钢二炼钢/analysis/skills/taigang-dm8-sql/SKILL.md>)** 统一执行。每处改写先在源码注释保留完整原 SQL，再写达梦 SQL；日期、空值等疑问进入[待人工复核 SQL 清单](<D:/work/company/太钢二炼钢/analysis/dameng-migration/待人工复核SQL清单.md>)，按用户答复处理对应条目，其余继续。

Skill 已通过 Skills Manager 加入本机技能库，并已刷新部署到 Codex 和 ZCODE；项目内 `analysis/skills/taigang-dm8-sql` 保留可维护源文件。2026-09-06 优化：SKILL.md 补充内容驱动块检测、盲区形态清单、逐模板函数核对与三断言；新增 [references/conversion-rules.md](<D:/work/company/太钢二炼钢/analysis/skills/taigang-dm8-sql/references/conversion-rules.md>)（T1—T15 规则表、支持白名单、待口径政策，均附官方出处）；三个副本已同步。调用示例：`使用 $taigang-dm8-sql，先处理 WMSM 模块，完成模块报告后停下来。` 结构校验和隔离样例检查已通过，两个 Agent 的副本与源文件一致，记录见[技能校验与部署记录](<D:/work/company/太钢二炼钢/analysis/dameng-migration/skill-setup-validation.json>)；这些检查不代表业务 SQL 已在 DM8 运行通过。

1. **[后台 SQL 达梦适配可行性与执行方案](<D:/work/company/太钢二炼钢/analysis/dameng-migration/后台SQL达梦适配可行性与执行方案.md>)**：后续执行的主文档，包含可行性结论、责任范围、当前进度、转换原则、批次顺序和完成标准。先读这一份。
2. [官方资料复核](<D:/work/company/太钢二炼钢/analysis/dameng-migration/review-20260906-official.md>)与[既有两处改动复核](<D:/work/company/太钢二炼钢/analysis/dameng-migration/review-20260906-changes.md>)：本次研究证据。已有两处改写有语法依据，两个完整服务仍有未处理语句；没有 DM8 执行记录。
3. [SQL 转换执行范围](<D:/work/company/太钢二炼钢/analysis/dameng-migration/执行准备与资料清单.md>)与[后台 SQL 转换判断](<D:/work/company/太钢二炼钢/analysis/dameng-migration/SQL转换判断.md>)：简版范围和此前处理记录；本轮复核补充了完整调用路径、日期语义与多库分支的注意事项。
4. [首批人工审查项](<D:/work/company/太钢二炼钢/analysis/dameng-migration/首批人工审查项.md>)：25 个主题、113 个源码证据位置，条目之间存在重叠，不是 25 个必改点。原记录的运行、迁数或部署依赖保留为历史背景，不能直接作为当前 SQL 转换的前置条件或完成状态。

## 2. 全量清单

| 文件 | 如何使用 |
|---|---|
| [file-checklist.csv](<D:/work/company/太钢二炼钢/analysis/dameng-migration/file-checklist.csv>) | 5,155 个候选文件，一文件一行；按 module、category、review_order、work_groups 筛选，查看建议、验证方法、原始规则行号及已审查条目 ID |
| [review-rules.csv](<D:/work/company/太钢二炼钢/analysis/dameng-migration/review-rules.csv>) | 10 类审查规则：分支、动态配置、序列锁、元数据、查询语义、其他方言、类型、事务、常规访问与部署材料 |
| [coverage-ledger.csv](<D:/work/company/太钢二炼钢/analysis/dameng-migration/coverage-ledger.csv>) | 6,338 个普通文件的覆盖台账，包含未命中和二进制；847 个可读文本未命中现有规则，不能据此断言没有数据库依赖 |
| [archive-checklist.csv](<D:/work/company/太钢二炼钢/analysis/dameng-migration/archive-checklist.csv>) | 113 个压缩包候选成员，单列发布身份、规则和当前工作区字节相同副本；完整 401 个成员仍见原始 archives.json |
| [business-coverage.csv](<D:/work/company/太钢二炼钢/analysis/dameng-migration/business-coverage.csv>) | 方案 8 类业务与初步代码阅读导航；作为 SQL 定位背景，不要求用户负责全业务验收 |
| [interface-register.csv](<D:/work/company/太钢二炼钢/analysis/dameng-migration/interface-register.csv>) | 原方案 21 个对接方的背景记录；整体接口联调不属于当前 SQL 转换交付 |

原扫描明细继续保留在 [database-workspace](<D:/work/company/太钢二炼钢/analysis/database-workspace/检索覆盖报告.md>)。当前清单增加审查顺序与处理方法，没有把正则命中改称不兼容结论。

## 3. 首批应关注的证据

| 条目 | 已确认的源码事实 | 需要验证或补齐 |
|---|---|---|
| BR-001 | 公共取号的 default 分支没有 Oracle 分支的 FOR UPDATE | DM8 实际 DatabaseKind 映射及取号事务/并发 |
| BR-002 | 业务通过 NEXTVAL 等表达式生成格式化序号 | 应用侧取值类型、格式与会话依赖；序列对象及状态迁移由数据库侧处理 |
| BR-004 / DY-011 | 实际元数据服务只将 VARCHAR2 分类为字符型；客户端另有注释旧 SQL | 迁移后目录类型、列长度和页面字段契约；两项属于同一链的不同视角 |
| BR-005 | 履历拼接用目录长度决定舍弃哪些旧片段 | 目标字段与 CString 的字符/字节长度单位 |
| BR-008 | 计划清理使用 TRIM 后 IS NULL 的条件 | 空串、空格与 NULL 对实际删除集合的影响 |
| DY-006 / 007 / 010 | 查询还来自 TMMTP 配置和 TGCPMSI01.SQL_CONTEXT、TED54 参数 | 库内生效 SQL、配置结构和生成后的查询模板 |
| DY-008 | 配置复制含 table@DB_LINK_NAME 并显式提交事务 | 实际跨库拓扑、启用状态和失败边界 |
| DY-003 / 012 | 某 C# 方法调用被注释；两个工程输出相同程序集名 | 可达性及当前部署制品对应源码，避免改错版本 |
| BR-012 | 一个 DB_KIND 命中仅包含各分支相同的普通查询 | 保留并回归，作为不因命中就改写的对照 |

## 4. 原试点资料的用途调整

选择 FBSM23S2N，是因为当前源码能追到查询、批量删除/新增和回读，且没有发现三个主服务直接外发电文。TFBSM23 被下游配料计算读取，必须使用隔离测试环境；表触发器及平台隐式依赖仍需确认。

此前设计的初始化、读写、回滚、并发等 11 组用例保留为后续测试人员参考；完成它们不再作为开始 SQL 转换的条件。当前任务不包含为此搭环境或迁移测试数据。

此链主要使用普通增删改查，不能为了做“转换试点”人为改写原本兼容的 SQL。当前优先检查首批清单中存在方言、函数签名或数据库分支差异的具体语句。

## 5. 验证与可重复生成

转换前已核对所有 6,338 个原文件的 SHA-256、覆盖集合、审查 ID 和源码位置。2026-09-06 再次读取全部原文件：无缺失，仅已记录的 2 个源码文件与基线不同。已有改动为 2 个文件中的 2 个 SQL 表达式，见 [sql-conversion-log.json](<D:/work/company/太钢二炼钢/analysis/dameng-migration/sql-conversion-log.json>)；当前清单中的哈希/特征行号仍表示转换前扫描基线。原试点的 8 文件、28 处定位记录保留为阅读证据。基线汇总见 [checklist-summary.json](<D:/work/company/太钢二炼钢/analysis/dameng-migration/checklist-summary.json>)和 [validation.json](<D:/work/company/太钢二炼钢/analysis/dameng-migration/validation.json>)。

[build_migration_checklist.py](<D:/work/company/太钢二炼钢/analysis/build_migration_checklist.py>)读取已有扫描与人工复核生成清单；源文件变化时会停止，避免复用过期位置。它不连接数据库、不执行应用、不输出环境配置值。下一执行批次需保留原快照、建立当前版本及逐条 SQL 状态，防止重新生成文件清单时覆盖人工结论。规则排序是辅助分流，具体位置以人工结论为准；“部分位置已审查”不代表该文件全部 SQL 已审查。

验证状态分别记录为源码/语法静态检查与实际数据库运行检查。未运行不妨碍交付有依据的源码转换，但不能把静态检查写成 DM8 已运行通过。只有某条改写确实需要字段类型、模式或平台映射时，才标记该条所需信息。

用户补充注释要求后，已有两处修改新增 26 行注释，完整保留原 SQL 及改写说明，未改变可执行内容；最新哈希、行号和字节核验见 [sql-comment-preservation-log.json](<D:/work/company/太钢二炼钢/analysis/dameng-migration/sql-comment-preservation-log.json>)。此前审查中的源码行号是补注释前快照，应结合当前内容和日志定位。
