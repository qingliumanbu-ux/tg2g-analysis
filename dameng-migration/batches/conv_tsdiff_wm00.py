# -*- coding: utf-8 -*-
# WM00: HR-002 口径① 落地,两参数 TIMESTAMPDIFF -> DATEDIFF(SECOND,起点,终点)/因子
import hashlib, shutil, os

def load(p):
    raw = open(p, 'rb').read()
    for enc in ('utf-8', 'gb18030'):
        try:
            return raw.decode(enc), enc, (b'\r\n' in raw)
        except UnicodeDecodeError:
            continue
    raise RuntimeError('decode fail: ' + p)

def save(p, t, enc):
    open(p, 'wb').write(t.encode(enc))

# f_create_crane_no (CHANGE-234)
_o234a = '\t\t\tsqlstr = "SELECT timestampdiff(8, CHAR(TIMESTAMP(to_date(\'" + dateNow14 + "\', \'yyyy-mm-dd hh24:mi:ss\')) - TIMESTAMP(to_date(\'" + tmmsm01["SLAB_CUT_TIME"].ToString() + "\', \'yyyy-mm-dd hh24:mi:ss\')))) AS diffTimes16"'
_o234b = '\t\t\t\t" FROM DUAL";'
_n234a = '\t\t\tsqlstr = "SELECT DATEDIFF(SECOND, TO_TIMESTAMP(\'" + tmmsm01["SLAB_CUT_TIME"].ToString() + "\',\'YYYYMMDDHH24MISS\'), TO_TIMESTAMP(\'" + dateNow14 + "\',\'YYYYMMDDHH24MISS\')) / 3600 AS diffTimes16"'
_n234b = '\t\t\t\t" FROM DUAL";'

# f_wm00_pile_jud (CHANGE-237)
_o237a = '\t\t\tsqlstr = "SELECT timestampdiff(8, CHAR(TIMESTAMP(to_date(\'" + dateNow14 + "\', \'yyyy-mm-dd hh24:mi:ss\')) - TIMESTAMP(to_date(\'" + tmmsm01.SLAB_CUT_TIME + "\', \'yyyy-mm-dd hh24:mi:ss\')))) AS diffTimes16"'
_o237b = '\t\t\t\t" FROM DUAL";'
_n237a = '\t\t\tsqlstr = "SELECT DATEDIFF(SECOND, TO_TIMESTAMP(\'" + tmmsm01.SLAB_CUT_TIME + "\',\'YYYYMMDDHH24MISS\'), TO_TIMESTAMP(\'" + dateNow14 + "\',\'YYYYMMDDHH24MISS\')) / 3600 AS diffTimes16"'
_n237b = '\t\t\t\t" FROM DUAL";'

# f_wm00_pile_jud (CHANGE-238)
_o238a = '\t\t\t\t\t\tsqlstr = "SELECT timestampdiff(8, CHAR(TIMESTAMP(to_date(\'" + dateNow14 + "\', \'yyyy-mm-dd hh24:mi:ss\')) - TIMESTAMP(to_date(\'" + v_cut_time_min + "\', \'yyyy-mm-dd hh24:mi:ss\')))) AS diffTimes16"'
_o238b = '\t\t\t\t\t\t\t" FROM DUAL";'
_n238a = '\t\t\t\t\t\tsqlstr = "SELECT DATEDIFF(SECOND, TO_TIMESTAMP(\'" + v_cut_time_min + "\',\'YYYYMMDDHH24MISS\'), TO_TIMESTAMP(\'" + dateNow14 + "\',\'YYYYMMDDHH24MISS\')) / 3600 AS diffTimes16"'
_n238b = '\t\t\t\t\t\t\t" FROM DUAL";'

_R234 = [
    '// 改写原因：DB2 两参数 TIMESTAMPDIFF(8=小时,当前时间减切断时间=板坯冷却小时数) 在 DM8 无对应写法,按 HR-002 确认口径①(实际完整时长)',
    '//   改为 DATEDIFF(SECOND,起点=切断时间,终点=当前时间)/3600,整数除法与 DB2 截断行为一致。',
    '//   时间值为 14 位 YYYYMMDDHH24MISS(HR-001 已确认),原 to_date(x,\'yyyy-mm-dd hh24:mi:ss\') 格式串与值不匹配,改为 TO_TIMESTAMP(x,\'YYYYMMDDHH24MISS\'),外层 TIMESTAMP() 包装一并去除;',
    '//   SYSIBM 辅助表改为 DUAL;依据 DM 官方文档,DM8 尚未实测。',
]

