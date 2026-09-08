# -*- coding: utf-8 -*-
"""修正全部转换块的第一行描述:读取活动 SQL,解析操作类型和表名,生成准确描述。"""
import io
import os
import re
import sys

sys.path.insert(0, r"D:\work\company\太钢二炼钢\analysis\dameng-migration\batches\wmsm")
import dm8lib

SERVER = r"D:\work\company\太钢二炼钢\Server"

# 方言中文说明
RULE_CN = {
    "T1": "SYSIBM 辅助表改为 DUAL",
    "T2": "DB2 天数后缀改为整数天运算",
    "T2b": "表达式级天数标注改为整数天运算",
    "T3": "DAYS() 天数差改用 DATEDIFF",
    "T4": "空值搜索 DECODE 改为标准 CASE",
    "T5": "二元标量 MAX 改为空值守卫 GREATEST",
    "T6": "ROWNUM 别名改为 RN",
    "T7": "序列 DDL 改为 DM 支持子句",
    "T8": "DB2 nextval for 改为 seq.NEXTVAL",
    "T9": "DB2 VALUE 改为 NVL",
    "T10": "SUBSTR2 改为 SUBSTR",
    "T11": "INTERVAL 改为小数天运算",
    "T12": "空串搜索 DECODE 改为标准 CASE",
    "T13": "时/分/秒标注改为小数天运算",
    "T14": "DB2 current 寄存器改为 CURRENT_*",
    "T15": "POSSTR 改为 INSTR",
}

# 从改写原因行反向提取规则名
REASON_TO_RULE = {}
for k, v in RULE_CN.items():
    # 提取改写原因中的关键词片段
    REASON_TO_RULE[v[:8]] = k

OPS = [
    (re.compile(r'\bINSERT\s+INTO\s+([A-Za-z_][\w.]*)', re.I), '写入'),
    (re.compile(r'\bUPDATE\s+([A-Za-z_][\w.]*)', re.I), '更新'),
    (re.compile(r'\bDELETE\s+FROM\s+([A-Za-z_][\w.]*)', re.I), '删除'),
    (re.compile(r'\bSELECT\b', re.I), '查询'),
]


def analyze_sql(sql_text):
    """分析 SQL:返回(操作类型, 表名列表)"""
    ops = []
    tables = []
    for pat, op_name in OPS:
        for m in pat.finditer(sql_text):
            if op_name not in ops:
                ops.append(op_name)
            if m.lastindex and m.lastindex >= 1:
                tbl = m.group(1).split('.')[-1].upper()
                if tbl not in tables and not tbl.startswith('('):
                    tables.append(tbl)
    if not ops:
        ops = ['查询']
    return ops, tables


def get_rules_from_reason(reason_line):
    """从改写原因行提取规则中文名列表"""
    rules = []
    for frag, rk in sorted(REASON_TO_RULE.items(), key=lambda x: -len(x[0])):
        if frag in reason_line:
            rules.append(RULE_CN[rk])
    return rules


def fix_file(src_path, mod):
    raw = open(src_path, 'rb').read()
    try:
        text = raw.decode('utf-8')
        enc = 'utf-8'
    except UnicodeDecodeError:
        text = raw.decode('gb18030')
        enc = 'gb18030'
    lines = text.split('\n')
    changed = 0

    i = 0
    while i < len(lines):
        m = re.search(r'//\s*DM8 适配 (CHANGE-\d+)：(.+)', lines[i])
        if not m:
            i += 1
            continue
        cid = m.group(1)
        old_desc = m.group(2)

        # 找改写原因行
        reason = ''
        for j in range(i + 1, min(i + 6, len(lines))):
            if '改写原因' in lines[j]:
                reason = lines[j]
                break

        # 找 DM8 SQL 行并读取活动 SQL 文本(到 ;)
        dm8_line = None
        for j in range(i, min(i + 30, len(lines))):
            if 'DM8 SQL' in lines[j]:
                dm8_line = j
                break
        if dm8_line is None:
            i += 1
            continue

        # 提取活动 SQL 文本
        sql_parts = []
        for j in range(dm8_line + 1, min(dm8_line + 40, len(lines))):
            l = lines[j].strip()
            if l.startswith('//'):
                continue
            for mm in re.finditer(r'"([^"]*)"', l):
                sql_parts.append(mm.group(1))
            if l.rstrip().endswith(';') or l.rstrip().endswith('";'):
                break
        sql_text = ' '.join(sql_parts)

        # 分析操作和表名
        ops, tables = analyze_sql(sql_text)
        rules = get_rules_from_reason(reason)

        # 生成新描述
        op_str = '/'.join(ops) if ops else 'SQL'
        tbl_str = ','.join(tables[:2]) if tables else ''
        biz = f'{op_str}' + (f' {tbl_str}' if tbl_str else '')
        new_desc = f'{cid}:{biz}。{"; ".join(rules) if rules else "见改写原因"}。'

        # 只在描述不准确时替换
        if '日期按天前推计算' in old_desc or old_desc.startswith('SQL') or len(old_desc) < 15:
            lines[i] = lines[i].replace(
                f'// DM8 适配 {cid}：{old_desc}',
                f'// DM8 适配 {new_desc}')
            changed += 1
        i = dm8_line + 1

    if changed:
        open(src_path, 'wb').write('\n'.join(lines).encode(enc))
    return changed


# 遍历全部已转换文件
total_fixed = 0
total_files = 0
for mod in sorted(os.listdir(SERVER)):
    mdir = os.path.join(SERVER, mod)
    if not os.path.isdir(mdir):
        continue
    for dp, dn, fn in os.walk(mdir):
        if '.git' in dn:
            dn.remove('.git')
        for f in fn:
            if not f.lower().endswith('.cpp'):
                continue
            p = os.path.join(dp, f)
            raw = open(p, 'rb').read()
            try:
                t = raw.decode('utf-8')
            except UnicodeDecodeError:
                t = raw.decode('gb18030', errors='replace')
            if 'DM8 适配 CHANGE-' not in t:
                continue
            if '日期按天前推计算' not in t:
                continue  # 描述已准确
            n = fix_file(p, mod)
            if n:
                total_fixed += n
                total_files += 1
                print(f'  {mod}/{os.path.relpath(p, mdir)}: {n} 行修正')

print(f'\n总计: {total_files} 文件, {total_fixed} 行描述修正')
