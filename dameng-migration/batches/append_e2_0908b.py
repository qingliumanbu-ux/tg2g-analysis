# -*- coding: utf-8 -*-
# E2 追加 v2:行级精确变量替换,再拼接
import re

TS = "'20240904143000'"

def load(p):
    raw = open(p, 'rb').read()
    try:
        return raw.decode('utf-8')
    except UnicodeDecodeError:
        return raw.decode('gb18030')

def get_active_lines(path, change_id):
    lines = load(path).split('\n')
    h = next(i for i, l in enumerate(lines, 1) if ('DM8 适配 ' + change_id + ':') in l)
    m = next(i for i in range(h, len(lines)) if lines[i-1].strip() == '// DM8 SQL：')
    j = m + 1
    while lines[j-1].strip() == '':
        j += 1
    e = j
    while not lines[e-1].rstrip().endswith('";'):
        e += 1
    return lines[j-1:e]

def join_statement(lines):
    parts = []
    for l in lines:
        body = l.rstrip().rstrip(';')
        a, b = body.find('"'), body.rfind('"')
        if a < 0 or b <= a:
            continue
        parts.append(body[a+1:b])
    return ''.join(parts)

def subst_vars(lines, exprs, mode):
    out = []
    tok = '120' if mode == 'num' else TS
    for l in lines:
        for e in exprs:
            l = re.sub(r"'\s*\"\s*\+\s*" + re.escape(e) + r'\s*\+\s*"\s*\'', tok, l)
            l = re.sub(r'"\s*\+\s*' + re.escape(e) + r'\s*\+\s*"', tok, l)
        out.append(l)
    return out

def to_e2(path, chg, exprs=(), mode='ts14', params=False):
    lines = get_active_lines(path, chg)
    lines = subst_vars(lines, exprs, mode)
    sql = join_statement(lines)
    if exprs:
        assert '+' not in re.sub(r"'[^']*'", '', sql), (chg, sql[:120])  # 引号外不得残留 C++ 拼接
    if params:
        sql = (sql.replace('@datetime1', "'20250901000000'")
                  .replace('@datetime2', "'20250903000000'")
                  .replace('@v_date', "'20250901'")
                  .replace('@v_circle_1', "'测试值'")
                  .replace('@v_circle', "'测试值'"))
    assert 'timestampdiff' not in sql.lower(), chg
    assert '@' not in sql, (chg, sql[:80])
    return sql

