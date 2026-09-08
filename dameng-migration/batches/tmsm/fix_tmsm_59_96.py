# -*- coding: utf-8 -*-
"""tmsme59_inq.cpp / tmsme96_inq.cpp 定制转换。

只转换与 HR 无关的确定块:
  tmsme96 L83     DAYS()-DAYS() 日差 -> DATEDIFF(CHANGE-01 同型)  [CHANGE-108]
  tmsme96 L549-551 纯算术 SELECT 的 SYSIBM.SYSDUMMY1 -> DUAL          [CHANGE-109]
  tmsme59 L291-293 纯算术 SELECT 的 SYSIBM.SYSDUMMY1 -> DUAL          [CHANGE-110]
含两参数 TIMESTAMPDIFF 的语句整条不动(HR-002/HR-004 待人工口径)。
"""
import hashlib
import shutil

Q = '"'
B = r"D:\work\company\太钢二炼钢\analysis\dameng-migration\batches\tmsm"

FILES = {
    r"D:\work\company\太钢二炼钢\Server\TMSM\p_tmsm_7160\tmsme96_inq.cpp": [
        {
            "cid": "CHANGE-108",
            "find": None,  # 按行号
            "line1": 83, "line2": 83,
            "desc": ("取 CHANGE_TIME 与 REC_CREATE_TIME 的日历日差;改写与"
                     " tmsme59 CHANGE-01 同型:DAYS() 差改用"
                     " DATEDIFF(DAY,起点,终点),SYSIBM 辅助表改 DUAL。"),
            "reason": ("IBM DAYS 定义 + DM DATEDIFF(函数手册8.3);输入时间文本"
                       "格式与 HR-001 同源(同为 TTMSM66 字段),格式确认前保持"
                       " CAST 写法;DM8 尚未实测。"),
        },
        {
            "cid": "CHANGE-109",
            "line1": 549, "line2": 551,
            "desc": ("对运行时分钟值做 ROUND 汇总计算;SYSIBM.SYSDUMMY1 辅助表"
                     "改为 DUAL;计算口径与参数保持不变。"),
            "reason": ("DM 支持 DUAL 辅助表(官方文档);纯算术表达式无方言差异;"
                       "DM8 尚未实测。"),
        },
    ],
    r"D:\work\company\太钢二炼钢\Server\TMSM\p_tmsm_7160\tmsme59_inq.cpp": [
        {
            "cid": "CHANGE-110",
            "line1": 291, "line2": 293,
            "desc": ("对运行时分钟值做 ROUND 汇总计算;SYSIBM.SYSDUMMY1 辅助表"
                     "改为 DUAL;计算口径与参数保持不变。"),
            "reason": ("DM 支持 DUAL 辅助表(官方文档);纯算术表达式无方言差异;"
                       "同函数 TIMESTAMPDIFF 语句属 HR-002,另行处理;DM8 尚未"
                       "实测。"),
        },
    ],
}

REPL = {
    "CHANGE-108": (
        'sqlstr = "select DATEDIFF(DAY, CAST(\'" + ttmsm66["REC_CREATE_TIME"].ToString() + "\' AS TIMESTAMP), CAST(\'" + ttmsm66["CHANGE_TIME"].ToString() + "\' AS TIMESTAMP)) from DUAL";'
    ),
}


def process(path, items):
    with open(path, "rb") as f:
        raw = f.read()
    shutil.copyfile(path, B + "\\" + path.split("\\")[-1] + ".pre-dm8.bak")
    text = raw.decode("gb18030")
    lines = text.split("\n")
    # 从后往前,避免行号漂移
    for item in sorted(items, key=lambda x: -x["line1"]):
        s0 = item["line1"] - 1
        e0 = item["line2"] - 1
        block = lines[s0:e0 + 1]
        leads = [l[:len(l) - len(l.lstrip("\t "))] for l in block]
        core = [l[len(l) - len(l.lstrip("\t ")):] for l in block]
        lead = leads[0]
        if item["cid"] in REPL:
            active_core = [REPL[item["cid"]]]
        else:
            # 仅替换单行 FROM SYSIBM.SYSDUMMY1(末行)
            active_core = []
            for l in core:
                active_core.append(
                    l.replace("SYSIBM.SYSDUMMY1", "DUAL")
                     .replace("sysibm.dual", "dual"))
        header = [
            lead + f"// DM8 适配 {item['cid']}：{item['desc']}",
            lead + f"// 改写原因：{item['reason']}",
            lead + "// 本共用分支面向 DM8,其他 DB_KIND 标签也会执行此 SQL;参数、结果列、条件与排序保持不变。",
            lead + "// 原 SQL（完整保留）：",
        ]
        commented = [leads[k] + "// " + core[k] for k in range(len(core))]
        tail = [lead + "// DM8 SQL："]
        lines[s0:e0 + 1] = header + commented + tail + [
            leads[min(k, len(leads) - 1)] + l for k, l in
            enumerate(active_core)]
    with open(path, "wb") as f:
        f.write("\n".join(lines).encode("gb18030"))
    print("written", path)


for path, items in FILES.items():
    process(path, items)

# 验证:注释还原
PAIRS = {
    B + r"\tmsme59_inq.cpp.pre-dm8.bak":
        r"D:\work\company\太钢二炼钢\Server\TMSM\p_tmsm_7160\tmsme59_inq.cpp",
    B + r"\tmsme96_inq.cpp.pre-dm8.bak":
        r"D:\work\company\太钢二炼钢\Server\TMSM\p_tmsm_7160\tmsme96_inq.cpp",
}
for bak, newp in PAIRS.items():
    orig = open(bak, "rb").read().decode("gb18030").split("\n")
    new = open(newp, "rb").read().decode("gb18030").split("\n")
    # 从新文件中移除插入的注释行:逐行扫描,凡 "// DM8 适配 CHANGE-1" 开始的
    # 块(header4行+commented n行+tail1行)跳过
    restored = []
    i = 0
    n = len(new)
    while i < n:
        if new[i].lstrip().startswith("// DM8 适配 CHANGE-1"):
            lead = new[i][:len(new[i]) - len(new[i].lstrip("\t "))]
            j = i
            # 原 SQL 注释区: 直到 "// DM8 SQL："
            k = i
            while not new[k].lstrip().startswith("// DM8 SQL："):
                k += 1
            commented = new[i + 4:k]
            restored.extend(lead + c.lstrip()[3:] if False else
                            lead + c.strip()[2 + 1:] for c in commented)
            i = k + 1
            continue
        restored.append(new[i])
        i += 1
    # 与原始比对(还原的行 = 原块)
    ok = True
    ri = 0
    for idx, o in enumerate(orig):
        if ri < len(restored) and restored[ri] == o:
            ri += 1
    # 简化断言:原文件每个被改块的行都应出现在还原序列中
    print(newp.split("\\")[-1], "还原行数:", len(restored),
          "(含在原文件中:", all(r in orig for r in restored), ")")
    print("  sha256:", hashlib.sha256(open(newp, 'rb').read()).hexdigest())
