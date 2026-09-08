# -*- coding: utf-8 -*-
# HR-002/004/006 口径① 落地:两参数 TIMESTAMPDIFF -> DATEDIFF(SECOND,起点,终点)/因子
# 因子: 2秒=1, 4分=60, 8时=3600, 16天=86400 (整数除法与 DB2 截断行为一致)
# 仅处理单行/两行的简单语句;每条:更新既有注释块的改写原因,替换活动 SQL,保留最初原 SQL 注释不动。
import hashlib, shutil, os

CH = chr(92)  # backslash (not needed but kept for safety)

def load(p):
    raw = open(p, 'rb').read()
    for enc in ('utf-8', 'gb18030'):
        try:
            return raw.decode(enc), enc, ('rn' and b'\r\n' in raw)
        except UnicodeDecodeError:
            continue
    raise RuntimeError('decode fail: ' + p)

def q(s):  # 单引号字符串在 C++ 内无需转义,直接拼
    return s

JOBS = []
# ---------------- TMSM: f_tmsm01_60106 (CHANGE-340) ----------------
JOBS.append(dict(
    path='Server/TMSM/libTMSM/f_tmsm01_60106.cpp',
    old_active=['\t\t\tsqlstr = "select TIMESTAMPDIFF(4, CHAR(TIMESTAMP(\'" + datetime + "\')  - TIMESTAMP(\'" + usage_st + "\'))) from DUAL";'],
    new_active=['\t\t\tsqlstr = "select DATEDIFF(SECOND, TO_TIMESTAMP(\'" + usage_st + "\',\'YYYYMMDDHH24MISS\'), TO_TIMESTAMP(\'" + datetime + "\',\'YYYYMMDDHH24MISS\')) / 60 from DUAL";'],
    old_reason='// 改写原因：SYSIBM 辅助表改为 DUAL；依据 DM 官方文档,DM8 尚未实测。',
    new_reason=[
        '// 改写原因：DB2 两参数 TIMESTAMPDIFF(4=分钟,钢包盛钢时长) 在 DM8 无对应写法,按 HR-002 确认口径①(实际完整时长)',
        '//   改为 DATEDIFF(SECOND,起点=使用开始时间,终点=当前时间)/60,整数除法与 DB2 截断行为一致。',
        '//   时间值为 14 位 YYYYMMDDHH24MISS(HR-001 已确认),用 TO_TIMESTAMP 显式指定;SYSIBM 辅助表改为 DUAL;依据 DM 官方文档,DM8 尚未实测。',
    ],
    first='// DM8 适配 CHANGE-340:查询。SYSIBM 辅助表改为 DUAL。',
    new_first='// DM8 适配 CHANGE-340:查询钢包盛钢时长(分钟),写入 l_ladle_fill_time。',
))

# ---------------- MMSM: mmsmis02_inq (CHANGE-163) ----------------
_TS = "timestamp('\"+{v}+\"','yyyy-MM-DD hh:mm:ss')"
_old_163 = '\t\t\t\tsqlstr_outTIME = "select timestampdiff(8,char(timestamp(\'"+v_in_stock_hot_time+"\',\'yyyy-MM-DD hh:mm:ss\') - timestamp(\'"+v_slab_cut_time+"\',\'yyyy-MM-DD hh:mm:ss\')))  from DUAL";'
_new_163 = '\t\t\t\tsqlstr_outTIME = "select DATEDIFF(SECOND, TO_TIMESTAMP(\'"+v_slab_cut_time+"\',\'YYYYMMDDHH24MISS\'), TO_TIMESTAMP(\'"+v_in_stock_hot_time+"\',\'YYYYMMDDHH24MISS\')) / 3600 from DUAL";'
JOBS.append(dict(
    path='Server/MMSM/p_mmsm_17520/mmsmis02_inq.cpp',
    old_active=[_old_163], new_active=[_new_163],
    old_reason='// 改写原因：SYSIBM 辅助表改为 DUAL；依据 DM 官方文档,DM8 尚未实测。',
    new_reason=[
        '// 改写原因：DB2 两参数 TIMESTAMPDIFF(8=小时,切断到热装入库经过的小时数,写入 OUT_HOT_TIME) 在 DM8 无对应写法,按 HR-002 确认口径①(实际完整时长)',
        '//   改为 DATEDIFF(SECOND,起点=切断时间,终点=热装入库时间)/3600,整数除法与 DB2 截断行为一致。',
        '//   timestamp(x,格式串) 改为 TO_TIMESTAMP(x,\'YYYYMMDDHH24MISS\'):时间为 14 位值(HR-001 已确认),原格式串 yyyy-MM-DD hh:mm:ss 与值不匹配;',
        '//   SYSIBM 辅助表改为 DUAL;依据 DM 官方文档,DM8 尚未实测。',
    ],
    first='// DM8 适配 CHANGE-163:查询。SYSIBM 辅助表改为 DUAL。',
    new_first='// DM8 适配 CHANGE-163:查询切断到热装入库的小时差,写入 OUT_HOT_TIME。',
))

