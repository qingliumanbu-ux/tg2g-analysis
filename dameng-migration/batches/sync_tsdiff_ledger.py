# -*- coding: utf-8 -*-
# 同步:台账 31 行 + 待人工清单落地说明 + 批次记录 + E2 追加
import csv, hashlib, io, re, os

# ---------- 已转换映射: sql_id -> (文件, 关键词) ----------
FILES = {
    'f_tmsm01': 'Server/TMSM/libTMSM/f_tmsm01_60106.cpp',
    'tmsme96': 'Server/TMSM/p_tmsm_7160/tmsme96_inq.cpp',
    'mmsmis02_inq': 'Server/MMSM/p_mmsm_17520/mmsmis02_inq.cpp',
    'mmsmis02_inqa': 'Server/MMSM/p_mmsm_17520/mmsmis02_inqa.cpp',
    'mmsmis02a1_inq': 'Server/MMSM/p_mmsm_17520/mmsmis02a1_inq.cpp',
    'mmsmis02a1_inqa': 'Server/MMSM/p_mmsm_17520/mmsmis02a1_inqa.cpp',
    'f_create_crane_no': 'Server/WM00/libWM00/f_create_crane_no.cpp',
    'f_wm00_pile_comf': 'Server/WM00/libWM00/f_wm00_pile_comf.cpp',
    'f_wm00_pile_jud': 'Server/WM00/libWM00/f_wm00_pile_jud.cpp',
    'mm00su47a1_m': 'Server/MM00/p_mm00_18010/mm00su47a1_m.cpp',
    'mmlgap07_inq': 'Server/PSSM/p_pssm_13060/mmlgap07_inq.cpp',
    'mmsmap07_inq': 'Server/PSSM/p_pssm_13060/mmsmap07_inq.cpp',
    'mmlgap09_inq': 'Server/PSSM/p_pssm_13060/mmlgap09_inq.cpp',
    'mmsmap09_inq': 'Server/PSSM/p_pssm_13060/mmsmap09_inq.cpp',
    'f_pssm27_upd_plno_n': 'Server/PSSM/libPSSM/f_pssm27_upd_plno_n.cpp',
}
shas = {}
texts = {}
for k, p in FILES.items():
    raw = open(p, 'rb').read()
    try:
        t = raw.decode('utf-8')
    except UnicodeDecodeError:
        t = raw.decode('gb18030')
    texts[k] = t
    shas[k] = hashlib.sha256(raw).hexdigest()

def block_range(key, change_no):
    """返回 (头行, 原SQL注释起, 原SQL注释止, 活动起, 活动止) 1-based"""
    lines = texts[key].split('\n')
    h = next(i for i, l in enumerate(lines, 1) if ('DM8 适配 ' + change_no + ':') in l)
    o = next(i for i in range(h, len(lines)) if '原 SQL（完整保留）' in lines[i-1])
    m = next(i for i in range(o, len(lines)) if lines[i-1].strip() == '// DM8 SQL：')
    # 活动语句:标记后第一条非空非注释行到 "; 结束
    j = m + 1
    while j < len(lines) and (lines[j-1].strip() == '' or lines[j-1].strip().startswith('//')):
        j += 1
    e = j
    while not lines[e-1].rstrip().endswith('";'):
        e += 1
    return h, o, m - 1, j, e

ROWS = []
def add(sql_id, key, chg, note):
    h, o, oe, a, ae = block_range(key, chg)
    ROWS.append((sql_id, key, note, f'L{h}-L{ae}', f'L{o}-L{oe}', f'L{a}-L{ae}'))

# TMSM
add('CHANGE-340', 'f_tmsm01', 'CHANGE-340', '已转换(钢包盛钢时长分钟,HR-004口径①,见CHANGE-340)')
add('CHANGE-108', 'tmsme96', 'CHANGE-108', '已转换(DAYS→DATEDIFF(DAY);此前转换曾丢失,2026-09-08 重做)')
for n in range(346, 356):
    add('CHANGE-%d' % n, 'tmsme96', 'CHANGE-%d' % n, '已转换(时长口径①,HR-004;此前转换曾丢失,2026-09-08 重做)')
