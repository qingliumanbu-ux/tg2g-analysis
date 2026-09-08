# DM8 转换规则与支持白名单(实证版)

来源:2026-09-06 全 21 模块(17,586 条语句/10,766 去重模板)转换与自查实证;每条规则附官方依据。改写一律"完整原 SQL 注释保留 → 唯一活动 DM8 SQL"。

## 一、改写规则 T1—T15

| 规则 | 原写法 | DM8 写法 | 依据 |
|---|---|---|---|
| T1 | `SYSIBM.SYSDUMMY1` / `SYSIBM.DUAL` / `sysibm.sysdummy1` | `DUAL` | DM 官方支持 DUAL 辅助表;CHANGE-01/02 先例 |
| T2 | `± N DAY(S)` | `± N` | DM 日期运算:日期与整数加减以天为单位(sql-dev/practice-date) |
| T2b | 表达式级天数标注,如 `DAYOFWEEK(x) DAYS` | 去掉 ` DAYS` 后缀 | 同上 |
| T3 | `DAYS(A) - DAYS(B)` | `DATEDIFF(DAY, B, A)` | IBM DAYS 定义 + DM DATEDIFF(函数手册 8.3);CHANGE-01 同型 |
| T4 | `DECODE(x, NULL, a, b)` | `CASE WHEN x IS NULL THEN a ELSE b END` | 标准 SQL;DM DECODE 的 NULL 匹配语义无官方记载,不依赖 |
| T5 | 二元标量 `MAX(a,b)` | `CASE WHEN a IS NULL OR b IS NULL THEN NULL ELSE GREATEST(a,b) END` | IBM 标量 MAX"任一参数 NULL 则结果 NULL"(z/OS sf-max);DM GREATEST 官方未记载 NULL 行为,仅在双非空分支调用 |
| T6 | ROWNUM 作列别名/`ORDER BY ROWNUM` | 别名改 `RN` | DM ROWNUM 为伪列关键字(查询语句 4.15) |
| T7 | `CREATE SEQUENCE … AS INT … NO CACHE …` | 去掉 `AS INT`;`NOCACHE`;只留官方子句 | DM CREATE SEQUENCE 官方语法(无 AS 类型;内部 BIGINT 精度,取值域由 MIN/MAX 约束) |
| T8 | `values nextval for X` / `SELECT nextval for X FROM t` | `select X.nextval from dual` / `X.NEXTVAL` | DM 序列伪列+FROM DUAL(数据定义语句) |
| T9 | `value(a,b)`(DB2) | `nvl(a,b)` | DM 空值函数表无 VALUE;NVL 两参数"返回第一个非空值" |
| T10 | `SUBSTR2(x,m,n)` | `SUBSTR(x,m,n)`;m=0 时显式改 1 | DM 无 SUBSTR2;SUBSTR 按字符;Oracle 将位置 0 视作 1 |
| T11 | `INTERVAL 'n' HOUR` | `n.0/24` | DM 日期运算官方示例用小数天(1/24=1 小时);文档无 INTERVAL 字面量 |
| T12 | `DECODE(x,'',a,b)` | `CASE WHEN x IS NULL OR x='' THEN a ELSE b END` | 空串/NULL 匹配语义随 DM 配置变化,标准 CASE 任何配置下确定 |
| T13 | `± N HOUR/MINUTE/SECOND` | `± n.0/24、n.0/1440、n.0/86400` | 同 T11 |
| T14 | `current date/time/timestamp/schema`(DB2 寄存器) | `CURRENT_DATE/CURRENT_TIME/CURRENT_TIMESTAMP/CURRENT_SCHEMA` | DM 官方函数手册 |
| T15 | `POSSTR(src, sub)`(DB2) | `INSTR(src, sub)` | POSSTR 不在 DM 函数手册;INSTR 为官方字符串函数,参数序与"未找到返回 0"一致 |

## 二、确认 DM8 支持并保留的写法(白名单,均有官方出处)

