// Isolated source sample for skill evaluation. BM2 API declarations are external.
// DATE_TIME input contract: YYYYMMDD; output: the previous calendar date.
void query_previous_date(CDbCommand& cmd)
{
    CString sqlstr =
        "SELECT TO_CHAR(TO_DATE(@DATE_TIME,'YYYYMMDD') - 1 DAY, 'YYYYMMDD') AS PREV_DATE "
        "FROM SYSIBM.SYSDUMMY1";
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
