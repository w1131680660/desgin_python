import datetime
import pymysql
import json
import os

# 连接数据库
def connect_mysql_operate(sql_text, dbs='operation', type='dict'):
    # conn = pymysql.Connect(host='106.52.43.196', port=3306, user='beyoungsql', passwd='Hp19921026.', db=dbs)
    # conn = pymysql.Connect(host='172.16.0.6', port=3306, user='beyoungsql', passwd='By1590123!@', db=dbs)
    conn = pymysql.Connect(host='gz-cdb-lwqgjirt.sql.tencentcdb.com', port=59656, user='beyoungsql', passwd='Bymy2021_', db=dbs)
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


def connect_mysql_master(sql_text, dbs='order', type='tuple'):
    conn = pymysql.Connect(host='106.53.250.215', port=3306, user='beyoungsql', passwd='Bymy2021.', db=dbs)

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


def connect_mysql_logistics(sql_text, dbs='product_supplier', type='dict'):
    # gz-cdb-lwqgjirt.sql.tencentcdb.com
    # conn = pymysql.Connect(host='172.16.0.6', port=3306, user='beyoungsql', passwd='By1590123!@', db=dbs)
    conn = pymysql.Connect(host='gz-cdb-lwqgjirt.sql.tencentcdb.com', port=59656, user='beyoungsql', passwd='Bymy2021_', db=dbs)
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


def store_country_code(store,country,language,type=''):
    if language == "en":
        if type == "low":
            if store == "胤佑":
                store = "yy"
            elif store == "爱瑙":
                store = "an"
            elif store == "中睿":
                store = "zr"
            elif store == "京汇":
                store = "jh"
            if country == "美国":
                country = "us"
            elif country == "英国":
                country = "uk"
            elif country == "加拿大":
                country = "ca"
            elif country == "日本":
                country = "jp"
            elif country == "欧洲":
                country = "eu"
            elif country == "澳洲":
                country = "au"
            elif country == "法国":
                country = "fr"
            elif country == "德国":
                country = "de"
            elif country == "意大利":
                country = "it"
            elif country == "西班牙":
                country = "es"
            elif country == "墨西哥":
                country = "mx"
            elif country == "西班牙":
                country = "ie"
            elif country == "葡萄牙":
                country = "pt"
            elif country == "瑞典":
                country = "se"
        else:
            if store == "胤佑":
                store = "YY"
            elif store == "爱瑙":
                store = "AN"
            elif store == "中睿":
                store = "ZR"
            elif store == "京汇":
                store = "JH"
            if country == "美国":
                country = "US"
            elif country == "英国":
                country = "UK"
            elif country == "加拿大":
                country = "CA"
            elif country == "日本":
                country = "JP"
            elif country == "欧洲":
                country = "EU"
            elif country == "澳洲":
                country = "AU"
            elif country == "法国":
                country = "FR"
            elif country == "德国":
                country = "DE"
            elif country == "意大利":
                country = "IT"
            elif country == "西班牙":
                country = "ES"
            elif country == "墨西哥":
                country = "MX"
            elif country == "西班牙":
                country = "IE"
            elif country == "葡萄牙":
                country = "PT"
            elif country == "瑞典":
                country = "SE"
    else:
        if store == "yy" or store == "YY":
            store = "胤佑"
        elif store == "an" or store == "AN":
            store = "爱瑙"
        elif store == "zr" or store == "ZR":
            store = "中睿"
        elif store == "jh" or store == "JH":
            store = "京汇"
        if country == "us" or country == "US":
            country = "美国"
        elif country == "uk" or country == "UK" or country == "GB":
            country = "英国"
        elif country == "ca" or country == "CA":
            country = "加拿大"
        elif country == "jp" or country == "JP":
            country = "日本"
        elif country == "eu" or country == "EU":
            country = "欧洲"
        elif country == "au" or country == "AU":
            country = "澳洲"
        elif country == "fr" or country == "FR":
            country = "法国"
        elif country == "de" or country == "DE":
            country = "德国"
        elif country == "it" or country == "IT":
            country = "意大利"
        elif country == "es" or country == "ES":
            country = "西班牙"
        elif country == "mx" or country == "MX":
            country = "墨西哥"
        elif country == "ie" or country == "IE":
            country = "西班牙"
        elif country == "pt" or country == "PT":
            country = "葡萄牙"
        elif country == "se" or country == "SE":
            country = "瑞典"
    return store,country


# ========================获取超时订单
# 查询欧洲订单数据表
sql1 = "select * from manually_create_order_yc where status='1' limit 0,1000;"