- NVL、无 NULL/空串搜索值的 DECODE(函数手册表 8.4/8.6)
- ROWNUM 伪列(查询语句 4.15;注意 `JOIN ON` 中不允许 ROWNUM)
- MINUS / EXCEPT / INTERSECT(查询语句:`<集合运算符>::=UNION|EXCEPT|MINUS|INTERSECT`;大字段限制见该节)
- CONNECT BY / START WITH / PRIOR 层次查询(sql-dev/advanced-hierarchical-query 专章)
- LISTAGG(…)[DISTINCT] WITHIN GROUP(…)(查询语句;官方明示支持 DISTINCT;超 32767 字节用 ON OVERFLOW 或 LISTAGG2)
- PIVOT / UNPIVOT 子句(查询语句 4.11;大字段参与需 ENABLE_BLOB_CMP_FLAG,否则报 -2038)
- LENGTH / LENGTHB / LENGTHC / LENGTH2 / LENGTH4 长度函数族(函数手册)
- REGEXP_LIKE / REGEXP_SUBSTR / REGEXP_COUNT / REGEXP_INSTR / REGEXP_REPLACE(函数手册,支持 `\数字` 反向引用)
- SYS_GUID()(官方社区确认,返回 BINARY(16);另有 GUID()/NEWID())
- FETCH FIRST n ROWS ONLY / OFFSET(查询语句 `<ROW_LIMIT子句>`;另有 LIMIT/TOP)
- seq.NEXTVAL/CURRVAL + FROM DUAL(数据定义语句:序列)
- SYSDATE 与小数天运算(sysdate-5.0/24=减 5 小时)、两 date 相减得天数×24=小时(sql-dev/practice-date)
- `FOR UPDATE`(含分页组合);Oracle `(+)` 外连接(官方 FAQ"语法大致相同,大部分不需要修改";建议 E2 验证,失败回退 ANSI JOIN)
- CAST(x AS INTEGER/DECIMAL…)、ROUND、SUBSTR、TO_CHAR、LPAD、`||` 连接、LEFT JOIN、UNION ALL

## 二b、项目业务规则(HR-001 确认)

**全库时间字段统一以 `YYYYMMDDHH24MISS`(14 位紧凑)格式存储。**

- 源码中 `.ToString()` 输出的时间字符串即为该格式(如 `20240904143000`)
- DM8 解析 14 位紧凑字符串时,`CAST(… AS TIMESTAMP)` 可能失败(默认期望带分隔符格式)
- **必须使用 `TO_TIMESTAMP(…, 'YYYYMMDDHH24MISS')` 显式指定格式**
- 遇到不同格式的时间字符串属于特殊情况,需要单独确认并特殊处理
- 此规则已通过 HR-001 确认(2026-09-06)

## 三、待人工口径/语义类(不自动改写)

- 两参数 `TIMESTAMPDIFF(码, expr)`:码 16=天/8=时/4=分/2=秒;"实际完整时长/单位边界数/DB2 月年估算"三选一是业务口径,按服务分别提请(HR-002/004/005/006),不跨服务套用。DM8 无两参数形式;相关块内其他方言可先行转换,整块挂起。
- `DIGITS(n)`(DB2):DM 无此函数;按类型全长零填充取数字串,语义需与口径一同确认(HR-005 范围)。
- `DECODE` 依赖 NULL/空串相等匹配、`TRIM(x) IS NULL` 删除条件等空串语义:按 HR-003/登记项处理,不扩大 UPDATE/DELETE 命中集合。
- 时间文本格式(如 `CAST('<文本>' AS TIMESTAMP)` 的解析格式):按 HR-001 处理。

## 四、检测与验证要点(实证教训)

1. 块识别按内容:任何赋值,字符串以 SQL 关键词开头即入块;变量名白名单(sql*/strSql*)会漏掉 `c_sql_condition`、`vtable`、`sql_insert` 等命名。
2. 盲区形态清单:`sprintf(sql,…)` 格式化、`CDbCommand name("SQL", conn)` 构造式、`+=` 纯片段追加、`#define` 宏、块注释内的历史代码(非活动)、日志字符串误报(需含 FROM/WHERE 等结构词才算 SQL)。
3. 扫描器方言模式必须与改写规则同步更新;扫描失败必须显式报错,不得静默沿用旧结果。
4. 每文件三断言:注释逐行还原、规则幂等、活动残留复扫(排除保留原句与挂起语句)。编码自适应(utf-8/gb18030)写回,换行保持。
5. CHANGE 编号跨模块全局唯一,收尾断言无重复。
6. 支持/保留判定逐个查官方文档后记录出处;第三方博客仅作旁证,不作唯一依据。
