import datetime
import pymysql
import json
from django.http import JsonResponse,FileResponse


# 获取问题订单
# 连接数据库
def connect_mysql(sql_text, dbs='order', type='tuple'):
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


def connect_mysql1(sql_text, dbs='product_supplier', type='tuple'):
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


bad_order_data = []

# 查询物流系统海外仓数据表
select = "select * from oversea_location_data where warehouse_code is not NULL;"
data = connect_mysql1(select,type='dict')


# 查询欧洲 发货成功后1小时还未出回传单号的订单
sql1 = "select * from manually_create_order_yc where order_code is not NULL and tracking_no is NULL;"
res1 = connect_mysql(sql1,type='dict')
for item1 in res1:
    # 查询问题订单表中此订单是否存在
    select1 = "select * from problem_data where orderid='%s';"%(item1["reference_ture"])
    result = connect_mysql(select1)
    if len(result) == 0:
        if item1["dates"] is not None:
            now = datetime.datetime.now()
            _hours = (now - datetime.datetime.strptime(item1["dates"],"%Y-%m-%dT%H-%M")).seconds/60/60
            if _hours > 1:
                warehouse1 = item1["warehouse_code"]
                for j in data:
                    if item1["warehouse_code"] == j["warehouse_code"]:
                        warehouse1 = j["warehouse_name"]
                        break
                # 超时
                _dict = {
                    "sysorder_id": item1["order_code"],
                    "orderid": item1["reference_ture"],
                    "common_carrier": warehouse1,
                    "sku": item1["product_sku"],
                    "country": item1["country_code"],
                    "recipient": item1["name"],
                    "reason": "超过1小时未出回传单号",
                    "state": '0'
                }
                bad_order_data.append(_dict)

# 查询欧洲疑似丢件订单
sql2 = "select * from manually_create_order_yc where status='1' and now_noticias like'%货件准备交给%' and latest_logistics_date is NULL;"
res2 = connect_mysql(sql2,type='dict')
for item2 in res2:
    # 查询问题订单表中此订单是否存在
    select1 = "select * from problem_data where orderid='%s';"%(item1["reference_ture"])
    result = connect_mysql(select1)
    if len(result) == 0:
        warehouse2 = item2["warehouse_code"]
        for j in data:
            if item2["warehouse_code"] == j["warehouse_code"]:
                warehouse2 = j["warehouse_name"]
                break

        _dict = {
            "sysorder_id": item2["order_code"],
            "orderid": item2["reference_ture"],
            "common_carrier": warehouse2,
            "sku": item2["product_sku"],
            "country": item2["country_code"],
            "recipient": item2["name"],
            "reason": "疑似丢件",
            "state": '0'
        }
        bad_order_data.append(_dict)

# 查询美国 发货成功后1小时还未出回传单号的订单
sql3 = "select * from manually_create_order where sysOrderId is not NULL and tracking_no is NULL;"
res3 = connect_mysql(sql3,type='dict')
for item3 in res3:
    # 查询问题订单表中此订单是否存在
    select1 = "select * from problem_data where orderid='%s';"%(item1["reference_ture"])
    result = connect_mysql(select1)
    if len(result) == 0:
        if item3["dates"] is not None:
            now = datetime.datetime.now()
            _hours = (now - datetime.datetime.strptime(item3["dates"],"%Y-%m-%dT%H-%M")).seconds/60/60
            if _hours > 1:
                warehous3 = item3["warehouse_code"]
                for j in data:
                    if item3["warehouse_code"] == j["warehouse_code"]:
                        warehous3 = j["warehouse_name"]
                        break

                # 超时
                _dict = {
                    "sysorder_id": item3["sysOrderId"],
                    "orderid": item3["reference_ture"],
                    "common_carrier": warehous3,
                    "sku": item3["sku"],
                    "country": item3["country_code"],
                    "recipient": item3["contact_name"],
                    "reason": "超过1小时未出回传单号",
                    "state": '0'
                }
                bad_order_data.append(_dict)

# 查询欧洲疑似丢件订单
sql4 = "select * from manually_create_order_yc where status='1' and now_noticias like'%货件准备交给%' and latest_logistics_date is NULL;"
res4 = connect_mysql(sql4,type='dict')
for item4 in res4:
    # 查询问题订单表中此订单是否存在
    select1 = "select * from problem_data where orderid='%s';"%(item1["reference_ture"])
    result = connect_mysql(select1)
    if len(result) == 0:
        warehous4 = item4["warehouse_code"]
        for j in data:
            if item4["warehouse_code"] == j["warehouse_code"]:
                warehous4 = j["warehouse_name"]
                break

        _dict = {
            "sysorder_id": item4["sysOrderId"],
            "orderid": item4["reference_ture"],
            "common_carrier": warehous4,
            "sku": item4["sku"],
            "country": item4["country_code"],
            "recipient": item4["contact_name"],
            "reason": "疑似丢件",
            "state": '0'
        }
        bad_order_data.append(_dict)

# 存入问题订单表
insert_sql = "insert into problem_data (sysorder_id,orderid,common_carrier,sku,country,recipient,reason,state) value "
for i in bad_order_data:
    insert_sql += "('" + i["sysorder_id"] + "','" + i["orderid"] + "','" + i["common_carrier"] + "','" + \
                  i["sku"] + "','" + i["country"] + "','" + i["recipient"] + "','" + i["reason"] + "','" + i["state"] + "'),"

insert_sql = insert_sql[:-1]

connect_mysql(insert_sql)


