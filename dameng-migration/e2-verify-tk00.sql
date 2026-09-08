-- TK00 E2 验证脚本(自动生成,需在 DM8 环境执行)
-- 语句数:2;生成日期:2026-09-06
-- 注意:仅验证语法可执行性(SELECT 返回列/类型),不验证结果等价性
-- 期望结果:全部语句编译通过,SELECT 语句返回结果集

-- [CHANGE-269] p_tksm_12020/tksm12_inq.cpp L78-L85
and prod_time<='测试值' and prod_time>='测试值' group by st_no union all select st_no,sum(prod_wt) prod_wt,sum(CO2_WT) CO2_WT,CASE WHEN trim('测试值') IS NULL OR trim('测试值') = '' THEN ' ' ELSE '其他' END equ_no,CASE WHEN trim('测试值') IS NULL OR trim('测试值') = '' THEN ' ' ELSE '其他' END gx_div,decode(sum(prod_wt),0,0,round(sum(CO2_WT)/sum(PROD_WT),6)) CO2_WT_UNIT from ttksm01 where 1=1;

-- [CHANGE-270] p_tksm_12020/tksm12_inq.cpp L156-L163
and prod_time<='测试值' and prod_time>='测试值' group by st_no union all select sum(prod_wt) prod_wt,sum(CO2_WT) CO2_WT,CASE WHEN trim('测试值') IS NULL OR trim('测试值') = '' THEN ' ' ELSE '其他' END equ_no,CASE WHEN trim('测试值') IS NULL OR trim('测试值') = '' THEN ' ' ELSE '其他' END gx_div,decode(sum(prod_wt),0,0,round(sum(CO2_WT)/sum(PROD_WT),6)) CO2_WT_UNIT from ttksm01 where 1=1;

