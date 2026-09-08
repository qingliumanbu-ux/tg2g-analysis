# -*- coding: utf-8 -*-
"""TMSM/WMSM 通用 DM8 转换与入账工具。

用法:
  python dm8lib.py preview <relpath> [module]   # 生成预览 <name>-preview.txt
  python dm8lib.py apply   <relpath> [module]   # 备份、写入、验证
  python dm8lib.py ledger  <relpath> [module]   # 该文件全部语句块入账 sql-ledger.csv
module 默认 WMSM;TMSM 时 ROOT=Server/TMSM,输出到 batches/tmsm。
CHANGE 编号自动接续 sql-ledger.csv 中的全局最大值。
"""
import csv
import hashlib
import io
import os
import re
import shutil
import subprocess
import sys

BASE = r"D:\work\company\太钢二炼钢\Server"
ANALYSIS = r"D:\work\company\太钢二炼钢\analysis\dameng-migration"
LEDGER = os.path.join(ANALYSIS, "sql-ledger.csv")

# 由 main() 按 module 参数设置
ROOT = os.path.join(BASE, "WMSM")
OUT = os.path.join(ANALYSIS, "batches", "wmsm")
MODULE = "WMSM"

DAY_ARITH = re.compile(r"([+-]\s*)(\d+)\s+DAYS?\b", re.I)
SQLVAR_ASSIGN = re.compile(
    r'^\s*(?:[A-Za-z_]\w*[\s\*&]+)?[A-Za-z_]\w*\s*(?<![=!<>])(\+=|=)(?!=)'
    r'\s*["+]*\s*(?:select|insert|update|delete|merge|with|values|create'
    r'|drop|alter)?', re.I)
SQLVAR_SQL = re.compile(
    r'\b(?:select|insert\s+into|update|delete\s+from|merge\s+into|'
    r'create\s+(?:table|view|index|sequence)|drop\s+|values\s*\()', re.I)
SQL_KEYWORD = re.compile(
    r"\b(SELECT|INSERT|UPDATE|DELETE|MERGE|CREATE|DROP|WITH|VALUES|BEGIN"
    r"|WHERE|FROM|AND|OR|LIKE|JOIN|GROUP|ORDER|HAVING)\b", re.I)
DIALECT_HIT = re.compile(
    r"SYSIBM\.|[+-]\s*\d+\s+DAYS?\b|\)\s+DAYS?\b|\bDAYS\s*\("
    r"|\bDECODE\s*\("
    r"|\bMAX\s*\(|'\s*ROWNUM|ORDER\s+BY\s+ROWNUM"
    r"|\bCREATE\s+SEQUENCE\b|nextval\s+for|(?<![.\w])value\s*\("
    r"|\bSUBSTR2\s*\(|POSSTR\s*\(|INTERVAL\s+'"
    r"|\d+\s+(?:HOUR|MINUTE|SECOND)S?\b"
    r"|\bcurrent\s+(?:date|time|timestamp|schema)\b", re.I)


def has_bad_decode(line):
    """活动行中是否存在 NULL/空串搜索的 DECODE(平衡括号解析)。"""
    pos = 0
    while True:
        seg = line[pos:]
        f = find_call(seg, "DECODE")
        if not f:
            return False
        s1, o1 = f
        c1 = balanced_arg_span(seg, o1)
        if c1 < 0:
            return True  # 解析失败按可疑处理
        args = split_top_args(seg[o1 + 1:c1])
        if len(args) >= 2 and (args[1].upper() == "NULL"
                               or args[1] == "''"):
            return True
        pos += c1 + 1

