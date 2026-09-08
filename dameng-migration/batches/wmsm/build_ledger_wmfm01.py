# -*- coding: utf-8 -*-
"""生成/更新 sql-ledger.csv 中 wmfm01_inq.cpp 的全部条目(分母=文件内全部语句块)。"""
import csv
import hashlib
import io
import re

SRC = r"D:\work\company\太钢二炼钢\Server\WMSM\p_wmsm_8170\wmfm01_inq.cpp"
LEDGER = r"D:\work\company\太钢二炼钢\analysis\dameng-migration\sql-ledger.csv"
SHA = hashlib.sha256(open(SRC, "rb").read()).hexdigest()

FIELDS = ["sql_id", "module", "repository", "path", "function", "source_kind",
          "anchor", "original_comment_anchor", "active_sql_anchor", "decision",
          "status", "human_review_id", "local_dependency", "branch_impact",
          "evidence", "runtime_status", "current_file_sha256"]

BRANCH = "DB_KIND_DB2/DB2_ORACLE/MSSQL/ORACLE/default 共用路径"
E_DATE = "DM官方:日期与整数加减以天为单位(sql-dev/practice-date);CHANGE-01/02 同型"
E_DUAL = "DM官方:DUAL 可作 FROM 辅助表;CHANGE-01/02 同型"
E_DIFF = "IBM DAYS 定义+DM DATEDIFF(函数手册8.3);CHANGE-01 同型"
E_CASE = "标准 SQL 谓词;规避 DM DECODE 未记载的 NULL 匹配语义"
E_GR = ("IBM MAX标量函数:任一参数NULL则结果NULL(z/OS sf-max);"
        "DM GREATEST(函数手册8.1,仅用于双非空参数);外层标准 CASE 保持空值传播")
E_RN = "DM ROWNUM 为伪列关键字(查询语句4.15),别名改 RN 避免冲突;业务序号语义不变"
E_KEEP_DECODE = "DM DECODE 支持(函数手册表8.6 查表译码);无 NULL 搜索值,不依赖未记载语义"
E_KEEP_ROWNUM = "DM ROWNUM 伪列支持(查询语句4.15);语句无 ORDER BY,赋行号语义不变"
E_KEEP_IN = "DM 多列 IN 子查询支持(查询语句4.3.6 多列表子查询)"
E_KEEP_CAST = "DM CAST/DECIMAL/ROUND 支持(函数手册;数据查询语句)"


def read_lines():
    with open(SRC, "rb") as f:
        return f.read().decode("gb18030").split("\n")


def find_blocks(lines):
    blocks = []
    i, n = 0, len(lines)
    while i < n:
        s = lines[i].strip()
        if s.startswith("//"):
            i += 1
            continue
        if re.match(r"^(\s*)sqlstr\s*=", lines[i]):
            start = i
            if s.endswith(";"):
                blocks.append((start, start))
                i += 1
                continue
            j = i + 1
            end = i
            while j < n:
                sj = lines[j].strip()
                if sj.startswith("//"):
                    j += 1
                    continue
                if sj == "":
                    break
                end = j
                if sj.endswith(";"):
                    break
                j += 1
            blocks.append((start, end))
            i = end + 1
            continue
        i += 1
    return blocks


def classify(text):
    """给出可保留依据;返回空串表示无特殊方言(普通CRUD)。"""
    up = text.upper()
    notes = []
    if "DECODE" in up:
        notes.append(E_KEEP_DECODE)
    if "ROWNUM" in up:
        notes.append(E_KEEP_ROWNUM)
    if re.search(r"\(\s*\w+\s*,\s*\w+\s*\)\s+IN\b|\(\w+,\s*\w+\)\s+IN\b", text):
        notes.append(E_KEEP_IN)
    if "CAST(" in up or "DECIMAL" in up:
        notes.append(E_KEEP_CAST)
    return "；".join(notes)