# 查询加拿大订单表
sql3 = "select * from manually_create_order_ups where status='1' limit 0,1000;"
# 查询物流系统仓库信息
sql4 = "select * from oversea_location_data;"
# 查询商品编码表
sql5 = "select * from commodity_codes_zr;"
channel = "Amazon"
# try:



ca_data = connect_mysql_master(sql3, type='dict')

data4 = connect_mysql_logistics(sql4, type='dict')
data5 = connect_mysql_master(sql5, dbs='reports', type='dict')


def conn_func(_dict):
    insert_sql = "insert IGNORE into timeout_orders (dates,  channel, station, country,  Amazon_id,  warehouse, " \
                 " warehouse_name, warehouse_code,logistic_supplier, " \
                 "  tracking_no,sku,product_name,question_type,question_reason,all_days) values " \
                 " ( '{0}' ,'{1}' ,'{2}' ,'{3}','{4}', '{5}','{6}', '{7}' ,'{8}', '{9}' ," \
                 " '{10}' , '{11}' ,'{12}', '{13}', '{14}')"
    if _dict["question_type"] is not None and _dict["question_type"] != '--' and _dict["question_type"] != '':
        # count += 1
        insert_sql = insert_sql.format(_dict["dates"], _dict["channel"], _dict["station"], _dict["country"],
                                       _dict["Amazon_id"], _dict["warehouse"], _dict["warehouse_name"],
                                       _dict["warehouse_code"], _dict["logistic_supplier"],
                                       _dict["tracking_no"], _dict["sku"],
                                       _dict["product_name"], _dict["question_type"], _dict["question_reason"],
                                       _dict["all_days"])
        print("insert_sql===", insert_sql)
        connect_mysql_operate(insert_sql)

def usa_func():
    # 查询美国订单表
    count_sql = " select count(id) as count_data from manually_create_order where status='1' "
    count_data = connect_mysql_master(count_sql,type='dict')[0].get('count_data')
    count_data = int(count_data)
    page = count_data
    print(page)
    sql2 = "select * from manually_create_order where status='1' "
    usa_data = connect_mysql_master(sql2, type='dict')

    data = []

    for data_dict in usa_data:
        store, country = store_country_code(data_dict["station"], data_dict["country_code"], 'zh')
        # print('这是什么',data_dict.keys(), data_dict.get("start_time"))

        _dict = {
            "dates": data_dict["dates"],
            "channel": channel,
            "station": store,
            "country": country,
            "Amazon_id": data_dict["reference_ture"],
            "warehouse": "--",
            "warehouse_name": '--',
            "warehouse_code": data_dict["warehouse_code"],
            "logistic_supplier": "--",
            "tracking_no": data_dict["tracking_no"],
            "sku": "--",
            "product_name": "--",
            "question_type": "--",
            "all_days": "--",
            "question_reason": "--"
        }
        product_name = ''

        if data_dict.get('country_code') =='US':
            _dict["logistic_supplier"] = "FedEx"
        _dict["sku"] = data_dict.get("sku")
        for item in data5:
            if item["sku"] in data_dict["sku"]:
                _dict["product_name"] = item["product_name"]
                product_name = item["product_name"]

        if data_dict["delivery_date"] is None or data_dict["delivery_date"] == '':
            if data_dict["dates"] is not None and data_dict["dates"] != '':
                days = (datetime.datetime.now() - datetime.datetime.strptime(data_dict["dates"], "%Y-%m-%dT%H-%M")).days
                # 大于2天超时
                if days > 2:
                    _dict["question_type"] = "出库超时"
                    _dict["question_reason"] = "海外仓"
                    _dict["all_days"] = '--'
            else:
                _dict["question_type"] = "--"
                _dict["question_reason"] = "--"
                _dict["all_days"] = '--'
        elif data_dict["delivery_date"] is not None and data_dict["delivery_date"] != '':
            if data_dict["dates"] is not None and data_dict["dates"] != '':
                if data_dict["delivery_date"] !='0000-00-00 00:00:00':

                    print( '\n',249,data_dict["delivery_date"] , data_dict["dates"])
                    delivery_date =datetime.datetime.strptime(data_dict["delivery_date"],"%Y-%m-%d %H:%M:%S")
                    dates = datetime.datetime.strptime(data_dict["dates"],"%Y-%m-%dT%H-%M")
                    days = ( delivery_date- dates).days
                    if days > 2:
                        _dict["question_type"] = "出库超时"
                        _dict["question_reason"] = "海外仓"
                        _dict["all_days"] = '--'
            else:
                _dict["question_type"] = "--"
                _dict["question_reason"] = "--"
                _dict["all_days"] = '--'

            # 判断取货是否超时

            if data_dict.get("start_time") is None or data_dict.get("start_time") == '':
                days = (datetime.datetime.now() - datetime.datetime.strptime(data_dict["delivery_date"],
                                                                             "%Y-%m-%d %H:%M:%S")).days
                if days > 2:
                    _dict["question_type"] = "取货超时"
                    _dict["question_reason"] = "物流商"
                    _dict["all_days"] = '--'
            elif data_dict["start_time"] is not None or data_dict["start_time"] != '':

                if len(data_dict["start_time"]) ==16:
                    data_dict["start_time"] = data_dict["start_time"]+':00'
                print('这是270', data_dict["start_time"], data_dict["delivery_date"])
                time_1 =datetime.datetime.strptime(data_dict["start_time"],"%Y-%m-%d %H:%M:%S")
                time_2 =datetime.datetime.strptime(data_dict["delivery_date"], "%Y-%m-%d %H:%M:%S")
                print(time_1,'这是273', time_2)

                days = (time_1- time_2).days
                if days > 2:
                    _dict["question_type"] = "取货超时"
                    _dict["question_reason"] = "物流商"
                    _dict["all_days"] = '--'

                # 判断配送是否超时
                if data_dict["end_time"] is None or data_dict["end_time"] == '':
                    days = (datetime.datetime.now() - datetime.datetime.strptime(data_dict["start_time"],
                                                                                 "%Y-%m-%d %H:%M:%S")).days
                    if days > 15:
                        _dict["question_type"] = "配送超时"
                        _dict["question_reason"] = "物流商"
                        _dict["all_days"] = '--'
                elif data_dict["end_time"] is not None and data_dict["end_time"] != '':
                    if len(data_dict["end_time"]) == 16:
                        data_dict["end_time"] = data_dict["end_time"] + ':00'
                    if len(data_dict["start_time"]) == 16:
                        data_dict["start_time"] = data_dict["start_time"] + ':00'
                    print(data_dict["end_time"] ,data_dict["start_time"])
                    begin_time = datetime.datetime.strptime(data_dict["end_time"], "%Y-%m-%d %H:%M:%S")
                    end_time = datetime.datetime.strptime(data_dict["start_time"], "%Y-%m-%d %H:%M:%S")
                    days = (begin_time - end_time).days
                    # days = (datetime.datetime.strptime(data_dict["end_time"],
                    #                                    "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(
                    #     data_dict["start_time"], "%Y-%m-%d %H:%M:%S")).days
                    days1 = (datetime.datetime.strptime(data_dict["end_time"],
                                                        "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(
                        data_dict["delivery_date"], "%Y-%m-%d %H:%M:%S")).days
                    if days > 15:
                        _dict["question_type"] = "配送超时"
                        _dict["question_reason"] = "物流商"
                        _dict["all_days"] = days1
        # print(_dict)
        conn_func(_dict)

