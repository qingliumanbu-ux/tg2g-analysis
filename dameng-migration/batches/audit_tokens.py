# -*- coding: utf-8 -*-
"""全量核对:提取全部活动 SQL -> 模板去重 -> 未知函数/标记清查。"""
import io
import os
import re
import sys
import hashlib
import pickle

sys.path.insert(0, r"D:\work\company\太钢二炼钢\analysis\dameng-migration\batches\wmsm")
import dm8lib

WL_FUNCS = set('''
ABS ACOS ASIN ATAN ATAN2 CEIL CEILING COS COSH COT DEGREES EXP FLOOR LN LOG LOG10 MOD PI POWER
RADIANS RAND ROUND SIGN SIN SINH SQRT TAN TANH TRUNC TRUNCATE BITAND GREATEST GREAT LEAST
TO_NUMBER BINTODEC DECTOBIN NCHAR
ASCII ASCIISTR BIT_LENGTH CHAR CHR CONCAT CONCAT_WS DIFFERENCE INITCAP INSERT INSTR INSTRB
LCASE LEFT LEN LENGTH LENGTHB LOCATE LOWER LPAD LTRIM OCTET_LENGTH POSITION REPEAT REPLACE
REPLICATE REVERSE RIGHT RPAD RTRIM SOUNDEX SPACE STRCOMPARE STRPOS STRPOSDEC STRPOSINC STUFF
SUBSTR SUBSTRB SUBSTR2 SUBSTR4 SUBCODE TO_CHAR TRANSLATE TRIM UCASE UPPER TEXT_START TEXT_END
EMPTY_CLOB EMPTY_BLOB
ADD_DAYS ADD_MONTHS ADD_WEEKS CURDATE CURTIME CURRENT_DATE CURRENT_TIME CURRENT_TIMESTAMP
DATEADD DATEDIFF DATENAME DATEPART DAY DAYNAME DAYOFMONTH DAYOFWEEK DAYOFYEAR DAYS_BETWEEN
EXTRACT GETDATE GETUTCDATE LAST_DAY LOCALTIME LOCALTIMESTAMP MONTH MONTHNAME MONTHS_BETWEEN
NEXT_DAY NOW QUARTER SECOND SYSDATE SYSTIMESTAMP TIME TIMESTAMPADD TIMESTAMPDIFF TO_DATE
TO_TIME TO_TIMESTAMP WEEK WEEKDAY WEEKS_BETWEEN YEAR TIMESTAMP
COALESCE IFNULL ISNULL NULLIF NVL NULL_EQU NVL2 DECODE
AVG COUNT MAX MIN SUM LISTAGG LISTAGG2 STDDEV STDDEV_POP STDDEV_SAMP VARIANCE VAR_POP VAR_SAMP
RANK DENSE_RANK ROW_NUMBER FIRST_VALUE LAST_VALUE LAG LEAD NTILE PERCENT_RANK RATIO_TO_REPORT
GROUPING GROUPING_ID WM_CONCAT MEDIAN
CAST CONVERT HEX TO_BLOB USER UID DATABASE SPL
INSTR2 INSTR4 POSITIONB TO_DOUBLE TO_DEC
'''.split())

WL_KEYWORDS = set('''
SELECT FROM WHERE AND OR NOT IN IS NULL LIKE BETWEEN EXISTS UNION EXCEPT MINUS
INTERSECT DISTINCT ALL AS ASC DESC ORDER BY GROUP HAVING JOIN INNER LEFT RIGHT FULL OUTER
ON USING CASE WHEN THEN ELSE END INTO VALUES INSERT UPDATE SET DELETE MERGE CREATE DROP
ALTER TABLE VIEW INDEX SEQUENCE TRIGGER PROCEDURE WITH RECURSIVE START CONNECT BY PRIOR
LEVEL ROWNUM FETCH FIRST NEXT ROWS ONLY OFFSET LIMIT TOP PERCENT TIES FOR UPDATE OF
NOWAIT READ COMMIT ROLLBACK SAVEPOINT TRANSACTION ISOLATION COMMITTED UNCOMMITTED
SERIALIZABLE GRANT REVOKE PRIMARY KEY FOREIGN REFERENCES CHECK UNIQUE DEFAULT CONSTRAINT
CASCADE NVL2 CURRENT_USER SESSION_USER SYSTEM_USER CURRENT_SCHEMA
ADD CACHE TRUNCATE COMMENT ENABLE DISABLE IDENTITY CYCLE NOCYCLE NOCACHE
NOORDER MAXVALUE MINVALUE INCREMENT START INT BIGINT SMALLINT TINYINT
BIT DECIMAL NUMERIC NUMBER FLOAT DOUBLE REAL CHAR VARCHAR VARCHAR2 TEXT CLOB BLOB IMAGE
DATE TIME DATETIME TIMESTAMP BINARY VARBINARY ROWID INTERVAL YEAR MONTH DAY HOUR
MINUTE SECOND ZONE
PARTITION OVER ROWS RANGE UNBOUNDED PRECEDING FOLLOWING CURRENT KEEP DENSE_RANK
LOCK WAIT HOLDLOCK LENGTHB INSTRB SUBSTRB SUBSTR4
LEADING TRAILING BOTH ANY SOME ALL ESCAPE
RETURNING OUTPUT TABLESPACE PCTFREE
'''.split())

