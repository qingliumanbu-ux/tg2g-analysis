"""Inventory all local working-tree files; never export source or config values."""
from pathlib import Path
from collections import Counter, defaultdict
from bisect import bisect_right
import csv
import hashlib
import json
import os
import re

from scan_database_surface import RULES

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "analysis" / "database-workspace"
PATTERNS = dict(RULES)
PATTERNS.update({
    "direct_client_query": r"\b(?:querySql|ExecQuery|ExecuteQuerySql|ExecuteSqlQuery)\s*\(",
    "row_number_paging": r"\b(?:ROWNUM|ROW_NUMBER|ROWNUMBER)\b|\b(?:OFFSET|LIMIT)\s+(?:\d+|@|:|\?)",
    "catalog_metadata": r"\b(?:USER|ALL|DBA)_(?:TAB\w*|COL\w*|CONS\w*|IND\w*|SEQ\w*|TRIG\w*|VIEW\w*)\b|\b(?:SYSIBM|SYSCAT|SYSSTAT|INFORMATION_SCHEMA)\s*\.|\bSYS\.(?:TABLES|COLUMNS|INDEXES)\b",
    "stored_program_call": r"\bCALL\s+[A-Za-z_]\w*\s*\(|\b(?:StoredProcedure|ExecuteProcedure)\b",
    "dml_ddl": r"\b(?:INSERT\s+INTO|DELETE\s+FROM|MERGE\s+INTO|UPDATE\s+\w+\s+SET|CREATE\s+(?:OR\s+REPLACE\s+)?(?:TABLE|VIEW|INDEX|SEQUENCE|TRIGGER|PROCEDURE|FUNCTION|PACKAGE)|ALTER\s+(?:TABLE|SEQUENCE)|DROP\s+(?:TABLE|VIEW|INDEX|SEQUENCE)|TRUNCATE\s+TABLE|GRANT\s+\w+|REVOKE\s+\w+)\b",
    "dynamic_sql_payload": r"\b(?:QUERY_SQL|QUERYSQL|SQL_TEXT|SQLTEXT|QUERY_TEXT|SQL_QUERY|SELECT_SQL|SQL_SELECT|SQL_WHERE|WHERE_SQL|SQL_CONDITION|SQL_STR|SQL_STMT|CMD_TEXT)\b",
    "query_execution": r"\b(?:SetCommandText|ExecuteQuery|ExecuteReader|ExecuteScalar|ExecuteNonQuery|ExecuteSql|QueryUtility|QueryTable|QueryDataSet|ExecuteSqlCommand|SQLExecDirect|SQLExecute|dpi_exec|dpi_exec_direct|SQLPrepare)\b",
    "sql_building_extended": r"\b\w*(?:sql|Sql|SQL)\w*\s*(?:\+=|=(?!=)|\.\s*(?:Append|Format|Replace|append|format|replace)\s*\()",
    "database_provider_reference": r"\b(?:DatabaseKind|DbProvider|ProviderName|DB_TYPE|DATABASE_TYPE|DB_KIND_\w+|ODBC|OleDb|OracleConnection|SqlConnection|DB2Connection|OdbcConnection|EntityFramework|Dapper|DPI|DbClient|DB2CLI|SQL_ATTR_AUTOCOMMIT)\b",
    "schema_metadata_api": r"\b(?:GetSchema|GetTableSchema|GetTableInfo|GetColumnInfo|GetColumns|SQLColumns|SQLTables|SQLPrimaryKeys|GetTableItem|GetTableComment|GetPrimaryKey)\b",
    "config_query_framework": r"\b(?:CFormDevConfig|QueryUtility|DataSetConfig|DATASET_SQL|QUERY_CONFIG|QUERY_SQL|FORM_CONFIG|DATA_SOURCE|DATASOURCE|dataSourceSql)\b",
    "model_crud": r"(?:\.|->)\s*(?:Insert|Update|Delete|Query|QueryEx|Merge|Save|InsertBatch|UpdateBatch|GetAllPrimaryKeys)\s*\(",
    "string_functions": r"\b(?:SUBSTR|SUBSTRING|SUBSTRB|LENGTH|LENGTHB|LEN|LOCATE|INSTR|POSSTR|CONCAT|LISTAGG|GROUP_CONCAT|WM_CONCAT|STRING_AGG|LPAD|RPAD|RTRIM|LTRIM|TRIM|REGEXP_REPLACE|REGEXP_LIKE)\s*\(",
    "numeric_conversion": r"\b(?:DECIMAL|DEC|NUMBER|NUMERIC|TO_NUMBER|DOUBLE|FLOAT|CAST|CONVERT|DIGITS|ROUND|TRUNC|CEIL|FLOOR|MOD)\s*\(",
    "date_time_extra": r"\b(?:SYSDATE|SYSTIMESTAMP|CURRENT_DATE|CURRENT_TIME|CURRENT_TIMESTAMP|GETDATE|DATEADD|DATEDIFF|DAYOFWEEK|LAST_DAY|NEXT_DAY|EXTRACT|YEAR|MONTH|DAY|HOUR|MINUTE|SECOND)\b",
    "group_hierarchy_window": r"\b(?:CONNECT\s+BY|START\s+WITH|WITH\s+RECURSIVE|PIVOT|UNPIVOT|GROUPING\s+SETS|ROLLUP\s*\(|CUBE\s*\(|OVER\s*\(|MINUS|EXCEPT|INTERSECT)\b",
    "ordering_limit": r"\b(?:ORDER\s+BY|NULLS\s+FIRST|NULLS\s+LAST|TOP\s+\d+|FETCH\s+(?:FIRST|NEXT))\b",
    "null_blank_semantics": r"\bIS\s+(?:NOT\s+)?NULL\b|\bTrimOrBlank\s*\(|(?:=|<>|!=)\s*'(?:| +)'",
    "concat_operator": r"\|\|",
    "db_transaction_and_errors": r"\b(?:CDbException|SQLCODE|SQLSTATE|SQL\s*CODE|BeginTrans\w*|Commit\w*|Rollback\w*|AutoCommit|Savepoint|IsolationLevel|TransactionScope|EITuxedo)\b",
    "db_object_program": r"\b(?:DBMS_\w+|UTL_\w+|DBLINK|DB_LINK|OPENQUERY|EXECUTE\s+IMMEDIATE|PREPARE\s+\w+\s+FROM)\b",
    "query_service_names": r"\b(?:gc00_ExcQrySql|gc00_GetTsCol|gc00_GetTs|gcpm_dataSet_inq|gcpm_initForm|[a-z0-9_]*config[a-z0-9_]*|[a-z0-9_]*dataset[a-z0-9_]*)\b",
})


