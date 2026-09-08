# -*- coding: utf-8 -*-
# E2 追加:本次转换语句的 DM8 语法验证版本(变量以测试值代入)
import re, io

TS14 = "'20240904143000'"

def load(p):
    raw = open(p, 'rb').read()
    try:
        return raw.decode('utf-8')
    except UnicodeDecodeError:
        return raw.decode('gb18030')

def join_statement(lines):
    parts = []
    for l in lines:
        body = l.rstrip().rstrip(';')
        a, b = body.find('"'), body.rfind('"')
        if a < 0 or b <= a:
            continue
        parts.append(body[a+1:b])
    return ''.join(parts)

def get_active(path, change_id):
    lines = load(path).split('\n')
    h = next(i for i, l in enumerate(lines, 1) if ('DM8 适配 ' + change_id + ':') in l)
    m = next(i for i in range(h, len(lines)) if lines[i-1].strip() == '// DM8 SQL：')
    j = m + 1
    while lines[j-1].strip() == '':
        j += 1
    e = j
    while not lines[e-1].rstrip().endswith('";'):
        e += 1
    return join_statement(lines[j-1:e])

CONCAT = re.compile(r"'\s*\"\s*\+\s*(.*?)\s*\+\s*\"\s*'", re.S)

def to_e2(sql, mode):
    if mode in ('ts14', 'num'):
        tok = '120' if mode == 'num' else TS14
        sql = CONCAT.sub(tok, sql)
    if 'params' in mode:
        sql = (sql.replace('@datetime1', "'20250901000000'")
                  .replace('@datetime2', "'20250903000000'")
                  .replace('@v_date', "'20250901'")
                  .replace('@v_circle_1', "'测试值'")
                  .replace('@v_circle', "'测试值'"))
    return sql

JOBS = {
    'analysis/dameng-migration/e2-verify-tmsm.sql': [
        ('CHANGE-108', 'Server/TMSM/p_tmsm_7160/tmsme96_inq.cpp', 'ts14'),
        ('CHANGE-109', 'Server/TMSM/p_tmsm_7160/tmsme96_inq.cpp', 'num'),
        ('CHANGE-340', 'Server/TMSM/libTMSM/f_tmsm01_60106.cpp', 'ts14'),
    ] + [('CHANGE-%d' % n, 'Server/TMSM/p_tmsm_7160/tmsme96_inq.cpp', 'ts14') for n in range(346, 356)],
    'analysis/dameng-migration/e2-verify-mmsm.sql': [
        ('CHANGE-%d' % n, 'Server/MMSM/p_mmsm_17520/' + f, 'ts14')
        for n, f in [(163, 'mmsmis02_inq.cpp'), (164, 'mmsmis02_inqa.cpp'),
                     (165, 'mmsmis02a1_inq.cpp'), (166, 'mmsmis02a1_inq.cpp'),
                     (167, 'mmsmis02a1_inqa.cpp'), (168, 'mmsmis02a1_inqa.cpp')]
    ],
    'analysis/dameng-migration/e2-verify-wm00.sql': [
        ('CHANGE-234', 'Server/WM00/libWM00/f_create_crane_no.cpp', 'ts14'),
        ('CHANGE-235', 'Server/WM00/libWM00/f_wm00_pile_comf.cpp', 'params'),
        ('CHANGE-236', 'Server/WM00/libWM00/f_wm00_pile_comf.cpp', 'params'),
        ('CHANGE-237', 'Server/WM00/libWM00/f_wm00_pile_jud.cpp', 'ts14'),
        ('CHANGE-238', 'Server/WM00/libWM00/f_wm00_pile_jud.cpp', 'ts14'),
    ],
    'analysis/dameng-migration/e2-verify-pssm.sql': [
        ('CHANGE-138', 'Server/PSSM/p_pssm_13060/mmlgap07_inq.cpp', 'params'),
        ('CHANGE-148', 'Server/PSSM/p_pssm_13060/mmsmap07_inq.cpp', 'params'),
        ('CHANGE-141', 'Server/PSSM/p_pssm_13060/mmlgap09_inq.cpp', 'params'),
        ('CHANGE-150', 'Server/PSSM/p_pssm_13060/mmsmap09_inq.cpp', 'params'),
    ],
}

for e2file, items in JOBS.items():
    add = []
    for chg, src, mode in items:
        sql = to_e2(get_active(src, chg), mode)
        assert 'timestampdiff' not in sql.lower(), chg
        assert '"' not in sql, (chg, sql[:80])
        add.append('-- [%s] %s (2026-09-08 追加,HR 口径①,变量以测试值代入;未执行)' % (chg, src))
        add.append(sql + '\n')
    t = open(e2file, encoding='utf-8').read()
    m = re.search(r'-- 语句数:(\d+)', t)
    old_n = int(m.group(1))
    t = t.replace(m.group(0), '-- 语句数:%d;生成日期:2026-09-06,2026-09-08 追加 %d 条(HR 口径①落地)' % (old_n + len(items), len(items)), 1)
    t = t.rstrip() + '\n\n' + '\n'.join(add)
    open(e2file, 'w', encoding='utf-8', newline='').write(t)
    print('OK', e2file.split("/")[-1], '+%d' % len(items))

# mm00:两条 CASE 表达式验证(原语句为多段拼接,取表达式形态验证)
e2 = 'analysis/dameng-migration/e2-verify-mm00.sql'
t = open(e2, encoding='utf-8').read()
add = '''-- [CHANGE-356] p_mm00_18010/mm00su47a1_m.cpp (2026-09-08 追加,HR-006 口径①;原语句为多段拼接的查询列,此处以表达式形态验证语法)
SELECT CASE WHEN LENGTH(TRIM('20240904143000')) = 14 THEN TO_CHAR(DATEDIFF(SECOND, TO_DATE('20240904143000','YYYYMMDDHH24MISS'), CURRENT_TIMESTAMP) / 86400) ELSE '' END AS IN_STOCK_DURA, CASE WHEN LENGTH(TRIM('20240904143000')) = 14 THEN TO_CHAR(DATEDIFF(SECOND, TO_DATE('20240904143000','YYYYMMDDHH24MISS'), CURRENT_TIMESTAMP) / 3600) ELSE '' END AS IN_STOCK_HOUR FROM DUAL;
-- [CHANGE-357] p_mm00_18010/mm00su47a1_m.cpp (2026-09-08 追加,HR-006 口径①)
SELECT CASE WHEN LENGTH(TRIM('20240904143000')) = 14 THEN TO_CHAR(DATEDIFF(SECOND, TO_DATE('20240904143000','YYYYMMDDHH24MISS'), CURRENT_TIMESTAMP) / 86400) ELSE '' END AS ROLL_TIME_DURA, CASE WHEN LENGTH(TRIM('20240904143000')) = 14 THEN TO_CHAR(DATEDIFF(SECOND, TO_DATE('20240904143000','YYYYMMDDHH24MISS'), CURRENT_TIMESTAMP) / 3600) ELSE '' END AS ROLL_TIME_HOUR FROM DUAL;
'''
m = re.search(r'-- 语句数:(\d+)', t)
t = t.replace(m.group(0), '-- 语句数:%d;生成日期:2026-09-06,2026-09-08 追加 2 条(HR 口径①落地)' % (int(m.group(1)) + 2), 1)
t = t.rstrip() + '\n\n' + add
open(e2, 'w', encoding='utf-8', newline='').write(t)
print('OK e2-verify-mm00.sql +2')
