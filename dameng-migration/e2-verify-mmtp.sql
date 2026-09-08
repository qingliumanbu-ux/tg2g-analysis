-- MMTP E2 验证脚本(自动生成,需在 DM8 环境执行)
-- 语句数:3;生成日期:2026-09-06
-- 注意:仅验证语法可执行性(SELECT 返回列/类型),不验证结果等价性
-- 期望结果:全部语句编译通过,SELECT 语句返回结果集

-- [CHANGE-271] libMMTP/f_mmtp_data_query.cpp L378-L378
FROM DUAL;

-- [CHANGE-275] p_mmtp_18030/mmtp_loadQuery.cpp L559-L560
SELECT remarks FROM SYSIBM.SYSTABLES WHERE name = '' AND creator = (SELECT CURRENT_SCHEMA FROM DUAL);

-- [CHANGE-360] libMMTP/f_mmtp_mat_track.cpp L989-L990
SELECT length FROM sysibm.syscolumns WHERE tbname ='' AND name = '' AND tbcreator = (SELECT CURRENT_SCHEMA FROM DUAL);

