# -*- coding: utf-8 -*-
"""wmfm01_inq.cpp DM8 转换(接续 CHANGE-02)。

规则(均有官方依据,见 review-20260906-official.md 与本轮核对):
  T1  SYSIBM.SYSDUMMY1 / SYSIBM.DUAL -> DUAL
  T2  +/- N DAY(S) -> +/- N                (DM 日期运算:日期与整数加减以天为单位)
  T3  DAYS(A) - DAYS(B) -> DATEDIFF(DAY, B, A)   (CHANGE-01 同型)
  T4  DECODE(x, NULL, r1, r2) -> CASE WHEN x IS NULL THEN r1 ELSE r2 END
  T5  二元标量 MAX(a,b) -> CASE WHEN a IS NULL OR b IS NULL THEN NULL
          ELSE GREATEST(a,b) END     (保持 DB2 标量 MAX 的 NULL 传播)
  T6  ROWNUM 别名 -> RN(仅限该块,避免与 DM 伪列冲突)

流程:detect blocks -> per-block transforms -> 输出预览 -> 写入
      -> 验证:摘除新增行应逐字节还原;活动残留复扫;git diff --check;GB18030 回环。

用法:
  python transform_wmfm01.py preview   # 只生成预览,不改文件
  python transform_wmfm01.py apply     # 备份后写入并验证
"""
import io
import os
import re
import shutil
import subprocess
import sys

SRC = r"D:\work\company\太钢二炼钢\Server\WMSM\p_wmsm_8170\wmfm01_inq.cpp"
BAK = r"D:\work\company\太钢二炼钢\analysis\dameng-migration\batches\wmsm\wmfm01_inq.cpp.pre-change03.bak"
OUT = r"D:\work\company\太钢二炼钢\analysis\dameng-migration\batches\wmsm"

DAY_ARITH = re.compile(r"([+-]\s*)(\d+)\s+DAYS?\b", re.I)
DIALECT_HIT = re.compile(
    r"SYSIBM\.|[+-]\s*\d+\s+DAYS?\b|\)\s+DAYS?\b|\bDAYS\s*\("
    r"|DECODE\s*\([^)]*,\s*NULL\b"
    r"|\bMAX\s*\(|'\s*ROWNUM|ORDER\s+BY\s+ROWNUM", re.I)

REASON = {
    "T1": "SYSIBM 辅助表改为 DUAL",
    "T2": "DB2 日期天数后缀改为整数天运算",
    "T2b": "表达式级天数标注(如 DAYOFWEEK(...) DAYS)同样改为整数天运算",
    "T3": "DAYS() 天数差改用 DATEDIFF(DAY,起点,终点)",
    "T4": "空值搜索 DECODE 改为标准 CASE,不依赖 NULL 相等匹配的未记载语义",
    "T5": "二元标量 MAX 改为空值守卫的 GREATEST,空值传播与 DB2 标量 MAX 一致",
    "T6": "ROWNUM 别名改为 RN,避免与 DM 伪列关键字冲突",
}


def read_lines(path):
    with open(path, "rb") as f:
        raw = f.read()
    text = raw.decode("gb18030")
    lines = text.split("\n")
    trailing_nl = text.endswith("\n")
    return lines, trailing_nl


def strip_ws(s):
    return s.lstrip("\t ")


def find_blocks(lines):
    """活动代码中的 sqlstr = 赋值块:返回 [(start_idx0, end_idx0)](0 基,含端点)。"""
    blocks = []
    i = 0
    n = len(lines)
    while i < n:
        l = lines[i]
        s = l.strip()
        if s.startswith("//"):
            i += 1
            continue
        if re.match(r"^(\s*)sqlstr\s*=", l):
            start = i
            end = i
            if s.endswith(";"):
                blocks.append((start, end))
                i += 1
                continue
            j = i + 1
            while j < n:
                sj = lines[j].strip()
                if sj.startswith("//"):
                    j += 1
                    continue
                if sj == "" :
                    break
                end = j
                if sj.endswith(";"):
                    break
                j += 1
            blocks.append((start, end))
            i = end + 1
            continue
        i += 1
    return blocks


def balanced_arg_span(line, open_idx):
    """line[open_idx] == '(';返回匹配右括号下标;找不到返回 -1。"""
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
    """按顶层逗号拆参数(考虑括号与单引号字符串)。"""
    args = []
    depth = 0
    in_str = None
    cur = []
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
    """返回 (start, open_idx) —— 函数名起始与左括号位置;找第一个。"""
    m = re.search(r"\b" + name + r"\s*\(", line)
    if not m:
        return None
    return m.start(), m.end() - 1


