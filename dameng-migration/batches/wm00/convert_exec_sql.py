# -*- coding: utf-8 -*-
"""EXEC SQL 方案B试点:WM00 f_wm00_stock_place_no.cpp 选两条改为 CDbCommand。
原 EXEC SQL 保留注释,方案A/B 并存,后期确认后放开其一。"""
import hashlib
import shutil

SRC = r"D:\work\company\太钢二炼钢\Server\WM00\libWM00\f_wm00_stock_place_no.cpp"
BAK = r"D:\work\company\太钢二炼钢\analysis\dameng-migration\batches\wm00\f_wm00_stock_place_no.exec-bak"
Q = "'"

shutil.copyfile(SRC, BAK)
with open(SRC, "rb") as f:
    lines = f.read().decode("gb18030").split("\n")

# ---- 转换1: L132-137 UPDATE ----
# 找 EXEC SQL UPDATE 区块
upd_start = None
for i, l in enumerate(lines):
    if "EXEC SQL" in l and "UPDATE" in l.upper():
        upd_start = i
        break
# EXEC SQL UPDATE 可能跨行,找分号
upd_end = upd_start
while upd_end < len(lines) and ";" not in lines[upd_end]:
    upd_end += 1
assert upd_start is not None, "UPDATE not found"

lead = lines[upd_start][:len(lines[upd_start]) - len(lines[upd_start].lstrip())]
orig_upd = lines[upd_start:upd_end + 1]

hdr1 = [
    lead + "// DM8 适配 CHANGE-EXEC-001:更新缺陷重量;EXEC SQL 改为 CDbCommand 调用(方案B试点)。",
    lead + "// 改写原因:EXEC SQL 嵌入式需 DB2 预编译器;方案B 改为 CDbCommand 参数绑定,消除预编译器依赖。",
    lead + "// 注意:方案A(保留 EXEC SQL)与方案B(CDbCommand)并存,后期确认构建系统支持后二选一。",
    lead + "// 原方案A(EXEC SQL,完整保留):",
]
for ol in orig_upd:
    hdr1.append(lead + "// " + ol.strip())
hdr1.append(lead + "// 方案B(CDbCommand):")
# 方案B
new_upd = [
    lead + '\tsqlstr = " UPDATE TMMSM01 SET DEFECT_WT = ?, SPARE_ITEM_N3 = ? WHERE mat_no = ? AND mat_position = \'1\'";',
    lead + "\tcmd_x1j197b.SetCommandText(sqlstr);",
    lead + "\tcmd_x1j197b.Parameters.Set(\"p1\", x1j197b.head_width);",
    lead + "\tcmd_x1j197b.Parameters.Set(\"p2\", x1j197b.tail_width);",
    lead + "\tcmd_x1j197b.Parameters.Set(\"p3\", tmmsm01.mat_no);",
    lead + "\tcmd_x1j197b.Execute();",
]
lines[upd_start:upd_end + 1] = hdr1 + new_upd

# ---- 转换2: SELECT INTO ----
# 重新定位(行号已偏移)
sel_start = None
for i, l in enumerate(lines):
    if "EXEC SQL" in l and "select" in l.lower() and "into" in l.lower():
        sel_start = i
        break
sel_end = sel_start
while sel_end < len(lines) and ";" not in lines[sel_end]:
    sel_end += 1
assert sel_start is not None, "SELECT INTO not found"

lead2 = lines[sel_start][:len(lines[sel_start]) - len(lines[sel_start].lstrip())]
orig_sel = lines[sel_start:sel_end + 1]

hdr2 = [
    lead2 + "// DM8 适配 CHANGE-EXEC-002:按板坯号查 tmmsm01;EXEC SQL 改为 CDbCommand(方案B试点)。",
    lead2 + "// 改写原因:同 CHANGE-EXEC-001;SELECT INTO :host_var 改为 ExecuteQuery。",
    lead2 + "// 原方案A(EXEC SQL,完整保留):",
]
for ol in orig_sel:
    hdr2.append(lead2 + "// " + ol.strip())
hdr2.append(lead2 + "// 方案B(CDbCommand):")

new_sel = [
    lead2 + '\tsqlstr = " SELECT * FROM tmmsm01 WHERE mat_no = ? AND mat_position IN(\'1\',\'2\')";',
    lead2 + "\tcmd_inq.SetCommandText(sqlstr);",
    lead2 + "\tcmd_inq.Parameters.Set(\"mat_no\", tmmsm01.mat_no);",
    lead2 + "\tcmd_inq.ExecuteQuery(tmmsm01);",
    lead2 + "\tif (tmmsm01.Rows.get_Count() == 0)  // 等价于 sqlca.sqlcode == M_NO_DATA_FOUND",
]
# 保留后续 sqlcode 判断块(更新条件)
# 找原 sqlcode 判断
for k in range(sel_end + 1, min(sel_end + 5, len(lines))):
    if "sqlca.sqlcode" in lines[k]:
        new_sel.append(lines[k])
        break

lines[sel_start:sel_end + 1] = hdr2 + new_sel

with open(SRC, "wb") as f:
    f.write("\n".join(lines).encode("gb18030"))

# 校验
bak = open(BAK, "rb").read().decode("gb18030").split("\n")
print("原文件行数:", len(bak), "; 转换后:", len(lines))
print("方案A注释行:", sum(1 for l in lines if "原方案A" in l))
print("方案B活动行:", sum(1 for l in lines if "方案B(CDbCommand)" in l))
print("sha256:", hashlib.sha256(open(SRC, "rb").read()).hexdigest()[:20])
