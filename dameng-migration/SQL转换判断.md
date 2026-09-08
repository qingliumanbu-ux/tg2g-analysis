# 后台 SQL 转换判断

> 2026-09-06 补充：下文源码行号为补注释前快照。已有两处转换现已完整注释保留原 SQL，新增 26 行说明且活动代码不变；当前位置见[注释日志](<D:/work/company/太钢二炼钢/analysis/dameng-migration/sql-comment-preservation-log.json>)。输入格式、时间口径等未决项见[人工复核清单](<D:/work/company/太钢二炼钢/analysis/dameng-migration/待人工复核SQL清单.md>)，最终状态按[主方案](<D:/work/company/太钢二炼钢/analysis/dameng-migration/后台SQL达梦适配可行性与执行方案.md>)区分。

日期：2026-09-04。按用户最新范围，只交付应用 SQL 的 DM8 适配；不以运行包、全库 DDL、样本或数据迁移为开始工作的前置。

## 已落地的首批源码转换

| 位置 | 原表达式与目标表达式 | 保持的含义 |
|---|---|---|
| [tmsme59_inq.cpp:86](<D:/work/company/太钢二炼钢/Server/TMSM/p_tmsm_7160/tmsme59_inq.cpp:86>) | DAYS(DATE(TIMESTAMP(end))) − DAYS(DATE(TIMESTAMP(start))) 改成 DATEDIFF(DAY, CAST(start AS TIMESTAMP), CAST(end AS TIMESTAMP))；单行辅助表改为 DUAL | 计算日历日差，参数仍按开始、结束顺序；跨午夜两秒仍跨一个日历日 |
| [wmfm01_inq.cpp:281](<D:/work/company/太钢二炼钢/Server/WMSM/p_wmsm_8170/wmfm01_inq.cpp:281>) | 三天日期序列中日期减 3 DAY、加 1 DAY、减 1 DAY 改为减 3、加 1、减 1；两处辅助表改为 DUAL | 继续生成 D−3、D−2、D−1；保留参数、别名、递归结构和外层关联 |

依据：DM 官方[函数说明](https://eco.dameng.com/document/dm/zh-cn/pm/function)定义 DATEDIFF 的日期边界计算；[日期运算](https://eco.dameng.com/document/dm/zh-cn/sql-dev/practice-date.html)说明日期可加减整数天；[查询语句](https://eco.dameng.com/document/dm/zh-cn/pm/check-phrases)说明 WITH 查询结构。

这是 2 个 SQL 表达式的源码转换，共 2 个文件、6 行变化；两个服务中还有其他待处理表达式，未把整文件或整服务标记为已适配。保留原文件编码和换行，未修改绑定方式、业务阈值、提交/回滚或其他业务逻辑。目标为 DM8，不声明改写后的共用分支仍支持所有旧数据库。

修改前后表达式和文件哈希见 [sql-conversion-log.json](<D:/work/company/太钢二炼钢/analysis/dameng-migration/sql-conversion-log.json>)。已进行静态差异核查，未执行数据库运行检查；没有把表无关常量样例当作已运行测试。

## 可以保留的写法

DM 官方文档包含 NVL、DECODE、TO_DATE、TO_CHAR、SUBSTR 等函数；普通 SELECT、INSERT、UPDATE、DELETE、JOIN、GROUP BY、UNION 等也不能因数据库产品变化一律改写。应核对具体参数和语义，保留已支持的表达式。函数依据见[官方函数说明](https://eco.dameng.com/document/dm/zh-cn/pm/function)。

对动态查询的 13 项首批记录，9 项在当前源码/自有 SQL 范围可以保留，4 项需要局部输入；通用执行端可保留，不意味着传入的任意 SQL 都已兼容。详见 [sql-dynamic-decisions.json](<D:/work/company/太钢二炼钢/analysis/dameng-migration/sql-dynamic-decisions.json>)。

## 继续转换的局部问题

- tmsme59_inq 的小时/分钟、垛位推荐等语句存在两参数 TIMESTAMPDIFF；目标官方函数为三参数形式。需要区分原表达式的跨月估算与业务希望的实际时长，不能机械替换后静默改变时间口径。这只影响相关表达式，不影响其他转换。
- DatabaseKind 选路、元数据类型分类和字符/字节长度依赖具体平台或字段语义；只标记该项所需映射/类型，不要求完整运行包和全库数据。
- TMMTP、TGCPMSI01/TED54、低代码数据集的部分 SQL 存在于源码外的配置中。只需取得实际 SQL 文本和参数定义后转换，不要求用户迁移配置表。
- C# 旧调用与同名输出程序集保留来源信息，不恢复注释调用、不以部署核对阻断其他源码转换。

12 项分支审查的当前裁定、候选表达式及来源见 [sql-branch-decisions.json](<D:/work/company/太钢二炼钢/analysis/dameng-migration/sql-branch-decisions.json>)。原迁移清单作为转换前扫描基线保留；本次两个文件的变化由转换日志补充，不能把基线哈希当成修改后的哈希。
