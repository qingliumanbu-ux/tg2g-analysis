# -*- coding: utf-8 -*-
# tmsme96_inq.cpp 全量转换(此前转换已丢失,按台账既有编号 CHANGE-108/109/346~355 重做)
# 口径:HR-001(14位 YYYYMMDDHH24MISS) + HR-002/004/006 口径①(实际完整时长,整数除法截断)
import hashlib, re, shutil

P = 'Server/TMSM/p_tmsm_7160/tmsme96_inq.cpp'
BAK = 'analysis/dameng-migration/batches/tsdiff-tmsme96_inq.cpp.bak'
shutil.copyfile(P, BAK)
raw = open(P, 'rb').read()
t = raw.decode('gb18030')
assert '\r\n' not in t
lines = t.split('\n')

T = '"YYYYMMDDHH24MISS"'
CH = 'ttmsm66["CHANGE_TIME"].ToString()'
RC = 'ttmsm66["REC_CREATE_TIME"].ToString()'
EN = 'dt_temp.Rows[j]["END_TIME"].ToString().Trim()'
ST = 'dt_temp.Rows[j]["START_TIME"].ToString().Trim()'
ED = 'dt_temp.Rows[j]["E_DATETIME"].ToString().Trim()'
SD = 'dt_temp.Rows[j]["S_DATETIME"].ToString().Trim()'

def block(no, biz, old_lines, new_lines, unit_desc):
    lead = old_lines[0][:len(old_lines[0]) - len(old_lines[0].lstrip())]
    out = []
    out.append(lead + '// DM8 适配 CHANGE-' + no + ':' + biz + '。')
    out.append(lead + '// 改写原因：' + unit_desc + '按 HR-002 确认口径①(实际完整时长)')
    out.append(lead + '//   改为 DATEDIFF(SECOND,起点,终点)/因子,整数除法与 DB2 截断行为一致。')
    out.append(lead + "//   时间值为 14 位 YYYYMMDDHH24MISS(HR-001 已确认),用 TO_TIMESTAMP 显式指定;SYSIBM 辅助表改为 DUAL;依据 DM 官方文档,DM8 尚未实测。")
    out.append(lead + '// 本共用分支面向 DM8,其他 DB_KIND 标签也会执行此 SQL;参数、结果列、条件与排序保持不变。')
    out.append(lead + '// 原 SQL（完整保留）：')
    for ol in old_lines:
        out.append(lead + '// ' + ol.strip())
    out.append(lead + '// DM8 SQL：')
    out.extend(new_lines)
    return out

R_HOURS = 'DB2 两参数 TIMESTAMPDIFF(8=小时) 在 DM8 无对应写法,'
R_MIN = 'DB2 两参数 TIMESTAMPDIFF(4=分钟) 在 DM8 无对应写法,'

jobs = []  # (start_line_idx0, end_line_idx0_exclusive, comment_block_lines)

def find_one(pat):
    hits = [i for i, l in enumerate(lines)
            if re.search(pat, l) and not l.strip().startswith('//') and not l.strip().startswith('*')]
    assert len(hits) == 1, (pat, hits)
    return hits[0]

# --- CHANGE-108: DAYS 日历天数差 ---
i = find_one(r'sqlstr = "select DAYS\(DATE\(TIMESTAMP')
old = [lines[i]]
new = ['\t\t\tsqlstr = "select DATEDIFF(DAY, TO_TIMESTAMP(\'' + '" + ' + RC + ' + "' + '\',' + T + '), TO_TIMESTAMP(\'' + '" + ' + CH + ' + "' + '\',' + T + ')) from DUAL";']
jobs.append((i, i + 1, block('108', '查询设备状态记录创建(REC_CREATE_TIME)到变更(CHANGE_TIME)的日历天数差',
                             old, new,
                             'DB2 DAYS(日期) 差改为 DM8 DATEDIFF(DAY,·),')))

# --- CHANGE-346: 小时差 REC→CHG ---
i = find_one(r'sqlstr = "select TIMESTAMPDIFF\(8,')
old = [lines[i]]
new = ['\t\t\tsqlstr = "select DATEDIFF(SECOND, TO_TIMESTAMP(\'' + '" + ' + RC + ' + "' + '\',' + T + '), TO_TIMESTAMP(\'' + '" + ' + CH + ' + "' + '\',' + T + ')) / 3600 from DUAL";']
jobs.append((i, i + 1, block('346', '查询设备状态记录持续小时数,写入 hours_diffx',
                             old, new, R_HOURS)))

# --- CHANGE-347: 分钟差 REC→CHG ---
i = find_one(r'sqlstr = "select TIMESTAMPDIFF\(4, CHAR\(TIMESTAMP\(\'" \+ ttmsm66')
old = [lines[i]]
new = ['\t\t\tsqlstr = "select DATEDIFF(SECOND, TO_TIMESTAMP(\'' + '" + ' + RC + ' + "' + '\',' + T + '), TO_TIMESTAMP(\'' + '" + ' + CH + ' + "' + '\',' + T + ')) / 60 from DUAL";']
jobs.append((i, i + 1, block('347', '查询设备状态记录持续分钟数,写入 minutes_diffx 并累计到 all_time',
                             old, new, R_MIN)))

