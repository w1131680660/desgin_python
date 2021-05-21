import datetime
import pymysql
import json
import os
import re

# 连接数据库
def connect_mysql(sql_text, dbs='operation', type='tuple'):
    conn = pymysql.Connect(host='gz-cdb-lwqgjirt.sql.tencentcdb.com', port=59656, user='beyoungsql', passwd='Bymy2021_',
                           db=dbs)

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


def connect_mysql_master(sql_text, dbs='order', type='dict'):
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

def connect_mysql2(sql_text, dbs='product_supplier', type='tuple'):
    conn = pymysql.Connect(host='gz-cdb-lwqgjirt.sql.tencentcdb.com', port=59656, user='beyoungsql', passwd='Bymy2021_',
                           db=dbs)
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
        elif country =='AT' or country =='at':
            country ='奥地利'
    return store,country


# 查询物流系统仓库信息
logistics_sql = "select * from oversea_location_data where {0};"
# 查询商品编码表
commodity_sql = "select * from commodity_codes_zr;"
channel = "Amazon"
def europe():
    europe_sql = "select * from manually_create_order_yc where status='1';"
    europe_data = connect_mysql(europe_sql, type='dict')


# 这个函数用来验证是否出库超时
def delivery_func(_dict, delivery_str_date , get_str_dates):
    print(1111,delivery_str_date ,'----',get_str_dates)
    days = (delivery_str_date - get_str_dates).days
    if days > 2:
        _dict["question_type"] = "出库超时"
        _dict["question_reason"] = "海外仓"
        day = delivery_str_date - get_str_dates
        _dict['overtime_time'] = '%s 天 %s 小时'%(day.days,round(float(day.seconds / 3600), 2) )


    return _dict

def start_func(_dict, start_str_time, delivery_str_date ):

    days = (start_str_time - delivery_str_date).days

    if days > 2:
        _dict["question_type"] = "取货超时"
        _dict["question_reason"] = "物流商"
        day = start_str_time - delivery_str_date
        _dict['overtime_time'] = '%s 天 %s 小时' % (day.days, round(float(day.seconds / 3600), 2))

    return _dict
# 这个函数用来验证配送超时
def change_func(_dict , end_str_time , latest_str_ship_date):

    ya_days = end_str_time - latest_str_ship_date
    daY = ya_days.days
    print('\n208行',ya_days ,'-',end_str_time ,latest_str_ship_date)
    if daY > 0:
        _dict["question_type"] = "配送超时"
        _dict["question_reason"] = "物流商"
        _dict['overtime_time'] = '%s 天 %s 小时'%(ya_days.days,round(ya_days.seconds / 3600, 2))
        _dict['status_name'] ='未处理'

    return _dict


def conn_sql_fun(_dict):
    insert_key = ''
    insert_value = ''
    for key, value in _dict.items():
        insert_key += " {0} , ".format(key)
        insert_value += ' "{0}" , '.format(value)
    insert_key = insert_key.rstrip(' , ')
    insert_value = insert_value.rstrip(' , ')
    if _dict.get("question_type") in ["配送超时", "取货超时", "出库超时"]:
        insert_sql = " insert  ignore into timeout_orders ({0}) values ({1})".format(insert_key, insert_value)
        print(insert_sql)
        connect_mysql(insert_sql)

def time_out_judge(_dict, latest_ship_date , end_time ,end_str_time, latest_str_ship_date ,get_str_dates):
    if latest_ship_date and not end_time:
        _days = (latest_str_ship_date - get_str_dates)

        _dict["expected_days"] = '%s 天 %s 小时' % (_days.days, round(float(_days.seconds / 3600), 2)  )  # 这是预计配送花费时间
    elif end_str_time and latest_str_ship_date:
        print(1111111111111111,end_str_time, get_str_dates)
        _days = (end_str_time - get_str_dates)
        over_time  = (end_str_time -latest_str_ship_date).days
        _dict["all_days"] = '%s 天 %s 小时' % (_days.days, round(float(_days.seconds / 3600 ), 2) )# 着实际送达花费时间
        _dict['overtime_time'] = over_time # 超时时间

    return _dict

