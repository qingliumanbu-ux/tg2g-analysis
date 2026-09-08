# -*- coding: utf-8 -*-
"""跨文件全局唯一化 CHANGE 编号(仅改注释头标签,行数不变)。"""
import io
import os
import subprocess
import sys

ROOT = r"D:\work\company\太钢二炼钢\Server\WMSM"
HERE = r"D:\work\company\太钢二炼钢\analysis\dameng-migration\batches\wmsm"

# (文件, {旧: 新}) —— 按处理顺序编到 85 之后
PLAN = [
    ("p_wmsm_8130/wmsm02_sg_inq.cpp", {66 + i: 85 + i for i in range(10)}),
    ("p_wmsm_8110/wmsm01gg_inq1.cpp", {66: 95, 67: 96}),
    ("p_wmsm_8110/wmsmsm11_inq.cpp", {66: 97}),
    ("p_wmsm_8130/wmsm01q0q_inq1.cpp", {66: 98}),
    ("p_wmsm_8180/wmsmpcgz_inq.cpp", {66: 99}),
    ("p_wmsm_8140/wm00_stockNo2.cpp", {66: 100, 67: 101}),
    ("p_wmsm_8140/wmsmhrzc_auto.cpp", {66: 102}),
    ("p_wmsm_8140/wmsmrsl_inq.cpp", {66: 103}),
    ("p_wmsm_8190/cm_p3t801_rcv.cpp", {66: 104}),
    ("libWMSM/f_wmsmsm_cranecmd_update.cpp", {66: 105}),
    ("p_wmsm_8140/wmsmsc_inq1.cpp", {66: 106}),
]

for rel, mapping in PLAN:
    path = os.path.join(ROOT, rel)
    with open(path, "rb") as f:
        raw = f.read()
    text = raw.decode("gb18030")
    for old, new in mapping.items():
        token_old = f"// DM8 适配 CHANGE-{old}："
        token_new = f"// DM8 适配 CHANGE-{new}："
        cnt = text.count(token_old)
        if cnt != 1:
            print(f"!! {rel}: CHANGE-{old} 出现 {cnt} 次,跳过")
            continue
        text = text.replace(token_old, token_new)
    with open(path, "wb") as f:
        f.write(text.encode("gb18030"))
    print(f"OK {rel}: {mapping}")
