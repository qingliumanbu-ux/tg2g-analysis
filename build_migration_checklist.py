"""Turn the existing scan into a review queue; never export source/config values."""
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime, timezone
import csv
import hashlib
import json
import os

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'analysis' / 'dameng-migration'
SCAN = ROOT / 'analysis' / 'database-workspace'
CODE = {'backend_source', 'web_source', 'desktop_source'}
# Application SQL conversion only. Runtime checks are not a global prerequisite.
RULES = [
    ('R01', '数据库分支选路', 'P1', {'db_kind_branch'},
     '确认实际 BM2 DatabaseKind 映射，逐一审查目标分支与 default；仅修改有证据的业务分支差异。',
     '静态核对各分支最终 SQL 与 DM8 官方语法；映射未知只影响对应条目，不阻塞其他转换。'),
    ('R02', '动态与配置SQL来源', 'P1', {'direct_client_query', 'dynamic_sql_payload', 'config_query_framework'},
     '关联产生端、执行端、配置定义及实际 SQL；注释、类型声明和普通数据源属性先辨别。',
     '还原最终 SQL 模板并核对语法、别名和参数位置；只对源码未包含的模板索取 SQL 文本。'),
    ('R03', '序列与并发锁', 'P1', {'sequence_identity', 'lock_for_update'},
     '检查序列引用与 FOR UPDATE 表达式，保持现有编号、条件和锁语义；不承担序列对象或状态迁移。',
     '按官方语法核对对象引用、返回格式和锁子句，保持业务控制流；特殊映射作为单项条件记录。'),
    ('R04', '系统目录与元数据', 'P1', {'catalog_metadata', 'db2_dummy_catalog', 'schema_metadata_api'},
     '核对目录查询、模式过滤、类型名称和长度含义，检查元数据消费者的分支。',
     '核对目标目录及返回列契约；仅在具体类型映射无法判定时记录所需字段信息，不索取全库 DDL。'),
    ('R05', '函数分页与查询语义', 'P2', {'date_formatting', 'timestamp_arithmetic', 'decode_function', 'row_number_paging', 'oracle_outer_join', 'group_hierarchy_window', 'date_time_extra'},
     '逐条确认日期、条件、连接、层次/窗口及分页语义；这些特征本身不等于不兼容。',
     '按官方函数签名核对参数顺序、单位、NULL、排序与边界；保留查询条件、别名、返回列及业务口径。'),
    ('R06', '其他数据库方言分支', 'P2', {'db2_isolation', 'db2_fetch_first', 'current_time_special', 'db_object_program', 'stored_program_call'},
     '审查语句所在分支与目标 SQL；仅适配应用中的程序调用，不承担库内对象创建与迁移。',
     '核对达梦原生签名和语法；需要兼容模式或调用签名的信息只登记到对应条目。'),
    ('R07', '类型长度与空值', 'P2', {'null_functions', 'null_blank_semantics', 'string_functions', 'numeric_conversion', 'concat_operator'},
     '区分宿主语言运算与 SQL，检查显式/隐式类型转换、UTF-8 长度、NULL 与空串；不做数据清洗或字段迁移。',
     '静态核对表达式类型和函数行为；只有决定某条改写所必需的字段类型/模式信息才单独标注。'),
    ('R08', '业务事务与错误处理', 'P2', {'transaction_api', 'db_transaction_and_errors', 'db_error_branch'},
     '沿用已适配 BM2，保留事务控制流；仅处理数据库错误分类或语法导致的应用差异，不顺带修复历史业务问题。',
     '检查改动是否保持原有错误分支与提交/回滚边界；代码错误分类需平台合同的，仅单项待确认。'),
    ('R09', '常规访问与SQL构造', 'P3', {'database_api', 'sql_keywords', 'dml_ddl', 'query_execution', 'model_crud', 'sql_bind_marker', 'sql_generation', 'sql_building_extended', 'merge_upsert', 'ordering_limit'},
     '识别实际 SQL/模型调用及业务使用情况，沿用已适配框架，记录保留或修改依据。',
     '静态检查 SELECT/INSERT/UPDATE/DELETE 的条件、列映射、排序、别名和参数；记录保留或转换依据及未运行状态。'),
    ('R10', '部署或辅助材料', 'P3', {'database_provider_reference', 'query_service_names'},
     '仅作为 SQL 来源与调用路径辅助证据；环境配置不输出值，不要求搭建运行环境。',
     '静态关联调用方和执行端；存在不同源码版本时标注差异及待确认身份，不据此暂停其他 SQL 转换。'),
]


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write_csv(name, columns, rows):
    with (OUT / name).open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            # Avoid treating a path/value as an Excel formula when a CSV is opened.
            writer.writerow({k: ("'" + str(v) if str(v).startswith(('=', '+', '-', '@')) else v) for k, v in row.items()})


