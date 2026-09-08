# -*- coding: utf-8 -*-
"""CHANGE-107:wmsmsmj3_rcm.cpp 吊车号 DECODE 改标准 CASE。"""
import hashlib
import re
import shutil

SRC = r"D:\work\company\太钢二炼钢\Server\WMSM\p_wmsm_8120\wmsmsmj3_rcm.cpp"
BAK = r"D:\work\company\太钢二炼钢\analysis\dameng-migration\batches\wmsm\wmsmsmj3_rcm.pre-dm8.bak"

Q = "'"  # 单引号
DQ = '"'  # 双引号

shutil.copyfile(SRC, BAK)
with open(SRC, "rb") as f:
    text = f.read().decode("gb18030")
lines = text.split("\n")

idx = None
for i, l in enumerate(lines):
    if "crane_no = decode(" in l:
        idx = i
        break
assert idx is not None, "未找到目标行"
orig = lines[idx]
lead = orig[:len(orig) - len(orig.lstrip("\t "))]
core = orig.lstrip("\t ")

# 第二个 decode:v_crane_no 为空(NULL/空串)时取 crane_no,否则取 v_crane_no
m = re.search(r"crane_no = decode\(.*\) order by crane_no", core)
assert m, "模式未找到"
old_expr = m.group(0)

v_lit = Q + DQ + " + v_crane_no + " + DQ + Q          # ' + v_crane_no + '
new_expr = (
    "crane_no = CASE WHEN " + v_lit + " IS NULL OR "
    + v_lit + " = " + Q + Q + " THEN crane_no ELSE " + v_lit
    + " END order by crane_no"
)

header = [
    lead + "// DM8 适配 CHANGE-107：吊车号过滤：吊车号为空(NULL 或空串)时不过滤，否则按吊车号过滤；语义与原 DECODE 的 Oracle 行为一致。",
    lead + "// 改写原因：DECODE 以空串和 NULL 为搜索值，其匹配语义在 DM 未记载且随空串配置变化；改为标准 CASE(WHEN v IS NULL OR v = '')任何配置下行为确定；DM8 尚未实测。",
    lead + "// 本语句为动态拼接，共用分支面向 DM8；过滤条件与排序保持不变。",
    lead + "// 原 SQL（完整保留）：",
    lead + "// " + core,
    lead + "// DM8 SQL：",
]
new_line = lead + core.replace(old_expr, new_expr)
lines[idx:idx + 1] = header + [new_line]

with open(SRC, "wb") as f:
    f.write("\n".join(lines).encode("gb18030"))

# 验证:注释还原
with open(BAK, "rb") as f:
    orig_lines = f.read().decode("gb18030").split("\n")
rec = []
for c in header[4:5]:
    ll = len(c) - len(c.lstrip("\t "))
    rec.append(c[:ll] + c[ll + 3:])
assert rec[0] == orig, "注释还原不一致"
with open(SRC, "rb") as f:
    raw = f.read()
print("OK CHANGE-107 应用;注释还原一致;sha256:",
      hashlib.sha256(raw).hexdigest())
