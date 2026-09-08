-- GCTP E2 验证脚本(自动生成,需在 DM8 环境执行)
-- 语句数:1;生成日期:2026-09-06
-- 注意:仅验证语法可执行性(SELECT 返回列/类型),不验证结果等价性
-- 期望结果:全部语句编译通过,SELECT 语句返回结果集

-- [CHANGE-361] libGCTP/f_gctp_getTableItem.cpp L109-L110
SELECT remarks FROM SYSIBM.SYSTABLES WHERE name = '' AND creator = (SELECT CURRENT_SCHEMA FROM DUAL);

