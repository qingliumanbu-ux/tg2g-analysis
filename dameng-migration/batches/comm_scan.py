# -*- coding: utf-8 -*-
# 周边系统通讯证据扫描:snd/rcv 全量盘点 + 配置文件 + 归档成员 + 中文对端系统关键词
import os, re, io, json

WS = 'D:/work/company/太钢二炼钢'
OUT = WS + '/analysis/dameng-migration/batches'

# ---------- 1) snd/rcv 全量盘点 ----------
rows = []
for root, dirs, files in os.walk(WS + '/Server'):
    dirs[:] = [d for d in dirs if d != '.git']
    for fn in files:
        if not fn.lower().endswith('.cpp'):
            continue
        low = fn.lower()
        if 'snd' not in low and 'rcv' not in low:
            continue
        p = os.path.join(root, fn)
        raw = open(p, 'rb').read()
        try:
            t = raw.decode('utf-8')
        except UnicodeDecodeError:
            t = raw.decode('gb18030', errors='replace')
        m = re.search(r'Description[:：]\s*(.+)', t)
        desc = m.group(1).strip() if m else ''
        tcs = set(re.findall(r'tc_?no\s*=\s*"([A-Za-z0-9_]{2,12})"', t, re.I))
        entry = 'TELE' if 'BM2F_ENTERACE_TELE' in t else ''
        direction = 'snd' if 'snd' in low else 'rcv'
        module = os.path.normpath(p).replace(os.sep, '/').split('/Server/')[1].split('/')[0]
        rows.append((module, fn, direction, desc[:70], ';'.join(sorted(tcs))[:44], entry))

rows.sort()
with io.open(OUT + '/comm_snd_rcv_inventory.tsv', 'w', encoding='utf-8') as out:
    out.write('模块\t程序\t方向\t描述\t电文号\t电文入口\n')
    for r in rows:
        out.write('\t'.join(str(x) for x in r) + '\n')

mods = {}
for m, fn, d, desc, tc, e in rows:
    a = mods.setdefault(m, [0, 0, 0])
    a[0] += 1
    if d == 'snd':
        a[1] += 1
    else:
        a[2] += 1
print('snd/rcv total', len(rows), {m: '共%d(发%d/收%d)' % tuple(a) for m, a in sorted(mods.items())})
teles = sum(1 for r in rows if r[5] == 'TELE')
print('BM2F_ENTERACE_TELE entries:', teles, '/', len(rows))

# ---------- 2) 中文对端系统关键词(全部 cpp,注释+字符串) ----------
PEERS = ['二级', 'L2', '三级', 'L3', '四级', 'L4', 'ERP', 'SAP', '计量', '检化验', '化验', '天车', '吊运',
         '行车', '能源', 'EMS', '薄板', '热轧', '冷轧', '连铸', '铁区', '烧结', '焦化', '南区', '北区',
         '运输', '铁路', '销售', '采购', '财务', '备件', '设备管理', '动电', '水处理', '除尘', '煤气回收',
         '调度', 'XCOM', 'MES', 'PES', 'MMS', 'NEMO', 'LIMS', 'MESG', 'BM2']
hits = {}
for root, dirs, files in os.walk(WS + '/Server'):
    dirs[:] = [d for d in dirs if d != '.git']
    for fn in files:
        if not fn.lower().endswith('.cpp'):
            continue
        p = os.path.join(root, fn)
        raw = open(p, 'rb').read()
        try:
            t = raw.decode('utf-8')
        except UnicodeDecodeError:
            t = raw.decode('gb18030', errors='replace')
        # 只看注释行与 Description 行(对端系统通常写在注释里)
        for i, l in enumerate(t.split('\n'), 1):
            s = l.strip()
            if not (s.startswith('//') or s.startswith('*') or s.startswith('/*') or 'Description' in s):
                continue
            for kw in ['二级', '四级', 'L2', 'L4', 'ERP', 'SAP', '计量', '检化验', '化验', '天车', '吊运',
                       '行车', '能源', '薄板', '热轧', '连铸', '铁区', '烧结', '焦化', '运输', '调度', 'XCOM']:
                if kw in s:
                    hits.setdefault(kw, []).append((os.path.normpath(p).replace(os.sep, '/').split('Server/')[1], i, s[:110]))
with io.open(OUT + '/comm_peer_evidence.tsv', 'w', encoding='utf-8') as out:
    out.write('关键词\t文件\t行\t内容\n')
    for kw, lst in sorted(hits.items(), key=lambda x: -len(x[1])):
        for f, i, s in lst[:40]:
            out.write(f'{kw}\t{f}\t{i}\t{s}\n')
print('peer keyword files:', {k: len(v) for k, v in sorted(hits.items(), key=lambda x: -len(x[1]))})

# ---------- 3) 归档成员 ----------
d = json.load(open(WS + '/analysis/database-workspace/archives.json', encoding='utf-8'))
members = d.get('members', [])
names = []
for m in members:
    n = m.get('member_name') or m.get('name') or ''
    names.append((m.get('archive') or m.get('archive_name') or '', n))
with io.open(OUT + '/comm_archive_members.txt', 'w', encoding='utf-8') as out:
    for a, n in names:
        out.write(f'{a}\t{n}\n')
print('archive members:', len(names))
# 打印疑似接口/通讯文档
for a, n in names:
    nl = str(n).lower()
    if any(k in nl for k in ['接口', '通讯', '电文', 'xcom', 'interface', 'comm', 'l2', 'l4', '对外']):
        print('  ARCHIVE-HIT:', a, n)
