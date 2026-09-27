#!/usr/bin/env python3
"""太钢二炼钢 达梦 SQL 转换离线校验器

用途：在已连接 VPN(可访问达梦库、但无外网)的环境里，自动批量验证 DM8 SQL 转换结果，
     不需要联网、不需要在线 AI、不需要安装达梦客户端。

依赖（已在本机隔离环境安装）：jpype1、jaydebeapi。
JVM 直接复用 DBeaver 自带运行时，JDBC 驱动复用 DBeaver 已下载的 DmJdbcDriver18 jar，
因此断网后所有依赖都在本地。

运行前请确认 VPN 已连接（能 ping 通 dm8conn.json 里的主机）。

用法：
  python dm8check.py selftest              # 只检查工具链(JVM/驱动/配置)，不连库
  python dm8check.py list                  # 离线列出待验证语句清单，不连库
  python dm8check.py e2                    # 批量执行 e2-verify-*.sql，输出 CSV
  python dm8check.py e2 --files a.sql b.sql
  python dm8check.py probe                 # 执行 probes/probe-*.sql
  python dm8check.py diff                  # 执行对拍查询并比较 old_v / new_v

安全约定：
  * 密码只从环境变量 DM8_PASSWORD 或交互输入读取，绝不写入任何文件。
  * 默认 autocommit 关闭；遇到 INSERT/UPDATE/DELETE/MERGE 会拒绝执行，除非显式加 --allow-dml。
"""

import argparse
import csv
import getpass
import glob
import os
import re
import sys
import time
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(HERE, "dm8conn.json")
E2_GLOB = os.path.join(HERE, "..", "e2-verify-*.sql")
PROBE_DIR = os.path.join(HERE, "probes")
OUT_DIR = os.path.join(HERE, "out")

DML_RE = re.compile(r"^\s*(insert|update|delete|merge|truncate|drop|alter)\b", re.I)

CATEGORY_RULES = [
    ("语法或函数不支持", [
        r"语法分析出错", r"syntax error", r"分析出错", r"无效的函数", r"函数.*不存在",
        r"不支持的", r"无效的参数", r"无法识别", r"无法解析", r"意外的",
    ]),
    ("对象不存在", [
        r"无效的表或视图名", r"表或视图不存在", r"无效的列名", r"对象.*不存在",
        r"invalid table", r"invalid column", r"does not exist",
    ]),
    ("权限不足", [r"权限", r"permission", r"privilege"]),
    ("数据类型或长度", [r"数据类型", r"数据长度", r"截断", r"溢出", r"numeric", r"overflow"]),
]


# ---------------------------------------------------------------- SQL 切分

def normalize(text):
    """去掉 C++ 注释残留、参数占位替换产生的非法限定名。仅用于校验，不改动源仓库文件。"""
    out = []
    replaced = 0
    for line in text.splitlines():
        if line.strip().startswith("//"):
            continue
        replaced += line.count("'测试值'.")
        out.append(line.replace("'测试值'.", ""))
    return "\n".join(out), replaced


LABEL_RE = re.compile(r"^--\s*\[(CHANGE-[0-9A-Za-z_\-]+)\]\s*(.*)$")
# 变量被剥离后留下的残缺表达式，例如 ROUND(/60,2)、ROUND(( - - )/ 60, 2)
DEFECT_RE = re.compile(r"[(),]\s*/\s*\d|[(),]\s*[-+*/]\s*[),*/]|\(\s*\(\s*/")


