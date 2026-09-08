-- QMTS E2 验证脚本(自动生成,需在 DM8 环境执行)
-- 语句数:47;生成日期:2026-09-06
-- 注意:仅验证语法可执行性(SELECT 返回列/类型),不验证结果等价性
-- 期望结果:全部语句编译通过,SELECT 语句返回结果集

-- [CHANGE-188] libQMTS/f_qmts_spe_single.cpp L179-L179
SELECT substr('测试值',1,'测试值'-1) || ')' || substr('测试值','测试值'+1) FROM DUAL;

-- [CHANGE-189] libQMTS/f_qmts_spe_single.cpp L193-L193
SELECT substr('测试值',1,'测试值'-1) || ')' || substr('测试值','测试值'+1) FROM DUAL;

-- [CHANGE-190] libQMTS/f_qmts_spe_single.cpp L221-L221
SELECT substr('测试值',1,'测试值'-1) || 'abs(' || substr('测试值','测试值'+1) FROM DUAL;

-- [CHANGE-191] libQMTS/f_qmts_spe_single.cpp L235-L235
SELECT substr('测试值',1,'测试值'-1) || 'abs(' || substr('测试值','测试值'+1) FROM DUAL;

-- [CHANGE-192] libQMTS/f_qmts_spe_single.cpp L288-L288
SELECT replace('测试值','测试值','') FROM DUAL;

-- [CHANGE-193] libQMTS/f_qmts_spe_single.cpp L302-L302
SELECT replace('测试值','测试值','') FROM DUAL;

-- [CHANGE-194] libQMTS/f_qmts_spe_single.cpp L402-L402
SELECT ROUND(1.0,4) FROM DUAL;

-- [CHANGE-195] libQMTS/f_qmts_spe_single.cpp L416-L416
SELECT ROUND(1.0,4) FROM DUAL;

-- [CHANGE-196] libQMTS/f_qmts_spe_sm.cpp L357-L357
SELECT substr('测试值',1,'测试值'-1) || ')' || substr('测试值','测试值'+1) FROM DUAL;

-- [CHANGE-197] libQMTS/f_qmts_spe_sm.cpp L371-L371
SELECT substr('测试值',1,'测试值'-1) || ')' || substr('测试值','测试值'+1) FROM DUAL;

-- [CHANGE-198] libQMTS/f_qmts_spe_sm.cpp L399-L399
SELECT substr('测试值',1,'测试值'-1) || 'abs(' || substr('测试值','测试值'+1) FROM DUAL;

-- [CHANGE-199] libQMTS/f_qmts_spe_sm.cpp L413-L413
SELECT substr('测试值',1,'测试值'-1) || 'abs(' || substr('测试值','测试值'+1) FROM DUAL;

-- [CHANGE-200] libQMTS/f_qmts_spe_sm.cpp L466-L466
SELECT replace('测试值','测试值','') FROM DUAL;

-- [CHANGE-201] libQMTS/f_qmts_spe_sm.cpp L480-L480
SELECT replace('测试值','测试值','') FROM DUAL;

-- [CHANGE-202] libQMTS/f_qmts_spe_sm.cpp L540-L540
SELECT replace('测试值','测试值','测试值') FROM DUAL;

-- [CHANGE-203] libQMTS/f_qmts_spe_sm.cpp L554-L554
SELECT replace('测试值','测试值','测试值') FROM DUAL;

-- [CHANGE-204] libQMTS/f_qmts_spe_sm.cpp L586-L586
SELECT replace('测试值','测试值','测试值') FROM DUAL;

-- [CHANGE-205] libQMTS/f_qmts_spe_sm.cpp L600-L600
SELECT replace('测试值','测试值','测试值') FROM DUAL;

-- [CHANGE-206] libQMTS/f_qmts_spe_sm.cpp L642-L642
SELECT ROUND(1.0,5) FROM DUAL;

-- [CHANGE-207] libQMTS/f_qmts_spe_sm.cpp L656-L656
SELECT ROUND(1.0,5) FROM DUAL;

-- [CHANGE-208] libQMTS/f_qmts_spe_sm.cpp L687-L687
SELECT replace('测试值','>','-') FROM DUAL;

-- [CHANGE-209] libQMTS/f_qmts_spe_sm.cpp L701-L701
SELECT replace('测试值','>','-') FROM DUAL;

-- [CHANGE-210] libQMTS/f_qmts_spe_sm.cpp L724-L724
SELECT replace('测试值','<','+') FROM DUAL;

