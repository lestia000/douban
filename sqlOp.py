import pymysql


def create_con(hostname, username, password, database):
    return pymysql.connect(
        host=hostname,
        user=username,
        password=password,
        database=database
    )


def table_exist(cursor, table_name):
    select_table_exist = 'SHOW TABLES LIKE %s'
    is_exist = cursor.execute(select_table_exist, table_name)
    return is_exist


def insert_data(conn, cursor, table_name, column, data, close=False):
    is_exist = table_exist(cursor, table_name)
    if not is_exist:
        init = 'CREATE TABLE `{}`('
        [names, types] = column[0], column[1]
        for ind in range(len(names)):
            init = init + f'{names[ind]} {types[ind]}'
            if ind != len(names) - 1:
                init = init + ','
        final_sql = init + ')'
        create_table_sql = final_sql.format(table_name)
        print(f"创建{table_name}表格成功")
        cursor.execute(create_table_sql)
    get_tables = '('
    table_value = '('
    for ind in range(len(column[0])):
        if "AUTO_INCREMENT" not in column[1][ind]:
            if ind == len(column[0]) - 1:
                get_tables = get_tables + f'{column[0][ind]}'
                table_value = table_value + '%s'
            else:
                get_tables = get_tables + f'{column[0][ind]},'
                table_value = table_value + '%s,'
    get_tables_name = get_tables + ")"
    table_value_name = table_value + ")"
    insert_sql = f'INSERT INTO `{table_name}` {get_tables_name} VALUES{table_value_name}'
    cursor.executemany(insert_sql, data)
    print("插入数据成功")
    if close:
        close_con(conn, cursor)


def select_data(cursor, table_name, columns):
    select_obj_name = ""
    if isinstance(columns, str):
        select_obj_name = select_obj_name + columns
    else:
        for column in columns:
            select_obj_name = select_obj_name + column + ","
        select_obj_name = select_obj_name[:-1]
    try:
        select_sql = f'SELECT {select_obj_name} FROM {table_name}'
        cursor.execute(select_sql)
        results = cursor.fetchall()
        return results
    except Exception as e:
        print("查询失败:" + str(e))


def close_con(conn, cursor):
    conn.close()
    cursor.close()
    print("关闭数据库连接成功")