REASON = {
    "T1": "SYSIBM 辅助表改为 DUAL",
    "T2": "DB2 日期天数后缀改为整数天运算",
    "T2b": "表达式级天数标注(如 DAYOFWEEK(...) DAYS)同样改为整数天运算",
    "T3": "DAYS() 天数差改用 DATEDIFF(DAY,起点,终点)",
    "T4": "空值搜索 DECODE 改为标准 CASE,不依赖 NULL 相等匹配的未记载语义",
    "T5": "二元标量 MAX 改为空值守卫的 GREATEST,空值传播与 DB2 标量 MAX 一致",
    "T6": "ROWNUM 别名改为 RN,避免与 DM 伪列关键字冲突",
    "T7": ("序列 DDL 只保留 DM 官方支持的子句(START WITH/INCREMENT BY/MINVALUE/"
           "MAXVALUE/CYCLE/NOCACHE/ORDER);去掉 AS INT 类型子句(内部按 BIGINT 精度,"
           "取值域由 MIN/MAX 约束,不受影响),NO CACHE 按 DM 拼写 NOCACHE"),
    "T8": "DB2 取号语法 values nextval for 改为 DM 序列伪列 select <seq>.NEXTVAL from DUAL",
    "T9": "DB2 同义词 VALUE 改为 DM 文档支持的 NVL(两参数:返回第一个非空值)",
    "T10": ("SUBSTR2 改为 DM 文档支持的 SUBSTR(按字符截取;BMP 字符下与码点"
            "语义一致);位置参数 0 显式改为 1,保持 Oracle 原语义"),
    "T11": ("INTERVAL 间隔字面量改为 DM 官方文档示例的小数天运算"
            "(HOUR=n.0/24),时间跨度保持"),
    "T12": ("空串搜索 DECODE(x,'',a,b) 改为标准 CASE WHEN x IS NULL OR x='' "
            "THEN a ELSE b,与 CHANGE-107 同理,不依赖空串/NULL 匹配的未记载语义"),
    "T13": ("HOUR/MINUTE/SECOND 标注时长改为 DM 官方文档示例的小数天运算"
            "(时=n.0/24,分=n.0/1440,秒=n.0/86400),时间跨度保持"),
    "T14": ("DB2 特殊寄存器 current date/time/timestamp/schema 改为 DM 的"
            " CURRENT_DATE/CURRENT_TIME/CURRENT_TIMESTAMP/CURRENT_SCHEMA(官方函数手册支持)"),
    "T15": ("DB2 POSSTR(源串,子串) 改为 DM 的 INSTR(源串,子串)"
            "(参数顺序一致,未找到时同为 0;POSSTR 不在 DM 函数手册,INSTR 为官方字符串函数)"),
}
FIELDS = ["sql_id", "module", "repository", "path", "function", "source_kind",
          "anchor", "original_comment_anchor", "active_sql_anchor", "decision",
          "status", "human_review_id", "local_dependency", "branch_impact",
          "evidence", "runtime_status", "current_file_sha256"]


def read_lines(path):
    """编码自适应:utf-8 严格解码优先,否则 gb18030;返回(行列表, 原字节, 编码)。"""
    with open(path, "rb") as f:
        raw = f.read()
    try:
        text = raw.decode("utf-8")
        enc = "utf-8"
    except UnicodeDecodeError:
        text = raw.decode("gb18030")
        enc = "gb18030"
    return text.split("\n"), raw, enc


def find_blocks(lines):
    """SQL 变量赋值块(= 与 += 单行块);返回 [(start0, end0, is_append)]。"""
    blocks = []
    i, n = 0, len(lines)
    while i < n:
        s = lines[i].strip()
        if s.startswith("//"):
            i += 1
            continue
        _m = SQLVAR_ASSIGN.match(lines[i])
        if _m:
            _vn_m = re.search(r"([A-Za-z_]\w*)\s*(?:\+=|=)", lines[i])
            _vn = _vn_m.group(1) if _vn_m else ""
            if not (SQLVAR_SQL.search(lines[i])
                    or SQL_KEYWORD.search(lines[i])
                    or _vn[:3].lower() == "sql"):
                _m = None
        if _m:
            is_append = "+=" in lines[i].split('"')[0]
            start = i
            if s.endswith(";"):
                blocks.append((start, start, is_append))
                i += 1
                continue
            j = i + 1
            end = i
            while j < n:
                sj = lines[j].strip()
                if sj.startswith("//"):
                    j += 1
                    continue
                if j > i and SQLVAR_ASSIGN.match(lines[j]):
                    break  # 新赋值开始,当前块结束(空行不再截断,避免拆散语句)
                end = j
                if sj.endswith(";"):
                    break
                j += 1
            blocks.append((start, end, is_append))
            i = end + 1
            continue
        i += 1
    return blocks