def ca_func():
    # 查询美国订单表
    count_sql = " select count(id) as count_data from manually_create_order where status='1' "
    sql3 = "select * from manually_create_order_ups where status='1';"
    # # count_data = connect_mysql_master(count_sql, type='dict')[0].get('count_data')
    # # count_data = int(count_data)
    # page = count_data
    # print(page)
    sql2 = "select * from manually_create_order_ups where status='1';"
    ca_data = connect_mysql_master(sql2, type='dict')

    data = []

    for data_dict in ca_data:
        store, country = store_country_code(data_dict["station"], data_dict["country_code"], 'zh')
        # print('这是什么',data_dict.keys(), data_dict.get("start_time"))

        _dict = {
            "dates": data_dict["dates"],
            "channel": channel,
            "station": store,
            "country": country,
            "Amazon_id": data_dict["reference_ture"],
            "warehouse": "--",
            "warehouse_name": '--',
            "warehouse_code": data_dict["warehouse_code"],
            "logistic_supplier": "--",
            "tracking_no": data_dict["tracking_no"],
            "sku": "--",
            "product_name": "--",
            "question_type": "--",
            "all_days": "--",
            "question_reason": "--"
        }
        product_name = ''

        if data_dict.get('country_code') == 'US':
            _dict["logistic_supplier"] = "FedEx"
        _dict["sku"] = data_dict.get("sku")
        for item in data5:
            if item["sku"] in data_dict["sku"]:
                _dict["product_name"] = item["product_name"]
                product_name = item["product_name"]

        if data_dict["delivery_date"] is None or data_dict["delivery_date"] == '':
            if data_dict["dates"] is not None and data_dict["dates"] != '':
                days = (datetime.datetime.now() - datetime.datetime.strptime(data_dict["dates"], "%Y-%m-%dT%H-%M")).days
                # 大于2天超时
                if days > 2:
                    _dict["question_type"] = "出库超时"
                    _dict["question_reason"] = "海外仓"
                    _dict["all_days"] = '--'
            else:
                _dict["question_type"] = "--"
                _dict["question_reason"] = "--"
                _dict["all_days"] = '--'
        elif data_dict["delivery_date"] is not None and data_dict["delivery_date"] != '':
            if data_dict["dates"] is not None and data_dict["dates"] != '':
                if data_dict["delivery_date"] != '0000-00-00 00:00:00':

                    print('\n', 249, data_dict["delivery_date"], data_dict["dates"])
                    delivery_date = datetime.datetime.strptime(data_dict["delivery_date"], "%Y-%m-%d %H:%M:%S")
                    dates = datetime.datetime.strptime(data_dict["dates"], "%Y-%m-%dT%H-%M")
                    days = (delivery_date - dates).days
                    if days > 2:
                        _dict["question_type"] = "出库超时"
                        _dict["question_reason"] = "海外仓"
                        _dict["all_days"] = '--'
            else:
                _dict["question_type"] = "--"
                _dict["question_reason"] = "--"
                _dict["all_days"] = '--'

            # 判断取货是否超时

            if data_dict.get("start_time") is None or data_dict.get("start_time") == '':
                days = (datetime.datetime.now() - datetime.datetime.strptime(data_dict["delivery_date"],
                                                                             "%Y-%m-%d %H:%M:%S")).days
                if days > 2:
                    _dict["question_type"] = "取货超时"
                    _dict["question_reason"] = "物流商"
                    _dict["all_days"] = '--'
            elif data_dict["start_time"] is not None or data_dict["start_time"] != '':

                if len(data_dict["start_time"]) == 16:
                    data_dict["start_time"] = data_dict["start_time"] + ':00'
                print('这是270', data_dict["start_time"], data_dict["delivery_date"])
                time_1 = datetime.datetime.strptime(data_dict["start_time"], "%Y-%m-%d %H:%M:%S")
                time_2 = datetime.datetime.strptime(data_dict["delivery_date"], "%Y-%m-%d %H:%M:%S")
                print(time_1, '这是273', time_2)

                days = (time_1 - time_2).days
                if days > 2:
                    _dict["question_type"] = "取货超时"
                    _dict["question_reason"] = "物流商"
                    _dict["all_days"] = '--'

                # 判断配送是否超时
                if data_dict["end_time"] is None or data_dict["end_time"] == '':
                    days = (datetime.datetime.now() - datetime.datetime.strptime(data_dict["start_time"],
                                                                                 "%Y-%m-%d %H:%M:%S")).days
                    if days > 15:
                        _dict["question_type"] = "配送超时"
                        _dict["question_reason"] = "物流商"
                        _dict["all_days"] = '--'
                elif data_dict["end_time"] is not None and data_dict["end_time"] != '':
                    if len(data_dict["end_time"]) == 16:
                        data_dict["end_time"] = data_dict["end_time"] + ':00'
                    if len(data_dict["start_time"]) == 16:
                        data_dict["start_time"] = data_dict["start_time"] + ':00'
                    print(data_dict["end_time"], data_dict["start_time"])
                    begin_time = datetime.datetime.strptime(data_dict["end_time"], "%Y-%m-%d %H:%M:%S")
                    end_time = datetime.datetime.strptime(data_dict["start_time"], "%Y-%m-%d %H:%M:%S")
                    days = (begin_time - end_time).days
                    # days = (datetime.datetime.strptime(data_dict["end_time"],
                    #                                    "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(
                    #     data_dict["start_time"], "%Y-%m-%d %H:%M:%S")).days
                    days1 = (datetime.datetime.strptime(data_dict["end_time"],
                                                        "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(
                        data_dict["delivery_date"], "%Y-%m-%d %H:%M:%S")).days
                    if days > 15:
                        _dict["question_type"] = "配送超时"
                        _dict["question_reason"] = "物流商"
                        _dict["all_days"] = days1
        # print(_dict)
        conn_func(_dict)

