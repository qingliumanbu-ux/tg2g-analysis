# -*- coding: utf-8 -*-
"""修正剩余 37 条 "SQL。" 描述:逐条读取完整 DM8 SQL(含续行),确定操作+表名。"""
import io
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wmsm'))
import dm8lib

BASE = r'D:\work\company\太钢二炼钢\Server'

# 从 _sql_desc.txt 读取目标
targets = io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               '_sql_desc.txt'), encoding='utf-8').read().splitlines()

# 按文件分组
by_file = {}
for t in targets:
    fp, ln = t.split('\t')[0].rsplit(':', 1)
    by_file.setdefault(fp, []).append(int(ln))

total = 0
for fp, line_nums in sorted(by_file.items()):
    full_path = os.path.join(BASE, fp.replace('/', os.sep))
    raw = open(full_path, 'rb').read()
    try:
        text = raw.decode('utf-8')
        enc = 'utf-8'
    except UnicodeDecodeError:
        text = raw.decode('gb18030')
        enc = 'gb18030'
    lines = text.split('\n')
    changed = False

    for ln in sorted(line_nums, reverse=True):
        idx = ln - 1
        if idx >= len(lines) or 'DM8 适配 CHANGE-' not in lines[idx]:
            continue
        # 找 DM8 SQL 行
        dm8_idx = None
        for j in range(idx, min(idx + 30, len(lines))):
            if 'DM8 SQL' in lines[j]:
                dm8_idx = j
                break
        if dm8_idx is None:
            continue
        # 提取全部字符串内容(到分号或下一个注释块)
        sql_parts = []
        for j in range(dm8_idx + 1, min(dm8_idx + 60, len(lines))):
            sl = lines[j].strip()
            if sl.startswith('//'):
                break
            # 去掉 C++ 代码,只保留字符串内容
            for mm in re.finditer(r'"([^"]*)"', sl):
                sql_parts.append(mm.group(1))
            # 检查是否是语句末尾
            clean = re.sub(r'"[^"]*"', '', sl).strip()
            if clean.endswith(';') or clean == ';':
                break
        sql_text = ' '.join(sql_parts)

        # 确定操作类型
        op = 'SQL'
        if re.search(r'\bINSERT\s+INTO\b', sql_text, re.I):
            op = '写入'
        elif re.search(r'\bUPDATE\b', sql_text, re.I):
            op = '更新'
        elif re.search(r'\bDELETE\s+FROM\b', sql_text, re.I):
            op = '删除'
        elif re.search(r'\bSELECT\b', sql_text, re.I):
            op = '查询'
        # 确定表名
        tbl = ''
        tm = re.search(r'(?:FROM|INTO|UPDATE)\s+([A-Za-z_]\w*)', sql_text, re.I)
        if tm:
            tbl = tm.group(1).upper()
        # 替换 "SQL。" 
        old = lines[idx]
        if 'SQL。' in old:
            new = old.replace('SQL。', f'{op}。' + (tbl + '。' if tbl else ''), 1)
            lines[idx] = new
            changed = True
            total += 1

    if changed:
        open(full_path, 'wb').write('\n'.join(lines).encode(enc))
        print(f'{fp}: {len(line_nums)} 行检查完成')

print(f'修正完成: {total} 行')
