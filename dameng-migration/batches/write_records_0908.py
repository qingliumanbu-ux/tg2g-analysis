# -*- coding: utf-8 -*-
# HR 清单落地说明 + 2026-09-08 批次记录
import io

# ---------- 1) 待人工复核清单:HR-002/004/006 落地说明 ----------
CP = 'analysis/dameng-migration/待人工复核SQL清单.md'
t = open(CP, encoding='utf-8').read()
note = '''

---

## 落地记录(2026-09-08)

HR-002 / HR-004 / HR-006 的答复(口径① 实际完整时长)已全部落地为代码转换,共 14 个文件、108 处两参数 TIMESTAMPDIFF 调用,涉及台账 31 行(HR-002:tmsme59 CHANGE-341~345 即 CHANGE-EXEC-097~101;HR-004:f_tmsm01_60106 CHANGE-340 与 tmsme96 CHANGE-346~355;HR-006:其余全部)。统一公式:

- `TIMESTAMPDIFF(2, X - Y)` → `DATEDIFF(SECOND, Y, X)`(秒,不除);
- `TIMESTAMPDIFF(4, X - Y)` → `DATEDIFF(SECOND, Y, X) / 60`(分钟);
- `TIMESTAMPDIFF(8, X - Y)` → `DATEDIFF(SECOND, Y, X) / 3600`(小时);
- `TIMESTAMPDIFF(16, X - Y)` → `DATEDIFF(SECOND, Y, X) / 86400`(天);

整数除法截断与 DB2 TIMESTAMPDIFF 行为一致;起点=被减数时间,终点=减数时间。14 位时间串按 HR-001 用 TO_TIMESTAMP(x,'YYYYMMDDHH24MISS') 显式指定。全部语句未在 DM8 执行。明细见 [2026-09-08-TIMESTAMPDIFF批次记录](<D:/work/company/太钢二炼钢/analysis/dameng-migration/batches/2026-09-08-TIMESTAMPDIFF批次记录.md>)。
'''
if '落地记录(2026-09-08)' not in t:
    t = t.rstrip() + '\n' + note
open(CP, 'w', encoding='utf-8', newline='').write(t)
print('checklist updated')

