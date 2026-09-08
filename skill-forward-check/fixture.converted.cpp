// Isolated source sample for skill evaluation. BM2 API declarations are external.
// DATE_TIME input contract: YYYYMMDD; output: the previous calendar date.
void query_previous_date(CDbCommand& cmd)
{
    // DM8 adaptation [FWD-SQL-001]: YYYYMMDD input; previous calendar date.
    // Integer day subtraction and DUAL preserve the one-row PREV_DATE result.
    // Original SQL (preserved, not executed):
    // CString sqlstr =
        // "SELECT TO_CHAR(TO_DATE(@DATE_TIME,'YYYYMMDD') - 1 DAY, 'YYYYMMDD') AS PREV_DATE "
        // "FROM SYSIBM.SYSDUMMY1";
    // DM8 SQL:
    CString sqlstr =
        "SELECT TO_CHAR(TO_DATE(@DATE_TIME,'YYYYMMDD') - 1, 'YYYYMMDD') AS PREV_DATE "
        "FROM DUAL";
    cmd.SetCommandText(sqlstr);
    cmd.ExecuteReader();
    cmd.Close();
}

void clean_empty_plans(CDbCommand& cmd)
{
    CString sqlstr =
        "DELETE FROM T_PLAN WHERE FACTORY_DIV = @FACTORY_DIV "
        "AND TRIM(PLAN_NO) IS NULL";
    cmd.SetCommandText(sqlstr);
    cmd.ExecuteNonQuery();
}