def classify(rel):
    parts = rel.parts
    if "@mf-types" in parts or "node_modules" in parts:
        return "dependency_or_type_declaration"
    if rel.name in {"package-lock.json", "yarn.lock", "pnpm-lock.yaml"}:
        return "dependency_lock"
    if rel.name.startswith(".env"):
        return "environment_config_values_not_exported"
    if rel.suffix.lower() in {".vcxproj", ".csproj", ".sln", ".props", ".targets"}:
        return "build_project"
    if rel.suffix.lower() in {".xml", ".resx", ".config", ".ini", ".json", ".yaml", ".yml"}:
        return "config_or_resource"
    if rel.suffix.lower() in {".md", ".txt", ".log"}:
        return "document_or_log"
    if "dist" in parts or "build" in parts or ".timestamp-" in rel.name:
        return "generated_or_build_support"
    if parts[0] == "Server" or (parts[0] == "Client" and "server" in parts):
        return "backend_source"
    if rel.suffix.lower() == ".cs":
        return "desktop_source"
    if rel.suffix.lower() in {".ts", ".js", ".vue", ".tsx", ".jsx", ".mjs", ".html"}:
        return "web_source"
    return "other_text"


def decode(raw):
    if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
        return raw.decode("utf-16"), "utf-16"
    if b"\0" in raw:
        return None, "binary"
    for encoding in ("utf-8-sig", "gb18030"):
        try:
            value = raw.decode(encoding)
            controls = sum(ord(c) < 32 and c not in "\r\n\t\f" for c in value)
            if controls > max(2, len(value) // 100):
                return None, "binary"
            return value, encoding
        except UnicodeDecodeError:
            pass
    return None, "undecodable_or_binary"


def main():
    OUT.mkdir(exist_ok=True)
    patterns = {key: re.compile(value, re.I) for key, value in PATTERNS.items()}
    records, skipped_dirs = [], []
    for folder, dirs, names in os.walk(ROOT, followlinks=False):
        retained = []
        for name in sorted(dirs):
            path = Path(folder) / name
            if name == ".git" or path == ROOT / "analysis" or path.is_symlink():
                skipped_dirs.append({"path": path.relative_to(ROOT).as_posix(), "reason": "git_metadata" if name == ".git" else "analysis_outputs" if path == ROOT / "analysis" else "symlink"})
            else:
                retained.append(name)
        dirs[:] = retained
        for name in sorted(names):
            path = Path(folder) / name
            rel = path.relative_to(ROOT)
            record = {"path": rel.as_posix(), "category": classify(rel)}
            if path.is_symlink():
                record["status"] = "symlink_not_followed"
                records.append(record)
                continue
            try:
                raw = path.read_bytes()
                text, encoding = decode(raw)
                record.update(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest(), encoding=encoding)
                if text is None:
                    record["status"] = encoding
                else:
                    record["status"] = "scanned"
                    record["line_count"] = text.count("\n") + 1
                    line_starts = [m.start() for m in re.finditer("\n", text)]
                    features = {}
                    for key, pattern in patterns.items():
                        lines = sorted({bisect_right(line_starts, m.start()) + 1 for m in pattern.finditer(text)})
                        if lines:
                            features[key] = lines
                    record["features"] = features
            except (OSError, UnicodeError) as exc:
                record.update(status="read_error", error_type=type(exc).__name__)
            records.append(record)
    counts = Counter(r["status"] for r in records)
    categories = defaultdict(Counter)
    feature_files = Counter()
    for r in records:
        categories[r["category"]]["files"] += 1
        categories[r["category"]][r["status"]] += 1
        if r.get("features"):
            categories[r["category"]]["candidate_files"] += 1
            feature_files.update(r["features"].keys())
    result = {
        "scope": "All current workspace files, including hidden configuration, dependency declarations, frontend and desktop code, resources and build scripts. Excludes Git internals, this task's analysis outputs, and linked directories/files.",
        "confirmed_by_user": "BM2 CDbConnection/CDbCommand/CModel already support Dameng, including binding, paging, type conversion and transactions. Not independently runtime-tested here.",
        "method": "Broad regex candidate inventory over full text including comments and disabled branches. Not a C++/SQL parser, SQL extractor or compatibility verdict. All locations are exported without code snippets or configuration values. Binary/resource payloads and runtime/external sources need separate coverage.",
        "rules": PATTERNS,
        "summary": {"enumerated_files": len(records), "statuses": dict(counts), "categories": dict(categories), "candidate_files": sum(bool(r.get('features')) for r in records), "files_by_feature": dict(feature_files)},
        "excluded_directories": skipped_dirs,
        "files": records,
    }
    (OUT / "inventory.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (OUT / "locations.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["path", "category", "feature", "line"])
        for r in records:
            for feature, lines in r.get("features", {}).items():
                for line in lines:
                    writer.writerow([r["path"], r["category"], feature, line])
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