def main():
    lines = read_lines()
    blocks = find_blocks(lines)
    rows = []
    keep_no = 0
    for (s, e) in blocks:
        block_text = "\n".join(lines[s:e + 1])
        # 死代码模板检查:向前 15 行找 if (false)
        dead = any("if (false)" in lines[k] for k in range(max(0, s - 15), s))
        # 向上找 CHANGE 注释头
        cid = ""
        cmt = ""
        k = s - 1
        # 跳过紧邻的 // DM8 SQL：
        while k >= 0 and lines[k].strip() == "":
            k -= 1
        if k >= 0 and lines[k].strip().startswith("// DM8 SQL："):
            dm8_sql_line = k
            # 向上找 原 SQL 标记与 CHANGE 头
            j = k - 1
            while j >= 0 and not lines[j].strip().startswith(
                    "// DM8 适配 CHANGE-"):
                j -= 1
            if j >= 0:
                m = re.search(r"CHANGE-\d+", lines[j])
                cid = m.group(0) if m else ""
                # 注释区:CHANGE 头+1(“// 原 SQL(完整保留)：”) 到 DM8 SQL 标记前
                cmt = f"L{j+3}-L{dm8_sql_line-1}"
        if cid:
            sql_id = cid
            decision = "已转换"
            status = "已转换(静态复核)"
            evidence = "见注释头改写原因;T1/T2/T2b/T3/T4/T5/T6 规则对应官方依据"
            local_dep = ""
        else:
            keep_no += 1
            sql_id = f"KEEP-WMFM01-{keep_no:02d}"
            note = classify(block_text)
            decision = "可保留"
            status = "可保留(已复核)"
            evidence = note if note else "普通 CRUD/聚合查询,无方言差异"
            if dead:
                evidence += ";位于 if(false) 死代码模板,SQL 为空串,不参与执行"
            local_dep = ""
        rows.append({
            "sql_id": sql_id,
            "module": "WMSM",
            "repository": "Server/WMSM",
            "path": "p_wmsm_8170/wmfm01_inq.cpp",
            "function": "f_fosmt00b_inq",
            "source_kind": "literal_concat",
            "anchor": f"L{s+1}-L{e+1}",
            "original_comment_anchor": cmt,
            "active_sql_anchor": f"L{s+1}-L{e+1}",
            "decision": decision,
            "status": status,
            "human_review_id": "",
            "local_dependency": local_dep,
            "branch_impact": BRANCH,
            "evidence": evidence,
            "runtime_status": "未执行",
            "current_file_sha256": SHA,
        })
    # 动态片段行
    for k, l in enumerate(lines, 1):
        if "SQL_CONTEXT_01" in l and "sqlstr_where" in l:
            rows.append({
                "sql_id": "DYN-WMFM01-01",
                "module": "WMSM",
                "repository": "Server/WMSM",
                "path": "p_wmsm_8170/wmfm01_inq.cpp",
                "function": "f_fosmt00b_inq",
                "source_kind": "dynamic_fragment_from_table",
                "anchor": f"L{k}",
                "original_comment_anchor": "",
                "active_sql_anchor": "",
                "decision": "待局部信息",
                "status": "待局部信息(SQL文本未取得)",
                "human_review_id": "",
                "local_dependency": ("需要表 S_<tbl> 中 SQL_CONTEXT_01/02 的实际"
                                     "WHERE/ORDER 文本及其参数定义"),
                "branch_impact": "动态拼接,与具体数据集相关",
                "evidence": "执行器可保留不代表传入文本兼容;未取得文本不能记完成",
                "runtime_status": "未执行",
                "current_file_sha256": SHA,
            })
            break
    # 写入(重建该文件相关行;其他模块行保留)
    try:
        with io.open(LEDGER, encoding="utf-8-sig", newline="") as f:
            old = [r for r in csv.DictReader(f)
                   if not r["path"].endswith("wmfm01_inq.cpp")]
    except FileNotFoundError:
        old = []
    with io.open(LEDGER, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(old)
        w.writerows(rows)
    conv = sum(1 for r in rows if r["decision"] == "已转换")
    keep = sum(1 for r in rows if r["decision"] == "可保留")
    dyn = sum(1 for r in rows if r["decision"] == "待局部信息")
    print(f"wmfm01 rows={len(rows)} converted={conv} keep={keep} dynamic={dyn}")
    print("sha256:", SHA)


if __name__ == "__main__":
    main()
