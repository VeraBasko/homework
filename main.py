def parse_connection_string(connection_string):
    """
    Принимает на вход строку соединения connection_string и возвращает словарь с ее составными частями
    dialect+driver://username:password@host:port/database
    """
    connection_dict = {'dialect': '',
                       'driver': '',
                       'username': '',
                       'password': '',
                       'host': '',
                       'port': '',
                       'database': ''}
    conn_list = connection_string.split('://', 1)
    driver_or_dialect = conn_list[0]
    driver_or_dialect = driver_or_dialect.split('+')
    if len(driver_or_dialect) > 1:
        connection_dict['dialect'] = driver_or_dialect[0]
        connection_dict['driver'] = driver_or_dialect[1]
    else:
        connection_dict['dialect'] = driver_or_dialect[0]
    connection_dict['database'] = conn_list[-1].split('/')[-1]
    conn_list = conn_list[-1].split('/')[:-1]
    if conn_list[0]:
        conn_list = conn_list[-1].split('@')
        if len(conn_list) > 1:
            small_conn = conn_list[1].split(':')
            connection_dict['host'] = small_conn[0]
            if len(small_conn) > 1:
                connection_dict['port'] = small_conn[1]
        small_conn = conn_list[0].split(':')
        if small_conn:
            connection_dict['username'] = small_conn[0]
            connection_dict['password'] = small_conn[1]

    return connection_dict

print(parse_connection_string("m2sql://admin:1234/b4_7"))