def one_block(path, first_old, first_new, reason_old, reason_new, pairs, tag):
    t, enc, crlf = load(path)
    t2 = t.replace('\r\n', '\n')
    assert first_old in t2, tag + ': first not found'
    t2 = t2.replace(first_old, first_new, 1)
    assert reason_old in t2, tag + ': reason not found'
    t2 = t2.replace(reason_old, '\n'.join(reason_new), 1)
    for oa, na in pairs:
        assert oa in t2, tag + ': old active not found: ' + oa[:70]
        t2 = t2.replace(oa, na, 1)
    lines = t2.split('\n')
    residue = [l for l in lines if 'timestampdiff' in l.lower() and not l.strip().startswith('//')
               and '原程序' not in l]
    assert not residue, (tag, residue)
    for na, _ in pairs:
        assert na.count('(') == na.count(')'), tag + ': paren imbalance'
    if crlf:
        t2 = t2.replace('\n', '\r\n')
    save(path, t2, enc)
    print('OK', tag, hashlib.sha256(open(path, 'rb').read()).hexdigest()[:16])

# ---- f_create_crane_no (CHANGE-234) ----
p = 'Server/WM00/libWM00/f_create_crane_no.cpp'
shutil.copyfile(p, 'analysis/dameng-migration/batches/tsdiff-f_create_crane_no.cpp.bak')
one_block(p,
    '// DM8 适配 CHANGE-234:查询。SYSIBM 辅助表改为 DUAL。',
    '// DM8 适配 CHANGE-234:查询板坯冷却小时数(diffTimes16),与垛位 COLD_HOT_REQ 冷却要求比较。',
    '// 改写原因：SYSIBM 辅助表改为 DUAL；依据 DM 官方文档,DM8 尚未实测。',
    _R234,
    [(_o234a, _n234a), (_o234b, _n234b)],
    'CHANGE-234')

# ---- f_wm00_pile_jud (CHANGE-237) ----
p = 'Server/WM00/libWM00/f_wm00_pile_jud.cpp'
shutil.copyfile(p, 'analysis/dameng-migration/batches/tsdiff-f_wm00_pile_jud.cpp.bak')
one_block(p,
    '// DM8 适配 CHANGE-237:查询。SYSIBM 辅助表改为 DUAL。',
    '// DM8 适配 CHANGE-237:查询板坯冷却时间(当前时间-切断时间,小时),写入 slab_cold_time 做冷热要求判断。',
    '// 改写原因：SYSIBM 辅助表改为 DUAL；依据 DM 官方文档,DM8 尚未实测。',
    _R234,
    [(_o237a, _n237a), (_o237b, _n237b)],
    'CHANGE-237')

# ---- f_wm00_pile_jud (CHANGE-238) 追加在同一文件 ----
t, enc, crlf = load(p)
t2 = t.replace('\r\n', '\n')
o_first = '// DM8 适配 CHANGE-238:查询。SYSIBM 辅助表改为 DUAL。'
n_first = '// DM8 适配 CHANGE-238:查询最大冷却时间(当前时间-垛内最早切断时间,小时),写入 v_max_cold_time。'
assert o_first in t2, 'CHANGE-238 first not found'
t2 = t2.replace(o_first, n_first, 1)
o_reason = '// 改写原因：SYSIBM 辅助表改为 DUAL；依据 DM 官方文档,DM8 尚未实测。'
assert o_reason in t2, 'CHANGE-238 reason not found'
t2 = t2.replace(o_reason, '\n'.join(_R234), 1)
assert _o238a in t2, 'CHANGE-238 active not found'
t2 = t2.replace(_o238a, _n238a, 1)
assert _o238b in t2, 'CHANGE-238 active-b not found'
t2 = t2.replace(_o238b, _n238b, 1)
lines = t2.split('\n')
residue = [l for l in lines if 'timestampdiff' in l.lower() and not l.strip().startswith('//') and '原程序' not in l]
assert not residue, ('CHANGE-238 residue', residue)
if crlf:
    t2 = t2.replace('\n', '\r\n')
save(p, t2, enc)
print('OK CHANGE-238', hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16])

