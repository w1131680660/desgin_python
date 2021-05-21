import pymysql
import hashlib
import json
import requests
import time


def pymysql_transaction(sql_list: list, dbs: str = 'supply_chain'):

    try:
        for sql in sql_list:
            urls = 'https://www.beyoung.group/script/'
            salt = 'BEYOUNG'
            types = 'tuple'
            system = 'new_system'

            data = {'sql': sql_list, 'dbs': dbs, 'type': types, 'system': system}

            times = time.strftime("%Y-%m-%d %X", time.localtime())
            token_str = sql + dbs + types + system + times + salt
            token = hashlib.md5(token_str.encode(encoding='UTF-8')).hexdigest()
            headers = {'token': token, 'times': times}

            res = requests.post(url=urls, headers=headers, data=data)
            res_object = json.loads(res.text)
            res_data = res_object['code']
            if res_data != 200:
                raise ValueError("sql Error!")

        mark = 1
    except Exception as e:
        urls = 'https://www.beyoung.group/rollback/'
        requests.post(url=urls)
        print("错误原因: ", e)
        mark = 0


    return mark


def connect_mysql(sql, dbs, type='tuple', system='new_system'):
    urls = 'https://www.beyoung.group/script/'
    salt = 'BEYOUNG'

    data = {'sql': sql, 'dbs': dbs, 'type': type, 'system': system}

    times = time.strftime("%Y-%m-%d %X", time.localtime())
    token_str = sql + dbs + type + system + times + salt
    token = hashlib.md5(token_str.encode(encoding='UTF-8')).hexdigest()
    headers = {'token': token, 'times': times}

    res = requests.post(url=urls, headers=headers, data=data)
    print(res)
    res_object = json.loads(res.text)
    res_data = res_object['data']
    return res_data