# -*- coding: utf-8 -*-
"""tmsme59_inq.cpp 从干净备份重新转换全部 TIMESTAMPDIFF(5条)。
同时修正 HR-001 的 CAST→TO_TIMESTAMP。每条注释写清楚。"""
import hashlib
import shutil

BAK = r"D:\work\company\太钢二炼钢\analysis\dameng-migration\batches\tmsm\tmsme59_inq.pre-dm8.bak"
SRC = r"D:\work\company\太钢二炼钢\Server\TMSM\p_tmsm_7160\tmsme59_inq.cpp"
DQ = '"'
SQ = "'"
FMT = SQ + "YYYYMMDDHH24MISS" + SQ

shutil.copyfile(BAK, SRC)
with open(SRC, "rb") as f:
    lines = f.read().decode("gb18030").split("\n")
print(f"从备份恢复: {len(lines)} 行")

# 1. HR-001: CAST AS TIMESTAMP → TO_TIMESTAMP
for i, l in enumerate(lines):
    if "CAST(" in l and "AS TIMESTAMP" in l:
        lines[i] = l.replace("CAST(", "TO_TIMESTAMP(").replace(" AS TIMESTAMP)", "," + FMT + ")")
        print(f"HR-001 修正 L{i+1}")

# 2. TIMESTAMPDIFF 转换(底部往上)
def find_ts(lines, unit, keyword, from_line=0):
    for i in range(len(lines)):
        if "TIMESTAMPDIFF(" in lines[i] and keyword in lines[i]:
            return i
    return None

def convert_ts(lines, idx0, cid, biz, unit_div, unit_name):
    end = idx0
    while end < len(lines) and ";" not in lines[end]:
        end += 1
    lead = lines[idx0][:len(lines[idx0]) - len(lines[idx0].lstrip())]
    orig = lines[idx0:end + 1]

    comment = [
        lead + "// DM8 适配 " + cid + ":" + biz,
        lead + "// 改写原因:DB2 两参数 TIMESTAMPDIFF 改为 DM8 标准写法(实际完整时长)。",
        lead + "// 口径:HR-002 已确认选①实际完整时长——不满 1 个单位不算,与 DB2 原行为一致。",
        lead + "// 改写公式:DB2 TIMESTAMPDIFF(" + unit_name + ") 改为 DM8 DATEDIFF(SECOND, 起点, 终点) / " + str(unit_div),
        lead + "//   整数除法自动舍去不满整数的部分,与 DB2 TIMESTAMPDIFF 行为一致。",
        lead + "// 时间格式:HR-001 确认全库时间为 YYYYMMDDHH24MISS(14位紧凑),用 TO_TIMESTAMP 显式指定。",
        lead + "// 原 SQL(完整保留):",
    ]
    for ol in orig:
        comment.append(lead + "// " + ol.strip())
    comment.append(lead + "// DM8 SQL:")

    # 从原始行提取 C++ 表达式部分
    joined = " ".join(x.strip() for x in orig)
    # 找 START 和 END 的表达式
    m_end = re.search(r"TIMESTAMP\('" + chr(34) + r"\s*\+\s*(.+?)\s*\+\s*" + chr(34), joined)
    parts = joined.split(" - ")
    if len(parts) >= 2:
        end_part = parts[0].replace("TIMESTAMP(", "").replace(")", "").strip()
        start_part = parts[-1].replace("TIMESTAMP(", "").replace(")", "").strip().rstrip(";").strip()
        # 提取纯 C++ 表达式(去掉引号)
        end_cpp = end_part.strip(SQ).strip(DQ).strip()
        start_cpp = start_part.strip(SQ).strip(DQ).strip()
    else:
        end_cpp = ""
        start_cpp = ""

    # 构建 C++ 代码行
    # 模式: sqlstr = "select DATEDIFF(SECOND, TO_TIMESTAMP('START_C++','fmt'), TO_TIMESTAMP('END_C++','fmt')) / div from DUAL";
    ts_start = "TO_TIMESTAMP('" + DQ + " + " + start_cpp + " + " + DQ + FMT + ")"
    ts_end = "TO_TIMESTAMP('" + DQ + " + " + end_cpp + " + " + DQ + FMT + ")"
    sql_body = "select DATEDIFF(SECOND, " + ts_start + ", " + ts_end + ") / " + str(unit_div) + " from DUAL"
    new_line = lead + "\t\tsqlstr = " + DQ + sql_body + DQ + ";"

    lines[idx0:end + 1] = comment + [new_line]

import re

# L262 (0-based 261): REPAIR_END - REPAIR_START, 分钟(4), 除数60
idx = find_ts(lines, "4", "REPAIR_END_TIME")
if idx is not None:
    convert_ts(lines, idx, "CHANGE-EXEC-101",
        "修理时间差分钟数:从 REPAIR_START_TIME 到 REPAIR_END_TIME 实际经过的完整分钟数",
        60, "4=分钟")
    print("EXEC-101 done")

# L224 (0-based 223): D_TIME - SUSPEND_TIME, 分钟
idx = find_ts(lines, "4", "D_TIME")
if idx is not None:
    convert_ts(lines, idx, "CHANGE-EXEC-100",
        "使用时间差分钟数:从 SUSPEND_TIME 到 D_TIME 实际经过的完整分钟数",
        60, "4=分钟")
    print("EXEC-100 done")

# L201 (0-based 200): SUSPEND_TIME - DEV_NAME, 分钟
idx = find_ts(lines, "4", "SUSPEND_TIME")
if idx is not None:
    convert_ts(lines, idx, "CHANGE-EXEC-099",
        "暂停时间差分钟数:从 DEV_NAME(存暂停开始时间)到 SUSPEND_TIME 实际经过的完整分钟数",
        60, "4=分钟")
    print("EXEC-099 done")

# L147 (0-based 146): CHANGE_TIME - REC_CREATE_TIME, 分钟
idx = find_ts(lines, "4", "REC_CREATE_TIME")
if idx is not None:
    convert_ts(lines, idx, "CHANGE-EXEC-098",
        "分钟差:从 REC_CREATE_TIME 到 CHANGE_TIME 实际经过的完整分钟数",
        60, "4=分钟")
    print("EXEC-098 done")

# L119 (0-based 118): CHANGE_TIME - REC_CREATE_TIME, 小时(8), 除数3600
idx = find_ts(lines, "8", "REC_CREATE_TIME")
if idx is not None:
    convert_ts(lines, idx, "CHANGE-EXEC-097",
        "小时差:从 REC_CREATE_TIME 到 CHANGE_TIME 实际经过的完整小时数",
        3600, "8=小时")
    print("EXEC-097 done")

with open(SRC, "wb") as f:
    f.write("\n".join(lines).encode("gb18030"))
print(f"全部转换完成: {len(lines)} 行")
print(f"sha256: {hashlib.sha256(open(SRC,'rb').read()).hexdigest()[:20]}")