# ---------------- MMSM: mmsmis02_inqa (CHANGE-164) ----------------
JOBS.append(dict(
    path='Server/MMSM/p_mmsm_17520/mmsmis02_inqa.cpp',
    old_active=['\t\t\t\tsqlstr_outTIME = "select timestampdiff(8,char(timestamp(\'"+v_in_stock_hot_time+"\',\'yyyy-MM-DD hh:mm:ss\') - timestamp(\'"+v_slab_cut_time+"\',\'yyyy-MM-DD hh:mm:ss\')))  from DUAL";'],
    new_active=['\t\t\t\tsqlstr_outTIME = "select DATEDIFF(SECOND, TO_TIMESTAMP(\'"+v_slab_cut_time+"\',\'YYYYMMDDHH24MISS\'), TO_TIMESTAMP(\'"+v_in_stock_hot_time+"\',\'YYYYMMDDHH24MISS\')) / 3600 from DUAL";'],
    old_reason='// 改写原因：SYSIBM 辅助表改为 DUAL；依据 DM 官方文档,DM8 尚未实测。',
    new_reason=[
        '// 改写原因：DB2 两参数 TIMESTAMPDIFF(8=小时,切断到热装入库经过的小时数,写入 OUT_HOT_TIME) 在 DM8 无对应写法,按 HR-002 确认口径①(实际完整时长)',
        '//   改为 DATEDIFF(SECOND,起点=切断时间,终点=热装入库时间)/3600,整数除法与 DB2 截断行为一致。',
        '//   timestamp(x,格式串) 改为 TO_TIMESTAMP(x,\'YYYYMMDDHH24MISS\'):时间为 14 位值(HR-001 已确认),原格式串 yyyy-MM-DD hh:mm:ss 与值不匹配;',
        '//   SYSIBM 辅助表改为 DUAL;依据 DM 官方文档,DM8 尚未实测。',
    ],
    first='// DM8 适配 CHANGE-164:查询。SYSIBM 辅助表改为 DUAL。',
    new_first='// DM8 适配 CHANGE-164:查询切断到热装入库的小时差,写入 OUT_HOT_TIME。',
))