-- [CHANGE-211] libQMTS/f_qmts_spe_sm.cpp L738-L738
SELECT replace('测试值','<','+') FROM DUAL;

-- [CHANGE-212] libQMTS/f_qmts_spe_sm.cpp L790-L790
SELECT replace('测试值','测试值','') FROM DUAL;

-- [CHANGE-213] libQMTS/f_qmts_spe_sm.cpp L804-L804
SELECT replace('测试值','测试值','') FROM DUAL;

-- [CHANGE-214] libQMTS/f_qmts_spe_sm.cpp L863-L863
SELECT replace('测试值','测试值','测试值') FROM DUAL;

-- [CHANGE-215] libQMTS/f_qmts_spe_sm.cpp L877-L877
SELECT replace('测试值','测试值','测试值') FROM DUAL;

-- [CHANGE-216] libQMTS/f_qmts_spe_sm.cpp L908-L908
SELECT replace('测试值','测试值','测试值') FROM DUAL;

-- [CHANGE-217] libQMTS/f_qmts_spe_sm.cpp L922-L922
SELECT replace('测试值','测试值','测试值') FROM DUAL;

-- [CHANGE-218] libQMTS/f_qmts_spe_sm.cpp L961-L961
SELECT FROM DUAL;

-- [CHANGE-219] libQMTS/f_qmts_spe_sm.cpp L975-L975
SELECT FROM DUAL;

-- [CHANGE-220] libQMTS/f_qmts_spe_sm.cpp L1095-L1095
SELECT substr('测试值',1,'测试值'-1) || ')' || substr('测试值','测试值'+1) FROM DUAL;

-- [CHANGE-221] libQMTS/f_qmts_spe_sm.cpp L1109-L1109
SELECT substr('测试值',1,'测试值'-1) || ')' || substr('测试值','测试值'+1) FROM DUAL;

-- [CHANGE-222] libQMTS/f_qmts_spe_sm.cpp L1137-L1137
SELECT substr('测试值',1,'测试值'-1) || 'abs(' || substr('测试值','测试值'+1) FROM DUAL;

-- [CHANGE-223] libQMTS/f_qmts_spe_sm.cpp L1151-L1151
SELECT substr('测试值',1,'测试值'-1) || 'abs(' || substr('测试值','测试值'+1) FROM DUAL;

-- [CHANGE-224] libQMTS/f_qmts_spe_sm.cpp L1203-L1203
SELECT replace('测试值','测试值','') FROM DUAL;

-- [CHANGE-225] libQMTS/f_qmts_spe_sm.cpp L1217-L1217
SELECT replace('测试值','测试值','') FROM DUAL;

-- [CHANGE-226] libQMTS/f_qmts_spe_sm.cpp L1276-L1276
SELECT replace('测试值','测试值','测试值') FROM DUAL;

-- [CHANGE-227] libQMTS/f_qmts_spe_sm.cpp L1290-L1290
SELECT replace('测试值','测试值','测试值') FROM DUAL;

-- [CHANGE-228] libQMTS/f_qmts_spe_sm.cpp L1322-L1322
SELECT replace('测试值','测试值','测试值') FROM DUAL;

-- [CHANGE-229] libQMTS/f_qmts_spe_sm.cpp L1336-L1336
SELECT replace('测试值','测试值','测试值') FROM DUAL;

-- [CHANGE-230] libQMTS/f_qmts_spe_sm.cpp L1377-L1377
SELECT ROUND(1.0,5) FROM DUAL;

-- [CHANGE-231] libQMTS/f_qmts_spe_sm.cpp L1391-L1391
SELECT ROUND(1.0,5) FROM DUAL;