def module(path):
    parts = Path(path).parts
    return '/'.join(parts[:2]) if len(parts) > 1 else 'workspace'


def main():
    OUT.mkdir(exist_ok=True)
    inventory = read_json(SCAN / 'inventory.json')
    archives = read_json(SCAN / 'archives.json')
    cpp = {f['path']: f['features'] for f in read_json(ROOT / 'analysis' / 'database-surface.json')['files']}
    # Refresh snapshot integrity, not the expensive full-text scan.
    files = {f['path']: f for f in inventory['files']}
    changed = [p for p, f in files.items() if not (ROOT / p).is_file() or hashlib.sha256((ROOT / p).read_bytes()).hexdigest() != f['sha256']]
    current = set()
    for folder, dirs, names in os.walk(ROOT, followlinks=False):
        dirs[:] = [d for d in dirs if d != '.git' and Path(folder) / d != ROOT / 'analysis' and not (Path(folder) / d).is_symlink()]
        current.update((Path(folder) / n).relative_to(ROOT).as_posix() for n in names)
    if changed or current != set(files):
        raise RuntimeError(f'Snapshot changed; refresh scan before classification. Changed={changed}; added={sorted(current-set(files))}; missing={sorted(set(files)-current)}')

    reviews = []
    for name in ('branch-reviews.json', 'dynamic-reviews.json'):
        data = read_json(OUT / name)
        reviews.extend(data['items'] if name == 'branch-reviews.json' else data['reviews'])
    review_by_file = defaultdict(list)
    evidence_count = 0
    for review in reviews:
        for e in review['evidence']:
            assert e['path'] in files, e
            assert 1 <= e['line'] <= files[e['path']]['line_count'], e
            review_by_file[e['path']].append(review['id'])
            evidence_count += 1
    assert len({r['id'] for r in reviews}) == len(reviews)

    candidates, coverage, archive_rows = [], [], []
    for path, f in sorted(files.items()):
        features = f.get('features', {})
        coverage.append({'path': path, 'module': module(path), 'category': f['category'], 'scan_status': f['status'], 'has_candidates': bool(features), 'sha256': f['sha256']})
        if not features:
            continue
        groups = [r for r in RULES if r[3].intersection(features)]
        priority = min((r[2] for r in groups), default='P4') if f['category'] in CODE else 'P3'
        first = min(min(lines) for lines in features.values())
        candidates.append({
            'id': 'FILE-' + hashlib.sha256(path.encode()).hexdigest()[:12], 'review_order': priority,
            'module': module(path), 'category': f['category'], 'path': path, 'first_candidate_line': first,
            'review_state': '部分位置已静态审查，整文件待审查' if path in review_by_file else '候选待人工审查',
            'deployment_state': '未验证部署身份，不作为全局转换前置',
            'current_task': '应用SQL适配DM8；不含建库、迁数、部署和全项目联调',
            'sql_conversion_state': '待逐句审查；静态审查记录不等于已完成转换',
            'work_groups': ';'.join(r[0] for r in groups) or '待分流',
            'review_ids': ';'.join(sorted(set(review_by_file[path]))),
            'recommendation': ' '.join(r[0] + ':' + r[4] for r in groups) or '辨别宽规则误报，保留分流结论。',
            'validation': ' '.join(r[0] + ':' + r[5] for r in groups) or '依据实际运行或配置证明用途。',
            'feature_lines': json.dumps(features, ensure_ascii=False, separators=(',', ':')),
            'cpp_comment_mask_reference': json.dumps(cpp.get(path, {}), ensure_ascii=False, separators=(',', ':')),
            'sha256': f['sha256'],
        })
    hashes = defaultdict(list)
    for f in files.values():
        hashes[f['sha256']].append(f['path'])
    for m in archives['members']:
        if not m.get('features'):
            continue
        archive_rows.append({'archive': m['archive'], 'member': m['member'], 'status': '压缩包候选，发布身份待确认', 'byte_identical_workspace_paths': ';'.join(hashes[m['sha256']]), 'feature_lines': json.dumps(m['features'], separators=(',', ':')), 'sha256': m['sha256'], 'recommendation': '确认参与发布与否；按内容关联当前源码，旧副本不自动删除或混算。'})
    write_csv('file-checklist.csv', list(candidates[0]), candidates)
    write_csv('coverage-ledger.csv', list(coverage[0]), coverage)
    write_csv('archive-checklist.csv', list(archive_rows[0]), archive_rows)
    rule_rows = [{'id': r[0], 'title': r[1], 'code_review_order': r[2], 'features': ';'.join(sorted(r[3])), 'recommendation': r[4], 'validation': r[5]} for r in RULES]
    write_csv('review-rules.csv', list(rule_rows[0]), rule_rows)
    document = (ROOT / 'analysis' / 'document-review' / 'doc2' / 'content.txt').read_text(encoding='utf-8').splitlines()
    business_text = next(l for l in document if l.startswith('[P151]'))
    interface_text = next(l for l in document if l.startswith('[P158]'))
    businesses = business_text.split('包含', 1)[1].rstrip('。').split('、')
    interfaces = interface_text.split('需要做与', 1)[1].split('的外部数据接口测试', 1)[0].split('、')
    assert len(businesses) == 8 and len(interfaces) == 21
    navigation = ['QMTS/QM00/Client质量工程', 'PSSM/APBD/PS00', 'MMSM/MM00/CAAI/WM10', 'WMSM/WM00/WM10', 'SMSM/SM00/WMSM', 'TMSM/MMSM', 'MMSM/Client料仓工程，FBSM依赖待核', 'MMSM/FOSMT']
    business_rows = [{'id': f'BUS-{i+1:02}', 'document_business': name, 'source': '第二份方案4.5.1/P151', 'code_navigation_candidate': navigation[i], 'mapping_status': '按已有源码调查提供导航，非完整或已确认的业务边界', 'page_service_object_mapping': '', 'validation_state': '待展开业务用例，尚未验证'} for i, name in enumerate(businesses)]
    interface_rows = [{'id': f'EXT-{i+1:02}', 'counterparty': name, 'source': '第二份方案4.5.1/P158', 'interface_id': '', 'direction': '', 'protocol': '', 'service_or_telegram': '', 'table_or_program_job': '', 'retry_ack_rules': '', 'owner': '', 'definition_state': '待RQ-08；一个对接方可展开多条接口', 'validation_state': '未联调'} for i, name in enumerate(interfaces)]
    write_csv('business-coverage.csv', list(business_rows[0]), business_rows)
    write_csv('interface-register.csv', list(interface_rows[0]), interface_rows)
    (OUT / 'reviewed-items.json').write_text(json.dumps(reviews, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    counts = Counter(r['module'] for r in candidates)
    reviewed_counts = Counter(r['status'] for r in reviews)
    summary = {'generated_at_utc': datetime.now(timezone.utc).isoformat(), 'workspace_files': len(coverage), 'candidate_files': len(candidates), 'candidate_archive_members': len(archive_rows), 'no_rule_hit_files': sum(not f.get('features') for f in files.values()), 'review_order_counts': dict(Counter(r['review_order'] for r in candidates)), 'candidate_files_by_module': dict(sorted(counts.items())), 'reviewed_items': len(reviews), 'review_statuses': dict(reviewed_counts), 'review_evidence_locations': evidence_count, 'source_files_changed_since_scan': changed, 'validation_scope': 'Snapshot hashes, file coverage, review ID uniqueness and evidence line bounds; not DM8 runtime compatibility.'}
    (OUT / 'checklist-summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    lines = ['# 首批人工审查项', '', '范围更新：当前只负责应用/后台 SQL 转换。下面保留初次源码审查事实；其中建库、迁数、部署和整体运行资料不再是当前工作前置。最新判断见 SQL转换判断.md 与 sql-branch-decisions.json、sql-dynamic-decisions.json。', '', '这些条目已根据源码静态核实，但尚未在 Oracle/DM8 对照环境执行。P1/P2/P3 表示审查优先级；不等于确定不兼容。', '']
    for r in reviews:
        lines += [f"## {r['id']} · {r['title']}", '', f"优先级：{r['priority']}。状态：{r['status']}。模块：{r['module']}。", '', '**证据：**', '']
        lines += [f"- [{e['path']}:{e['line']}](<{(ROOT / e['path']).as_posix()}:{e['line']}>)：{e['role']}" for e in r['evidence']]
        lines += ['', '**发现：** ' + r['finding'], '', '**处理建议：** ' + r['recommendation'], '', '**验证：** ' + r['validation'], '', '**依赖资料：** ' + '；'.join(r['dependencies']), '']
    (OUT / '首批人工审查项.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
