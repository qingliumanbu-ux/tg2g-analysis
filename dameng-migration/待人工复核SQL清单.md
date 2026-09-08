# 待人工复核 SQL 清单

日期：2026-09-06。首批 3 项，后续按相同格式追加。只登记无法从现有代码确定的业务口径或输入约定；其他明确的 SQL 继续转换。

**以下差异示例均为理论推导，未在 Oracle 或 DM8 执行。** 你只需回答每项的一个问题；确认后按结论做局部处理。空白结论不视为同意，人工确认也不替代数据库执行验证。

| 编号 | 需要确认的内容 | 当前状态 |
|---|---|---|
| HR-001 | 行车作业率查询的两个输入时间采用什么文本格式 | 日历日差已改写，输入解析约定待确认 |
| HR-002 | 行车作业率查询的小时、分钟采用哪种时长口径 | 两参数 TIMESTAMPDIFF 尚未转换 |
| HR-003 | 删除无计划号记录时，空串和纯空格是否一起删除 | 原删除条件保留，未扩大删除范围 |
| HR-004 | tmsme96、f_tmsm01_60106 的小时/分钟口径是否沿用 HR-002 的选择 | 11 处两参数 TIMESTAMPDIFF 整条挂起 |
| HR-005 | PSSM 大型报表查询(约 79 处天/分/秒 TIMESTAMPDIFF)采用哪种时长口径 | 4 个语句块挂起,块内其他方言已转换 |
| HR-006 | MMSM(6)、WM00(5)及 QMTS 等其余模块的两参数 TIMESTAMPDIFF 口径 | 语句整条或部分挂起,其余方言已转换 |

## HR-001　输入时间文本格式

**位置与锚点：** [tmsme59_inq.cpp](<D:/work/company/太钢二炼钢/Server/TMSM/p_tmsm_7160/tmsme59_inq.cpp(CHANGE-110 附近,原 92 行区域)>)，函数 `f_tmsme59_inq`；锚点是 `DATEDIFF(DAY, CAST(`，输入来自 `REC_CREATE_TIME`、`CHANGE_TIME` 的 `ToString()`。这两个值由接收行合入模型，当前片段没有显式规定输出格式。

原关键 SQL 为 `DAYS(DATE(TIMESTAMP('<结束文本>'))) - DAYS(DATE(TIMESTAMP('<开始文本>')))`；目前已改为：

```sql
DATEDIFF(DAY, CAST('<开始文本>' AS TIMESTAMP), CAST('<结束文本>' AS TIMESTAMP))
```

日历日差的计算方向明确；尚需确认字符串能够按正确格式被解析。`20260904235959` 与 `2026-09-04 23:59:59` 可以表达同一时刻，但所需解析格式不同，不能仅凭二者含义相同就认定同一个隐式转换都能处理。若开始为 9 月 4 日 23:59:59、结束为 9 月 5 日 00:00:01，原日历日口径应为 **1 天**。

拟议处理：若已有固定且匹配目标解析规则的格式，可保留 CAST；若格式需要明确指定，局部采用匹配该格式的日期解析表达式。保持“按日期跨了几天”的含义，不改成实际秒数除以一天。

**只需回答：这两个字段实际传入的时间文本格式是什么？** 可填写格式，例如 `YYYY-MM-DD HH24:MI:SS` 或 `YYYYMMDDHH24MISS`；不需要提供真实业务数据。

人工结论：**`YYYYMMDDHH24MISS`(14 位紧凑格式)**　确认人/日期：用户 2026-09-06

确认后的处理：✅ 已完成。全库时间字段统一为此格式。涉及 CAST AS TIMESTAMP 的 2 处(tmsme59/tmsme96)已改为 `TO_TIMESTAMP(…,'YYYYMMDDHH24MISS')`。后续转换遇到时间字段一律按此格式处理。

## HR-002　小时、分钟的统计口径

**位置与锚点：** [tmsme59_inq.cpp](<D:/work/company/太钢二炼钢/Server/TMSM/p_tmsm_7160/tmsme59_inq.cpp(现 L125 附近)>)，函数 `f_tmsme59_inq`；锚点 `TIMESTAMPDIFF(8, CHAR(TIMESTAMP(` 对应 `hours_diffx`，第 147 行的 `TIMESTAMPDIFF(4, CHAR(TIMESTAMP(` 对应 `minutes_diffx`。同函数后续还累计 `prep_time`、`use_time`。

原关键 SQL（仍为活动代码）：

```sql
TIMESTAMPDIFF(8, CHAR(TIMESTAMP('<结束文本>') - TIMESTAMP('<开始文本>')))
TIMESTAMPDIFF(4, CHAR(TIMESTAMP('<结束文本>') - TIMESTAMP('<开始文本>')))
```

