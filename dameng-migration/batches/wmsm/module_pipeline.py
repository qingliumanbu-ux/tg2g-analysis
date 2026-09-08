# -*- coding: utf-8 -*-
"""模块流水线:scan / preview / apply / finalize。

用法:
  python module_pipeline.py scan <M>      # 扫描方言命中
  python module_pipeline.py preview <M>   # 批量预览,输出 <M>-all-previews.txt
  python module_pipeline.py apply <M>     # 对有转换的文件批量 apply
  python module_pipeline.py finalize <M> [hr_id]  # 重编号+入账+HR标记+残留+统计
hr_id:该模块 TIMESTAMPDIFF 块的人工复核编号(默认 HR-006)。
"""
import csv
import hashlib
import io
import os
import re
import subprocess
import sys

sys.path.insert(0, r"D:\work\company\太钢二炼钢\analysis\dameng-migration\batches\wmsm")
import dm8lib

BASE = r"D:\work\company\太钢二炼钢\Server"
ANALYSIS = r"D:\work\company\太钢二炼钢\analysis\dameng-migration"
HERE = os.path.dirname(os.path.abspath(__file__))
HEAD = re.compile(r"//\s*DM8 适配 CHANGE-(\d+)：")
RES = re.compile(
    r"SYSIBM\.|[+-]\s*\d+\s+DAYS?\b|\)\s+DAYS?\b|\bDAYS\s*\("
    r"|'\s*ROWNUM|ORDER\s+BY\s+ROWNUM"
    r"|\bAS\s+INT\b|\bNO\s+CACHE\b|nextval\s+for|(?<![.\w])value\s*\("
    r"|\bSUBSTR2\s*\(|INTERVAL\s+'"
    r"|\d+\s+(?:HOUR|MINUTE|SECOND)S?\b", re.I)


def git_clean(mod):
    r = subprocess.run(["git", "-C", os.path.join(BASE, mod), "status",
                        "--porcelain"], capture_output=True, text=True)
    mods = [l[3:].strip() for l in r.stdout.splitlines()
            if l.startswith(" M ")]
    return mods