def split_statements(text, path):
    """按引号感知切分 SQL 语句，并把上一行的 -- [CHANGE-xxx] 作为标签。

    两条健壮性规则（E2 脚本是自动生成的，本身可能残缺）：
    1. 遇到新的 -- [CHANGE-xxx] 标签行时，无论上一条是否以分号结束都强制收尾，
       避免一条残缺语句把后面所有语句吞成一条；
    2. 单行内单引号数量为奇数时判定该行残缺，行尾重置引号状态并记录缺陷位置。
    """
    stmts = []
    defects = []
    buf = []
    label = None
    start_line = 0
    in_q = False

    def flush(terminated):
        stmt = "".join(buf).strip()
        if stmt:
            stmts.append({
                "label": label or "%s:L%d" % (path, start_line),
                "sql": stmt, "line": start_line,
                "terminated": terminated,
                "defect": bool(DEFECT_RE.search(stmt)),
            })
        del buf[:]

    for line_no, raw in enumerate(text.splitlines(), 1):
        s = raw.strip()
        if not in_q:
            m = LABEL_RE.match(s)
            if m:
                flush(False)
                label = m.group(1) + " " + m.group(2).strip()
                continue
            if not buf and s.startswith("--"):
                continue
        if not buf:
            start_line = line_no

        i = 0
        while i < len(raw):
            c = raw[i]
            if not in_q and c == "-" and i + 1 < len(raw) and raw[i + 1] == "-":
                break
            if c == "'":
                if in_q and i + 1 < len(raw) and raw[i + 1] == "'":
                    buf.append("''")
                    i += 2
                    continue
                in_q = not in_q
            if c == ";" and not in_q:
                stmt = "".join(buf).strip()
                if stmt:
                    stmts.append({
                        "label": label or "%s:L%d" % (path, start_line),
                        "sql": stmt, "line": start_line,
                        "terminated": True,
                        "defect": bool(DEFECT_RE.search(stmt)),
                    })
                del buf[:]
                label = None
                start_line = line_no
                i += 1
                continue
            buf.append(c)
            i += 1

        if in_q and raw.count("'") % 2 == 1:
            in_q = False
            defects.append("%s:L%d" % (os.path.basename(path), line_no))
        if buf:
            buf.append("\n")

    flush(False)
    return stmts, defects


def classify(message):
    for name, pats in CATEGORY_RULES:
        for p in pats:
            if re.search(p, message, re.I):
                return name
    return "其他错误"


# ---------------------------------------------------------------- 工具链

def load_config():
    import json
    with open(CONFIG, "r", encoding="utf-8") as f:
        return json.load(f)


def start_jvm(cfg):
    java_home = cfg["java_home"]
    if not os.path.isdir(java_home):
        sys.exit("JAVA_HOME 无效：%s" % java_home)
    os.environ["JAVA_HOME"] = java_home
    os.environ["PATH"] = os.path.join(java_home, "bin") + os.pathsep + os.environ["PATH"]

    jars = glob.glob(cfg["driver_jar_glob"])
    if not jars:
        sys.exit("未找到达梦 JDBC 驱动，请检查 driver_jar_glob：%s" % cfg["driver_jar_glob"])
    import jpype
    jpype.startJVM(classpath=jars, convertStrings=True)
    return jars[0]


def connect(cfg, args):
    import jaydebeapi
    user = args.user or cfg.get("user") or os.environ.get("DM8_USER")
    if not user:
        user = input("达梦用户名: ").strip()
    password = os.environ.get("DM8_PASSWORD")
    if password is None:
        password = getpass.getpass("达梦密码(不落盘): ")
    url = args.url or cfg["url"]
    conn = jaydebeapi.connect(cfg["driver_class"], url, [user, password])
    jc = conn.jconn
    try:
        jc.setAutoCommit(False)
        jc.setLoginTimeout(int(cfg.get("login_timeout_seconds", 15)))
    except Exception:
        pass
    conn._dm8_user = user
    return conn, user, url


# ---------------------------------------------------------------- 执行

def run_statement(conn, sql, timeout):
    import jaydebeapi
    stmt = None
    try:
        stmt = conn.jconn.createStatement()
        try:
            stmt.setQueryTimeout(int(timeout))
        except Exception:
            pass
        has_result = stmt.execute(sql)
        if has_result:
            rs = stmt.getResultSet()
            cols = []
            meta = rs.getMetaData()
            for i in range(1, meta.getColumnCount() + 1):
                cols.append(meta.getColumnLabel(i))
            rows = []
            while rs.next() and len(rows) < 500:
                rows.append([rs.getString(i + 1) for i in range(meta.getColumnCount())])
            rs.close()
            return "成功", len(rows), "|".join(cols), rows
        return "成功", stmt.getUpdateCount(), "", []
    finally:
        if stmt is not None:
            try:
                stmt.close()
            except Exception:
                pass
        try:
            conn.jconn.rollback()
        except Exception:
            pass


