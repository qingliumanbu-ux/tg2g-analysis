# taigang-dm8-sql 隔离正向验证

日期：2026-09-06。已实际使用 `analysis/skills/taigang-dm8-sql/SKILL.md` 处理隔离样例，交付 1 条确定转换及 1 条待人工复核记录。本样例属于部分完成，不能宣称该模块的全部 SQL 已适配完成。构建、数据库执行和应用运行均未执行。

## 范围与执行决定

- 输入仅为 [fixture.cpp](<D:/work/company/太钢二炼钢/analysis/skill-forward-check/fixture.cpp>)，共 2 个函数、2 条完整活动 SQL、2 个执行入口。没有条件拼接变体、DatabaseKind 分支、外置 SQL 或归档输入；该结论仅限这份样例。
- 用户确认 BM2 已适配，API 声明在样例外；保留 `@DATE_TIME`、`@FACTORY_DIV` 和现有 BM2 调用方式，不补写绑定、连接或事务代码。
- 已读 Skill、`references/project-context.md`、`references/comment-format.md`，以及项目上下文要求的主方案、README、官方资料复核。主项目统计和业务结论不作为本例事实；本例使用独立编号 `FWD-SQL-*`、`FWD-REVIEW-*`，不复用主项目人工复核编号。
- 工作区根目录不是 Git 仓库。该隔离样例没有可用的 Git 基线，改前文件本身及 SHA-256 是可信基线；没有操作其他子仓库。
- 只新写 [fixture.converted.cpp](<D:/work/company/太钢二炼钢/analysis/skill-forward-check/fixture.converted.cpp>) 和本报告；没有修改输入文件、业务源码、Skill 或项目台账，没有安装任何工具。
- 目标 DM8 小版本、兼容模式和相关参数未知。使用 DM8 官方公开手册做静态判断，未自行选择或修改兼容模式；只将配置相关的 DELETE 挂起。

## 逐条处理记录

| 编号 | 来源及完整模板位置 | 执行入口 | 参数和结果 | 分支影响 | 处理状态 | 运行状态 |
|---|---|---|---|---|---|---|
| FWD-SQL-001 | `fixture.cpp`，`query_previous_date`，5–7 行，C++ 相邻字符串字面量 | 原文件 8–10 行 `SetCommandText → ExecuteReader → Close` | `@DATE_TIME` 格式为 YYYYMMDD；返回一行、一列 `PREV_DATE`，为前一日的 YYYYMMDD 字符串 | 无分支；该函数活动 SQL 改为 DM8 写法 | 已转换已复核，仅静态 | 未执行 |
| FWD-SQL-002 | `fixture.cpp`，`clean_empty_plans`，15–17 行，C++ 相邻字符串字面量 | 原文件 18–19 行 `SetCommandText → ExecuteNonQuery` | `@FACTORY_DIV` 约束工厂；删除 T_PLAN 中满足计划号条件的行；无查询结果列 | 无分支；活动 SQL 保留原文，等待语义结论 | 待人工复核，关联 FWD-REVIEW-001 | 未执行 |

### FWD-SQL-001：前一日查询

完整原 SQL 已保留在转换文件 8–10 行，包括 `CString sqlstr =`、两段字符串及分号；活动 SQL 位于 12–14 行，说明与编号位于 5–7 行：

```sql
SELECT TO_CHAR(TO_DATE(@DATE_TIME,'YYYYMMDD') - 1, 'YYYYMMDD') AS PREV_DATE FROM DUAL
```