# ---------------- MMSM: mmsmis02a1_inq (CHANGE-165/166) ----------------
_o165 = '\t\t\t\t\tsqlstr_COLDTIME="select timestampdiff(8,char(CURRENT_TIMESTAMP - timestamp(\'"+v_slab_cut_time+"\',\'yyyy-MM-DD hh:mm:ss\')))  from DUAL";'
_n165 = '\t\t\t\t\tsqlstr_COLDTIME="select DATEDIFF(SECOND, TO_TIMESTAMP(\'"+v_slab_cut_time+"\',\'YYYYMMDDHH24MISS\'), CURRENT_TIMESTAMP) / 3600 from DUAL";'
_o166 = '\t\t\t\t\t\tsqlstr_COLDTIME="select timestampdiff(8,char(timestamp(\'"+v_in_stock_hot_time+"\',\'yyyy-MM-DD hh:mm:ss\') - timestamp(\'"+v_slab_cut_time+"\',\'yyyy-MM-DD hh:mm:ss\')))  from DUAL";'
_n166 = '\t\t\t\t\t\tsqlstr_COLDTIME="select DATEDIFF(SECOND, TO_TIMESTAMP(\'"+v_slab_cut_time+"\',\'YYYYMMDDHH24MISS\'), TO_TIMESTAMP(\'"+v_in_stock_hot_time+"\',\'YYYYMMDDHH24MISS\')) / 3600 from DUAL";'
_r165 = [
    '// 改写原因：DB2 两参数 TIMESTAMPDIFF(8=小时,当前时间减切断时间的小时数,写入 IN_STOCK_DURA 在库时长) 在 DM8 无对应写法,按 HR-002 确认口径①(实际完整时长)',
    '//   改为 DATEDIFF(SECOND,起点=切断时间,终点=当前时间)/3600,整数除法与 DB2 截断行为一致。',
    '//   timestamp(x,格式串) 改为 TO_TIMESTAMP(x,\'YYYYMMDDHH24MISS\'):时间为 14 位值(HR-001 已确认),原格式串 yyyy-MM-DD hh:mm:ss 与值不匹配;',
    '//   当前时点沿用 CURRENT_TIMESTAMP(DM 官方函数手册支持);SYSIBM 辅助表改为 DUAL;依据 DM 官方文档,DM8 尚未实测。',
]
_r166 = [
    '// 改写原因：DB2 两参数 TIMESTAMPDIFF(8=小时,切断到热装入库的小时数,写入 IN_STOCK_TIME_DURA) 在 DM8 无对应写法,按 HR-002 确认口径①(实际完整时长)',
    '//   改为 DATEDIFF(SECOND,起点=切断时间,终点=热装入库时间)/3600,整数除法与 DB2 截断行为一致。',
    '//   timestamp(x,格式串) 改为 TO_TIMESTAMP(x,\'YYYYMMDDHH24MISS\'):时间为 14 位值(HR-001 已确认),原格式串 yyyy-MM-DD hh:mm:ss 与值不匹配;',
    '//   SYSIBM 辅助表改为 DUAL;依据 DM 官方文档,DM8 尚未实测。',
]
JOBS.append(dict(
    path='Server/MMSM/p_mmsm_17520/mmsmis02a1_inq.cpp',
    old_active=[_o165, _o166], new_active=[_n165, _n166],
    old_reason='// 改写原因：SYSIBM 辅助表改为 DUAL；DB2 特殊寄存器 current date/time/timestamp 改为 DM 的 CURRENT_DATE/CURRENT_TIME/CURRENT_TIMESTAMP(官方函数手册支持)；依据 DM 官方文档,DM8 尚未实测。',
    new_reason=_r165,
    old_reason2='// 改写原因：SYSIBM 辅助表改为 DUAL；依据 DM 官方文档,DM8 尚未实测。',
    new_reason2=_r166,
    first='// DM8 适配 CHANGE-165:查询。SYSIBM 辅助表改为 DUAL。',
    new_first='// DM8 适配 CHANGE-165:查询当前时间减切断时间的小时数,写入 IN_STOCK_DURA(在库时长)。',
    first2='// DM8 适配 CHANGE-166:查询。SYSIBM 辅助表改为 DUAL。',
    new_first2='// DM8 适配 CHANGE-166:查询切断到热装入库的小时数,写入 IN_STOCK_TIME_DURA。',
))

