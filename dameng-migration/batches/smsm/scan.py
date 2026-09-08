# -*- coding: utf-8 -*-
"""WMSM 模块活动 SQL 盘点扫描。

对 Server/WMSM 的 .cpp/.h 逐文件:
- 检测编码(优先 utf-8,其次 gb18030)与换行风格;
- 跟踪 // 与 /* */ 注释状态,只统计活动代码行;
- 识别 SQL 语句起始行(字符串字面量以 SELECT/INSERT/UPDATE/DELETE/MERGE/WITH 开头);
- 识别方言命中(需要逐条人工判定的标记)。

输出(UTF-8):
  smsm-scan-summary.csv   每文件一行:编码/换行/语句数/方言命中数
  smsm-dialect-hits.tsv   活动·代码·方言命中明细(file, line, text)
  smsm-sql-statements.tsv 语句块明细(file, start, end, 首行预览)
仅盘点,不改源码。
"""
import csv
import io
import json
import os
import re
import sys

ROOT = r"D:\work\company\太钢二炼钢\Server\SMSM"
OUT = r"D:\work\company\太钢二炼钢\analysis\dameng-migration\batches\smsm"

SQL_START = re.compile(
    r'"(\s*)(select|insert|update|delete|merge|with)\b', re.I)
DIALECT = re.compile(
    r"\bSYSIBM|\bSYSDUMMY1|\bSYSTABLES|\bSYSCOLUMNS|DAYS\s*\(|\s*\d+\s+DAYS?\b|\+\s*\d+\s+DAYS?\b|\d+\s+(?:HOUR|MINUTE|SECOND)S?\b|INTERVAL\s+'|POSSTR|TIMESTAMPDIFF|ROWNUM|NEXTVAL|CURRVAL|FETCH\s+FIRST|FOR\s+UPDATE|\(\+\)|ADD_MONTHS|MONTHS_BETWEEN|NVL\s*\(|DECODE\s*\(|SYSDATE|GREATEST|current\s+(?:date|time|timestamp|schema)|nextval\s+for|CREATE\s+SEQUENCE|(?<![.\w])value\s*\(|SUBSTR2\s*\(|LISTAGG\s*\(|CONNECT\s+BY|START\s+WITH|\bMINUS\b", re.I)
STMT_KEYWORD = re.compile(
    r'^\s*"(?:\s*)(select|insert|update|delete|merge|with)\b', re.I)


def detect(bytes_):
    enc = None
    try:
        text = bytes_.decode("utf-8")
        enc = "utf-8"
    except UnicodeDecodeError:
        text = bytes_.decode("gb18030", errors="replace")
        enc = "gb18030"
    nl = "CRLF" if b"\r\n" in bytes_ else "LF"
    return enc, nl, text


def scan_file(path):
    with open(path, "rb") as f:
        raw = f.read()
    enc, nl, text = detect(raw)
    lines = text.split("\n")
    stmts = []          # (start, end, preview)
    dialect_hits = []   # (line, text)
    in_block = False
    cur = None          # 当前语句块 dict
    for idx, line in enumerate(lines, 1):
        stripped = line.strip()
        # /* */ 块注释状态
        if in_block:
            if "*/" in line:
                in_block = False
            continue
        pos = stripped.find("/*")
        if pos != -1 and (pos == 0 or stripped[:pos].rstrip().endswith(";") is False):
            # 简化:行内出现 /* 且其前无引号闭合复杂场景,按遇到块注释处理
            pass
        if stripped.startswith("/*"):
            if "*/" not in stripped:
                in_block = True
            continue
        if stripped.startswith("//") or stripped == "":
            continue
        # 活动:语句块边界
        m = re.search(r'"\s*(select|insert|update|delete|merge|with)\b', line, re.I)
        if m:
            if cur is None:
                cur = {"start": idx, "end": idx,
                       "preview": stripped[:160]}
            else:
                # 上一块未闭合就遇到新起始:把上一块结束在上一行
                stmts.append(cur)
                cur = {"start": idx, "end": idx, "preview": stripped[:160]}
        else:
            has_quote = '"' in stripped
            if cur is not None:
                if has_quote or stripped.endswith(";") or stripped.endswith(");"):
                    cur["end"] = idx
                    if stripped.endswith(";"):
                        stmts.append(cur)
                        cur = None
                # 既无引号又非分号:暂不结束,容忍续行
        # 方言命中
        dm = DIALECT.search(line)
        if dm:
            dialect_hits.append((idx, stripped[:240]))
    if cur is not None:
        # 文件尾未闭合
        j = cur["end"]
        while j < len(lines) and lines[j - 1].strip() != "" and not lines[j - 1].strip().endswith(";"):
            j += 1
            cur["end"] = j
        stmts.append(cur)
    rel = os.path.relpath(path, ROOT).replace("\\", "/")
    return {
        "path": rel, "encoding": enc, "newline": nl,
        "stmts": stmts, "dialect": dialect_hits,
    }


def main():
    rows = []
    hits_f = io.open(os.path.join(OUT, "smsm-dialect-hits.tsv"), "w",
                     encoding="utf-8", newline="")
    stmt_f = io.open(os.path.join(OUT, "smsm-sql-statements.tsv"), "w",
                     encoding="utf-8", newline="")
    hits_f.write("file\tline\ttext\n")
    stmt_f.write("file\tstart\tend\tpreview\n")
    for dirpath, dirnames, filenames in os.walk(ROOT):
        if ".git" in dirnames:
            dirnames.remove(".git")
        for name in sorted(filenames):
            if not name.lower().endswith((".cpp", ".h")):
                continue
            path = os.path.join(dirpath, name)
            r = scan_file(path)
            rows.append({
                "file": r["path"], "encoding": r["encoding"],
                "newline": r["newline"],
                "sql_statements": len(r["stmts"]),
                "dialect_hits": len(r["dialect"]),
            })
            for (ln, tx) in r["dialect"]:
                hits_f.write(f"{r['path']}\t{ln}\t{tx}\n")
            for s in r["stmts"]:
                stmt_f.write(f"{r['path']}\t{s['start']}\t{s['end']}\t{s['preview']}\n")
    hits_f.close()
    stmt_f.close()
    with io.open(os.path.join(OUT, "smsm-scan-summary.csv"), "w",
                 encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=[
            "file", "encoding", "newline", "sql_statements", "dialect_hits"])
        w.writeheader()
        w.writerows(rows)
    total_stmt = sum(r["sql_statements"] for r in rows)
    total_hit = sum(r["dialect_hits"] for r in rows)
    with_hit = sum(1 for r in rows if r["dialect_hits"])
    print(f"files={len(rows)} statements={total_stmt} dialect_hits={total_hit} "
          f"files_with_dialect={with_hit}")
    print("encodings:", {r["encoding"] for r in rows},
          "newlines:", {r["newline"] for r in rows})


if __name__ == "__main__":
    main()