# --- CHANGE-348~354: 7 条相同 END/START 分钟差(倒罐/脱硫/转炉/吹氩/RH/LF/连铸) ---
biz = {
    '348': '查询倒罐作业(TMMSM12)开始到结束的分钟数,累计 use_time',
    '349': '查询脱硫作业(TMMSM14)开始到结束的分钟数,累计 use_time',
    '350': '查询转炉作业(TMMSM21)开始到结束的分钟数,累计 use_time',
    '351': '查询吹氩作业(TMMSM22)开始到结束的分钟数,累计 use_time',
    '352': '查询RH作业(TMMSM23)开始到结束的分钟数,累计 use_time',
    '353': '查询LF作业(TMMSM22)开始到结束的分钟数,累计 use_time',
    '354': '查询连铸作业(TMMSM31)开始到结束的分钟数,累计 use_time',
}
pat_es = re.compile(r'sqlstr = "select TIMESTAMPDIFF\(4, CHAR\(TIMESTAMP\(\'" \+ dt_temp\.Rows\[j\]\["END_TIME"\]')
hits = [i for i, l in enumerate(lines) if pat_es.search(l) and not l.strip().startswith('//')]
assert len(hits) == 7, hits
for no, i in zip(['348', '349', '350', '351', '352', '353', '354'], hits):
    old = [lines[i]]
    lead = old[0][:len(old[0]) - len(old[0].lstrip())]
    new = [lead + 'sqlstr = "select DATEDIFF(SECOND, TO_TIMESTAMP(\'' + '" + ' + ST + ' + "' + '\',' + T + '), TO_TIMESTAMP(\'' + '" + ' + EN + ' + "' + '\',' + T + ')) / 60 from DUAL";']
    jobs.append((i, i + 1, block(no, biz[no], old, new, R_MIN)))

# --- CHANGE-355: 维修 E/S 分钟差 ---
i = find_one(r'sqlstr = "select TIMESTAMPDIFF\(4, CHAR\(TIMESTAMP\(\'" \+ dt_temp\.Rows\[j\]\["E_DATETIME"\]')
old = [lines[i]]
new = ['\t\t\t\t\tsqlstr = "select DATEDIFF(SECOND, TO_TIMESTAMP(\'' + '" + ' + SD + ' + "' + '\',' + T + '), TO_TIMESTAMP(\'' + '" + ' + ED + ' + "' + '\',' + T + ')) / 60 from DUAL";']
jobs.append((i, i + 1, block('355', '查询维修作业(TTMSM95,STATUS=11)开始到结束的分钟数,累计 repair_time',
                             old, new, R_MIN)))

# --- CHANGE-109: 汇总 ROUND 语句 SYSIBM→DUAL(三行) ---
i = find_one(r'FROM SYSIBM\.SYSDUMMY1";\s*$')
old = [lines[i - 2], lines[i - 1], lines[i]]
assert 'SELECT ROUND(' in old[0] and 'repair_time' in old[1]
lead = old[2][:len(old[2]) - len(old[2].lstrip())]
new = [old[0].rstrip(), old[1].rstrip(), lead + '" FROM DUAL";']
jobs.append((i - 2, i + 1, block('109', '汇总使用/空闲/维修时长(小时)与作业率(good_rate),纯算术表达式',
                                 old, new,
                                 'SYSIBM.SYSDUMMY1 辅助表改为 DUAL;计算口径与参数不变;')))

# --- 自下而上替换 ---
jobs.sort(key=lambda x: -x[0])
for s, e, blk in jobs:
    lines[s:e] = blk

t2 = '\n'.join(lines)
open(P, 'wb').write(t2.encode('gb18030'))

# --- 断言 ---
chk = open(P, 'rb').read().decode('gb18030')
cl = chk.split('\n')
res = [l for l in cl if not l.strip().startswith('//') and not l.strip().startswith('*')
       and (re.search(r'TIMESTAMPDIFF\s*\(', l, re.I) or re.search(r'\bDAYS\(', l)
            or 'SYSIBM' in l.upper() or 'SYSDUMMY1' in l.upper())]
assert not res, res
for no in ['108', '109'] + [str(x) for x in range(346, 356)]:
    assert ('CHANGE-' + no + ':') in chk, no
# 注释还原:每条 "原 SQL" 标记后紧邻行去前缀,须与其对应备份中的原行一致
bak_lines = open(BAK, 'rb').read().decode('gb18030').split('\n')
orig_active = [l for l in bak_lines if re.search(r'sqlstr = "select (TIMESTAMPDIFF|DAYS)\(', l)
               or 'FROM SYSIBM.SYSDUMMY1";' in l]
restored = []
for i2, l in enumerate(cl):
    if '原 SQL（完整保留）：' in l:
        for j in range(i2 + 1, len(cl)):
            s = cl[j].strip()
            if s.startswith('// '):
                restored.append(s[3:])
            else:
                break
restored_set = set(x.strip() for x in restored)
orig_set = set(x.strip() for x in orig_active)
assert orig_set <= restored_set, ('missing restores', orig_set - restored_set)
sha = hashlib.sha256(open(P, 'rb').read()).hexdigest()
print('ALL ASSERTIONS PASS, 12 blocks converted, sha256=' + sha)
