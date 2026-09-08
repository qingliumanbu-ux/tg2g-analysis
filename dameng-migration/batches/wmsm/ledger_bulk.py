# -*- coding: utf-8 -*-
"""对 WMSM 剩余文件批量入账;输出意外转换与错误。"""
import os
import subprocess
import sys

BASE = r"D:\work\company\太钢二炼钢\Server\WMSM"
HERE = r"D:\work\company\太钢二炼钢\analysis\dameng-migration\batches\wmsm"
PY = sys.executable


def norm(p):
    return p.replace("\\", "/")


def main():
    done = set()
    for name in ("_done.txt", "_todo.txt"):
        path = os.path.join(HERE, name)
        if os.path.exists(path):
            done |= {x.strip() for x in open(path, encoding="utf-8")
                     if x.strip()}
    allf = []
    for dp, dn, fn in os.walk(BASE):
        if ".git" in dn:
            dn.remove(".git")
        for n in fn:
            if n.lower().endswith(".cpp"):
                allf.append(norm(os.path.relpath(os.path.join(dp, n), BASE)))
    rest = [f for f in sorted(allf) if f not in done]
    print("remaining files:", len(rest))
    for f in rest:
        r = subprocess.run([PY, os.path.join(HERE, "dm8lib.py"),
                            "ledger", f],
                           capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        out = (r.stdout + r.stderr).strip().splitlines()
        line = out[0] if out else "(no output)"
        interesting = ("converted=" in line and " converted=0 " not in line
                       and not line.endswith("converted=0"))
        if interesting or r.returncode != 0 or "Traceback" in (r.stdout + r.stderr):
            print(">>", line)
            if r.returncode != 0:
                print(r.stdout[-500:], r.stderr[-500:])
    print("bulk ledger done")


if __name__ == "__main__":
    main()