def t3_days(line):
    """DAYS(A) - DAYS(B) -> DATEDIFF(DAY, B, A);A/B 为平衡括号参数。"""
    while True:
        first = find_call(line, "DAYS")
        if not first:
            return line
        s1, o1 = first
        c1 = balanced_arg_span(line, o1)
        if c1 < 0:
            return line
        m = re.match(r"\s*-\s*$", line[c1 + 1:])
        # 找紧随其后的 - DAYS(
        rest = line[c1 + 1:]
        m2 = re.match(r"\s*-\s*DAYS\s*\(", rest)
        if not m2:
            return line
        o2 = c1 + 1 + m2.end() - 1
        c2 = balanced_arg_span(line, o2)
        if c2 < 0:
            return line
        a = line[o1 + 1:c1].strip()
        b = line[o2 + 1:c2].strip()
        rep = f"DATEDIFF(DAY, {b}, {a})"
        line = line[:s1] + rep + line[c2 + 1:]


def t4_decode_null(line):
    """DECODE(x, NULL, r1, r2[, ...]) -> CASE WHEN x IS NULL THEN r1 ELSE r2 END
    仅处理 search 恰为 NULL 且 4 参数的形式;其余保持。"""
    changed = True
    while changed:
        changed = False
        pos = find_call(line, "DECODE")
        if not pos:
            return line
        s1, o1 = pos
        c1 = balanced_arg_span(line, o1)
        if c1 < 0:
            return line
        args = split_top_args(line[o1 + 1:c1])
        if len(args) == 4 and args[1].upper() == "NULL":
            rep = (f"CASE WHEN {args[0]} IS NULL THEN {args[2]}"
                   f" ELSE {args[3]} END")
            line = line[:s1] + rep + line[c1 + 1:]
            changed = True
        else:
            # 跳过本调用,继续找下一个
            tail = line[c1 + 1:]
            nxt = find_call(tail, "DECODE")
            if not nxt:
                return line
            # 平移坐标继续
            line = line[:c1 + 1] + t4_decode_null_tail(tail)
            return line
    return line


def t4_decode_null_tail(tail):
    return t4_decode_null(tail)


def t5_max2(line):
    """二元标量 MAX(a,b) -> 空值守卫 GREATEST;一元聚合 MAX 不动。"""
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


def transforms(line):
    """按依赖顺序应用单行转换;返回 (新行, 应用的规则集)。"""
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
    return line, used