# ---- f_wm00_pile_comf (CHANGE-235 / 236) ----
p = 'Server/WM00/libWM00/f_wm00_pile_comf.cpp'
shutil.copyfile(p, 'analysis/dameng-migration/batches/tsdiff-f_wm00_pile_comf.cpp.bak')
t, enc, crlf = load(p)
t2 = t.replace('\r\n', '\n')

o_f235 = '// DM8 适配 CHANGE-235:查询。见改写原因。'
n_f235 = '// DM8 适配 CHANGE-235:查询 24 小时内使用过的垛位集(STOCK_PLACE_NO),供 D1 循环推荐。'
o_r235 = '// 改写原因：DB2 特殊寄存器 current date/time/timestamp 改为 DM 的 CURRENT_DATE/CURRENT_TIME/CURRENT_TIMESTAMP(官方函数手册支持)；依据 DM 官方文档,DM8 尚未实测。'
n_r235 = '\n'.join([
    '// 改写原因：DB2 两参数 TIMESTAMPDIFF(4=分钟,垛位 24 小时内使用过) 在 DM8 无对应写法,按 HR-002 确认口径①(实际完整时长)',
    '//   改为 DATEDIFF(SECOND,起点=FIELDNO_UPTIME,终点=当前时间)/60 <= 24*60,整数除法与 DB2 截断行为一致。',
    '//   FIELDNO_UPTIME 按原程序注释为字符型时间,用 TO_DATE(FIELDNO_UPTIME,\'YYYY-MM-DD HH24:MI:SS\') 显式转换;',
    '//   当前时点沿用 CURRENT_TIMESTAMP(DM 官方函数手册支持);依据 DM 官方文档,DM8 尚未实测。',
])
o_a235 = '\t\t\t" AND timestampdiff(4, char(CURRENT_TIMESTAMP - timestamp(FIELDNO_UPTIME))) <= 24 * 60 "/*原程序current timestamp - TO_DATE(FIELDNO_UPTIME,\'YYYY-MM-DD HH24:MI:SS\') <= 24*60*60*/'
n_a235 = '\t\t\t" AND DATEDIFF(SECOND, TO_DATE(FIELDNO_UPTIME, \'YYYY-MM-DD HH24:MI:SS\'), CURRENT_TIMESTAMP) / 60 <= 24 * 60 "/*原程序current timestamp - TO_DATE(FIELDNO_UPTIME,\'YYYY-MM-DD HH24:MI:SS\') <= 24*60*60*/'

o_f236 = '// DM8 适配 CHANGE-236:查询。见改写原因。'
n_f236 = '// DM8 适配 CHANGE-236:查询 24 小时内使用过的辅助垛位(FIELDNO=\'9\',STORE_AREA=\'1\',PRE_MAT_NUM=0)。'
o_a236 = '\t\t\t\t" AND timestampdiff(4, char(CURRENT_TIMESTAMP - timestamp(FIELDNO_UPTIME))) <= 24 * 60"'
n_a236 = '\t\t\t\t" AND DATEDIFF(SECOND, TO_DATE(FIELDNO_UPTIME, \'YYYY-MM-DD HH24:MI:SS\'), CURRENT_TIMESTAMP) / 60 <= 24 * 60"'

for x, nm in [(o_f235, '235-first'), (o_r235, '235-reason'), (o_a235, '235-active'),
              (o_f236, '236-first'), (o_a236, '236-active')]:
    assert x in t2, nm + ' not found'
t2 = t2.replace(o_f235, n_f235, 1)
t2 = t2.replace(o_r235, n_r235, 1)
t2 = t2.replace(o_a235, n_a235, 1)
t2 = t2.replace(o_f236, n_f236, 1)
# CHANGE-236 的改写原因行与 235 相同文本,替换第二处
i = t2.find(o_r235)
assert i >= 0, '236 reason not found'
t2 = t2[:i] + n_r235 + t2[i + len(o_r235):]
lines = t2.split('\n')
residue = [l for l in lines if 'timestampdiff' in l.lower() and not l.strip().startswith('//') and '原程序' not in l]
assert not residue, ('pile_comf residue', residue)
if crlf:
    t2 = t2.replace('\n', '\r\n')
save(p, t2, enc)
print('OK CHANGE-235/236', hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16])
print('WM00 ALL DONE')
