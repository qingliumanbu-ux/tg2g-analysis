# -*- coding: utf-8 -*-
# WM00 剩余: f_wm00_pile_jud (CHANGE-237+238) 与 f_wm00_pile_comf (CHANGE-235+236)
import hashlib, shutil

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

_R = [
    '// 改写原因：DB2 两参数 TIMESTAMPDIFF(8=小时,当前时间减切断时间=板坯冷却小时数) 在 DM8 无对应写法,按 HR-002 确认口径①(实际完整时长)',
    '//   改为 DATEDIFF(SECOND,起点=切断时间,终点=当前时间)/3600,整数除法与 DB2 截断行为一致。',
    '//   时间值为 14 位 YYYYMMDDHH24MISS(HR-001 已确认),原 to_date(x,\'yyyy-mm-dd hh24:mi:ss\') 格式串与值不匹配,改为 TO_TIMESTAMP(x,\'YYYYMMDDHH24MISS\'),外层 TIMESTAMP() 包装一并去除;',
    '//   SYSIBM 辅助表改为 DUAL;依据 DM 官方文档,DM8 尚未实测。',
]

def finish(path, t2, crlf, enc, tag, allow_residue=0):
    lines = t2.split('\n')
    residue = [l for l in lines if 'timestampdiff' in l.lower() and not l.strip().startswith('//') and '原程序' not in l]
    assert len(residue) == allow_residue, (tag, residue)
    if crlf:
        t2 = t2.replace('\n', '\r\n')
    save(path, t2, enc)
    print('OK', tag, hashlib.sha256(open(path, 'rb').read()).hexdigest()[:16])

# ============ f_wm00_pile_jud: CHANGE-237 + 238 ============
p = 'Server/WM00/libWM00/f_wm00_pile_jud.cpp'
shutil.copyfile(p, 'analysis/dameng-migration/batches/tsdiff-f_wm00_pile_jud.cpp.bak')
t, enc, crlf = load(p)
t2 = t.replace('\r\n', '\n')

edits = [
    ('// DM8 适配 CHANGE-237:查询。SYSIBM 辅助表改为 DUAL。',
     '// DM8 适配 CHANGE-237:查询板坯冷却时间(当前时间-切断时间,小时),写入 slab_cold_time 做冷热要求判断。'),
    ('// DM8 适配 CHANGE-237:查询。SYSIBM 辅助表改为 DUAL。', None),  # 238 first line: same text, handle second occurrence after first replaced
]
# 237 first
assert t2.count('// DM8 适配 CHANGE-237:查询。SYSIBM 辅助表改为 DUAL。') == 1
t2 = t2.replace('// DM8 适配 CHANGE-237:查询。SYSIBM 辅助表改为 DUAL。',
                '// DM8 适配 CHANGE-237:查询板坯冷却时间(当前时间-切断时间,小时),写入 slab_cold_time 做冷热要求判断。', 1)
assert t2.count('// DM8 适配 CHANGE-238:查询。SYSIBM 辅助表改为 DUAL。') == 1
t2 = t2.replace('// DM8 适配 CHANGE-238:查询。SYSIBM 辅助表改为 DUAL。',
                '// DM8 适配 CHANGE-238:查询最大冷却时间(当前时间-垛内最早切断时间,小时),写入 v_max_cold_time。', 1)
# reasons: two occurrences of same text; replace 237's first, then 238's
_o_reason = '// 改写原因：SYSIBM 辅助表改为 DUAL；依据 DM 官方文档,DM8 尚未实测。'
assert t2.count(_o_reason) >= 2, t2.count(_o_reason)
t2 = t2.replace(_o_reason, '\n'.join(_R), 1)          # 237 (first occurrence)
i = t2.find(_o_reason)                                 # next remaining = 238
assert i >= 0
t2 = t2[:i] + '\n'.join(_R) + t2[i + len(_o_reason):]

_o237a = '\t\t\tsqlstr = "SELECT timestampdiff(8, CHAR(TIMESTAMP(to_date(\'" + dateNow14 + "\', \'yyyy-mm-dd hh24:mi:ss\')) - TIMESTAMP(to_date(\'" + tmmsm01.SLAB_CUT_TIME + "\', \'yyyy-mm-dd hh24:mi:ss\')))) AS diffTimes16"'
_n237a = '\t\t\tsqlstr = "SELECT DATEDIFF(SECOND, TO_TIMESTAMP(\'" + tmmsm01.SLAB_CUT_TIME + "\',\'YYYYMMDDHH24MISS\'), TO_TIMESTAMP(\'" + dateNow14 + "\',\'YYYYMMDDHH24MISS\')) / 3600 AS diffTimes16"'
_o237b = '\t\t\t\t" FROM DUAL";'
_o238a = '\t\t\t\t\t\tsqlstr = "SELECT timestampdiff(8, CHAR(TIMESTAMP(to_date(\'" + dateNow14 + "\', \'yyyy-mm-dd hh24:mi:ss\')) - TIMESTAMP(to_date(\'" + v_cut_time_min + "\', \'yyyy-mm-dd hh24:mi:ss\')))) AS diffTimes16"'
_n238a = '\t\t\t\t\t\tsqlstr = "SELECT DATEDIFF(SECOND, TO_TIMESTAMP(\'" + v_cut_time_min + "\',\'YYYYMMDDHH24MISS\'), TO_TIMESTAMP(\'" + dateNow14 + "\',\'YYYYMMDDHH24MISS\')) / 3600 AS diffTimes16"'
_o238b = '\t\t\t\t\t\t\t" FROM DUAL";'
for oa, nm in [(_o237a, '237a'), (_o237b, '237b'), (_o238a, '238a'), (_o238b, '238b')]:
    assert oa in t2, nm + ' not found'
