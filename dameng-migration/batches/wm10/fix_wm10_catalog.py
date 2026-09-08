# -*- coding: utf-8 -*-
"""WM10 wm11/12/17/a2_inq.cpp:SYSIBM.SYSTABLES 表存在性查询改为 ALL_TABLES
(共用路径,无 DB_KIND 分支;DM 的 Oracle 兼容视图)。"""
import hashlib
import shutil

OLD = "SELECT Name FROM SYSIBM.SYSTABLES WHERE TID <> 0 AND Name IN( 'TMMCR01','TMMHR01','TMMSM01','TMMHP01','TMMBW01')"
NEW = "SELECT table_name FROM ALL_TABLES WHERE table_name IN( 'TMMCR01','TMMHR01','TMMSM01','TMMHP01','TMMBW01')"
FILES = [
    r"D:\work\company\太钢二炼钢\Server\WM10\p_wm10_8630\wm11_inq.cpp",
    r"D:\work\company\太钢二炼钢\Server\WM10\p_wm10_8630\wm12_inq.cpp",
    r"D:\work\company\太钢二炼钢\Server\WM10\p_wm10_8630\wm17_inq.cpp",
    r"D:\work\company\太钢二炼钢\Server\WM10\p_wm10_8630\wma2_inq.cpp",
]
BAKDIR = r"D:\work\company\太钢二炼钢\analysis\dameng-migration\batches\wm10"
import os
os.makedirs(BAKDIR, exist_ok=True)

no = 0
for SRC in FILES:
    no += 1
    cid = f"CHANGE-{288 + no}"  # 占位,终态由全局重编号统一
    name = os.path.basename(SRC).split(".")[0]
    BAK = os.path.join(BAKDIR, name + ".pre-dm8.bak")
    shutil.copyfile(SRC, BAK)
    with open(SRC, "rb") as f:
        lines = f.read().decode("gb18030").split("\n")
    idx = None
    for i, l in enumerate(lines):
        if "SYSIBM.SYSTABLES" in l:
            idx = i
            break
    assert idx is not None, SRC
    orig = lines[idx]
    lead = orig[:len(orig) - len(orig.lstrip("\t "))]
    core = orig.lstrip("\t ")
    assert OLD in core, core[:120]
    header = [
        lead + f"// DM8 适配 {cid}:检查主档表是否存在;DB2 目录表 SYSIBM.SYSTABLES 改为 DM 的 Oracle 兼容视图 ALL_TABLES。",
        lead + "// 改写原因:DM 无 SYSIBM.SYSTABLES;ALL_TABLES 为 DM 官方 Oracle 兼容视图;原 TID<>0 条件随目录表一并去除;大小写与 IN 列表保持。",
        lead + "// 注意:原 DB2 语义为全库范围,ALL_TABLES 限当前用户可见范围;主档表与应用同 schema 时等价(schema 布局属部署契约,见台账)。",
        lead + "// 本语句为共用路径(无 DB_KIND 分支),DM8 直接执行;返回列用法 Rows[0][0] 保持不变;DM8 尚未实测。",
        lead + "// 原 SQL(完整保留):",
        lead + "// " + core,
        lead + "// DM8 SQL:",
    ]
    new_core = core.replace(OLD, NEW)
    lines[idx:idx + 1] = header + [lead + new_core]
    with open(SRC, "wb") as f:
        f.write("\n".join(lines).encode("gb18030"))
    # 还原校验
    bak = open(BAK, "rb").read().decode("gb18030").split("\n")
    rec = []
    i = 0
    while i < len(lines):
        if lines[i].lstrip("\t ").startswith(f"// DM8 适配 {cid}:"):
            k = i + 4
            while not lines[k].lstrip("\t ").startswith("// DM8 SQL:"):
                k += 1
            for c in lines[i + 4:k]:
                ll = len(c) - len(c.lstrip("\t "))
                rec.append(c[:ll] + c[ll + 3:])
            i = k + 2
            continue
        rec.append(lines[i])
        i += 1
    print(name, "还原一致:", rec == bak,
          hashlib.sha256(open(SRC, "rb").read()).hexdigest()[:16])