T96 = 'Server/TMSM/p_tmsm_7160/tmsme96_inq.cpp'
_CH = ['ttmsm66["REC_CREATE_TIME"].ToString()', 'ttmsm66["CHANGE_TIME"].ToString()']
_ES = ['dt_temp.Rows[j]["END_TIME"].ToString().Trim()', 'dt_temp.Rows[j]["START_TIME"].ToString().Trim()']
_JOBS = {
    'analysis/dameng-migration/e2-verify-tmsm.sql': [
        ('CHANGE-108', T96, _CH, 'ts14', False),
        ('CHANGE-109', T96, ['use_time.ToString()', 'all_time.ToString()', 'repair_time.ToString()'], 'num', False),
        ('CHANGE-340', 'Server/TMSM/libTMSM/f_tmsm01_60106.cpp', ['datetime', 'usage_st'], 'ts14', False),
    ] + [('CHANGE-%d' % n, T96,
          _CH if n in (346, 347) else
          (['dt_temp.Rows[j]["E_DATETIME"].ToString().Trim()', 'dt_temp.Rows[j]["S_DATETIME"].ToString().Trim()'] if n == 355 else _ES),
          'ts14', False) for n in range(346, 356)],
    'analysis/dameng-migration/e2-verify-mmsm.sql': [
        ('CHANGE-163', 'Server/MMSM/p_mmsm_17520/mmsmis02_inq.cpp',
         ['v_in_stock_hot_time', 'v_slab_cut_time'], 'ts14', False),
        ('CHANGE-164', 'Server/MMSM/p_mmsm_17520/mmsmis02_inqa.cpp',
         ['v_in_stock_hot_time', 'v_slab_cut_time'], 'ts14', False),
        ('CHANGE-165', 'Server/MMSM/p_mmsm_17520/mmsmis02a1_inq.cpp', ['v_slab_cut_time'], 'ts14', False),
        ('CHANGE-166', 'Server/MMSM/p_mmsm_17520/mmsmis02a1_inq.cpp',
         ['v_in_stock_hot_time', 'v_slab_cut_time'], 'ts14', False),
        ('CHANGE-167', 'Server/MMSM/p_mmsm_17520/mmsmis02a1_inqa.cpp', ['v_slab_cut_time'], 'ts14', False),
        ('CHANGE-168', 'Server/MMSM/p_mmsm_17520/mmsmis02a1_inqa.cpp',
         ['v_in_stock_hot_time', 'v_slab_cut_time'], 'ts14', False),
    ],
    'analysis/dameng-migration/e2-verify-wm00.sql': [
        ('CHANGE-234', 'Server/WM00/libWM00/f_create_crane_no.cpp',
         ['dateNow14', 'tmmsm01["SLAB_CUT_TIME"].ToString()'], 'ts14', False),
        ('CHANGE-235', 'Server/WM00/libWM00/f_wm00_pile_comf.cpp', [], 'ts14', True),
        ('CHANGE-236', 'Server/WM00/libWM00/f_wm00_pile_comf.cpp', [], 'ts14', True),
        ('CHANGE-237', 'Server/WM00/libWM00/f_wm00_pile_jud.cpp',
         ['dateNow14', 'tmmsm01.SLAB_CUT_TIME'], 'ts14', False),
        ('CHANGE-238', 'Server/WM00/libWM00/f_wm00_pile_jud.cpp',
         ['dateNow14', 'v_cut_time_min'], 'ts14', False),
    ],
    'analysis/dameng-migration/e2-verify-pssm.sql': [
        ('CHANGE-138', 'Server/PSSM/p_pssm_13060/mmlgap07_inq.cpp', [], 'ts14', True),
        ('CHANGE-148', 'Server/PSSM/p_pssm_13060/mmsmap07_inq.cpp', [], 'ts14', True),
        ('CHANGE-141', 'Server/PSSM/p_pssm_13060/mmlgap09_inq.cpp', [], 'ts14', True),
        ('CHANGE-150', 'Server/PSSM/p_pssm_13060/mmsmap09_inq.cpp', [], 'ts14', True),
    ],
}

# 清掉此前运行可能写入的残段(从追加标记行开始截断)
MARK = '-- [CHANGE-'
for e2file, items in _JOBS.items():
    t = open(e2file, encoding='utf-8').read()
    first_add = min(t.find('-- [%s] ' % c) for c, *_ in items if t.find('-- [%s] ' % c) >= 0) if any(t.find('-- [%s] ' % c) >= 0 for c, *_ in items) else -1
    if first_add >= 0:
        t = t[:first_add].rstrip()
        m = re.search(r'-- 语句数:(\d+)', t)
        t = t.replace(m.group(0), '-- 语句数:%d;生成日期:2026-09-06,2026-09-08 追加 %d 条(HR 口径①落地)' % (int(m.group(1)) + len(items), len(items)), 1)
    add = []
    for chg, src, exprs, mode, params in items:
        sql = to_e2(src, chg, exprs, mode, params)
        assert '"' not in sql, (chg, sql[:100])
        add.append('-- [%s] %s (2026-09-08 追加,HR 口径①,变量以测试值代入;未执行)' % (chg, src))
        add.append(sql + '\n')
    t = t.rstrip() + '\n\n' + '\n'.join(add)
    open(e2file, 'w', encoding='utf-8', newline='').write(t)
    print('OK', e2file.split("/")[-1], '+%d' % len(items))
