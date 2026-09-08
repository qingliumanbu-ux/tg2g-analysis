# 2026-09-08 批次记录:HR-003 落地 + 全量两参数 TIMESTAMPDIFF 转换

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


## 2026-09-08 Git 提交记录

以上全部改动已提交并推送到各模块独立仓库的 `dev` 分支(origin/dev),工作区全部干净、本地与远程一致:

| 仓库 | 提交 | 推送 |
|---|---|---|
| Server/WMSM | 90f14b0 | e8992ce..90f14b0 |
| Server/TMSM | ab1f08f | 74919c4..ab1f08f |
| Server/PSSM | 31fddba | 98147ea..31fddba |
| Server/MMSM | 75b246b | ee32201..75b246b |
| Server/QMTS | ac90497 | c3d781d..ac90497 |
| Server/WM00 | 0a75dca | 已推送 |
| Server/CAAI | 9fae811 | 3ef266e..9fae811 |
| Server/FOSMT | 1bd585c | 90414b7..1bd585c |
| Server/SM00 | 1d08f64 | 4258261..1d08f64 |
| Server/TK00 | 1a5d7c8 | 71d918c..1a5d7c8 |
| Server/MMTP | 0bb1da2 | 1faf333..0bb1da2 |
| Server/GCTP | 7387589 | b201a52..7387589 |
| Server/MM00 | ddf833f | 6c9fc67..ddf833f |
| Server/WM10 | 54caf93 | 958b820..54caf93 |

提交信息统一为"DM8适配:后台SQL达梦基础转换(本模块N个文件)",正文说明:原 SQL 注释完整保留、HR 答复口径落地、明细见台账与批次记录、未在 DM8 执行。analysis/ 分析目录不在任何 Git 仓库内,不入库(按交接文档口径维护)。