改动只有两项：`- 1 DAY` 改为整数天减法 `- 1`，`SYSIBM.SYSDUMMY1` 改为 `DUAL`。日期契约直接来自输入文件第 2 行，并非复制 Skill 示例或推测业务规则。DM 官方日期运算文档支持天数加减，也展示了使用 DUAL 的日期表达式；IBM 定义确认 SYSDUMMY1 是单行辅助表。本查询不读取辅助表字段，因此据此判断可以保持一行输出。[DM 日期运算](https://eco.dameng.com/document/dm/zh-cn/sql-dev/practice-date.html)、[IBM SYSDUMMY1](https://www.ibm.com/docs/en/db2-for-zos/13.0.0?topic=tables-sysdummy1)

TO_DATE 的中间返回类型可能受模式影响，但本例显式给出年月日格式，缺失的时分秒补零，并通过 TO_CHAR 输出年月日字符串；没有直接向 BM2 返回日期类型。因此，本次静态判断不把未知兼容模式作为该条转换的全局前置条件。目标实例上的实际表现仍未验证。[DM 函数手册](https://eco.dameng.com/document/dm/zh-cn/pm/function.html)

供后续使用的理论期望（未在 DM 执行，也不记作测试通过）：

| DATE_TIME | 理论 PREV_DATE | 覆盖点 |
|---|---|---|
| 20260906 | 20260905 | 普通日期 |
| 20260301 | 20260228 | 非闰年月初 |
| 20240301 | 20240229 | 闰年二月 |
| 20260101 | 20251231 | 跨年 |

这里只确认源码公开的格式和日期口径，没有扩展无效输入处理或改变输入验证逻辑。

### FWD-SQL-002 / FWD-REVIEW-001：清理计划号的删除范围

当前完整 SQL 出处为输入文件 15–17 行，转换文件仍完整保留在 22–24 行；函数为 `clean_empty_plans`，表达式锚点为 `TRIM(PLAN_NO) IS NULL`：

```sql
DELETE FROM T_PLAN WHERE FACTORY_DIV = @FACTORY_DIV AND TRIM(PLAN_NO) IS NULL
```

原意证据只有函数名和这个条件。它可能是在清理真正的 NULL，也可能意图清理空串与仅有普通空格的计划号，现有材料不能代选。DM 官方说明默认模式下空串与 NULL 有区别，兼容模式会影响存储和操作结果，故不能因函数语法可识别就认定该 DELETE 的命中集合已保持。[DM Oracle 移植说明](https://eco.dameng.com/document/dm/zh-cn/start/oracle_dm)

**一个待用户回答的问题：在指定 FACTORY_DIV 下，PLAN_NO 为 NULL、空串或仅由普通空格组成时，分别应当删除还是保留？**

不同业务选择的理论差异如下。表格描述意图，不是当前目标库的实际结果；如果空串已被目标模式存储为 NULL，两类值可能无法再区分。

| 计划号逻辑状态 | 只删除真正 NULL | 删除 NULL、空串及仅普通空格 |
|---|---|---|
| NULL | 删除 | 删除 |
| 空串 | 保留（能与 NULL 区分时） | 删除 |
| 仅普通空格 | 保留 | 删除 |
| P001 或两侧带空格的有效编号 | 保留 | 保留 |

没有足够业务证据推荐其中一种删除范围。收到结论后可按局部前提选择写法：

- 若只删除真正 NULL，候选条件为 `PLAN_NO IS NULL`，但需确认目标存储能否区分空串与 NULL。
- 若删除三种空值状态，候选条件为 `(TRIM(PLAN_NO) IS NULL OR TRIM(PLAN_NO) = '')`，前提是 PLAN_NO 的实际类型支持该字符语义，并按目标模式核对其结果。OR 必须包含在括号里，继续与 `FACTORY_DIV = @FACTORY_DIV` 做 AND，不能扩大到其他工厂。
- 若原条件在既定模式和字段契约下已满足用户结论，可以保留现有 SQL，无需制造重复历史块。是否包括制表符、全角空格等其他字符不在当前普通空格语义内，不能自行扩大。

上述均为待确认候选，未写入活动代码。当前建议是暂时保持该语句原样，仅完成确定的日期查询转换。

局部资料需求，仅用于关闭本条：目标 DM8 小版本及既定兼容/空串配置、T_PLAN.PLAN_NO 的字段类型和空串存储规则。无需全库 DDL、构建包、连接信息或真实生产数据。

用户结论：未收到。确认人：未填写。后续处理：收到真实业务结论和所需局部契约后，按完整 SQL 单位保留原句、实施必要改写并复核；任何人工结论都不代替 DM 实际执行证据。

## 静态验证证据

采用对这份已逐行阅读样例适用的检查方式；它仅含普通 C++ 字符串和独占行 `//` 注释，没有宏续行、原始字符串或块注释，不将该检查器推广为通用 C++ 解析器。

| 检查 | 实际结果 |
|---|---|
| 原 SQL 注释完整性 | 去掉转换文件 8–10 行新增的注释标记后，与输入 5–7 行完整赋值逐字符一致 |
| 活动代码差异 | 排除独占行注释后，转换文本严格等于输入活动文本仅执行两处预期 SQL 替换的结果 |
| 待复核 DELETE | `clean_empty_plans` 函数整体及文件尾部与输入逐字节一致 |
| 活动 SQL 数 | 仍为 2 个完整赋值及 2 个执行入口；不是 3 条 SQL |
| 日期旧模式 | `SYSIBM.SYSDUMMY1`、`- 1 DAY` 只存在于原 SQL 注释，活动代码中均为 0；历史命中不作为活动残留 |
| 未关闭的活动条件 | `TRIM(PLAN_NO) IS NULL` 保持 1 处，已登记 FWD-REVIEW-001，不追求关键词清零 |
| 参数、别名与控制流 | 参数标记、`PREV_DATE` 列名、SQL 拼接边界、BM2 调用及事务位置无额外变化 |
| 编码与换行 | 输入为纯 ASCII 字节（兼容 UTF-8）、无 BOM、20 个 LF；输出仍为纯 ASCII、无 BOM、27 个 LF，均无 CR；文件大小 648 → 1005 字节 |
| 输入保护 | 改前改后 SHA-256 一致，输入文件没有修改 |
| 构建/运行 | 未构建运行包，未编译样例，未创建或连接数据库，未执行 SQL |

版本指纹：

- `fixture.cpp`：`3292171B3AC5A1E1A3A0E49F3A31B6CEBDE62281C86F15F4DEFB3E31D1588F4D`
- `fixture.converted.cpp`：`C20C1EADCA5D980ACB690AB8CC5ABE219ED0F2CA903F356848077E9EBCF3FC45`

统计分母：1 份输入文件，2 条完整活动 SQL；已转换已静态复核 1 条，待人工复核 1 条，待局部信息依附同一待复核条目，不重复增加分母。原 SQL 历史注释为 1 个完整模板。当前没有源码外 SQL 缺口，仅有已公开的外部 BM2 声明边界和上述局部语义资料需求。

官方函数手册直连抓取超时，本轮从官方域名搜索返回的该手册正文检索到 TO_DATE 返回类型和缺省时分秒规则；日期运算、查询语句、Oracle 移植说明可直接读取。全部为公开文档证据，未把网页示例结果当作本机 DM 执行结果。

## 对 Skill 的实际观察

这次正向执行没有发现必须修正后才能继续的行为缺陷：Skill 足以引导完整原句保留、确定项推进、空值 DELETE 暂挂、编码保护、独立运行状态以及不夸大范围完成度。

可改进之处是引用入口偏重：即使只有两条隔离 SQL，项目上下文仍要求读取主方案和项目 README；其中真实项目统计、HR 编号与本例无关。后续可在 Skill 增加“明确的隔离样例使用本地编号与本地交付记录”的简短分流，以降低误继承业务结论的可能。本次依照用户明确的隔离边界处理，没有修改 Skill 或请求无关主项目资料。

本次验证只覆盖静态 C++ 相邻字符串、日期步长、辅助表和空值删除语义；不证明该 Skill 已覆盖复杂动态 SQL、各语言注释、数据库分支或真实 DM8 运行。