MARKERS = re.compile(
    r'\(\+\)|\bMINUS\b|\bCONNECT\s+BY\b|\bSTART\s+WITH\b|\bLISTAGG\s*\(|\bPOSSTR\s*\(|'
    r'\bWITH\s+(?:UR|RS|CS|RR)\b|\bLOCK\s+TABLE\b|\bSET\s+SCHEMA\b|\bCOMMENT\s+ON\b|'
    r'\bLABEL\s+ON\b|\bVALUES\s+INTO\b|\bFOR\s+READ\s+ONLY\b|\bOPTIMIZE\s+FOR\b|'
    r'\bKEEP\s+UPDATE\b|\bEXECUTE\s+IMMEDIATE\b|\bPREPARE\b|\bDECLARE\b|\bCALL\b|'
    r'\bDECFLOAT\b|\bSQLCODE\b|\bSQLSTATE\b|\bMICROSECOND\b|\bRID\s*\(|\bDIGITS\s*\(|'
    r'\bTIMESTAMP_FORMAT\s*\(|\bVARCHAR_FORMAT\s*\(|\bXMLELEMENT\b|\bXMLQUERY\b', re.I)

FUNC = re.compile(r'([A-Za-z_][A-Za-z0-9_]*)\s*\(')
COVERED = re.compile(
    r'(?:SetCommandText|QueryCString|QueryCDecimal|QueryTable|ExecuteNonQuery|'
    r'ExecuteScalar|ExecuteReader|Execute|CDbCommand\s+\w+\s*\(|sprintf\s*\(|'
    r'\.Format\s*\()', re.I)


def extract_sql_text(lines, s, e):
    parts = []
    for k in range(s, e + 1):
        for m in re.finditer(r'"([^"]*)"', lines[k]):
            parts.append(m.group(1))
    return ' '.join(parts)


def normalize(sql):
    sql = re.sub(r"'(?:[^']|'')*'", '?', sql)
    sql = re.sub(r'@\w+', '?', sql)
    sql = re.sub(r'\s+', ' ', sql).strip().upper()
    return sql


report = {}
for mod in sorted(os.listdir(r'D:\work\company\太钢二炼钢\Server')):
    mdir = os.path.join(r'D:\work\company\太钢二炼钢\Server', mod)
    if not os.path.isdir(mdir):
        continue
    dm8lib.set_module(mod)
    pats = {}
    for dp, dn, fn in os.walk(mdir):
        if '.git' in dn:
            dn.remove('.git')
        for f in fn:
            if not f.lower().endswith('.cpp'):
                continue
            p = os.path.join(dp, f)
            raw = open(p, 'rb').read()
            try:
                text = raw.decode('utf-8')
            except UnicodeDecodeError:
                text = raw.decode('gb18030', errors='replace')
            lines = text.split('\n')
            blocks = dm8lib.find_blocks(lines)
            segs = []
            for (s, e, ap) in blocks:
                segs.append(extract_sql_text(lines, s, e))
            for k, l in enumerate(lines, 1):
                s2 = l.strip()
                if s2.startswith('//'):
                    continue
                if dm8lib.SQLVAR_ASSIGN.match(l):
                    continue
                m2 = re.search(r'"([^"]*)"', l)
                if m2 and COVERED.search(l):
                    segs.append(m2.group(1))
            for sqlt in segs:
                nz = normalize(sqlt)
                if len(nz) < 12:
                    continue
                h = hashlib.md5(nz.encode()).hexdigest()[:10]
                if h not in pats:
                    pats[h] = {'sql': nz[:300], 'files': set(),
                               'tokens': set(), 'markers': set()}
                pats[h]['files'].add(f)
                for fm in FUNC.finditer(sqlt):
                    name = fm.group(1).upper()
                    if name not in WL_FUNCS and name not in WL_KEYWORDS:
                        pats[h]['tokens'].add(name)
                for mm in MARKERS.finditer(sqlt):
                    pats[h]['markers'].add(mm.group(0).upper())
    report[mod] = pats

unk = {}
tot = 0
marker_pats = {}
for mod, pats in report.items():
    tot += len(pats)
    for h, info in pats.items():
        for tk in info['tokens']:
            unk.setdefault(tk, []).append(
                (mod, h, sorted(info['files'])[:2], info['sql'][:130]))
        if info['markers']:
            marker_pats.setdefault(
                tuple(sorted(info['markers'])), []).append(
                (mod, sorted(info['files'])[:2], info['sql'][:150]))

print('distinct SQL templates:', tot)
print('unknown function tokens:', len(unk))
out = io.open(r'D:\work\company\太钢二炼钢\analysis\dameng-migration\batches\_tokens.txt',
              'w', encoding='utf-8')
for tk in sorted(unk):
    out.write(f'== {tk} ({len(unk[tk])} patterns)\n')
    for mod, h, files, sql in unk[tk][:2]:
        out.write(f'   [{mod}] {files}\n     {sql}\n')
out.write('\n==== MARKER PATTERNS ====\n')
for mk, lst in sorted(marker_pats.items()):
    out.write(f'== {" & ".join(mk)} ({len(lst)} patterns)\n')
    for mod, files, sql in lst[:1]:
        out.write(f'   [{mod}] {files}\n     {sql}\n')
out.close()
with open(r'D:\work\company\太钢二炼钢\analysis\dameng-migration\batches\_pats.pkl',
          'wb') as f:
    pickle.dump({m: {h: {'sql': v['sql'], 'files': sorted(v['files']),
                         'tokens': sorted(v['tokens']),
                         'markers': sorted(v['markers'])}
                     for h, v in p.items()} for m, p in report.items()}, f)
print('saved _pats.pkl')
