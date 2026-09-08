"""Read-only C++ database-surface inventory; outputs locations, never source text."""
from pathlib import Path
from collections import Counter
import json
import re

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent / "database-surface.json"
RULES = {
    "database_api": r"\b(?:CDbConnection|CDbCommand|CModel|CPageInfo)\b",
    "sql_keywords": r"\b(?:SELECT|INSERT\s+INTO|UPDATE\s+\w+\s+SET|DELETE\s+FROM|MERGE\s+INTO|TRUNCATE\s+TABLE)\b",
    "db_kind_branch": r"\bDB_KIND_\w+\b",
    "db2_isolation": r"\bWITH\s+(?:UR|RS|CS|RR)\b",
    "db2_fetch_first": r"\bFETCH\s+FIRST\b",
    "db2_dummy_catalog": r"\b(?:SYSIBM|SYSCAT|SYSSTAT)\s*\.",
    "current_time_special": r"\bCURRENT\s+(?:TIMESTAMP|DATE|TIME)\b",
    "timestamp_arithmetic": r"\b(?:TIMESTAMPDIFF|TIMESTAMP_FORMAT|DAYS|MIDNIGHT_SECONDS|ADD_MONTHS|MONTHS_BETWEEN)\s*\(",
    "date_formatting": r"\b(?:TO_CHAR|TO_DATE|TO_TIMESTAMP|VARCHAR_FORMAT|DATE_FORMAT)\s*\(",
    "null_functions": r"\b(?:NVL|NVL2|VALUE|IFNULL|ISNULL|COALESCE)\s*\(",
    "decode_function": r"\bDECODE\s*\(",
    "row_number_paging": r"\b(?:ROWNUM|ROW_NUMBER\s*\(|OFFSET\s+\d+|LIMIT\s+\d+)\b",
    "oracle_outer_join": r"\(\s*\+\s*\)",
    "sequence_identity": r"\b(?:NEXTVAL|CURRVAL|NEXT\s+VALUE\s+FOR|IDENTITY_VAL_LOCAL)\b",
    "lock_for_update": r"\bFOR\s+UPDATE\b",
    "merge_upsert": r"\bMERGE\s+INTO\b",
    "catalog_metadata": r"\b(?:ALL_TAB_COLUMNS|USER_TAB_COLUMNS|ALL_TABLES|USER_TABLES|ALL_COL_COMMENTS|USER_COL_COMMENTS|SYSCOLUMNS|SYSTABLES)\b",
    "stored_program_call": r"\b(?:CALL\s+[A-Za-z_]\w*|CommandType\s*[:.]\s*StoredProcedure)\b",
    "sql_bind_marker": r"@[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)?",
    "transaction_api": r"\b(?:BeginTransaction|Commit|Rollback|AutoCommit|SetAutoCommit)\s*\(",
    "db_error_branch": r"\b(?:SQLCODE|SQLSTATE|GetSqlCode|GetSQLState)\b",
    "sql_generation": r"\b(?:sqlstr|sql_str|sqlString|c_sql|v_sql)\w*\s*\+?=",
}
TOKENS = re.compile(r'//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'')


def without_comments(text):
    return TOKENS.sub(
        lambda m: re.sub(r"[^\n]", " ", m.group()) if m.group().startswith(("//", "/*")) else m.group(),
        text,
    )


def main():
    files = sorted((ROOT / "Server").rglob("*.cpp"))
    files += sorted((ROOT / "Client" / "xr-qmbs-ag" / "server").rglob("*.cpp"))
    patterns = {name: re.compile(pattern, re.I) for name, pattern in RULES.items()}
    file_records = []
    encodings = Counter()
    for path in files:
        raw = path.read_bytes()
        try:
            text = raw.decode("utf-8-sig")
            encodings["utf-8"] += 1
        except UnicodeDecodeError:
            text = raw.decode("gb18030", errors="replace")
            encodings["gb18030_fallback"] += 1
        code = without_comments(text)
        features = {}
        for name, pattern in patterns.items():
            lines = sorted({code.count("\n", 0, match.start()) + 1 for match in pattern.finditer(code)})
            if lines:
                features[name] = lines
        file_records.append({"path": path.relative_to(ROOT).as_posix(), "features": features})
    totals = {name: sum(name in f["features"] for f in file_records) for name in RULES}
    report = {
        "scope": ["Server/**/*.cpp", "Client/xr-qmbs-ag/server/**/*.cpp"],
        "method": "Regex candidates after masking ordinary C++ comments and retaining string literals. Not a C++/SQL parser. Raw strings, SQL comments, inactive preprocessor branches and runtime-generated SQL require review. Feature totals overlap; file hits are not SQL statement counts or confirmed incompatibilities.",
        "source_file_count": len(files),
        "encoding_reads": dict(encodings),
        "rule_patterns": RULES,
        "files_by_feature": totals,
        "files": file_records,
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"source_file_count": len(files), "files_by_feature": totals}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