def time_change(_dict,delivery_date,dates ,start_time ,end_time ,get_dates, latest_ship_date):
    get_dates=get_dates if get_dates else ''
    print('1231\n','delivery_date',delivery_date,'dates',dates ,
           'start_time',start_time ,'end_time',end_time ,'get_dates',get_dates,'latest_ship_date' ,latest_ship_date ,'\n')
    delivery_str_date, get_str_dates, start_str_time, end_str_time, latest_str_ship_date = '', '' ,'' ,'' ,''

    if delivery_date == '0000-00-00 00:00:00':
        return
    if delivery_date:
        if len(delivery_date) == len('2020-12-26 15:51') or len(delivery_date)  == len('2021-01-14 2:28'):
            delivery_date = '%s:00'%(delivery_date)
        delivery_str_date = datetime.datetime.strptime(delivery_date, "%Y-%m-%d %H:%M:%S")
    if dates:
        dates_str_date = datetime.datetime.strptime(dates, "%Y-%m-%dT%H-%M")
    if start_time:

        if len(start_time) == len('2021-01-04 21:55') or len(start_time) == len('2021-01-14 2:28'):
            start_time = '%s:00' % (start_time)
        start_str_time = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    if end_time:
        print(123,end_time, type(end_time))
        if len(end_time) > len('2021-01-05 17:01:00:00'):
            print(end_time.split(':00'))
            end_time = end_time.split(':00')[-2]
        if '.' in end_time:
            end_time = end_time.split('.')[0]
        if len(end_time) in [len('2021-01-04 12:49:00:')]:
            end_time = end_time.rstrip(':')
        if len(end_time) in [len('2021-01-05 16:53:00:00')]:
            end_time = end_time.rstrip(':00')
        if len(end_time) in [len('2021-01-04 21:55'), len('2021-01-21 9:58'), len('2021-1-26 9:38')]  :
            end_time = '%s:11' % (end_time)
        if len(end_time) in [len('2021-01-06 ')]:
            end_time = '%s12:10:00'%(end_time)

        print(end_time)

        end_str_time = datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        _dict['actual_date'] =end_str_time

    if 'T' in get_dates:
        print(123132, get_dates)
        get_dates = get_dates.replace('T', ' ').replace('Z', '')
        getz = get_dates.split(' ')
        if '-' in getz[-1]:
            two = getz[-1].replace('-',':')
            one = getz[0]
            get_dates = '%s %s'%(one,two)
            print(get_dates)
        if len(get_dates) in [len('2021-01-26 19-01')]:
            get_dates ='%s:00'%(get_dates)
        print(get_dates)
        get_str_dates = datetime.datetime.strptime(get_dates, "%Y-%m-%d %H:%M:%S")
    elif get_dates:
        print(get_dates)
        # if get_dates
        get_str_dates = datetime.datetime.strptime(get_dates, "%Y-%m-%d %H:%M:%S")
    if latest_ship_date:
        latest_ship_date = latest_ship_date.replace('Z', '')
        latest_str_ship_date = datetime.datetime.strptime(latest_ship_date, "%Y-%m-%dT%H:%M:%S")
        print(123, latest_str_ship_date)
        _dict['expected_date'] = latest_str_ship_date
    return delivery_str_date,get_str_dates,start_str_time ,end_str_time,latest_str_ship_date

