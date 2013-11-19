CREATE OR REPLACE FUNCTION seq_update(text)
RETURNS void AS
$BODY$
Declare
tab1 varchar;
col1 varchar;
seqname1 varchar;
maxcolval integer;
ssql varchar;
BEGIN
    FOR tab1, col1, seqname1 in Select distinct constraint_column_usage.table_name, 
        constraint_column_usage.column_name,
        replace(replace(columns.column_default,'''::regclass)',''),'nextval(''','')
        From information_schema.constraint_column_usage, information_schema.columns
        where constraint_column_usage.table_schema = $1 AND 
        columns.table_schema = $1 
        AND columns.table_name=constraint_column_usage.table_name
        AND constraint_column_usage.column_name = columns.column_name
        AND columns.column_default is not null 
        AND constraint_column_usage.table_name not in ('user', 'usermodulespages')
        --AND constraint_column_usage.table_name = 'role'
        AND constraint_column_usage.table_name NOT IN ('ip_geo_country', 'ip_geo_local')
        order by 1 
        LOOP
            ssql := 'select COALESCE(max(' || col1 || ') + 1, 1) as max from ' || $1 || '.' || tab1 ;
            RAISE NOTICE 'SQL : %', ssql;
            execute ssql into maxcolval;
            RAISE NOTICE 'max value : %', maxcolval;
            EXECUTE 'alter sequence ' || seqname1 ||' restart with ' || maxcolval;
        END LOOP;
    END;
    $BODY$
    LANGUAGE plpgsql VOLATILE;
