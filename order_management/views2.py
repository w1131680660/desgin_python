import json
import time
from datetime import date, timedelta
import pymysql
import pandas as pd
import requests
from django.http import JsonResponse
from settings import conf_fun

# # 连接数据库
# def connect_mysql1(sql_text, dbs='operation', type='tuple'):
#     conn = pymysql.Connect(host='172.16.0.6', port=3306, user='beyoungsql', passwd='By1590123!@', db=dbs)
#
#     if type == 'tuple':
#         cursor = conn.cursor()
#     else:
#         cursor = conn.cursor(pymysql.cursors.DictCursor)
#     cursor.execute(sql_text)
#     response = cursor.fetchall()
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return response
#
#
# def connect_mysql(sql_text, dbs='order', type='tuple'):
#     conn = pymysql.Connect(host='106.53.250.215', port=3306, user='beyoungsql', passwd='Bymy2021.', db=dbs)
#
#     if type == 'tuple':
#         cursor = conn.cursor()
#     else:
#         cursor = conn.cursor(pymysql.cursors.DictCursor)
#     cursor.execute(sql_text)
#     response = cursor.fetchall()
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return response


def upload_advertising_report(request):
    files = request.FILES.get('files')
    area = request.POST.get('area')
    area1 = request.POST.get('area1')
    status = request.POST.get('status')
    times = request.POST.get('times')

    urls = 'https://www.beyoung.group/advertising_report_upload/'

    date_date = date(*map(int, times.split('_')))
    if status != '广告报告':
        year = str(date_date + timedelta(days=1)).split('-')[0]
        month = str(date_date + timedelta(days=1)).split('-')[1]
        day = str(date_date + timedelta(days=1)).split('-')[2]
    else:
        year = str(date_date).split('-')[0]
        month = str(date_date).split('-')[1]
        day = str(date_date).split('-')[2]
    if status == '广告报告' or status =='不完整广告报告':
        if status == '广告报告':
            filename1 = area + '_' + times + '.xls'
        else:
            filename1 = area + '_' + times + '_zd.xls'
        with open('/home/static/advertising_report/' + filename1, "wb") as f:
            for line in files:
                f.write(line)
        df = pd.read_excel('/home/static/advertising_report/' + filename1)
        try:
            df = df[['广告SKU', '广告ASIN', '展现量', '点击量', '点击率(CTR)', '花费']]
            df.columns = ['SKU', 'ASIN', '展现量', '点击量', '点击率(CTR)', '花费']
        except:
            pass
        df.to_excel('/home/static/advertising_report/' + filename1)

    else:
        if '英国' in area1 or '法国' in area1 or '德国' in area1 or '意大利' in area1 or '西班牙' in area1:
            area1 = area1[:2] + '欧洲'
        filename1 = area1 + '_' + status + '_' + year + '_' + month + '_' + day + '.txt'
        with open('/home/static/advertising_report/' + filename1, "wb") as f:
            for line in files:
                f.write(line)
    data = {"times": times, "area": area}
    with open('/home/static/advertising_report/' + filename1, "rb") as f:
        res = requests.post(url=urls, files={'files': f}, data=data)
    print(res)
    res_data = json.loads(res.text)
    return JsonResponse(res_data)


# 更新出库日期
def update_delivery_date(request):
    file = request.FILES.get('files')
    file_path = '/home/by_operate/static/data/delivery_date/' + file.name
    with open(file_path, "wb") as f:
        for line in file:
            f.write(line)

    df = pd.read_excel(file_path)

    for i in range(df.shape[0]):
        if df.iloc[i, 3] in ['UKPJ', 'DEPJ'] and df.iloc[i, 30] not in ['', '0000-00-00 00:00:00']:
            sql = "select id,delivery_date from manually_create_order_yc where reference_no='{}'"
            sql = sql.format(df.iloc[i, 10])
            res = conf_fun.connect_mysql_or(sql)
            if res[0][0] != str(df.iloc[i, 30]):
                sql = "update manually_create_order_yc set delivery_date='{}' where reference_no='{}'"
                sql = sql.format(str(df.iloc[i, 30]), df.iloc[i, 10])
        elif df.iloc[i, 3] in ['PJWL', 'NVPJ', 'NJPJ'] and df.iloc[i, 30] not in ['', '0000-00-00 00:00:00']:
            sql = "select id,delivery_date from manually_create_order where customer_order_number='{}'"
            sql = sql.format(df.iloc[i, 10])
            res = conf_fun.connect_mysql_or(sql)
            if res[0][0] != str(df.iloc[i, 30]):
                sql = "update manually_create_order set delivery_date='{}', where customer_order_number='{}'"
                sql = sql.format(str(df.iloc[i, 30]), df.iloc[i, 10])
        else:
            continue
        conf_fun.connect_mysql_or(sql)
    return JsonResponse({"code": 200, "msg": "更新完成!"})