def run_batch(stmts, conn, cfg, out_csv, allow_dml):
    timeout = cfg.get("query_timeout_seconds", 120)
    rows = []
    counts = {}
    total = len(stmts)
    for idx, st in enumerate(stmts, 1):
        sql = st["sql"]
        if DML_RE.match(sql) and not allow_dml:
            status, rows_n, cols, code, msg = "跳过(写操作)", "", "", "SECURITY", "未加 --allow-dml"
        else:
            t0 = time.time()
            try:
                status, rows_n, cols, _ = run_statement(conn, sql, timeout)
                code, msg = "", ""
            except Exception as e:
                raw = str(e)
                code = ""
                m = re.search(r"ERROR CODE[:：]\s*(-?\d+)", raw)
                if m:
                    code = m.group(1)
                status = "失败"
                rows_n = ""
                cols = ""
                msg = " ".join(raw.split())[:400]
            cost = "%.2f" % (time.time() - t0)
        category = classify(msg) if status == "失败" else ""
        counts[status if status != "失败" else category] = counts.get(status if status != "失败" else category, 0) + 1
        label = st["label"]
        print("[%d/%d] %-14s %s" % (idx, total, status if status != "失败" else category, label))
        if status == "失败":
            print("        %s" % msg[:220])
        rows.append({
            "序号": idx, "语句标签": label, "来源行": st["line"],
            "结果": status, "错误分类": category, "错误码": code,
            "返回列数": len(cols.split("|")) if cols else 0,
            "返回行数": rows_n, "耗时秒": cost if status != "跳过(写操作)" else "",
            "语句完整": "完整" if st.get("terminated", True) else "未以分号结束",
            "疑似残缺": "是" if st.get("defect") else "",
            "语句摘要": " ".join(sql.split())[:200],
            "错误信息": msg,
        })
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    with open(out_csv, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print("\n=== 汇总 ===")
    for k, v in sorted(counts.items(), key=lambda x: -x[1]):
        print("  %-16s %d" % (k, v))
    print("明细已写入: %s" % out_csv)
    return rows


# ---------------------------------------------------------------- 对拍

def run_diff(conn, files, cfg, out_csv):
    """执行对拍查询：每条语句须返回 case_key / old_v / new_v 三列，逐行比较。"""
    timeout = cfg.get("query_timeout_seconds", 120)
    rows = []
    for path in files:
        with open(path, "r", encoding="utf-8-sig") as f:
            raw, _ = normalize(f.read())
        stmts, _defects = split_statements(raw, os.path.basename(path))
        for st in stmts:
            try:
                status, _n, cols, data = run_statement(conn, st["sql"], timeout)
            except Exception as e:
                rows.append({"来源": st["label"], "用例": "", "old_v": "", "new_v": "",
                             "结论": "查询失败", "说明": " ".join(str(e).split())[:200]})
                continue
            lower = [c.lower() for c in cols.split("|")] if cols else []
            need = ["case_key", "old_v", "new_v"]
            if not all(n in lower for n in need):
                rows.append({"来源": st["label"], "用例": "", "old_v": "", "new_v": "",
                             "结论": "列不合规", "说明": "需返回 case_key/old_v/new_v，实际: %s" % cols})
                continue
            i_k, i_o, i_n = (lower.index(n) for n in need)
            for r in data:
                same = r[i_o] == r[i_n]
                rows.append({"来源": st["label"], "用例": r[i_k], "old_v": r[i_o], "new_v": r[i_n],
                             "结论": "一致" if same else "不一致", "说明": ""})
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    with open(out_csv, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    bad = [r for r in rows if r["结论"] != "一致"]
    print("\n=== 对拍结果 ===")
    print("  用例总数 %d，一致 %d，需关注 %d" % (len(rows), len(rows) - len(bad), len(bad)))
    for r in bad[:40]:
        print("  [%s] %s | old=%r new=%r %s" % (r["结论"], r["用例"], r["old_v"], r["new_v"], r["说明"]))
    print("明细已写入: %s" % out_csv)
    return rows


# ---------------------------------------------------------------- 模式

def collect_e2(files):
    paths = files or sorted(glob.glob(E2_GLOB))
    stmts = []
    for p in paths:
        with open(p, "r", encoding="utf-8-sig") as f:
            raw, replaced = normalize(f.read())
        got, defects = split_statements(raw, os.path.basename(p))
        note = ""
        if replaced:
            note += "  归一化 %d 处" % replaced
        if defects:
            note += "  引号残缺 " + ",".join(defects)
        print("%-30s %3d 条%s" % (os.path.basename(p), len(got), note))
        stmts.extend(got)
    return stmts


def stamp():
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="达梦 SQL 转换离线校验器")
    ap.add_argument("mode", choices=["selftest", "list", "e2", "probe", "diff"])
    ap.add_argument("--files", nargs="*", default=None, help="指定 SQL 文件，默认按模式取内置路径")
    ap.add_argument("--user", default=None)
    ap.add_argument("--url", default=None)
    ap.add_argument("--allow-dml", action="store_true", help="允许执行写操作(仍会回滚)")
    ap.add_argument("--out", default=None, help="结果 CSV 路径")
    args = ap.parse_args()

    cfg = load_config()

    if args.mode in ("list", "e2"):
        stmts = collect_e2(args.files)
        print("合计待验证语句: %d" % len(stmts))
        if args.mode == "list":
            out = args.out or os.path.join(OUT_DIR, "e2-清单-%s.csv" % stamp())
            os.makedirs(OUT_DIR, exist_ok=True)
            with open(out, "w", encoding="utf-8-sig", newline="") as f:
                w = csv.DictWriter(f, fieldnames=["序号", "语句标签", "来源行", "语句摘要"])
                w.writeheader()
                for i, st in enumerate(stmts, 1):
                    w.writerow({"序号": i, "语句标签": st["label"], "来源行": st["line"],
                                "语句摘要": " ".join(st["sql"].split())[:200]})
            print("清单已写入: %s" % out)
            return

    if args.mode == "probe":
        paths = args.files or sorted(glob.glob(os.path.join(PROBE_DIR, "probe-*.sql")))
        stmts = []
        for p in paths:
            with open(p, "r", encoding="utf-8-sig") as f:
                raw, _ = normalize(f.read())
            got, defects = split_statements(raw, os.path.basename(p))
            print("%-38s %3d 条%s" % (os.path.basename(p), len(got),
                                      "  引号残缺 " + ",".join(defects) if defects else ""))
            stmts.extend(got)
        print("合计探针语句: %d" % len(stmts))

    if args.mode == "selftest":
        jar = start_jvm(cfg)
        print("JVM      : %s" % __import__("jpype").getDefaultJVMPath())
        print("驱动 jar : %s" % jar)
        print("连接串   : %s" % cfg["url"])
        import socket
        host, port = re.sub(r"^jdbc:dm://", "", cfg["url"]).split(":")
        port = int(port.split("/")[0])
        s = socket.socket()
        s.settimeout(8)
        try:
            s.connect((host, port))
            print("网络连通 : 是 (%s:%d)" % (host, port))
        except Exception as e:
            print("网络连通 : 否 (%s:%d) —— 请确认 VPN 已连接 [%s]" % (host, port, e))
        finally:
            s.close()
        print("工具链就绪。")
        return

    # 需要连库的模式
    start_jvm(cfg)
    conn, user, url = connect(cfg, args)
    print("已连接: %s  用户: %s  自动提交: 关闭" % (url, user))
    try:
        if args.mode == "probe":
            out = args.out or os.path.join(OUT_DIR, "probe-%s.csv" % stamp())
            run_batch(stmts, conn, cfg, out, args.allow_dml)
        elif args.mode == "diff":
            paths = args.files or sorted(glob.glob(os.path.join(PROBE_DIR, "*.diff.sql")))
            out = args.out or os.path.join(OUT_DIR, "diff-%s.csv" % stamp())
            run_diff(conn, paths, cfg, out)
        else:
            out = args.out or os.path.join(OUT_DIR, "e2-%s.csv" % stamp())
            run_batch(stmts, conn, cfg, out, args.allow_dml)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
