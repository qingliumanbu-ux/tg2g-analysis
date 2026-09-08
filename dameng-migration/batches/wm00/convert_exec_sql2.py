# -*- coding: utf-8 -*-
"""EXEC SQL 方案B试点(精确版):WM00 f_wm00_stock_place_no.cpp 选 L150 和 L811。
每条:EXEC SQL 行注释保留 → CDbCommand 方案B写在下方。
sqlca.sqlcode 判断注释保留 → 等价 CDbCommand 判断写在下方。"""
import hashlib
import shutil

SRC = r"D:\work\company\太钢二炼钢\Server\WM00\libWM00\f_wm00_stock_place_no.cpp"
BAK = r"D:\work\company\太钢二炼钢\analysis\dameng-migration\batches\wm00\f_wm00_stock_place_no.exec-bak"
shutil.copyfile(SRC, BAK)

with open(SRC, "rb") as f:
    lines = f.read().decode("gb18030").split("\n")

# ===== L150 (0-based 149): SELECT INTO :tmmsm01 =====
# 原始(0-based): 149=EXEC SQL行, 150=sqlca判断行
lead = lines[149][:len(lines[149]) - len(lines[149].lstrip())]

repl_150 = [
    lead + "// DM8 适配 CHANGE-EXEC-001:按板坯号查 tmmsm01;EXEC SQL 改为 CDbCommand(方案B试点)。",
    lead + "// 改写原因:EXEC SQL 需 DB2 预编译器;方案B 改为 CDbCommand 消除预编译器依赖。",
    lead + "// 注意:方案A/B 并存,后期确认构建系统支持 DM dpc 后二选一。",
    lead + "// 原方案A(EXEC SQL,完整保留):",
    lead + "// " + lines[149].strip(),
    lead + "// 原 sqlca 判断(完整保留):",
    lead + "// " + lines[150].strip(),
    lead + "// 方案B(CDbCommand):",
    lead + '\tsqlstr = " SELECT * FROM tmmsm01 WHERE mat_no = ? AND mat_position IN(\'1\',\'2\')";',
    lead + "\tcmd_inq.SetCommandText(sqlstr);",
    lead + "\tcmd_inq.Parameters.Set(\"mat_no\", tmmsm01.mat_no);",
    lead + "\tcmd_inq.ExecuteQuery(tmmsm01);",
    lead + "\tif (tmmsm01.Rows.get_Count() == 0)  // 等价于 sqlca.sqlcode == M_NO_DATA_FOUND",
]
# L150 和 L151 替换为 13 行
lines[149:151] = repl_150

# ===== L811 (0-based,现在偏移了 11 行 → 811-1+11 = 821) =====
# 找偏移后的位置
off = len(repl_150) - 2  # 新增 11 行
l811_idx = 810 + off  # 0-based 810 → 偏移后 821

lead2 = lines[l811_idx][:len(lines[l811_idx]) - len(lines[l811_idx].lstrip())]

repl_811 = [
    lead2 + "// DM8 适配 CHANGE-EXEC-002:按板坯号查 tmmsm01(仅 mat_position='1');EXEC SQL 改为 CDbCommand(方案B试点)。",
    lead2 + "// 改写原因:同 CHANGE-EXEC-001。",
    lead2 + "// 原方案A(EXEC SQL,完整保留):",
    lead2 + "// " + lines[l811_idx].strip(),
    lead2 + "// 方案B(CDbCommand):",
    lead2 + '\tsqlstr = " SELECT * FROM tmmsm01 WHERE mat_no = ? AND mat_position = \'1\'";',
    lead2 + "\tcmd_inq.SetCommandText(sqlstr);",
    lead2 + "\tcmd_inq.Parameters.Set(\"mat_no\", tmmsm01.mat_no);",
    lead2 + "\tcmd_inq.ExecuteQuery(tmmsm01);",
]
# L811 替换为 9 行
lines[l811_idx:l811_idx + 1] = repl_811

with open(SRC, "wb") as f:
    f.write("\n".join(lines).encode("gb18030"))

# 验证:方案B行存在、原EXEC SQL已注释
import io
out = io.open(r"D:\work\company\太钢二炼钢\analysis\dameng-migration\batches\wm00\_verify.txt",
              "w", encoding="utf-8")
for i, l in enumerate(lines, 1):
    if "CHANGE-EXEC" in l or "方案B" in l:
        out.write(f"L{i}\t{l.strip()[:140]}\n")
    if "EXEC SQL" in l and "原方案A" not in l and not l.strip().startswith("//"):
        out.write(f"!! 未注释 L{i}\t{l.strip()[:140]}\n")
out.close()
import hashlib
print("转换完成 sha256:", hashlib.sha256(open(SRC, "rb").read()).hexdigest()[:20])
