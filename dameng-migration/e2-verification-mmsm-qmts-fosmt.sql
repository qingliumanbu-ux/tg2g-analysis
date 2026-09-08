-- =====================================================================
-- E2 验证脚本: MMSM / QMTS / FOSMT 已转换 DM8 SQL 汇总
-- 生成来源: analysis/dameng-migration/sql-ledger.csv 中 module 属于
--           MMSM/QMTS/FOSMT 且 decision=已转换 的 143 条记录(2026-09-07 生成)
-- 语句来源: 各行 active_sql_anchor 指向源码位置的活动 DM8 SQL 原文(逐字还原,
--           含 C++ 字符串拼接;拼接变量已按 GAP_FILL 注入测试常量)。
-- 参数替换: @字符串参数 -> '测试值';@数字参数 -> 1。表名/列名保持源码原样。
-- 说明:
--   1. 本脚本用于 E2(DM8 可执行)验证的准备材料,生成时未连接数据库执行(runtime_status=未执行)。
--   2. 标注「片段」的条目为 WHERE 拼接片段,不能单独执行,已注释保留,需拼入宿主语句验证。
--   3. 动态表名/动态条件处已填入代表性常量(见各条目「参数/填充」注释),执行结果不代表全部取值路径。
--   4. 源码为 GB18030 编码,本脚本为 UTF-8(BOM)/CRLF;disql 执行前请确认会话编码一致。
--   5. 各语句前注释含 sql_id 与模块,便于与 sql-ledger.csv、源码 CHANGE 注释对照。
-- =====================================================================

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-188 | module: QMTS
-- 来源: Server/QMTS/libQMTS/f_qmts_spe_single.cpp | 函数: f_qmts_spe_single | 锚点: L179-L179
-- 参数: @formula_value='测试值', @i=1
SELECT substr('测试值',1,1-1) || ')' || substr('测试值',1+1) FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-189 | module: QMTS
-- 来源: Server/QMTS/libQMTS/f_qmts_spe_single.cpp | 函数: f_qmts_spe_single | 锚点: L193-L193
-- 参数: @formula_value='测试值', @i=1
SELECT substr('测试值',1,1-1) || ')' || substr('测试值',1+1) FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-190 | module: QMTS
-- 来源: Server/QMTS/libQMTS/f_qmts_spe_single.cpp | 函数: f_qmts_spe_single | 锚点: L221-L221
-- 参数: @formula_value='测试值', @i=1
SELECT substr('测试值',1,1-1) || 'abs(' || substr('测试值',1+1) FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-191 | module: QMTS
-- 来源: Server/QMTS/libQMTS/f_qmts_spe_single.cpp | 函数: f_qmts_spe_single | 锚点: L235-L235
-- 参数: @formula_value='测试值', @i=1
SELECT substr('测试值',1,1-1) || 'abs(' || substr('测试值',1+1) FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-192 | module: QMTS
-- 来源: Server/QMTS/libQMTS/f_qmts_spe_single.cpp | 函数: f_qmts_spe_single | 锚点: L288-L288
-- 参数: @formula_value='测试值', @elm_name='测试值'
SELECT replace('测试值','测试值','') FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-193 | module: QMTS
-- 来源: Server/QMTS/libQMTS/f_qmts_spe_single.cpp | 函数: f_qmts_spe_single | 锚点: L302-L302
-- 参数: @formula_value='测试值', @elm_name='测试值'
SELECT replace('测试值','测试值','') FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-194 | module: QMTS
-- 来源: Server/QMTS/libQMTS/f_qmts_spe_single.cpp | 函数: f_qmts_spe_single | 锚点: L402-L402
-- 拼接填充: formula_value=1
SELECT ROUND(1,4) FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-195 | module: QMTS
-- 来源: Server/QMTS/libQMTS/f_qmts_spe_single.cpp | 函数: f_qmts_spe_single | 锚点: L416-L416
-- 拼接填充: formula_value=1
SELECT ROUND(1,4) FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-196 | module: QMTS
-- 来源: Server/QMTS/libQMTS/f_qmts_spe_sm.cpp | 函数: f_qmts_spe_sm | 锚点: L357-L357
-- 参数: @formula_value='测试值', @i=1
SELECT substr('测试值',1,1-1) || ')' || substr('测试值',1+1) FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-197 | module: QMTS
-- 来源: Server/QMTS/libQMTS/f_qmts_spe_sm.cpp | 函数: f_qmts_spe_sm | 锚点: L371-L371
-- 参数: @formula_value='测试值', @i=1
SELECT substr('测试值',1,1-1) || ')' || substr('测试值',1+1) FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-198 | module: QMTS
-- 来源: Server/QMTS/libQMTS/f_qmts_spe_sm.cpp | 函数: f_qmts_spe_sm | 锚点: L399-L399
-- 参数: @formula_value='测试值', @i=1
SELECT substr('测试值',1,1-1) || 'abs(' || substr('测试值',1+1) FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-199 | module: QMTS
-- 来源: Server/QMTS/libQMTS/f_qmts_spe_sm.cpp | 函数: f_qmts_spe_sm | 锚点: L413-L413
-- 参数: @formula_value='测试值', @i=1
SELECT substr('测试值',1,1-1) || 'abs(' || substr('测试值',1+1) FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-200 | module: QMTS
-- 来源: Server/QMTS/libQMTS/f_qmts_spe_sm.cpp | 函数: f_qmts_spe_sm | 锚点: L466-L466
-- 参数: @formula_value='测试值', @elm_name='测试值'
SELECT replace('测试值','测试值','') FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-201 | module: QMTS
-- 来源: Server/QMTS/libQMTS/f_qmts_spe_sm.cpp | 函数: f_qmts_spe_sm | 锚点: L480-L480
-- 参数: @formula_value='测试值', @elm_name='测试值'
SELECT replace('测试值','测试值','') FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-202 | module: QMTS
-- 来源: Server/QMTS/libQMTS/f_qmts_spe_sm.cpp | 函数: f_qmts_spe_sm | 锚点: L540-L540
-- 参数: @formula_value='测试值', @elm_name='测试值', @elm_value='测试值'
SELECT replace('测试值','测试值','测试值') FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-203 | module: QMTS
-- 来源: Server/QMTS/libQMTS/f_qmts_spe_sm.cpp | 函数: f_qmts_spe_sm | 锚点: L554-L554
-- 参数: @formula_value='测试值', @elm_name='测试值', @elm_value='测试值'
SELECT replace('测试值','测试值','测试值') FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-204 | module: QMTS
-- 来源: Server/QMTS/libQMTS/f_qmts_spe_sm.cpp | 函数: f_qmts_spe_sm | 锚点: L586-L586
-- 参数: @formula_value='测试值', @elm_name='测试值', @elm_value='测试值'
SELECT replace('测试值','测试值','测试值') FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-205 | module: QMTS
-- 来源: Server/QMTS/libQMTS/f_qmts_spe_sm.cpp | 函数: f_qmts_spe_sm | 锚点: L600-L600
-- 参数: @formula_value='测试值', @elm_name='测试值', @elm_value='测试值'
SELECT replace('测试值','测试值','测试值') FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-206 | module: QMTS
-- 来源: Server/QMTS/libQMTS/f_qmts_spe_sm.cpp | 函数: f_qmts_spe_sm | 锚点: L642-L642
-- 拼接填充: formula_value=1
SELECT ROUND(1,5) FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-207 | module: QMTS
-- 来源: Server/QMTS/libQMTS/f_qmts_spe_sm.cpp | 函数: f_qmts_spe_sm | 锚点: L656-L656
-- 拼接填充: formula_value=1
SELECT ROUND(1,5) FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-208 | module: QMTS
-- 来源: Server/QMTS/libQMTS/f_qmts_spe_sm.cpp | 函数: f_qmts_spe_sm | 锚点: L687-L687
-- 参数: @symbol='测试值'
SELECT replace('测试值','>','-') FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-209 | module: QMTS
-- 来源: Server/QMTS/libQMTS/f_qmts_spe_sm.cpp | 函数: f_qmts_spe_sm | 锚点: L701-L701
-- 参数: @symbol='测试值'
SELECT replace('测试值','>','-') FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-210 | module: QMTS
-- 来源: Server/QMTS/libQMTS/f_qmts_spe_sm.cpp | 函数: f_qmts_spe_sm | 锚点: L724-L724
-- 参数: @symbol='测试值'
SELECT replace('测试值','<','+') FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-211 | module: QMTS
-- 来源: Server/QMTS/libQMTS/f_qmts_spe_sm.cpp | 函数: f_qmts_spe_sm | 锚点: L738-L738
-- 参数: @symbol='测试值'
SELECT replace('测试值','<','+') FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-212 | module: QMTS
-- 来源: Server/QMTS/libQMTS/f_qmts_spe_sm.cpp | 函数: f_qmts_spe_sm | 锚点: L790-L790
-- 参数: @symbol='测试值', @elm_name='测试值'
SELECT replace('测试值','测试值','') FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-213 | module: QMTS
-- 来源: Server/QMTS/libQMTS/f_qmts_spe_sm.cpp | 函数: f_qmts_spe_sm | 锚点: L804-L804
-- 参数: @symbol='测试值', @elm_name='测试值'
SELECT replace('测试值','测试值','') FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-214 | module: QMTS
-- 来源: Server/QMTS/libQMTS/f_qmts_spe_sm.cpp | 函数: f_qmts_spe_sm | 锚点: L863-L863
-- 参数: @symbol='测试值', @elm_name='测试值', @elm_value='测试值'
SELECT replace('测试值','测试值','测试值') FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-215 | module: QMTS
-- 来源: Server/QMTS/libQMTS/f_qmts_spe_sm.cpp | 函数: f_qmts_spe_sm | 锚点: L877-L877
-- 参数: @symbol='测试值', @elm_name='测试值', @elm_value='测试值'
SELECT replace('测试值','测试值','测试值') FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-216 | module: QMTS
-- 来源: Server/QMTS/libQMTS/f_qmts_spe_sm.cpp | 函数: f_qmts_spe_sm | 锚点: L908-L908
-- 参数: @symbol='测试值', @elm_name='测试值', @elm_value='测试值'
SELECT replace('测试值','测试值','测试值') FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-217 | module: QMTS
-- 来源: Server/QMTS/libQMTS/f_qmts_spe_sm.cpp | 函数: f_qmts_spe_sm | 锚点: L922-L922
-- 参数: @symbol='测试值', @elm_name='测试值', @elm_value='测试值'
SELECT replace('测试值','测试值','测试值') FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-218 | module: QMTS
-- 来源: Server/QMTS/libQMTS/f_qmts_spe_sm.cpp | 函数: f_qmts_spe_sm | 锚点: L961-L961
-- 拼接填充: symbol=1
SELECT 1 FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-219 | module: QMTS
-- 来源: Server/QMTS/libQMTS/f_qmts_spe_sm.cpp | 函数: f_qmts_spe_sm | 锚点: L975-L975
-- 拼接填充: symbol=1
SELECT 1 FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-220 | module: QMTS
-- 来源: Server/QMTS/libQMTS/f_qmts_spe_sm.cpp | 函数: f_qmts_spe_sm | 锚点: L1095-L1095
-- 参数: @formula_std='测试值', @i=1
SELECT substr('测试值',1,1-1) || ')' || substr('测试值',1+1) FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-221 | module: QMTS
-- 来源: Server/QMTS/libQMTS/f_qmts_spe_sm.cpp | 函数: f_qmts_spe_sm | 锚点: L1109-L1109
-- 参数: @formula_std='测试值', @i=1
SELECT substr('测试值',1,1-1) || ')' || substr('测试值',1+1) FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-222 | module: QMTS
-- 来源: Server/QMTS/libQMTS/f_qmts_spe_sm.cpp | 函数: f_qmts_spe_sm | 锚点: L1137-L1137
-- 参数: @formula_std='测试值', @i=1
SELECT substr('测试值',1,1-1) || 'abs(' || substr('测试值',1+1) FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-223 | module: QMTS
-- 来源: Server/QMTS/libQMTS/f_qmts_spe_sm.cpp | 函数: f_qmts_spe_sm | 锚点: L1151-L1151
-- 参数: @formula_std='测试值', @i=1
SELECT substr('测试值',1,1-1) || 'abs(' || substr('测试值',1+1) FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-224 | module: QMTS
-- 来源: Server/QMTS/libQMTS/f_qmts_spe_sm.cpp | 函数: f_qmts_spe_sm | 锚点: L1203-L1203
-- 参数: @formula_std='测试值', @elm_name='测试值'
SELECT replace('测试值','测试值','') FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-225 | module: QMTS
-- 来源: Server/QMTS/libQMTS/f_qmts_spe_sm.cpp | 函数: f_qmts_spe_sm | 锚点: L1217-L1217
-- 参数: @formula_std='测试值', @elm_name='测试值'
SELECT replace('测试值','测试值','') FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-226 | module: QMTS
-- 来源: Server/QMTS/libQMTS/f_qmts_spe_sm.cpp | 函数: f_qmts_spe_sm | 锚点: L1276-L1276
-- 参数: @formula_std='测试值', @elm_name='测试值', @elm_value='测试值'
SELECT replace('测试值','测试值','测试值') FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-227 | module: QMTS
-- 来源: Server/QMTS/libQMTS/f_qmts_spe_sm.cpp | 函数: f_qmts_spe_sm | 锚点: L1290-L1290
-- 参数: @formula_std='测试值', @elm_name='测试值', @elm_value='测试值'
SELECT replace('测试值','测试值','测试值') FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-228 | module: QMTS
-- 来源: Server/QMTS/libQMTS/f_qmts_spe_sm.cpp | 函数: f_qmts_spe_sm | 锚点: L1322-L1322
-- 参数: @formula_std='测试值', @elm_name='测试值', @elm_value='测试值'
SELECT replace('测试值','测试值','测试值') FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-229 | module: QMTS
-- 来源: Server/QMTS/libQMTS/f_qmts_spe_sm.cpp | 函数: f_qmts_spe_sm | 锚点: L1336-L1336
-- 参数: @formula_std='测试值', @elm_name='测试值', @elm_value='测试值'
SELECT replace('测试值','测试值','测试值') FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-230 | module: QMTS
-- 来源: Server/QMTS/libQMTS/f_qmts_spe_sm.cpp | 函数: f_qmts_spe_sm | 锚点: L1377-L1377
-- 拼接填充: formula_std=1
SELECT ROUND(1,5) FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-231 | module: QMTS
-- 来源: Server/QMTS/libQMTS/f_qmts_spe_sm.cpp | 函数: f_qmts_spe_sm | 锚点: L1391-L1391
-- 拼接填充: formula_std=1
SELECT ROUND(1,5) FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-232 | module: QMTS
-- 来源: Server/QMTS/p_qmts_4800/qmts0rdr_inq.cpp | 函数: f_qmts0rdr_inq | 锚点: L133-L171
SELECT * FROM ( SELECT T.*, CASE WHEN T.ELM_01_TC IS NULL OR T.ELM_01_TC = '' THEN '0' ELSE '1' END AS XY_FLAG, CASE WHEN T.ELM_16_TC != ' ' OR T.ELM_VALUE_16 != ' ' THEN '2' ELSE '1' END AS HS FROM( SELECT T1.*, T2.AYL_FLAG, T2.CHECK_FLAG, T2.DECIDE_CODE, T2.ELM_VALUE_16, T2.ELM_01_TC, T2.ELM_01_MIN_TC, T2.ELM_01_MAX_TC, T2.ELM_02_TC, T2.ELM_02_MIN_TC, T2.ELM_02_MAX_TC, T2.ELM_03_TC, T2.ELM_03_MIN_TC, T2.ELM_03_MAX_TC, T2.ELM_04_TC, T2.ELM_04_MIN_TC, T2.ELM_04_MAX_TC, T2.ELM_05_TC, T2.ELM_05_MIN_TC, T2.ELM_05_MAX_TC, T2.ELM_06_TC, T2.ELM_06_MIN_TC, T2.ELM_06_MAX_TC, T2.ELM_07_TC, T2.ELM_07_MIN_TC, T2.ELM_07_MAX_TC, T2.ELM_08_TC, T2.ELM_08_MIN_TC, T2.ELM_08_MAX_TC, T2.ELM_09_TC, T2.ELM_09_MIN_TC, T2.ELM_09_MAX_TC, T2.ELM_10_TC, T2.ELM_10_MIN_TC, T2.ELM_10_MAX_TC, T2.ELM_11_TC, T2.ELM_11_MIN_TC, T2.ELM_11_MAX_TC, T2.ELM_12_TC, T2.ELM_12_MIN_TC, T2.ELM_12_MAX_TC, T2.ELM_13_TC, T2.ELM_13_MIN_TC, T2.ELM_13_MAX_TC, T2.ELM_14_TC, T2.ELM_14_MIN_TC, T2.ELM_14_MAX_TC, T2.ELM_15_TC, T2.ELM_15_MIN_TC, T2.ELM_15_MAX_TC, T2.ELM_16_TC, T2.ELM_16_MIN_TC, T2.ELM_16_MAX_TC, T2.ELM_17_TC, T2.ELM_17_MIN_TC, T2.ELM_17_MAX_TC, T2.ELM_18_TC, T2.ELM_18_MIN_TC, T2.ELM_18_MAX_TC, T2.ELM_19_TC, T2.ELM_19_MIN_TC, T2.ELM_19_MAX_TC, T2.ELM_20_TC, T2.ELM_20_MIN_TC, T2.ELM_20_MAX_TC, T2.ELM_21_TC, T2.ELM_21_MIN_TC, T2.ELM_21_MAX_TC, T2.ELM_22_TC, T2.ELM_22_MIN_TC, T2.ELM_22_MAX_TC, T2.ELM_23_TC, T2.ELM_23_MIN_TC, T2.ELM_23_MAX_TC, T2.ELM_24_TC, T2.ELM_24_MIN_TC, T2.ELM_24_MAX_TC, T2.ELM_25_TC, T2.ELM_25_MIN_TC, T2.ELM_25_MAX_TC, T2.ELM_26_TC, T2.ELM_26_MIN_TC, T2.ELM_26_MAX_TC, T2.ELM_27_TC, T2.ELM_27_MIN_TC, T2.ELM_27_MAX_TC, T2.ELM_28_TC, T2.ELM_28_MIN_TC, T2.ELM_28_MAX_TC, T2.ELM_29_TC, T2.ELM_29_MIN_TC, T2.ELM_29_MAX_TC, T2.ELM_30_TC, T2.ELM_30_MIN_TC, T2.ELM_30_MAX_TC FROM TQMTS0RDR T1 LEFT JOIN TQMTS0R05 T2 ON T1.HEAT_NO = T2.HEAT_NO AND T1.ORDER_NO = T2.ORDER_NO AND T1.NOW_ROW = T2.NOW_ROW)T ) WHERE 1 = 1;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-233 | module: QMTS
-- 来源: Server/QMTS/p_qmts_4850/cm_0rt805_rcv.cpp | 函数: f_cm_0rt805_rcv | 锚点: L103-L103
-- 拼接填充: v_heat_no=测试值, v_order_no=测试值
SELECT CASE WHEN max(now_row) IS NULL THEN 0 ELSE max(now_row) END FROM TQMTS0R05 where heat_no='测试值'and order_no='测试值';

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-334 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28190/fosmt90_pro.cpp | 函数: f_fosmt90_pro | 锚点: L256-L259
-- 参数: @BREAKDN_DATE='测试值', @DEP_NAME='测试值'
SELECT DATEDIFF(DAY, TO_DATE(MAX(BREAKDN_DATE),'YYYYMMDD'), TO_DATE('测试值','YYYYMMDD')) FROM TFOSMT02A WHERE DEP_NAME = '测试值';

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-187 | module: QMTS
-- 来源: Server/QMTS/libQMTS/f_qmts_30_ins.cpp | 函数: f_qmts_30_ins | 锚点: L116-L118
-- 参数: @st_sample_no='测试值', @st_no='测试值'
SELECT T2.ELM_NAME, CASE WHEN (decode(SUBSTR(ELM_ACT,1,1),'.','0'||ELM_ACT,ELM_ACT)) IS NULL THEN '无检验或缺失' ELSE (decode(SUBSTR(ELM_ACT,1,1),'.','0'||ELM_ACT,ELM_ACT)) END, SPE_MIN, SPE_MAX, T1.ELM_OK FROM(SELECT * FROM tqmts25 WHERE ST_SAMPLE_NO = '测试值') T1 RIGHT JOIN(SELECT * FROM TQMTS02 WHERE IDX_NO IN(SELECT ELM_STD_IDX_A FROM TQMTS0X WHERE ST_NO = '测试值')) T2 ON T1.ELM_CODE = T2.ELM_CODE WHERE (ELM_OK = '1' OR ELM_OK IS NULL);

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-276 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosm02_inq.cpp | 函数: f_fosm02_inq | 锚点: L213-L228
-- 参数: @DATE_TIME='测试值'
SELECT A.CODE, A.CODE_DESC_1_CONTENT DEP_NAME, C.BREAKDN_DATE, C.REMARK REMARK_BFR, B.REMARK, CASE WHEN B.BREAKDN_DATE IS NULL THEN DATEDIFF(DAY, TO_DATE(C.BREAKDN_DATE,'YYYYMMDD'), TO_DATE('测试值','YYYYMMDD')) ELSE 0 END OPERATE_CYCLE, CASE WHEN C.TOTAL_OPERATE_CYCLE IS NULL OR CASE WHEN B.REMARK IS NULL THEN DATEDIFF(DAY, TO_DATE(C.BREAKDN_DATE,'YYYYMMDD'), TO_DATE('测试值','YYYYMMDD')) ELSE B.TOTAL_OPERATE_CYCLE END IS NULL THEN NULL ELSE GREATEST(C.TOTAL_OPERATE_CYCLE, CASE WHEN B.REMARK IS NULL THEN DATEDIFF(DAY, TO_DATE(C.BREAKDN_DATE,'YYYYMMDD'), TO_DATE('测试值','YYYYMMDD')) ELSE B.TOTAL_OPERATE_CYCLE END) END TOTAL_OPERATE_CYCLE FROM TEP0002 A LEFT JOIN TFOSMT02A B ON A.CODE = B.DEP_NAME AND B.BREAKDN_DATE = '测试值' LEFT JOIN (SELECT DEP_NAME, REMARK, BREAKDN_DATE, TOTAL_OPERATE_CYCLE FROM TFOSMT02A WHERE (DEP_NAME, BREAKDN_DATE) IN (SELECT DEP_NAME, MAX(BREAKDN_DATE) FROM TFOSMT02A WHERE BREAKDN_DATE < '测试值' GROUP BY DEP_NAME) ) C ON A.CODE = C.DEP_NAME LEFT JOIN TFOSMT02B D ON A.CODE = D.DEP_NAME WHERE A.CODE_CLASS = 'FOSMT1' AND A.CODE_DESC_2_CONTENT != ' ' ORDER BY A.CODE_DESC_2_CONTENT;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-277 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosm02_inq.cpp | 函数: f_fosm02_inq | 锚点: L350-L356
-- 参数: @DATE_TIME='测试值'
SELECT DATE_TIME, PLAN_CHARGE, PRODUCT_CHARGE FROM TFOSMT03A WHERE FACTORY_DIV = 'A20' AND DATE_TIME > TO_CHAR((TO_DATE('测试值','YYYYMMDD') - 7),'YYYYMMDD') AND DATE_TIME <= '测试值' ORDER BY DATE_TIME;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-278 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosm02_inq.cpp | 函数: f_fosm02_inq | 锚点: L396-L410
-- 参数: @DATE_TIME='测试值'
WITH A(LEVEL, TIME) AS (SELECT 1, TO_DATE('测试值','YYYYMMDD') - 6 FROM DUAL WHERE 1 = 1 UNION ALL SELECT LEVEL + 1,TIME + 1 FROM DUAL, A WHERE A.TIME < TO_DATE('测试值','YYYYMMDD')) SELECT TO_CHAR(A.TIME,'YYYYMMDD') DATE_TIME, B1.STOCK_TOTAL_WT STOCK_TOTAL_WT_1, B2.STOCK_TOTAL_WT STOCK_TOTAL_WT_2 FROM A LEFT JOIN TFOSMT03A B1 ON TO_CHAR(A.TIME,'YYYYMMDD') = B1.DATE_TIME AND B1.FACTORY_DIV = 'A10' LEFT JOIN TFOSMT03A B2 ON TO_CHAR(A.TIME,'YYYYMMDD') = B2.DATE_TIME AND B2.FACTORY_DIV = 'A20' WHERE 1 = 1;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-279 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosm02_inq.cpp | 函数: f_fosm02_inq | 锚点: L450-L464
-- 参数: @DATE_TIME='测试值'
WITH A(LEVEL, TIME) AS (SELECT 1, TO_DATE('测试值','YYYYMMDD') - 6 FROM DUAL WHERE 1 = 1 UNION ALL SELECT LEVEL + 1,TIME + 1 FROM DUAL, A WHERE A.TIME < TO_DATE('测试值','YYYYMMDD')) SELECT TO_CHAR(A.TIME,'YYYYMMDD') DATE_TIME, B1.CC_REMAIN_RATE / 100 CC_REMAIN_RATE_1, B2.CC_REMAIN_RATE / 100 CC_REMAIN_RATE_2 FROM A LEFT JOIN TFOSMT03A B1 ON TO_CHAR(A.TIME,'YYYYMMDD') = B1.DATE_TIME AND B1.FACTORY_DIV = 'A10' LEFT JOIN TFOSMT03A B2 ON TO_CHAR(A.TIME,'YYYYMMDD') = B2.DATE_TIME AND B2.FACTORY_DIV = 'A20' WHERE 1 = 1;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-280 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosm02_inq.cpp | 函数: f_fosm02_inq | 锚点: L628-L636
-- 参数: @DATE_TIME='测试值'
SELECT DATE_TIME, IRON_SLAB_RATE IRON_SLAB_RATE FROM TFOSMT03A WHERE 1 = 1 AND DATE_TIME > TO_CHAR((TO_DATE('测试值','YYYYMMDD') - 7),'YYYYMMDD') AND DATE_TIME <= '测试值' AND FACTORY_DIV = 'A10' ORDER BY DATE_TIME;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-281 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosm02_inq.cpp | 函数: f_fosm02_inq | 锚点: L668-L676
-- 参数: @DATE_TIME='测试值'
SELECT DATE_TIME, IRON_SLAB_RATE IRON_SLAB_RATE FROM TFOSMT03A WHERE 1 = 1 AND DATE_TIME > TO_CHAR((TO_DATE('测试值','YYYYMMDD') - 7),'YYYYMMDD') AND DATE_TIME <= '测试值' AND FACTORY_DIV = 'A20' ORDER BY DATE_TIME;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-282 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosm02_inq.cpp | 函数: f_fosm02_inq | 锚点: L736-L770
-- 参数: @DATE_TIME='测试值'
WITH A(LEVEL, TIME) AS (SELECT 1, TO_DATE('测试值','YYYYMMDD') - 9 FROM DUAL WHERE 1 = 1 UNION ALL SELECT LEVEL + 1,TIME + 1 FROM DUAL, A WHERE A.TIME < TO_DATE('测试值','YYYYMMDD')) SELECT TO_CHAR(A.TIME,'YYYYMMDD') DATE_TIME, B1.IRON_RELEASE_WT IRON_RELEASE_WT_1, B1.SEQ_NO DEDUCT_PT_1, B2.IRON_RELEASE_WT IRON_RELEASE_WT_2, B2.SEQ_NO DEDUCT_PT_2, B3.IRON_RELEASE_WT IRON_RELEASE_WT_3, B3.SEQ_NO DEDUCT_PT_3, B4.IRON_RELEASE_WT IRON_RELEASE_WT_4, B4.SEQ_NO DEDUCT_PT_4, B5.IRON_RELEASE_WT IRON_RELEASE_WT_5, B5.SEQ_NO DEDUCT_PT_5, B6.IRON_RELEASE_WT IRON_RELEASE_WT_6, B6.SEQ_NO DEDUCT_PT_6, B7.IRON_RELEASE_WT IRON_RELEASE_WT_7, B7.SEQ_NO DEDUCT_PT_7, CASE WHEN B1.REMARK IS NULL THEN '' ELSE TRIM(B1.REMARK) END || CASE WHEN B2.REMARK IS NULL THEN '' ELSE TRIM(B2.REMARK) END || CASE WHEN B3.REMARK IS NULL THEN '' ELSE TRIM(B3.REMARK) END || CASE WHEN B4.REMARK IS NULL THEN '' ELSE TRIM(B4.REMARK) END || CASE WHEN B5.REMARK IS NULL THEN '' ELSE TRIM(B5.REMARK) END || CASE WHEN B6.REMARK IS NULL THEN '' ELSE TRIM(B6.REMARK) END || CASE WHEN B7.REMARK IS NULL THEN '' ELSE TRIM(B7.REMARK) END REMARK FROM A LEFT JOIN TFOSMT03B B1 ON TO_CHAR(A.TIME,'YYYYMMDD') = B1.DATE_TIME AND B1.DEP_NAME = '02' LEFT JOIN TFOSMT03B B2 ON TO_CHAR(A.TIME,'YYYYMMDD') = B2.DATE_TIME AND B2.DEP_NAME = '03' LEFT JOIN TFOSMT03B B3 ON TO_CHAR(A.TIME,'YYYYMMDD') = B3.DATE_TIME AND B3.DEP_NAME = '05' LEFT JOIN TFOSMT03B B4 ON TO_CHAR(A.TIME,'YYYYMMDD') = B4.DATE_TIME AND B4.DEP_NAME = '04' LEFT JOIN TFOSMT03B B5 ON TO_CHAR(A.TIME,'YYYYMMDD') = B5.DATE_TIME AND B5.DEP_NAME = '01' LEFT JOIN TFOSMT03B B6 ON TO_CHAR(A.TIME,'YYYYMMDD') = B6.DATE_TIME AND B6.DEP_NAME = '07' LEFT JOIN TFOSMT03B B7 ON TO_CHAR(A.TIME,'YYYYMMDD') = B7.DATE_TIME AND B7.DEP_NAME = '10' WHERE 1 = 1;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-283 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosm02_inq.cpp | 函数: f_fosm02_inq | 锚点: L860-L872
-- 参数: @DATE_TIME='测试值'
SELECT A.FACTORY_DIV, A.DATE_TIME, A.SHIFT_NO, A.SHIFT_GROUP, A.PLAN_CHARGE, A.SMELT_CHARGE, A.PRODUCT_CHARGE, B.ADJUST_CHARGE, DECODE(B.START_TIME, ' ', ' ', (TO_CHAR(TO_DATE(B.START_TIME, 'YYYYMMDDHH24MISS'), 'HH24:MI')) || '-' || DECODE(B.START_TIME, ' ', ' ', TO_CHAR(TO_DATE(B.END_TIME, 'YYYYMMDDHH24MISS'), 'HH24:MI'))) PERIOD_TIME, B.REMARK, B.STOP_TOTAL_TIME, B.DEP_NAME FROM TFOSMT04A A LEFT JOIN TFOSMT04B B ON A.FACTORY_DIV = B.FACTORY_DIV AND A.DATE_TIME = B.DATE_TIME AND A.SHIFT_NO = B.SHIFT_NO WHERE A.FACTORY_DIV = 'A10' AND ((A.DATE_TIME = '测试值' AND A.SHIFT_NO = '1') OR A.DATE_TIME = TO_CHAR(TO_DATE('测试值','YYYYMMDD') - 1,'YYYYMMDD') AND A.SHIFT_NO <> '1') ORDER BY A.DATE_TIME, A.SHIFT_NO, B.CHARGE_NO;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-284 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosm02_inq.cpp | 函数: f_fosm02_inq | 锚点: L908-L920
-- 参数: @DATE_TIME='测试值'
SELECT A.FACTORY_DIV, A.DATE_TIME, A.SHIFT_NO, A.SHIFT_GROUP, A.PLAN_CHARGE, A.SMELT_CHARGE, A.PRODUCT_CHARGE, B.ADJUST_CHARGE, DECODE(B.START_TIME, ' ', ' ', (TO_CHAR(TO_DATE(B.START_TIME, 'YYYYMMDDHH24MISS'), 'HH24:MI')) || '-' || DECODE(B.START_TIME, ' ', ' ', TO_CHAR(TO_DATE(B.END_TIME, 'YYYYMMDDHH24MISS'), 'HH24:MI'))) PERIOD_TIME, B.REMARK, B.STOP_TOTAL_TIME, B.DEP_NAME FROM TFOSMT04A A LEFT JOIN TFOSMT04B B ON A.FACTORY_DIV = B.FACTORY_DIV AND A.DATE_TIME = B.DATE_TIME AND A.SHIFT_NO = B.SHIFT_NO WHERE A.FACTORY_DIV = 'A20' AND ((A.DATE_TIME = '测试值' AND A.SHIFT_NO = '1') OR A.DATE_TIME = TO_CHAR(TO_DATE('测试值','YYYYMMDD') - 1,'YYYYMMDD') AND A.SHIFT_NO <> '1') ORDER BY A.DATE_TIME, A.SHIFT_NO, B.CHARGE_NO;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-285 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosm02_inq.cpp | 函数: f_fosm02_inq | 锚点: L955-L962
-- 参数: @DATE_TIME='测试值'
SELECT * FROM TFOSMT05A WHERE FACTORY_DIV = 'A10' AND DATE_TIME > TO_CHAR(TO_DATE('测试值','YYYYMMDD') - 3,'YYYYMMDD') AND DATE_TIME <= '测试值' ORDER BY DATE_TIME, SEQ_NO;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-286 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosm02_inq.cpp | 函数: f_fosm02_inq | 锚点: L993-L1000
-- 参数: @DATE_TIME='测试值'
SELECT * FROM TFOSMT05A WHERE FACTORY_DIV = 'A20' AND DATE_TIME > TO_CHAR(TO_DATE('测试值','YYYYMMDD') - 3,'YYYYMMDD') AND DATE_TIME <= '测试值' ORDER BY DATE_TIME;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-287 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosm02_inq.cpp | 函数: f_fosm02_inq | 锚点: L1034-L1042
-- 参数: @DATE_TIME='测试值'
SELECT DATE_TIME, COUNT(HEAT_NO) COUNT_PONO FROM TFOSMT05A WHERE FACTORY_DIV = 'A10' AND DATE_TIME > TO_CHAR(TO_DATE('测试值','YYYYMMDD') - 7,'YYYYMMDD') AND DATE_TIME <= '测试值' GROUP BY DATE_TIME ORDER BY DATE_TIME;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-288 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosm02_inq.cpp | 函数: f_fosm02_inq | 锚点: L1074-L1082
-- 参数: @DATE_TIME='测试值'
SELECT DATE_TIME, COUNT(HEAT_NO) COUNT_PONO FROM TFOSMT05A WHERE FACTORY_DIV = 'A20' AND DATE_TIME > TO_CHAR(TO_DATE('测试值','YYYYMMDD') - 7,'YYYYMMDD') AND DATE_TIME <= '测试值' GROUP BY DATE_TIME ORDER BY DATE_TIME;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-289 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosm02_inq.cpp | 函数: f_fosm02_inq | 锚点: L1116-L1124
-- 参数: @DATE_TIME='测试值'
SELECT ELM_DESC, COUNT(ELM_DESC) COUNT_PONO FROM TFOSMT05A WHERE FACTORY_DIV = 'A10' AND DATE_TIME > TO_CHAR(TO_DATE('测试值','YYYYMMDD') - 30,'YYYYMMDD') AND DATE_TIME <= '测试值' GROUP BY ELM_DESC ORDER BY ELM_DESC;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-290 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosm02_inq.cpp | 函数: f_fosm02_inq | 锚点: L1156-L1164
-- 参数: @DATE_TIME='测试值'
SELECT ELM_DESC, COUNT(ELM_DESC) COUNT_PONO FROM TFOSMT05A WHERE FACTORY_DIV = 'A20' AND DATE_TIME > TO_CHAR(TO_DATE('测试值','YYYYMMDD') - 30,'YYYYMMDD') AND DATE_TIME <= '测试值' GROUP BY ELM_DESC ORDER BY ELM_DESC;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-291 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosm02_inq.cpp | 函数: f_fosm02_inq | 锚点: L1196-L1202
-- 参数: @DATE_TIME='测试值'
SELECT DATE_TIME, SHIFT_GROUP, HEAT_NO, OLD_ST_NO, ST_NO, REMARK FROM TFOSMT05B WHERE FACTORY_DIV = 'A10' AND DATE_TIME > TO_CHAR(TO_DATE('测试值','YYYYMMDD') - 3,'YYYYMMDD') AND DATE_TIME <= '测试值';

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-292 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosm02_inq.cpp | 函数: f_fosm02_inq | 锚点: L1232-L1238
-- 参数: @DATE_TIME='测试值'
SELECT DATE_TIME, SHIFT_GROUP, HEAT_NO, OLD_ST_NO, ST_NO, REMARK FROM TFOSMT05B WHERE FACTORY_DIV = 'A20' AND DATE_TIME > TO_CHAR(TO_DATE('测试值','YYYYMMDD') - 3,'YYYYMMDD') AND DATE_TIME <= '测试值';

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-293 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosm02_inq.cpp | 函数: f_fosm02_inq | 锚点: L1355-L1363
-- 参数: @DATE_TIME='测试值'
SELECT DATE_TIME, CC_MACH_NO, SUM(PRODUCT_CHARGE), SUM(QUALIFIED_CHARGE), ROUND(SUM(PRODUCT_CHARGE) / SUM(QUALIFIED_CHARGE), 4) QUALIFIED_RATE FROM TFOSMT05C WHERE FACTORY_DIV = 'A20' AND DATE_TIME > TO_CHAR(TO_DATE('测试值','YYYYMMDD') - 7,'YYYYMMDD') AND DATE_TIME <= '测试值' GROUP BY DATE_TIME, CC_MACH_NO ORDER BY DATE_TIME, CC_MACH_NO;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-294 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosm02_inq.cpp | 函数: f_fosm02_inq | 锚点: L1471-L1524
-- 参数: @DATE_TIME='测试值'
WITH T AS ( SELECT A.FACTORY_DIV, A.DEP_NAME, A.RATE RATE_TARGET, B1.RATE RATE_1, B2.RATE RATE_2, B3.RATE RATE_3, B4.RATE RATE_4, B5.RATE RATE_5, CAST(ROUND((B1.RATE + B2.RATE + B3.RATE + B4.RATE + B5.RATE) / 5, 3) AS DECIMAL(5,3)) RATE_AVG FROM TFOSMT06B A LEFT JOIN TFOSMT06A B1 ON A.FACTORY_DIV = B1.FACTORY_DIV AND A.DEP_NAME = B1.DEP_NAME AND B1.DATE_TIME = TO_CHAR(TO_DATE('测试值','YYYYMMDD') - 4,'YYYYMMDD') LEFT JOIN TFOSMT06A B2 ON A.FACTORY_DIV = B2.FACTORY_DIV AND A.DEP_NAME = B2.DEP_NAME AND B2.DATE_TIME = TO_CHAR(TO_DATE('测试值','YYYYMMDD') - 4,'YYYYMMDD') LEFT JOIN TFOSMT06A B3 ON A.FACTORY_DIV = B3.FACTORY_DIV AND A.DEP_NAME = B3.DEP_NAME AND B3.DATE_TIME = TO_CHAR(TO_DATE('测试值','YYYYMMDD') - 4,'YYYYMMDD') LEFT JOIN TFOSMT06A B4 ON A.FACTORY_DIV = B4.FACTORY_DIV AND A.DEP_NAME = B4.DEP_NAME AND B4.DATE_TIME = TO_CHAR(TO_DATE('测试值','YYYYMMDD') - 4,'YYYYMMDD') LEFT JOIN TFOSMT06A B5 ON A.FACTORY_DIV = B5.FACTORY_DIV AND A.DEP_NAME = B5.DEP_NAME AND B5.DATE_TIME = TO_CHAR(TO_DATE('测试值','YYYYMMDD') - 4,'YYYYMMDD') ORDER BY FACTORY_DIV, DEP_NAME ) SELECT * FROM T WHERE FACTORY_DIV = 'A10' UNION ALL SELECT FACTORY_DIV, '综合' DEP_NAME, SUM(RATE_TARGET), SUM(RATE_1), SUM(RATE_2), SUM(RATE_3), SUM(RATE_4), SUM(RATE_5), SUM(RATE_AVG) FROM T WHERE FACTORY_DIV = 'A10' GROUP BY FACTORY_DIV UNION ALL SELECT * FROM T WHERE FACTORY_DIV = 'A20' UNION ALL SELECT FACTORY_DIV, '综合' DEP_NAME, SUM(RATE_TARGET), SUM(RATE_1), SUM(RATE_2), SUM(RATE_3), SUM(RATE_4), SUM(RATE_5), SUM(RATE_AVG) FROM T WHERE FACTORY_DIV = 'A20' GROUP BY FACTORY_DIV UNION ALL SELECT '合计', '', AVG(RATE_TARGET), AVG(RATE_1), AVG(RATE_2), AVG(RATE_3), AVG(RATE_4), AVG(RATE_5), AVG(RATE_AVG) FROM ( SELECT FACTORY_DIV, '综合' DEP_NAME, SUM(RATE_TARGET) RATE_TARGET, SUM(RATE_1) RATE_1, SUM(RATE_2) RATE_2, SUM(RATE_3) RATE_3, SUM(RATE_4) RATE_4, SUM(RATE_5) RATE_5, SUM(RATE_AVG) RATE_AVG FROM T WHERE FACTORY_DIV = 'A10' GROUP BY FACTORY_DIV UNION ALL SELECT FACTORY_DIV, '综合' DEP_NAME, SUM(RATE_TARGET), SUM(RATE_1), SUM(RATE_2), SUM(RATE_3), SUM(RATE_4), SUM(RATE_5), SUM(RATE_AVG) FROM T WHERE FACTORY_DIV = 'A20' GROUP BY FACTORY_DIV ) T2 ORDER BY FACTORY_DIV, DEP_NAME;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-295 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosm02_inq.cpp | 函数: f_fosm02_inq | 锚点: L1596-L1640
-- 参数: @DATE_TIME='测试值'
WITH A(LEVEL, TIME) AS (SELECT 1, TO_DATE('测试值','YYYYMMDD') - 2 FROM DUAL WHERE 1 = 1 UNION ALL SELECT LEVEL + 1,TIME + 1 FROM DUAL, A WHERE A.TIME < TO_DATE('测试值','YYYYMMDD')), C AS ( SELECT MAT_TYPE, MAT_NAME, FACTORY_DIV, SUM(DEVO_WT) DEVO_WT FROM TFOSMT07A WHERE 1 = 1 AND SUBSTR(DATE_TIME, 1, 6) = SUBSTR('测试值', 1, 6) GROUP BY MAT_TYPE, MAT_NAME, FACTORY_DIV ) SELECT TO_CHAR(A.TIME,'YYYYMMDD') DATE_TIME, B1.DEVO_WT DEVO_WT_1, B2.DEVO_WT DEVO_WT_2, B3.DEVO_WT DEVO_WT_3, B1.DEVO_WT + B2.DEVO_WT+ B3.DEVO_WT DEVO_WT_4, B4.DEVO_WT DEVO_WT_5, B5.DEVO_WT DEVO_WT_6, B4.DEVO_WT + B5.DEVO_WT DEVO_WT_7, B6.DEVO_WT DEVO_WT_8, B7.DEVO_WT DEVO_WT_9, B6.DEVO_WT + B7.DEVO_WT DEVO_WT_10 FROM A LEFT JOIN TFOSMT07A B1 ON TO_CHAR(A.TIME,'YYYYMMDD') = B1.DATE_TIME AND B1.MAT_TYPE = '1' AND B1.MAT_NAME = '渣钢大块' LEFT JOIN TFOSMT07A B2 ON TO_CHAR(A.TIME,'YYYYMMDD') = B2.DATE_TIME AND B2.MAT_TYPE = '1' AND B2.MAT_NAME = '渣钢粒' LEFT JOIN TFOSMT07A B3 ON TO_CHAR(A.TIME,'YYYYMMDD') = B3.DATE_TIME AND B3.MAT_TYPE = '1' AND B3.MAT_NAME = '豆钢' LEFT JOIN TFOSMT07A B4 ON TO_CHAR(A.TIME,'YYYYMMDD') = B4.DATE_TIME AND B4.MAT_TYPE = '2' AND B4.MAT_NAME = '渣铁大块' LEFT JOIN TFOSMT07A B5 ON TO_CHAR(A.TIME,'YYYYMMDD') = B5.DATE_TIME AND B5.MAT_TYPE = '2' AND B5.MAT_NAME = '渣铁300' LEFT JOIN TFOSMT07A B6 ON TO_CHAR(A.TIME,'YYYYMMDD') = B6.DATE_TIME AND B6.MAT_TYPE = '3' AND B6.FACTORY_DIV = 'A10' LEFT JOIN TFOSMT07A B7 ON TO_CHAR(A.TIME,'YYYYMMDD') = B7.DATE_TIME AND B7.MAT_TYPE = '3' AND B7.FACTORY_DIV = 'A20' UNION ALL SELECT '合计', C1.DEVO_WT, C2.DEVO_WT, C3.DEVO_WT, C1.DEVO_WT + C2.DEVO_WT + C3.DEVO_WT, C4.DEVO_WT, C5.DEVO_WT, C4.DEVO_WT + C5.DEVO_WT, C6.DEVO_WT, C7.DEVO_WT, C6.DEVO_WT + C7.DEVO_WT FROM DUAL LEFT JOIN C C1 ON C1.MAT_TYPE = '1' AND C1.MAT_NAME = '渣钢大块' LEFT JOIN C C2 ON C2.MAT_TYPE = '1' AND C2.MAT_NAME = '渣钢粒' LEFT JOIN C C3 ON C3.MAT_TYPE = '1' AND C3.MAT_NAME = '豆钢' LEFT JOIN C C4 ON C4.MAT_TYPE = '2' AND C4.MAT_NAME = '渣铁大块' LEFT JOIN C C5 ON C5.MAT_TYPE = '2' AND C5.MAT_NAME = '渣铁300' LEFT JOIN C C6 ON C6.MAT_TYPE = '3' AND C6.FACTORY_DIV = 'A10' LEFT JOIN C C7 ON C7.MAT_TYPE = '3' AND C7.FACTORY_DIV = 'A20' WHERE 1 = 1 ORDER BY DATE_TIME;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-296 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosm02_inq.cpp | 函数: f_fosm02_inq | 锚点: L1717-L1770
-- 参数: @DATE_TIME='测试值'
WITH A(LEVEL, TIME) AS (SELECT 1, TO_DATE('测试值','YYYYMMDD') - 2 FROM DUAL WHERE 1 = 1 UNION ALL SELECT LEVEL + 1,TIME + 1 FROM DUAL, A WHERE A.TIME < TO_DATE('测试值','YYYYMMDD')), C AS ( SELECT MAT_TYPE, MAT_NAME, FACTORY_DIV, SUM(DEVO_WT) DEVO_WT FROM TFOSMT07A WHERE 1 = 1 AND SUBSTR(DATE_TIME, 1, 6) = SUBSTR('测试值', 1, 6) GROUP BY MAT_TYPE, MAT_NAME, FACTORY_DIV ) SELECT TO_CHAR(A.TIME,'YYYYMMDD') DATE_TIME, B1.DEVO_WT DEVO_WT_1, B2.DEVO_WT DEVO_WT_2, B3.DEVO_WT DEVO_WT_3, B1.DEVO_WT + B2.DEVO_WT+ B3.DEVO_WT DEVO_WT_4, B4.DEVO_WT DEVO_WT_5, B5.DEVO_WT DEVO_WT_6, B6.DEVO_WT DEVO_WT_7, B4.DEVO_WT + B5.DEVO_WT + B6.DEVO_WT DEVO_WT_8, B7.DEVO_WT DEVO_WT_9, B8.DEVO_WT DEVO_WT_10, B7.DEVO_WT + B8.DEVO_WT DEVO_WT_11, B9.DEVO_WT DEVO_WT_12, BA.DEVO_WT DEVO_WT_13, B9.DEVO_WT + BA.DEVO_WT DEVO_WT_14 FROM A LEFT JOIN TFOSMT07A B1 ON TO_CHAR(A.TIME,'YYYYMMDD') = B1.DATE_TIME AND B1.MAT_TYPE = '4' AND B1.MAT_NAME = '渣钢' LEFT JOIN TFOSMT07A B2 ON TO_CHAR(A.TIME,'YYYYMMDD') = B2.DATE_TIME AND B2.MAT_TYPE = '4' AND B2.MAT_NAME = '切割' LEFT JOIN TFOSMT07A B3 ON TO_CHAR(A.TIME,'YYYYMMDD') = B3.DATE_TIME AND B3.MAT_TYPE = '4' AND B3.MAT_NAME = '中包' LEFT JOIN TFOSMT07A B4 ON TO_CHAR(A.TIME,'YYYYMMDD') = B4.DATE_TIME AND B4.MAT_TYPE = '5' AND B4.MAT_NAME = '渣盆' LEFT JOIN TFOSMT07A B5 ON TO_CHAR(A.TIME,'YYYYMMDD') = B5.DATE_TIME AND B5.MAT_TYPE = '5' AND B5.MAT_NAME = '落锤' LEFT JOIN TFOSMT07A B6 ON TO_CHAR(A.TIME,'YYYYMMDD') = B6.DATE_TIME AND B6.MAT_TYPE = '5' AND B6.MAT_NAME = '中包' LEFT JOIN TFOSMT07A B7 ON TO_CHAR(A.TIME,'YYYYMMDD') = B7.DATE_TIME AND B7.MAT_TYPE = '6' AND B7.FACTORY_DIV = 'A10' LEFT JOIN TFOSMT07A B8 ON TO_CHAR(A.TIME,'YYYYMMDD') = B8.DATE_TIME AND B8.MAT_TYPE = '6' AND B8.FACTORY_DIV = 'A20' LEFT JOIN TFOSMT07A B9 ON TO_CHAR(A.TIME,'YYYYMMDD') = B9.DATE_TIME AND B9.MAT_TYPE = '7' AND B9.FACTORY_DIV = 'A10' LEFT JOIN TFOSMT07A BA ON TO_CHAR(A.TIME,'YYYYMMDD') = BA.DATE_TIME AND BA.MAT_TYPE = '7' AND BA.FACTORY_DIV = 'A20' UNION ALL SELECT '合计', C1.DEVO_WT, C2.DEVO_WT, C3.DEVO_WT, C1.DEVO_WT + C2.DEVO_WT + C3.DEVO_WT, C4.DEVO_WT, C5.DEVO_WT, C6.DEVO_WT, C4.DEVO_WT + C5.DEVO_WT + C6.DEVO_WT, C7.DEVO_WT, C8.DEVO_WT, C7.DEVO_WT + C8.DEVO_WT, C9.DEVO_WT, CA.DEVO_WT, C9.DEVO_WT + CA.DEVO_WT FROM DUAL LEFT JOIN C C1 ON C1.MAT_TYPE = '4' AND C1.MAT_NAME = '渣钢' LEFT JOIN C C2 ON C2.MAT_TYPE = '4' AND C2.MAT_NAME = '切割' LEFT JOIN C C3 ON C3.MAT_TYPE = '4' AND C3.MAT_NAME = '中包' LEFT JOIN C C4 ON C4.MAT_TYPE = '5' AND C4.MAT_NAME = '渣盆' LEFT JOIN C C5 ON C5.MAT_TYPE = '5' AND C5.MAT_NAME = '落锤' LEFT JOIN C C6 ON C6.MAT_TYPE = '5' AND C6.MAT_NAME = '中包' LEFT JOIN C C7 ON C7.MAT_TYPE = '6' AND C7.FACTORY_DIV = 'A10' LEFT JOIN C C8 ON C8.MAT_TYPE = '6' AND C8.FACTORY_DIV = 'A20' LEFT JOIN C C9 ON C9.MAT_TYPE = '7' AND C9.FACTORY_DIV = 'A10' LEFT JOIN C CA ON CA.MAT_TYPE = '7' AND CA.FACTORY_DIV = 'A20' WHERE 1 = 1 ORDER BY DATE_TIME;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-297 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosm02_inq.cpp | 函数: f_fosm02_inq | 锚点: L1839-L1849
-- 参数: @DATE_TIME='测试值'
SELECT A1.ENERGY_CODE, A1.ENERGY_CNAME, A1.UNIT, A1.PRICE, A1.VALUE_REAL, A1.VALUE_TARGET, B1.VALUE_DAY VALUE_DAY_1, B2.VALUE_DAY VALUE_DAY_2, B3.VALUE_DAY VALUE_DAY_3, B4.VALUE_DAY VALUE_MONTH FROM TFOSMT09B A1 LEFT JOIN TFOSMT09A B1 ON A1.ENERGY_CODE = B1.ENERGY_CODE AND B1.DATE_TIME = TO_CHAR((TO_DATE('测试值','YYYYMMDD') - 2),'YYYYMMDD') LEFT JOIN TFOSMT09A B2 ON A1.ENERGY_CODE = B2.ENERGY_CODE AND B2.DATE_TIME = TO_CHAR((TO_DATE('测试值','YYYYMMDD') - 1),'YYYYMMDD') LEFT JOIN TFOSMT09A B3 ON A1.ENERGY_CODE = B3.ENERGY_CODE AND B3.DATE_TIME = '测试值' LEFT JOIN (SELECT ENERGY_CODE, SUM(VALUE_DAY) VALUE_DAY FROM TFOSMT09A WHERE SUBSTR(DATE_TIME,1,6) = SUBSTR('测试值',1,6) GROUP BY ENERGY_CODE) B4 ON A1.ENERGY_CODE = B4.ENERGY_CODE WHERE 1 = 1;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-298 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosm02_inq.cpp | 函数: f_fosm02_inq | 锚点: L1940-L1947
-- 参数: @DATE_TIME='测试值'
SELECT A.DATE_TIME, A.IRON_S VALUE FROM TFOSMT10I A WHERE 1 = 1 AND DATE_TIME > TO_CHAR((TO_DATE('测试值','YYYYMMDD') - 7),'YYYYMMDD') AND DATE_TIME <= '测试值' AND STATION_NO = '2';

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-299 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosm02_inq.cpp | 函数: f_fosm02_inq | 锚点: L1978-L1985
-- 参数: @DATE_TIME='测试值'
SELECT A.DATE_TIME, A.IRON_S VALUE FROM TFOSMT10I A WHERE 1 = 1 AND DATE_TIME > TO_CHAR((TO_DATE('测试值','YYYYMMDD') - 7),'YYYYMMDD') AND DATE_TIME <= '测试值' AND STATION_NO = '4';

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-300 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosm02_inq.cpp | 函数: f_fosm02_inq | 锚点: L2016-L2023
-- 参数: @DATE_TIME='测试值'
SELECT A.DATE_TIME, A.IRON_S VALUE FROM TFOSMT10I A WHERE 1 = 1 AND DATE_TIME > TO_CHAR((TO_DATE('测试值','YYYYMMDD') - 7),'YYYYMMDD') AND DATE_TIME <= '测试值' AND STATION_NO = '5';

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-301 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosm02_inq.cpp | 函数: f_fosm02_inq | 锚点: L2180-L2188
-- 参数: @DATE_TIME='测试值'
SELECT A.DATE_TIME, A.ADJUST_CHARGE ADJUST_CHARGE_1, A.MOLTIRON_WT MOLTIRON_WT_1, A.REMARK REMARK_1, B.ADJUST_CHARGE ADJUST_CHARGE_2, B.MOLTIRON_WT MOLTIRON_WT_2, B.REMARK REMARK_2, A.ADJUST_CHARGE + B.ADJUST_CHARGE MOLTIRON_WT_TOTAL FROM TFOSMT10D A LEFT JOIN TFOSMT10D B ON A.DATE_TIME = B.DATE_TIME AND B.FACTORY_DIV = 'A20' WHERE A.FACTORY_DIV = 'A10' AND A.DATE_TIME > TO_CHAR((TO_DATE('测试值','YYYYMMDD') - 10),'YYYYMMDD') AND A.DATE_TIME <= '测试值';

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-302 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosm02_inq.cpp | 函数: f_fosm02_inq | 锚点: L2250-L2271
-- 参数: @DATE_TIME='测试值'
WITH A(LEVEL, TIME) AS (SELECT 1, TO_DATE('测试值','YYYYMMDD') - 9 FROM DUAL WHERE 1 = 1 UNION ALL SELECT LEVEL + 1,TIME + 1 FROM DUAL, A WHERE A.TIME < TO_DATE('测试值','YYYYMMDD')) SELECT TO_CHAR(A.TIME,'YYYYMMDD') DATE_TIME, B1.RATE RATE_1, B2.RATE RATE_2, B3.RATE RATE_3, B4.RATE RATE_4, B5.RATE RATE_5, B6.RATE RATE_6, B7.RATE RATE_7, B8.RATE RATE_8, B1.RATE + B5.RATE RATE_9, B2.RATE + B6.RATE RATE_10, B3.RATE + B7.RATE RATE_11, B4.RATE + B8.RATE RATE_12 FROM A LEFT JOIN TFOSMT10E B1 ON TO_CHAR(A.TIME,'YYYYMMDD') = B1.DATE_TIME AND B1.FACTORY_DIV = 'A10' AND B1.MAT_NAME = '硅铁单耗' LEFT JOIN TFOSMT10E B2 ON TO_CHAR(A.TIME,'YYYYMMDD') = B2.DATE_TIME AND B2.FACTORY_DIV = 'A10' AND B2.MAT_NAME = '石墨单耗' LEFT JOIN TFOSMT10E B3 ON TO_CHAR(A.TIME,'YYYYMMDD') = B3.DATE_TIME AND B3.FACTORY_DIV = 'A10' AND B3.MAT_NAME = '发热球单耗' LEFT JOIN TFOSMT10E B4 ON TO_CHAR(A.TIME,'YYYYMMDD') = B4.DATE_TIME AND B4.FACTORY_DIV = 'A10' AND B4.MAT_NAME = '折合石墨单耗' LEFT JOIN TFOSMT10E B5 ON TO_CHAR(A.TIME,'YYYYMMDD') = B5.DATE_TIME AND B5.FACTORY_DIV = 'A20' AND B5.MAT_NAME = '硅铁单耗' LEFT JOIN TFOSMT10E B6 ON TO_CHAR(A.TIME,'YYYYMMDD') = B6.DATE_TIME AND B6.FACTORY_DIV = 'A20' AND B6.MAT_NAME = '石墨单耗' LEFT JOIN TFOSMT10E B7 ON TO_CHAR(A.TIME,'YYYYMMDD') = B7.DATE_TIME AND B7.FACTORY_DIV = 'A20' AND B7.MAT_NAME = '发热球单耗' LEFT JOIN TFOSMT10E B8 ON TO_CHAR(A.TIME,'YYYYMMDD') = B8.DATE_TIME AND B8.FACTORY_DIV = 'A20' AND B8.MAT_NAME = '折合石墨单耗';

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-303 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosm02_inq.cpp | 函数: f_fosm02_inq | 锚点: L2338-L2358
-- 参数: @DATE_TIME='测试值'
WITH A(LEVEL, TIME) AS (SELECT 1, TO_DATE('测试值','YYYYMMDD') - 9 FROM DUAL WHERE 1 = 1 UNION ALL SELECT LEVEL + 1,TIME + 1 FROM DUAL, A WHERE A.TIME < TO_DATE('测试值','YYYYMMDD')) SELECT TO_CHAR(A.TIME,'YYYYMMDD') DATE_TIME, B1.PRODUCT_CHARGE + B2.PRODUCT_CHARGE PRODUCT_CHARGE_1, B1.SMELT_CHARGE SMELT_CHARGE_L1, B1.RATE RATE_L1, B1.TOTAL_DURATION TOTAL_DURATION_L1, B2.SMELT_CHARGE SMELT_CHARGE_R1, B2.RATE RATE_R1, B3.PRODUCT_CHARGE + B4.PRODUCT_CHARGE PRODUCT_CHARGE_2, B3.SMELT_CHARGE SMELT_CHARGE_L2, B3.RATE RATE_L2, B3.TOTAL_DURATION TOTAL_DURATION_L2, B4.SMELT_CHARGE SMELT_CHARGE_R2, B4.RATE RATE_R2 FROM A LEFT JOIN TFOSMT10F B1 ON TO_CHAR(A.TIME,'YYYYMMDD') = B1.DATE_TIME AND B1.FACTORY_DIV = 'A10' AND B1.STATION_ID = 'L' LEFT JOIN TFOSMT10F B2 ON TO_CHAR(A.TIME,'YYYYMMDD') = B2.DATE_TIME AND B2.FACTORY_DIV = 'A10' AND B2.STATION_ID = 'L' LEFT JOIN TFOSMT10F B3 ON TO_CHAR(A.TIME,'YYYYMMDD') = B3.DATE_TIME AND B3.FACTORY_DIV = 'A20' AND B3.STATION_ID = 'R' LEFT JOIN TFOSMT10F B4 ON TO_CHAR(A.TIME,'YYYYMMDD') = B4.DATE_TIME AND B4.FACTORY_DIV = 'A20' AND B4.STATION_ID = 'R';

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-304 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosm02_inq.cpp | 函数: f_fosm02_inq | 锚点: L2510-L2539
-- 参数: @DATE_TIME='测试值'
SELECT A.CODE, A.CODE_DESC_2_CONTENT, 'A10' FACTORY_DIV, A.CODE_DESC_1_CONTENT STATION_NAME, B1.STATION_NO STATION_NO_1, B2.STATION_NO STATION_NO_2, B3.STATION_NO STATION_NO_3, B4.STATION_NO STATION_NO_4, B5.STATION_NO STATION_NO_5, B6.STATION_NO STATION_NO_6, B7.STATION_NO STATION_NO_7, B1.START_TIME || '-' || B1.END_TIME PERIOD_TIME, B1.REMARK FROM TEP0002 A LEFT JOIN TFOSMT11A B1 ON A.CODE = B1.STATION_ID AND B1.FACTORY_DIV = 'A10' AND B1.DATE_TIME = '测试值' LEFT JOIN TFOSMT11A B2 ON A.CODE = B2.STATION_ID AND B2.FACTORY_DIV = 'A10' AND B2.DATE_TIME = TO_CHAR((TO_DATE('测试值','YYYYMMDD') + 1),'YYYYMMDD') LEFT JOIN TFOSMT11A B3 ON A.CODE = B3.STATION_ID AND B3.FACTORY_DIV = 'A10' AND B3.DATE_TIME = TO_CHAR((TO_DATE('测试值','YYYYMMDD') + 2),'YYYYMMDD') LEFT JOIN TFOSMT11A B4 ON A.CODE = B4.STATION_ID AND B4.FACTORY_DIV = 'A10' AND B4.DATE_TIME = TO_CHAR((TO_DATE('测试值','YYYYMMDD') + 3),'YYYYMMDD') LEFT JOIN TFOSMT11A B5 ON A.CODE = B5.STATION_ID AND B5.FACTORY_DIV = 'A10' AND B5.DATE_TIME = TO_CHAR((TO_DATE('测试值','YYYYMMDD') + 4),'YYYYMMDD') LEFT JOIN TFOSMT11A B6 ON A.CODE = B6.STATION_ID AND B6.FACTORY_DIV = 'A10' AND B6.DATE_TIME = TO_CHAR((TO_DATE('测试值','YYYYMMDD') + 5),'YYYYMMDD') LEFT JOIN TFOSMT11A B7 ON A.CODE = B7.STATION_ID AND B7.FACTORY_DIV = 'A10' AND B7.DATE_TIME = TO_CHAR((TO_DATE('测试值','YYYYMMDD') + 6),'YYYYMMDD') WHERE A.CODE_CLASS = 'FOSMT2' UNION ALL SELECT A.CODE, A.CODE_DESC_2_CONTENT, 'A20' FACTORY_DIV, A.CODE_DESC_1_CONTENT STATION_NAME, B1.STATION_NO STATION_NO_1, B2.STATION_NO STATION_NO_2, B3.STATION_NO STATION_NO_3, B4.STATION_NO STATION_NO_4, B5.STATION_NO STATION_NO_5, B6.STATION_NO STATION_NO_6, B7.STATION_NO STATION_NO_7, B1.START_TIME || '-' || B1.END_TIME PERIOD_TIME, B1.REMARK FROM TEP0002 A LEFT JOIN TFOSMT11A B1 ON A.CODE = B1.STATION_ID AND B1.FACTORY_DIV = 'A20' AND B1.DATE_TIME = '测试值' LEFT JOIN TFOSMT11A B2 ON A.CODE = B2.STATION_ID AND B2.FACTORY_DIV = 'A20' AND B2.DATE_TIME = TO_CHAR((TO_DATE('测试值','YYYYMMDD') + 1),'YYYYMMDD') LEFT JOIN TFOSMT11A B3 ON A.CODE = B3.STATION_ID AND B3.FACTORY_DIV = 'A20' AND B3.DATE_TIME = TO_CHAR((TO_DATE('测试值','YYYYMMDD') + 2),'YYYYMMDD') LEFT JOIN TFOSMT11A B4 ON A.CODE = B4.STATION_ID AND B4.FACTORY_DIV = 'A20' AND B4.DATE_TIME = TO_CHAR((TO_DATE('测试值','YYYYMMDD') + 3),'YYYYMMDD') LEFT JOIN TFOSMT11A B5 ON A.CODE = B5.STATION_ID AND B5.FACTORY_DIV = 'A20' AND B5.DATE_TIME = TO_CHAR((TO_DATE('测试值','YYYYMMDD') + 4),'YYYYMMDD') LEFT JOIN TFOSMT11A B6 ON A.CODE = B6.STATION_ID AND B6.FACTORY_DIV = 'A20' AND B6.DATE_TIME = TO_CHAR((TO_DATE('测试值','YYYYMMDD') + 5),'YYYYMMDD') LEFT JOIN TFOSMT11A B7 ON A.CODE = B7.STATION_ID AND B7.FACTORY_DIV = 'A20' AND B7.DATE_TIME = TO_CHAR((TO_DATE('测试值','YYYYMMDD') + 6),'YYYYMMDD') WHERE A.CODE_CLASS = 'FOSMT2' ORDER BY FACTORY_DIV, CODE_DESC_2_CONTENT;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-305 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosmt00_inq.cpp | 函数: f_fosmt00_inq | 锚点: L213-L228
-- 参数: @DATE_TIME='测试值'
SELECT A.CODE, A.CODE_DESC_1_CONTENT DEP_NAME, C.BREAKDN_DATE, C.REMARK REMARK_BFR, B.REMARK, CASE WHEN B.BREAKDN_DATE IS NULL THEN DATEDIFF(DAY, TO_DATE(C.BREAKDN_DATE,'YYYYMMDD'), TO_DATE('测试值','YYYYMMDD')) ELSE 0 END OPERATE_CYCLE, CASE WHEN C.TOTAL_OPERATE_CYCLE IS NULL OR CASE WHEN B.REMARK IS NULL THEN DATEDIFF(DAY, TO_DATE(C.BREAKDN_DATE,'YYYYMMDD'), TO_DATE('测试值','YYYYMMDD')) ELSE B.TOTAL_OPERATE_CYCLE END IS NULL THEN NULL ELSE GREATEST(C.TOTAL_OPERATE_CYCLE, CASE WHEN B.REMARK IS NULL THEN DATEDIFF(DAY, TO_DATE(C.BREAKDN_DATE,'YYYYMMDD'), TO_DATE('测试值','YYYYMMDD')) ELSE B.TOTAL_OPERATE_CYCLE END) END TOTAL_OPERATE_CYCLE FROM TEP0002 A LEFT JOIN TFOSMT02A B ON A.CODE = B.DEP_NAME AND B.BREAKDN_DATE = '测试值' LEFT JOIN (SELECT DEP_NAME, REMARK, BREAKDN_DATE, TOTAL_OPERATE_CYCLE FROM TFOSMT02A WHERE (DEP_NAME, BREAKDN_DATE) IN (SELECT DEP_NAME, MAX(BREAKDN_DATE) FROM TFOSMT02A WHERE BREAKDN_DATE < '测试值' GROUP BY DEP_NAME) ) C ON A.CODE = C.DEP_NAME LEFT JOIN TFOSMT02B D ON A.CODE = D.DEP_NAME WHERE A.CODE_CLASS = 'FOSMT1' AND A.CODE_DESC_2_CONTENT != ' ' ORDER BY A.CODE_DESC_2_CONTENT;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-306 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosmt00_inq.cpp | 函数: f_fosmt00_inq | 锚点: L350-L356
-- 参数: @DATE_TIME='测试值'
SELECT DATE_TIME, PLAN_CHARGE, PRODUCT_CHARGE FROM TFOSMT03A WHERE FACTORY_DIV = 'A20' AND DATE_TIME > TO_CHAR((TO_DATE('测试值','YYYYMMDD') - 7),'YYYYMMDD') AND DATE_TIME <= '测试值' ORDER BY DATE_TIME;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-307 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosmt00_inq.cpp | 函数: f_fosmt00_inq | 锚点: L396-L410
-- 参数: @DATE_TIME='测试值'
WITH A(LEVEL, TIME) AS (SELECT 1, TO_DATE('测试值','YYYYMMDD') - 6 FROM DUAL WHERE 1 = 1 UNION ALL SELECT LEVEL + 1,TIME + 1 FROM DUAL, A WHERE A.TIME < TO_DATE('测试值','YYYYMMDD')) SELECT TO_CHAR(A.TIME,'YYYYMMDD') DATE_TIME, B1.STOCK_TOTAL_WT STOCK_TOTAL_WT_1, B2.STOCK_TOTAL_WT STOCK_TOTAL_WT_2 FROM A LEFT JOIN TFOSMT03A B1 ON TO_CHAR(A.TIME,'YYYYMMDD') = B1.DATE_TIME AND B1.FACTORY_DIV = 'A10' LEFT JOIN TFOSMT03A B2 ON TO_CHAR(A.TIME,'YYYYMMDD') = B2.DATE_TIME AND B2.FACTORY_DIV = 'A20' WHERE 1 = 1;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-308 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosmt00_inq.cpp | 函数: f_fosmt00_inq | 锚点: L450-L464
-- 参数: @DATE_TIME='测试值'
WITH A(LEVEL, TIME) AS (SELECT 1, TO_DATE('测试值','YYYYMMDD') - 6 FROM DUAL WHERE 1 = 1 UNION ALL SELECT LEVEL + 1,TIME + 1 FROM DUAL, A WHERE A.TIME < TO_DATE('测试值','YYYYMMDD')) SELECT TO_CHAR(A.TIME,'YYYYMMDD') DATE_TIME, B1.CC_REMAIN_RATE / 100 CC_REMAIN_RATE_1, B2.CC_REMAIN_RATE / 100 CC_REMAIN_RATE_2 FROM A LEFT JOIN TFOSMT03A B1 ON TO_CHAR(A.TIME,'YYYYMMDD') = B1.DATE_TIME AND B1.FACTORY_DIV = 'A10' LEFT JOIN TFOSMT03A B2 ON TO_CHAR(A.TIME,'YYYYMMDD') = B2.DATE_TIME AND B2.FACTORY_DIV = 'A20' WHERE 1 = 1;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-309 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosmt00_inq.cpp | 函数: f_fosmt00_inq | 锚点: L628-L636
-- 参数: @DATE_TIME='测试值'
SELECT DATE_TIME, IRON_SLAB_RATE IRON_SLAB_RATE FROM TFOSMT03A WHERE 1 = 1 AND DATE_TIME > TO_CHAR((TO_DATE('测试值','YYYYMMDD') - 7),'YYYYMMDD') AND DATE_TIME <= '测试值' AND FACTORY_DIV = 'A10' ORDER BY DATE_TIME;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-310 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosmt00_inq.cpp | 函数: f_fosmt00_inq | 锚点: L668-L676
-- 参数: @DATE_TIME='测试值'
SELECT DATE_TIME, IRON_SLAB_RATE IRON_SLAB_RATE FROM TFOSMT03A WHERE 1 = 1 AND DATE_TIME > TO_CHAR((TO_DATE('测试值','YYYYMMDD') - 7),'YYYYMMDD') AND DATE_TIME <= '测试值' AND FACTORY_DIV = 'A20' ORDER BY DATE_TIME;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-311 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosmt00_inq.cpp | 函数: f_fosmt00_inq | 锚点: L736-L770
-- 参数: @DATE_TIME='测试值'
WITH A(LEVEL, TIME) AS (SELECT 1, TO_DATE('测试值','YYYYMMDD') - 9 FROM DUAL WHERE 1 = 1 UNION ALL SELECT LEVEL + 1,TIME + 1 FROM DUAL, A WHERE A.TIME < TO_DATE('测试值','YYYYMMDD')) SELECT TO_CHAR(A.TIME,'YYYYMMDD') DATE_TIME, B1.IRON_RELEASE_WT IRON_RELEASE_WT_1, B1.SEQ_NO DEDUCT_PT_1, B2.IRON_RELEASE_WT IRON_RELEASE_WT_2, B2.SEQ_NO DEDUCT_PT_2, B3.IRON_RELEASE_WT IRON_RELEASE_WT_3, B3.SEQ_NO DEDUCT_PT_3, B4.IRON_RELEASE_WT IRON_RELEASE_WT_4, B4.SEQ_NO DEDUCT_PT_4, B5.IRON_RELEASE_WT IRON_RELEASE_WT_5, B5.SEQ_NO DEDUCT_PT_5, B6.IRON_RELEASE_WT IRON_RELEASE_WT_6, B6.SEQ_NO DEDUCT_PT_6, B7.IRON_RELEASE_WT IRON_RELEASE_WT_7, B7.SEQ_NO DEDUCT_PT_7, CASE WHEN B1.REMARK IS NULL THEN '' ELSE TRIM(B1.REMARK) END || CASE WHEN B2.REMARK IS NULL THEN '' ELSE TRIM(B2.REMARK) END || CASE WHEN B3.REMARK IS NULL THEN '' ELSE TRIM(B3.REMARK) END || CASE WHEN B4.REMARK IS NULL THEN '' ELSE TRIM(B4.REMARK) END || CASE WHEN B5.REMARK IS NULL THEN '' ELSE TRIM(B5.REMARK) END || CASE WHEN B6.REMARK IS NULL THEN '' ELSE TRIM(B6.REMARK) END || CASE WHEN B7.REMARK IS NULL THEN '' ELSE TRIM(B7.REMARK) END REMARK FROM A LEFT JOIN TFOSMT03B B1 ON TO_CHAR(A.TIME,'YYYYMMDD') = B1.DATE_TIME AND B1.DEP_NAME = '02' LEFT JOIN TFOSMT03B B2 ON TO_CHAR(A.TIME,'YYYYMMDD') = B2.DATE_TIME AND B2.DEP_NAME = '03' LEFT JOIN TFOSMT03B B3 ON TO_CHAR(A.TIME,'YYYYMMDD') = B3.DATE_TIME AND B3.DEP_NAME = '05' LEFT JOIN TFOSMT03B B4 ON TO_CHAR(A.TIME,'YYYYMMDD') = B4.DATE_TIME AND B4.DEP_NAME = '04' LEFT JOIN TFOSMT03B B5 ON TO_CHAR(A.TIME,'YYYYMMDD') = B5.DATE_TIME AND B5.DEP_NAME = '01' LEFT JOIN TFOSMT03B B6 ON TO_CHAR(A.TIME,'YYYYMMDD') = B6.DATE_TIME AND B6.DEP_NAME = '07' LEFT JOIN TFOSMT03B B7 ON TO_CHAR(A.TIME,'YYYYMMDD') = B7.DATE_TIME AND B7.DEP_NAME = '10' WHERE 1 = 1;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-312 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosmt00_inq.cpp | 函数: f_fosmt00_inq | 锚点: L860-L872
-- 参数: @DATE_TIME='测试值'
SELECT A.FACTORY_DIV, A.DATE_TIME, A.SHIFT_NO, A.SHIFT_GROUP, A.PLAN_CHARGE, A.SMELT_CHARGE, A.PRODUCT_CHARGE, B.ADJUST_CHARGE, DECODE(B.START_TIME, ' ', ' ', (TO_CHAR(TO_DATE(B.START_TIME, 'YYYYMMDDHH24MISS'), 'HH24:MI')) || '-' || DECODE(B.START_TIME, ' ', ' ', TO_CHAR(TO_DATE(B.END_TIME, 'YYYYMMDDHH24MISS'), 'HH24:MI'))) PERIOD_TIME, B.REMARK, B.STOP_TOTAL_TIME, B.DEP_NAME FROM TFOSMT04A A LEFT JOIN TFOSMT04B B ON A.FACTORY_DIV = B.FACTORY_DIV AND A.DATE_TIME = B.DATE_TIME AND A.SHIFT_NO = B.SHIFT_NO WHERE A.FACTORY_DIV = 'A10' AND ((A.DATE_TIME = '测试值' AND A.SHIFT_NO = '1') OR A.DATE_TIME = TO_CHAR(TO_DATE('测试值','YYYYMMDD') - 1,'YYYYMMDD') AND A.SHIFT_NO <> '1') ORDER BY A.DATE_TIME, A.SHIFT_NO, B.CHARGE_NO;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-313 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosmt00_inq.cpp | 函数: f_fosmt00_inq | 锚点: L908-L920
-- 参数: @DATE_TIME='测试值'
SELECT A.FACTORY_DIV, A.DATE_TIME, A.SHIFT_NO, A.SHIFT_GROUP, A.PLAN_CHARGE, A.SMELT_CHARGE, A.PRODUCT_CHARGE, B.ADJUST_CHARGE, DECODE(B.START_TIME, ' ', ' ', (TO_CHAR(TO_DATE(B.START_TIME, 'YYYYMMDDHH24MISS'), 'HH24:MI')) || '-' || DECODE(B.START_TIME, ' ', ' ', TO_CHAR(TO_DATE(B.END_TIME, 'YYYYMMDDHH24MISS'), 'HH24:MI'))) PERIOD_TIME, B.REMARK, B.STOP_TOTAL_TIME, B.DEP_NAME FROM TFOSMT04A A LEFT JOIN TFOSMT04B B ON A.FACTORY_DIV = B.FACTORY_DIV AND A.DATE_TIME = B.DATE_TIME AND A.SHIFT_NO = B.SHIFT_NO WHERE A.FACTORY_DIV = 'A20' AND ((A.DATE_TIME = '测试值' AND A.SHIFT_NO = '1') OR A.DATE_TIME = TO_CHAR(TO_DATE('测试值','YYYYMMDD') - 1,'YYYYMMDD') AND A.SHIFT_NO <> '1') ORDER BY A.DATE_TIME, A.SHIFT_NO, B.CHARGE_NO;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-314 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosmt00_inq.cpp | 函数: f_fosmt00_inq | 锚点: L955-L962
-- 参数: @DATE_TIME='测试值'
SELECT * FROM TFOSMT05A WHERE FACTORY_DIV = 'A10' AND DATE_TIME > TO_CHAR(TO_DATE('测试值','YYYYMMDD') - 3,'YYYYMMDD') AND DATE_TIME <= '测试值' ORDER BY DATE_TIME, SEQ_NO;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-315 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosmt00_inq.cpp | 函数: f_fosmt00_inq | 锚点: L993-L1000
-- 参数: @DATE_TIME='测试值'
SELECT * FROM TFOSMT05A WHERE FACTORY_DIV = 'A20' AND DATE_TIME > TO_CHAR(TO_DATE('测试值','YYYYMMDD') - 3,'YYYYMMDD') AND DATE_TIME <= '测试值' ORDER BY DATE_TIME;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-316 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosmt00_inq.cpp | 函数: f_fosmt00_inq | 锚点: L1034-L1042
-- 参数: @DATE_TIME='测试值'
SELECT DATE_TIME, COUNT(HEAT_NO) COUNT_PONO FROM TFOSMT05A WHERE FACTORY_DIV = 'A10' AND DATE_TIME > TO_CHAR(TO_DATE('测试值','YYYYMMDD') - 7,'YYYYMMDD') AND DATE_TIME <= '测试值' GROUP BY DATE_TIME ORDER BY DATE_TIME;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-317 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosmt00_inq.cpp | 函数: f_fosmt00_inq | 锚点: L1074-L1082
-- 参数: @DATE_TIME='测试值'
SELECT DATE_TIME, COUNT(HEAT_NO) COUNT_PONO FROM TFOSMT05A WHERE FACTORY_DIV = 'A20' AND DATE_TIME > TO_CHAR(TO_DATE('测试值','YYYYMMDD') - 7,'YYYYMMDD') AND DATE_TIME <= '测试值' GROUP BY DATE_TIME ORDER BY DATE_TIME;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-318 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosmt00_inq.cpp | 函数: f_fosmt00_inq | 锚点: L1116-L1124
-- 参数: @DATE_TIME='测试值'
SELECT ELM_DESC, COUNT(ELM_DESC) COUNT_PONO FROM TFOSMT05A WHERE FACTORY_DIV = 'A10' AND DATE_TIME > TO_CHAR(TO_DATE('测试值','YYYYMMDD') - 30,'YYYYMMDD') AND DATE_TIME <= '测试值' GROUP BY ELM_DESC ORDER BY ELM_DESC;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-319 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosmt00_inq.cpp | 函数: f_fosmt00_inq | 锚点: L1156-L1164
-- 参数: @DATE_TIME='测试值'
SELECT ELM_DESC, COUNT(ELM_DESC) COUNT_PONO FROM TFOSMT05A WHERE FACTORY_DIV = 'A20' AND DATE_TIME > TO_CHAR(TO_DATE('测试值','YYYYMMDD') - 30,'YYYYMMDD') AND DATE_TIME <= '测试值' GROUP BY ELM_DESC ORDER BY ELM_DESC;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-320 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosmt00_inq.cpp | 函数: f_fosmt00_inq | 锚点: L1196-L1202
-- 参数: @DATE_TIME='测试值'
SELECT DATE_TIME, SHIFT_GROUP, HEAT_NO, OLD_ST_NO, ST_NO, REMARK FROM TFOSMT05B WHERE FACTORY_DIV = 'A10' AND DATE_TIME > TO_CHAR(TO_DATE('测试值','YYYYMMDD') - 3,'YYYYMMDD') AND DATE_TIME <= '测试值';

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-321 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosmt00_inq.cpp | 函数: f_fosmt00_inq | 锚点: L1232-L1238
-- 参数: @DATE_TIME='测试值'
SELECT DATE_TIME, SHIFT_GROUP, HEAT_NO, OLD_ST_NO, ST_NO, REMARK FROM TFOSMT05B WHERE FACTORY_DIV = 'A20' AND DATE_TIME > TO_CHAR(TO_DATE('测试值','YYYYMMDD') - 3,'YYYYMMDD') AND DATE_TIME <= '测试值';

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-322 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosmt00_inq.cpp | 函数: f_fosmt00_inq | 锚点: L1355-L1363
-- 参数: @DATE_TIME='测试值'
SELECT DATE_TIME, CC_MACH_NO, SUM(PRODUCT_CHARGE), SUM(QUALIFIED_CHARGE), ROUND(SUM(PRODUCT_CHARGE) / SUM(QUALIFIED_CHARGE), 4) QUALIFIED_RATE FROM TFOSMT05C WHERE FACTORY_DIV = 'A20' AND DATE_TIME > TO_CHAR(TO_DATE('测试值','YYYYMMDD') - 7,'YYYYMMDD') AND DATE_TIME <= '测试值' GROUP BY DATE_TIME, CC_MACH_NO ORDER BY DATE_TIME, CC_MACH_NO;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-323 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosmt00_inq.cpp | 函数: f_fosmt00_inq | 锚点: L1471-L1524
-- 参数: @DATE_TIME='测试值'
WITH T AS ( SELECT A.FACTORY_DIV, A.DEP_NAME, A.RATE RATE_TARGET, B1.RATE RATE_1, B2.RATE RATE_2, B3.RATE RATE_3, B4.RATE RATE_4, B5.RATE RATE_5, CAST(ROUND((B1.RATE + B2.RATE + B3.RATE + B4.RATE + B5.RATE) / 5, 3) AS DECIMAL(5,3)) RATE_AVG FROM TFOSMT06B A LEFT JOIN TFOSMT06A B1 ON A.FACTORY_DIV = B1.FACTORY_DIV AND A.DEP_NAME = B1.DEP_NAME AND B1.DATE_TIME = TO_CHAR(TO_DATE('测试值','YYYYMMDD') - 4,'YYYYMMDD') LEFT JOIN TFOSMT06A B2 ON A.FACTORY_DIV = B2.FACTORY_DIV AND A.DEP_NAME = B2.DEP_NAME AND B2.DATE_TIME = TO_CHAR(TO_DATE('测试值','YYYYMMDD') - 3,'YYYYMMDD') LEFT JOIN TFOSMT06A B3 ON A.FACTORY_DIV = B3.FACTORY_DIV AND A.DEP_NAME = B3.DEP_NAME AND B3.DATE_TIME = TO_CHAR(TO_DATE('测试值','YYYYMMDD') - 2,'YYYYMMDD') LEFT JOIN TFOSMT06A B4 ON A.FACTORY_DIV = B4.FACTORY_DIV AND A.DEP_NAME = B4.DEP_NAME AND B4.DATE_TIME = TO_CHAR(TO_DATE('测试值','YYYYMMDD') - 1,'YYYYMMDD') LEFT JOIN TFOSMT06A B5 ON A.FACTORY_DIV = B5.FACTORY_DIV AND A.DEP_NAME = B5.DEP_NAME AND B5.DATE_TIME = TO_CHAR(TO_DATE('测试值','YYYYMMDD') - 0,'YYYYMMDD') ORDER BY FACTORY_DIV, DEP_NAME ) SELECT * FROM T WHERE FACTORY_DIV = 'A10' UNION ALL SELECT FACTORY_DIV, '综合' DEP_NAME, SUM(RATE_TARGET), SUM(RATE_1), SUM(RATE_2), SUM(RATE_3), SUM(RATE_4), SUM(RATE_5), SUM(RATE_AVG) FROM T WHERE FACTORY_DIV = 'A10' GROUP BY FACTORY_DIV UNION ALL SELECT * FROM T WHERE FACTORY_DIV = 'A20' UNION ALL SELECT FACTORY_DIV, '综合' DEP_NAME, SUM(RATE_TARGET), SUM(RATE_1), SUM(RATE_2), SUM(RATE_3), SUM(RATE_4), SUM(RATE_5), SUM(RATE_AVG) FROM T WHERE FACTORY_DIV = 'A20' GROUP BY FACTORY_DIV UNION ALL SELECT '合计', '', AVG(RATE_TARGET), AVG(RATE_1), AVG(RATE_2), AVG(RATE_3), AVG(RATE_4), AVG(RATE_5), AVG(RATE_AVG) FROM ( SELECT FACTORY_DIV, '综合' DEP_NAME, SUM(RATE_TARGET) RATE_TARGET, SUM(RATE_1) RATE_1, SUM(RATE_2) RATE_2, SUM(RATE_3) RATE_3, SUM(RATE_4) RATE_4, SUM(RATE_5) RATE_5, SUM(RATE_AVG) RATE_AVG FROM T WHERE FACTORY_DIV = 'A10' GROUP BY FACTORY_DIV UNION ALL SELECT FACTORY_DIV, '综合' DEP_NAME, SUM(RATE_TARGET), SUM(RATE_1), SUM(RATE_2), SUM(RATE_3), SUM(RATE_4), SUM(RATE_5), SUM(RATE_AVG) FROM T WHERE FACTORY_DIV = 'A20' GROUP BY FACTORY_DIV ) T2 ORDER BY FACTORY_DIV, DEP_NAME;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-324 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosmt00_inq.cpp | 函数: f_fosmt00_inq | 锚点: L1597-L1641
-- 参数: @DATE_TIME='测试值'
WITH A(LEVEL, TIME) AS (SELECT 1, TO_DATE('测试值','YYYYMMDD') - 2 FROM DUAL WHERE 1 = 1 UNION ALL SELECT LEVEL + 1,TIME + 1 FROM DUAL, A WHERE A.TIME < TO_DATE('测试值','YYYYMMDD')), C AS ( SELECT MAT_TYPE, MAT_NAME, FACTORY_DIV, SUM(DEVO_WT) DEVO_WT FROM TFOSMT07A WHERE 1 = 1 AND SUBSTR(DATE_TIME, 1, 6) = SUBSTR('测试值', 1, 6) GROUP BY MAT_TYPE, MAT_NAME, FACTORY_DIV ) SELECT TO_CHAR(A.TIME,'YYYYMMDD') DATE_TIME, B1.DEVO_WT DEVO_WT_1, B2.DEVO_WT DEVO_WT_2, B3.DEVO_WT DEVO_WT_3, B1.DEVO_WT + B2.DEVO_WT+ B3.DEVO_WT DEVO_WT_4, B4.DEVO_WT DEVO_WT_5, B5.DEVO_WT DEVO_WT_6, B4.DEVO_WT + B5.DEVO_WT DEVO_WT_7, B6.DEVO_WT DEVO_WT_8, B7.DEVO_WT DEVO_WT_9, B6.DEVO_WT + B7.DEVO_WT DEVO_WT_10 FROM A LEFT JOIN TFOSMT07A B1 ON TO_CHAR(A.TIME,'YYYYMMDD') = B1.DATE_TIME AND B1.MAT_TYPE = '1' AND B1.MAT_NAME = '渣钢大块' LEFT JOIN TFOSMT07A B2 ON TO_CHAR(A.TIME,'YYYYMMDD') = B2.DATE_TIME AND B2.MAT_TYPE = '1' AND B2.MAT_NAME = '渣钢粒' LEFT JOIN TFOSMT07A B3 ON TO_CHAR(A.TIME,'YYYYMMDD') = B3.DATE_TIME AND B3.MAT_TYPE = '1' AND B3.MAT_NAME = '豆钢' LEFT JOIN TFOSMT07A B4 ON TO_CHAR(A.TIME,'YYYYMMDD') = B4.DATE_TIME AND B4.MAT_TYPE = '2' AND B4.MAT_NAME = '渣铁大块' LEFT JOIN TFOSMT07A B5 ON TO_CHAR(A.TIME,'YYYYMMDD') = B5.DATE_TIME AND B5.MAT_TYPE = '2' AND B5.MAT_NAME = '渣铁300' LEFT JOIN TFOSMT07A B6 ON TO_CHAR(A.TIME,'YYYYMMDD') = B6.DATE_TIME AND B6.MAT_TYPE = '3' AND B6.FACTORY_DIV = 'A10' LEFT JOIN TFOSMT07A B7 ON TO_CHAR(A.TIME,'YYYYMMDD') = B7.DATE_TIME AND B7.MAT_TYPE = '3' AND B7.FACTORY_DIV = 'A20' UNION ALL SELECT '合计', C1.DEVO_WT, C2.DEVO_WT, C3.DEVO_WT, C1.DEVO_WT + C2.DEVO_WT + C3.DEVO_WT, C4.DEVO_WT, C5.DEVO_WT, C4.DEVO_WT + C5.DEVO_WT, C6.DEVO_WT, C7.DEVO_WT, C6.DEVO_WT + C7.DEVO_WT FROM DUAL LEFT JOIN C C1 ON C1.MAT_TYPE = '1' AND C1.MAT_NAME = '渣钢大块' LEFT JOIN C C2 ON C2.MAT_TYPE = '1' AND C2.MAT_NAME = '渣钢粒' LEFT JOIN C C3 ON C3.MAT_TYPE = '1' AND C3.MAT_NAME = '豆钢' LEFT JOIN C C4 ON C4.MAT_TYPE = '2' AND C4.MAT_NAME = '渣铁大块' LEFT JOIN C C5 ON C5.MAT_TYPE = '2' AND C5.MAT_NAME = '渣铁300' LEFT JOIN C C6 ON C6.MAT_TYPE = '3' AND C6.FACTORY_DIV = 'A10' LEFT JOIN C C7 ON C7.MAT_TYPE = '3' AND C7.FACTORY_DIV = 'A20' WHERE 1 = 1 ORDER BY DATE_TIME;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-325 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosmt00_inq.cpp | 函数: f_fosmt00_inq | 锚点: L1718-L1771
-- 参数: @DATE_TIME='测试值'
WITH A(LEVEL, TIME) AS (SELECT 1, TO_DATE('测试值','YYYYMMDD') - 2 FROM DUAL WHERE 1 = 1 UNION ALL SELECT LEVEL + 1,TIME + 1 FROM DUAL, A WHERE A.TIME < TO_DATE('测试值','YYYYMMDD')), C AS ( SELECT MAT_TYPE, MAT_NAME, FACTORY_DIV, SUM(DEVO_WT) DEVO_WT FROM TFOSMT07A WHERE 1 = 1 AND SUBSTR(DATE_TIME, 1, 6) = SUBSTR('测试值', 1, 6) GROUP BY MAT_TYPE, MAT_NAME, FACTORY_DIV ) SELECT TO_CHAR(A.TIME,'YYYYMMDD') DATE_TIME, B1.DEVO_WT DEVO_WT_1, B2.DEVO_WT DEVO_WT_2, B3.DEVO_WT DEVO_WT_3, B1.DEVO_WT + B2.DEVO_WT+ B3.DEVO_WT DEVO_WT_4, B4.DEVO_WT DEVO_WT_5, B5.DEVO_WT DEVO_WT_6, B6.DEVO_WT DEVO_WT_7, B4.DEVO_WT + B5.DEVO_WT + B6.DEVO_WT DEVO_WT_8, B7.DEVO_WT DEVO_WT_9, B8.DEVO_WT DEVO_WT_10, B7.DEVO_WT + B8.DEVO_WT DEVO_WT_11, B9.DEVO_WT DEVO_WT_12, BA.DEVO_WT DEVO_WT_13, B9.DEVO_WT + BA.DEVO_WT DEVO_WT_14 FROM A LEFT JOIN TFOSMT07A B1 ON TO_CHAR(A.TIME,'YYYYMMDD') = B1.DATE_TIME AND B1.MAT_TYPE = '4' AND B1.MAT_NAME = '渣钢' LEFT JOIN TFOSMT07A B2 ON TO_CHAR(A.TIME,'YYYYMMDD') = B2.DATE_TIME AND B2.MAT_TYPE = '4' AND B2.MAT_NAME = '切割' LEFT JOIN TFOSMT07A B3 ON TO_CHAR(A.TIME,'YYYYMMDD') = B3.DATE_TIME AND B3.MAT_TYPE = '4' AND B3.MAT_NAME = '中包' LEFT JOIN TFOSMT07A B4 ON TO_CHAR(A.TIME,'YYYYMMDD') = B4.DATE_TIME AND B4.MAT_TYPE = '5' AND B4.MAT_NAME = '渣盆' LEFT JOIN TFOSMT07A B5 ON TO_CHAR(A.TIME,'YYYYMMDD') = B5.DATE_TIME AND B5.MAT_TYPE = '5' AND B5.MAT_NAME = '落锤' LEFT JOIN TFOSMT07A B6 ON TO_CHAR(A.TIME,'YYYYMMDD') = B6.DATE_TIME AND B6.MAT_TYPE = '5' AND B6.MAT_NAME = '中包' LEFT JOIN TFOSMT07A B7 ON TO_CHAR(A.TIME,'YYYYMMDD') = B7.DATE_TIME AND B7.MAT_TYPE = '6' AND B7.FACTORY_DIV = 'A10' LEFT JOIN TFOSMT07A B8 ON TO_CHAR(A.TIME,'YYYYMMDD') = B8.DATE_TIME AND B8.MAT_TYPE = '6' AND B8.FACTORY_DIV = 'A20' LEFT JOIN TFOSMT07A B9 ON TO_CHAR(A.TIME,'YYYYMMDD') = B9.DATE_TIME AND B9.MAT_TYPE = '7' AND B9.FACTORY_DIV = 'A10' LEFT JOIN TFOSMT07A BA ON TO_CHAR(A.TIME,'YYYYMMDD') = BA.DATE_TIME AND BA.MAT_TYPE = '7' AND BA.FACTORY_DIV = 'A20' UNION ALL SELECT '合计', C1.DEVO_WT, C2.DEVO_WT, C3.DEVO_WT, C1.DEVO_WT + C2.DEVO_WT + C3.DEVO_WT, C4.DEVO_WT, C5.DEVO_WT, C6.DEVO_WT, C4.DEVO_WT + C5.DEVO_WT + C6.DEVO_WT, C7.DEVO_WT, C8.DEVO_WT, C7.DEVO_WT + C8.DEVO_WT, C9.DEVO_WT, CA.DEVO_WT, C9.DEVO_WT + CA.DEVO_WT FROM DUAL LEFT JOIN C C1 ON C1.MAT_TYPE = '4' AND C1.MAT_NAME = '渣钢' LEFT JOIN C C2 ON C2.MAT_TYPE = '4' AND C2.MAT_NAME = '切割' LEFT JOIN C C3 ON C3.MAT_TYPE = '4' AND C3.MAT_NAME = '中包' LEFT JOIN C C4 ON C4.MAT_TYPE = '5' AND C4.MAT_NAME = '渣盆' LEFT JOIN C C5 ON C5.MAT_TYPE = '5' AND C5.MAT_NAME = '落锤' LEFT JOIN C C6 ON C6.MAT_TYPE = '5' AND C6.MAT_NAME = '中包' LEFT JOIN C C7 ON C7.MAT_TYPE = '6' AND C7.FACTORY_DIV = 'A10' LEFT JOIN C C8 ON C8.MAT_TYPE = '6' AND C8.FACTORY_DIV = 'A20' LEFT JOIN C C9 ON C9.MAT_TYPE = '7' AND C9.FACTORY_DIV = 'A10' LEFT JOIN C CA ON CA.MAT_TYPE = '7' AND CA.FACTORY_DIV = 'A20' WHERE 1 = 1 ORDER BY DATE_TIME;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-326 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosmt00_inq.cpp | 函数: f_fosmt00_inq | 锚点: L1840-L1850
-- 参数: @DATE_TIME='测试值'
SELECT A1.ENERGY_CODE, A1.ENERGY_CNAME, A1.UNIT, A1.PRICE, A1.VALUE_REAL, A1.VALUE_TARGET, B1.VALUE_DAY VALUE_DAY_1, B2.VALUE_DAY VALUE_DAY_2, B3.VALUE_DAY VALUE_DAY_3, B4.VALUE_DAY VALUE_MONTH FROM TFOSMT09B A1 LEFT JOIN TFOSMT09A B1 ON A1.ENERGY_CODE = B1.ENERGY_CODE AND B1.DATE_TIME = TO_CHAR((TO_DATE('测试值','YYYYMMDD') - 2),'YYYYMMDD') LEFT JOIN TFOSMT09A B2 ON A1.ENERGY_CODE = B2.ENERGY_CODE AND B2.DATE_TIME = TO_CHAR((TO_DATE('测试值','YYYYMMDD') - 1),'YYYYMMDD') LEFT JOIN TFOSMT09A B3 ON A1.ENERGY_CODE = B3.ENERGY_CODE AND B3.DATE_TIME = '测试值' LEFT JOIN (SELECT ENERGY_CODE, SUM(VALUE_DAY) VALUE_DAY FROM TFOSMT09A WHERE SUBSTR(DATE_TIME,1,6) = SUBSTR('测试值',1,6) GROUP BY ENERGY_CODE) B4 ON A1.ENERGY_CODE = B4.ENERGY_CODE WHERE 1 = 1;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-327 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosmt00_inq.cpp | 函数: f_fosmt00_inq | 锚点: L1941-L1948
-- 参数: @DATE_TIME='测试值'
SELECT A.DATE_TIME, A.IRON_S VALUE FROM TFOSMT10I A WHERE 1 = 1 AND DATE_TIME > TO_CHAR((TO_DATE('测试值','YYYYMMDD') - 7),'YYYYMMDD') AND DATE_TIME <= '测试值' AND STATION_NO = '2';

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-328 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosmt00_inq.cpp | 函数: f_fosmt00_inq | 锚点: L1979-L1986
-- 参数: @DATE_TIME='测试值'
SELECT A.DATE_TIME, A.IRON_S VALUE FROM TFOSMT10I A WHERE 1 = 1 AND DATE_TIME > TO_CHAR((TO_DATE('测试值','YYYYMMDD') - 7),'YYYYMMDD') AND DATE_TIME <= '测试值' AND STATION_NO = '4';

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-329 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosmt00_inq.cpp | 函数: f_fosmt00_inq | 锚点: L2017-L2024
-- 参数: @DATE_TIME='测试值'
SELECT A.DATE_TIME, A.IRON_S VALUE FROM TFOSMT10I A WHERE 1 = 1 AND DATE_TIME > TO_CHAR((TO_DATE('测试值','YYYYMMDD') - 7),'YYYYMMDD') AND DATE_TIME <= '测试值' AND STATION_NO = '5';

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-330 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosmt00_inq.cpp | 函数: f_fosmt00_inq | 锚点: L2181-L2189
-- 参数: @DATE_TIME='测试值'
SELECT A.DATE_TIME, A.ADJUST_CHARGE ADJUST_CHARGE_1, A.MOLTIRON_WT MOLTIRON_WT_1, A.REMARK REMARK_1, B.ADJUST_CHARGE ADJUST_CHARGE_2, B.MOLTIRON_WT MOLTIRON_WT_2, B.REMARK REMARK_2, A.ADJUST_CHARGE + B.ADJUST_CHARGE MOLTIRON_WT_TOTAL FROM TFOSMT10D A LEFT JOIN TFOSMT10D B ON A.DATE_TIME = B.DATE_TIME AND B.FACTORY_DIV = 'A20' WHERE A.FACTORY_DIV = 'A10' AND A.DATE_TIME > TO_CHAR((TO_DATE('测试值','YYYYMMDD') - 10),'YYYYMMDD') AND A.DATE_TIME <= '测试值';

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-331 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosmt00_inq.cpp | 函数: f_fosmt00_inq | 锚点: L2251-L2272
-- 参数: @DATE_TIME='测试值'
WITH A(LEVEL, TIME) AS (SELECT 1, TO_DATE('测试值','YYYYMMDD') - 9 FROM DUAL WHERE 1 = 1 UNION ALL SELECT LEVEL + 1,TIME + 1 FROM DUAL, A WHERE A.TIME < TO_DATE('测试值','YYYYMMDD')) SELECT TO_CHAR(A.TIME,'YYYYMMDD') DATE_TIME, B1.RATE RATE_1, B2.RATE RATE_2, B3.RATE RATE_3, B4.RATE RATE_4, B5.RATE RATE_5, B6.RATE RATE_6, B7.RATE RATE_7, B8.RATE RATE_8, B1.RATE + B5.RATE RATE_9, B2.RATE + B6.RATE RATE_10, B3.RATE + B7.RATE RATE_11, B4.RATE + B8.RATE RATE_12 FROM A LEFT JOIN TFOSMT10E B1 ON TO_CHAR(A.TIME,'YYYYMMDD') = B1.DATE_TIME AND B1.FACTORY_DIV = 'A10' AND B1.MAT_NAME = '硅铁单耗' LEFT JOIN TFOSMT10E B2 ON TO_CHAR(A.TIME,'YYYYMMDD') = B2.DATE_TIME AND B2.FACTORY_DIV = 'A10' AND B2.MAT_NAME = '石墨单耗' LEFT JOIN TFOSMT10E B3 ON TO_CHAR(A.TIME,'YYYYMMDD') = B3.DATE_TIME AND B3.FACTORY_DIV = 'A10' AND B3.MAT_NAME = '发热球单耗' LEFT JOIN TFOSMT10E B4 ON TO_CHAR(A.TIME,'YYYYMMDD') = B4.DATE_TIME AND B4.FACTORY_DIV = 'A10' AND B4.MAT_NAME = '折合石墨单耗' LEFT JOIN TFOSMT10E B5 ON TO_CHAR(A.TIME,'YYYYMMDD') = B5.DATE_TIME AND B5.FACTORY_DIV = 'A20' AND B5.MAT_NAME = '硅铁单耗' LEFT JOIN TFOSMT10E B6 ON TO_CHAR(A.TIME,'YYYYMMDD') = B6.DATE_TIME AND B6.FACTORY_DIV = 'A20' AND B6.MAT_NAME = '石墨单耗' LEFT JOIN TFOSMT10E B7 ON TO_CHAR(A.TIME,'YYYYMMDD') = B7.DATE_TIME AND B7.FACTORY_DIV = 'A20' AND B7.MAT_NAME = '发热球单耗' LEFT JOIN TFOSMT10E B8 ON TO_CHAR(A.TIME,'YYYYMMDD') = B8.DATE_TIME AND B8.FACTORY_DIV = 'A20' AND B8.MAT_NAME = '折合石墨单耗';

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-332 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosmt00_inq.cpp | 函数: f_fosmt00_inq | 锚点: L2339-L2359
-- 参数: @DATE_TIME='测试值'
WITH A(LEVEL, TIME) AS (SELECT 1, TO_DATE('测试值','YYYYMMDD') - 9 FROM DUAL WHERE 1 = 1 UNION ALL SELECT LEVEL + 1,TIME + 1 FROM DUAL, A WHERE A.TIME < TO_DATE('测试值','YYYYMMDD')) SELECT TO_CHAR(A.TIME,'YYYYMMDD') DATE_TIME, B1.PRODUCT_CHARGE + B2.PRODUCT_CHARGE PRODUCT_CHARGE_1, B1.SMELT_CHARGE SMELT_CHARGE_L1, B1.RATE RATE_L1, B1.TOTAL_DURATION TOTAL_DURATION_L1, B2.SMELT_CHARGE SMELT_CHARGE_R1, B2.RATE RATE_R1, B3.PRODUCT_CHARGE + B4.PRODUCT_CHARGE PRODUCT_CHARGE_2, B3.SMELT_CHARGE SMELT_CHARGE_L2, B3.RATE RATE_L2, B3.TOTAL_DURATION TOTAL_DURATION_L2, B4.SMELT_CHARGE SMELT_CHARGE_R2, B4.RATE RATE_R2 FROM A LEFT JOIN TFOSMT10F B1 ON TO_CHAR(A.TIME,'YYYYMMDD') = B1.DATE_TIME AND B1.FACTORY_DIV = 'A10' AND B1.STATION_ID = 'L' LEFT JOIN TFOSMT10F B2 ON TO_CHAR(A.TIME,'YYYYMMDD') = B2.DATE_TIME AND B2.FACTORY_DIV = 'A10' AND B2.STATION_ID = 'L' LEFT JOIN TFOSMT10F B3 ON TO_CHAR(A.TIME,'YYYYMMDD') = B3.DATE_TIME AND B3.FACTORY_DIV = 'A20' AND B3.STATION_ID = 'R' LEFT JOIN TFOSMT10F B4 ON TO_CHAR(A.TIME,'YYYYMMDD') = B4.DATE_TIME AND B4.FACTORY_DIV = 'A20' AND B4.STATION_ID = 'R';

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-333 | module: FOSMT
-- 来源: Server/FOSMT/p_fosmt_28180/fosmt00_inq.cpp | 函数: f_fosmt00_inq | 锚点: L2511-L2540
-- 参数: @DATE_TIME='测试值'
SELECT A.CODE, A.CODE_DESC_2_CONTENT, 'A10' FACTORY_DIV, A.CODE_DESC_1_CONTENT STATION_NAME, B1.STATION_NO STATION_NO_1, B2.STATION_NO STATION_NO_2, B3.STATION_NO STATION_NO_3, B4.STATION_NO STATION_NO_4, B5.STATION_NO STATION_NO_5, B6.STATION_NO STATION_NO_6, B7.STATION_NO STATION_NO_7, B1.START_TIME || '-' || B1.END_TIME PERIOD_TIME, B1.REMARK FROM TEP0002 A LEFT JOIN TFOSMT11A B1 ON A.CODE = B1.STATION_ID AND B1.FACTORY_DIV = 'A10' AND B1.DATE_TIME = '测试值' LEFT JOIN TFOSMT11A B2 ON A.CODE = B2.STATION_ID AND B2.FACTORY_DIV = 'A10' AND B2.DATE_TIME = TO_CHAR((TO_DATE('测试值','YYYYMMDD') + 1),'YYYYMMDD') LEFT JOIN TFOSMT11A B3 ON A.CODE = B3.STATION_ID AND B3.FACTORY_DIV = 'A10' AND B3.DATE_TIME = TO_CHAR((TO_DATE('测试值','YYYYMMDD') + 2),'YYYYMMDD') LEFT JOIN TFOSMT11A B4 ON A.CODE = B4.STATION_ID AND B4.FACTORY_DIV = 'A10' AND B4.DATE_TIME = TO_CHAR((TO_DATE('测试值','YYYYMMDD') + 3),'YYYYMMDD') LEFT JOIN TFOSMT11A B5 ON A.CODE = B5.STATION_ID AND B5.FACTORY_DIV = 'A10' AND B5.DATE_TIME = TO_CHAR((TO_DATE('测试值','YYYYMMDD') + 4),'YYYYMMDD') LEFT JOIN TFOSMT11A B6 ON A.CODE = B6.STATION_ID AND B6.FACTORY_DIV = 'A10' AND B6.DATE_TIME = TO_CHAR((TO_DATE('测试值','YYYYMMDD') + 5),'YYYYMMDD') LEFT JOIN TFOSMT11A B7 ON A.CODE = B7.STATION_ID AND B7.FACTORY_DIV = 'A10' AND B7.DATE_TIME = TO_CHAR((TO_DATE('测试值','YYYYMMDD') + 6),'YYYYMMDD') WHERE A.CODE_CLASS = 'FOSMT2' UNION ALL SELECT A.CODE, A.CODE_DESC_2_CONTENT, 'A20' FACTORY_DIV, A.CODE_DESC_1_CONTENT STATION_NAME, B1.STATION_NO STATION_NO_1, B2.STATION_NO STATION_NO_2, B3.STATION_NO STATION_NO_3, B4.STATION_NO STATION_NO_4, B5.STATION_NO STATION_NO_5, B6.STATION_NO STATION_NO_6, B7.STATION_NO STATION_NO_7, B1.START_TIME || '-' || B1.END_TIME PERIOD_TIME, B1.REMARK FROM TEP0002 A LEFT JOIN TFOSMT11A B1 ON A.CODE = B1.STATION_ID AND B1.FACTORY_DIV = 'A20' AND B1.DATE_TIME = '测试值' LEFT JOIN TFOSMT11A B2 ON A.CODE = B2.STATION_ID AND B2.FACTORY_DIV = 'A20' AND B2.DATE_TIME = TO_CHAR((TO_DATE('测试值','YYYYMMDD') + 1),'YYYYMMDD') LEFT JOIN TFOSMT11A B3 ON A.CODE = B3.STATION_ID AND B3.FACTORY_DIV = 'A20' AND B3.DATE_TIME = TO_CHAR((TO_DATE('测试值','YYYYMMDD') + 2),'YYYYMMDD') LEFT JOIN TFOSMT11A B4 ON A.CODE = B4.STATION_ID AND B4.FACTORY_DIV = 'A20' AND B4.DATE_TIME = TO_CHAR((TO_DATE('测试值','YYYYMMDD') + 3),'YYYYMMDD') LEFT JOIN TFOSMT11A B5 ON A.CODE = B5.STATION_ID AND B5.FACTORY_DIV = 'A20' AND B5.DATE_TIME = TO_CHAR((TO_DATE('测试值','YYYYMMDD') + 4),'YYYYMMDD') LEFT JOIN TFOSMT11A B6 ON A.CODE = B6.STATION_ID AND B6.FACTORY_DIV = 'A20' AND B6.DATE_TIME = TO_CHAR((TO_DATE('测试值','YYYYMMDD') + 5),'YYYYMMDD') LEFT JOIN TFOSMT11A B7 ON A.CODE = B7.STATION_ID AND B7.FACTORY_DIV = 'A20' AND B7.DATE_TIME = TO_CHAR((TO_DATE('测试值','YYYYMMDD') + 6),'YYYYMMDD') WHERE A.CODE_CLASS = 'FOSMT2' ORDER BY FACTORY_DIV, CODE_DESC_2_CONTENT;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-339 | module: MMSM
-- 来源: Server/MMSM/libMMSM/f_mmsm81.cpp | 函数: file_scope | 锚点: L101
SELECT MMSM_MATNO_SEQ.NEXTVAL FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-151 | module: MMSM
-- 来源: Server/MMSM/libMMSM/f_mmsm7101_proc.cpp | 函数: f_mmsm7101_proc | 锚点: L84-L84
SELECT MAX(SUBSTR(SLAG_PROC_NO, 5, 5)) + 1 FROM TMMSM71 WHERE SUBSTR(SLAG_PROC_NO, 1, 2) = (SELECT substr(to_char(CURRENT_DATE,'yyyy'),3,2) FROM DUAL);

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-152 | module: MMSM
-- 来源: Server/MMSM/libMMSM/f_mmsm7101_proc.cpp | 函数: f_mmsm7101_proc | 锚点: L98-L98
SELECT MAX(SUBSTR(SLAG_PROC_NO, 5, 5)) + 1 FROM TMMSM71 WHERE SUBSTR(SLAG_PROC_NO, 1, 2) = (SELECT substr(to_char(CURRENT_DATE,'yyyy'),3,2) FROM DUAL);

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-153 | module: MMSM
-- 来源: Server/MMSM/libMMSM/f_mmsm80a.cpp | 函数: f_mmsm80a | 锚点: L447-L449
SELECT TO_CHAR(CURRENT_TIMESTAMP, 'YYYYMMDDHH24MISSFF4');

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-154 | module: MMSM
-- 来源: Server/MMSM/libMMSM/f_mmsm_acyfl_seq.cpp | 函数: f_mmsm_acyfl_seq | 锚点: L44-L47
SELECT LPAD(TO_CHAR(MMSM_MATNO_SEQ.NEXTVAL),4,'0');

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-155 | module: MMSM
-- 来源: Server/MMSM/libMMSM/f_mmsm_get_density.cpp | 函数: f_mmsm_get_density | 锚点: L58-L58
select CODE_DESC_1_CONTENT,CASE WHEN trim(CODE_DESC_2_CONTENT) IS NULL OR trim(CODE_DESC_2_CONTENT) = '' THEN 7.85 ELSE trim(CODE_DESC_2_CONTENT) END CODE_DESC_2_CONTENT from TWMSMZD02 where CODE_CLASS='MMSMDENS' ORDER BY CODE;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-156 | module: MMSM
-- 来源: Server/MMSM/libMMSM/f_mmsm_get_seq_no.cpp | 函数: f_mmsm_get_seq_no | 锚点: L68-L70
SELECT LPAD(TO_CHAR(MMSM_MATNO_SEQ.NEXTVAL),6,'0');

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-157 | module: MMSM
-- 来源: Server/MMSM/libMMSM/f_mmsm_get_seq_no.cpp | 函数: f_mmsm_get_seq_no | 锚点: L156-L158
SELECT LPAD(TO_CHAR(MMSM_MATNO_SEQ.NEXTVAL),6,'0');

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-158 | module: MMSM
-- 来源: Server/MMSM/libMMSM/f_mmsm_gyupd.cpp | 函数: f_mmsm_gyupd | 锚点: L148-L158
-- 参数: @rec_creator='测试值', @rec_create_time='测试值', @heat_no='测试值'
insert into tmmsmgy08(REC_CREATOR,REC_CREATE_TIME,sm_plan_nol2,heat_no,l2_proc_no,PROC_NO,dev_code,mat_code,DEVO_TIME,DEVO_WT,HANDLE_DIV) select '测试值','测试值',t1.sm_plan_nol2,t1.heat_no,t1.l2_proc_no,t1.PROC_NO,t1.dev_code,'TS0000',t1.START_TIME,case when nvl((select DES_TREATMENT_NO from tmmsm21 t2 where t2.heat_no= t1.l2_proc_no and rownum=1),' ')=' ' then round(MOLTIRON_WT*RATIO_B* CASE WHEN BACK_C1 > 0 THEN (BACK_C1*0.01) ELSE 1 / HEAT_COUNT END*1000,0) else round(MOLTIRON_WT*RATIO_B*RATIO_KR* CASE WHEN BACK_C1 > 0 THEN (BACK_C1*0.01) ELSE 1 / HEAT_COUNT END*1000,0) end,HANDLE_DIV from ( select sm_plan_nol2,heat_no,l2_proc_no,PROC_NO,dev_code,decode(HEAT_COUNT,0,1,HEAT_COUNT) HEAT_COUNT,TO_NUMBER(TRIM(CASE WHEN trim(BACK_C1) IS NULL THEN 0 ELSE BACK_C1 END)) as BACK_C1,HANDLE_DIV,START_TIME,RATIO_B,RATIO_KR from tmmsmgy06 t1 ,tmmsmw3 t3 where 1=1 and dev_code like 'B%' and heat_no='测试值' ) t1 left join tmmsmgy05 t2 on t1.l2_proc_no=t2.heat_no where nvl(MOLTIRON_WT,0)!=0;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-159 | module: MMSM
-- 来源: Server/MMSM/libMMSM/f_mmsm_gyupd.cpp | 函数: f_mmsm_gyupd | 锚点: L184-L195
-- 参数: @rec_creator='测试值', @rec_create_time='测试值', @heat_no='测试值'
insert into tmmsmgy08(REC_CREATOR,REC_CREATE_TIME,sm_plan_nol2,heat_no,l2_proc_no,PROC_NO,dev_code,mat_code,DEVO_TIME,DEVO_WT,HANDLE_DIV) select '测试值','测试值',t1.sm_plan_nol2,t1.heat_no,t1.l2_proc_no,t1.PROC_NO,t1.dev_code,'TS0000',t1.START_TIME,case when nvl((select DES_TREATMENT_NO from tmmsm21 t2 where t2.heat_no= t1.l2_proc_no and rownum=1),' ')=' ' then round(MOLTIRON_WT*RATIO_B* CASE WHEN BACK_C1 > 0 THEN (BACK_C1*0.01) ELSE 1 / HEAT_COUNT END*1000,0) else round(MOLTIRON_WT*RATIO_B*RATIO_KR* CASE WHEN BACK_C1 > 0 THEN (BACK_C1*0.01) ELSE 1 / HEAT_COUNT END*1000,0) end,HANDLE_DIV from ( select sm_plan_nol2,heat_no,l2_proc_no,PROC_NO,dev_code,decode(HEAT_COUNT,0,1,HEAT_COUNT) HEAT_COUNT,TO_NUMBER(TRIM(CASE WHEN trim(BACK_C1) IS NULL THEN 0 ELSE BACK_C1 END)) as BACK_C1,HANDLE_DIV,START_TIME,RATIO_B,RATIO_KR from tmmsmgy06 t1 ,tmmsmw3 t3 where 1=1 and not exists(select 1 from tmmsmgy05 t4 WHERE t1.l2_proc_no = t4.heat_no) and dev_code like 'B%' and heat_no='测试值' ) t1 left join tmmsm21 t2 on t1.l2_proc_no=t2.l2_proc_no where nvl(MOLTIRON_WT,0)!=0;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-160 | module: MMSM
-- 来源: Server/MMSM/libMMSM/f_mmsm_gyupd.cpp | 函数: f_mmsm_gyupd | 锚点: L244-L255
-- 参数: @rec_creator='测试值', @rec_create_time='测试值', @heat_no='测试值'
insert into tmmsmgy08(REC_CREATOR,REC_CREATE_TIME,sm_plan_nol2,heat_no,l2_proc_no,PROC_NO,dev_code,mat_code,ID_2A,PROC_COUNT,WEIGH_NO,QUALITY_BATCH_NO,LOT_NO,DEVO_TIME,DEVO_WT,HANDLE_DIV,STK_NO,CHARGE_TYPE) select '测试值','测试值',sm_plan_nol2,heat_no,l2_proc_no,PROC_NO,dev_code,mat_code,ID_2A,PROC_COUNT,WEIGH_NO,QUALITY_BATCH_NO,LOT_NO,DEVO_TIME,round(sum(DEVO_WT* CASE WHEN BACK_C1 > 0 THEN (BACK_C1*0.01) ELSE 1 / HEAT_COUNT END),0) DEVO_WT,NVL(trim(HANDLE_DIV),'I'),STK_NO,CHARGE_TYPE from ( select t1.sm_plan_nol2,t1.heat_no,t1.l2_proc_no,t1.proc_no,t1.dev_code,decode(t1.HEAT_COUNT,0,1,t1.HEAT_COUNT) HEAT_COUNT,TO_NUMBER(TRIM(CASE WHEN trim(BACK_C1) IS NULL THEN 0 ELSE BACK_C1 END)) as BACK_C1,t2.mat_code,t2.ID_2A,t2.PROC_COUNT,t2.WEIGH_NO,t2.LOT_NO,t2.QUALITY_BATCH_NO,t2.DEVO_TIME,t2.DEVO_WT,t1.HANDLE_DIV,t2.STK_NO,t2.CHARGE_TYPE from tmmsmgy06 t1 left join tmmsm2a_yl t2 on t1.dev_code = t2.dev_code and t1.l2_proc_no=t2.l2_proc_no where 1=1 and substr(t1.dev_code,1,1) not in ('F','R','S','V') and nvl(DEVO_WT,0)!=0 and t1.heat_no= '测试值') group by sm_plan_nol2,heat_no,l2_proc_no,PROC_NO,dev_code,mat_code,ID_2A,PROC_COUNT,WEIGH_NO,QUALITY_BATCH_NO,LOT_NO,DEVO_TIME,STK_NO,CHARGE_TYPE,NVL(trim(HANDLE_DIV),'I');

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-161 | module: MMSM
-- 来源: Server/MMSM/libMMSM/f_mmsm_gyupd.cpp | 函数: f_mmsm_gyupd | 锚点: L281-L292
-- 参数: @rec_creator='测试值', @rec_create_time='测试值', @heat_no='测试值'
insert into tmmsmgy08(REC_CREATOR,REC_CREATE_TIME,sm_plan_nol2,heat_no,l2_proc_no,PROC_NO,dev_code,mat_code,ID_2A,PROC_COUNT,WEIGH_NO,QUALITY_BATCH_NO,LOT_NO,DEVO_TIME,DEVO_WT,HANDLE_DIV,STK_NO,CHARGE_TYPE) select '测试值','测试值',sm_plan_nol2,heat_no,l2_proc_no,PROC_NO,dev_code,mat_code,ID_2A,PROC_COUNT,WEIGH_NO,QUALITY_BATCH_NO,LOT_NO,DEVO_TIME,round(sum(DEVO_WT* CASE WHEN BACK_C1 > 0 THEN (BACK_C1*0.01) ELSE 1 / HEAT_COUNT END),0) DEVO_WT,NVL(trim(HANDLE_DIV),'I'),STK_NO,CHARGE_TYPE from ( select t1.sm_plan_nol2,t1.heat_no,t1.l2_proc_no,t1.proc_no,t1.dev_code,decode(t1.HEAT_COUNT,0,1,t1.HEAT_COUNT) HEAT_COUNT,TO_NUMBER(TRIM(CASE WHEN trim(BACK_C1) IS NULL THEN 0 ELSE BACK_C1 END)) as BACK_C1,t2.mat_code,t2.ID_2A,t2.PROC_COUNT,t2.WEIGH_NO,t2.QUALITY_BATCH_NO,t2.LOT_NO,t2.DEVO_TIME,t2.DEVO_WT,t1.HANDLE_DIV,t2.STK_NO,t2.CHARGE_TYPE from tmmsmgy06 t1 left join tmmsm2a_yl t2 on substr(t1.dev_code,1,1) = substr(t2.dev_code,1,1) and t1.l2_proc_no=t2.l2_proc_no where 1=1 and substr(t1.dev_code,1,1) in ('F','R','S','V') and nvl(DEVO_WT,0)!=0 and t1.heat_no= '测试值') group by sm_plan_nol2,heat_no,l2_proc_no,PROC_NO,dev_code,mat_code,ID_2A,PROC_COUNT,WEIGH_NO,QUALITY_BATCH_NO,LOT_NO,DEVO_TIME,STK_NO,CHARGE_TYPE,NVL(trim(HANDLE_DIV),'I');

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-162 | module: MMSM
-- 来源: Server/MMSM/libMMSM/f_mmsm_matno_catch_sm.cpp | 函数: f_mmsm_matno_catch_sm | 锚点: L597-L597
-- 参数: @seq='测试值'
SELECT chr(to_number(ABS(ASCII('测试值') - 55))+55+1) FROM DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-362 | module: MMSM
-- 来源: Server/MMSM/p_mmsm_17520/mmsm01g2_inq.cpp | 函数: f_mmsm01g2_inq | 锚点: L135-L136
-- 参数: @m_whole_backlog_code1='测试值', @v_whole_backlog_code1='测试值'
-- 片段(不可单独执行,需拼入宿主语句验证): OR ( A.WHOLE_BACKLOG LIKE '测试值' AND (INSTR(A.WHOLE_BACKLOG, '测试值')-INSTR(A.WHOLE_BACKLOG, '测试值')/2 *2)>0)

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-363 | module: MMSM
-- 来源: Server/MMSM/p_mmsm_17520/mmsm01g2_inq.cpp | 函数: f_mmsm01g2_inq | 锚点: L147-L148
-- 参数: @m_whole_backlog_code2='测试值', @v_whole_backlog_code2='测试值'
-- 片段(不可单独执行,需拼入宿主语句验证): OR ( A.WHOLE_BACKLOG LIKE '测试值' AND (INSTR(A.WHOLE_BACKLOG, '测试值')-INSTR(A.WHOLE_BACKLOG, '测试值')/2 *2)>0)

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-364 | module: MMSM
-- 来源: Server/MMSM/p_mmsm_17520/mmsm01g2_inq.cpp | 函数: f_mmsm01g2_inq | 锚点: L160-L161
-- 参数: @m_whole_backlog_code3='测试值', @v_whole_backlog_code3='测试值'
-- 片段(不可单独执行,需拼入宿主语句验证): OR ( A.WHOLE_BACKLOG LIKE '测试值' AND (INSTR(A.WHOLE_BACKLOG, '测试值')-INSTR(A.WHOLE_BACKLOG, '测试值')/2 *2)>0)

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-365 | module: MMSM
-- 来源: Server/MMSM/p_mmsm_17520/mmsmis02a1_inq.cpp | 函数: f_mmsmis02a1_inq | 锚点: L312-L313
-- 参数: @v_whole_backlog_code1='测试值', @whole_backlog_code1='测试值'
-- 片段(不可单独执行,需拼入宿主语句验证): AND ((a.WHOLE_BACKLOG like '测试值' and (INSTR(a.WHOLE_BACKLOG, '测试值') - INSTR(a.WHOLE_BACKLOG, '测试值')/2 *2) > 0 )

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-366 | module: MMSM
-- 来源: Server/MMSM/p_mmsm_17520/mmsmis02a1_inq.cpp | 函数: f_mmsmis02a1_inq | 锚点: L327-L328
-- 参数: @v_whole_backlog_code2='测试值', @whole_backlog_code2='测试值'
-- 片段(不可单独执行,需拼入宿主语句验证): OR (a.WHOLE_BACKLOG like '测试值' and (INSTR(a.WHOLE_BACKLOG, '测试值') - INSTR(a.WHOLE_BACKLOG, '测试值')/2 *2) > 0 )

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-367 | module: MMSM
-- 来源: Server/MMSM/p_mmsm_17520/mmsmis02a1_inq.cpp | 函数: f_mmsmis02a1_inq | 锚点: L342-L343
-- 参数: @v_whole_backlog_code3='测试值', @whole_backlog_code3='测试值'
-- 片段(不可单独执行,需拼入宿主语句验证): OR (a.WHOLE_BACKLOG like '测试值' and (INSTR(a.WHOLE_BACKLOG, '测试值') - INSTR(a.WHOLE_BACKLOG, '测试值')/2 *2) > 0 )

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-169 | module: MMSM
-- 来源: Server/MMSM/p_mmsm_17550/mmsmcf_inq.cpp | 函数: f_mmsmcf_inq | 锚点: L104-L113
-- 拼接填充: heat_no=测试值, st_sample_no=测试值, heat_no=测试值, st_sample_no=测试值, heat_no=测试值, st_sample_no=测试值, heat_no=测试值, st_sample_no=测试值, heat_no=测试值, st_sample_no=测试值, heat_no=测试值, st_sample_no=测试值, heat_no=测试值, st_sample_no=测试值, heat_no=测试值, st_sample_no=测试值, heat_no=测试值, st_sample_no=测试值, heat_no=测试值, st_sample_no=测试值
select (SELECT nvl(ELM_ACT,0) FROM TQMTS25 WHERE heat_no = '测试值' and elm_code = '012' and st_sample_no = '测试值' ) C, (SELECT nvl(ELM_ACT,0) FROM TQMTS25 WHERE heat_no = '测试值' and elm_code = '028' and st_sample_no = '测试值' ) SI, (SELECT nvl(ELM_ACT,0) FROM TQMTS25 WHERE heat_no = '测试值' and elm_code = '055' and st_sample_no = '测试值' ) MN, (SELECT nvl(ELM_ACT,0) FROM TQMTS25 WHERE heat_no = '测试值' and elm_code = '030' and st_sample_no = '测试值' ) P, (SELECT nvl(ELM_ACT,0) FROM TQMTS25 WHERE heat_no = '测试值' and elm_code = '032' and st_sample_no = '测试值' ) S, (SELECT nvl(ELM_ACT,0) FROM TQMTS25 WHERE heat_no = '测试值' and elm_code = '051' and st_sample_no = '测试值' ) V, (SELECT nvl(ELM_ACT,0) FROM TQMTS25 WHERE heat_no = '测试值' and elm_code = '093' and st_sample_no = '测试值' ) NB, (SELECT nvl(ELM_ACT,0) FROM TQMTS25 WHERE heat_no = '测试值' and elm_code = '211' and st_sample_no = '测试值' ) ALS, (SELECT nvl(ELM_ACT,0) FROM TQMTS25 WHERE heat_no = '测试值' and elm_code = '052' and st_sample_no = '测试值' ) CR, (SELECT nvl(ELM_ACT,0) FROM TQMTS25 WHERE heat_no = '测试值' and elm_code = '058' and st_sample_no = '测试值' ) NI from DUAL;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-170 | module: MMSM
-- 来源: Server/MMSM/p_mmsm_17570/mmsmacshf2_inq.cpp | 函数: f_mmsmacshf2_inq | 锚点: L247-L252
-- 拼接填充: sqlstr_temp=AND 1 = 1, sqlstr_temp=AND 1 = 1
SELECT * FROM ( SELECT CASE WHEN (SELECT PONO FROM TPSSM11 S WHERE S.PONO = T.PONO ) IS NULL and (SELECT PONO FROM TPSSM_PLAN_ST S WHERE S.PONO = T.PONO) IS NULL THEN '8' WHEN T.PONO_SLAB <> ' ' THEN '9' ELSE '3' END AS SLAB_TYPE_OLD,DECODE(substr(TQ01.ORDER_NO,0,1),'A',TQ01.TRNP_MODE_CODE,' ') TRNP_MODE_CODE_1,TQ01.ORDER_THICK,TQ01.PROD_CLASS_DESC, CASE WHEN t2.MAT_NO IS NULL THEN '0' ELSE '1' END need_mend,nvl(t2.MEND_CAUSE, ' ') MEND_CAUSE, T.*,CASE WHEN T.RCV_MAT_FLAG = 'N' THEN ' ' WHEN T.measure_wt = T.receive_weight THEN '1' ELSE '0' END AS avlb_flag1 FROM TMMSM01 T LEFT JOIN TQMOM01 TQ01 ON T.ORDER_NO =TQ01.ORDER_NO LEFT JOIN get_mend_flag t2 ON T.mat_no = t2.MAT_NO WHERE 1 = 1 AND 1 = 1 UNION ALL SELECT CASE WHEN(SELECT PONO FROM TPSSM11 S WHERE S.PONO = T.PONO) IS NULL and(SELECT PONO FROM TPSSM_PLAN_ST S WHERE S.PONO = T.PONO) IS NULL THEN '8' WHEN T.PONO_SLAB <> ' ' THEN '9' ELSE '3' END AS SLAB_TYPE_OLD, DECODE(substr(TQ01.ORDER_NO,0,1),'A',TQ01.TRNP_MODE_CODE,' ') TRNP_MODE_CODE_1,TQ01.ORDER_THICK,TQ01.PROD_CLASS_DESC, CASE WHEN t2.MAT_NO IS NULL THEN '0' ELSE '1' END need_mend,nvl(t2.MEND_CAUSE, ' ') MEND_CAUSE, T.*,CASE WHEN T.RCV_MAT_FLAG = 'N' THEN ' ' WHEN T.measure_wt = T.receive_weight THEN '1' ELSE '0' END AS avlb_flag1 FROM HMMSM01 T LEFT JOIN TQMOM01 TQ01 ON T.ORDER_NO =TQ01.ORDER_NO LEFT JOIN get_mend_flag t2 ON T.mat_no = t2.MAT_NO WHERE 1 = 1 AND 1 = 1 AND USAGE_DECISION <> '3001' ) ORDER BY PROD_TIME DESC;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-183 | module: MMSM
-- 来源: Server/MMSM/p_mmsm_17570/mmsmwt_del.cpp | 函数: f_mmsmwt_del | 锚点: L75-L75
SELECT MMSM_MATNO_SEQ.NEXTVAL FROM TMMSM25;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-184 | module: MMSM
-- 来源: Server/MMSM/p_mmsm_17570/mmsmwt_ins.cpp | 函数: f_mmsmwt_ins | 锚点: L52-L52
SELECT MMSM_MATNO_SEQ.NEXTVAL FROM TMMSM25;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-185 | module: MMSM
-- 来源: Server/MMSM/p_mmsm_17570/mmsmwt_upd.cpp | 函数: f_mmsmwt_upd | 锚点: L58-L58
SELECT MMSM_MATNO_SEQ.NEXTVAL FROM TMMSM25;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-171 | module: MMSM
-- 来源: Server/MMSM/p_mmsm_17580/mmsmxmjl_inq.cpp | 函数: f_mmsmxmjl_inq | 锚点: L95-L103
SELECT E.*,R.GRADE_TYPE, ROUND((((CASE WHEN MEND_AFTER_WEIGHT IS NULL THEN 0 ELSE MEND_AFTER_WEIGHT END * CASE WHEN MEND_RATE IS NULL THEN 0 ELSE MEND_RATE END / 100 * 1000) * (18.3 / DECODE(MEND_AFTER_WEIGHT, 0, NULL, MEND_AFTER_WEIGHT)) / 238 * (10.25 / DECODE(decode(trim(MEND_METAL_RATE1), null, 0, MEND_METAL_RATE1), 0, null, MEND_METAL_RATE1))) * CASE WHEN MEND_AFTER_WEIGHT IS NULL THEN 0 ELSE MEND_AFTER_WEIGHT END), 3) AS MEND_WEIGHT1 FROM (SELECT T.*, Q.CODE_DESC_1_CONTENT AS MEND_METAL_RATE1 FROM TMMSM34 T LEFT JOIN (select * from TWMSMZD02 WHERE CODE_CLASS = 'METALRATE') Q ON T.ST_NO = Q.CODE )E LEFT JOIN DA_GRADE_TYPE R ON E.ST_NO = R.GRADE_ID WHERE 1 = 1;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-172 | module: MMSM
-- 来源: Server/MMSM/p_mmsm_17610/mmsm01a1f2_inq.cpp | 函数: f_mmsm01a1f2_inq | 锚点: L117-L123
-- 拼接填充: tbl= TMMSM01 A
SELECT A.*,DECODE(substr(TQ01.ORDER_NO,0,1),'A',TQ01.TRNP_MODE_CODE,' ') TRNP_MODE_CODE_1,CASE WHEN t2.MAT_NO IS NULL THEN '0' ELSE '1' END need_mend,nvl(t2.MEND_CAUSE,' ')MEND_CAUSE,TQ01.ORDER_THICK,TQ01.PROD_CLASS_DESC,CASE WHEN A.RCV_MAT_FLAG = 'N' THEN ' ' WHEN A.measure_wt = A.receive_weight THEN '1' ELSE '0' END AS avlb_flag1 FROM TMMSM01 A LEFT JOIN TQMOM01 TQ01 ON A.ORDER_NO =TQ01.ORDER_NO LEFT JOIN get_mend_flag t2 ON A.mat_no =t2.MAT_NO WHERE 1 = 1;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-359 | module: MMSM
-- 来源: Server/MMSM/p_mmsm_17640/cm_0rt801_rcv.cpp | 函数: f_cm_0rt801_rcv | 锚点: L899-L899
-- 拼接填充: tmmsm01["ORDER_NO"].ToString()=测试值
select SUBSTR(WHOLE_BACKLOG, INSTR(WHOLE_BACKLOG, '9A') -2, 2) from tqmom03 WHERE ORDER_NO = '测试值';

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-173 | module: MMSM
-- 来源: Server/MMSM/p_mmsm_17650/mmsmdrsj_add.cpp | 函数: f_mmsmdrsj_add | 锚点: L72-L72
-- 拼接填充: v_heat_no=测试值, v_order_no=测试值
SELECT CASE WHEN max(now_row) IS NULL THEN 0 ELSE max(now_row) END FROM TQMTS0RDR where heat_no='测试值'and order_no='测试值';

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-174 | module: MMSM
-- 来源: Server/MMSM/p_mmsm_17660/mmsmcyzjl_inq.cpp | 函数: f_mmsmcyzjl_inq | 锚点: L110-L121
select a.PROD_TIME,a.PROD_SHIFT_GROUP,a.HEAT_NO,a.MAT_NO,a.ST_NO,a.MAT_LEN,a.MAT_WIDTH,a.MAT_THICK,a.MAT_WT, CASE WHEN b.SHIFT_GROUP IS NULL THEN c.shift_group ELSE b.SHIFT_GROUP END LOAD_UP_SHIFT_GROUP,CASE WHEN b.OUT_STOCK_TIME IS NULL THEN c.OUT_STOCK_TIME ELSE b.OUT_STOCK_TIME END LOAD_UP_TIME, CASE WHEN substr(b.OUT_STOCK_TIME,9,4)>='0800' AND substr(b.OUT_STOCK_TIME,9,4)<='2000' THEN '白班' ELSE '夜班' END SHIFT_NO, a.HAND_OVER_GROUP AS OUT_STOCK_SHIFT_GROUP, c.LOAD_END_TIME AS OUT_STOCK_TIME, DECODE(TRAN_END_TIME,' ',TRAN_TIME,TRAN_END_TIME)TRAN_TIME ,B.OPERATOR EMP_NAME, a.LGORT, CASE WHEN b.UNLOAD_CODE IS NULL THEN c.UNLOAD_CODE ELSE b.UNLOAD_CODE END UNLOAD_CODE, CASE WHEN b.TRUCK_NO IS NULL THEN c.TRUCK_NO ELSE b.TRUCK_NO END TRUCK_NO, D.CODE_DESC_1_CONTENT, b.OPERATOR, GUIDE_DEST, STOCK_L2, C.REMARK, a.UNIT_CODE,a.c_div from vmmsm01 a left join vwmsm12 b on a.LOAD_SCHEME_NO = b.LOAD_SCHEME_NO and a.MAT_NO = b.MAT_NO left join twmsm61 c on a.PRACTICE_NO = c.PRACTICE_NO and a.MAT_NO = c.MAT_NO left join twmsmzd02 d on d.CODE = b.TRUCK_NO and d.code_class='WM01' where 1=1 AND A.LOAD_SCHEME_NO!=' ';

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-186 | module: MMSM
-- 来源: Server/MMSM/p_mmsm_17660/mmsmdbdc_inq.cpp | 函数: f_mmsmdbdc_inq | 锚点: L280-L354
-- 拼接填充: sqlstr_temp=AND 1 = 1, sqlstr_temp=AND 1 = 1
SELECT T.SLAB_CUT_TIME,T.PROD_SHIFT_GROUP,T.HEAT_NO,T.BATCH,' ' WL_CODE,' ' WL_DESCRIPTION,T.ST_NO,T.MAT_ACT_LEN,T.MAT_ACT_WIDTH,T.MAT_ACT_THICK,T.RECEIVE_WEIGHT,T.GUIDE_DEST,T.CASTING_PRE_JUDGMENT, T.CASTING_PURPOSE, T.SURF_QUALITY, DECODE(T.RECEIVE_WEIGHT, 0, 'N', 'Y') RECEIVE_STATUS, T.RECV_MAT_TIME, DECODE(T.RECEIVE_WEIGHT, 0, 'N', 'S') SPECIFIC_SEND, DECODE(T.C_STATESIGN, '3', 'S', '1', 'W', 'N') C_STATESIGN, T.USAGE_DECISION, tm34.MEND_SHIFT as PROD_GROUP_TMMSM34, CASE WHEN T.C_DELIVERY_STOCK = '6235' THEN 'C0' WHEN(SUBSTR(T.MAT_NO, 0, 2) = 'A0' OR SUBSTR(T.MAT_NO, 0, 2) = 'A1' OR SUBSTR(T.MAT_NO, 0, 2) = 'A2' OR SUBSTR(T.MAT_NO, 0, 2) = 'A3' OR SUBSTR(T.MAT_NO, 0, 2) = 'A5' OR SUBSTR(T.MAT_NO, 0, 2) = 'A5' OR SUBSTR(T.MAT_NO, 0, 2) = 'A6' OR SUBSTR(T.MAT_NO, 0, 2) = 'B0' OR SUBSTR(T.MAT_NO, 0, 2) = 'B1' OR SUBSTR(T.MAT_NO, 0, 2) = 'B2' OR SUBSTR(T.MAT_NO, 0, 2) = 'B9') AND tm34.mat_no is null AND TM34_1.MAT_NO <>' ' AND TM34_1.MEND_AFTER_WEIGHT <> tm34_1.MEND_BEFORE_WEIGHT THEN 'B0' WHEN T.ARCHIVE_TIME <>' ' AND T.MEND_FLAG in ('0',' ') AND T.C_DIV='1' THEN 'A0' else tm34.MEND_SET end MEND_SET, tm34.MEND_AFTER_WEIGHT MEND_AFTER_WEIGHT, tm34.START_TIME XM_TIME, tm34.MEND_INNER_MODE MEND_INNER_MODE, tm34.MEND_OUTER_MODE MEND_OUTER_MODE, tm34.MEND_CALCULATE_RATE, tm34.MEND_TOTAL_TIME MEND_TOTAL_TIME, CASE WHEN substr(T.TRAN_END_TIME,9,4)>='0800' AND substr(T.TRAN_END_TIME,9,4)<='2000' THEN '白班' WHEN T.TRAN_END_TIME = ' ' THEN ' ' ELSE '夜班' END PROD_SHIFT_NO, T.TRAN_END_TIME, T.HAND_OVER_GROUP JK_SHIFT_GROUP,T.RESP, t.DST_STOCK_CODE, t.mat_act_wt, CASE WHEN TW62.LOAD_CODE_FACTORY IS NULL THEN TWM41.C_SENDDEPT ELSE TW62.LOAD_CODE_FACTORY END RETURNPLANT,CASE WHEN TW62.SHIFT_GROUP IS NULL THEN TWM41.C_GROUP ELSE TW62.SHIFT_GROUP END SHIFTRETURN, CASE WHEN TW62.UNLOAD_END_TIME IS NULL THEN TWM41.T_INSTOCKTIME ELSE TW62.UNLOAD_END_TIME END RETURNDATE, CASE WHEN TW62.BACK1 IS NULL THEN TWM41.C_QULITYTYPE ELSE TW62.BACK1 END RETURNREASON, tm39.RECUT_DATE GQ_RECUT_DATE, tm39.PROD_SHIFT_GROUP GQ_PROD_GROUP, tm39.CUTTING_TYPE GQ_CUTTING_TYPE, case when length2(SLAB_NO)>=20 then to_number(decode(substr(T.slab_no, length(T.slab_no) - 2, 3), ' ', 0,substr(T.slab_no, length(T.slab_no) - 2, 3))) end CAST_DIV_NO, t.DEV_CODE, (SELECT PROD_SHIFT_GROUP FROM TMMSM36 WHERE MAT_NO = T.MAT_NO) PROD_GROUP_SB, t.HOT_SEND_FLAG, t.ZL_REASON_DESC, t.JUDGE_RESULT_1, t.REMARK, CASE WHEN CASE WHEN TWM12.UNLOAD_CODE_AREA IS NULL THEN twm61.UNLOAD_CODE_AREA ELSE TWM12.UNLOAD_CODE_AREA END IS NULL THEN TWM32M.UNLOAD_CODE_AREA ELSE CASE WHEN TWM12.UNLOAD_CODE_AREA IS NULL THEN twm61.UNLOAD_CODE_AREA ELSE TWM12.UNLOAD_CODE_AREA END END UNLOAD_CODE_AREA,DECODE(decode(TWM12.TRUCK_NO, null, twm61.TRUCK_NO, TWM12.TRUCK_NO), NULL, TWM32M.TRUCK_NO, CASE WHEN TWM12.TRUCK_NO IS NULL THEN twm61.TRUCK_NO ELSE TWM12.TRUCK_NO END) TRUCK_NO, t.STOCK_L2, t.ORDER_NO, t.mat_no, (SELECT DELIVY_DATE from tqmom01 where ORDER_NO = T.ORDER_NO) DELIVY_DATE, (SELECT ORDER_THICK from tqmom01 where ORDER_NO = T.ORDER_NO) ORDER_THICK, t.SG_GRADE_1, (SELECT GRADE_TYPE FROM DA_GRADE_TYPE WHERE GRADE_ID = T.ST_NO) GRADE_TYPE, (SELECT SCRAP_TYPE FROM DA_GRADE_TYPE WHERE GRADE_ID = T.ST_NO) SCRAP_TYPE, t.slab_no, tm34.GRINDING_START_TIME, tm34.GRINDING_OUTER_END_TIME, decode(tm34.MEND_BEFORE_UPPER_TEMP, 0, tm34.MEND_AFTER_UPPER_TEMP, tm34.MEND_BEFORE_UPPER_TEMP) MEND_BEFORE_TEMP, decode(tm34.MEND_BEFORE_BOTTOM_TEMP, 0, tm34.MEND_AFTER_BOTTOM_TEMP, MEND_BEFORE_BOTTOM_TEMP) MEND_AFTER_TEMP, t.TRUCK_NO as CHEHAO, T.STOCK_PLACE_NO, T.STOCK_L2 BP_TOCK_L2, TM34.REC_REVISE_TIME REC_REVISE_TIME, ' ' ORDER_NO_DD, DECODE(SUBSTR(T.ST_NO, 0, 1), 1, '不锈钢', '碳钢') ST_NO_TYPE_1, CASE WHEN SUBSTR(T.ST_NO, 0, 2) = '1A' OR SUBSTR(T.ST_NO, 0, 2) = '1D' THEN '镍钢' WHEN SUBSTR(T.ST_NO, 0, 2) = '1M' OR SUBSTR(T.ST_NO, 0, 2) = '1F' THEN '铬钢' WHEN SUBSTR(T.ST_NO, 0, 1) = '1' THEN '不锈钢' else '碳钢' end as ST_NO_TYPE_2, CASE WHEN CASE WHEN TWM12.SHIFT_GROUP IS NULL THEN twm61.SHIFT_GROUP ELSE TWM12.SHIFT_GROUP END IS NULL THEN TWM32M.SHIFT_GROUP ELSE CASE WHEN TWM12.SHIFT_GROUP IS NULL THEN twm61.SHIFT_GROUP ELSE TWM12.SHIFT_GROUP END END ZC_PROD_GROUP,CASE WHEN CASE WHEN TWM12.OUT_STOCK_TIME IS NULL THEN twm61.LOAD_END_TIME ELSE TWM12.OUT_STOCK_TIME END IS NULL THEN TWM32M.LOAD_END_TIME ELSE CASE WHEN TWM12.OUT_STOCK_TIME IS NULL THEN twm61.LOAD_END_TIME ELSE TWM12.OUT_STOCK_TIME END END ZC_TIME, T.C_DELIVERY_STOCK, DECODE(T.LOGISTICS_STATUS, '2', 'W', '3', 'Y', 'N') LOGISTICS_STATUS, DECODE(T.LGORT, '6242', '成品库', '6246', '修磨库') VALUE_TYPE, T.PRODUCT_FLAG,CASE WHEN t2.MAT_NO IS NULL THEN '0' ELSE '1' END need_mend,nvl(t2.OFFLINE_FLAG, ' ') OFFLINE_FLAG,nvl(t2.MEND_CAUSE, ' ') MEND_CAUSE,nvl(t2.OFFLINE_REASON, ' ') OFFLINE_REASON, case when t.C_STATESIGN = '3' and t.C_DELIVERY_STOCK = '6361' THEN '2250' when t.C_STATESIGN = '3' and t.C_DELIVERY_STOCK = '6351' THEN '1549' when t.C_STATESIGN = '3' and t.C_DELIVERY_STOCK = '6391' THEN '4300' when t.C_STATESIGN = '3' and t.C_DELIVERY_STOCK = '6222' THEN '南区' when t.C_STATESIGN = '3' and t.C_DELIVERY_STOCK = '6311' and t.PRODUCT_FLAG = '0' THEN '型材' when t.C_STATESIGN = '3' and t.C_DELIVERY_STOCK = '6311' and t.PRODUCT_FLAG = '1' and t.TRANSFER_FLAG != '1' and DST_STOCK_CODE in('WXK101', 'WXK102', 'WXK103') THEN '储运站' when t.C_STATESIGN = '3' and t.C_DELIVERY_STOCK = '6311' and t.PRODUCT_FLAG = '1' and t.TRANSFER_FLAG != '1' and DST_STOCK_CODE = 'WXK104' THEN '储运站' when t.C_STATESIGN = '3' and t.C_DELIVERY_STOCK = '6311' and t.PRODUCT_FLAG = '1' and t.TRANSFER_FLAG = '1' then '厂外' else '二钢北区' end location, nvl(TEMP.CC_MACH_NO, ' ') AS CC_MACH_NO, nvl(TEMP.SMELTING_TEMP, 0) AS SMELTING_TEMP, nvl(TEMP.MEAS_TEMP_TIME, ' ') AS MEAS_TEMP_TIME FROM(SELECT MAT_NO, SLAB_CUT_TIME, PROD_SHIFT_GROUP, HEAT_NO, BATCH, ST_NO, MAT_ACT_LEN, MAT_ACT_WIDTH, MAT_ACT_THICK, RECEIVE_WEIGHT, GUIDE_DEST, CASTING_PRE_JUDGMENT, CASTING_PURPOSE, SURF_QUALITY, RECV_MAT_TIME, C_STATESIGN, TRANSFER_FLAG,USAGE_DECISION, ARCHIVE_TIME, MEND_FLAG, C_DELIVERY_STOCK, TRAN_END_TIME, PRACTICE_NO, DST_STOCK_CODE, mat_act_wt, slab_no, DEV_CODE,C_ISHOTSEND HOT_SEND_FLAG, ZL_REASON_DESC, JUDGE_RESULT_1, REMARK, UNLOAD_CODE, ORDER_NO, SG_GRADE_1, TRUCK_NO, STOCK_PLACE_NO, STOCK_L2, LOAD_SCHEME_NO, LOGISTICS_STATUS, LGORT, PRODUCT_FLAG, HAND_OVER_GROUP,C_DIV,RESP,PRINT_NO FROM TMMSM01 where 1 = 1 AND 1 = 1 AND MAT_NO NOT IN(select IN_MAT_NO FROM TMMSM35 GROUP BY IN_MAT_NO) UNION ALL SELECT MAT_NO, SLAB_CUT_TIME, PROD_SHIFT_GROUP, HEAT_NO, BATCH, ST_NO, MAT_ACT_LEN, MAT_ACT_WIDTH, MAT_ACT_THICK, RECEIVE_WEIGHT, GUIDE_DEST, CASTING_PRE_JUDGMENT, CASTING_PURPOSE, SURF_QUALITY, RECV_MAT_TIME, C_STATESIGN, TRANSFER_FLAG,USAGE_DECISION, ARCHIVE_TIME, MEND_FLAG, C_DELIVERY_STOCK, TRAN_END_TIME, PRACTICE_NO, DST_STOCK_CODE, mat_act_wt, slab_no, DEV_CODE,C_ISHOTSEND HOT_SEND_FLAG, ZL_REASON_DESC, JUDGE_RESULT_1, REMARK, UNLOAD_CODE, ORDER_NO, SG_GRADE_1, TRUCK_NO, STOCK_PLACE_NO, STOCK_L2, LOAD_SCHEME_NO, LOGISTICS_STATUS, LGORT, PRODUCT_FLAG, HAND_OVER_GROUP,C_DIV,RESP,PRINT_NO FROM HMMSM01 where 1 = 1 AND 1 = 1 AND MAT_NO NOT IN(select IN_MAT_NO FROM TMMSM35 GROUP BY IN_MAT_NO) ) T LEFT JOIN(SELECT PROD_SHIFT_GROUP, MEND_SHIFT,MEND_SET, MEND_AFTER_WEIGHT, START_TIME, MEND_INNER_MODE, MEND_OUTER_MODE, MEND_CALCULATE_RATE, MEND_TOTAL_TIME, GRINDING_START_TIME, GRINDING_OUTER_END_TIME, MEND_BEFORE_UPPER_TEMP, MEND_AFTER_UPPER_TEMP, MEND_BEFORE_BOTTOM_TEMP, MEND_AFTER_BOTTOM_TEMP, REC_REVISE_TIME, mat_no FROM( SELECT ROW_NUMBER() over(PARTITION BY MAT_NO ORDER BY REC_CREATE_TIME DESC) TM34_MAX, PROD_SHIFT_GROUP,MEND_SHIFT, MEND_SET, MEND_AFTER_WEIGHT, START_TIME, MEND_INNER_MODE, MEND_OUTER_MODE, MEND_CALCULATE_RATE, MEND_TOTAL_TIME, GRINDING_START_TIME, GRINDING_OUTER_END_TIME, MEND_BEFORE_UPPER_TEMP, MEND_AFTER_UPPER_TEMP, MEND_BEFORE_BOTTOM_TEMP, MEND_AFTER_BOTTOM_TEMP, REC_REVISE_TIME, mat_no FROM TMMSM34) WHERE TM34_MAX = 1) tm34 on t.mat_no = tm34.MAT_NO LEFT JOIN(select RECUT_DATE, PROD_SHIFT_GROUP, CUTTING_TYPE, MAT_no from(SELECT ROW_NUMBER() over(PARTITION BY MAT_NO ORDER BY RESUME_SEQ_NO DESC) TM39max, RECUT_DATE, PROD_SHIFT_GROUP, CUTTING_TYPE, MAT_NO from tmmsm39) where TM39max = '1') TM39 ON t.mat_no = tm39.mat_no LEFT JOIN(select LOAD_CODE_FACTORY, SHIFT_GROUP, MAT_NO, UNLOAD_END_TIME, RETURNREASON, BACK1 from(SELECT ROW_NUMBER() over(PARTITION BY MAT_NO ORDER BY REC_CREATE_TIME DESC) tw62_max, LOAD_CODE_FACTORY, mat_no, SHIFT_GROUP, UNLOAD_END_TIME, RETURNREASON,BACK1 from(select LOAD_CODE_FACTORY,mat_no,SHIFT_GROUP,UNLOAD_END_TIME,RETURNREASON,BACK1, REC_CREATE_TIME from twmsm62 union select UNLOAD_CODE_FACTORY LOAD_CODE_FACTORY, mat_no,BACK3 SHIFT_GROUP,UNLOAD_END_TIME,UNLOAD_CODE_FACTORY || BACK2 RETURNREASON,BACK1, REC_CREATE_TIME from twmsm13))where tw62_max = '1') TW62 ON T.MAT_NO = TW62.MAT_NO LEFT JOIN(SELECT MAT_NO, MEND_BEFORE_WEIGHT, MEND_AFTER_WEIGHT FROM(SELECT ROW_NUMBER() over(PARTITION BY MAT_NO ORDER BY REC_CREATE_TIME DESC) TM34_1MAX, MAT_NO, MEND_BEFORE_WEIGHT, MEND_AFTER_WEIGHT FROM TMMSM34_1) WHERE TM34_1MAX = '1') tm34_1 on t.mat_no = tm34_1.MAT_NO LEFT JOIN (SELECT OUT_STOCK_TIME,UNLOAD_CODE_AREA,TRUCK_NO,SHIFT_GROUP,LOAD_SCHEME_NO,MAT_NO FROM vWMSM12) TWM12 ON T.MAT_NO = TWM12.MAT_NO AND TWM12.LOAD_SCHEME_NO = T.LOAD_SCHEME_NO LEFT JOIN(SELECT UNLOAD_CODE_AREA, TRUCK_NO, SHIFT_GROUP, LOAD_END_TIME, PRACTICE_NO, MAT_NO FROM twmsm61) TWM61 ON T.MAT_NO = TWM61.MAT_NO AND TWM61.PRACTICE_NO = T.PRACTICE_NO LEFT JOIN(SELECT MAT_NO, TRUCK_NO, UNLOAD_CODE_AREA, SHIFT_GROUP, LOAD_END_TIME FROM(select ROW_NUMBER() over(PARTITION BY MAT_NO ORDER BY TWM32M.REC_CREATE_TIME DESC) TW32M_1MAX, TWM32M.MAT_NO, TWM32.TRUCK_NO, '6381' UNLOAD_CODE_AREA, twm32m.REMARK1 SHIFT_GROUP, TWM32M.REC_CREATE_TIME LOAD_END_TIME from(SELECT MAT_NO, REMARK1, REC_CREATE_TIME, PLAN_NO, MISSION_NO FROM TWMSM32M) TWM32M LEFT JOIN (SELECT TRUCK_NO,PLAN_NO,MISSION_NO FROM TWMSM32) TWM32 ON TWM32M.PLAN_NO = TWM32.PLAN_NO AND TWM32M.MISSION_NO = TWM32.MISSION_NO WHERE TWM32M.MAT_NO != ' ') WHERE TW32M_1MAX = '1') TWM32M ON T.MAT_NO = TWM32M.MAT_NO LEFT JOIN (select MAT_NO,OFFLINE_FLAG,MEND_CAUSE,OFFLINE_REASON from get_offline_flag) t2 ON t.mat_no = t2.MAT_NO LEFT JOIN (SELECT C_BATCHUNIT, I_RESERVECOL4, C_STATESIGN, C_SENDDEPT, C_GROUP, T_INSTOCKTIME, C_QULITYTYPE FROM(SELECT ROW_NUMBER() over(PARTITION BY C_BATCHUNIT ORDER BY REC_CREATE_TIME DESC) TW41_1MAX, C_BATCHUNIT,I_RESERVECOL4,C_STATESIGN,C_SENDDEPT,C_GROUP,T_INSTOCKTIME,C_QULITYTYPE FROM TWM41DJ WHERE I_RESERVECOL4 = '1' AND C_STATESIGN = '2') WHERE TW41_1MAX = '1') TWM41 ON T.MAT_NO = TWM41.C_BATCHUNIT LEFT JOIN (SELECT CC_MACH_NO,PRINT_NO,SMELTING_TEMP,MEAS_TEMP_TIME FROM TMMSM31_TEMP )TEMP ON T.PRINT_NO = TEMP.PRINT_NO;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-176 | module: MMSM
-- 来源: Server/MMSM/p_mmsm_17660/mmsmhsljl_inq.cpp | 函数: f_mmsmhsljl_inq | 锚点: L89-L98
SELECT E.*,R.GRADE_TYPE,R.grade_name,W.DEV_CODE, ROUND((((CASE WHEN e.MEND_AFTER_WEIGHT IS NULL THEN 0 ELSE e.MEND_AFTER_WEIGHT END * CASE WHEN MEND_RATE IS NULL THEN 0 ELSE MEND_RATE END / 100 * 1000) * (18.3 / DECODE(e.MEND_AFTER_WEIGHT, 0, NULL, e.MEND_AFTER_WEIGHT)) / 238 * (10.25 / DECODE(decode(trim(MEND_METAL_RATE1), null, 0, MEND_METAL_RATE1), 0, null, MEND_METAL_RATE1))) * CASE WHEN e.MEND_AFTER_WEIGHT IS NULL THEN 0 ELSE e.MEND_AFTER_WEIGHT END), 3) AS MEND_WEIGHT1 FROM (SELECT T.*, Q.CODE_DESC_1_CONTENT AS MEND_METAL_RATE1 FROM TMMSM34 T LEFT JOIN(select * from TWMSMZD02 WHERE CODE_CLASS = 'METALRATE') Q ON T.ST_NO = Q.CODE)E LEFT JOIN DA_GRADE_TYPE R ON E.ST_NO = R.GRADE_ID LEFT JOIN TMMSM01 W ON E.MAT_NO = W.MAT_NO WHERE 1 = 1;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-177 | module: MMSM
-- 来源: Server/MMSM/p_mmsm_17660/mmsmlcbgx_inq.cpp | 函数: f_mmsmlcbgx_inq | 锚点: L132-L132
-- 参数: @v_from='测试值'
-- 片段(不可单独执行,需拼入宿主语句验证): AND to_char(to_date(CASE WHEN trim(AOD_BOF_E_DTIME) IS NULL THEN '1999-01-01 00:01:01' ELSE AOD_BOF_E_DTIME END,'yyyy-mm-dd hh24:mi:ss'),'yyyyMMddhhmiss')>= '测试值'

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-178 | module: MMSM
-- 来源: Server/MMSM/p_mmsm_17660/mmsmlcbgx_inq.cpp | 函数: f_mmsmlcbgx_inq | 锚点: L142-L142
-- 参数: @v_to='测试值'
-- 片段(不可单独执行,需拼入宿主语句验证): AND to_char(to_date(CASE WHEN trim(AOD_BOF_E_DTIME) IS NULL THEN '1999-01-01 00:01:01' ELSE AOD_BOF_E_DTIME END,'yyyy-mm-dd hh24:mi:ss'),'yyyyMMddhhmiss')<= '测试值'

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-179 | module: MMSM
-- 来源: Server/MMSM/p_mmsm_17660/mmsmlcbqx_inq.cpp | 函数: f_mmsmlcbqx_inq | 锚点: L133-L133
-- 参数: @v_from='测试值'
-- 片段(不可单独执行,需拼入宿主语句验证): AND to_char(to_date(CASE WHEN trim(AOD_BOF_E_DTIME) IS NULL THEN '1999-01-01 00:01:01' ELSE AOD_BOF_E_DTIME END,'yyyy-mm-dd hh24:mi:ss'),'yyyyMMddhhmiss')>= '测试值'

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-180 | module: MMSM
-- 来源: Server/MMSM/p_mmsm_17660/mmsmlcbqx_inq.cpp | 函数: f_mmsmlcbqx_inq | 锚点: L143-L143
-- 参数: @v_to='测试值'
-- 片段(不可单独执行,需拼入宿主语句验证): AND to_char(to_date(CASE WHEN trim(AOD_BOF_E_DTIME) IS NULL THEN '1999-01-01 00:01:01' ELSE AOD_BOF_E_DTIME END,'yyyy-mm-dd hh24:mi:ss'),'yyyyMMddhhmiss')<= '测试值'

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-181 | module: MMSM
-- 来源: Server/MMSM/p_mmsm_17660/mmsmqxdc_inq.cpp | 函数: f_mmsmqxdc_inq | 锚点: L159-L198
-- 拼接填充: sqlstr_temp=AND 1 = 1
SELECT T.SLAB_CUT_TIME,T.PROD_SHIFT_GROUP,T.HEAT_NO,T.BATCH,' ' WL_CODE,' ' WL_DESCRIPTION,T.ST_NO,T.MAT_ACT_LEN,T.MAT_ACT_WIDTH,T.MAT_ACT_THICK,T.RECEIVE_WEIGHT,T.GUIDE_DEST,T.CASTING_PRE_JUDGMENT, T.CASTING_PURPOSE, T.SURF_QUALITY, DECODE(T.RECEIVE_WEIGHT, 0, 'N', 'Y') RECEIVE_STATUS, T.RECV_MAT_TIME, DECODE(T.RECEIVE_WEIGHT, 0, 'N', 'S') SPECIFIC_SEND, DECODE(T.C_STATESIGN, '3', 'S', '1', 'W', 'N') C_STATESIGN, T.USAGE_DECISION, tm34.MEND_SHIFT as PROD_GROUP_TMMSM34, CASE WHEN T.C_DELIVERY_STOCK = '6235' THEN 'C0' WHEN(SUBSTR(T.MAT_NO, 0, 2) = 'A0' OR SUBSTR(T.MAT_NO, 0, 2) = 'A1' OR SUBSTR(T.MAT_NO, 0, 2) = 'A2' OR SUBSTR(T.MAT_NO, 0, 2) = 'A3' OR SUBSTR(T.MAT_NO, 0, 2) = 'A5' OR SUBSTR(T.MAT_NO, 0, 2) = 'A5' OR SUBSTR(T.MAT_NO, 0, 2) = 'A6' OR SUBSTR(T.MAT_NO, 0, 2) = 'B0' OR SUBSTR(T.MAT_NO, 0, 2) = 'B1' OR SUBSTR(T.MAT_NO, 0, 2) = 'B2' OR SUBSTR(T.MAT_NO, 0, 2) = 'B9') AND tm34.mat_no is null AND TM34_1.MAT_NO <>' ' AND TM34_1.MEND_AFTER_WEIGHT <> tm34_1.MEND_BEFORE_WEIGHT THEN 'B0' WHEN T.ARCHIVE_TIME <>' ' AND T.MEND_FLAG = '0' AND T.C_DIV='1' THEN 'A0' else tm34.MEND_SET end MEND_SET, tm34.MEND_AFTER_WEIGHT MEND_AFTER_WEIGHT, tm34.START_TIME XM_TIME, tm34.MEND_INNER_MODE MEND_INNER_MODE, tm34.MEND_OUTER_MODE MEND_OUTER_MODE, tm34.MEND_CALCULATE_RATE, tm34.MEND_TOTAL_TIME MEND_TOTAL_TIME, T.TRAN_END_TIME, T.HAND_OVER_GROUP JK_SHIFT_GROUP, t.DST_STOCK_CODE, t.mat_act_wt, CASE WHEN TW62.LOAD_CODE_FACTORY IS NULL THEN TWM41.C_SENDDEPT ELSE TW62.LOAD_CODE_FACTORY END RETURNPLANT,CASE WHEN TW62.SHIFT_GROUP IS NULL THEN TWM41.C_GROUP ELSE TW62.SHIFT_GROUP END SHIFTRETURN, CASE WHEN TW62.UNLOAD_END_TIME IS NULL THEN TWM41.T_INSTOCKTIME ELSE TW62.UNLOAD_END_TIME END RETURNDATE, CASE WHEN TW62.BACK1 IS NULL THEN TWM41.C_QULITYTYPE ELSE TW62.BACK1 END RETURNREASON, tm39.RECUT_DATE GQ_RECUT_DATE, tm39.PROD_SHIFT_GROUP GQ_PROD_GROUP, tm39.CUTTING_TYPE GQ_CUTTING_TYPE, case when length2(SLAB_NO)>=20 then to_number(decode(substr(T.slab_no, length(T.slab_no) - 2, 3), ' ', 0,substr(T.slab_no, length(T.slab_no) - 2, 3))) end CAST_DIV_NO, t.DEV_CODE, (SELECT PROD_SHIFT_GROUP FROM TMMSM36 WHERE MAT_NO = T.MAT_NO) PROD_GROUP_SB, t.HOT_SEND_FLAG, t.ZL_REASON_DESC, t.JUDGE_RESULT_1, t.REMARK,CASE WHEN TWM12.UNLOAD_CODE_AREA IS NULL THEN twm61.UNLOAD_CODE_AREA ELSE TWM12.UNLOAD_CODE_AREA END UNLOAD_CODE_AREA, CASE WHEN TWM12.TRUCK_NO IS NULL THEN twm61.TRUCK_NO ELSE TWM12.TRUCK_NO END TRUCK_NO, t.STOCK_L2, t.ORDER_NO, t.mat_no, (SELECT DELIVY_DATE from tqmom01 where ORDER_NO = T.ORDER_NO) DELIVY_DATE, (SELECT ORDER_THICK from tqmom01 where ORDER_NO = T.ORDER_NO) ORDER_THICK, t.SG_GRADE_1, (SELECT GRADE_TYPE FROM DA_GRADE_TYPE WHERE GRADE_ID = T.ST_NO) GRADE_TYPE, (SELECT SCRAP_TYPE FROM DA_GRADE_TYPE WHERE GRADE_ID = T.ST_NO) SCRAP_TYPE, t.slab_no, tm34.GRINDING_START_TIME, tm34.GRINDING_OUTER_END_TIME, decode(tm34.MEND_BEFORE_UPPER_TEMP, 0, tm34.MEND_AFTER_UPPER_TEMP, tm34.MEND_BEFORE_UPPER_TEMP) MEND_BEFORE_TEMP, decode(tm34.MEND_BEFORE_BOTTOM_TEMP, 0, tm34.MEND_AFTER_BOTTOM_TEMP, MEND_BEFORE_BOTTOM_TEMP) MEND_AFTER_TEMP, t.TRUCK_NO as CHEHAO, T.STOCK_PLACE_NO, T.STOCK_PLACE_NO BP_TOCK_L2, TM34.REC_REVISE_TIME REC_REVISE_TIME, ' ' ORDER_NO_DD, DECODE(SUBSTR(T.ST_NO, 0, 1), 1, '不锈钢', '碳钢') ST_NO_TYPE_1, CASE WHEN SUBSTR(T.ST_NO, 0, 2) = '1A' OR SUBSTR(T.ST_NO, 0, 2) = '1D' THEN '镍钢' WHEN SUBSTR(T.ST_NO, 0, 2) = '1M' OR SUBSTR(T.ST_NO, 0, 2) = '1F' THEN '铬钢' WHEN SUBSTR(T.ST_NO, 0, 1) = '1' THEN '不锈钢' else '碳钢' end as ST_NO_TYPE_2, CASE WHEN TWM12.SHIFT_GROUP IS NULL THEN twm61.SHIFT_GROUP ELSE TWM12.SHIFT_GROUP END ZC_PROD_GROUP, CASE WHEN TWM12.OUT_STOCK_TIME IS NULL THEN twm61.LOAD_END_TIME ELSE TWM12.OUT_STOCK_TIME END ZC_TIME, T.C_DELIVERY_STOCK, DECODE(T.LOGISTICS_STATUS, '2', 'W', '3', 'Y', 'N') LOGISTICS_STATUS, DECODE(T.LGORT, '6242', '成品库', '6246', '修磨库') VALUE_TYPE, T.PRODUCT_FLAG , case when STOCK_L2 in('CS-HSM', 'SS-HSM', 'HF') THEN '2250' when DST_STOCK_CODE = 'WXK104' THEN '钢坯库' when DST_STOCK_CODE in('WXK101', 'WXK102', 'WXK103') THEN '储运站' when DST_STOCK_CODE in('635003') THEN '1549' when DST_STOCK_CODE in('639002') THEN '4300' when DST_STOCK_CODE in('622002') THEN '南区' when DST_STOCK_CODE in('631003') THEN '型材' when DST_STOCK_CODE in('TBZX01') THEN '太北' else '二钢北区' end location,CASE WHEN t2.MAT_NO IS NULL THEN '0' ELSE '1' END need_mend,nvl(t2.OFFLINE_FLAG, ' ') OFFLINE_FLAG,nvl(t2.MEND_CAUSE, ' ') MEND_CAUSE,nvl(t2.OFFLINE_REASON, ' ') OFFLINE_REASON FROM(SELECT MAT_NO, SLAB_CUT_TIME, PROD_SHIFT_GROUP, HEAT_NO, BATCH, ST_NO, MAT_ACT_LEN, MAT_ACT_WIDTH, MAT_ACT_THICK, RECEIVE_WEIGHT, GUIDE_DEST, CASTING_PRE_JUDGMENT, CASTING_PURPOSE, SURF_QUALITY, RECV_MAT_TIME, C_STATESIGN, USAGE_DECISION, ARCHIVE_TIME, MEND_FLAG, C_DELIVERY_STOCK, TRAN_END_TIME, PRACTICE_NO, DST_STOCK_CODE, mat_act_wt, slab_no, DEV_CODE, HOT_SEND_FLAG, ZL_REASON_DESC, JUDGE_RESULT_1, REMARK, UNLOAD_CODE, ORDER_NO, SG_GRADE_1, TRUCK_NO, STOCK_PLACE_NO, STOCK_L2, LOAD_SCHEME_NO, LOGISTICS_STATUS, LGORT, PRODUCT_FLAG, HAND_OVER_GROUP,C_DIV FROM TMMSM01 where 1 = 1 AND 1 = 1 ) T LEFT JOIN(SELECT PROD_SHIFT_GROUP, MEND_SHIFT,MEND_SET, MEND_AFTER_WEIGHT, START_TIME, MEND_INNER_MODE, MEND_OUTER_MODE, MEND_CALCULATE_RATE, MEND_TOTAL_TIME, GRINDING_START_TIME, GRINDING_OUTER_END_TIME, MEND_BEFORE_UPPER_TEMP, MEND_AFTER_UPPER_TEMP, MEND_BEFORE_BOTTOM_TEMP, MEND_AFTER_BOTTOM_TEMP, REC_REVISE_TIME, mat_no FROM( SELECT ROW_NUMBER() over(PARTITION BY MAT_NO ORDER BY REC_CREATE_TIME DESC) TM34_MAX, PROD_SHIFT_GROUP,MEND_SHIFT, MEND_SET, MEND_AFTER_WEIGHT, START_TIME, MEND_INNER_MODE, MEND_OUTER_MODE, MEND_CALCULATE_RATE, MEND_TOTAL_TIME, GRINDING_START_TIME, GRINDING_OUTER_END_TIME, MEND_BEFORE_UPPER_TEMP, MEND_AFTER_UPPER_TEMP, MEND_BEFORE_BOTTOM_TEMP, MEND_AFTER_BOTTOM_TEMP, REC_REVISE_TIME, mat_no FROM TMMSM34) WHERE TM34_MAX = 1) tm34 on t.mat_no = tm34.MAT_NO LEFT JOIN(select RECUT_DATE, PROD_SHIFT_GROUP, CUTTING_TYPE, MAT_no from(SELECT ROW_NUMBER() over(PARTITION BY MAT_NO ORDER BY RESUME_SEQ_NO DESC) TM39max, RECUT_DATE, PROD_SHIFT_GROUP, CUTTING_TYPE, MAT_NO from tmmsm39) where TM39max = '1') TM39 ON t.mat_no = tm39.mat_no LEFT JOIN(select LOAD_CODE_FACTORY, SHIFT_GROUP, MAT_NO, LOAD_END_TIME, RETURNREASON,UNLOAD_END_TIME,BACK1 from(SELECT ROW_NUMBER() over(PARTITION BY MAT_NO ORDER BY REC_CREATE_TIME DESC) tw62_max, LOAD_CODE_FACTORY, mat_no, SHIFT_GROUP, LOAD_END_TIME, RETURNREASON,UNLOAD_END_TIME,BACK1 from (SELECT MAT_NO,REC_CREATE_TIME,LOAD_CODE_FACTORY,SHIFT_GROUP,LOAD_END_TIME,RETURNREASON,UNLOAD_END_TIME,BACK1 FROM TWMSM62 WHERE UNLOAD_CODE_FACTORY = '6240' AND MAT_NO != ' ' UNION SELECT MAT_NO,REC_CREATE_TIME,UNLOAD_CODE_FACTORY,BACK3,UNLOAD_END_TIME,BACK4,UNLOAD_END_TIME,BACK1 FROM TWMSM13)) where tw62_max = '1') TW62 ON T.MAT_NO = TW62.MAT_NO LEFT JOIN(SELECT MAT_NO, MEND_BEFORE_WEIGHT, MEND_AFTER_WEIGHT FROM(SELECT ROW_NUMBER() over(PARTITION BY MAT_NO ORDER BY REC_CREATE_TIME DESC) TM34_1MAX, MAT_NO, MEND_BEFORE_WEIGHT, MEND_AFTER_WEIGHT FROM TMMSM34_1) WHERE TM34_1MAX = '1') tm34_1 on t.mat_no = tm34_1.MAT_NO LEFT JOIN vWMSM12 TWM12 ON T.MAT_NO = TWM12.MAT_NO AND TWM12.LOAD_SCHEME_NO = T.LOAD_SCHEME_NO LEFT JOIN (select MAT_NO,OFFLINE_FLAG,MEND_CAUSE,OFFLINE_REASON from get_offline_flag) t2 ON t.mat_no =t2.MAT_NO LEFT JOIN twmsm61 TWM61 ON T.MAT_NO = TWM61.MAT_NO AND TWM61.PRACTICE_NO = T.PRACTICE_NO AND TWM61.LOAD_CODE!='624002065' LEFT JOIN (SELECT C_BATCHUNIT, I_RESERVECOL4,C_STATESIGN,C_SENDDEPT,C_GROUP,T_INSTOCKTIME,C_QULITYTYPE FROM(SELECT ROW_NUMBER() over(PARTITION BY C_BATCHUNIT ORDER BY REC_CREATE_TIME DESC) TW41_1MAX,C_BATCHUNIT, I_RESERVECOL4, C_STATESIGN, C_SENDDEPT, C_GROUP, T_INSTOCKTIME, C_QULITYTYPE FROM TWM41DJ WHERE I_RESERVECOL4 = '1' AND C_STATESIGN = '2') WHERE TW41_1MAX = '1') TWM41 ON T.MAT_NO = TWM41.C_BATCHUNIT WHERE T.MAT_ACT_WT > 0;

-- ---------------------------------------------------------------------
-- sql_id: CHANGE-182 | module: MMSM
-- 来源: Server/MMSM/p_mmsm_17660/mmsmshdc_inq.cpp | 函数: f_mmsmshdc_inq | 锚点: L286-L366
-- 拼接填充: sqlstr_temp=AND 1 = 1, sqlstr_temp=AND 1 = 1, sqlstr_temp=AND 1 = 1, sqlstr_temp=AND 1 = 1, sqlstr_temp=AND 1 = 1
SELECT t1.REC_CREATE_TIME, t1.SLAB_CUT_TIME, t1.PROD_SHIFT_GROUP, t1.HEAT_NO, t1.BATCH, t1.WL_CODE, t1.WL_DESCRIPTION, t1.ST_NO, 
 t1.MAT_ACT_LEN, t1.MAT_ACT_WIDTH, t1.MAT_ACT_THICK, t1.RECEIVE_WEIGHT, t1.GUIDE_DEST, t1.CASTING_PRE_JUDGMENT, t1.CASTING_PURPOSE,
 t1.SURF_QUALITY, t1.RECEIVE_STATUS, t1.RECV_MAT_TIME, t1.SPECIFIC_SEND, t1.C_STATESIGN, t1.USAGE_DECISION, t1.PROD_GROUP_TMMSM34,
 t1.MEND_SET, t1.MEND_AFTER_WEIGHT, t1.XM_TIME, t1.MEND_INNER_MODE, t1.MEND_OUTER_MODE, t1.MEND_CALCULATE_RATE, t1.MEND_TOTAL_TIME,
 t1.PROD_SHIFT_NO, t1.TRAN_END_TIME, t1.JK_SHIFT_GROUP, t1.DST_STOCK_CODE, t1.mat_act_wt, t1.RETURNPLANT, t1.SHIFTRETURN,
 t1.RETURNDATE, t1.RETURNREASON, t1.GQ_RECUT_DATE, t1.GQ_PROD_GROUP, t1.GQ_CUTTING_TYPE, t1.CAST_DIV_NO, t1.DEV_CODE, t1.PROD_GROUP_SB,
 t1.HOT_SEND_FLAG, t1.ZL_REASON_DESC, t1.JUDGE_RESULT_1, t1.REMARK, t1.UNLOAD_CODE_AREA, t1.TRUCK_NO, t1.STOCK_L2, t1.ORDER_NO,
 t1.mat_no, t1.DELIVY_DATE, t1.ORDER_THICK, t1.SG_GRADE_1, t1.GRADE_TYPE, t1.SCRAP_TYPE, t1.slab_no, t1.GRINDING_START_TIME,
 t1.GRINDING_OUTER_END_TIME, t1.MEND_BEFORE_TEMP, t1.MEND_AFTER_TEMP, t1.CHEHAO, t1.STOCK_PLACE_NO, t1.BP_TOCK_L2, t1.REC_REVISE_TIME,
 t1.ORDER_NO_DD, t1.ST_NO_TYPE_1, t1.ST_NO_TYPE_2, t1.ZC_PROD_GROUP, t1.ZC_TIME, t1.C_DELIVERY_STOCK, t1.LOGISTICS_STATUS,
 t1.VALUE_TYPE, t1.PRODUCT_FLAG, t1.C_DIV, t1.SLAB_STORAGE_TYPE, t1.MAT_ID, t1.need_mend, t1.MEND_CAUSE,T1.OFFLINE_FLAG,T1.OFFLINE_REASON, t1.location,
 CASE WHEN (t1.SLAB_STORAGE_TYPE = ' ' or t1.SLAB_STORAGE_TYPE = '01') THEN ' ' WHEN t1.SLAB_STORAGE_TYPE = '02' AND t1.SLAB_CUT_TIME <> ' ' THEN TO_CHAR(TO_DATE(t1.SLAB_CUT_TIME, 'YYYYMMDDHH24MISS') + t1.TIME_OFFSET_A, 'YYYYMMDDHH24MISS') WHEN t1.SLAB_STORAGE_TYPE = '03' AND t1.SLAB_CUT_TIME <> ' ' THEN TO_CHAR(TO_DATE(t1.SLAB_CUT_TIME, 'YYYYMMDDHH24MISS') + t1.TIME_OFFSET_B, 'YYYYMMDDHH24MISS') 
 WHEN t1.SLAB_STORAGE_TYPE = '04' AND t1.ZC_TIME <> ' ' THEN TO_CHAR(TO_DATE(t1.ZC_TIME, 'YYYYMMDDHH24MISS') + t1.TIME_OFFSET_C, 'YYYYMMDDHH24MISS') WHEN t1.SLAB_STORAGE_TYPE = '05' AND t1.ZC_TIME <> ' ' THEN t1.ZC_TIME ELSE ' ' END AS PILE_COOL_START_TIME,
 CASE WHEN t1.SLAB_STORAGE_TYPE = ' ' THEN ' ' WHEN t1.SLAB_STORAGE_TYPE = '01' THEN ' ' WHEN(t1.SLAB_STORAGE_TYPE = '02' or t1.SLAB_STORAGE_TYPE = '03') THEN CASE WHEN t1.MEND_TOTAL_TIME IS NOT NULL AND t1.GRINDING_START_TIME IS NOT NULL THEN TO_CHAR(TO_DATE(t1.GRINDING_START_TIME, 'YYYYMMDDHH24MISS') - t1.TIME_OFFSET_A, 'YYYYMMDDHH24MISS') WHEN t1.MEND_TOTAL_TIME IS NULL AND t1.ZC_TIME IS NOT NULL 
 THEN TO_CHAR(TO_DATE(t1.ZC_TIME, 'YYYYMMDDHH24MISS') - t1.TIME_OFFSET_A, 'YYYYMMDDHH24MISS') WHEN t1.MEND_TOTAL_TIME IS NULL AND t1.ZC_TIME IS NULL AND t1.TRAN_END_TIME <> ' ' THEN TO_CHAR(TO_DATE(t1.TRAN_END_TIME, 'YYYYMMDDHH24MISS') - t1.TIME_OFFSET_A, 'YYYYMMDDHH24MISS') ELSE ' ' END WHEN t1.SLAB_STORAGE_TYPE = '05' THEN t1.REC_CREATE_TIME ELSE ' ' END AS PILE_COOL_END_TIME, 
 CASE WHEN t1.SLAB_STORAGE_TYPE = ' ' THEN ' ' WHEN t1.SLAB_STORAGE_TYPE = '01' THEN CASE WHEN t1.PROD_SHIFT_GROUP = 'A' THEN '张宇峰' WHEN t1.PROD_SHIFT_GROUP = 'B' THEN '崔谦' WHEN t1.PROD_SHIFT_GROUP = 'C' THEN '黄竹生' WHEN t1.PROD_SHIFT_GROUP = 'D' THEN '李洪伟' ELSE ' ' END WHEN(t1.SLAB_STORAGE_TYPE = '02' or t1.SLAB_STORAGE_TYPE = '03' or t1.SLAB_STORAGE_TYPE = '04') 
 THEN CASE WHEN t1.MEND_TOTAL_TIME IS NOT NULL THEN t1.PROD_GROUP_TMMSM34 WHEN t1.MEND_TOTAL_TIME IS NULL AND t1.ZC_PROD_GROUP IS NOT NULL THEN t1.ZC_PROD_GROUP WHEN t1.MEND_TOTAL_TIME IS NULL AND t1.ZC_PROD_GROUP IS NULL AND t1.TRAN_END_TIME IS NOT NULL THEN t1.JK_SHIFT_GROUP ELSE ' ' END ELSE ' ' END AS HEAT_TREAT_OPERATOR 
 FROM(SELECT t.*,
 CASE SUBSTR(t.MAT_ID, -1) 
 WHEN '0' THEN 0.01074 WHEN '1' THEN 0.01119 WHEN '2' THEN 0.0124 WHEN '3' THEN 0.01266 WHEN '4' THEN 0.01365 WHEN '5' THEN 0.01094 
 WHEN '6' THEN 0.01178 WHEN '7' THEN 0.01194 WHEN '8' THEN 0.01288 WHEN '9' THEN 0.01322 END AS TIME_OFFSET_A,
 CASE SUBSTR(t.MAT_ID, -1) 
 WHEN '0' THEN 0.00369 WHEN '1' THEN 0.00465 WHEN '2' THEN 0.00492 WHEN '3' THEN 0.00598 WHEN '4' THEN 0.00649 WHEN '5' THEN 0.00409 
 WHEN '6' THEN 0.00429 WHEN '7' THEN 0.00542 WHEN '8' THEN 0.00566 WHEN '9' THEN 0.00664 END AS TIME_OFFSET_B,
 CASE SUBSTR(t.MAT_ID, -1) 
 WHEN '0' THEN 0.02112 WHEN '1' THEN 0.02243 WHEN '2' THEN 0.02426 WHEN '3' THEN 0.02434 WHEN '4' THEN 0.02617 WHEN '5' THEN 0.02188 
 WHEN '6' THEN 0.0231 WHEN '7' THEN 0.02534 WHEN '8' THEN 0.02699 WHEN '9' THEN 0.02718 END AS TIME_OFFSET_C 
 FROM(SELECT NVL(TM_XC.RECV_MAT_TIME,' ') REC_CREATE_TIME, T.SLAB_CUT_TIME, T.PROD_SHIFT_GROUP, T.HEAT_NO, T.BATCH, ' ' WL_CODE, ' ' WL_DESCRIPTION, T.ST_NO, T.MAT_ACT_LEN, T.MAT_ACT_WIDTH, T.MAT_ACT_THICK, T.RECEIVE_WEIGHT, T.GUIDE_DEST, T.CASTING_PRE_JUDGMENT, T.CASTING_PURPOSE, T.SURF_QUALITY,
 DECODE(T.RECEIVE_WEIGHT, 0, 'N', 'Y') RECEIVE_STATUS, T.RECV_MAT_TIME, DECODE(T.RECEIVE_WEIGHT, 0, 'N', 'S') SPECIFIC_SEND, DECODE(T.C_STATESIGN, '3', 'S', '1', 'W', 'N') C_STATESIGN, T.USAGE_DECISION, tm34.MEND_SHIFT as PROD_GROUP_TMMSM34,
 CASE WHEN T.C_DELIVERY_STOCK = '6235' THEN 'C0' WHEN(SUBSTR(T.MAT_NO, 0, 2) = 'A0' OR SUBSTR(T.MAT_NO, 0, 2) = 'A1' OR SUBSTR(T.MAT_NO, 0, 2) = 'A2' OR SUBSTR(T.MAT_NO, 0, 2) = 'A3' OR SUBSTR(T.MAT_NO, 0, 2) = 'A5' OR SUBSTR(T.MAT_NO, 0, 2) = 'A5' OR SUBSTR(T.MAT_NO, 0, 2) = 'A6' OR SUBSTR(T.MAT_NO, 0, 2) = 'B0' OR SUBSTR(T.MAT_NO, 0, 2) = 'B1' OR SUBSTR(T.MAT_NO, 0, 2) = 'B2'
 OR SUBSTR(T.MAT_NO, 0, 2) = 'B9') AND tm34.mat_no is null AND TM34_1.MAT_NO <> ' ' AND TM34_1.MEND_AFTER_WEIGHT <> tm34_1.MEND_BEFORE_WEIGHT THEN 'B0' WHEN T.ARCHIVE_TIME <> ' ' AND T.MEND_FLAG in('0', ' ') AND T.C_DIV = '1' THEN 'A0' else tm34.MEND_SET end MEND_SET,
 tm34.MEND_AFTER_WEIGHT MEND_AFTER_WEIGHT, tm34.START_TIME XM_TIME, tm34.MEND_INNER_MODE MEND_INNER_MODE, tm34.MEND_OUTER_MODE MEND_OUTER_MODE, tm34.MEND_CALCULATE_RATE, tm34.MEND_TOTAL_TIME MEND_TOTAL_TIME,
 CASE WHEN substr(T.RECV_MAT_TIME, 9, 4) >= '0800' AND substr(T.RECV_MAT_TIME, 9, 4) <= '2000' THEN '白班' WHEN T.RECV_MAT_TIME = ' ' THEN ' ' ELSE '夜班' END PROD_SHIFT_NO,
 T.TRAN_END_TIME, T.HAND_OVER_GROUP JK_SHIFT_GROUP, t.DST_STOCK_CODE, t.mat_act_wt,
 CASE WHEN TW62.LOAD_CODE_FACTORY IS NULL THEN TWM41.C_SENDDEPT ELSE TW62.LOAD_CODE_FACTORY END RETURNPLANT,
 CASE WHEN TW62.SHIFT_GROUP IS NULL THEN TWM41.C_GROUP ELSE TW62.SHIFT_GROUP END SHIFTRETURN,
 CASE WHEN TW62.UNLOAD_END_TIME IS NULL THEN TWM41.T_INSTOCKTIME ELSE TW62.UNLOAD_END_TIME END RETURNDATE,
 CASE WHEN TW62.BACK1 IS NULL THEN TWM41.C_QULITYTYPE ELSE TW62.BACK1 END RETURNREASON,
 tm39.RECUT_DATE GQ_RECUT_DATE, tm39.PROD_SHIFT_GROUP GQ_PROD_GROUP, tm39.CUTTING_TYPE GQ_CUTTING_TYPE,
 case when length2(SLAB_NO) >= 20 then to_number(decode(substr(T.slab_no, length(T.slab_no) - 2, 3), ' ', 0, substr(T.slab_no, length(T.slab_no) - 2, 3))) end CAST_DIV_NO,
 t.DEV_CODE, (SELECT PROD_SHIFT_GROUP FROM TMMSM36 WHERE MAT_NO = T.MAT_NO) PROD_GROUP_SB, t.HOT_SEND_FLAG, t.ZL_REASON_DESC, t.JUDGE_RESULT_1, t.REMARK,
 CASE WHEN TWM12.UNLOAD_CODE_AREA IS NULL THEN twm61.UNLOAD_CODE_AREA ELSE TWM12.UNLOAD_CODE_AREA END UNLOAD_CODE_AREA,
 CASE WHEN TWM12.TRUCK_NO IS NULL THEN twm61.TRUCK_NO ELSE TWM12.TRUCK_NO END TRUCK_NO,
 t.STOCK_L2, t.ORDER_NO, t.mat_no,
 (SELECT DELIVY_DATE from tqmom01 where ORDER_NO = T.ORDER_NO) DELIVY_DATE,
 (SELECT ORDER_THICK from tqmom01 where ORDER_NO = T.ORDER_NO) ORDER_THICK,
 t.SG_GRADE_1, (SELECT GRADE_TYPE FROM DA_GRADE_TYPE WHERE GRADE_ID = T.ST_NO) GRADE_TYPE, (SELECT SCRAP_TYPE FROM DA_GRADE_TYPE WHERE GRADE_ID = T.ST_NO) SCRAP_TYPE,
 t.slab_no, tm34.GRINDING_START_TIME, tm34.GRINDING_OUTER_END_TIME,
 decode(tm34.MEND_BEFORE_UPPER_TEMP, 0, tm34.MEND_AFTER_UPPER_TEMP, tm34.MEND_BEFORE_UPPER_TEMP) MEND_BEFORE_TEMP,
 decode(tm34.MEND_BEFORE_BOTTOM_TEMP, 0, tm34.MEND_AFTER_BOTTOM_TEMP, MEND_BEFORE_BOTTOM_TEMP) MEND_AFTER_TEMP,
 t.TRUCK_NO as CHEHAO, T.STOCK_PLACE_NO, T.STOCK_L2 BP_TOCK_L2, TM34.REC_REVISE_TIME REC_REVISE_TIME, ' ' ORDER_NO_DD,DECODE(SUBSTR(T.ST_NO, 0, 1), 1, '不锈钢', '碳钢') ST_NO_TYPE_1,
 CASE WHEN SUBSTR(T.ST_NO, 0, 2) = '1A' OR SUBSTR(T.ST_NO, 0, 2) = '1D' THEN '镍钢' WHEN SUBSTR(T.ST_NO, 0, 2) = '1M' OR SUBSTR(T.ST_NO, 0, 2) = '1F' THEN '铬钢' WHEN SUBSTR(T.ST_NO, 0, 1) = '1' THEN '不锈钢' else '碳钢' end as ST_NO_TYPE_2,
 CASE WHEN TWM12.SHIFT_GROUP IS NULL THEN twm61.SHIFT_GROUP ELSE TWM12.SHIFT_GROUP END ZC_PROD_GROUP,
 CASE WHEN TWM12.OUT_STOCK_TIME IS NULL THEN twm61.LOAD_END_TIME ELSE TWM12.OUT_STOCK_TIME END ZC_TIME,
 T.C_DELIVERY_STOCK, DECODE(T.LOGISTICS_STATUS, '2', 'W', '3', 'Y', 'N') LOGISTICS_STATUS,
 DECODE(T.LGORT, '6242', '成品库', '6246', '修磨库') VALUE_TYPE, T.PRODUCT_FLAG, T.C_DIV, T.SLAB_STORAGE_TYPE, T.MAT_ID,
 CASE WHEN t2.MAT_NO IS NULL THEN '0' ELSE '1' END need_mend, nvl(t2.OFFLINE_FLAG, ' ') OFFLINE_FLAG,nvl(t2.MEND_CAUSE, ' ') MEND_CAUSE,nvl(t2.OFFLINE_REASON, ' ') OFFLINE_REASON,
 case when t.C_STATESIGN != '3' and STOCK_L2 in('CS-HSM', 'SS-HSM', 'HF') THEN '2250' when t.C_STATESIGN != '3' and DST_STOCK_CODE = 'WXK104' THEN '钢坯库' when t.C_STATESIGN != '3' and DST_STOCK_CODE in('WXK101', 'WXK102', 'WXK103') THEN '储运站' when t.C_STATESIGN != '3' and DST_STOCK_CODE in('635003') THEN '1549' when t.C_STATESIGN != '3' and DST_STOCK_CODE in('639002') THEN '4300' when t.C_STATESIGN != '3' and DST_STOCK_CODE in('622002') THEN '南区'
 when t.C_STATESIGN != '3' and DST_STOCK_CODE in('631003') THEN '型材' when t.C_STATESIGN != '3' and DST_STOCK_CODE in('TBZX01') THEN '太北' when t.C_STATESIGN != '3' then '二钢北区' when t.C_STATESIGN = '3' and t.C_DELIVERY_STOCK = '6361' THEN '2250' when t.C_STATESIGN = '3' and t.C_DELIVERY_STOCK = '6351' THEN '1549' when t.C_STATESIGN = '3' and t.C_DELIVERY_STOCK = '6391' THEN '4300' when t.C_STATESIGN = '3' and t.C_DELIVERY_STOCK = '6222' THEN '南区'
 when t.C_STATESIGN = '3' and t.C_DELIVERY_STOCK = '6311' and t.PRODUCT_FLAG = '0' THEN '型材' when t.C_STATESIGN = '3' and t.C_DELIVERY_STOCK = '6311' and t.PRODUCT_FLAG = '1' and t.TRANSFER_FLAG != '1' and DST_STOCK_CODE in('WXK101', 'WXK102', 'WXK103') THEN '储运站' when t.C_STATESIGN = '3' and t.C_DELIVERY_STOCK = '6311' and t.PRODUCT_FLAG = '1' and t.TRANSFER_FLAG != '1' and DST_STOCK_CODE = 'WXK104' THEN '储运站' when t.C_STATESIGN = '3'
 and t.C_DELIVERY_STOCK = '6311' and t.PRODUCT_FLAG = '1' and t.TRANSFER_FLAG = '1' then '厂外' else '二钢北区' end location
 FROM(SELECT MAT_NO, SLAB_CUT_TIME, PROD_SHIFT_GROUP, HEAT_NO, BATCH, ST_NO, MAT_ACT_LEN, MAT_ACT_WIDTH, MAT_ACT_THICK, RECEIVE_WEIGHT, GUIDE_DEST, CASTING_PRE_JUDGMENT, CASTING_PURPOSE, SURF_QUALITY, RECV_MAT_TIME, C_STATESIGN, TRANSFER_FLAG, USAGE_DECISION, ARCHIVE_TIME, MEND_FLAG, C_DELIVERY_STOCK, TRAN_END_TIME, PRACTICE_NO, DST_STOCK_CODE, mat_act_wt, slab_no, DEV_CODE, HOT_SEND_FLAG, ZL_REASON_DESC, JUDGE_RESULT_1, REMARK, UNLOAD_CODE, ORDER_NO, SG_GRADE_1, TRUCK_NO, STOCK_PLACE_NO, STOCK_L2, LOAD_SCHEME_NO, LOGISTICS_STATUS, LGORT, PRODUCT_FLAG, HAND_OVER_GROUP, C_DIV, SLAB_STORAGE_TYPE, MAT_ID FROM TMMSM01 where 1 = 1 AND 1 = 1 AND MAT_NO NOT IN(select IN_MAT_NO FROM TMMSM35) and mat_no not in(SELECT MAT_NO FROM TMMSM35) UNION ALL SELECT MAT_NO, SLAB_CUT_TIME, PROD_SHIFT_GROUP, HEAT_NO, BATCH, ST_NO, MAT_ACT_LEN, MAT_ACT_WIDTH, MAT_ACT_THICK, RECEIVE_WEIGHT, GUIDE_DEST, CASTING_PRE_JUDGMENT, CASTING_PURPOSE, SURF_QUALITY, RECV_MAT_TIME, C_STATESIGN, TRANSFER_FLAG, USAGE_DECISION, ARCHIVE_TIME, MEND_FLAG, C_DELIVERY_STOCK, TRAN_END_TIME, PRACTICE_NO, DST_STOCK_CODE, mat_act_wt, slab_no, DEV_CODE, HOT_SEND_FLAG, ZL_REASON_DESC, JUDGE_RESULT_1, REMARK, UNLOAD_CODE,
 ORDER_NO, SG_GRADE_1, TRUCK_NO, STOCK_PLACE_NO, STOCK_L2, LOAD_SCHEME_NO, LOGISTICS_STATUS, LGORT, PRODUCT_FLAG, HAND_OVER_GROUP, C_DIV, SLAB_STORAGE_TYPE, MAT_ID FROM HMMSM01 where 1 = 1 AND 1 = 1 AND MAT_NO NOT IN(select IN_MAT_NO FROM TMMSM35) and mat_no not in(SELECT MAT_NO FROM TMMSM35) UNION ALL SELECT MAT_NO, SLAB_CUT_TIME, PROD_SHIFT_GROUP, HEAT_NO, BATCH, ST_NO, MAT_ACT_LEN, MAT_ACT_WIDTH, MAT_ACT_THICK, RECEIVE_WEIGHT, GUIDE_DEST, CASTING_PRE_JUDGMENT, CASTING_PURPOSE, SURF_QUALITY, RECV_MAT_TIME, C_STATESIGN, TRANSFER_FLAG, USAGE_DECISION, ARCHIVE_TIME, MEND_FLAG, C_DELIVERY_STOCK, TRAN_END_TIME, PRACTICE_NO, DST_STOCK_CODE, mat_act_wt, slab_no, DEV_CODE, HOT_SEND_FLAG, ZL_REASON_DESC, JUDGE_RESULT_1, REMARK, UNLOAD_CODE,
 ORDER_NO, SG_GRADE_1, TRUCK_NO, STOCK_PLACE_NO, STOCK_L2, LOAD_SCHEME_NO, LOGISTICS_STATUS, LGORT, PRODUCT_FLAG, HAND_OVER_GROUP, C_DIV, SLAB_STORAGE_TYPE, MAT_ID FROM TMMSM01 WHERE BATCH = IN_MAT_NO AND IN_MAT_NO <> ' ' AND 1 = 1 UNION ALL SELECT MAT_NO, SLAB_CUT_TIME, PROD_SHIFT_GROUP, HEAT_NO, BATCH, ST_NO, MAT_ACT_LEN, MAT_ACT_WIDTH, MAT_ACT_THICK, RECEIVE_WEIGHT, GUIDE_DEST, CASTING_PRE_JUDGMENT, CASTING_PURPOSE, SURF_QUALITY, RECV_MAT_TIME, C_STATESIGN, TRANSFER_FLAG, USAGE_DECISION, ARCHIVE_TIME, MEND_FLAG, C_DELIVERY_STOCK, TRAN_END_TIME, PRACTICE_NO, DST_STOCK_CODE, mat_act_wt, slab_no, DEV_CODE, HOT_SEND_FLAG, ZL_REASON_DESC, JUDGE_RESULT_1, REMARK, UNLOAD_CODE,
 ORDER_NO, SG_GRADE_1, TRUCK_NO, STOCK_PLACE_NO, STOCK_L2, LOAD_SCHEME_NO, LOGISTICS_STATUS, LGORT, PRODUCT_FLAG, HAND_OVER_GROUP, C_DIV, SLAB_STORAGE_TYPE, MAT_ID FROM HMMSM01 WHERE BATCH = IN_MAT_NO AND IN_MAT_NO <> ' ' AND 1 = 1) T LEFT JOIN(SELECT PROD_SHIFT_GROUP, MEND_SHIFT, MEND_SET, MEND_AFTER_WEIGHT, START_TIME, MEND_INNER_MODE, MEND_OUTER_MODE, MEND_CALCULATE_RATE, MEND_TOTAL_TIME, GRINDING_START_TIME, GRINDING_OUTER_END_TIME, MEND_BEFORE_UPPER_TEMP, MEND_AFTER_UPPER_TEMP, MEND_BEFORE_BOTTOM_TEMP, MEND_AFTER_BOTTOM_TEMP, REC_REVISE_TIME, mat_no FROM(SELECT ROW_NUMBER() over(PARTITION BY MAT_NO ORDER BY REC_CREATE_TIME DESC) TM34_MAX, PROD_SHIFT_GROUP, MEND_SHIFT, MEND_SET,
 MEND_AFTER_WEIGHT, START_TIME, MEND_INNER_MODE, MEND_OUTER_MODE, MEND_CALCULATE_RATE, MEND_TOTAL_TIME, GRINDING_START_TIME, GRINDING_OUTER_END_TIME, MEND_BEFORE_UPPER_TEMP, MEND_AFTER_UPPER_TEMP, MEND_BEFORE_BOTTOM_TEMP, MEND_AFTER_BOTTOM_TEMP, REC_REVISE_TIME, mat_no FROM TMMSM34) WHERE TM34_MAX = 1) tm34 on t.mat_no = tm34.MAT_NO
 LEFT JOIN(select RECUT_DATE, PROD_SHIFT_GROUP, CUTTING_TYPE, MAT_no from(SELECT ROW_NUMBER() over(PARTITION BY MAT_NO ORDER BY RESUME_SEQ_NO DESC) TM39max, RECUT_DATE, PROD_SHIFT_GROUP, CUTTING_TYPE, MAT_NO from tmmsm39) where TM39max = '1') TM39 ON t.mat_no = tm39.mat_no
 LEFT JOIN(select LOAD_CODE_FACTORY, SHIFT_GROUP, MAT_NO, UNLOAD_END_TIME, RETURNREASON, BACK1 from(SELECT ROW_NUMBER() over(PARTITION BY MAT_NO ORDER BY REC_CREATE_TIME DESC) tw62_max, LOAD_CODE_FACTORY, mat_no, SHIFT_GROUP, UNLOAD_END_TIME, RETURNREASON, BACK1 from twmsm62) where tw62_max = '1') TW62 ON T.MAT_NO = TW62.MAT_NO
 LEFT JOIN(SELECT MAT_NO, MEND_BEFORE_WEIGHT, MEND_AFTER_WEIGHT FROM(SELECT ROW_NUMBER() over(PARTITION BY MAT_NO ORDER BY REC_CREATE_TIME DESC) TM34_1MAX, MAT_NO, MEND_BEFORE_WEIGHT, MEND_AFTER_WEIGHT FROM TMMSM34_1) WHERE TM34_1MAX = '1') tm34_1 on t.mat_no = tm34_1.MAT_NO
 LEFT JOIN vWMSM12 TWM12 ON T.MAT_NO = TWM12.MAT_NO AND TWM12.LOAD_SCHEME_NO = T.LOAD_SCHEME_NO
 LEFT JOIN twmsm61 TWM61 ON T.MAT_NO = TWM61.MAT_NO AND TWM61.PRACTICE_NO = T.PRACTICE_NO
 LEFT JOIN (select MAT_NO,OFFLINE_FLAG,MEND_CAUSE,OFFLINE_REASON from get_offline_flag) t2 ON t.mat_no = t2.MAT_NO
 LEFT JOIN(SELECT C_BATCHUNIT, I_RESERVECOL4, C_STATESIGN, C_SENDDEPT, C_GROUP, T_INSTOCKTIME, C_QULITYTYPE FROM(SELECT ROW_NUMBER() over(PARTITION BY C_BATCHUNIT ORDER BY REC_CREATE_TIME DESC) TW41_1MAX, C_BATCHUNIT, I_RESERVECOL4, C_STATESIGN, C_SENDDEPT, C_GROUP, T_INSTOCKTIME, C_QULITYTYPE FROM TWM41DJ WHERE I_RESERVECOL4 = '1' AND C_STATESIGN = '2') WHERE TW41_1MAX = '1') TWM41 ON T.MAT_NO = TWM41.C_BATCHUNIT
 LEFT JOIN (SELECT * FROM VMMSMSHDC_XC WHERE 1 = 1 AND 1 = 1) TM_XC ON T.MAT_NO = TM_XC.MAT_NO_XC 
 WHERE T.MAT_ACT_WT > 0) t) t1;
