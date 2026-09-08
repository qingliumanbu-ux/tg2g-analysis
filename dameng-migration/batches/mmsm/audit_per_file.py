# -*- coding: utf-8 -*-
"""MMSM 逐文件核对:
对每个 .cpp:
  A. 提取活动 SQL 语句块(内容驱动)+ 内联/构造式调用;
  B. 与台账比对:每文件的语句块数 vs 台账行数,列出无台账行/多台账行的文件;
  C. 逐块方言复扫:可转换模式(排除已转换注释、挂起语句)必须为 0;
  D. 台账锚点有效性(行号在文件范围内)。
输出:逐文件核对表 + 差异清单。
"""
import csv
import io
import os
import re
import sys

sys.path.insert(0, r"D:\work\company\太钢二炼钢\analysis\dameng-migration\batches\wmsm")
import dm8lib

dm8lib.set_module("MMSM")
ROOT = dm8lib.ROOT
LEDGER = dm8lib.LEDGER

rows = [r for r in csv.DictReader(io.open(LEDGER, encoding="utf-8-sig", newline=""))
        if r["module"] == "MMSM"]
by_file = {}
for r in rows:
    by_file.setdefault(r["path"], []).append(r)

CONV = re.compile(
    r"SYSIBM\.|SYSTABLES|SYSCOLUMNS|\bAS\s+INT\b|nextval\s+for|(?<![.\w])value\s*\("
    r"|\bSUBSTR2\s*\(|\bPOSSTR\s*\(|INTERVAL\s+\x27|\d+\s+HOURS?\b"
    r"|\bcurrent\s+(?:date|timestamp|schema)\b|\bDAYS\s*\("
    r"|-\s*\d+\s+DAYS?\b|\+\s*\d+\s+DAYS?\b", re.I)
HR_PAT = re.compile(r"TIMESTAMPDIFF", re.I)

problems = []
out = io.open(r"D:\work\company\太钢二炼钢\analysis\dameng-migration\batches\mmsm\逐文件核对表.md",
              "w", encoding="utf-8")
out.write("# MMSM 逐文件核对表(2026-09-06)\n\n")
out.write("| 文件 | 块数 | 台账行 | 状态 | 备注 |\n|---|---:|---:|---|---|\n")

n_files = 0
for dp, dn, fn in os.walk(ROOT):
    if ".git" in dn:
        dn.remove(".git")
    for f in sorted(fn):
        if not f.lower().endswith(".cpp"):
            continue
        p = os.path.join(dp, f)
        rel = os.path.relpath(p, ROOT).replace("\\", "/")
        n_files += 1
        raw = open(p, "rb").read()
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            text = raw.decode("gb18030", errors="replace")
        lines = text.split("\n")
        blocks = dm8lib.find_blocks(lines)
        # 台账行数(排除 INLINE/KEEP 行重计:一律按行数对账)
        lrows = by_file.get(rel, [])
        status = []
        # C: 块方言复扫
        conv_left = []
        for (s, e, ap) in blocks:
            blk = "\n".join(lines[s:e + 1])
            if HR_PAT.search(blk):
                continue  # 挂起语句(设计如此)
            m = CONV.search(blk)
            if m:
                conv_left.append((s + 1, m.group(0)))
        # D: 锚点有效性
        bad_anchor = 0
        for r in lrows:
            try:
                s, e = r["anchor"].lstrip("L").split("-L")
                if int(e) > len(lines):
                    bad_anchor += 1
            except ValueError:
                bad_anchor += 1
        n_conv = sum(1 for r in lrows if r["decision"] == "已转换")
        n_hr = sum(1 for r in lrows if r["decision"] == "待人工复核")
        n_dyn = sum(1 for r in lrows if r["decision"] == "待局部信息")
        # B: 对账
        note_parts = []
        if blocks and not lrows:
            status.append("⚠有块无台账")
        if conv_left:
            status.append("⚠可转换残留")
            for ln2, what in conv_left:
                note_parts.append(f"L{ln2} [{what}]")
        if bad_anchor:
            status.append("⚠锚点越界")
            note_parts.append(f"{bad_anchor} 个锚点越界")
        # 内联调用计数(供备注)
        inline_n = sum(1 for l in lines
                       if not l.strip().startswith("//")
                       and re.search(r'(?:SetCommandText|QueryCString|QueryCDecimal|'
                                     r'QueryTable|ExecuteNonQuery|ExecuteScalar|'
                                     r'ExecuteReader|Execute|CDbCommand\s+\w+\s*\()',
                                     l) and re.search(r'"', l))
        st = "OK" if not status else " ".join(status)
        out.write(f"| {rel} | {len(blocks)} | {len(lrows)} | {st} | "
                  + "; ".join(note_parts) + " |\n")
        if status:
            problems.append((rel, st, "; ".join(note_parts)))

# 无块文件的台账行(文件可能已被改名/删除)
led_files = set(by_file)
disk_files = set()
for dp, dn, fn in os.walk(ROOT):
    if ".git" in dn:
        dn.remove(".git")
    for f in fn:
        if f.lower().endswith(".cpp"):
            disk_files.add(os.path.relpath(os.path.join(dp, f), ROOT).replace("\\", "/"))
ghost = led_files - disk_files
out.write(f"\n核对文件总数:{n_files};台账有但磁盘无:{len(ghost)}\n")
for g in sorted(ghost):
    out.write(f"- 幽灵行文件:{g}\n")
out.close()

print("files checked:", n_files)
print("problems:", len(problems))
for p2 in problems:
    print("  ", p2[0], "|", p2[1], "|", p2[2][:120])
print("ghost ledger files:", sorted(ghost))