这是 DB2 风格的两参数表达式，8 表示小时、4 表示分钟。其月年部分可能采用估算；DM 原生函数采用三个参数。不能只改参数数量就默认结果一致。[IBM 源函数定义](https://www.ibm.com/docs/en/db2-for-zos/13.0.0?topic=functions-timestampdiff)、[DM 函数手册](https://eco.dameng.com/document/dm/zh-cn/pm/function.html)

| 示例 | 实际完整时长：不满单位舍去 | 跨过的单位边界数 | 沿用 DB2 月年估算 |
|---|---|---|---|
| 同日 08:59:59 → 09:00:01，共 2 秒 | 0 小时、0 分钟 | 1 个小时边界、1 个分钟边界 | 此例为 0 小时、0 分钟 |
| 2026-02-01 00:00 → 2026-03-01 00:00 | 28 天，即 672 小时、40320 分钟 | 此例同为 672 个小时边界、40320 个分钟边界 | 月按 30 天折算，即 720 小时、43200 分钟 |

拟议处理：实际完整时长采用相应 DM 间隔表达式；单位边界数采用对应边界计算；保留 DB2 估算则按该算法制定等价表达式。都先核对 HR-001 的解析约定，保留起终点顺序、原单位和正负方向。

**只需回答：这个服务的小时、分钟统计，应按“实际完整时长”“单位边界数”还是“沿用 DB2 月年估算”计算？**

人工结论：**①实际完整时长**　确认人/日期：用户 2026-09-06

确认后的处理：按选定口径修改本服务对应表达式，列出跨单位、跨月和负时差的预期结果。该结论只适用于此处时间统计，不自动用于其他服务的同名函数或改变其他时长阈值。

## HR-003　无计划号记录的删除范围

**位置与锚点：** [f_pssm27_upd_plno_n.cpp](<D:/work/company/太钢二炼钢/Server/PSSM/libPSSM/f_pssm27_upd_plno_n.cpp:111>)，函数 `f_pssm27_upd_plno_n`；锚点 `DELETE FROM TPSSM27` 与 `TRIM(SM_PLAN_NO)is NULL`。该删除位于 `sm_plan_no_used[0] == ' '` 分支，随后执行记录插入。

原关键 SQL（当前保留）：

```sql
DELETE FROM TPSSM27
WHERE FACTORY_DIV = @tpssm27.FACTORY_DIV
  AND TRIM(SM_PLAN_NO) IS NULL
```

空串、空值和 TRIM 后的结果受数据库规则影响，现有证据不足以认定目标库已经出错。[Oracle 移植说明](https://eco.dameng.com/document/dm/zh-cn/start/oracle_dm)、[DM TRIM 定义](https://eco.dameng.com/document/dm/zh-cn/pm/function.html)

下表只比较两种处理规则下的理论删除集合；所有示例都假定工厂条件相同，且进入上述分支。

| 计划号输入 | 若去空格后的空串按 NULL 处理 | 若去空格后的空串仍与 NULL 区分 |
|---|---|---|
| NULL | 删除 | 删除 |
| 空串 `''` | 删除 | 不由当前 `IS NULL` 条件命中 |
| 只有普通空格 `'   '` | 删除 | 若 TRIM 结果为空串，则不命中 |
| 正常计划号 `' P001 '` | 不删除 | 不删除 |

拟议处理：确认应包含所有空白计划号后，先核对目标规则；现有条件已经满足就保留，确需补充时仅调整这一段空白判断，并保留工厂过滤及原流程。如果只允许删除数据库 NULL，则单独评估 `SM_PLAN_NO IS NULL`；已被数据库存成 NULL 的原始空串不能仅凭当前值再区分出来。

**只需回答：这里的“无计划号记录”，是否包括 NULL、空串和只有普通空格这三类，都应一起删除？**

人工结论：**三种情况(NULL、空串、纯空格)一起删除**　确认人/日期：用户 2026-09-08

确认后的处理：**已落地(2026-09-08,CHANGE-388)**：`Server/PSSM/libPSSM/f_pssm27_upd_plno_n.cpp` L111-L121，WHERE 改为 `COALESCE(LENGTH(TRIM(SM_PLAN_NO)), 0) = 0`（不使用空串字面量，任何 DM8 兼容模式下三种情况都命中）；原 SQL 注释保留，原写法已无活动残留；尚未在 DM8 实测。，再按目标空串规则决定保留或最小修改；未确认前不扩大 DELETE 条件，也不修改其他 SQL。

## 使用与更新

- 后续发现同类问题，仍按具体业务登记，避免一次回答被错误套用到所有模块。
- 每条关闭时补充结论、实际修改位置和验证层级；不把“人工已确认”记录为“DM8 已执行通过”。
- 原始覆盖和官方依据分别见[迁移清单入口](<D:/work/company/太钢二炼钢/analysis/dameng-migration/README.md>)、[官方资料复核](<D:/work/company/太钢二炼钢/analysis/dameng-migration/review-20260906-official.md>)。

## HR-004　tmsme96、f_tmsm01_60106 的小时/分钟口径

**位置与锚点（2026-09-06 登记于 TMSM 模块）:**

- [tmsme96_inq.cpp](<D:/work/company/太钢二炼钢/Server/TMSM/p_tmsm_7160/tmsme96_inq.cpp(现 L165 附近)>) 第 110、138 行(`TIMESTAMPDIFF(8/4, …)` 作用于 TTMSM66 时间字段),第 247、286、326、366、406、446、523 行(作用于 END_TIME/START_TIME、E_DATETIME/S_DATETIME 等字段);
- [f_tmsm01_60106.cpp](<D:/work/company/太钢二炼钢/Server/TMSM/libTMSM/f_tmsm01_60106.cpp:162>) 第 162 行(`TIMESTAMPDIFF(4, …)`)。

合计 10+1 处两参数 DB2 `TIMESTAMPDIFF`,与 HR-002 是同一种表达式;涉及服务不同,按"一个服务的答案不自动套用其他服务"的约定单独登记。当前这些语句**整条保持原样**(未做任何改写),因为 DM8 无两参数形式,任何改写都必须先定口径。

**只需回答:这两个服务的小时/分钟统计,是否沿用你对 HR-002 的同一选择(实际完整时长/单位边界数/沿用 DB2 月年估算)?** 若不同,请分别说明。

人工结论:**①实际完整时长(同HR-002)**　确认人/日期:用户 2026-09-06

确认后的处理:按选定口径整条改写上述语句(写法与 HR-002 关闭后的 tmsme59 同型),保留完整原 SQL 注释;未执行验证继续标未执行。

## HR-005　PSSM 大型报表查询的天/分/秒口径

**位置与锚点(2026-09-06 登记于 PSSM 模块):** 4 个语句块(台账 HR-005 行)——

- [mmlgap07_inq.cpp](<D:/work/company/太钢二炼钢/Server/PSSM/p_pssm_13060/mmlgap07_inq.cpp>) `timestampdiff(16, …)`(天)×8;
- [mmsmap09_inq.cpp](<D:/work/company/太钢二炼钢/Server/PSSM/p_pssm_13060/mmsmap09_inq.cpp>) `timestampdiff(2, …)`(秒)×18;
- [mmlgap09_inq.cpp](<D:/work/company/太钢二炼钢/Server/PSSM/p_pssm_13060/mmlgap09_inq.cpp>)、[mmsmap07_inq.cpp](<D:/work/company/太钢二炼钢/Server/PSSM/p_pssm_13060/mmsmap07_inq.cpp>) `timestampdiff(4, …)`(分)×53。

合计约 79 处两参数 DB2 `TIMESTAMPDIFF`,均嵌在大型 UNION 报表查询中;块内其他方言(SYSIBM、`+ 3 HOUR` 等)已按 CHANGE-115—150 转换,仅 TIMESTAMPDIFF 表达式保持原样——DM8 无两参数形式,须先定口径。天(16)同样存在"日历日边界 vs 实际经过 24 小时"的差异,与分/秒的"边界数 vs 完整时长"一致。

**只需回答:PSSM 这些报表的天、分、秒统计,是否沿用你对 HR-002 的同一选择?** 若不同,请分别说明。

人工结论:**①实际完整时长(同HR-002)**　确认人/日期:用户 2026-09-06

确认后的处理:按选定口径制定天/分/秒的等价表达式(同 HR-002 关闭后的写法),整块改写并保留完整原 SQL 注释;**同块内 DB2 DIGITS() 函数(DM 无此函数,零填充语义)需一并改写为等价表达式**;未执行验证继续标未执行。


---

## 落地记录(2026-09-08)

HR-002 / HR-004 / HR-006 的答复(口径① 实际完整时长)已全部落地为代码转换,共 14 个文件、108 处两参数 TIMESTAMPDIFF 调用,涉及台账 31 行(HR-002:tmsme59 CHANGE-341~345 即 CHANGE-EXEC-097~101;HR-004:f_tmsm01_60106 CHANGE-340 与 tmsme96 CHANGE-346~355;HR-006:其余全部)。统一公式:

- `TIMESTAMPDIFF(2, X - Y)` → `DATEDIFF(SECOND, Y, X)`(秒,不除);
- `TIMESTAMPDIFF(4, X - Y)` → `DATEDIFF(SECOND, Y, X) / 60`(分钟);
- `TIMESTAMPDIFF(8, X - Y)` → `DATEDIFF(SECOND, Y, X) / 3600`(小时);
- `TIMESTAMPDIFF(16, X - Y)` → `DATEDIFF(SECOND, Y, X) / 86400`(天);

整数除法截断与 DB2 TIMESTAMPDIFF 行为一致;起点=被减数时间,终点=减数时间。14 位时间串按 HR-001 用 TO_TIMESTAMP(x,'YYYYMMDDHH24MISS') 显式指定。全部语句未在 DM8 执行。明细见 [2026-09-08-TIMESTAMPDIFF批次记录](<D:/work/company/太钢二炼钢/analysis/dameng-migration/batches/2026-09-08-TIMESTAMPDIFF批次记录.md>)。
