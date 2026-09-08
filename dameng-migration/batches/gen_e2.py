# -*- coding: utf-8 -*-
"""从台账提取全部已转换语句,生成 DM8 E2 验证 SQL 脚本。"""
import csv
import io
import os
import re
import sys

sys.path.insert(0, r"D:\work\company\太钢二炼钢\analysis\dameng-migration\batches\wmsm")
import dm8lib

LEDGER = r"D:\work\company\太钢二炼钢\analysis\dameng-migration\sql-ledger.csv"
OUTDIR = r"D:\work\company\太钢二炼钢\analysis\dameng-migration"

rows = list(csv.DictReader(io.open(LEDGER, encoding="utf-8-sig", newline="")))
conv = [r for r in rows if r["decision"] == "已转换"]
print(f"已转换 {len(conv)} 条")

# 按模块分组
by_mod = {}
for r in conv:
    by_mod.setdefault(r["module"], []).append(r)

# 缓存文件内容
cache = {}


def get_lines(mod, rel):
    key = mod + "/" + rel
    if key not in cache:
        dm8lib.set_module(mod)
        p = os.path.join(dm8lib.ROOT, rel.replace("/", os.sep))
        if os.path.exists(p):
            cache[key] = dm8lib.read_lines(p)[0]
        else:
            cache[key] = []
    return cache[key]


def extract_active_sql(lines, anchor):
    """从锚点行读取活动 DM8 SQL(直到 ; 或块尾)"""
    m = re.match(r"^L(\d+)(?:-L(\d+))?$", anchor)
    if not m:
        return None
    s = int(m.group(1))
    e = int(m.group(2) or m.group(1))
    if s > len(lines):
        return None
    e = min(e, len(lines))
    parts = []
    for k in range(s - 1, e):
        l = lines[k].rstrip()
        # 提取字符串字面量
        for mm in re.finditer(r'"([^"]*)"', l):
            parts.append(mm.group(1))
    sql = "".join(parts)
    # 去掉 C++ 拼接残留
    sql = re.sub(r"\s+", " ", sql).strip()
    return sql if len(sql) > 5 else None


def to_test_sql(sql):
    """将 @param 替换为测试常量"""
    sql = re.sub(r"@\w+", "'测试值'", sql)
    return sql


grand = 0
for mod in sorted(by_mod):
    recs = by_mod[mod]
    dm8lib.set_module(mod)
    outfile = os.path.join(OUTDIR, f"e2-verify-{mod.lower()}.sql")
    with io.open(outfile, "w", encoding="utf-8") as f:
        f.write(f"-- {mod} E2 验证脚本(自动生成,需在 DM8 环境执行)\n")
        f.write(f"-- 语句数:{len(recs)};生成日期:2026-09-06\n")
        f.write("-- 注意:仅验证语法可执行性(SELECT 返回列/类型),不验证结果等价性\n")
        f.write("-- 期望结果:全部语句编译通过,SELECT 语句返回结果集\n\n")
        ok = 0
        skip = 0
        for r in recs:
            sid = r["sql_id"]
            anchor = r["active_sql_anchor"] or r["anchor"]
            lines = get_lines(mod, r["path"])
            sql = extract_active_sql(lines, anchor)
            if not sql:
                # 尝试从注释行后取
                m = re.match(r"^L(\d+)$", anchor)
                if m:
                    ln = int(m.group(1))
                    if ln < len(lines):
                        sql = re.sub(r'"\s*', '', lines[ln - 1]).strip()
            if not sql or len(sql) < 5:
                f.write(f"-- [{sid}] 无法提取 SQL(anchor={anchor})\n\n")
                skip += 1
                continue
            sql = to_test_sql(sql)
            f.write(f"-- [{sid}] {r['path']} {anchor}\n")
            # UPDATE/DELETE 加 ROLLBACK 保护
            kw = sql[:6].upper()
            if kw.startswith("UPDATE") or kw.startswith("DELETE") or kw.startswith("INSERT"):
                f.write(f"-- 以下为写操作,执行前确认在测试环境!\n")
            f.write(f"{sql};\n\n")
            ok += 1
        print(f"{mod}: {ok} 条写入, {skip} 条跳过")
        grand += ok

print(f"总计写入 {grand} 条 E2 验证语句")
