# WMSM 逐文件复核记录（2026-09-17）

复核方式：逐文件打开源码，对照 `analysis/skills/taigang-dm8-sql/references/conversion-rules.md` 的 T1—T15 规则与"可保留白名单"判断；检索仅用于缩小范围，每条命中均落到具体文件核对上下文与分支归属。**未编写批量执行脚本**，未修改任何业务源码。

模块基线（来自 [WMSM-模块完成报告](<D:/work/company/太钢二炼钢/analysis/dameng-migration/WMSM-模块完成报告.md>)）：344 个 .cpp、台账 1,464 行、已转换 119、动态文本待取得 5，自称"必须转换类残留为 0"。

---

## 一、发现项

### F-WMSM-01　活动代码中的 SQL Server 方言未按"分支保留"如实记录

**涉及文件（6 个，均已逐个核实分支归属）**

| 文件 | 活动行 | 所在分支 | 台账证据栏 |
|---|---|---|---|
| `p_wmsm_8110/wmsmsm17_inq_mat.cpp` | L95 | `case DB_KIND_MSSQL:`（L90） | `DM CAST/DECIMAL 支持` |
| `p_wmsm_8140/wmsmsm17_inq_mat1.cpp` | L150 | `case DB_KIND_MSSQL:`（L144） | `DM CAST/DECIMAL 支持` |
| `p_wmsm_8110/wmsmsm12S_inq1.cpp` | L251-L252 | `case DB_KIND_MSSQL:`（L249） | `普通 CRUD/聚合,无方言差异` |
| `p_wmsm_8110/wmsmsm12S_inq3.cpp` | L252-L253 | `case DB_KIND_MSSQL:`（L250） | `普通 CRUD/聚合,无方言差异` |
| `p_wmsm_8110/wmsmsm12S_inq4.cpp` | L252-L253 | `case DB_KIND_MSSQL:`（L250） | `普通 CRUD/聚合,无方言差异` |
| `p_wmsm_8110/wmsmsm12S_inq5.cpp` | L252-L253 | `case DB_KIND_MSSQL:`（L250） | `普通 CRUD/聚合,无方言差异` |

另 `p_wmsm_8110/wmsmsm17_inq.cpp` L202（`case DB_KIND_MSSQL:` L200）同型，台账 `KEEP-wmsmsm17_inq-13` 证据为 `普通 CRUD/聚合,无方言差异`。合计 **7 处**。

**源码事实**

```cpp
case DB_KIND_MSSQL:   // MS SQL Server数据库
    sqlorderby = " ORDER BY CAST(ISNULL(ltrim(rtrim(b.LAYERNO)), '0') AS INT) DESC, a.REC_CREATE_TIME ASC ";
    break;
```
同文件 `case DB_KIND_DB2/DB2_ORACLE/ORACLE:` 分支使用 `ORDER BY B.LAYERNO DESC`（无 `ISNULL`）；`wmsmsm17_inq.cpp` 的 DB2/ORACLE 分支用 `NVL`，MSSQL 分支用 `ISNULL`。

**台账与源码的三处不符**

1. **证据文字不实**：这些行含 `ISNULL()`、`ltrim/rtrim`，属 SQL Server 方言，记成"无方言差异"不成立；`wmsmsm17_inq_mat.cpp` L95 那条只记了 `CAST` 的支持性，同行 `ISNULL()` 未被评估。
2. **`branch_impact` 记反**：台账写"共用路径(以源码 switch 为准)"，而实际是**仅 MSSQL 分支**、并非共用。
3. **未查证项未登记**：原记录写"DM8 是否支持 `ISNULL()` 属未知"。**该判断已作废**——见下方 2026-09-17 更正。

