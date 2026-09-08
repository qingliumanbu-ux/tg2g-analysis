-- CAAI E2 验证脚本(自动生成,需在 DM8 环境执行)
-- 语句数:24;生成日期:2026-09-06
-- 注意:仅验证语法可执行性(SELECT 返回列/类型),不验证结果等价性
-- 期望结果:全部语句编译通过,SELECT 语句返回结果集

-- [CHANGE-242] libCAAI/f_caai_check1.cpp L49-L60
-- 以下为写操作,执行前确认在测试环境!
update tcaaia1 set STATS_PERIOD = '测试值' ,REC_REVISE_TIME = '测试值' ,STATUS_FLAG = '0' ,CHECK_FLAG = '1' WHERE 1=1 AND (MAT_CODE IN (SELECT MAT_CODE FROM TCAAC11) or length(MAT_CODE)>19) AND SUB_BACKLOG_CODE !=' ' AND CHECK_FLAG in ('0',' ') and dept_code = CASE WHEN trim('测试值') IS NULL OR trim('测试值') = '' THEN dept_code ELSE '测试值' END AND PROD_TIME between '测试值' AND '测试值';

-- [CHANGE-243] libCAAI/f_caai_check1.cpp L89-L100
-- 以下为写操作,执行前确认在测试环境!
update tcaaia1 set STATS_PERIOD = '测试值' ,REC_REVISE_TIME = '测试值' ,STATUS_FLAG = '0' ,CHECK_FLAG = '0' ,ERROR_INFO = '交易数据有误，工序代码不能为空！' WHERE 1=1 and dept_code = CASE WHEN trim('测试值') IS NULL OR trim('测试值') = '' THEN dept_code ELSE '测试值' END AND PROD_TIME between '测试值' AND '测试值' AND SUB_BACKLOG_CODE =' ' AND CHECK_FLAG in('0', ' ');

-- [CHANGE-244] libCAAI/f_caai_check1.cpp L128-L139
-- 以下为写操作,执行前确认在测试环境!
update tcaaia1 set STATS_PERIOD = '测试值' ,REC_REVISE_TIME = '测试值' ,STATUS_FLAG = '0' ,CHECK_FLAG = '0' ,ERROR_INFO = '交易数据有误，该物料代码在产副品代码表中不存在!' WHERE CHECK_FLAG in ('0',' ') AND SUB_BACKLOG_CODE !=' ' AND (MAT_CODE NOT IN (SELECT MAT_CODE FROM TCAAC11) or length(MAT_CODE)>19) and dept_code = CASE WHEN trim('测试值') IS NULL OR trim('测试值') = '' THEN dept_code ELSE '测试值' END AND PROD_TIME between '测试值' AND '测试值';

-- [CHANGE-245] libCAAI/f_caai_check1.cpp L167-L178
-- 以下为写操作,执行前确认在测试环境!
update tcaaia1 set REC_REVISE_TIME = '测试值' ,STATUS_FLAG='1' ,ERROR_INFO=' ' WHERE 1=1 AND (exists (SELECT 1 FROM TCAAC03 WHERE TCAAC03.SUB_BACKLOG_CODE = tcaaia1.SUB_BACKLOG_CODE and TCAAC03.MAT_CODE = tcaaia1.MAT_CODE ) OR PRO_FLAG = 'O' or length(mat_code)>19) AND CHECK_FLAG='1' AND STATUS_FLAG in('0',' ') and dept_code = CASE WHEN trim('测试值') IS NULL OR trim('测试值') = '' THEN dept_code ELSE '测试值' END AND STATS_PERIOD = '测试值';

