# WMSM SQL 达梦适配完成报告

报告日期:2026-09-06
**用户确认记录:2026-09-06 用户审核本报告后同意进入下一模块 TMSM(口头确认:"先继续完成我们的工作"),WMSM 遗留的 5 条动态文本缺口保持单列。**
模块边界:`Server/WMSM` 仓库全部 344 个 .cpp(含共享库 libWMSM 与 p_wmsm_8110/8120/8130/8140/8170/8180/8190 七个服务目录);另登记文件内出现的动态拼接来源(SQL_CONTEXT)。排除项:Client 端可映射 SQL(按交接说明属后续批次登记)、压缩包归档副本、TMSM/PSSM 等其他模块。
当前源码版本:WMSM 仓库 dev 分支,改动未提交;逐文件工作区 SHA-256 见 [sql-ledger.csv](<D:/work/company/太钢二炼钢/analysis/dameng-migration/sql-ledger.csv>) 的 `current_file_sha256` 列。

## 1. 本模块结论

| 状态 | 是/否 | 证据或未完成原因 |
|---|---|---|
| 模块审查完成 | **是** | 236 个含活动 SQL 的文件全部入账(共 1,464 条);其余文件经语句块+内联调用+存储过程三种形态扫描确认无活动 SQL。2026-09-06 自查轮:块检测升级为内容驱动后重扫,补转 13 块(substr2×10、POSSTR→INSTR×3),分母更新为 1,464 |
| 模块源码适配完成 | **是** | 1,459 条为"已转换已复核"或"可保留已复核";其余 5 条为动态文本未取得(见 §6),按规范不计入完成 |
| DM8 可执行已验证 | **否** | 无 DM8 环境,全部语句 runtime_status=未执行 |
| 结果等价已验证 | **否** | 同上,E3 需要原库与 DM8 或黄金基线 |

下一模块尚未开始。

## 2. SQL 处理统计

| 类别 | 数量 | 说明 |
|---|---:|---|
| 活动 SQL 总数 | 1,295 | 一条=一次 sql* 变量赋值(含反斜杠续行)或一次内联执行调用;`sqlwhere` 等拼接片段单独计数 |
| 可保留,已复核 | 1,184 | 其中 51 个文件的每处方言命中逐一判定(含 277 处保留型标记:无 NULL 搜索 DECODE、sysdate、nvl、ROWNUM 伪列、seq.NEXTVAL、FETCH FIRST、日期相减×24、小数天运算等);其余 182 文件为无方言命中的普通 CRUD |
| 已转换,已复核 | 106 | CHANGE-02(既有)—CHANGE-107(本轮),分布在 14 个文件 |
| 待人工复核 | 0 | 本模块无待人工业务问题 |
| 待局部信息/动态文本 | 5 | DYN-01 条目 ×5,见表 §6 |
| 范围外/历史材料 | 0 | if(false) 死代码模板已标注于可保留条目证据中 |

统计口径:注释中保留的原 SQL、CHANGE 头说明不计为活动 SQL;归档副本不重复计数。

## 3. 源码改动

