# -*- coding: utf-8 -*-
# MM00 mm00su47a1_m.cpp CHANGE-356/357:大 SQL 内 6 处 TIMESTAMPDIFF 表达式(16=天/8=小时)
import hashlib, shutil, re

P = 'Server/MM00/p_mm00_18010/mm00su47a1_m.cpp'
BAK = 'analysis/dameng-migration/batches/tsdiff-mm00su47a1_m.cpp.bak'
shutil.copyfile(P, BAK)
raw = open(P, 'rb').read()
t = raw.decode('gb18030')
t2 = t.replace('\r\n', '\n')

R = '\n'.join([
    '// 改写原因：DB2 两参数 TIMESTAMPDIFF(16=天/8=小时,系统当前时间减产出/入库时间) 在 DM8 无对应写法,按 HR-006 确认口径①(实际完整时长)',
    '//   改为 DATEDIFF(SECOND,起点=TO_DATE(时间列),终点=CURRENT_TIMESTAMP)/86400(天)或/3600(小时),整数除法与 DB2 截断行为一致;外层 TO_CHAR 保留;',
    '//   DB2 时长转字符的内层 TO_CHAR 包装随 TIMESTAMPDIFF 一并去除;当前时点沿用 CURRENT_TIMESTAMP(官方函数手册支持);依据 DM 官方文档,DM8 尚未实测。',
])
_o_reason = '// 改写原因：DB2 特殊寄存器 current date/time/timestamp/schema 改为 DM 的 CURRENT_DATE/CURRENT_TIME/CURRENT_TIMESTAMP/CURRENT_SCHEMA(官方函数手册支持)；依据 DM 官方文档,DM8 尚未实测。'
assert t2.count(_o_reason) == 2, t2.count(_o_reason)

pairs = [
    ('// DM8 适配 CHANGE-356:查询。见改写原因。',
     '// DM8 适配 CHANGE-356:计算在库/产出时间的天数与小时数(IN_STOCK_DURA/IN_STOCK_HOUR/IN_STOCK_TIME_DURA/IN_STOCK_TIME_HOUR)。'),
    ('// DM8 适配 CHANGE-357:查询。见改写原因。',
     '// DM8 适配 CHANGE-357:计算热卷轧制时间的天数与小时数(ROLL_TIME_DURA/ROLL_TIME_HOUR,系统当前时间-卷曲时间)。'),
]
for o, n in pairs:
    assert t2.count(o) == 1, (o, t2.count(o))
    t2 = t2.replace(o, n, 1)

# 两条 reason 行相同文本:各替换一次(第一处 356,第二处 357)
t2 = t2.replace(_o_reason, R, 1)
i = t2.find(_o_reason)
assert i >= 0
t2 = t2[:i] + R + t2[i + len(_o_reason):]

reps = [
    ('"THEN TO_CHAR(TIMESTAMPDIFF(16,TO_CHAR(CURRENT_TIMESTAMP-TO_DATE(t1.SLAB_CUT_TIME,\'YYYYMMDDHH24MISS\') ))) "',
     '"THEN TO_CHAR(DATEDIFF(SECOND, TO_DATE(t1.SLAB_CUT_TIME,\'YYYYMMDDHH24MISS\'), CURRENT_TIMESTAMP) / 86400) "'),
    ('"THEN TO_CHAR(TIMESTAMPDIFF(8,TO_CHAR(CURRENT_TIMESTAMP-TO_DATE(t1.SLAB_CUT_TIME,\'YYYYMMDDHH24MISS\') ))) "',
     '"THEN TO_CHAR(DATEDIFF(SECOND, TO_DATE(t1.SLAB_CUT_TIME,\'YYYYMMDDHH24MISS\'), CURRENT_TIMESTAMP) / 3600) "'),
    ('"THEN TO_CHAR(TIMESTAMPDIFF(16,TO_CHAR(CURRENT_TIMESTAMP-TO_DATE(t1.IN_STOCK_TIME,\'YYYYMMDDHH24MISS\') ))) "',
     '"THEN TO_CHAR(DATEDIFF(SECOND, TO_DATE(t1.IN_STOCK_TIME,\'YYYYMMDDHH24MISS\'), CURRENT_TIMESTAMP) / 86400) "'),
    ('"THEN TO_CHAR(TIMESTAMPDIFF(8,TO_CHAR(CURRENT_TIMESTAMP-TO_DATE(t1.IN_STOCK_TIME,\'YYYYMMDDHH24MISS\') ))) "',
     '"THEN TO_CHAR(DATEDIFF(SECOND, TO_DATE(t1.IN_STOCK_TIME,\'YYYYMMDDHH24MISS\'), CURRENT_TIMESTAMP) / 3600) "'),
    ('"THEN TO_CHAR(TIMESTAMPDIFF(16,TO_CHAR(CURRENT_TIMESTAMP-TO_DATE(t1.COILED_TIME,\'YYYYMMDDHH24MISS\') ))) "',
     '"THEN TO_CHAR(DATEDIFF(SECOND, TO_DATE(t1.COILED_TIME,\'YYYYMMDDHH24MISS\'), CURRENT_TIMESTAMP) / 86400) "'),
    ('"THEN TO_CHAR(TIMESTAMPDIFF(8,TO_CHAR(CURRENT_TIMESTAMP-TO_DATE(t1.COILED_TIME,\'YYYYMMDDHH24MISS\') ))) "',
     '"THEN TO_CHAR(DATEDIFF(SECOND, TO_DATE(t1.COILED_TIME,\'YYYYMMDDHH24MISS\'), CURRENT_TIMESTAMP) / 3600) "'),
]
for o, n in reps:
    assert t2.count(o) == 1, (o[:60], t2.count(o))
    t2 = t2.replace(o, n, 1)

# 断言
cl = t2.split('\n')
res = [l for l in cl if not l.strip().startswith('//') and 'TIMESTAMPDIFF' in l.upper()]
assert not res, res
for l in cl:
    if 'DATEDIFF' in l and not l.strip().startswith('//'):
        assert l.count('(') == l.count(')'), l
assert 'CURRENT TIMESTAMP' in t2  # 原 SQL 注释里的 DB2 原文仍在
if b'\r\n' in open(P, 'rb').read():
    t2 = t2.replace('\n', '\r\n')
open(P, 'wb').write(t2.encode('gb18030'))
print('OK mm00su47a1 CHANGE-356/357 sha256=' + hashlib.sha256(open(P, 'rb').read()).hexdigest()[:16])