# ---------- 2) 批次记录 ----------
BP = 'analysis/dameng-migration/batches/2026-09-08-TIMESTAMPDIFF批次记录.md'
rec = '''# 2026-09-08 批次记录:HR-003 落地 + 全量两参数 TIMESTAMPDIFF 转换

## 范围与结论

- HR-003(空串/NULL/纯空格一起删除)落地为 CHANGE-388:`Server/PSSM/libPSSM/f_pssm27_upd_plno_n.cpp` L111-L121,WHERE 改为 `COALESCE(LENGTH(TRIM(SM_PLAN_NO)), 0) = 0`。
- HR-002/004/006 口径①(实际完整时长)落地:14 个文件、108 处两参数 TIMESTAMPDIFF 调用全部转换,台账 36 行由"待人工复核"改为"已转换"。
- 台账现状:可保留 17,426 / 已转换 384 / 待局部信息 15 / 待人工 0。
- 全部语句未在 DM8 执行(runtime_status=未执行);E2 语法验证脚本已追加对应语句。

## 统一转换公式(HR-002 口径①)

| DB2 | DM8 | 说明 |
|---|---|---|
| TIMESTAMPDIFF(2, X - Y) | DATEDIFF(SECOND, Y, X) | 秒 |
| TIMESTAMPDIFF(4, X - Y) | DATEDIFF(SECOND, Y, X) / 60 | 分钟 |
| TIMESTAMPDIFF(8, X - Y) | DATEDIFF(SECOND, Y, X) / 3600 | 小时 |
| TIMESTAMPDIFF(16, X - Y) | DATEDIFF(SECOND, Y, X) / 86400 | 天 |

DB2 的 TIMESTAMPDIFF(N,·) 按"总秒数÷因子截断取整"计算,DM8 整数除法结果一致。起点=减数(较早),终点=被减数(较晚)。14 位时间串用 TO_TIMESTAMP(x,'YYYYMMDDHH24MISS')(HR-001)。

## 逐文件明细

| 文件 | 台账行 | 调用数 | 说明 |
|---|---|---|---|
| TMSM/libTMSM/f_tmsm01_60106.cpp | CHANGE-340 | 1 | 钢包盛钢时长(分钟);usage_st/datetime 为 14 位 |
| TMSM/p_tmsm_7160/tmsme96_inq.cpp | CHANGE-108/109/346~355 | 10+1天+1汇总 | 设备使用率:各工位作业分钟数、日历天差、汇总 ROUND;**此前转换曾丢失(文件被回退),本次按台账编号重做** |
| MMSM/p_mmsm_17520/mmsmis02_inq.cpp | CHANGE-163 | 1 | 切断→热装小时差(OUT_HOT_TIME);timestamp(x,格式串) 改 TO_TIMESTAMP(格式串与 14 位值不匹配,一并修正) |
| MMSM/p_mmsm_17520/mmsmis02_inqa.cpp | CHANGE-164 | 1 | 同上 |
| MMSM/p_mmsm_17520/mmsmis02a1_inq.cpp | CHANGE-165/166 | 2 | 在库时长/热装小时差 |
| MMSM/p_mmsm_17520/mmsmis02a1_inqa.cpp | CHANGE-167/168 | 2 | 同上 |
| WM00/libWM00/f_create_crane_no.cpp | CHANGE-234 | 1 | 板坯冷却小时数(diffTimes16);原 to_date 格式串与 14 位值不匹配,改 TO_TIMESTAMP |
| WM00/libWM00/f_wm00_pile_comf.cpp | CHANGE-235/236 | 2 | 垛位 24 小时内使用;FIELDNO_UPTIME 按程序内注释为字符型时间,用 TO_DATE(x,'YYYY-MM-DD HH24:MI:SS') |
| WM00/libWM00/f_wm00_pile_jud.cpp | CHANGE-237/238 | 2 | 冷却时间/最大冷却时间 |
| MM00/p_mm00_18010/mm00su47a1_m.cpp | CHANGE-356/357 | 6 | 在库/产出/轧制时间的天数与小时数表达式(语句内原地替换,注释块原位更新) |
| PSSM/p_pssm_13060/mmlgap07_inq.cpp | CHANGE-138 | 2 | 累计作业率 ljzyl 的天数分母(16=天) |
| PSSM/p_pssm_13060/mmsmap07_inq.cpp | CHANGE-148 | 2 | 同上 |
| PSSM/p_pssm_13060/mmlgap09_inq.cpp | CHANGE-141(+381 并入) | 38 | 连铸日报:秒/分钟/天三类;**叠加的 CHANGE-381 注释块已并入 CHANGE-141 一块,含 SYSIBM 的真原始 SQL 以保留块为准** |
| PSSM/p_pssm_13060/mmsmap09_inq.cpp | CHANGE-150 | 38 | 同类大型语句,整体重排(原 SQL 注释保留) |

## 方法与验证

- 小语句:精确内容匹配替换活动行,注释块原位更新(保留最初原 SQL 一份,不叠加)。
- 大语句(mmsmap09 约 500 行):拼接 C++ 字符串片段→平衡括号解析每个 timestampdiff 调用→原地替换→重新按 120 字符折行输出。
- 每文件断言:①注释还原(原 SQL 逐字节保留);②活动残留 timestampdiff = 0;③等价性(把调用替换为占位符后,新旧剩余文本逐字节一致);④括号平衡;⑤原始注释段调用数=活动语句调用数。
- 改前备份:批次目录下 `tsdiff-*.cpp.bak` 与 `f_pssm27_upd_plno_n.pre-change388.bak`。

## 其他同步

- 待人工复核SQL清单.md:HR-002/004/006 增加落地记录;HR-003 标记已落地(CHANGE-388)。
- E2 脚本:各模块追加本次转换语句(变量以 14 位测试值代入)。
- 本批次未执行任何数据库、构建或部署。
'''
open(BP, 'w', encoding='utf-8', newline='').write(rec)
print('batch record written')
