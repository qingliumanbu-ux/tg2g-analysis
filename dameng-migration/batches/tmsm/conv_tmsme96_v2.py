# -*- coding: utf-8 -*-
"""tmsme96_inq.cpp:按字段名识别 TIMESTAMPDIFF 类型,整行替换为 DM8 CDbCommand。
注释详细写明业务含义和改写公式。"""
import hashlib
import os
import re

SRC = r"D:\work\company\太钢二炼钢\Server\TMSM\p_tmsm_7160\tmsme96_inq.cpp"
DQ = '"'
FMT = SQ = "'"
FMT_STR = SQ + "YYYYMMDDHH24MISS" + SQ

with open(SRC, "rb") as f:
    lines = f.read().decode("gb18030").split("\n")

# 从底部往上处理
ts_lines = []
for i in range(len(lines) - 1, -1, -1):
    s = lines[i].strip()
    if "TIMESTAMPDIFF" in s and "sqlstr" in s and not s.startswith("//"):
        ts_lines.append(i)

print(f"找到 {len(ts_lines)} 条活跃 TIMESTAMPDIFF")

converted = 0
for idx0 in ts_lines:
    line = lines[idx0]
    lead = line[:len(line) - len(line.lstrip())]
    orig_line = line.strip()

    # 识别字段名
    end_field, start_field = "", ""
    if "CHANGE_TIME" in line and "REC_CREATE_TIME" in line:
        end_field, start_field = "CHANGE_TIME", "REC_CREATE_TIME"
        tbl = "ttmsm66"
    elif "END_TIME" in line and "START_TIME" in line:
        end_field, start_field = "END_TIME", "START_TIME"
        tbl = "dt_temp.Rows[j]"
    elif "E_DATETIME" in line and "S_DATETIME" in line:
        end_field, start_field = "E_DATETIME", "S_DATETIME"
        tbl = "dt_temp.Rows[j]"
    else:
        print(f"!! L{idx0+1} 未识别字段,跳过: {orig_line[:80]}")
        continue

    # 识别单位
    if "TIMESTAMPDIFF(8" in line:
        unit_div, unit_cn = "3600", "小时"
    elif "TIMESTAMPDIFF(4" in line:
        unit_div, unit_cn = "60", "分钟"
    elif "TIMESTAMPDIFF(2" in line:
        unit_div, unit_cn = "1", "秒"
    elif "TIMESTAMPDIFF(16" in line:
        unit_div, unit_cn = "86400", "天"
    else:
        print(f"!! L{idx0+1} 未识别单位")
        continue

    # 构建 C++ 宿主变量表达式
    if tbl == "ttmsm66":
        end_cpp = tbl + "[" + DQ + end_field + DQ + "].ToString()"
        start_cpp = tbl + "[" + DQ + start_field + DQ + "].ToString()"
    else:
        end_cpp = tbl + "[" + DQ + end_field + DQ + "].ToString().Trim()"
        start_cpp = tbl + "[" + DQ + start_field + DQ + "].ToString().Trim()"

    # 业务描述
    if end_field == "CHANGE_TIME":
        biz = f"从 REC_CREATE_TIME 到 CHANGE_TIME 实际经过的完整{unit_cn}数"
    elif end_field == "END_TIME":
        biz = f"从 START_TIME 到 END_TIME 实际经过的完整{unit_cn}数"
    elif end_field == "E_DATETIME":
        biz = f"从 S_DATETIME 到 E_DATETIME 实际经过的完整{unit_cn}数"
    else:
        biz = f"实际经过的完整{unit_cn}数"

    # 构建 CDbCommand 代码
    ts_start = "TO_TIMESTAMP(" + DQ + " + " + start_cpp + " + " + DQ + FMT_STR + ")"
    ts_end = "TO_TIMESTAMP(" + DQ + " + " + end_cpp + " + " + DQ + FMT_STR + ")"
    sql_body = ("select DATEDIFF(SECOND, " + ts_start + ", " + ts_end
                + ") / " + unit_div + " from DUAL")
    new_code = lead + "\t\tsqlstr = " + DQ + sql_body + DQ + ";"

    # 构建注释
    cnum = converted + 1
    comment = [
        lead + "// DM8 适配 CHANGE-EXEC-T96-" + str(cnum).zfill(2) + ":" + biz + "。",
        lead + "// 改写原因:DB2 两参数 TIMESTAMPDIFF(" + str(unit_div and {"3600": "8", "60": "4", "1": "2", "86400": "16"}.get(unit_div, "?")) + "=" + unit_cn + ") 改为 DM8 标准写法(实际完整时长)。",
        lead + "// 口径:HR-004 已确认选①实际完整时长(同 HR-002)——不满 1 个单位不算,与 DB2 原行为一致。",
        lead + "// 改写公式:DB2 TIMESTAMPDIFF → DM8 DATEDIFF(SECOND, 起点, 终点) / " + unit_div,
        lead + "//   整数除法自动舍去不满整数的部分。时间格式:HR-001 确认为 YYYYMMDDHH24MISS。",
        lead + "// 原 SQL(完整保留):",
        lead + "// " + orig_line,
        lead + "// DM8 SQL:",
    ]

    # 替换(从 idx0 到分号行)
    end = idx0
    while end < len(lines) and ";" not in lines[end]:
        end += 1
    lines[idx0:end + 1] = comment + [new_code]
    converted += 1

with open(SRC, "wb") as f:
    f.write("\n".join(lines).encode("gb18030"))

print(f"转换完成: {converted} 条")
print(f"文件行数: {len(lines)}")
active = sum(1 for l in lines if "TIMESTAMPDIFF" in l
             and not l.strip().startswith("//")
             and not l.strip().startswith("/*"))
print(f"活跃 TIMESTAMPDIFF 残留: {active}")
print(f"sha256: {hashlib.sha256(open(SRC,'rb').read()).hexdigest()[:20]}")
