# -*- coding: utf-8 -*-
# PSSM 4 文件:大聚合语句中两参数 TIMESTAMPDIFF -> DATEDIFF(SECOND,起点,终点)/因子 (HR-006 口径①)
# mmlgap09 需合并叠加的 CHANGE-381/141 注释块(381 块内为含 SYSIBM 的真原始 SQL)
import hashlib, re, shutil

FAC = {'2': None, '4': '60', '8': '3600', '16': '86400'}

def load(p):
    raw = open(p, 'rb').read()
    for enc in ('utf-8', 'gb18030'):
        try:
            return raw.decode(enc), enc, (b'\r\n' in raw)
        except UnicodeDecodeError:
            continue
    raise RuntimeError('decode fail: ' + p)

def find_calls(sql):
    """[(start, end, fac, X, Y)]; end=闭括号后一位;引号内跳过"""
    calls = []
    i = 0
    low = sql.lower()
    while True:
        j = low.find('timestampdiff(', i)
        if j < 0:
            break
        k = j + len('timestampdiff(')
        m = re.match(r'\s*(\d+)\s*,', sql[k:])
        assert m, 'no factor: ' + sql[j:j+60]
        fac = m.group(1)
        assert fac in FAC, fac
        depth, q, in_q = 1, k + m.end(), False
        while depth > 0:
            c = sql[q]
            if in_q:
                if c == "'":
                    in_q = False
            elif c == "'":
                in_q = True
            elif c == '(':
                depth += 1
            elif c == ')':
                depth -= 1
            q += 1
        body = sql[k + m.end():q-1]
        d, in_q, minus, other = 1, False, None, 0
        for x, c in enumerate(body):
            if in_q:
                if c == "'":
                    in_q = False
                continue
            if c == "'":
                in_q = True
            elif c == '(':
                d += 1
            elif c == ')':
                d -= 1
            elif d == 1 and c == '-' and minus is None:
                minus = x
            elif d == 1 and c in '+-*/':
                other += 1
        assert minus is not None, 'no top-level minus: ' + sql[j:q][:120]
        assert other == 0, 'multi top-level terms: ' + sql[j:q][:160]
        calls.append((j, q, fac, body[:minus].strip(), body[minus+1:].strip()))
        i = q
    return calls

def transform(sql):
    calls = find_calls(sql)
    out, prev = [], 0
    for (s, e, fac, X, Y) in calls:
        out.append(sql[prev:s])
        div = '' if FAC[fac] is None else ' / ' + FAC[fac]
        out.append('(DATEDIFF(SECOND, ' + Y + ', ' + X + ')' + div + ')')
        prev = e
    out.append(sql[prev:])
    return ''.join(out), calls

def remainder_after_datediff(sql):
    """去掉所有 (DATEDIFF(SECOND, ...) 顶层括号 span 后的剩余文本"""
    out, prev = [], 0
    i = 0
    n = 0
    while True:
        j = sql.find('(DATEDIFF(SECOND, ', i)
        if j < 0:
            break
        depth, q, in_q = 0, j, False
        while True:
            c = sql[q]
            if in_q:
                if c == "'":
                    in_q = False
            elif c == "'":
                in_q = True
            elif c == '(':
                depth += 1
            elif c == ')':
                depth -= 1
                if depth == 0:
                    q += 1
                    break
            q += 1
        out.append(sql[prev:j])
        prev = q
        i = q
        n += 1
    out.append(sql[prev:])
    return ''.join(out), n

def split_lines(sql, first_prefix, cont_prefix, width=120):
    chunks = []
    pos = 0
    while len(sql) - pos > width:
        cut = sql.rfind(' ', pos, pos + width)
        if cut <= pos:
            cut = pos + width
        else:
            cut += 1
        chunks.append(sql[pos:cut])
        pos = cut
    chunks.append(sql[pos:])
    lines = []
    for k, c in enumerate(chunks):
        tail = '";' if k == len(chunks) - 1 else '"'
        pref = first_prefix if k == 0 else cont_prefix
        lines.append(pref + '"' + c + tail)
    return lines

def join_statement(lines):
    parts = []
    for l in lines:
        body = l.rstrip().rstrip(';')
        a, b = body.find('"'), body.rfind('"')
        if a < 0 or b <= a:
            continue  # 空 "//" 分隔行等无片段行
        content = body[a+1:b]
        assert '"' not in content, l[:80]
        parts.append(content)
    return ''.join(parts)

def count_calls(sql):
    return len(re.findall(r'timestampdiff\s*\(\s*\d+\s*,', sql, re.I))