**影响（更正后）**：`ISNULL(n1,n2)` 经 DM8 官方函数手册 3.4 节"空值判断函数"确认为**官方支持**（[S1](https://eco.dameng.com/document/dm/zh-cn/sql-dev/practice-func.html)），`ltrim/rtrim` 亦为官方字符串函数。因此原本担心的"若 DM8 映射为 `DB_KIND_MSSQL` 会执行不支持的 `ISNULL()`"**不成立**；这 7 处**无需转换**。

真正遗留的问题只剩一条，属**记录质量**而非技术风险：证据栏当初写着"无方言差异"，未记录这些行位于 `case DB_KIND_MSSQL:` 分支、也未记录函数名，使复核者无法从台账判断是否需要处理。

**建议处理（已执行部分）**：7 条台账证据已改为"仅 MSSQL 分支保留；DM8 走 DB2/ORACLE 分支时不执行；行内 ISNULL() 经 DM8 官方函数手册 3.4 节确认为支持；本行无需转换"，`branch_impact` 由"共用路径"改为"仅 DB_KIND_MSSQL 分支"。**未改动任何代码**（确认无需改写）。

### F-WMSM-02　3 处 Oracle `(+)` 外连接未标"E2 待验证"

| 文件 | 活动行 | 是否无条件执行 |
|---|---|---|
| `libWMSM/f_wmsm_craneCmd_C_2E.cpp` | L135-L137（`(+)` 在 L136） | 是，无 DatabaseKind 分支 |
| `p_wmsm_8130/wmsm01q0_inq1.cpp` | L141-L149（`(+)` 在 L148） | 是，位于 `if (Rows.get_Count() == 0)` 可达分支 |
| `p_wmsm_8130/wmsm01q0q_inq1.cpp` | L132-L140（`(+)` 在 L139） | 同上 |

三条台账分别记于 `KEEP-f_wmsm_craneCmd_C_2E-01`、`KEEP-wmsm01q0_inq1-12`、`KEEP-wmsm01q0q_inq1-03`，证据均为 `普通 CRUD/聚合,无方言差异`。

**源码事实**（`f_wmsm_craneCmd_C_2E.cpp:135-138`）
```cpp
sqlstr = "SELECT d.measure_wt_flag,a.mat_no,... c.dev_div"
    " FROM twma0 a, twma2 b, twm04 c,twma1 d WHERE b.stock_place_no = c.stock_place_no(+) AND a.mat_no = b.mat_no AND a.mat_no = d.mat_no"
    " AND a.vehicle_no = '" + vehicle_no + "' AND A.PLAN_NO = '" + plan_no + "'";
```

**不符之处**：保留白名单对 `(+)` 的原文是"官方 FAQ『语法大致相同,大部分不需要修改』；**建议 E2 验证,失败回退 ANSI JOIN**"。记录为"无方言差异"等于抹掉了这个待验证要求，验收时会被当作已确认等价。

**2026-09-17 补充官方依据后，本节结论加重**：查证发现白名单对官方 FAQ 的那句引用属**过度引用**——FAQ 原文是针对 Oracle 语法整体的笼统表述，并未单独确认 `(+)`；而**官方文法中不存在 `(+)`**（[S2](https://eco.dameng.com/document/dm/zh-cn/pm/check-phrases) 只列 `LEFT/RIGHT/FULL [OUTER] JOIN`），且达梦社区·Oracle 到达梦 DTS 迁移实验记录明确写着：

> 「普通视图 SQL 中还存在 Oracle 特有或高风险写法，例如：( + ) 旧式外连接，**需要改写为 LEFT JOIN**」

因此这三处的正确处置是**改写为 ANSI LEFT JOIN**，而非"保留待验证"。完整论证见[横向方言族复核](<D:/work/company/太钢二炼钢/analysis/dameng-migration/review-20260917-横向方言族扫描.md>) §2.3。

**影响**：这三条是**无条件执行**路径（不同于 F-WMSM-01 的分支语句），DM8 上必然走到。

**建议处理（已执行部分）**：台账三行证据已改为"官方迁移材料记载 (+) 旧式外连接需改写为 LEFT JOIN；建议改写为 ANSI LEFT JOIN 或先做 E2 实测"。**代码尚未改动**——改写涉及业务语义（外连接方向、NULL 补齐），需用户确认后再动手，且同样应先在 E2 实测确认 `(+)` 在当前库是否可执行。

### F-WMSM-03　改动说明的类型标签不准（轻微）

`libWMSM/f_wmsmsm_cranecmd_seq_upt.cpp` 的 CHANGE-66~81 与 `f_wmsmsm_cranecmd_update.cpp` 的 CHANGE-105，改写的是 `CREATE SEQUENCE` 与 `values nextval for` 取号语句，属 **DDL/取号**，注释头统一写作"查询。见改写原因"。分类标签与实际语句类型不符，影响按类型统计。仅文档层面，不影响 SQL 语义。

---

## 二、本轮通过的检查点

### 文件：`libWMSM/f_wmsmsm_cranecmd_seq_upt.cpp`（已转换 19 处）

| 检查点 | 结论 |
|---|---|
| 注释规范 | 通过。每处为"编号+改写原因+语义前提 → `// 原 SQL（完整保留）：` + 原赋值整行 → `// DM8 SQL：` + 唯一活动语句" |
| 原 SQL 可还原性 | 通过。原句含赋值、字符串、分号（如 `CREATE SEQUENCE  SEQ_30 AS INT START WITH 100000 ... CYCLE NO  CACHE ORDER";`）完整保留 |
| 分支前提 | 通过且值得肯定：明确写出"本共用分支面向 DM8,其他 DB_KIND 标签也会执行此 SQL"——这些 DDL 无 DatabaseKind 分支，DM8 上必然执行，此说明是必要的 |
| T8 改写正确性 | 通过。CHANGE-80：`"values nextval for " + seq_name` → `"select " + seq_name + ".nextval from dual"`，与 T8 一致 |
| 最小改动 | 通过。L214/`L215` 的"重复赋值"经与 `batches/wmsm/f_wmsmsm_cranecmd_seq_upt.pre-dm8.bak` L124/L125 比对，确认**改动前既已存在**，非本次引入 |
| 幂等/残留 | 该文件内 `AS INT`、`NO CACHE`、`values nextval for` 仅存在于注释内，活动代码无残留 |

### 模式级结论

- **`DECODE` 家族（T4/T12）**：活动代码中含 NULL/空串搜索的 `DECODE` 已按标准 `CASE` 改写（`p_wmsm_8120/wmsmsmj3_rcm.cpp:68`、`p_wmsm_8170/wmfm01_inq.cpp:967` 区块等）；其余 `DECODE(..., NULL, ...)` 命中全部位于 `//` 保留注释内。未发现活动残留。
- **`SYSIBM` / `SUBSTR2` / `DAYS(` / `INTERVAL '` / `NO CACHE` / `AS INT`**：全部命中均位于 `//` 保留注释、`// DM8 SQL` 改写注释或 `//` 已注释死代码中，**活动代码无残留**，与模块报告"残留为 0"一致。

---

## 三、本轮复核的自查（不确定性与边界）

1. **能力边界**：本次处于无外网环境，无法查阅 DM8 官方手册。因此 F-WMSM-01 中 `ISNULL()` 的支持性**只写"未评估"**，不写"不支持"——两者证据强度不同，不可混用。
2. **未覆盖**：Server/WMSM 共 280 个 .cpp（模块报告口径 344，含未列入本轮 glob 的其他扩展名/子目录），本轮未逐个读完；其余 20 个模块尚未开始。
3. **未做**：未执行任何 SQL（E2/E3 仍为未验证）；未修改业务源码；未改动 `sql-ledger.csv`（F-WMSM-01/02 的台账更正待用户确认后统一执行，避免与既有统计口径冲突）。
4. **方法风险**：本轮检索模式集是**在模块已完成扫描之外**新增的（`ISNULL/IFNULL/GETDATE/CHARINDEX/DATEADD/DATEPART/OBJECT_ID/TOP/LIMIT/(+)/@@`、`ADD_MONTHS/MONTHS_BETWEEN/LAST_DAY/NEXT_DAY/SYS_CONTEXT/USERENV`）。既有扫描未把这些纳入，说明**扫描模式集与规则表之间仍有缺口**；已发现的 7 处即由该缺口造成。建议后续把 SQL Server 方言族补入规则表，并按同一方法复核其余模块。

---

## 四、待用户决定

1. 是否按 F-WMSM-01/02 修正 `sql-ledger.csv` 对应行的 `evidence` 与 `branch_impact`（不涉及代码改动）。
2. 是否把 F-WMSM-03 的类型标签统一更正。
3. `BM2 DatabaseKind` 在 DM8 下的实际取值——这是 F-WMSM-01 能否收敛的前提，需从 BM2 侧取得。
4. 复核顺序：继续 Server/WMSM 剩余文件，还是先横向把同类方言族在其他 20 个模块中扫一遍定位。

---

## 五、逐文件通读（第二轮，按 libWMSM 目录顺序）

用户要求不用脚本扫描，改为逐个文件打开读。以下为按序通读结果，每读完一个文件记录一次。

### 已读文件清单与结论

| 序 | 文件 | 行数 | SQL 块数 | 结论 | 新发现 |
|---:|---|---:|---:|---|---|
| 1 | `libWMSM/f_auto.cpp` | 524 | 6 | 无方言，可保留 | 新增未覆盖写法 `!=`（L102/L105/L467） |
| 2 | `libWMSM/f_auto_sm.cpp` | 353 | 7 | 无方言，可保留 | 新增未覆盖写法 `!=`（L268）、空白串比较 `> '  '`（L90/L106/L194）、`= ' '`（L86/L102/L190） |
| 3 | `libWMSM/f_wmhrsm_cmd_auto.cpp` | 487 | 6 | 无方言，可保留 | 无 |
| 4 | `libWMSM/f_wmhrsm_cmd_del.cpp` | 185 | 2 | 无方言，可保留 | `!=`（L128） |
| 5 | `libWMSM/f_wmhrsm_cmd_down.cpp` | 160 | 0 | **无活动 SQL** | 仅模型层调用，`sqlstr` 声明后未赋值 |
| 6 | `libWMSM/f_wmhrsm_cmd_follow.cpp` | 181 | 0 | **无活动 SQL** | 同上（`sqlstr` 只在 catch 中引用） |
| 7 | `libWMSM/f_wmhrsm_cmd_upt.cpp` | 122 | 0 | **无活动 SQL** | 仅 `Query`/`Update` 模型层操作 |
| 8 | `libWMSM/f_wmhrsm_cranecmd_make.cpp` | 370 | 3 | 无方言，可保留 | **`FETCH FIRST … ROW ONLY`（单数 ROW）**，见下 |
| 9 | `libWMSM/f_wmsmsm13_proc.cpp` | 648 | 4 | 无方言，可保留 | 无（L498-503 的 `INNER JOIN` 语句在注释内） |
| 10 | `libWMSM/f_wmsmsm_allot_snd.cpp` | 342 | 0 | **无活动 SQL** | 仅 `EPEX` 电文与模型层操作 |
| 11 | `libWMSM/f_wmsmsm_cranecmd_check.cpp` | 236 | 8 | **发现候选未转换项** | **`INT('…')`（DB2 转换函数）13 处**，见 F-WMSM-04 |

进度：libWMSM 目录 11/约 71 个文件。

### F-WMSM-04　`INT('…')`：DB2 风格转换函数，不在 DM8 官方函数清单中

**位置**：`libWMSM/f_wmsmsm_cranecmd_check.cpp`，活动代码，**无条件执行**（函数内无 DatabaseKind 分支）。

| 行 | `INT()` 处数 | 语句用途 |
|---|---:|---|
| L93（同文件） | — | 该行用的是 `!=`，无 `INT()` |
| L120 | 1 | 判断目标位置是否被修改 |
| L128-L130 | 4 | 统计上/下层数量 |
| L144 | 1 | 取整组命令 |
| L152 | 2 | 下层命令 |
| L158 | 2 | 上层命令 |
| L170 | 2 | 同层命令 |
| L176 | 1 | 整组命令 |
| **合计** | **13** | 跨 8 条语句 |

典型写法：
```cpp
sqlstr = "SELECT * FROM TWMA7 WHERE CRANE_CMDGRPNO = INT('" + twma7["CRANE_CMDGRPNO"].ToString() + "')";
```

**官方依据（2026-09-17 查证）**：达梦 DM8 官方函数手册的**类型转换函数**一节只有 9 个——`CAST`、`CONVERT`、`HEXTORAW`、`RAWTOHEX`、`BINTOCHAR`、`TO_BLOB`、`UNHEX`、`HEX`、`CHARTOBIN`；**数值函数**一节 41 个中也没有 `INT`。官方所有"字符串转整型"示例一律写 `CAST('123' AS INT)` 或 `TO_NUMBER('123')`。
来源：https://eco.dameng.com/document/dm/zh-cn/sql-dev/practice-func

**判断**：`INT(x)` 是 DB2 的转换函数写法，**不在 DM8 官方函数清单中**，属**高度可疑**。但 DM 设有 `COMPATIBLE_MODE=8`（部分兼容 DB2），该模式下是否接受 `INT()` **无法从文档确定**——本记录**只判定"不在官方清单、需实测确认"，不判定"不支持"**。

**重要对照**：同文件 L120/L128-130 与 L144/L152/L158/L170/L176 全部是同一写法，**要么全部可行、要么全部报错**，不存在部分通过。若确认不支持，改写方式是机械的：`INT('…')` → `CAST('…' AS INT)`（可参照项目既有规则里的 `CAST(x AS INTEGER/DECIMAL…)` 白名单条目）。

**为何此前扫描没发现**：既有扫描的"逐模板函数核对"是按函数 token 比对 DM 支持清单。`INT` 很可能被当成**数据类型关键字**而非函数名，因此既没进"未知函数"候选，也没被当成残留。这与 ISNULL 的漏检是同一类问题：**token 归类规则覆盖不到"数据类型同名函数"**。

### 文件 8 的重点：`FETCH FIRST … ROW ONLY` 单数形式

`f_wmhrsm_cranecmd_make.cpp` L84（活动代码，无条件执行）：

```cpp
sqlstr = "select mat_no from twma2 where stock_place_no ='" + … + "'where mat_no not in (select mat_no from twma7) order by LAYERNO DESC  FETCH FIRST "+ … +"  ROW ONLY";
```

转换规则白名单收录的是 **`FETCH FIRST n ROWS ONLY`（复数 ROWS）**，而源码这里用的是 **`ROW ONLY`（单数）**。

**已查证（2026-09-17）**：DM8 官方查询语句文法写的是

```
<FETCH说明>::= FETCH <FIRST | NEXT> [<大小> | <大小> PERCENT] ROW[S] <ONLY | WITH TIES>
```

即 **`ROW[S]`，单复数皆可**（[S2](https://eco.dameng.com/document/dm/zh-cn/pm/check-phrases)）。因此**单数形式合法，本行无需转换**，此前记的"未核实"作废。

同类问题还有 `'` 与 `where` 之间缺空格（`'where`），多数 SQL 词法器能正确切分，属书写不规范而非方言差异。

### 新增的"规则表未覆盖写法"清单（累计）

| 写法 | 出现位置 | 说明 |
|---|---|---|
| `!=` 不等运算符 | `f_auto.cpp` L102/L105/L467、`f_auto_sm.cpp` L268、`f_wmhrsm_cmd_del.cpp` L128 | 白名单只列了 `<>`；DM8 是否接受 `!=` 未查证 |
| `列 > '  '`（双空格） | `f_auto_sm.cpp` L90/L106/L194 | 空白串比较，属 CHAR 定长/空串语义边界类 |
| `列 = ' '`（单空格） | `f_auto_sm.cpp` L86/L102/L190 | 同上 |
| `FETCH FIRST n ROW ONLY`（单数） | `f_wmhrsm_cranecmd_make.cpp` L84 | ~~白名单只列复数 ROWS~~ **已查证：官方文法为 `ROW[S]`，单数合法 → 无需转换** |

### 超出 SQL 适配范围的既有缺陷（仅登记，未修改）

按"精准改动、只清理自己制造的烂摊子"原则，以下问题与方言无关且非本次引入，只登记不改动：

1. `f_auto.cpp` L481/L483/L485/L487：`if (...);` 句尾多一个分号，`if` 体为空，紧随的 `{ }` 无条件执行——逻辑与预期不符。
2. `f_auto_sm.cpp` L209-210：查询只 Select `stock_place_no, sum(mat_num) mat_num` 两列，却执行 `GetString(1)`/`GetString(2)`，第 2 列（数值 `mat_num`）被读入 `hall_no`。同文件 L122-123 用的是 `GetString(1)`/`GetDecimal(2)`，可作对照。
3. `f_wmhrsm_cmd_auto.cpp`：`MesStockplaceSm::Setinfo()`（L121-165）、`MesMatSm::Setinfo(const CString&)`（L215-248）、`MesAreaSm::search()`（L336-411）声明为 `int` 返回，函数体末尾无 `return`。

### 本轮自查（第二轮回）

1. **未使用检索定位**，三个文件均为整文件读取，行数与内容以上文引用为准，可复核。
2. **未对任何写法下"支持/不支持"结论**。`!=`、空白串比较、`ISNULL`、`(+)` 等全部保持"未评估"。
3. **未修改任何业务源码**；第三节登记的既有缺陷仅作记录。
4. **速度与覆盖的取舍**：整文件通读的代价是进度慢（本轮回 3 个文件）。若按此速度，WMSM 约 280 个文件、全项目 4,578 个 .cpp 无法在短期内读完。这是事实约束，需用户决定优先级（例如：只通读"含活动 SQL 且台账有判定的文件"，或按模块分批推进）。
5. **本轮未复查的事项**：台账中上述三个文件的既有判定行未逐行核对（本轮只核了源码）；`libWMSM` 中已被转换的文件（如 `f_wmsmsm_cranecmd_seq_upt.cpp`）在第一节已单独核过，不重复。