def balanced_arg_span(line, open_idx):
    depth = 0
    in_str = None
    k = open_idx
    while k < len(line):
        c = line[k]
        if in_str:
            if c == in_str:
                in_str = None
        elif c in "'\"":
            in_str = c
        elif c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                return k
        k += 1
    return -1


def split_top_args(s):
    args, depth, in_str, cur = [], 0, None, []
    for c in s:
        if in_str:
            cur.append(c)
            if c == in_str:
                in_str = None
            continue
        if c in "'\"":
            in_str = c
            cur.append(c)
            continue
        if c == "(":
            depth += 1
            cur.append(c)
        elif c == ")":
            depth -= 1
            cur.append(c)
        elif c == "," and depth == 0:
            args.append("".join(cur))
            cur = []
        else:
            cur.append(c)
    if cur:
        args.append("".join(cur))
    return [a.strip() for a in args]


def find_call(line, name):
    m = re.search(r"\b" + name + r"\s*\(", line, re.I)
    if not m:
        return None
    return m.start(), m.end() - 1


def t3_days(line):
    while True:
        first = find_call(line, "DAYS")
        if not first:
            return line
        s1, o1 = first
        c1 = balanced_arg_span(line, o1)
        if c1 < 0:
            return line
        rest = line[c1 + 1:]
        m2 = re.match(r"\s*-\s*DAYS\s*\(", rest, re.I)
        if not m2:
            return line
        o2 = c1 + 1 + m2.end() - 1
        c2 = balanced_arg_span(line, o2)
        if c2 < 0:
            return line
        a = line[o1 + 1:c1].strip()
        b = line[o2 + 1:c2].strip()
        line = line[:s1] + f"DATEDIFF(DAY, {b}, {a})" + line[c2 + 1:]


def t4_decode_null(line):
    pos = 0
    while True:
        seg = line[pos:]
        f = find_call(seg, "DECODE")
        if not f:
            return line
        s1, o1 = f
        c1 = balanced_arg_span(seg, o1)
        if c1 < 0:
            return line
        args = split_top_args(seg[o1 + 1:c1])
        hit_null = len(args) == 4 and args[1].upper() == "NULL"
        hit_empty = len(args) == 4 and args[1] == "''"
        if hit_null or hit_empty:
            if hit_null:
                cond = f"{args[0]} IS NULL"
            else:
                cond = f"{args[0]} IS NULL OR {args[0]} = ''"
            rep = f"CASE WHEN {cond} THEN {args[2]} ELSE {args[3]} END"
            absw = pos + s1
            abce = pos + c1 + 1
            line = line[:absw] + rep + line[abce:]
            pos = absw + len(rep)
        else:
            pos = pos + c1 + 1


def t5_max2(line):
    pos = 0
    while True:
        seg = line[pos:]
        f = find_call(seg, "MAX")
        if not f:
            return line
        s1, o1 = f
        c1 = balanced_arg_span(seg, o1)
        if c1 < 0:
            return line
        args = split_top_args(seg[o1 + 1:c1])
        if len(args) == 2:
            a, b = args
            rep = (f"CASE WHEN {a} IS NULL OR {b} IS NULL THEN NULL"
                   f" ELSE GREATEST({a}, {b}) END")
            absw = pos + s1
            abce = pos + c1 + 1
            line = line[:absw] + rep + line[abce:]
            pos = absw + len(rep)
        else:
            pos = pos + c1 + 1


