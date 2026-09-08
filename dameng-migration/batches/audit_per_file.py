# -*- coding: utf-8 -*-
"""逐文件核对:<模块> 全部 .cpp。
A. 语句块提取(内容驱动)与台账对账;
B. 方言复扫(排除挂起/注释/CAST AS INT 误报);
C. 锚点有效性(支持单行锚点);
D. 无台账文件甄别(真 SQL vs 无 SQL/死代码)。
"""
import csv, io, os, re, sys
sys.path.insert(0, r'D:\work\company\太钢二炼钢\analysis\dameng-migration\batches\wmsm')
import dm8lib

MOD = sys.argv[1] if len(sys.argv) > 1 else 'QMTS'
dm8lib.set_module(MOD)
rows = [r for r in csv.DictReader(io.open(dm8lib.LEDGER, encoding='utf-8-sig', newline=''))
        if r['module'] == MOD]
by_file = {}
for r in rows:
    by_file.setdefault(r['path'], []).append(r)

CONV = re.compile(
    r'SYSIBM\.|SYSTABLES|SYSCOLUMNS|nextval\s+for|(?<![.\w])value\s*\('
    r'|\bSUBSTR2\s*\(|\bPOSSTR\s*\(|INTERVAL\s+\x27|\d+\s+HOURS?\b'
    r'|\bcurrent\s+(?:date|timestamp|schema)\b|\bDAYS\s*\('
    r'|-\s*\d+\s+DAYS?\b|\+\s*\d+\s+DAYS?\b', re.I)
HR_PAT = re.compile(r'TIMESTAMPDIFF', re.I)
ANCHOR = re.compile(r'^L(\d+)(?:-L(\d+))?$', re.I)
NOSQL = re.compile(r'^\s*CString\s+\w+\s*(=\s*[^"]*;\s*$|;)')  # 纯声明
REAL = re.compile(r'=\s*"[^"]*(?:\bselect\b|\binsert\s+into\b|\bupdate\b|\bdelete\s+from\b)'
                  r'|"\s*(?:select|insert\s+into|update|delete\s+from)\b', re.I)

problems = []
n_files = n_blocks = n_rows = 0
for dp, dn, fn in os.walk(dm8lib.ROOT):
    if '.git' in dn:
        dn.remove('.git')
    for f in sorted(fn):
        if not f.lower().endswith('.cpp'):
            continue
        p = os.path.join(dp, f)
        rel = os.path.relpath(p, dm8lib.ROOT).replace(os.sep, '/')
        n_files += 1
        raw = open(p, 'rb').read()
        try:
            text = raw.decode('utf-8')
        except UnicodeDecodeError:
            text = raw.decode('gb18030', errors='replace')
        lines = text.split('\n')
        blocks = dm8lib.find_blocks(lines)
        n_blocks += len(blocks)
        lrows = by_file.get(rel, [])
        n_rows += len(lrows)
        status = []
        conv_left = []
        for (s, e, ap) in blocks:
            blk = '\n'.join(lines[s:e + 1])
            if HR_PAT.search(blk):
                continue
            if NOSQL.match(blk.strip()):
                continue
            m = CONV.search(blk)
            if m:
                conv_left.append((s + 1, m.group(0)))
        bad_anchor = 0
        for r in lrows:
            m = ANCHOR.match(r['anchor'])
            if not m:
                bad_anchor += 1
                continue
            e_line = int(m.group(2) or m.group(1))
            if e_line > len(lines):
                bad_anchor += 1
        if blocks and not lrows:
            real = False
            for (s, e, ap) in blocks:
                joined = ' '.join(lines[s:e + 1])
                if dm8lib.SQL_KEYWORD.search(joined):
                    real = True
                    break
            if real:
                status.append('有块无台账')
        if conv_left:
            status.append('可转换残留')
        if bad_anchor:
            status.append(f'锚点异常{bad_anchor}')
        if status:
            problems.append((rel, ' '.join(status),
                             '; '.join(f'L{x} [{w}]' for x, w in conv_left)[:100]))

print(f'{MOD}: files={n_files} blocks={n_blocks} ledger_rows={n_rows}')
print('problems:', len(problems))
for p2 in problems:
    print('  ', p2[0], '|', p2[1], '|', p2[2])
