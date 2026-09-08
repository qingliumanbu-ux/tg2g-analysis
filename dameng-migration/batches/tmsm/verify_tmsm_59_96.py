# -*- coding: utf-8 -*-
"""严格校验 tmsme59/96:摘除新增注释行、活动块还原为注释中的原行后,
应与改前备份逐字节一致。"""
import hashlib

D = r"D:\work\company\太钢二炼钢\analysis\dameng-migration\batches\tmsm"
SRC = r"D:\work\company\太钢二炼钢\Server\TMSM\p_tmsm_7160"

for name in ("tmsme59_inq.cpp", "tmsme96_inq.cpp"):
    bak = open(D + "\\" + name + ".pre-dm8.bak", "rb").read() \
        .decode("gb18030").split("\n")
    new = open(SRC + "\\" + name, "rb").read().decode("gb18030").split("\n")
    restored = []
    i, n = 0, len(new)
    while i < n:
        s = new[i].lstrip("\t ")
        if s.startswith("// DM8 适配 CHANGE-1"):
            k = i + 4  # 跳过 4 行头(适配/原因/共用分支/原SQL标记)
            while not new[k].lstrip("\t ").startswith("// DM8 SQL："):
                k += 1
            commented = new[i + 4:k]
            for c in commented:
                ll = len(c) - len(c.lstrip("\t "))
                restored.append(c[:ll] + c[ll + 3:])
            # 跳过活动块(行数 = 注释行数)
            i = k + 1 + len(commented)
            continue
        restored.append(new[i])
        i += 1
    same = restored == bak
    print(name, "严格还原一致:", same)
    if not same:
        for a, b in zip(restored, bak):
            if a != b:
                print("  新:", repr(a[:100]))
                print("  原:", repr(b[:100]))
                break
    print("  sha256:", hashlib.sha256(
        open(SRC + "\\" + name, "rb").read()).hexdigest())
