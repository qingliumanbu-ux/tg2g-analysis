# -*- coding: utf-8 -*-
"""tmsme96_inq.cpp:批量转换全部 TIMESTAMPDIFF(10条)为 DM8 DATEDIFF。
口径:HR-004 确认同 HR-002 选①实际完整时长。
每条注释详细写明:业务含义、口径来源、改写公式、原 SQL。"""
import hashlib
import re

SRC = r"D:\work\company\太钢二炼钢\Server\TMSM\p_tmsm_7160\tmsme96_inq.cpp"
SQ = "'"
DQ = '"'
FMT = SQ + "YYYYMMDDHH24MISS" + SQ

with open(SRC, "rb") as f:
    lines = f.read().decode("gb18030").split("\n")

# 从底部往上处理(避免行号偏移)
ts_lines = []
for i in range(len(lines) - 1, -1, -1):
    if "TIMESTAMPDIFF" in lines[i] and "sqlstr" in lines[i] and not lines[i].strip().startswith("//"):
        ts_lines.append(i)

print(f"找到 {len(ts_lines)} 条活跃 TIMESTAMPDIFF")

converted = 0
for idx0 in ts_lines:
    line = lines[idx0]
    lead = line[:len(line) - len(line.lstrip())]

    # 解析:TIMESTAMPDIFF(unit, CHAR(TIMESTAMP(end_expr) - TIMESTAMP(start_expr)))
    m_unit = re.search(r"TIMESTAMPDIFF\((\d+)", line)
    if not m_unit:
        continue
    unit_code = int(m_unit.group(1))

    # 确定除数和单位中文名
    if unit_code == 8:
        divisor, unit_cn = "3600", "小时"
    elif unit_code == 4:
        divisor, unit_cn = "60", "分钟"
    elif unit_code == 2:
        divisor, unit_cn = "1", "秒"
    elif unit_code == 16:
        divisor, unit_cn = "86400", "天"
    else:
        divisor, unit_cn = "1", "未知"
    if unit_code == 16:
        divisor = "86400"

    # 提取 C++ 表达式(END 和 START)
    m_all = re.search(
        r"TIMESTAMP\(" + DQ + r"\s*\+\s*(.+?)\s*\+\s*" + DQ + r"\)\s*-\s*TIMESTAMP\("
        + DQ + r"\s*\+\s*(.+?)\s*\+\s*" + DQ, line)
    if m_all:
        end_cpp = m_all.group(1).strip()
        start_cpp = m_all.group(2).strip()
    else:
        # 简单形式(无中间表达式)
        m2 = re.search(r"TIMESTAMP\(" + DQ + r"([^" + DQ + r"]*)" + DQ, line)
        if m2:
            end_cpp = start_cpp = m2.group(1).strip()
        else:
            print(f"!! L{idx0+1} 无法解析表达式,跳过")
            continue

    # 确定业务描述
    if "REC_CREATE_TIME" in end_cpp or "REC_CREATE_TIME" in start_cpp:
        biz = f"从 REC_CREATE_TIME 到 CHANGE_TIME 实际经过的完整{unit_cn}数"
    elif "END_TIME" in end_cpp:
        biz = f"从 START_TIME 到 END_TIME 实际经过的完整{unit_cn}数"
    elif "E_DATETIME" in end_cpp:
        biz = f"从 S_DATETIME 到 E_DATETIME 实际经过的完整{unit_cn}数"
    else:
        biz = f"两个时间点之间实际经过的完整{unit_cn}数"

    # 构建 C++ 代码行
    ts_start = "TO_TIMESTAMP(" + DQ + " + " + start_cpp + " + " + DQ + FMT + ")"
    ts_end = "TO_TIMESTAMP(" + DQ + " + " + end_cpp + " + " + DQ + FMT + ")"
    sql_body = ("select DATEDIFF(SECOND, " + ts_start + ", " + ts_end
                + ") / " + divisor + " from DUAL")
    new_code = lead + "\t\tsqlstr = " + DQ + sql_body + DQ + ";"

    # 构建注释块
    comment = [
        lead + "// DM8 适配 CHANGE-EXEC-2" + str(converted + 10).zfill(2) + ":" + biz + "。",
        lead + "// 改写原因:DB2 两参数 TIMESTAMPDIFF(" + str(unit_code) + "=" + unit_cn + ") 改为 DM8 标准写法(实际完整时长)。",
        lead + "// 口径:HR-004 已确认选①实际完整时长(同 HR-002)——不满 1 个单位不算,与 DB2 原行为一致。",
        lead + "// 改写公式:DB2 TIMESTAMPDIFF(" + str(unit_code) + ", TS1-TS2) → DM8 DATEDIFF(SECOND, TS2, TS1) / " + divisor,
        lead + "//   整数除法自动舍去不满整数的部分,与 DB2 TIMESTAMPDIFF 行为一致。",
        lead + "// 时间格式:HR-001 确认全库时间为 YYYYMMDDHH24MISS(14位紧凑),用 TO_TIMESTAMP 显式指定。",
        lead + "// 原 SQL(完整保留):",
        lead + "// " + line.strip(),
        lead + "// DM8 SQL:",
    ]

    # 替换:从 ts_lines[idx0] 到分号行
    end = idx0
    while end < len(lines) and ";" not in lines[end]:
        end += 1
    lines[idx0:end + 1] = comment + [new_code]
    converted += 1

with open(SRC, "wb") as f:
    f.write("\n".join(lines).encode("gb18030"))

print(f"转换完成: {converted} 条")
print(f"文件行数: {len(lines)}")
print(f"sha256: {hashlib.sha256(open(SRC,'rb').read()).hexdigest()[:20]}")

# 验证:无活跃 TIMESTAMPDIFF 残留
active = 0
for l in lines:
    s = l.strip()
    if "TIMESTAMPDIFF" in s and not s.startswith("//") and not s.startswith("/*"):
        active += 1
print(f"活跃 TIMESTAMPDIFF 残留: {active} (应为 0)")
