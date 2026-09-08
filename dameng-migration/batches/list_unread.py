import csv, io, os
rows = [r for r in csv.DictReader(open(
    r'D:\work\company\太钢二炼钢\analysis\dameng-migration\sql-ledger.csv',
    encoding='utf-8-sig')) if r['decision'] == '已转换']
files = {}
for r in rows:
    key = (r['module'], r['path'])
    files.setdefault(key, []).append(r['sql_id'])

read_already = set()
for mod, paths in {
    'TMSM': ['p_tmsm_7110/tmsm11av_inq.cpp', 'p_tmsm_7120/tmsm53_ins.cpp',
             'p_tmsm_7160/tmsme59_inq.cpp', 'p_tmsm_7160/tmsme68a1_offline.cpp',
             'p_tmsm_7160/tmsme91a1_act.cpp', 'p_tmsm_7160/tmsme96_inq.cpp'],
    'QMTS': ['libQMTS/f_qmts_30_ins.cpp', 'libQMTS/f_qmts_spe_single.cpp',
             'libQMTS/f_qmts_spe_sm.cpp', 'p_qmts_4800/qmts0rdr_inq.cpp',
             'p_qmts_4850/cm_0rt805_rcv.cpp'],
    'PSSM': ['libPSSM/f_pssm11_planno_n.cpp', 'libPSSM/f_pssm12_save_job_n.cpp',
             'p_pssm_13030/pssm21_inq.cpp', 'p_pssm_13050/pssm10cllcf2_inq.cpp',
             'p_pssm_13050/pssm14f2_inq.cpp', 'p_pssm_13050/pssm14f2_inq2.cpp',
             'p_pssm_13060/mmlgap05_inq.cpp', 'p_pssm_13060/mmsmap05_inq.cpp',
             'p_pssm_13060/mmlgap08_inq.cpp', 'p_pssm_13060/pslgap03_bof_inq.cpp'],
    'FOSMT': ['p_fosmt_28180/fosm02_inq.cpp'],
    'MMSM': ['libMMSM/f_mmsm7101_proc.cpp', 'libMMSM/f_mmsm81.cpp',
             'libMMSM/f_mmsm_get_density.cpp', 'libMMSM/f_mmsm_gyupd.cpp',
             'p_mmsm_17520/mmsm01g2_inq.cpp', 'p_mmsm_17660/mmsmshdc_inq.cpp',
             'p_mmsm_17660/mmsmlcbgx_inq.cpp'],
    'CAAI': ['libCAAI/f_caai_rate.cpp', 'libCAAI/f_caai_ft.cpp',
             'p_caac_3820/caaib1_ins.cpp'],
    'WM00': ['libWM00/f_auto_sail.cpp'],
    'WM10': ['p_wm10_8630/wm11_inq.cpp'],
    'SM00': ['libSM00/f_sm00_plan_mat.cpp'],
    'TK00': ['p_tksm_12020/tksm12_inq.cpp'],
    'MMTP': ['libMMTP/f_mmtp_data_query.cpp'],
}.items():
    for p in paths:
        read_already.add((mod, p))

unread = {}
for (mod, path), ids in sorted(files.items()):
    if (mod, path) not in read_already:
        unread.setdefault(mod, []).append((path, len(ids)))

total = sum(len(v) for v in unread.values())
print(f'未逐个读过的转换文件: {total} 个')
for mod in sorted(unread):
    print(f'\n{mod} ({len(unread[mod])} 个):')
    for path, n in unread[mod]:
        print(f'  {path} ({n} 块)')

import json
groups = {
    'PSSM': [p for m, p in unread.get('PSSM', [])],
    'MMSM_A': [p for m, p in unread.get('MMSM', [])[:8]],
    'MMSM_B': [p for m, p in unread.get('MMSM', [])[8:]],
    'CAAI_WM00_WM10': ([p for m, p in unread.get('CAAI', [])] +
                       [p for m, p in unread.get('WM00', [])] +
                       [p for m, p in unread.get('WM10', [])]),
    'FOSMT_MMTP': ([p for m, p in unread.get('FOSMT', [])] +
                   [p for m, p in unread.get('MMTP', [])] +
                   [p for m, p in unread.get('SM00', [])] +
                   [p for m, p in unread.get('TK00', [])]),
}
with open(r'D:\work\company\太钢二炼钢\analysis\dameng-migration\batches\_unread_groups.json', 'w') as f:
    json.dump(groups, f, indent=2)
print('\nGroups written')
