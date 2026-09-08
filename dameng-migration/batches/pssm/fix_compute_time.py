# -*- coding: utf-8 -*-
"""f_pssm_compute_time.cpp L478 内联 SQL 转换(current timestamp -> CURRENT_TIMESTAMP,
sysibm.sysdummy1 -> DUAL)。"""
import hashlib
import shutil

SRC = r"D:\work\company\太钢二炼钢\Server\PSSM\libPSSM\f_pssm_compute_time.cpp"
BAK = r"D:\work\company\太钢二炼钢\analysis\dameng-migration\batches\pssm\f_pssm_compute_time.pre-dm8.bak"
OLD = "SetCommandText(\"SELECT  SUBSTR(TO_CHAR(current timestamp,'yyyymmddhh24missff6'),1,20)  from sysibm.sysdummy1; \");"
NEW = "SetCommandText(\"SELECT  SUBSTR(TO_CHAR(CURRENT_TIMESTAMP,'yyyymmddhh24missff6'),1,20)  from DUAL; \");"
CID = "CHANGE-208"

shutil.copyfile(SRC, BAK)
with open(SRC, "rb") as f:
    lines = f.read().decode("gb18030").split("\n")
idx = None
for i, l in enumerate(lines):
    if "current timestamp" in l and "SetCommandText" in l:
        idx = i
        break
assert idx is not None, "未找到目标行"
orig = lines[idx]
lead = orig[:len(orig) - len(orig.lstrip("\t "))]
core = orig.lstrip("\t ")
assert OLD in core, "原句形态与预期不符"
header = [
    lead + f"// DM8 适配 {CID}：取当前时间戳格式化为 yyyyMMddhh24missff6(微秒精度)后取前 20 位;DB2 特殊寄存器 current timestamp 改为 DM 的 CURRENT_TIMESTAMP,SYSIBM 辅助表改 DUAL。",
    lead + "// 改写原因:DM 官方函数手册支持 CURRENT_TIMESTAMP;FF1-FF9 为官方日期格式元素(FF6=微秒);TO_CHAR 仅取日期时间字段,与 DB2 current timestamp 输出等价;DM8 尚未实测。",
    lead + "// 内联语句,无 DB_KIND 分支;返回列与读取方式(GetString(1))保持不变。",
    lead + "// 原 SQL（完整保留）：",
    lead + "// " + core,
    lead + "// DM8 SQL：",
]
new_core = core.replace(OLD, NEW)
lines[idx:idx + 1] = header + [lead + new_core]
with open(SRC, "wb") as f:
    f.write("\n".join(lines).encode("gb18030"))

# 校验:还原一致
bak = open(BAK, "rb").read().decode("gb18030").split("\n")
rec = []
i, n = 0, len(lines)
while i < n:
    s = lines[i].lstrip("\t ")
    if s.startswith(f"// DM8 适配 {CID}："):
        k = i + 4
        while not lines[k].lstrip("\t ").startswith("// DM8 SQL："):
            k += 1
        for c in lines[i + 4:k]:
            ll = len(c) - len(c.lstrip("\t "))
            rec.append(c[:ll] + c[ll + 3:])
        i = k + 1 + 1  # 活动块 1 行
        continue
    rec.append(lines[i])
    i += 1
print("还原一致:", rec == bak)
print("sha256:", hashlib.sha256(open(SRC, "rb").read()).hexdigest())
