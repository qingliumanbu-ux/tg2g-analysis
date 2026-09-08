# -*- coding: utf-8 -*-
"""PSSM 全局重编号 + 命中文件入账 + HR 行标记。"""
import csv
import hashlib
import io
import os
import re
import subprocess
import sys

sys.path.insert(0, r"D:\work\company\太钢二炼钢\analysis\dameng-migration\batches\wmsm")
import dm8lib

dm8lib.set_module("PSSM")
ROOT = dm8lib.ROOT
LEDGER = dm8lib.LEDGER
HERE = r"D:\work\company\太钢二炼钢\analysis\dameng-migration\batches\wmsm"

# 1) 找出 PSSM 已修改文件(git),稳定排序
r = subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain"],
                   capture_output=True, text=True)
modified = []
for line in r.stdout.splitlines():
    if line.startswith(" M ") or line.startswith("M "):
        modified.append(line[3:].strip().replace("\\", "/"))
modified = sorted(m for m in modified if m.endswith(".cpp"))
print("modified files:", len(modified))

# 2) 全局重编号:按文件顺序、文件内行顺序,从 115 起连续分配
HEAD = re.compile(r"//\s*DM8 适配 CHANGE-(\d+)：")
n = 114
for rel in modified:
    path = os.path.join(ROOT, rel)
    raw = open(path, "rb").read()
    try:
        text = raw.decode("utf-8"); enc = "utf-8"
    except UnicodeDecodeError:
        text = raw.decode("gb18030"); enc = "gb18030"
    lines = text.split("\n")
    hits = [i for i, l in enumerate(lines) if HEAD.search(l)]
    if not hits:
        continue
    for i in hits:
        n += 1
        lines[i] = HEAD.sub(f"// DM8 适配 CHANGE-{n}：", lines[i], count=1)
    open(path, "wb").write("\n".join(lines).encode(enc))
    print(f"renumber {rel}: {len(hits)} blocks -> up to CHANGE-{n}")

print("global max CHANGE:", n)

# 3) 命中文件入账
hits_file = r"D:\work\company\太钢二炼钢\analysis\dameng-migration\batches\pssm\pssm-dialect-hits.tsv"
hit_lines = io.open(hits_file, encoding="utf-8").read().splitlines()[1:]
hit_files = sorted({l.split("\t", 2)[0] for l in hit_lines
                    if not l.split("\t", 2)[2].strip().startswith("case DB_KIND_")})
for f in hit_files:
    r2 = subprocess.run([sys.executable, os.path.join(HERE, "dm8lib.py"),
                         "ledger", f, "PSSM"],
                        capture_output=True, text=True,
                        encoding="utf-8", errors="replace")
    out = (r2.stdout + r2.stderr).strip().splitlines()
    if r2.returncode != 0:
        print("!!", f, out[:2])

# 4) HR-005 标记(TIMESTAMPDIFF 块)与特殊行
rows = list(csv.DictReader(io.open(LEDGER, encoding="utf-8-sig", newline="")))
hr5 = 0
for r3 in rows:
    if r3["module"] != "PSSM" or r3["decision"] != "可保留":
        continue
    try:
        s, e = r3["anchor"].lstrip("L").split("-L")
    except ValueError:
        continue
    path = os.path.join(ROOT, r3["path"])
    if not os.path.exists(path):
        continue
    lines, _, _ = dm8lib.read_lines(path)
    block = "\n".join(lines[int(s) - 1:int(e)])
    if re.search(r"TIMESTAMPDIFF", block, re.I):
        r3["decision"] = "待人工复核"
        r3["status"] = "待人工复核(时长口径,见HR-005)"
        r3["human_review_id"] = "HR-005"
        r3["local_dependency"] = "需用户选定天/分/秒口径后整条改写;DM8 无两参数 TIMESTAMPDIFF"
        r3["evidence"] = "IBM TIMESTAMPDIFF 定义 + DM DATEDIFF;口径未定不改写"
        hr5 += 1
    elif "TRIM(SM_PLAN_NO)" in block and "DELETE" in block.upper():
        r3["decision"] = "待人工复核"
        r3["status"] = "待人工复核(空串/NULL删除范围,见HR-003)"
        r3["human_review_id"] = "HR-003"
        r3["local_dependency"] = "等 HR-003 答复;答复前不扩大删除条件"
        r3["evidence"] = "空串与 NULL 语义随 DM 配置变化,见待人工复核清单 HR-003"
        hr5 += 1
    elif "current timestamp" in block.lower():
        r3["decision"] = "已转换"
        r3["status"] = "已转换(静态复核)"
        r3["sql_id"] = "CHANGE-" + str(n)
        r3["evidence"] = "DM CURRENT_TIMESTAMP + FF6 官方格式元素;内联语句,注释保留原句"
        hr5 += 1
with io.open(LEDGER, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=dm8lib.FIELDS)
    w.writeheader()
    w.writerows(rows)
print("special rows patched:", hr5)
