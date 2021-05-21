import pymysql
def connect_mysql(sql_text, dbs='operation', type='tuple'):
    # conn = pymysql.Connect(host='106.52.43.196', port=3306, user='beyoungsql', passwd='Hp19921026.', db=dbs)
    conn = pymysql.Connect(host='172.16.0.6', port=3306, user='beyoungsql', passwd='Bymy2021_', db=dbs)
    if type == 'tuple':
        cursor = conn.cursor()
    else:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql_text)
    response = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return response


'''获取供应链的数据'''
def connect_mysql_sp(sql_text, dbs='supply_chain_test', type='tuple'):
    # conn = pymysql.Connect(host='81.71.16.127',
    #                        port=3306,
    #                        user='beyoungsql',
    #                        passwd='By20201314.',
    #                        db=dbs)
    conn = pymysql.Connect(host='172.16.0.6', port=3306, user='beyoungsql', passwd='Bymy2021_', db=dbs)
    if type == 'tuple':
        cursor = conn.cursor()
        # ((值, 值),)
    else:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # [{字段：值},]
    cursor.execute(sql_text)
    response = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return response