def usa():
    usa_sql = "select * from manually_create_order where status='1';"
    usa_data = connect_mysql_master(usa_sql , type='dict')
    logistics_sql = "select * from oversea_location_data;"
    # 查询商品编码表

    commodity_sql = "select * from commodity_codes_zr;"
    logistics_data = connect_mysql2(logistics_sql, type='dict')
    commodity_data = connect_mysql(commodity_sql, type='dict')

    for  data_dict in usa_data:
        print(data_dict.get('content'),'\n', type(data_dict.get('content')))
        store, country = store_country_code(data_dict["station"], data_dict["country_code"], 'zh')

        _dict = {
            "dates": data_dict.get("dates"),
            "channel": channel,
            'logistics_information':data_dict.get('content'),
            "station": store,
            "country": country,
            "Amazon_id": data_dict.get("reference_ture"),
            "warehouse": "",
            "warehouse_name": '',
            "warehouse_code": data_dict.get("warehouse_code"),
            "logistic_supplier": "",
            "tracking_no": data_dict.get("tracking_no"),
            "sku": "",
            "product_name": "",
            "question_type": "",
            "all_days": "",
            "question_reason": " ",
            'status_name': '未处理',
            'expected_date':'',# 亚马逊语句送达时间
            'actual_date':'',# 快递实际到达日期
            'expected_days':'',# 预计花费天数,
            'delivery_status': '' ,# 配送状态
            }

        for index, logistics_dict in enumerate(logistics_data):
            if data_dict.get("warehouse_code") == logistics_dict["warehouse_code"]:
                _dict["warehouse_name"] = logistics_dict["warehouse_name"]
                _dict["warehouse"] = logistics_dict["warehouse_type"]
        _dict["sku"] = data_dict["sku"]

        for item in commodity_data:
            if item["sku"] in data_dict["sku"]:
                _dict["product_name"] = item["product_name"]
        if 'Z' in data_dict.get("tracking_no"):
            _dict["logistic_supplier"] = 'UPS'
        else:
            _dict["logistic_supplier"] = "FedEx"
        delivery_date = data_dict["delivery_date"] # 出库时间
        dates = data_dict['dates'] # 颜劲通过接口给快递下单的时间
        start_time = data_dict.get('start_time') # 取货时间
        end_time = data_dict.get('end_time')  # 快递送达时间
        get_dates = data_dict.get('get_dates') # 卖家创建时间
        latest_ship_date = data_dict.get('latest_ship_date') # 亚马逊预计最迟送达时间
        now_time = datetime.datetime.now()
        delivery_str_date, get_str_dates, start_str_time, end_str_time ,latest_str_ship_date = \
            time_change(_dict,delivery_date,dates ,start_time ,end_time ,get_dates, latest_ship_date)
        # 这是通过判断是否送达 来 他 是否查收
        # 判断出库是否超时  出库时间减去订单创建时间 大于2
        if delivery_date and get_dates:
            _dict = delivery_func(_dict, delivery_str_date, get_str_dates)
            if delivery_date and not start_time:
                print( now_time ,delivery_date)
                judge_date =( now_time - delivery_str_date).days
                if judge_date == 1:
                    _dict['warning_status'] = '距离货物仓库日期还有{0}天'.format(judge_date)
                _dict['status_name'] ='未处理'
        if start_time and latest_ship_date:
            _dict = start_func(_dict, start_str_time,latest_str_ship_date)
            if start_time and not end_time :
                judge_date = (now_time - start_str_time).days
                if judge_date == 1:
                    _dict['warning_status'] = '距离取货日期还有{0}天'.format(judge_date)

        if end_str_time and latest_ship_date: # 这单意味已经送达了
            # 判断是否
            # 是送达后是否配送超时
            print(end_str_time, latest_str_ship_date)
            _dict = change_func( _dict , end_str_time , latest_str_ship_date)

        _dict['delivery_status'] = '已送达' if end_time else '在配送'
        # 判断配送是否超时 end_time 实际配送时间， 预计送达时间

        _dict = time_out_judge(_dict, latest_ship_date , end_time ,end_str_time,latest_str_ship_date ,get_str_dates)
        conn_sql_fun(_dict)




# usa()



