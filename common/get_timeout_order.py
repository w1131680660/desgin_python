import datetime
import pymysql
import json
import os

# 连接数据库
def connect_mysql(sql_text, dbs='operation', type='tuple'):
    conn = pymysql.Connect(host='106.52.43.196', port=3306, user='beyoungsql', passwd='Hp19921026.', db=dbs)

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


def connect_mysql1(sql_text, dbs='order', type='tuple'):
    conn = pymysql.Connect(host='106.53.250.215', port=3306, user='beyoungsql', passwd='Qwert789.', db=dbs)

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


def connect_mysql2(sql_text, dbs='product_supplier', type='tuple'):
    conn = pymysql.Connect(host='42.194.146.85', port=3306, user='beyoungsql', passwd='By20201314.', db=dbs)

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
sql1 = "select * from manually_create_order_yc where status='1';"
# 查询美国订单表
sql2 = "select * from manually_create_order where status='1';"
# 查询加拿大订单表
sql3 = "select * from manually_create_order_ups where status='1';"
# 查询物流系统仓库信息
sql4 = "select * from oversea_location_data;"
# 查询商品编码表
sql5 = "select * from commodity_codes_zr;"
channel = "Amazon"
try:
    data1 = connect_mysql1(sql1, type='dict')
    data2 = connect_mysql1(sql2, type='dict')
    data3 = connect_mysql1(sql3, type='dict')
    data4 = connect_mysql2(sql4, type='dict')
    data5 = connect_mysql1(sql5, dbs='reports', type='dict')
    data6 = data1 + data2 + data3
    data = []
    for i in data6:
        # 查询当前订单号在超时订单表中是否存在
        sql6 = "select * from timeout_orders where Amazon_id='%s';"%(i["reference_ture"])
        res = connect_mysql(sql6)
        if len(res) == 0:
            store, country = store_country_code(i["station"], i["country_code"], 'zh')
            _dict = {
                "dates": i["dates"],
                "channel": channel,
                "station": store,
                "country": country,
                "Amazon_id": i["reference_ture"],
                "warehouse":"--",
                "warehouse_name": '--',
                "warehouse_code": i["warehouse_code"],
                "logistic_supplier":"--",
                "tracking_no": i["tracking_no"],
                "sku":"--",
                "product_name":"--",
                "question_type":"--",
                "all_days": "--",
                "question_reason": "--"
            }

            for index,j in enumerate(data4):
                if i["warehouse_code"] == j["code"]:
                    _dict["warehouse_name"] = j["warehouse_name"]
                    _dict["warehouse"] = j["carrier_name"]

            if i["country_code"] == "US" or i["country_code"] == "CA":
                if i["country_code"] == "US":
                    _dict["logistic_supplier"] = "FedEx"
                else:
                    _dict["logistic_supplier"] = "UPS"
                _dict["sku"] = i["sku"]

                for item in data5:
                    if item["sku"] in i["sku"]:
                        _dict["product_name"] = item["product_name"]
                # 判断出库是否超时
                if i["delivery_date"] is None and i["delivery_date"] != '':
                    if i["dates"] is not None and i["dates"] != '':
                        days = (datetime.datetime.now() - datetime.datetime.strptime(i["dates"], "%Y-%m-%dT%H-%M")).days
                        if days > 2:
                            _dict["question_type"] = "出库超时"
                            _dict["question_reason"] = "海外仓"
                            _dict["all_days"] = '--'
                    else:
                        _dict["question_type"] = "--"
                        _dict["question_reason"] = "--"
                        _dict["all_days"] = '--'
                elif i["delivery_date"] is not None and i["delivery_date"] != '':
                    if i["dates"] is not None and i["dates"] != '':
                        days = (datetime.datetime.strptime(i["delivery_date"],
                                                           "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(i["dates"],
                                                                                                             "%Y-%m-%dT%H-%M")).days
                        if days > 2:
                            _dict["question_type"] = "出库超时"
                            _dict["question_reason"] = "海外仓"
                            _dict["all_days"] = '--'
                    else:
                        _dict["question_type"] = "--"
                        _dict["question_reason"] = "--"
                        _dict["all_days"] = '--'

                    # 判断取货是否超时
                    if i["start_time"] is None and i["start_time"] != '':
                        days = (datetime.datetime.now() - datetime.datetime.strptime(i["delivery_date"],
                                                                                     "%Y-%m-%d %H:%M:%S")).days
                        if days > 2:
                            _dict["question_type"] = "取货超时"
                            _dict["question_reason"] = "物流商"
                            _dict["all_days"] = '--'
                    elif i["start_time"] is not None and i["start_time"] != '':
                        days = (datetime.datetime.strptime(i["start_time"],
                                                           "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(
                            i["delivery_date"], "%Y-%m-%d %H:%M:%S")).days
                        if days > 2:
                            _dict["question_type"] = "取货超时"
                            _dict["question_reason"] = "物流商"
                            _dict["all_days"] = '--'

                        # 判断配送是否超时
                        if i["end_time"] is None and i["end_time"] != '':
                            days = (datetime.datetime.now() - datetime.datetime.strptime(i["start_time"],
                                                                                         "%Y-%m-%d %H:%M:%S")).days
                            if days > 15:
                                _dict["question_type"] = "配送超时"
                                _dict["question_reason"] = "物流商"
                                _dict["all_days"] = '--'
                        elif i["end_time"] is not None and i["end_time"] != '':
                            days = (datetime.datetime.strptime(i["end_time"],
                                                               "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(
                                i["start_time"], "%Y-%m-%d %H:%M:%S")).days
                            days1 = (datetime.datetime.strptime(i["end_time"],
                                                                "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(
                                i["delivery_date"], "%Y-%m-%d %H:%M:%S")).days
                            if days > 15:
                                _dict["question_type"] = "配送超时"
                                _dict["question_reason"] = "物流商"
                                _dict["all_days"] = days1
            else:
                _dict["logistic_supplier"] = i["shipping_method"]
                _dict["sku"] = i["product_sku"]

                for item in data5:
                    if item["sku"] in i["product_sku"]:
                        _dict["product_name"] = item["product_name"]
                # 判断出库是否超时
                if i["delivery_date"] is None and i["delivery_date"] != '':
                    if i["dates"] is not None and i["dates"] != '':
                        days = (datetime.datetime.now() - datetime.datetime.strptime(i["dates"], "%Y-%m-%dT%H-%M")).days
                        if days > 2:
                            _dict["question_type"] = "出库超时"
                            _dict["question_reason"] = "海外仓"
                            _dict["all_days"] = "--"
                    else:
                        _dict["question_type"] = "--"
                        _dict["question_reason"] = "--"
                        _dict["all_days"] = "--"
                elif i["delivery_date"] is not None and i["delivery_date"] != '':
                    if i["dates"] is not None and i["dates"] != '':
                        days = (datetime.datetime.strptime(i["delivery_date"],
                                                           "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(i["dates"],
                                                                                                             "%Y-%m-%dT%H-%M")).days
                        if days > 2:
                            _dict["question_type"] = "出库超时"
                            _dict["question_reason"] = "海外仓"
                            _dict["all_days"] = "--"
                    else:
                        _dict["question_type"] = "--"
                        _dict["question_reason"] = "--"
                        _dict["all_days"] = "--"

                    # 判断取货是否超时
                    if i["start_times"] is None and i["start_times"] != '':
                        days = (datetime.datetime.now() - datetime.datetime.strptime(i["delivery_date"],
                                                                                     "%Y-%m-%d %H:%M:%S")).days
                        if days > 2:
                            _dict["question_type"] = "取货超时"
                            _dict["question_reason"] = "物流商"
                            _dict["all_days"] = "--"
                    elif i["start_times"] is not None and i["start_times"] != '':
                        days = (datetime.datetime.strptime(i["start_times"],
                                                           "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(
                            i["delivery_date"], "%Y-%m-%d %H:%M:%S")).days
                        if days > 2:
                            _dict["question_type"] = "取货超时"
                            _dict["question_reason"] = "物流商"
                            _dict["all_days"] = "--"

                        # 判断配送是否超时
                        if i["end_times"] is None and i["end_times"] != '':
                            days = (datetime.datetime.now() - datetime.datetime.strptime(i["start_times"],
                                                                                         "%Y-%m-%d %H:%M:%S")).days
                            if days > 15:
                                _dict["question_type"] = "配送超时"
                                _dict["question_reason"] = "物流商"
                                _dict["all_days"] = "--"
                        elif i["end_times"] is not None and i["end_times"] != '':
                            days = (datetime.datetime.strptime(i["end_times"],
                                                               "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(
                                i["start_times"], "%Y-%m-%d %H:%M:%S")).days
                            days1 = (datetime.datetime.strptime(i["end_times"],
                                                                "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(
                                i["delivery_date"], "%Y-%m-%d %H:%M:%S")).days
                            if days > 15:
                                _dict["question_type"] = "配送超时"
                                _dict["question_reason"] = "物流商"
                                _dict["all_days"] = days1

            data.append(_dict)

    # 存入数据库
    insert_sql = "insert into timeout_orders (dates,channel,station,country,Amazon_id,warehouse,warehouse_name," \
                 "warehouse_code,logistic_supplier,tracking_no,sku,product_name,question_type,question_reason,all_days) values "
    count = 0
    for item in data:
        if item["question_type"] is not None and item["question_type"] != '--' and item["question_type"] != '':
            count += 1
            insert_sql += "('" +  item["dates"] + "','" + item["channel"] + "','" + item["station"] + "','" + item["country"] + \
                          "','" + item["Amazon_id"] + "','" + item["warehouse"] + "','" + item["warehouse_name"] + \
                          "','" + item["warehouse_code"] + "','" + item["logistic_supplier"] + "','" + item["tracking_no"] + "','" + item["sku"] + \
                          "','" + item["product_name"] + "','" + item["question_type"] + "','" + item["question_reason"] + \
                          "','" + item["all_days"] + "'),"
    insert_sql = insert_sql[:-1]
    print("insert_sql===",insert_sql)
    if count > 0:
        connect_mysql(insert_sql)
    print("已存入数据库")
except Exception as e:
    print(str(e))