def scan(mod):
    src = io.open(os.path.join(ANALYSIS, "batches", "pssm_scan.py"),
                  encoding="utf-8").read()
    src = src.replace(r"Server\PSSM", f"Server\\{mod}")
    src = src.replace(r"batches\pssm", f"batches\\{mod.lower()}")
    src = src.replace("pssm-scan-summary.csv", f"{mod.lower()}-scan-summary.csv")
    src = src.replace("pssm-dialect-hits.tsv", f"{mod.lower()}-dialect-hits.tsv")
    src = src.replace("pssm-sql-statements.tsv", f"{mod.lower()}-sql-statements.tsv")
    os.makedirs(os.path.join(ANALYSIS, "batches", mod.lower()), exist_ok=True)
    sp = os.path.join(ANALYSIS, "batches", mod.lower(), "scan.py")
    io.open(sp, "w", encoding="utf-8", newline="").write(src)
    r = subprocess.run([sys.executable, sp], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    print(r.stdout.strip())


def hit_files(mod):
    hf = os.path.join(ANALYSIS, "batches", mod.lower(),
                      f"{mod.lower()}-dialect-hits.tsv")
    lines = io.open(hf, encoding="utf-8").read().splitlines()[1:]
    return sorted({l.split("\t", 2)[0] for l in lines
                   if not l.split("\t", 2)[2].strip().startswith("case DB_KIND_")})


def preview(mod):
    dm8lib.set_module(mod)
    files = hit_files(mod)
    print("files to preview:", len(files))
    allprev = io.open(os.path.join(ANALYSIS, "batches", mod.lower(),
                                   f"{mod.lower()}-all-previews.txt"), "w",
                      encoding="utf-8")
    conv = []
    for f in files:
        r = subprocess.run([sys.executable, os.path.join(HERE, "dm8lib.py"),
                            "preview", f, mod], capture_output=True,
                           text=True, encoding="utf-8", errors="replace")
        out = (r.stdout + r.stderr).strip().splitlines()
        line = out[0] if out else "(none)"
        m = re.search(r"converted=(\d+)", line)
        name = os.path.basename(f).split(".")[0]
        pf = os.path.join(ANALYSIS, "batches", mod.lower(),
                          f"{name}-preview.txt")
        if m and int(m.group(1)) > 0:
            conv.append((f, int(m.group(1))))
            if os.path.exists(pf):
                allprev.write(f"######## {f}\n"
                              + io.open(pf, encoding="utf-8").read() + "\n")
        if r.returncode != 0:
            print("!!", f, line, (r.stderr or "")[-200:])
    allprev.close()
    print("files with conversions:", len(conv),
          "; total blocks:", sum(n for _, n in conv))
    for f, n in sorted(conv, key=lambda x: -x[1]):
        print(f'{n:>3}  {f}')


def apply(mod):
    dm8lib.set_module(mod)
    files = hit_files(mod)
    for f in files:
        r = subprocess.run([sys.executable, os.path.join(HERE, "dm8lib.py"),
                            "apply", f, mod], capture_output=True,
                           text=True, encoding="utf-8", errors="replace")
        out = (r.stdout + r.stderr).strip().splitlines()
        first = out[0] if out else "(none)"
        m = re.search(r"converted=(\d+)", first)
        if r.returncode != 0 or (m and int(m.group(1)) > 0):
            print(first)
            for l in out[1:]:
                if l.startswith("!!"):
                    print("  ", l)
    print("apply done")


def finalize(mod, hr_id="HR-006"):
    dm8lib.set_module(mod)
    n = dm8lib.max_change_no()
    known = set()
    for r in csv.DictReader(io.open(dm8lib.LEDGER, encoding="utf-8-sig")):
        if re.match(r"CHANGE-\d+$", r.get("sql_id", "")):
            known.add(r["sql_id"])
    modified = [m for m in git_clean(mod) if m.endswith(".cpp")]
    for rel in sorted(modified):
        path = os.path.join(dm8lib.ROOT, rel)
        raw = open(path, "rb").read()
        try:
            text = raw.decode("utf-8"); enc = "utf-8"
        except UnicodeDecodeError:
            text = raw.decode("gb18030"); enc = "gb18030"
        lines = text.split("\n")
        fresh = [(i, HEAD.search(l).group(1)) for i, l in enumerate(lines)
                 if HEAD.search(l)
                 and f"CHANGE-{HEAD.search(l).group(1)}" not in known]
        for i, g in fresh:
            n += 1
            lines[i] = HEAD.sub(f"// DM8 适配 CHANGE-{n}：", lines[i], count=1)
        if fresh:
            open(path, "wb").write("\n".join(lines).encode(enc))
    print(f"renumber done, global max CHANGE-{n}; modified files: {len(modified)}")

    for f in hit_files(mod):
        subprocess.run([sys.executable, os.path.join(HERE, "dm8lib.py"),
                        "ledger", f, mod], capture_output=True)
    # 批量入账其余文件
    led = dm8lib.LEDGER
    done = {r["path"] for r in csv.DictReader(
        io.open(led, encoding="utf-8-sig")) if r["module"] == mod}
    allf = []
    for p in pathlib_all(dm8lib.ROOT):
        rel = p.relative_to(dm8lib.ROOT).as_posix()
        if rel not in done:
            allf.append(rel)
    for f in allf:
        subprocess.run([sys.executable, os.path.join(HERE, "dm8lib.py"),
                        "ledger", f, mod], capture_output=True)
    print("ledger done; bulk files:", len(allf))

    rows = list(csv.DictReader(io.open(led, encoding="utf-8-sig", newline="")))
    hr = 0
    for r in rows:
        if r["module"] != mod or r["decision"] not in ("可保留", "已转换"):
            continue
        try:
            s, e = r["anchor"].lstrip("L").split("-L")
        except ValueError:
            continue
        p = os.path.join(dm8lib.ROOT, r["path"])
        if not os.path.exists(p):
            continue
        lines, _, _ = dm8lib.read_lines(p)
        blk = "\n".join(lines[int(s) - 1:int(e)])
        if re.search(r"TIMESTAMPDIFF", blk, re.I):
            if r["decision"] == "已转换":
                r["status"] = (f"待人工复核(时长口径;其余方言已转换,见{r['sql_id']})")
            else:
                r["status"] = f"待人工复核(时长口径,见{hr_id})"
            r["decision"] = "待人工复核"
            r["human_review_id"] = hr_id
            r["local_dependency"] = ("需用户选定口径后整条改写 TIMESTAMPDIFF;"
                                     "DM8 无两参数形式")
            r["evidence"] = ("IBM TIMESTAMPDIFF 定义 + DM DATEDIFF;口径未定不改写;"
                             "块内其他方言已按 CHANGE 完成")
            hr += 1
    with io.open(led, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=dm8lib.FIELDS)
        w.writeheader()
        w.writerows(rows)
    print(f"HR rows ({hr_id}):", hr)

    # 残留复扫
    hf = os.path.join(ANALYSIS, "batches", mod.lower(),
                      f"{mod.lower()}-dialect-hits.tsv")
    if os.path.exists(hf):
        lines = io.open(hf, encoding="utf-8").read().splitlines()[1:]
        bad = 0
        kinds = {}
        for l in lines:
            parts = l.split("\t", 2)
            if len(parts) < 3:
                continue
            f2, ln, tx = parts
            if tx.strip().startswith("case DB_KIND_"):
                continue
            m = RES.search(tx)
            if m:
                bad += 1
                k = m.group(0).upper()[:20]
                kinds[k] = kinds.get(k, 0) + 1
        print("residue(active, incl. HR-pending & keeps):", bad, kinds)

    rows = [r for r in csv.DictReader(io.open(led, encoding="utf-8-sig"))
            if r["module"] == mod]
    from collections import Counter
    print(f"{mod} rows:", len(rows), "| files:", len({r['path'] for r in rows}))
    print(Counter(r["decision"] for r in rows))


def pathlib_all(root):
    import pathlib
    return [p for p in pathlib.Path(root).rglob("*.cpp")
            if ".git" not in p.parts]


def main():
    mode, mod = sys.argv[1], sys.argv[2]
    hr = sys.argv[3] if len(sys.argv) > 3 else "HR-006"
    if mode == "scan":
        scan(mod)
    elif mode == "preview":
        preview(mod)
    elif mode == "apply":
        apply(mod)
    elif mode == "finalize":
        finalize(mod, hr)
    else:
        print("unknown mode")


if __name__ == "__main__":
    main()
