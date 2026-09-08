-- WM10 E2 验证脚本(自动生成,需在 DM8 环境执行)
-- 语句数:6;生成日期:2026-09-06
-- 注意:仅验证语法可执行性(SELECT 返回列/类型),不验证结果等价性
-- 期望结果:全部语句编译通过,SELECT 语句返回结果集

-- [CHANGE-335] p_wm10_8630/wm11_inq.cpp L110-L110
SELECT table_name FROM ALL_TABLES WHERE table_name IN( 'TMMCR01','TMMHR01','TMMSM01','TMMHP01','TMMBW01');

-- [CHANGE-336] p_wm10_8630/wm12_inq.cpp L110-L110
SELECT table_name FROM ALL_TABLES WHERE table_name IN( 'TMMCR01','TMMHR01','TMMSM01','TMMHP01','TMMBW01');

-- [CHANGE-337] p_wm10_8630/wm17_inq.cpp L110-L110
SELECT table_name FROM ALL_TABLES WHERE table_name IN( 'TMMCR01','TMMHR01','TMMSM01','TMMHP01','TMMBW01');

-- [CHANGE-338] p_wm10_8630/wma2_inq.cpp L110-L110
SELECT table_name FROM ALL_TABLES WHERE table_name IN( 'TMMCR01','TMMHR01','TMMSM01','TMMHP01','TMMBW01');

-- [CHANGE-273] libWM10/f_wmhrhr_crane_make.cpp L205-L205
values seqTest.NEXTVAL;

-- [CHANGE-274] libWM10/f_wmhrhr_crane_make.cpp L655-L655
values seqTest.NEXTVAL;