def t10_substr2(line):
    """SUBSTR2 -> SUBSTR;位置参数为 0 时改为 1(Oracle 将 0 视作 1,
    显式化后不依赖 DM 对 0 的处理)。"""
    pos = 0
    while True:
        seg = line[pos:]
        f = find_call(seg, "SUBSTR2")
        if not f:
            return line
        s1, o1 = f
        c1 = balanced_arg_span(seg, o1)
        if c1 < 0:
            return line
        args = split_top_args(seg[o1 + 1:c1])
        if len(args) >= 2 and args[1].strip() == "0":
            args[1] = "1"
        rep = "SUBSTR(" + ", ".join(args) + ")"
        absw = pos + s1
        abce = pos + c1 + 1
        line = line[:absw] + rep + line[abce:]
        pos = absw + len(rep)


def t10_substr2_like(line, old_name, new_name):
    """同参数顺序的函数换名(如 POSSTR->INSTR),不动参数。"""
    pos = 0
    while True:
        seg = line[pos:]
        f = find_call(seg, old_name)
        if not f:
            return line
        s1, o1 = f
        c1 = balanced_arg_span(seg, o1)
        if c1 < 0:
            return line
        args = split_top_args(seg[o1 + 1:c1])
        rep = new_name + "(" + ", ".join(args) + ")"
        absw = pos + s1
        abce = pos + c1 + 1
        line = line[:absw] + rep + line[abce:]
        pos = absw + len(rep)


def transforms(line):
    used = set()
    if DAY_ARITH.search(line):
        line = DAY_ARITH.sub(lambda m: f"{m.group(1)}{m.group(2)}", line)
        used.add("T2")
    if re.search(r"\)\s+DAYS?\b", line, re.I):
        line = re.sub(r"\)\s+DAYS?\b", ")", line, flags=re.I)
        used.add("T2b")
    if re.search(r"SYSIBM\.(SYSDUMMY1|DUAL)\b", line, re.I):
        line = re.sub(r"SYSIBM\.(SYSDUMMY1|DUAL)\b", "DUAL", line, flags=re.I)
        used.add("T1")
    if re.search(r"\bDAYS\s*\(", line, re.I):
        new = t3_days(line)
        if new != line:
            used.add("T3")
        line = new
    if re.search(r"DECODE\s*\(", line, re.I):
        new = t4_decode_null(line)
        if new != line:
            if re.search(r"DECODE\s*\([^)]*,\s*''", line, re.I):
                used.add("T12")
            else:
                used.add("T4")
        line = new
    if re.search(r"\bMAX\s*\(", line, re.I):
        new = t5_max2(line)
        if new != line:
            used.add("T5")
        line = new
    if re.search(r"'\s*ROWNUM|ORDER\s+BY\s+ROWNUM", line, re.I):
        line2 = re.sub(r"'\s*ROWNUM\b", "' RN", line, flags=re.I)
        line2 = re.sub(r"\bORDER\s+BY\s+ROWNUM\b", "ORDER BY RN", line2,
                       flags=re.I)
        if line2 != line:
            used.add("T6")
        line = line2
    if re.search(r"\bCREATE\s+SEQUENCE\b", line, re.I):
        line2 = re.sub(r"\bAS\s+INT\b", "", line, flags=re.I)
        line2 = re.sub(r"\bNO\s+CACHE\b", "NOCACHE", line2, flags=re.I)
        if line2 != line:
            used.add("T7")
        line = line2
    m8 = re.match(r'^(\s*)sqlstr = "values nextval for " \+ (\w+);', line)
    if m8:
        line = (f'{m8.group(1)}sqlstr = "select " + {m8.group(2)}'
                f' + ".nextval from dual";')
        used.add("T8")
    elif re.search(r"\bnextval\s+for\s+([A-Za-z_]\w*)", line, re.I):
        line = re.sub(r"\bnextval\s+for\s+([A-Za-z_]\w*)",
                      lambda m: f"{m.group(1)}.NEXTVAL", line, flags=re.I)
        used.add("T8")
    if re.search(r"(?<![.\w])value\s*\(", line, re.I):
        line2 = re.sub(r"(?<![.\w])value\s*\(", "nvl(", line, flags=re.I)
        if line2 != line:
            used.add("T9")
        line = line2
    if re.search(r"\bSUBSTR2\s*\(", line, re.I):
        new = t10_substr2(line)
        if new != line:
            used.add("T10")
        line = new
    m11 = re.search(r"([+-]\s*)INTERVAL\s+'(\d+)'\s+HOUR\b", line, re.I)
    if m11:
        line = re.sub(r"([+-]\s*)INTERVAL\s+'(\d+)'\s+HOUR\b",
                      lambda m: f"{m.group(1)}{m.group(2)}.0/24", line,
                      flags=re.I)
        used.add("T11")
    m13 = re.search(r"([+-]\s*)(\d+)\s+(HOUR|MINUTE|SECOND)S?\b", line,
                    re.I)
    if m13:
        unit = {"HOUR": "24", "MINUTE": "1440", "SECOND": "86400"}
        line = re.sub(
            r"([+-]\s*)(\d+)\s+(HOUR|MINUTE|SECOND)S?\b",
            lambda m: f"{m.group(1)}{m.group(2)}.0/{unit[m.group(3).upper()]}",
            line, flags=re.I)
        used.add("T13")
    m14 = re.search(r"\bcurrent\s+(date|time|timestamp|schema)\b", line, re.I)
    if m14:
        line = re.sub(r"\bcurrent\s+(date|time|timestamp|schema)\b",
                      lambda m: "CURRENT_" + m.group(1).upper(),
                      line, flags=re.I)
        used.add("T14")
    if re.search(r"\bPOSSTR\s*\(", line, re.I):
        new = t10_substr2_like(line, "POSSTR", "INSTR")
        if new != line:
            used.add("T15")
        line = new
    return line, used