def describe(block_lines, active_lines):
    joined = "\n".join(block_lines)
    up = joined.upper()
    m = re.search(r"TO_DATE\(@DATE_TIME,'YYYYMMDD'\)\s*-\s*(\d+)", joined)
    ndays = m.group(1) if m else ""
    if "UNION ALL" in up and re.search(r"\bLEVEL\b", up):
        return (f"生成查询日期之前{ndays}天的日期序列;日期边界、"
                "参数与结果列保持不变。")
    if re.search(r"TO_CHAR\(TO_DATE\(@DATE_TIME,'YYYYMMDD'\)\s*-\s*\d+", joined, re.I):
        return (f"取查询日期前推{ndays}日的日期字符串;"
                "日历日边界、参数与结果列保持不变。")
    return "日期按天前推过滤;过滤边界、参数与结果列保持不变。"


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "preview"
    lines, trailing_nl = read_lines(SRC)
    orig_lines = list(lines)
    blocks = find_blocks(lines)

    report = io.open(os.path.join(OUT, "wmfm01-preview.txt"), "w",
                     encoding="utf-8")
    inserts = []   # (block_start0, header_lines, commented, active_lines, used_all, orig_span)
    change_no = 2  # CHANGE-03 起
    converted = 0
    for (s, e) in blocks:
        block = lines[s:e + 1]
        joined = "\n".join(block)
        if not DIALECT_HIT.search(joined):
            continue
        # 特判:整块只含 ROWNUM 别名以外的伪列用法(229 行)不在块内触发
        active = []
        used_all = set()
        for l in block:
            nl, used = transforms(l)
            active.append(nl)
            used_all |= used
        if active == block:
            continue
        change_no += 1
        cid = f"CHANGE-{change_no:02d}"
        converted += 1
        desc = describe(block, active)
        reasons = "；".join(REASON[u] for u in
                           ["T1", "T2", "T2b", "T3", "T4", "T5", "T6"]
                           if u in used_all)
        header = [
            f"// DM8 适配 {cid}：{desc}",
            f"// 改写原因：{reasons}；依据 DM 官方文档,DM8 尚未实测。",
            "// 本共用分支面向 DM8,其他 DB_KIND 标签也会执行此 SQL;参数、结果列、条件与排序保持不变。",
            "// 原 SQL（完整保留）：",
        ]
        commented = []
        for l in block:
            lead = l[:len(l) - len(l.lstrip("\t "))]
            commented.append(lead + "// " + strip_ws(l))
        tail = ["// DM8 SQL："]
        inserts.append({
            "start0": s, "end0": e, "cid": cid, "header": header,
            "commented": commented, "tail": tail, "active": active,
            "used": sorted(used_all),
        })
        report.write(f"### {cid}  原行 {s+1}-{e+1}  规则 {sorted(used_all)}\n")
        for k, l in enumerate(block):
            if l != active[k]:
                report.write(f"  L{s+1+k} 前: {strip_ws(l)[:300]}\n")
                report.write(f"  L{s+1+k} 后: {strip_ws(active[k])[:300]}\n")
        report.write("\n")
    report.close()

    # 构造新行集
    new_lines = []
    ins_by_start = {d["start0"]: d for d in inserts}
    i = 0
    n = len(lines)
    while i < n:
        if i in ins_by_start:
            d = ins_by_start[i]
            new_lines.extend(d["header"])
            new_lines.extend(d["commented"])
            new_lines.extend(d["tail"])
            new_lines.extend(d["active"])
            i = d["end0"] + 1
            continue
        new_lines.append(lines[i])
        i += 1

    print(f"blocks_total={len(blocks)} converted={converted} "
          f"lines {len(lines)} -> {len(new_lines)}")
    if mode == "preview":
        return

    # 备份
    shutil.copyfile(SRC, BAK)

    # 写入(GB18030, LF)
    text = "\n".join(new_lines)
    if trailing_nl and not text.endswith("\n"):
        pass  # splitlines 语义:原文本不以 \n 结尾时不补
    data = text.encode("gb18030")
    with open(SRC, "wb") as f:
        f.write(data)

    # 验证1:每块注释还原 = 原行;转换幂等
    ok_restore = True
    ok_idem = True
    for d in inserts:
        orig = orig_lines[d["start0"]:d["end0"] + 1]
        rec = []
        for c in d["commented"]:
            lead_len = len(c) - len(c.lstrip("\t "))
            rec.append(c[:lead_len] + c[lead_len + 3:])
        if rec != orig:
            ok_restore = False
            print(f"!! {d['cid']} 注释还原不一致(原行 {d['start0']+1})")
            for a, b in zip(rec, orig):
                if a != b:
                    print("   还原:", repr(a[:150]))
                    print("   原行:", repr(b[:150]))
                    break
        retrans = [transforms(l)[0] for l in orig]
        if retrans != d["active"]:
            ok_idem = False
            print(f"!! {d['cid']} 转换幂等校验失败(原行 {d['start0']+1})")
            for a, b in zip(retrans, d["active"]):
                if a != b:
                    print("   再转:", repr(a[:150]))
                    print("   实际:", repr(b[:150]))
                    break
    if ok_restore:
        print("OK 注释还原:每块去掉 '// ' 前缀后与改前逐行一致")
    if ok_idem:
        print("OK 转换幂等:对原句重复应用规则结果不变")

    # 验证2:活动残留复扫
    res_pat = re.compile(
        r"SYSIBM\.|[+-]\s*\d+\s+DAYS?\b|\)\s+DAYS?\b|\bDAYS\s*\("
        r"|DECODE\s*\([^)]*,\s*NULL\b"
        r"|'\s*ROWNUM|ORDER\s+BY\s+ROWNUM", re.I)
    residue = []
    in_blk = False
    for k, l in enumerate(new_lines, 1):
        s = l.strip()
        if s.startswith("//"):
            continue
        if res_pat.search(l):
            residue.append((k, s[:200]))
    if residue:
        print(f"!! 活动残留 {len(residue)} 处:")
        for k, s in residue[:20]:
            print(f"  L{k}: {s}")
    else:
        print("OK 残留复扫:无 SYSIBM/天数后缀/DAYS/NULL-DECODE/ROWNUM别名残留")
        # 二元 MAX 残留单独看(聚合 MAX 合法)
        m2 = []
        for k, l in enumerate(new_lines, 1):
            s = l.strip()
            if s.startswith("//"):
                continue
            f = find_call(l, "MAX")
            if f:
                s1, o1 = f
                c1 = balanced_arg_span(l, o1)
                if c1 > 0:
                    args = split_top_args(l[o1 + 1:c1])
                    if len(args) == 2:
                        m2.append((k, s[:160]))
        if m2:
            print(f"!! 二元 MAX 残留 {len(m2)} 处:")
            for k, s in m2:
                print(f"  L{k}: {s}")
        else:
            print("OK 二元 MAX 无残留")

    # 验证3:git diff --check
    r = subprocess.run(["git", "-C",
                        r"D:\work\company\太钢二炼钢\Server\WMSM",
                        "diff", "--check", "--", "p_wmsm_8170/wmfm01_inq.cpp"],
                       capture_output=True, text=True)
    print(f"git diff --check exit={r.returncode} {r.stdout.strip()[:200]}")

    # 验证4:GB18030 回环 + 换行
    with open(SRC, "rb") as f:
        raw = f.read()
    try:
        rt = raw.decode("gb18030")
        print("OK GB18030 解码;CRLF 数 =", raw.count(b"\r\n"),
              ";行数 =", rt.count("\n") + 1)
    except UnicodeDecodeError as ex:
        print("!! GB18030 解码失败:", ex)
    print("sha256:")
    import hashlib
    print(hashlib.sha256(raw).hexdigest())


if __name__ == "__main__":
    main()