add('CHANGE-109', 'tmsme96', 'CHANGE-109', '已转换(SYSIBM→DUAL 汇总语句;此前转换曾丢失,2026-09-08 重做)')
# MMSM
add('CHANGE-163', 'mmsmis02_inq', 'CHANGE-163', '已转换(切断到热装小时差,HR-006口径①)')
add('CHANGE-164', 'mmsmis02_inqa', 'CHANGE-164', '已转换(切断到热装小时差,HR-006口径①)')
add('CHANGE-165', 'mmsmis02a1_inq', 'CHANGE-165', '已转换(当前-切断在库小时数,HR-006口径①)')
add('CHANGE-166', 'mmsmis02a1_inq', 'CHANGE-166', '已转换(切断到热装小时数,HR-006口径①)')
add('CHANGE-167', 'mmsmis02a1_inqa', 'CHANGE-167', '已转换(当前-切断在库小时数,HR-006口径①)')
add('CHANGE-168', 'mmsmis02a1_inqa', 'CHANGE-168', '已转换(切断到热装小时数,HR-006口径①)')
# WM00
add('CHANGE-234', 'f_create_crane_no', 'CHANGE-234', '已转换(板坯冷却小时数,HR-006口径①)')
add('CHANGE-235', 'f_wm00_pile_comf', 'CHANGE-235', '已转换(垛位24小时内使用,HR-006口径①)')
add('CHANGE-236', 'f_wm00_pile_comf', 'CHANGE-236', '已转换(辅助垛位24小时内使用,HR-006口径①)')
add('CHANGE-237', 'f_wm00_pile_jud', 'CHANGE-237', '已转换(板坯冷却时间,HR-006口径①)')
add('CHANGE-238', 'f_wm00_pile_jud', 'CHANGE-238', '已转换(最大冷却时间,HR-006口径①)')
# MM00
add('CHANGE-356', 'mm00su47a1_m', 'CHANGE-356', '已转换(在库/产出天数与小时数,HR-006口径①)')
add('CHANGE-357', 'mm00su47a1_m', 'CHANGE-357', '已转换(轧制时间天数与小时数,HR-006口径①)')
# PSSM
add('CHANGE-138', 'mmlgap07_inq', 'CHANGE-138', '已转换(累计作业率天数分母,HR-006口径①)')
add('CHANGE-148', 'mmsmap07_inq', 'CHANGE-148', '已转换(累计作业率天数分母,HR-006口径①)')
add('CHANGE-141', 'mmlgap09_inq', 'CHANGE-141', '已转换(38处秒/分钟/天时长,HR-006口径①;381叠加块并入本块)')
add('CHANGE-150', 'mmsmap09_inq', 'CHANGE-150', '已转换(38处秒/分钟/天时长,HR-006口径①)')
add('CHANGE-381', 'mmlgap09_inq', 'CHANGE-141', '已转换(SYSIBM→DUAL;注释块已并入 CHANGE-141 同一块,原始SQL以本块为准)')

# ---------- 台账更新 ----------
LP = 'analysis/dameng-migration/sql-ledger.csv'
rows = list(csv.DictReader(open(LP, encoding='utf-8-sig')))
fields = list(rows[0].keys())
upd = 0
for r in rows:
    for (sql_id, key, note, anchor, oanchor, aanchor) in ROWS:
        if r['sql_id'] == sql_id:
            r['anchor'] = anchor
            r['original_comment_anchor'] = oanchor
            r['active_sql_anchor'] = aanchor
            r['decision'] = '已转换'
            r['status'] = note
            if 'HR-003' in sql_id:
                pass
            r['runtime_status'] = '未执行'
            r['current_file_sha256'] = shas[key]
            upd += 1
# HR-003 行的哈希已是最新,补刷新
for r in rows:
    if r['sql_id'] == 'KEEP-f_pssm27_upd_plno_n-02':
        r['current_file_sha256'] = shas['f_pssm27_upd_plno_n']
        upd += 1
assert upd == len(ROWS) + 1, (upd, len(ROWS))
with open(LP, 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(rows)
print('ledger updated rows =', upd)

# ---------- 状态统计 ----------
cnt = {}
for r in rows:
    st = '已转换' if r['status'].startswith('已转换') else ('可保留' if r['status'].startswith('可保留') else ('待人工' if '待人工' in r['status'] else '其他'))
    cnt[st] = cnt.get(st, 0) + 1
print(cnt)