def ca():
    ca_sql  = "select * from manually_create_order_ups where status='1';"
    ca_data = connect_mysql_master(ca_sql , type='dict')
    logistics_sql = "select * from oversea_location_data;"
    # 查询商品编码表
    commodity_sql = "select * from commodity_codes_zr;"
    logistics_data = connect_mysql2(logistics_sql, type='dict')
    commodity_data = connect_mysql(commodity_sql, type='dict')

    for data_dict in ca_data:
        print(data_dict.get('content'), '\n', type(data_dict.get('content')))
        store, country = store_country_code(data_dict["station"], data_dict["country_code"], 'zh')

        _dict = {
            "dates": data_dict.get("dates"),
            "channel": channel,
            'logistics_information': data_dict.get('content'),
            "station": store,
            "country": country,
            "Amazon_id": data_dict.get("reference_ture"),
            "warehouse": "",
            "warehouse_name": '',
            "warehouse_code": data_dict.get("warehouse_code"),
            "logistic_supplier": "",
            "tracking_no": data_dict.get("tracking_no"),
            "sku": "",
            "product_name": "",
            "question_type": "",
            "all_days": "",
            "question_reason": " ",
            'status_name': '未处理',
            'expected_date': '',  # 亚马逊语句送达时间
            'actual_date': '',  # 快递实际到达日期
            'expected_days': '',  # 预计花费天数,
            'delivery_status': '',  # 配送状态
        }

        for index, logistics_dict in enumerate(logistics_data):
            if data_dict.get("warehouse_code") == logistics_dict["warehouse_code"]:
                _dict["warehouse_name"] = logistics_dict["warehouse_name"]
                _dict["warehouse"] = logistics_dict["warehouse_type"]
        _dict["sku"] = data_dict["sku"]

        for item in commodity_data:
            if item["sku"] in data_dict["sku"]:
                _dict["product_name"] = item["product_name"]
        if 'Z' in data_dict.get("tracking_no"):
            _dict["logistic_supplier"] = 'UPS'
        else:
            _dict["logistic_supplier"] = "FedEx"
        delivery_date = data_dict["delivery_date"]  # 出库时间
        dates = data_dict['dates']  # 颜劲通过接口给快递下单的时间
        start_time = data_dict.get('start_time')  # 取货时间
        end_time = data_dict.get('end_time')  # 快递送达时间
        get_dates = data_dict.get('get_dates')  # 卖家创建时间
        latest_ship_date = data_dict.get('latest_ship_date')  # 亚马逊预计最迟送达时间
        now_time = datetime.datetime.now()
        delivery_str_date, get_str_dates, start_str_time, end_str_time, latest_str_ship_date = \
            time_change(_dict, delivery_date, dates, start_time, end_time, get_dates, latest_ship_date)
        # 这是通过判断是否送达 来 他 是否查收
        # 判断出库是否超时  出库时间减去订单创建时间 大于2
        if delivery_date and get_dates:
            _dict = delivery_func(_dict, delivery_str_date, get_str_dates)
            if delivery_date and not start_time:
                print(now_time, delivery_date)
                judge_date = (now_time - delivery_str_date).days
                if judge_date == 1:
                    _dict['warning_status'] = '距离货物仓库日期还有{0}天'.format(judge_date)
                _dict['status_name'] = '未处理'
        if start_time and latest_ship_date:
            _dict = start_func(_dict, start_str_time, latest_str_ship_date)
            if start_time and not end_time:
                judge_date = (now_time - start_str_time).days
                if judge_date == 1:
                    _dict['warning_status'] = '距离取货日期还有{0}天'.format(judge_date)

        if end_str_time and latest_ship_date:  # 这单意味已经送达了
            # 判断是否
            # 是送达后是否配送超时
            print(end_str_time, latest_str_ship_date)
            _dict = change_func(_dict, end_str_time, latest_str_ship_date)

        _dict['delivery_status'] = '已送达' if end_time else '在配送'
        # 判断配送是否超时 end_time 实际配送时间， 预计送达时间

        _dict = time_out_judge(_dict, latest_ship_date, end_time, end_str_time, latest_str_ship_date, get_str_dates)
        conn_sql_fun(_dict)