def europe_func():
    sql1 = "select * from manually_create_order_yc where status='1';"

    europe_data = connect_mysql_master(sql1, type='dict')
    for index_1,data_dict in enumerate(europe_data):

        # 查询当前订单号在超时订单表中是否存在
        sql6 = "select * from timeout_orders where Amazon_id='%s';"%(data_dict["reference_ture"])
        res = connect_mysql_operate(sql6)
        if len(res) == 0:
            store, country = store_country_code(data_dict["station"], data_dict["country_code"], 'zh')
            _dict = {
                "dates": data_dict["dates"],
                "channel": channel,
                "station": store,
                "country": country,
                "Amazon_id": data_dict["reference_ture"],
                "warehouse":"--",
                "warehouse_name": '--',
                "warehouse_code": data_dict["warehouse_code"],
                "logistic_supplier":"--",
                "tracking_no": data_dict["tracking_no"],
                "sku":"--",
                "product_name":"--",
                "question_type":"--",
                "all_days": "--",
                "question_reason": "--"
            }

            for index,j in enumerate(data4):
                if data_dict["warehouse_code"] == j["code"]:
                    _dict["warehouse_name"] = j["warehouse_name"]
                    _dict["warehouse"] = j["carrier_name"]
                _dict["logistic_supplier"] = data_dict["shipping_method"]
                _dict["sku"] = data_dict["product_sku"]

                for item in data5:
                    if item["sku"] in data_dict["product_sku"]:
                        _dict["product_name"] = item["product_name"]
                # 判断出库是否超时
                if data_dict["delivery_date"] is None and data_dict["delivery_date"] != '':
                    if data_dict["dates"] is not None and data_dict["dates"] != '':
                        days = (datetime.datetime.now() - datetime.datetime.strptime(data_dict["dates"], "%Y-%m-%dT%H-%M")).days
                        if days > 2:
                            _dict["question_type"] = "出库超时"
                            _dict["question_reason"] = "海外仓"
                            _dict["all_days"] = "--"
                    else:
                        _dict["question_type"] = "--"
                        _dict["question_reason"] = "--"
                        _dict["all_days"] = "--"
                elif data_dict["delivery_date"] is not None and data_dict["delivery_date"] != '':
                    if data_dict["dates"] is not None and data_dict["dates"] != '':
                        # 出库超时出库的时间减去订单创建的时间
                        print(data_dict["delivery_date"])
                        del_date =datetime.datetime.strptime(data_dict["delivery_date"], "%Y-%m-%d %H:%M:%S")
                        dates_1 =datetime.datetime.strptime(data_dict["dates"],"%Y-%m-%dT%H-%M")
                        days = (del_date- dates_1).days
                        if days > 2:
                            _dict["question_type"] = "出库超时"
                            _dict["question_reason"] = "海外仓"
                            _dict["all_days"] = "--"
                    else:
                        _dict["question_type"] = "--"
                        _dict["question_reason"] = "--"
                        _dict["all_days"] = "--"

                    # 判断取货是否超时
                    print(index_1, data_dict.keys())
                    print('\n\n这是330',data_dict.get('start_time'))
                    if data_dict.get("start_time") :
                        print('????????????????????????')
                        days = (datetime.datetime.now() - datetime.datetime.strptime(data_dict["delivery_date"],
                                                                                     "%Y-%m-%d %H:%M:%S")).days
                        if days > 2:
                            _dict["question_type"] = "取货超时"
                            _dict["question_reason"] = "物流商"
                            _dict["all_days"] = "--"
                    elif data_dict.get("start_time") is not None and data_dict.get("start_time") != '':
                        days = (datetime.datetime.strptime(data_dict["start_time"],
                                                           "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(
                            data_dict["delivery_date"], "%Y-%m-%d %H:%M:%S")).days
                        if days > 2:
                            _dict["question_type"] = "取货超时"
                            _dict["question_reason"] = "物流商"
                            _dict["all_days"] = "--"

                        # 判断配送是否超时
                        if data_dict["end_times"] is None and data_dict["end_times"] != '':
                            days = (datetime.datetime.now() - datetime.datetime.strptime(data_dict["start_time"],
                                                                                         "%Y-%m-%d %H:%M:%S")).days
                            if days > 15:
                                _dict["question_type"] = "配送超时"
                                _dict["question_reason"] = "物流商"
                                _dict["all_days"] = "--"
                        elif data_dict["end_times"] is not None and data_dict["end_times"] != '':
                            days = (datetime.datetime.strptime(data_dict["end_times"],
                                                               "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(
                                data_dict["start_time"], "%Y-%m-%d %H:%M:%S")).days
                            days1 = (datetime.datetime.strptime(data_dict["end_times"],
                                                                "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(
                                data_dict["delivery_date"], "%Y-%m-%d %H:%M:%S")).days
                            if days > 15:
                                _dict["question_type"] = "配送超时"
                                _dict["question_reason"] = "物流商"
                                _dict["all_days"] = days1
            conn_func(_dict)

usa_func()
ca_func()
europe_func()