-- [CHANGE-232] p_qmts_4800/qmts0rdr_inq.cpp L133-L171
SELECT * FROM ( SELECT T.*, CASE WHEN T.ELM_01_TC IS NULL OR T.ELM_01_TC = '' THEN '0' ELSE '1' END AS XY_FLAG, CASE WHEN T.ELM_16_TC != ' ' OR T.ELM_VALUE_16 != ' ' THEN '2' ELSE '1' END AS HS FROM( SELECT T1.*, T2.AYL_FLAG, T2.CHECK_FLAG, T2.DECIDE_CODE, T2.ELM_VALUE_16, T2.ELM_01_TC, T2.ELM_01_MIN_TC, T2.ELM_01_MAX_TC, T2.ELM_02_TC, T2.ELM_02_MIN_TC, T2.ELM_02_MAX_TC, T2.ELM_03_TC, T2.ELM_03_MIN_TC, T2.ELM_03_MAX_TC, T2.ELM_04_TC, T2.ELM_04_MIN_TC, T2.ELM_04_MAX_TC, T2.ELM_05_TC, T2.ELM_05_MIN_TC, T2.ELM_05_MAX_TC, T2.ELM_06_TC, T2.ELM_06_MIN_TC, T2.ELM_06_MAX_TC, T2.ELM_07_TC, T2.ELM_07_MIN_TC, T2.ELM_07_MAX_TC, T2.ELM_08_TC, T2.ELM_08_MIN_TC, T2.ELM_08_MAX_TC, T2.ELM_09_TC, T2.ELM_09_MIN_TC, T2.ELM_09_MAX_TC, T2.ELM_10_TC, T2.ELM_10_MIN_TC, T2.ELM_10_MAX_TC, T2.ELM_11_TC, T2.ELM_11_MIN_TC, T2.ELM_11_MAX_TC, T2.ELM_12_TC, T2.ELM_12_MIN_TC, T2.ELM_12_MAX_TC, T2.ELM_13_TC, T2.ELM_13_MIN_TC, T2.ELM_13_MAX_TC, T2.ELM_14_TC, T2.ELM_14_MIN_TC, T2.ELM_14_MAX_TC, T2.ELM_15_TC, T2.ELM_15_MIN_TC, T2.ELM_15_MAX_TC, T2.ELM_16_TC, T2.ELM_16_MIN_TC, T2.ELM_16_MAX_TC, T2.ELM_17_TC, T2.ELM_17_MIN_TC, T2.ELM_17_MAX_TC, T2.ELM_18_TC, T2.ELM_18_MIN_TC, T2.ELM_18_MAX_TC, T2.ELM_19_TC, T2.ELM_19_MIN_TC, T2.ELM_19_MAX_TC, T2.ELM_20_TC, T2.ELM_20_MIN_TC, T2.ELM_20_MAX_TC, T2.ELM_21_TC, T2.ELM_21_MIN_TC, T2.ELM_21_MAX_TC, T2.ELM_22_TC, T2.ELM_22_MIN_TC, T2.ELM_22_MAX_TC, T2.ELM_23_TC, T2.ELM_23_MIN_TC, T2.ELM_23_MAX_TC, T2.ELM_24_TC, T2.ELM_24_MIN_TC, T2.ELM_24_MAX_TC, T2.ELM_25_TC, T2.ELM_25_MIN_TC, T2.ELM_25_MAX_TC, T2.ELM_26_TC, T2.ELM_26_MIN_TC, T2.ELM_26_MAX_TC, T2.ELM_27_TC, T2.ELM_27_MIN_TC, T2.ELM_27_MAX_TC, T2.ELM_28_TC, T2.ELM_28_MIN_TC, T2.ELM_28_MAX_TC, T2.ELM_29_TC, T2.ELM_29_MIN_TC, T2.ELM_29_MAX_TC, T2.ELM_30_TC, T2.ELM_30_MIN_TC, T2.ELM_30_MAX_TC FROM TQMTS0RDR T1 LEFT JOIN TQMTS0R05 T2 ON T1.HEAT_NO = T2.HEAT_NO AND T1.ORDER_NO = T2.ORDER_NO AND T1.NOW_ROW = T2.NOW_ROW)T ) WHERE 1 = 1;

-- [CHANGE-233] p_qmts_4850/cm_0rt805_rcv.cpp L103-L103
SELECT CASE WHEN max(now_row) IS NULL THEN 0 ELSE max(now_row) END FROM TQMTS0R05 where heat_no=''and order_no='';

-- [CHANGE-187] libQMTS/f_qmts_30_ins.cpp L116-L118
SELECT T2.ELM_NAME, CASE WHEN (decode(SUBSTR(ELM_ACT,1,1),'.','0'||ELM_ACT,ELM_ACT)) IS NULL THEN '无检验或缺失' ELSE (decode(SUBSTR(ELM_ACT,1,1),'.','0'||ELM_ACT,ELM_ACT)) END, SPE_MIN, SPE_MAX, T1.ELM_OK FROM(SELECT * FROM tqmts25 WHERE ST_SAMPLE_NO = '测试值') T1 RIGHT JOIN(SELECT * FROM TQMTS02 WHERE IDX_NO IN(SELECT ELM_STD_IDX_A FROM TQMTS0X WHERE ST_NO = '测试值')) T2 ON T1.ELM_CODE = T2.ELM_CODE WHERE (ELM_OK = '1' OR ELM_OK IS NULL);