-- [CHANGE-246] libCAAI/f_caai_check1.cpp L206-L219
-- 以下为写操作,执行前确认在测试环境!
update tcaaia1 set REC_REVISE_TIME = '测试值' ,CHECK_FLAG='0' ,STATUS_FLAG='0' ,ERROR_INFO = '工序代码为【'||SUB_BACKLOG_CODE||'】，物料代码为【'||MAT_CODE||'】未维护收集规则，请至CAAC03画面维护!' WHERE 1=1 AND CHECK_FLAG='1' AND STATUS_FLAG in('0',' ') and length(MAT_CODE)<19 AND PRO_FLAG = 'I' AND not exists (SELECT 1 FROM TCAAC03 WHERE TCAAC03.SUB_BACKLOG_CODE = tcaaia1.SUB_BACKLOG_CODE and TCAAC03.MAT_CODE = tcaaia1.MAT_CODE ) and dept_code = CASE WHEN trim('测试值') IS NULL OR trim('测试值') = '' THEN dept_code ELSE '测试值' END AND STATS_PERIOD = '测试值';

-- [CHANGE-247] libCAAI/f_caai_check1.cpp L281-L287
-- 以下为写操作,执行前确认在测试环境!
update tcaaia1 set cost_center = sub_backlog_code WHERE 1=1 AND CHECK_FLAG='1' and dept_code = CASE WHEN trim('测试值') IS NULL OR trim('测试值') = '' THEN dept_code ELSE '测试值' END and STATS_PERIOD = '测试值';

-- [CHANGE-248] libCAAI/f_caai_check1.cpp L313-L325
-- 以下为写操作,执行前确认在测试环境!
update tcaaia1 t1 set REC_REVISE_TIME = '测试值' ,CHECK_FLAG='0' ,STATUS_FLAG='0' ,ERROR_INFO = '批次号为【'||RELATION_NO||'】，工序为【'||SUB_BACKLOG_CODE||'】有投无产!' WHERE 1=1 AND CHECK_FLAG='1' AND STATUS_FLAG in('0',' ') AND PRO_FLAG = 'I' AND not exists (SELECT 1 FROM tcaaia1 t2 WHERE t1.RELATION_NO = t2.RELATION_NO and t1.sub_Backlog_code = t2.sub_Backlog_code and t1.stats_period = t2.stats_period and PRO_FLAG = 'O' and dept_code = CASE WHEN trim('测试值') IS NULL OR trim('测试值') = '' THEN dept_code ELSE '测试值' END and t2.STATS_PERIOD = '测试值' ) and dept_code = CASE WHEN trim('测试值') IS NULL OR trim('测试值') = '' THEN dept_code ELSE '测试值' END and STATS_PERIOD = '测试值';

-- [CHANGE-249] libCAAI/f_caai_check1.cpp L349-L359
-- 以下为写操作,执行前确认在测试环境!
update tcaaia1 t1 set REC_REVISE_TIME = '测试值' ,ERROR_INFO = '【警告】批次号为【'||RELATION_NO||'】，工序为【'||SUB_BACKLOG_CODE||'】有产无投!' WHERE 1=1 AND CHECK_FLAG='1' AND STATUS_FLAG in('0',' ') AND PRO_FLAG = 'O' AND not exists (SELECT 1 FROM tcaaia1 t2 WHERE t1.RELATION_NO = t2.RELATION_NO and t1.sub_Backlog_code = t2.sub_Backlog_code and t1.stats_period = t2.stats_period and PRO_FLAG = 'I' and dept_code = CASE WHEN trim('测试值') IS NULL OR trim('测试值') = '' THEN dept_code ELSE '测试值' END and t2.STATS_PERIOD = '测试值' ) and dept_code = CASE WHEN trim('测试值') IS NULL OR trim('测试值') = '' THEN dept_code ELSE '测试值' END and STATS_PERIOD = '测试值';