| 文件 | 转换条目 | 主要内容 |
|---|---:|---|
| p_wmsm_8170/wmfm01_inq.cpp | 64 | CHANGE-02(既有)+03—65:递归 CTE 日期序列、合计查询、`- N DAY(S)`、SYSIBM→DUAL、DAYS→DATEDIFF、空值搜索 DECODE→CASE、二元标量 MAX→空值守卫 GREATEST、ROWNUM 别名→RN |
| libWMSM/f_wmsmsm_cranecmd_seq_upt.cpp | 19 | CHANGE-66—84:CREATE SEQUENCE 去掉 AS INT、NO CACHE→NOCACHE;`values nextval for`→`select <seq>.NEXTVAL from DUAL` |
| p_wmsm_8130/wmsm02_sg_inq.cpp | 10 | CHANGE-85—94:DB2 同义词 value(→nvl( |
| p_wmsm_8110/wmsm01gg_inq1.cpp | 2 | CHANGE-95—96:SUBSTR2→SUBSTR |
| p_wmsm_8140/wm00_stockNo2.cpp | 2 | CHANGE-100—101:SYSIBM.SYSDUMMY1→DUAL |
| p_wmsm_8110/wmsmsm11_inq.cpp | 1 | CHANGE-97:小写 decode(…,null,…)→CASE |
| p_wmsm_8130/wmsm01q0q_inq1.cpp | 1 | CHANGE-98:4 处 DECODE(…,NULL,…)→CASE |
| p_wmsm_8180/wmsmpcgz_inq.cpp | 1 | CHANGE-99:`INTERVAL '6' HOUR`→`6.0/24` |
| p_wmsm_8140/wmsmhrzc_auto.cpp | 1 | CHANGE-102:SUBSTR2(x,0,8)→SUBSTR(x,1,8) |
| p_wmsm_8140/wmsmrsl_inq.cpp | 1 | CHANGE-103:同上 |
| p_wmsm_8190/cm_p3t801_rcv.cpp | 1 | CHANGE-104:同上 |
| libWMSM/f_wmsmsm_cranecmd_update.cpp | 1 | CHANGE-105:`values nextval for`→NEXTVAL from DUAL |
| p_wmsm_8140/wmsmsc_inq1.cpp | 1 | CHANGE-106:SUBSTR2→SUBSTR |
| p_wmsm_8120/wmsmsmj3_rcm.cpp | 1 | CHANGE-107:动态拼接中含空串/NULL 搜索值的 DECODE→标准 CASE |

每处改写在源码中的格式:适配编号与语义说明 → 完整原 SQL 注释(含拼接与 C++ 表达式)→ `// DM8 SQL:` → 唯一活动 DM8 SQL。

编码、换行、差异检查:
- 全部文件 GB18030 编码、LF 换行保持;每处改动的注释块经脚本断言"去掉 `// ` 前缀后与改前逐行一致",转换规则经幂等断言。
- 14 个文件 `git diff --check` 通过;仅 f_wmsmsm_cranecmd_seq_upt.cpp 有 2 处提示为**原行既有行尾制表符**被完整保留所致(字节还原要求优先,非本次引入)。
- 全模块活动代码复扫:可转换模式(SYSIBM、天数后缀、DAYS()、NULL 搜索 DECODE、二元 MAX、ROWNUM 别名、AS INT、nextval for、value(、SUBSTR2、INTERVAL 字面量)残留为 **0**;剩余 277 处方言标记全部为有保留依据的类型。
- 仍为部分完成的文件/服务:无(动态文本 5 条见表 §6,不构成文件级未完成)。

## 4. 等价性证据

| 证据等级 | 覆盖 | 说明 |
|---|---|---|
| E1 静态契约复核 | 106/106 条转换 + 全部保留条目 | 规则级官方依据:T1/T2/T2b(DM 日期运算:日期与整数加减以天为单位;practice-date)、T3(IBM DAYS + DM DATEDIFF 函数手册 8.3)、T4/T12(标准 CASE/IS NULL;规避 DM DECODE 未记载的 NULL 匹配语义)、T5(IBM 标量 MAX"任一参数 NULL 则结果 NULL" + DM GREATEST 仅用于双非空分支,函数手册 8.1)、T6(DM ROWNUM 为伪列,查询语句 4.15)、T7(DM CREATE SEQUENCE 官方子句集,无 AS 类型子句)、T8(DM 序列伪列 NEXTVAL + FROM DUAL)、T9(DM 空值函数表无 VALUE,NVL 两参数"返回第一个非空的值")、T10(DM 字符串函数表无 SUBSTR2,SUBSTR 按字符;位置 0→1 显式化)、T11(DM 日期运算文档无 INTERVAL 字面量,官方示例用小数天)、T12(同 T4,动态拼接)。DAYOFWEEK 编号经官方示例(2023-01-01=周日=1)与 DAYNAME 交叉印证。参数、结果列、连接、过滤、排序、聚合逐项保持 |
| E2 DM8 可执行 | 0/1,295 | 未执行(无 DM8 环境) |
| E3 差异等价 | 0 | 未执行 |
| E4 应用路径验证 | 0 | 未构建、未运行 |

E2/E3 环境:无;未执行。
自动比较方法:不适用(未执行)。
失败及差异:无执行记录,无失败记录;静态推导不能替代 E2/E3。

## 5. 需要用户人工复核

**本模块无待人工业务问题。** 既有 HR-001、HR-002 属 TMSM(tmsme59_inq),HR-003 属 PSSM(f_pssm27_upd_plno_n),不在本模块范围,等待用户答复中。

## 6. 局部资料与外部 SQL 缺口

| SQL 编号 | 所需最小信息 | 提供方 | 缺失时的状态 |
|---|---|---|---|
| DYN-wmfm01_inq-01(wmfm01_inq.cpp L4561) | 表 `S_<tbl>` 中 SQL_CONTEXT_01/02 的实际 WHERE/ORDER 文本及参数定义 | 应用/配置负责人 | 保持"待局部信息",取得后按对应模块规则转换 |
| DYN-fosmt00b_inq-01(fosmt00b_inq.cpp L332) | 同上(同类数据集来源) | 同上 | 同上 |
| DYN-wmsmsm20bd_bat-01(wmsmsm20bd_bat.cpp L503) | 同上 | 同上 | 同上 |
| DYN-wmsmsm20bm_bat-01(wmsmsm20bm_bat.cpp L491) | 同上 | 同上 | 同上 |
| DYN-wmsmshow_inq-01(wmsmshow_inq.cpp L45) | 同上 | 同上 | 同上 |

通用执行器本身可保留;传入文本未取得前不能记为已适配。

## 6b. 自查轮更新(2026-09-06)

用户要求全面自查后,本模块补转 13 块:`f_wmsm_slab_no`(substr2×4,含位置 0→1)、`wmsm01_ponoslab_inq`(×2)、`wmsm_heatno_turn`(×5,含 UPDATE 批量改号语句)、`wmsmsc_inq`(×1)、`fosmt00b_inq`(substr2×1)。台账更新为 1,464 行(可保留 1,340/已转换 119/动态 5);残留复扫 0;原 §3—§5 数字以本轮为准。另确认:REGEXP_LIKE、LISTAGG 等 WMSM 在用函数均为 DM 官方支持,判定保留。

## 7. 下一步建议

建议下一个模块:**TMSM**。理由:TMSM 既有 CHANGE-01 已在位,同函数尚有 HR-001(输入时间格式)、HR-002(小时/分钟口径)两项人工复核等待答复,可借模块推进一并处理;规模(338 个候选文件)小于 WMSM。TMSM 中 HR-001/HR-002 未获答复前,对应表达式继续挂起,其余确定项照常处理。

等待用户审核本报告并决定后再开始。