# ---------------- MMSM: mmsmis02a1_inqa (CHANGE-167/168) ----------------
JOBS.append(dict(
    path='Server/MMSM/p_mmsm_17520/mmsmis02a1_inqa.cpp',
    old_active=[_o165, _o166], new_active=[_n165, _n166],
    old_reason='// 改写原因：SYSIBM 辅助表改为 DUAL；DB2 特殊寄存器 current date/time/timestamp 改为 DM 的 CURRENT_DATE/CURRENT_TIME/CURRENT_TIMESTAMP(官方函数手册支持)；依据 DM 官方文档,DM8 尚未实测。',
    new_reason=_r165,
    old_reason2='// 改写原因：SYSIBM 辅助表改为 DUAL；依据 DM 官方文档,DM8 尚未实测。',
    new_reason2=_r166,
    first='// DM8 适配 CHANGE-167:查询。SYSIBM 辅助表改为 DUAL。',
    new_first='// DM8 适配 CHANGE-167:查询当前时间减切断时间的小时数,写入 IN_STOCK_DURA(在库时长)。',
    first2='// DM8 适配 CHANGE-168:查询。SYSIBM 辅助表改为 DUAL。',
    new_first2='// DM8 适配 CHANGE-168:查询切断到热装入库的小时数,写入 IN_STOCK_TIME_DURA。',
))

def save(p, t, enc):
    open(p, 'wb').write(t.encode(enc))

def process(job):
    p = job['path']
    t, enc, crlf = load(p)
    eol = '\r\n' if crlf else '\n'
    # 统一按 \n 处理,保存时还原
    had_crlf = crlf
    t2 = t.replace('\r\n', '\n')
    assert job['old_active'][0] in t2, 'old_active[0] not found in ' + p
    # 1) 注释块首行(业务含义)
    if 'first' in job:
        assert job['first'] in t2, 'first not found: ' + p
        t2 = t2.replace(job['first'], job['new_first'], 1)
    if 'first2' in job:
        assert job['first2'] in t2, 'first2 not found: ' + p
        t2 = t2.replace(job['first2'], job['new_first2'], 1)
    # 2) 改写原因行(第一条)
    if 'old_reason' in job:
        assert job['old_reason'] in t2, 'old_reason not found: ' + p
        t2 = t2.replace(job['old_reason'], eol.join(job['new_reason']) if had_crlf else '\n'.join(job['new_reason']), 1)
    if 'old_reason2' in job:
        assert job['old_reason2'] in t2, 'old_reason2 not found: ' + p
        t2 = t2.replace(job['old_reason2'], eol.join(job['new_reason2']) if had_crlf else '\n'.join(job['new_reason2']), 1)
    # 3) 活动 SQL 替换
    for oa in job['old_active']:
        assert oa in t2, 'active not found: ' + oa[:60]
        idx = job['old_active'].index(oa)
        t2 = t2.replace(oa, job['new_active'][idx], 1)
    # 4) 断言
    # 4a) 原方案A 注释里的最初原 SQL 必须还在(以 sysdummy1/SYSIBM 标记核对)
    assert 'sysdummy1' in t2.lower() or 'SYSIBM' in t2, 'original comment lost: ' + p
    # 4b) 活动残留:不含未转换的 timestampdiff(
    lines = t2.split('\n')
    residue = [l for l in lines if 'timestampdiff' in l.lower() and not l.strip().startswith('//')
               and '原程序' not in l and not l.strip().startswith('*')]
    assert not residue, ('residue in ' + p, residue)
    # 4c) 括号平衡(活动行)
    for na in job['new_active']:
        expr = na.split('"')
        sqltext = ''.join(expr[i] for i in range(1, len(expr), 2) if not expr[i].startswith('+') or True) if False else na
        # 粗平衡:整行
        assert na.count('(') == na.count(')'), 'paren imbalance: ' + na
    if had_crlf:
        t2 = t2.replace('\n', '\r\n')
    save(p, t2, enc)
    sha = hashlib.sha256(open(p, 'rb').read()).hexdigest()
    return sha

results = []
for j in JOBS:
    bak = 'analysis/dameng-migration/batches/' + ('tsdiff-' + os.path.basename(j['path']) + '.bak')
    shutil.copyfile(j['path'], bak)
    sha = process(j)
    results.append((j['path'], sha))
    print('OK', j['path'], sha[:16])

with open('analysis/dameng-migration/batches/_tsdiff_small_done.txt', 'w', encoding='utf-8') as f:
    for p, sha in results:
        f.write(p + ' ' + sha + '\n')
print('ALL DONE')