def process(path, bak, change_no, new_header, new_reason_lines, delete_change=None):
    t, enc, crlf = load(path)
    shutil.copyfile(path, bak)
    assert not crlf, 'unexpected CRLF'
    lines = t.split('\n')

    # 1) 合并叠加块:删除 delete_change 的整块(头行 -> 它自己的 // DM8 SQL： 标记)
    if delete_change:
        s = next(i for i, l in enumerate(lines) if l.strip().startswith('// DM8 适配 ' + delete_change + ':'))
        e = next(i for i in range(s + 1, len(lines)) if lines[i].strip() == '// DM8 SQL：')
        del lines[s:e + 1]

    # 2) 更新块头(按编号定位头行与紧随的改写原因行)
    h = next(i for i, l in enumerate(lines) if l.strip().startswith('// DM8 适配 ' + change_no + ':'))
    assert '原 SQL' not in lines[h + 2], 'unexpected block layout'
    lines[h] = new_header
    lines[h + 1:h + 2] = new_reason_lines

    # 3) 定位含 timestampdiff 的活动语句:扫描每个 // DM8 SQL： 标记
    target = None
    for i, l in enumerate(lines):
        if l.strip() != '// DM8 SQL：':
            continue
        j = i + 1
        while j < len(lines) and lines[j].strip() == '':
            j += 1
        if j >= len(lines) or not re.match(r'\s*sqlstr\w*\s*=', lines[j]):
            continue  # 孤立标记(无活动语句)
        e = j
        while not lines[e].rstrip().endswith('";'):
            e += 1
            assert e < len(lines) and not lines[e].strip().startswith('// DM8 适配'), 'terminator not found'
        act = lines[j:e + 1]
        if 'timestampdiff' in ''.join(act).lower():
            assert target is None, 'multiple active tsd statements'
            target = (i, j, e)
    assert target, 'no active statement with timestampdiff'
    mi, s, e = target

    # 4) 原 SQL 注释段的调用数须与活动语句一致
    k = next(i for i in range(mi, 0, -1) if lines[i].strip().startswith('// 原 SQL（完整保留）'))
    orig = join_statement([re.sub(r'^\s*//\s?', '', lines[x]) for x in range(k + 1, mi)])
    joined = join_statement(lines[s:e + 1])
    n_active = count_calls(joined)
    n_orig = count_calls(orig)
    assert n_active == n_orig and n_active > 0, (n_active, n_orig)

    # 5) 变换 + 等价性断言
    new_sql, calls = transform(joined)
    rem_new, n_dd = remainder_after_datediff(new_sql)
    rem_old, _, _ = '', None, None
    segs, prev = [], 0
    for (st, en, f, X, Y) in calls:
        segs.append(joined[prev:st])
        prev = en
    segs.append(joined[prev:])
    assert rem_new == ''.join(segs), 'residual text mismatch'
    assert n_dd == n_active

    # 6) 重排行并写回
    lead = lines[s][:len(lines[s]) - len(lines[s].lstrip())]
    new_lines = split_lines(new_sql, lead + 'sqlstr = ', lead + '\t')
    lines[s:e + 1] = new_lines
    open(path, 'wb').write('\n'.join(lines).encode(enc))

    # 7) 写后断言
    chk = open(path, 'rb').read().decode(enc)
    res = [l for l in chk.split('\n') if not l.strip().startswith('//') and 'timestampdiff' in l.lower()]
    assert not res, res
    print('OK', path.split("/")[-1], 'calls=', n_active, 'sha256=' + hashlib.sha256(open(path, 'rb').read()).hexdigest()[:16])
    return n_active

_R07 = [
    '// 改写原因：HOUR/MINUTE/SECOND 标注时长改为 DM 官方文档示例的小数天运算(+ 3 HOUR → + 3.0/24 等),时间跨度保持;',
    '//   DB2 两参数 TIMESTAMPDIFF(16=天,@datetime2 减 @datetime1,用作累计作业率 ljzyl 的分母) 按 HR-006 确认口径①(实际完整时长)',
    "//   改为 (DATEDIFF(SECOND,to_date(@datetime1,'yyyymmddhh24miss'),to_date(@datetime2,'yyyymmddhh24miss'))/86400),整数除法与 DB2 截断行为一致;依据 DM 官方文档,DM8 尚未实测。",
]
_R09 = [
    '// 改写原因：①SYSIBM 辅助表改为 DUAL(首轮,编号 CHANGE-381,并入本块);②HOUR/MINUTE/SECOND 标注时长改为 DM 官方文档示例的小数天运算(+ 3 HOUR → + 3.0/24 等),时间跨度保持;',
    '//   ③DB2 两参数 TIMESTAMPDIFF(2=秒/4=分钟/16=天,起点-终点) 按 HR-006 确认口径①(实际完整时长)改为 DATEDIFF(SECOND,起点,终点),',
    '//   分钟/天再 /60、/86400,整数除法与 DB2 截断行为一致;digits(cast(... as bigint)) 供 right() 取位的原写法保持不变;依据 DM 官方文档,DM8 尚未实测。',
]

import sys
if True:
    pass
n1 = process('Server/PSSM/p_pssm_13060/mmlgap07_inq.cpp', 'analysis/dameng-migration/batches/tsdiff-mmlgap07_inq.cpp.bak',
             'CHANGE-138',
             '// DM8 适配 CHANGE-138:查询转炉生产日报(当日/累计,含#转炉与一系列/二系列合计)的产量、节奏、时长与作业率指标。',
             _R07)
n2 = process('Server/PSSM/p_pssm_13060/mmsmap07_inq.cpp', 'analysis/dameng-migration/batches/tsdiff-mmsmap07_inq.cpp.bak',
             'CHANGE-148',
             '// DM8 适配 CHANGE-148:查询转炉生产日报(当日/累计,含#转炉与一系列合计)的产量、节奏、时长与作业率指标。',
             _R07)
n3 = process('Server/PSSM/p_pssm_13060/mmlgap09_inq.cpp', 'analysis/dameng-migration/batches/tsdiff-mmlgap09_inq.cpp.bak',
             'CHANGE-141',
             '// DM8 适配 CHANGE-141:查询连铸生产日报(当日/累计,含#连铸与系列合计)的产量、节奏、时长与作业率指标。',
             _R09, delete_change='CHANGE-381')
n4 = process('Server/PSSM/p_pssm_13060/mmsmap09_inq.cpp', 'analysis/dameng-migration/batches/tsdiff-mmsmap09_inq.cpp.bak',
             'CHANGE-150',
             '// DM8 适配 CHANGE-150:查询连铸生产日报(当日/累计,含#连铸与系列合计)的产量、节奏、时长与作业率指标。',
             _R09)
print('PSSM ALL DONE', n1, n2, n3, n4)
