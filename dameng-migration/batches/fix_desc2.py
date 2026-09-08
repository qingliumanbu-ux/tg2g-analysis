# -*- coding: utf-8 -*-
"""修正全部转换块描述行:从活动 SQL 提取操作类型+表名,生成准确描述。"""
import csv, hashlib, io, os, re, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wmsm'))
import dm8lib

BASE = r'D:\work\company\太钢二炼钢\Server'
LEDGER = os.path.join(os.path.dirname(os.path.abspath(__file__)).replace(
    os.path.join('analysis', 'dameng-migration', 'batches'),
    os.path.join('analysis', 'dameng-migration')), 'sql-ledger.csv')

KNOWN = set(
    'ABS ACOS ASIN ATAN ATAN2 CEIL CEILING COS COSH COT DEGREES EXP FLOOR LN LOG LOG10 MOD PI '
    'POWER RADIANS RAND ROUND SIGN SIN SINH SQRT TAN TANH TRUNC TRUNCATE BITAND GREATEST GREAT '
    'LEAST TO_NUMBER ASCII CHR CONCAT INSTR LENGTH LENGTHB LENGTH2 LENGTH4 LOCATE LOWER LPAD '
    'LTRIM POSITION REPLACE REVERSE RIGHT RPAD RTRIM SOUNDEX SPACE SUBSTR SUBSTRB SUBSTR2 '
    'SUBSTR4 TO_CHAR TRANSLATE TRIM UCASE UPPER NVL NVL2 NULLIF COALESCE ISNULL IFNULL NULL_EQU '
    'ADD_DAYS ADD_MONTHS ADD_WEEKS CURDATE CURTIME CURRENT_DATE CURRENT_TIME CURRENT_TIMESTAMP '
    'DATEADD DATEDIFF DATENAME DATEPART DAY DAYNAME DAYOFMONTH DAYOFWEEK DAYOFYEAR '
    'DAYS_BETWEEN EXTRACT GETDATE LAST_DAY LOCALTIME LOCALTIMESTAMP MONTH MONTHNAME '
    'MONTHS_BETWEEN NEXT_DAY NOW QUARTER SECOND SYSDATE SYSTIMESTAMP TIME TIMESTAMPADD '
    'TIMESTAMPDIFF TO_DATE TO_TIME TO_TIMESTAMP WEEK WEEKDAY WEEKS_BETWEEN YEAR TIMESTAMP '
    'DECODE LISTAGG PIVOT UNPIVOT REGEXP_LIKE REGEXP_SUBSTR REGEXP_COUNT REGEXP_INSTR '
    'REGEXP_REPLACE SYS_GUID GUID NEWID AVG COUNT MAX MIN SUM RANK DENSE_RANK ROW_NUMBER '
    'FIRST_VALUE LAST_VALUE LAG LEAD CAST CONVERT USER UID DATABASE MEDIAN GROUPING '
    'GROUPING_ID SELECT FROM WHERE AND OR NOT IN IS NULL LIKE BETWEEN EXISTS UNION EXCEPT '
    'MINUS INTERSECT DISTINCT ALL AS ASC DESC ORDER GROUP HAVING JOIN INNER LEFT RIGHT FULL '
    'OUTER ON USING CASE WHEN THEN ELSE END INTO VALUES INSERT UPDATE SET DELETE MERGE CREATE '
    'DROP ALTER TABLE VIEW INDEX SEQUENCE TRIGGER PROCEDURE WITH RECURSIVE START CONNECT PRIOR '
    'LEVEL ROWNUM FETCH FIRST NEXT ROWS ONLY OFFSET LIMIT TOP FOR UPDATE NOWAIT COMMIT '
    'ROLLBACK PRIMARY KEY FOREIGN REFERENCES CHECK UNIQUE DEFAULT CONSTRAINT IDENTITY CACHE '
    'NOCACHE CYCLE NOCYCLE NOORDER MAXVALUE MINVALUE INCREMENT START INT BIGINT SMALLINT '
    'TINYINT BIT DECIMAL NUMERIC NUMBER FLOAT DOUBLE REAL CHAR VARCHAR VARCHAR2 TEXT CLOB BLOB '
    'IMAGE DATE TIME DATETIME TIMESTAMP BINARY VARBINARY NVL2 CURRENT_USER SESSION_USER '
    'PARTITION OVER ROWS RANGE UNBOUNDED PRECEDING FOLLOWING CURRENT KEEP LENGTHC INSTR2 '
    'INSTR4 POSITIONB TO_DOUBLE TO_DEC STRPOS ELSEIF TRY CATCH'
.split())