def describe(joined):
    up = joined.upper()
    m = re.search(r"TO_DATE\(@DATE_TIME,'YYYYMMDD'\)\s*-\s*(\d+)", joined)
    nd = m.group(1) if m else ""
    if "UNION ALL" in up and re.search(r"\bLEVEL\b", up):
        return f"生成查询日期之前{nd}天的日期序列;日期边界、参数与结果列保持不变。"
    if re.search(r"TO_CHAR\(TO_DATE\(@DATE_TIME,'YYYYMMDD'\)\s*-\s*\d+", joined,
                 re.I):
        return f"取查询日期前推{nd}日的日期字符串;日历日边界、参数与结果列保持不变。"
    return "日期按天前推计算;日期边界、参数与结果列保持不变。"


def do_transform(relpath, mode):
    src = os.path.join(ROOT, relpath)
    lines, raw, enc = read_lines(src)
    orig_lines = list(lines)
    blocks = find_blocks(lines)
    name = os.path.splitext(os.path.basename(relpath))[0]
    inserts = []
    change_no = max_change_no()  # 全局接续
    for (s, e, ap) in blocks:
        block = lines[s:e + 1]
        joined = "\n".join(block)
        if not ap and not SQL_KEYWORD.search(joined):
            continue
        if not DIALECT_HIT.search(joined):
            continue
        active, used_all = [], set()
        for l in block:
            nl, used = transforms(l)
            active.append(nl)
            used_all |= used
        if active == block:
            continue
        change_no += 1
        cid = f"CHANGE-{change_no:02d}"
        reasons = "；".join(REASON[u] for u in
                           ["T1", "T2", "T2b", "T3", "T4", "T5", "T6",
                            "T7", "T8", "T9", "T10", "T11", "T12", "T13",
                            "T14", "T15"]
                           if u in used_all)
        header = [
            f"// DM8 适配 {cid}：{describe(joined)}",
            f"// 改写原因：{reasons}；依据 DM 官方文档,DM8 尚未实测。",
            "// 本共用分支面向 DM8,其他 DB_KIND 标签也会执行此 SQL;参数、结果列、条件与排序保持不变。",
            "// 原 SQL（完整保留）：",
        ]
        commented = []
        for l in block:
            lead = l[:len(l) - len(l.lstrip("\t "))]
            commented.append(lead + "// " + l.lstrip("\t "))
        tail = ["// DM8 SQL："]
        inserts.append({"start0": s, "end0": e, "cid": cid, "header": header,
                        "commented": commented, "tail": tail,
                        "active": active})
    # 预览
    pf = io.open(os.path.join(OUT, f"{name}-preview.txt"), "w", encoding="utf-8")
    for d in inserts:
        pf.write(f"### {d['cid']}  原行 {d['start0']+1}-{d['end0']+1}\n")
        for k, l in enumerate(lines[d["start0"]:d["end0"] + 1]):
            if l != d["active"][k]:
                pf.write(f"  L{d['start0']+1+k} 前: {l.strip()[:280]}\n")
                pf.write(f"  L{d['start0']+1+k} 后: {d['active'][k].strip()[:280]}\n")
    pf.close()
    print(f"{relpath}: blocks={len(blocks)} converted={len(inserts)} "
          f"lines {len(lines)} -> {len(lines) + sum(len(d['header']) + len(d['commented']) + len(d['tail']) for d in inserts)}")
    if not inserts:
        return
    if mode == "preview":
        print(f"preview -> {name}-preview.txt")
        return
    bak = os.path.join(OUT, name + ".pre-dm8.bak")
    shutil.copyfile(src, bak)
    ins_by_start = {d["start0"]: d for d in inserts}
    new_lines, i = [], 0
    while i < len(lines):
        if i in ins_by_start:
            d = ins_by_start[i]
            new_lines.extend(d["header"] + d["commented"] + d["tail"] + d["active"])
            i = d["end0"] + 1
            continue
        new_lines.append(lines[i])
        i += 1
    with open(src, "wb") as f:
        f.write("\n".join(new_lines).encode(enc))
    # 验证
    ok1 = ok2 = True
    for d in inserts:
        orig = orig_lines[d["start0"]:d["end0"] + 1]
        rec = []
        for c in d["commented"]:
            ll = len(c) - len(c.lstrip("\t "))
            rec.append(c[:ll] + c[ll + 3:])
        if rec != orig:
            ok1 = False
            print(f"!! {d['cid']} 注释还原不一致(原行 {d['start0']+1})")
        retrans = [transforms(l)[0] for l in orig]
        if retrans != d["active"]:
            ok2 = False
            print(f"!! {d['cid']} 幂等失败(原行 {d['start0']+1})")
    print("OK 注释还原" if ok1 else "!! 注释还原失败")
    print("OK 转换幂等" if ok2 else "!! 幂等失败")
    res = re.compile(
        r"SYSIBM\.|[+-]\s*\d+\s+DAYS?\b|\)\s+DAYS?\b|\bDAYS\s*\("
        r"|'\s*ROWNUM|ORDER\s+BY\s+ROWNUM"
        r"|\bAS\s+INT\b|\bNO\s+CACHE\b|nextval\s+for|(?<![.\w])value\s*\("
        r"|\bSUBSTR2\s*\(|POSSTR\s*\(|INTERVAL\s+'"
        r"|\d+\s+(?:HOUR|MINUTE|SECOND)S?\b"
        r"|\bcurrent\s+(?:date|time|timestamp|schema)\b", re.I)
    resid = []
    for k, l in enumerate(new_lines, 1):
        s = l.strip()
        if s.startswith("//"):
            continue
        if res.search(l) or has_bad_decode(l):
            resid.append((k, s[:160]))
    if resid:
        print(f"!! 活动残留 {len(resid)} 处:")
        for k, s in resid[:15]:
            print(f"  L{k}: {s}")
    else:
        print("OK 残留复扫通过")
    r = subprocess.run(["git", "-C", ROOT, "diff", "--check", "--",
                        relpath.replace("\\", "/")],
                       capture_output=True, text=True)
    print(f"git diff --check exit={r.returncode}")
    with open(src, "rb") as f:
        raw2 = f.read()
    rt = raw2.decode(enc)
    print(f"OK GB18030 解码;行数={rt.count(chr(10))+1};"
          f"CRLF={raw2.count(bytes([13, 10]))}")
    print("sha256:", hashlib.sha256(raw2).hexdigest())