-- [CHANGE-250] libCAAI/f_caai_ft.cpp L272-L278
select sum(wt) from ( SELECT t1.DEPT_CODE, STATS_PERIOD, COST_CENTER, prod_date, prod_shift_group, prod_shift_no, t1.sub_backlog_code, equ_no, t1.sg_sign, t1.mat_thick, t1.mat_width,SUM(CASE WHEN CAL_RATE IS NULL OR CAL_RATE = '' THEN 0 ELSE CAL_RATE END*divvy_basic_n) wt FROM tcaai01 t1 left join tcaac09 t9 on t1.cost_center=t9.sub_backlog_code and t9.mat_code='测试值' WHERE 1=1;

-- [CHANGE-251] libCAAI/f_caai_ft.cpp L344-L352
-- 以下为写操作,执行前确认在测试环境!
insert into tcaai02 (REC_CREATE_TIME,dept_code,prod_date,sub_backlog_code,cost_center,stats_period,product_code,equ_no, sg_sign,prod_shift_group,prod_shift_no, mat_thick, mat_width,VFREE1,VFREE2,MAT_CODE,RULE_TYPE,DIVVY_TYPE,WT,AMT,key_seq) select '测试值',dept_code,prod_date,sub_backlog_code,sub_backlog_code,stats_period,product_code,equ_no, sg_sign,prod_shift_group,prod_shift_no, mat_thick, mat_width,VFREE1,VFREE2,MAT_CODE,'测试值','7',wt,amt,'ft'||trim('测试值')||trim('测试值') from ( SELECT t1.product_code,t1.DEPT_CODE, STATS_PERIOD, COST_CENTER, prod_date, prod_shift_group, prod_shift_no, t1.sub_backlog_code, equ_no, t1.sg_sign, t1.mat_thick, t1.mat_width,t1.VFREE1,t1.VFREE2,'测试值' mat_code,cast(SUM(CASE WHEN CAL_RATE IS NULL OR CAL_RATE = '' THEN 0 ELSE CAL_RATE END*divvy_basic_n)/'测试值'*'测试值' as decimal(16,4)) wt,cast(SUM(CASE WHEN CAL_RATE IS NULL OR CAL_RATE = '' THEN 0 ELSE CAL_RATE END*divvy_basic_n)/'测试值'*'测试值' as decimal(12,2) ) amt FROM tcaai01 t1 left join tcaac09 t9 on t1.cost_center=t9.sub_backlog_code and t9.mat_code='测试值' WHERE 1=1;

-- [CHANGE-252] libCAAI/f_caai_ft.cpp L372-L380
-- 以下为写操作,执行前确认在测试环境!
insert into tcaai02 (REC_CREATE_TIME,dept_code,prod_date,sub_backlog_code,cost_center,stats_period,product_code,equ_no, sg_sign,prod_shift_group,prod_shift_no, mat_thick, mat_width,VFREE1,VFREE2,MAT_CODE,RULE_TYPE,DIVVY_TYPE,WT,AMT,key_seq) select '测试值',dept_code,prod_date,sub_backlog_code,sub_backlog_code,stats_period,product_code,equ_no, sg_sign,prod_shift_group,prod_shift_no, mat_thick, mat_width,VFREE1,VFREE2,MAT_CODE,'测试值','7',wt,amt,'ft'||trim('测试值')||trim('测试值') from ( SELECT t1.product_code,t1.DEPT_CODE, STATS_PERIOD, COST_CENTER, prod_date, prod_shift_group, prod_shift_no, t1.sub_backlog_code, equ_no, t1.sg_sign, t1.mat_thick, t1.mat_width,t1.VFREE1,t1.VFREE2,'测试值' mat_code,SUM(CASE WHEN CAL_RATE IS NULL OR CAL_RATE = '' THEN 0 ELSE CAL_RATE END*divvy_basic_n)/'测试值'*'测试值' as wt,SUM(CASE WHEN CAL_RATE IS NULL OR CAL_RATE = '' THEN 0 ELSE CAL_RATE END*divvy_basic_n)/'测试值'*'测试值' as amt FROM tcaai01 t1 left join tcaac09 t9 on t1.cost_center=t9.sub_backlog_code and t9.mat_code='测试值' WHERE 1=1;

-- [CHANGE-253] libCAAI/f_caai_ft.cpp L416-L422
AND t1.sub_backlog_code = '测试值' AND DIVVY_TYPE ='1' AND stats_period = '测试值' group by t1.product_code,t1.DEPT_CODE, STATS_PERIOD, COST_CENTER, prod_date, prod_shift_group, prod_shift_no, t1.sub_backlog_code, equ_no, t1.sg_sign, t1.mat_thick, t1.mat_width,t1.VFREE1,t1.VFREE2 HAVING SUM(CASE WHEN CAL_RATE IS NULL OR CAL_RATE = '' THEN 0 ELSE CAL_RATE END*divvy_basic_n)!=0 );

-- [CHANGE-254] libCAAI/f_caai_ny.cpp L130-L141
-- 以下为写操作,执行前确认在测试环境!
insert into tcaai01(REC_CREATE_TIME,dept_code, stats_period, cost_center, prod_date, prod_shift_group, prod_shift_no, sub_backlog_code, equ_no, sg_sign, mat_thick, mat_width, product_code, product_code_cname,divvy_type, divvy_basic_n ) SELECT '测试值', t1.DEPT_CODE, STATS_PERIOD, COST_CENTER, prod_date, prod_shift_group, prod_shift_no, t1.sub_backlog_code, equ_no, t1.sg_sign, t1.mat_thick, t1.mat_width,t1.MAT_CODE,t1.mat_name,'7',SUM(CASE WHEN CAL_RATE IS NULL OR CAL_RATE = '' THEN 0 ELSE CAL_RATE END*WT) FROM TCAAIS1 t1 left join tcaac09 t9 on t1.sg_sign = t9.sg_sign AND t1.mat_thick = t9.mat_thick AND t1.mat_width = t9.mat_width and t1.cost_center=t9.sub_backlog_code and t1.dept_code=t9.dept_code and t9.mat_code='测试值' WHERE 1=1 AND t1.sub_backlog_code = '测试值' AND PRO_FLAG ='O' AND stats_period = '测试值' group by t1.DEPT_CODE, STATS_PERIOD, COST_CENTER, prod_date, prod_shift_group, prod_shift_no, t1.sub_backlog_code, equ_no, t1.sg_sign, t1.mat_thick, t1.mat_width,t1.MAT_CODE,t1.mat_name HAVING SUM(CASE WHEN CAL_RATE IS NULL OR CAL_RATE = '' THEN 0 ELSE CAL_RATE END*WT)!=0;

-- [CHANGE-255] libCAAI/f_caai_rate.cpp L47-L52
-- 以下为写操作,执行前确认在测试环境!
delete from tcaai01 where 1=1 AND sub_backlog_code = CASE WHEN trim('测试值') IS NULL OR trim('测试值') = '' THEN sub_backlog_code ELSE '测试值' END and divvy_type = '1' and STATS_PERIOD = '测试值';

-- [CHANGE-256] libCAAI/f_caai_rate.cpp L74-L83
-- 以下为写操作,执行前确认在测试环境!
insert into tcaai01(REC_CREATE_TIME,dept_code, stats_period, cost_center, prod_date, prod_shift_group, prod_shift_no, sub_backlog_code, unit_code, sg_sign, mat_thick, mat_width, product_code, product_code_cname, divvy_type, divvy_basic_n ) SELECT '测试值', DEPT_CODE, STATS_PERIOD, COST_CENTER, prod_date, prod_shift_group, prod_shift_no, sub_backlog_code, equ_no, sg_sign, mat_thick, mat_width,MAT_CODE,mat_name,'1',SUM(WT) FROM TCAAIS1 WHERE 1=1 AND sub_backlog_code = CASE WHEN trim('测试值') IS NULL OR trim('测试值') = '' THEN sub_backlog_code ELSE '测试值' END AND PRO_FLAG ='O' AND stats_period = '测试值' group by DEPT_CODE, STATS_PERIOD, COST_CENTER, prod_date, prod_shift_group, prod_shift_no, sub_backlog_code, equ_no, sg_sign, mat_thick, mat_width,MAT_CODE,mat_name HAVING SUM(WT)!=0;

-- [CHANGE-257] libCAAI/f_caai_rate.cpp L108-L113
-- 以下为写操作,执行前确认在测试环境!
delete from tcaai01 where 1=1 AND sub_backlog_code = CASE WHEN trim('测试值') IS NULL OR trim('测试值') = '' THEN sub_backlog_code ELSE '测试值' END and divvy_type = '8' and STATS_PERIOD = '测试值';

-- [CHANGE-258] libCAAI/f_caai_rate.cpp L137-L148
-- 以下为写操作,执行前确认在测试环境!
insert into tcaai01(REC_CREATE_TIME,dept_code, stats_period, cost_center, prod_date, prod_shift_group, prod_shift_no, sub_backlog_code, unit_code, sg_sign, mat_thick, mat_width, product_code, product_code_cname, divvy_type, divvy_basic_n ) SELECT '测试值', DEPT_CODE, STATS_PERIOD, COST_CENTER, prod_time, prod_shift_group, prod_shift_no, sub_backlog_code, equ_no, sg_sign, mat_thick, mat_width,MAT_CODE,mat_name,'8',SUM(WT) from ( select DEPT_CODE, STATS_PERIOD, COST_CENTER, prod_time, prod_shift_group, prod_shift_no, sub_backlog_code, equ_no, sg_sign, mat_thick, mat_width,MAT_CODE,mat_name,2*mat_thick*mat_width+2*(mat_thick+mat_width)*mat_len WT FROM TCAAIA1 WHERE 1=1 AND sub_backlog_code = CASE WHEN trim('测试值') IS NULL OR trim('测试值') = '' THEN sub_backlog_code ELSE '测试值' END AND PRO_FLAG ='O' AND stats_period = '测试值' ) group by DEPT_CODE, STATS_PERIOD, COST_CENTER, prod_time, prod_shift_group, prod_shift_no, sub_backlog_code, equ_no, sg_sign, mat_thick, mat_width,MAT_CODE,mat_name HAVING SUM(WT)!=0;

-- [CHANGE-259] libCAAI/f_caai_rate.cpp L172-L178
-- 以下为写操作,执行前确认在测试环境!
delete from tcaai01 where 1=1 AND sub_backlog_code = CASE WHEN trim('测试值') IS NULL OR trim('测试值') = '' THEN sub_backlog_code ELSE '测试值' END and divvy_type = '9' and STATS_PERIOD = '测试值';

-- [CHANGE-260] libCAAI/f_caai_rate.cpp L202-L213
-- 以下为写操作,执行前确认在测试环境!
insert into tcaai01(REC_CREATE_TIME,dept_code, stats_period, cost_center, prod_date, prod_shift_group, prod_shift_no, sub_backlog_code, unit_code, sg_sign, mat_thick, mat_width, product_code, product_code_cname, divvy_type, divvy_basic_n ) SELECT '测试值', DEPT_CODE, STATS_PERIOD, COST_CENTER, prod_time, prod_shift_group, prod_shift_no, sub_backlog_code, equ_no, sg_sign, mat_thick, mat_width,MAT_CODE,mat_name,'9',SUM(WT) from ( select DEPT_CODE, STATS_PERIOD, COST_CENTER, prod_time, prod_shift_group, prod_shift_no, sub_backlog_code, equ_no, sg_sign, mat_thick, mat_width,MAT_CODE,mat_name,mat_len WT FROM TCAAIA1 WHERE 1=1 AND sub_backlog_code = CASE WHEN trim('测试值') IS NULL OR trim('测试值') = '' THEN sub_backlog_code ELSE '测试值' END AND PRO_FLAG ='O' AND stats_period = '测试值' ) group by DEPT_CODE, STATS_PERIOD, COST_CENTER, prod_time, prod_shift_group, prod_shift_no, sub_backlog_code, equ_no, sg_sign, mat_thick, mat_width,MAT_CODE,mat_name HAVING SUM(WT)!=0;

-- [CHANGE-261] libCAAI/f_caai_sj.cpp L88-L120
-- 以下为写操作,执行前确认在测试环境!
insert into tcaai02 (REC_CREATE_TIME,dept_code,cost_center,stats_period,RELATION_NO,product_code,MAT_CODE,RULE_TYPE,WT ,prod_date, prod_shift_group, prod_shift_no, sub_backlog_code, equ_no, sg_sign, mat_thick, mat_width, vfree1, vfree2, vfree3, vfree4, vfree5 ) select '测试值',dept_code,t1.cost_center,stats_period,t1.RELATION_NO,product_code,mat_code,'1',decode(all_wt,0,0,ROUND(WT*use_wt/all_wt,4)) ,prod_date, prod_shift_group, prod_shift_no, sub_backlog_code, equ_no, sg_sign, mat_thick, mat_width, vfree1, vfree2, vfree3, vfree4, vfree5 FROM (select dept_code, cost_center, stats_period, RELATION_NO, MAT_CODE product_code, SUM(QTY) QTY, SUM(WT) WT , prod_date, prod_shift_group, prod_shift_no, sub_backlog_code, equ_no, sg_sign, mat_thick, mat_width, vfree1, vfree2, vfree3, vfree4, vfree5 from tcaais1 where 1 = 1 AND PRO_FLAG = 'O' AND DEPT_CODE = '测试值' AND STATS_PERIOD = '测试值' group by dept_code, cost_center, stats_period, relation_no, MAT_CODE , prod_date, prod_shift_group, prod_shift_no, sub_backlog_code, equ_no, sg_sign, mat_thick, mat_width, vfree1, vfree2, vfree3, vfree4, vfree5 ) t1 left join (select cost_center, relation_no, SUM(WT) all_wt from tcaais1 where 1 = 1 AND PRO_FLAG = 'O' AND DEPT_CODE = '测试值' AND STATS_PERIOD = '测试值' GROUP BY cost_center, relation_no) t2 on t1.cost_center = t2.cost_center and t1.relation_no = t2.relation_no left join (select mat_code, cost_center, relation_no, sum(wt) use_wt from tcaais1 where 1 = 1 AND PRO_FLAG = 'I' AND DEPT_CODE = '测试值' AND STATS_PERIOD = '测试值' GROUP BY MAT_CODE, cost_center, relation_no) t3 on t1.cost_center = t3.cost_center and t1.relation_no = t3.relation_no where CASE WHEN mat_code IS NULL OR mat_code = '' THEN ' ' ELSE mat_code END != ' ';

-- [CHANGE-262] p_caac_3820/caaib1_ins.cpp L58-L64
select '测试值'||CASE WHEN key_seq IS NULL OR key_seq = '' THEN '000001' ELSE trim(to_char(to_number(nvl(key_seq,0))+1, '000000')) END from ( select max(substr(key_seq,length('测试值')+1,6)) key_seq from tcaaib1 where 1=1 and project_id = '测试值');

-- [CHANGE-263] p_caai_3840/caais2_ins.cpp L99-L107
select '测试值'||CASE WHEN key_seq IS NULL OR key_seq = '' THEN '00001' ELSE trim(to_char(to_number(nvl(key_seq,0))+1, '00000')) END from ( select max(substr(key_seq,length('测试值')+1,6)) key_seq from tcaais2 where 1=1 and data_from ='测试值' and sub_backlog_code = '测试值' and stats_period = '测试值');

-- [CHANGE-264] p_caai_3860/caai_ins_start.cpp L325-L330
select distinct sub_backlog_code,divvy_type from tcaais2 where 1=1 AND dept_code = CASE WHEN trim('测试值') IS NULL OR trim('测试值') = '' THEN sub_backlog_code ELSE '测试值' END and STATS_PERIOD = '测试值';

-- [CHANGE-265] p_caai_3860/caai_start.cpp L178-L183
select distinct sub_backlog_code,divvy_type from tcaais2 where 1=1 AND dept_code = CASE WHEN trim('测试值') IS NULL OR trim('测试值') = '' THEN sub_backlog_code ELSE '测试值' END and STATS_PERIOD = '测试值';