def eu():
    eu_sql = "select * from manually_create_order_yc where status='1';"
    eu_data = connect_mysql_master(eu_sql,type='dict')
    logistics_sql = "select * from oversea_location_data;"
    # 查询商品编码表
    commodity_sql = "select * from commodity_codes_zr;"
    logistics_data = connect_mysql2(logistics_sql, type='dict')
    commodity_data = connect_mysql(commodity_sql, type='dict')
    # try:
    for data_dict in eu_data:

        store, country = store_country_code(data_dict["station"], data_dict["country_code"], 'zh')

        _dict = {
            "dates": data_dict.get("get_dates"),
            "channel": channel,
            "station": store,
            "country": country,
            "Amazon_id": data_dict.get("reference_ture"),
            "warehouse": "--",
            "warehouse_name": '--',
            "warehouse_code": data_dict.get("warehouse_code"),
            "logistic_supplier": "--",
            "tracking_no": data_dict.get("tracking_no"),
            "sku": "--",
            "product_name": "--",
            "question_type": "--",
            "all_days": "--",
            "question_reason": "--",
            'status_name': '未处理'
        }
        for index, logistics_dict in enumerate(logistics_data):
            if data_dict.get("warehouse_code") == logistics_dict["warehouse_code"]:
                _dict["warehouse_name"] = logistics_dict["warehouse_name"]
                _dict["warehouse"] = logistics_dict["warehouse_type"]

        _dict["sku"] = data_dict["product_sku"]

        for item in commodity_data:
            if item["sku"] in data_dict["product_sku"]:
                _dict["product_name"] = item["product_name"]
        if  data_dict.get("shipping_method"):
            if 'DHL' in data_dict.get("shipping_method"):
                _dict["logistic_supplier"] = 'DHL'
            elif 'GLS' in data_dict.get("shipping_method"):
                _dict["logistic_supplier"] = 'GLS'
            elif 'DPD' in data_dict.get("shipping_method"):
                _dict["logistic_supplier"] = 'DPD'
            elif 'YODEL' in data_dict.get("shipping_method"):
                _dict["logistic_supplier"] = 'YODEL'
            elif 'D29' in data_dict.get("shipping_method"):
                _dict["logistic_supplier"] = 'DPD'
                # _dict["logistic_supplier"] = 'DPD'
                # _dict["logistic_supplier"] = "FedEx"
        delivery_date = data_dict["delivery_date"]  # 出库时间
        dates = data_dict['dates']  # 颜劲通过接口给快递下单的时间
        start_time = data_dict.get('start_time')  # 取货时间
        end_time = data_dict.get('end_time')  # 快递送达时间
        get_dates = data_dict.get('get_dates')  # 卖家创建时间
        latest_ship_date = data_dict.get('latest_ship_date')  # 亚马逊预计最迟送达时间
        now_time = datetime.datetime.now()
        print('delivery_date', delivery_date, '-dates', dates, '-start_time', start_time,
              '-end_time ', end_time, '-get_dates', get_dates, '-latest_ship_date', latest_ship_date)
        delivery_str_date, get_str_dates, start_str_time, end_str_time, latest_str_ship_date = \
            time_change(_dict, delivery_date, dates, start_time, end_time, get_dates, latest_ship_date)
        # 这是通过判断是否送达 来 他 是否查收
        # 判断出库是否超时  出库时间减去订单创建时间 大于2
        if delivery_str_date and get_str_dates:
            _dict = delivery_func(_dict, delivery_str_date, get_str_dates)
            if delivery_date and not start_time:
                print(now_time, delivery_date)
                judge_date = (now_time - delivery_str_date).days
                if judge_date == 1:
                    _dict['warning_status'] = '距离货物仓库日期还有{0}天'.format(judge_date)
                _dict['status_name'] = '未处理'
        if start_time and latest_ship_date:
            _dict = start_func(_dict, start_str_time, latest_str_ship_date)
            if start_time and not end_time:
                judge_date = (now_time - start_str_time).days
                if judge_date == 1:
                    _dict['warning_status'] = '距离取货日期还有{0}天'.format(judge_date)

        if end_str_time and latest_ship_date:  # 这单意味已经送达了
            # 判断是否
            # 是送达后是否配送超时
            print(end_str_time, latest_str_ship_date)
            _dict = change_func(_dict, end_str_time, latest_str_ship_date)

        _dict['delivery_status'] = '已送达' if end_time else '在配送'
        # 判断配送是否超时 end_time 实际配送时间， 预计送达时间

        _dict = time_out_judge(_dict, latest_ship_date, end_time, end_str_time, latest_str_ship_date,  get_str_dates)
        conn_sql_fun(_dict)
    # except:pass
# usa()
# ca()
eu()