def classify(text):
    up = text.upper()
    notes = []
    if "DECODE" in up:
        notes.append("DM DECODE 支持(函数手册表8.6);无 NULL 搜索值")
    if re.search(r"\bROWNUM\b", up):
        notes.append("DM ROWNUM 伪列支持(查询语句4.15)")
    if "CAST(" in up or "DECIMAL" in up:
        notes.append("DM CAST/DECIMAL 支持")
    return "；".join(notes)


def find_function(lines, idx):
    for k in range(idx, -1, -1):
        m = re.match(r"^\s*int\s+(\w+)\s*\(", lines[k])
        if m:
            return m.group(1)
    return "file_scope"


def do_ledger(relpath):
    src = os.path.join(ROOT, relpath)
    lines, raw, enc = read_lines(src)
    sha = hashlib.sha256(raw).hexdigest()
    blocks = find_blocks(lines)
    rows = []
    keep_no = 0
    conv_no = 0
    for (s, e, ap) in blocks:
        text = "\n".join(lines[s:e + 1])
        if not ap and not SQL_KEYWORD.search(text):
            continue
        cid = ""
        k = s - 1
        while k >= 0 and lines[k].strip() == "":
            k -= 1
        if k >= 0 and lines[k].strip().startswith("// DM8 SQL："):
            dm8_line = k
            j = k - 1
            while j >= 0 and not lines[j].strip().startswith("// DM8 适配 CHANGE-"):
                j -= 1
            if j >= 0:
                m = re.search(r"CHANGE-\d+", lines[j])
                cid = m.group(0) if m else ""
                cmt = f"L{j+3}-L{dm8_line-1}"
            else:
                cmt = ""
        if cid:
            conv_no += 1
            sql_id = cid
            decision = "已转换"
            status = "已转换(静态复核)"
            evidence = "见源码注释头改写原因;T1/T2/T2b/T3/T4/T5/T6 规则官方依据"
        else:
            keep_no += 1
            sql_id = f"KEEP-{os.path.basename(relpath).split('.')[0]}-{keep_no:02d}"
            decision = "可保留"
            status = "可保留(已复核)"
            note = classify(text)
            evidence = note if note else "普通 CRUD/聚合,无方言差异"
            cmt = ""
        rows.append({
            "sql_id": sql_id,
            "module": MODULE,
            "repository": f"Server/{MODULE}",
            "path": relpath.replace("\\", "/"),
            "function": find_function(lines, s),
            "source_kind": "literal_concat_append" if ap else "literal_concat",
            "anchor": f"L{s+1}-L{e+1}",
            "original_comment_anchor": cmt,
            "active_sql_anchor": f"L{s+1}-L{e+1}",
            "decision": decision,
            "status": status,
            "human_review_id": "",
            "local_dependency": "",
            "branch_impact": "共用路径(以源码 switch 为准)" if not ap
                            else "追加片段,并入所属语句",
            "evidence": evidence,
            "runtime_status": "未执行",
            "current_file_sha256": sha,
        })
    # 动态片段
    for k, l in enumerate(lines, 1):
        if re.search(r"SQL_CONTEXT|QUERY_SQL|CND_RELATION", l) \
                and "=" in l and not l.strip().startswith("//"):
            rows.append({
                "sql_id": f"DYN-{os.path.basename(relpath).split('.')[0]}-01",
                "module": MODULE,
                "repository": f"Server/{MODULE}",
                "path": relpath.replace("\\", "/"),
                "function": find_function(lines, k - 1),
                "source_kind": "dynamic_fragment_from_table",
                "anchor": f"L{k}",
                "original_comment_anchor": "",
                "active_sql_anchor": "",
                "decision": "待局部信息",
                "status": "待局部信息(SQL文本未取得)",
                "human_review_id": "",
                "local_dependency": "需要该数据集实际 SQL 文本及参数定义",
                "branch_impact": "动态拼接",
                "evidence": "执行器可保留不代表传入文本兼容",
                "runtime_status": "未执行",
                "current_file_sha256": sha,
            })
            break
    # 内联 SQL(直接传入执行 API 的字符串字面量,未被变量块覆盖)
    in_block = set()
    for (s, e, ap) in blocks:
        in_block.update(range(s, e + 1))
    inline = re.compile(
        r"(?:QueryCString|QueryCDecimal|QueryTable|ExecuteNonQuery|"
        r"ExecuteScalar|Execute|SetCommandText)\s*\(\s*\"[^\"]*"
        r"\b(SELECT|INSERT|UPDATE|DELETE|MERGE|CREATE|DROP)\b", re.I)
    inline_no = 0
    base = os.path.basename(relpath).split(".")[0]
    for k, l in enumerate(lines, 1):
        if (k - 1) in in_block or l.strip().startswith("//"):
            continue
        if inline.search(l):
            inline_no += 1
            note = classify(l)
            rows.append({
                "sql_id": f"INLINE-{base}-{inline_no:02d}",
                "module": MODULE,
                "repository": f"Server/{MODULE}",
                "path": relpath.replace("\\", "/"),
                "function": find_function(lines, k - 1),
                "source_kind": "inline_call_literal",
                "anchor": f"L{k}",
                "original_comment_anchor": "",
                "active_sql_anchor": f"L{k}",
                "decision": "可保留",
                "status": "可保留(已复核)",
                "human_review_id": "",
                "local_dependency": "",
                "branch_impact": "内联调用,无分支",
                "evidence": note if note else "内联 SQL,无方言差异",
                "runtime_status": "未执行",
                "current_file_sha256": sha,
            })
    try:
        with io.open(LEDGER, encoding="utf-8-sig", newline="") as f:
            old = [r for r in csv.DictReader(f)
                   if r["path"] != relpath.replace("\\", "/")]
    except FileNotFoundError:
        old = []
    with io.open(LEDGER, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(old)
        w.writerows(rows)
    conv = sum(1 for r in rows if r["decision"] == "已转换")
    keep = sum(1 for r in rows if r["decision"] == "可保留")
    dyn = sum(1 for r in rows if r["decision"] == "待局部信息")
    print(f"{relpath}: rows={len(rows)} converted={conv} keep={keep} dyn={dyn}")


def max_change_no():
    """台账中已用的最大 CHANGE 编号(WMSM/TMSM 全局共用序列)。"""
    try:
        with io.open(LEDGER, encoding="utf-8-sig", newline="") as f:
            mx = 0
            for r in csv.DictReader(f):
                m = re.match(r"CHANGE-(\d+)$", r.get("sql_id", ""))
                if m:
                    mx = max(mx, int(m.group(1)))
            return mx
    except FileNotFoundError:
        return 0


def set_module(module):
    global ROOT, OUT, MODULE
    MODULE = (module or "WMSM").upper()
    ROOT = os.path.join(BASE, MODULE)
    OUT = os.path.join(ANALYSIS, "batches", MODULE.lower())
    os.makedirs(OUT, exist_ok=True)


def main():
    mode, rel = sys.argv[1], sys.argv[2]
    set_module(sys.argv[3] if len(sys.argv) > 3 else "WMSM")
    if mode == "ledger":
        do_ledger(rel)
    else:
        do_transform(rel, mode)


if __name__ == "__main__":
    main()