FUNC_PAT = re.compile(r'([A-Za-z_][A-Za-z0-9_]*)\s*\(')
OP_PATS = [
    (re.compile(r'\bINSERT\s+INTO\s+([A-Za-z_]\w*)', re.I), '写入'),
    (re.compile(r'\bUPDATE\s+([A-Za-z_]\w*)', re.I), '更新'),
    (re.compile(r'\bDELETE\s+FROM\s+([A-Za-z_]\w*)', re.I), '删除'),
    (re.compile(r'\bSELECT\b', re.I), '查询'),
]

total_fixed = 0
total_files = 0
for mod in sorted(os.listdir(BASE)):
    mdir = os.path.join(BASE, mod)
    if not os.path.isdir(mdir) or mod.startswith('.'):
        continue
    dm8lib.set_module(mod)
    for dp, dn, fn in os.walk(mdir):
        if '.git' in dn:
            dn.remove('.git')
        for f in sorted(fn):
            if not f.lower().endswith('.cpp'):
                continue
            fp = os.path.join(dp, f)
            raw = open(fp, 'rb').read()
            try:
                text = raw.decode('utf-8')
                enc = 'utf-8'
            except UnicodeDecodeError:
                text = raw.decode('gb18030')
                enc = 'gb18030'
            if '日期按天前推计算' not in text:
                continue
            lines = text.split('\n')
            changed = 0
            i = 0
            while i < len(lines):
                if 'DM8 适配 CHANGE-' not in lines[i]:
                    i += 1
                    continue
                m_cid = re.search(r'CHANGE-\d+', lines[i])
                cid = m_cid.group(0) if m_cid else 'CHANGE-???'
                reason_line = ''
                for j in range(i + 1, min(i + 6, len(lines))):
                    if '改写原因' in lines[j]:
                        reason_line = lines[j]
                        break
                dm8_idx = None
                for j in range(i, min(i + 30, len(lines))):
                    if 'DM8 SQL' in lines[j]:
                        dm8_idx = j
                        break
                sql_text = ''
                if dm8_idx is not None:
                    for j in range(dm8_idx + 1, min(dm8_idx + 40, len(lines))):
                        sl = lines[j].strip()
                        if sl.startswith('//'):
                            break
                        for mm in re.finditer(r'"([^"]*)"', sl):
                            sql_text += mm.group(1) + ' '
                        if sl.endswith(';') or sl.endswith('";'):
                            break
                ops = []
                tables = []
                for pat, op_name in OP_PATS:
                    for m2 in pat.finditer(sql_text):
                        if op_name not in ops:
                            ops.append(op_name)
                        if m2.lastindex and m2.lastindex >= 1:
                            tbl = m2.group(1).split('.')[-1].upper()
                            if tbl not in tables and not tbl.startswith('('):
                                tables.append(tbl)
                op_str = '/'.join(ops) if ops else 'SQL'
                tbl_str = ' '.join(tables[:2])
                new_desc = f'{cid}:{op_str}'
                if tbl_str:
                    new_desc += f' {tbl_str}'
                new_desc += '。'
                if reason_line:
                    rm = re.search(r'改写原因[：:](.+?)[；;]', reason_line)
                    if rm:
                        new_desc += rm.group(1).strip() + '。'
                    else:
                        rm2 = re.search(r'改写原因[：:](.+)', reason_line)
                        if rm2:
                            rp = rm2.group(1).split('；')[0].split('。')[0]
                            new_desc += rp.strip() + '。'
                lead = lines[i][:len(lines[i]) - len(lines[i].lstrip())]
                lines[i] = lead + '// ' + new_desc
                changed += 1
                total_fixed += 1
                i += 1
            if changed:
                open(fp, 'wb').write('\n'.join(lines).encode(enc))
                total_files += 1

print(f'修正: {total_files} 文件, {total_fixed} 行描述')