t2 = t2.replace(_o237a, _n237a, 1)
# 237b/238b 的 " FROM DUAL"; 行内容不变,无需替换(同文行在其他已转换语句中也存在,只校验 238b 行存在)
assert t2.count(_o238b) >= 1
t2 = t2.replace(_o238a, _n238a, 1)
finish(p, t2, crlf, enc, 'CHANGE-237+238')

# ============ f_wm00_pile_comf: CHANGE-235 + 236 ============
p = 'Server/WM00/libWM00/f_wm00_pile_comf.cpp'
shutil.copyfile(p, 'analysis/dameng-migration/batches/tsdiff-f_wm00_pile_comf.cpp.bak')
t, enc, crlf = load(p)
t2 = t.replace('\r\n', '\n')

n_r235 = '\n'.join([
    '// 改写原因：DB2 两参数 TIMESTAMPDIFF(4=分钟,垛位 24 小时内使用过) 在 DM8 无对应写法,按 HR-002 确认口径①(实际完整时长)',
    '//   改为 DATEDIFF(SECOND,起点=FIELDNO_UPTIME,终点=当前时间)/60 <= 24*60,整数除法与 DB2 截断行为一致。',
    '//   FIELDNO_UPTIME 按原程序注释为字符型时间,用 TO_DATE(FIELDNO_UPTIME,\'YYYY-MM-DD HH24:MI:SS\') 显式转换;',
    '//   当前时点沿用 CURRENT_TIMESTAMP(DM 官方函数手册支持);依据 DM 官方文档,DM8 尚未实测。',
])
_o_r = '// 改写原因：DB2 特殊寄存器 current date/time/timestamp 改为 DM 的 CURRENT_DATE/CURRENT_TIME/CURRENT_TIMESTAMP(官方函数手册支持)；依据 DM 官方文档,DM8 尚未实测。'
assert t2.count(_o_r) == 2, t2.count(_o_r)
t2 = t2.replace('// DM8 适配 CHANGE-235:查询。见改写原因。',
                '// DM8 适配 CHANGE-235:查询 24 小时内使用过的垛位集(STOCK_PLACE_NO),供 D1 循环推荐。', 1)
t2 = t2.replace(_o_r, n_r235, 1)
i = t2.find(_o_r)
assert i >= 0
t2 = t2[:i] + n_r235 + t2[i + len(_o_r):]

_o_a235 = '\t\t\t" AND timestampdiff(4, char(CURRENT_TIMESTAMP - timestamp(FIELDNO_UPTIME))) <= 24 * 60 "/*原程序current timestamp - TO_DATE(FIELDNO_UPTIME,\'YYYY-MM-DD HH24:MI:SS\') <= 24*60*60*/'
_n_a235 = '\t\t\t" AND DATEDIFF(SECOND, TO_DATE(FIELDNO_UPTIME, \'YYYY-MM-DD HH24:MI:SS\'), CURRENT_TIMESTAMP) / 60 <= 24 * 60 "/*原程序current timestamp - TO_DATE(FIELDNO_UPTIME,\'YYYY-MM-DD HH24:MI:SS\') <= 24*60*60*/'
_o_a236 = '\t\t\t\t" AND timestampdiff(4, char(CURRENT_TIMESTAMP - timestamp(FIELDNO_UPTIME))) <= 24 * 60"'
_n_a236 = '\t\t\t\t" AND DATEDIFF(SECOND, TO_DATE(FIELDNO_UPTIME, \'YYYY-MM-DD HH24:MI:SS\'), CURRENT_TIMESTAMP) / 60 <= 24 * 60"'
for x, nm in [(_o_a235, '235a'), (_o_a236, '236a')]:
    assert x in t2, nm + ' not found'
t2 = t2.replace(_o_a235, _n_a235, 1)
t2 = t2.replace(_o_a236, _n_a236, 1)
finish(p, t2, crlf, enc, 'CHANGE-235+236')
print('WM00 REST DONE')
